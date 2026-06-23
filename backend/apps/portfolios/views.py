from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .limits import check_can_create_portfolio
from .models import Portfolio
from .serializers import (
    GenerateSerializer,
    PortfolioDetailSerializer,
    PortfolioListSerializer,
    RegenerateSerializer,
)
from .tasks import generate_portfolio_task
from .throttles import DeployThrottle, GenerateThrottle
from .utils import unique_slug, unique_subdomain


class PortfolioViewSet(viewsets.ModelViewSet):
    """User-scoped CRUD + generate/regenerate/deploy/status."""

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return PortfolioListSerializer
        return PortfolioDetailSerializer

    def get_throttles(self):
        if self.action == "generate":
            return [GenerateThrottle()]
        if self.action == "deploy":
            return [DeployThrottle()]
        return super().get_throttles()

    @action(detail=False, methods=["post"])
    def generate(self, request):
        ser = GenerateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        # Free-tier enforcement (service layer, not DB constraint)
        check_can_create_portfolio(request.user)

        intro_card = data["intro_card"]
        base = intro_card.get("name") or request.user.username
        avatar_data = data["avatar_data"]

        portfolio = Portfolio.objects.create(
            user=request.user,
            title=intro_card.get("name", ""),
            slug=unique_slug(base),
            subdomain=unique_subdomain(base),
            niche=data["niche"],
            questionnaire=data["questionnaire"],
            avatar_type=data["avatar_type"],
            avatar_url=avatar_data.get("file_url", ""),
            avatar_generation_data=avatar_data,
            intro_card=intro_card,
            generation_status="text_pending",
        )

        # Kick async pipeline (eager in dev).
        generate_portfolio_task.delay(str(portfolio.id))

        portfolio.refresh_from_db()
        return Response(
            PortfolioDetailSerializer(portfolio).data,
            status=status.HTTP_202_ACCEPTED,
        )

    @action(detail=True, methods=["post"])
    def regenerate(self, request, pk=None):
        portfolio = self.get_object()
        RegenerateSerializer(data=request.data).is_valid(raise_exception=True)
        portfolio.generation_status = "text_pending"
        portfolio.save(update_fields=["generation_status"])
        generate_portfolio_task.delay(str(portfolio.id))
        portfolio.refresh_from_db()
        return Response(PortfolioDetailSerializer(portfolio).data, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["post"])
    def deploy(self, request, pk=None):
        from services.publisher import publish_portfolio
        portfolio = self.get_object()
        url = publish_portfolio(portfolio)
        return Response({
            "portfolio_id": str(portfolio.id),
            "live_url": url,
            "deployment_status": portfolio.deployment_status,
        })

    @action(detail=True, methods=["get"], url_path="status")
    def status_view(self, request, pk=None):
        portfolio = self.get_object()
        return Response({
            "generation_status": portfolio.generation_status,
            "deployment_status": portfolio.deployment_status,
            "published_url": portfolio.published_url,
            "avatar_url": portfolio.avatar_url,
        })

    # --- Custom domain ---
    @action(detail=True, methods=["post"], url_path="domain")
    def add_domain(self, request, pk=None):
        from services.domains import dns_instructions, is_valid_domain, make_token, normalize_domain
        portfolio = self.get_object()
        domain = normalize_domain(request.data.get("domain", ""))
        if not is_valid_domain(domain):
            return Response({"detail": "Enter a valid domain (e.g. me.example.com)."},
                            status=status.HTTP_400_BAD_REQUEST)
        if Portfolio.objects.filter(custom_domain=domain).exclude(pk=portfolio.pk).exists():
            return Response({"detail": "That domain is already in use."},
                            status=status.HTTP_409_CONFLICT)
        portfolio.custom_domain = domain
        portfolio.custom_domain_token = make_token()
        portfolio.custom_domain_status = "pending"
        portfolio.has_custom_domain = False
        portfolio.save(update_fields=[
            "custom_domain", "custom_domain_token", "custom_domain_status", "has_custom_domain",
        ])
        return Response({
            "domain": domain,
            "status": "pending",
            "dns": dns_instructions(domain, portfolio.custom_domain_token),
        })

    @action(detail=True, methods=["post"], url_path="domain/verify")
    def verify_domain(self, request, pk=None):
        from services.domains import provision_ssl, verify_txt
        portfolio = self.get_object()
        if not portfolio.custom_domain:
            return Response({"detail": "No domain to verify."}, status=status.HTTP_400_BAD_REQUEST)
        if not verify_txt(portfolio.custom_domain, portfolio.custom_domain_token):
            portfolio.custom_domain_status = "failed"
            portfolio.save(update_fields=["custom_domain_status"])
            return Response(
                {"status": "failed", "detail": "TXT record not found yet. DNS can take a few minutes."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        provision_ssl(portfolio.custom_domain)
        portfolio.has_custom_domain = True
        portfolio.custom_domain_status = "verified"
        portfolio.published_url = f"https://{portfolio.custom_domain}"
        portfolio.save(update_fields=["has_custom_domain", "custom_domain_status", "published_url"])
        return Response({"status": "verified", "published_url": portfolio.published_url})

    @action(detail=True, methods=["delete"], url_path="domain/remove")
    def remove_domain(self, request, pk=None):
        portfolio = self.get_object()
        portfolio.custom_domain = None
        portfolio.custom_domain_token = ""
        portfolio.custom_domain_status = ""
        portfolio.has_custom_domain = False
        portfolio.published_url = f"https://{portfolio.subdomain}.{settings.PORTFOLIO_WILDCARD_DOMAIN}"
        portfolio.save(update_fields=[
            "custom_domain", "custom_domain_token", "custom_domain_status",
            "has_custom_domain", "published_url",
        ])
        return Response({"status": "removed"})
