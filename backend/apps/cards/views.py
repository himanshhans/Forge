import uuid

from django.conf import settings
from django.db.models import F
from django.http import HttpResponse
from django.utils.text import slugify
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from services.contact_card import build_vcard, generate_card
from .models import ContactCard
from .serializers import (
    CardCreateSerializer,
    CardSiteSerializer,
    CardSummarySerializer,
    ContactCardSerializer,
)


def _unique_slug(base: str) -> str:
    root = slugify(base) or "card"
    candidate = root
    while ContactCard.objects.filter(slug=candidate).exists():
        candidate = f"{root}-{uuid.uuid4().hex[:5]}"
    return candidate


def _check_card_limit(user):
    if getattr(user, "is_pro", False):
        return
    if ContactCard.objects.filter(user=user).count() >= settings.FREE_PLAN_MAX_INTRO_CARDS:
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied(
            f"Free plan limit reached ({settings.FREE_PLAN_MAX_INTRO_CARDS} contact card). Upgrade to Pro."
        )


class ContactCardViewSet(viewsets.ModelViewSet):
    serializer_class = ContactCardSerializer

    def get_queryset(self):
        return ContactCard.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return CardSummarySerializer if self.action == "list" else ContactCardSerializer

    @action(detail=False, methods=["post"])
    def generate(self, request):
        ser = CardCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        _check_card_limit(request.user)

        slug = _unique_slug(data["name"])
        published_url = f"{settings.SITE_BASE_URL}/c/{slug}"
        card = ContactCard(
            user=request.user, slug=slug, published_url=published_url,
            name=data["name"], headline=data["headline"], bio=data["bio"],
            avatar_url=data["avatar_url"], email=data["email"],
            phone=data["phone"], location=data["location"], links=data["links"],
        )
        rendered = generate_card(card, published_url)
        card.generated_html = rendered["html"]
        card.generated_css = rendered["css"]
        card.design = rendered["design"]
        card.save()
        return Response(ContactCardSerializer(card).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def regenerate(self, request, pk=None):
        """Reroll the random design (content unchanged)."""
        card = self.get_object()
        rendered = generate_card(card, card.published_url)
        card.generated_html = rendered["html"]
        card.generated_css = rendered["css"]
        card.design = rendered["design"]
        card.save(update_fields=["generated_html", "generated_css", "design", "updated_at"])
        return Response(ContactCardSerializer(card).data)


class CardSiteView(generics.RetrieveAPIView):
    """Public: rendered card by slug (published only)."""
    serializer_class = CardSiteSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field = "slug"

    def get_queryset(self):
        return ContactCard.objects.filter(is_published=True)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        ContactCard.objects.filter(pk=obj.pk).update(views=F("views") + 1)
        return super().retrieve(request, *args, **kwargs)


class CardVCardView(generics.RetrieveAPIView):
    """Public: download .vcf by slug."""
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field = "slug"

    def get_queryset(self):
        return ContactCard.objects.filter(is_published=True)

    def retrieve(self, request, *args, **kwargs):
        card = self.get_object()
        resp = HttpResponse(build_vcard(card), content_type="text/vcard")
        resp["Content-Disposition"] = f'attachment; filename="{card.slug}.vcf"'
        return resp
