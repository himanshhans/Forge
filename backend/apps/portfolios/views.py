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
