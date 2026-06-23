from rest_framework import serializers

from .models import ContactCard

MAX_LINKS = 8
MAX_BIO = 600


class ContactCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactCard
        fields = (
            "id", "slug", "name", "headline", "bio", "avatar_url", "links",
            "email", "phone", "location", "published_url", "is_published",
            "design", "views", "created_at",
        )
        read_only_fields = (
            "id", "slug", "published_url", "design", "views", "created_at",
        )


class CardCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    headline = serializers.CharField(max_length=160, required=False, allow_blank=True, default="")
    bio = serializers.CharField(max_length=MAX_BIO, required=False, allow_blank=True, default="")
    avatar_url = serializers.CharField(max_length=500, required=False, allow_blank=True, default="")
    email = serializers.EmailField(required=False, allow_blank=True, default="")
    phone = serializers.CharField(max_length=40, required=False, allow_blank=True, default="")
    location = serializers.CharField(max_length=120, required=False, allow_blank=True, default="")
    links = serializers.ListField(child=serializers.DictField(), required=False, default=list)

    def validate_links(self, value):
        if len(value) > MAX_LINKS:
            raise serializers.ValidationError(f"Too many links (max {MAX_LINKS})")
        cleaned = []
        for link in value:
            url = (link.get("url") or "").strip()
            if not url:
                continue
            cleaned.append({"label": (link.get("label") or url)[:60], "url": url[:500]})
        return cleaned


class CardSiteSerializer(serializers.ModelSerializer):
    """Public render payload."""
    class Meta:
        model = ContactCard
        fields = ("slug", "name", "generated_html", "generated_css")


class CardSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactCard
        fields = ("id", "slug", "name", "headline", "published_url", "views", "created_at")
