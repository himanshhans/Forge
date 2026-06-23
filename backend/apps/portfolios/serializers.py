import json

from rest_framework import serializers

from .models import Portfolio
from .niches import get_niche

# Input caps (cost + prompt-injection guard)
MAX_QUESTIONNAIRE_BYTES = 10_240   # ~10 KB
MAX_AVATAR_DESC_CHARS = 500
MAX_BIO_CHARS = 1000


class PortfolioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = (
            "id", "title", "niche", "slug", "subdomain", "published_url",
            "custom_domain", "custom_domain_status", "has_custom_domain",
            "generation_status", "deployment_status", "created_at",
        )


class PortfolioDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = (
            "id", "title", "slug", "subdomain", "custom_domain", "niche",
            "questionnaire", "generated_html", "generated_css", "generated_metadata",
            "avatar_type", "avatar_url", "intro_card", "intro_card_features",
            "published_url", "has_custom_domain", "custom_domain_status",
            "generation_status", "deployment_status", "last_deployed_at",
            "views", "is_featured", "in_showcase", "llm_provider",
            "created_at", "updated_at",
        )
        read_only_fields = (
            "id", "slug", "subdomain", "generated_html", "generated_css",
            "generated_metadata", "published_url", "generation_status",
            "deployment_status", "last_deployed_at", "views", "is_featured",
            "llm_provider", "created_at", "updated_at",
        )


class GenerateSerializer(serializers.Serializer):
    AVATAR_TYPES = ["photo", "3d", "2d_illustrated", "ai_photo"]

    niche = serializers.CharField()
    questionnaire = serializers.JSONField()
    avatar_type = serializers.ChoiceField(choices=AVATAR_TYPES, required=False, default="photo")
    avatar_data = serializers.JSONField(required=False, default=dict)
    intro_card = serializers.JSONField(required=False, default=dict)

    def validate_niche(self, value):
        if not get_niche(value):
            raise serializers.ValidationError("Unknown niche")
        return value

    def validate_questionnaire(self, value):
        if len(json.dumps(value).encode()) > MAX_QUESTIONNAIRE_BYTES:
            raise serializers.ValidationError("Questionnaire too large (max 10 KB)")
        return value

    def validate_avatar_data(self, value):
        desc = value.get("description", "")
        if len(desc) > MAX_AVATAR_DESC_CHARS:
            raise serializers.ValidationError("Avatar description too long (max 500 chars)")
        return value

    def validate_intro_card(self, value):
        bio = value.get("bio", "")
        if len(bio) > MAX_BIO_CHARS:
            raise serializers.ValidationError("Bio too long (max 1000 chars)")
        return value


class RegenerateSerializer(serializers.Serializer):
    SECTIONS = ["hero", "projects", "all"]
    niche_section = serializers.ChoiceField(choices=SECTIONS, default="all")


class SiteSerializer(serializers.ModelSerializer):
    """Public render payload for wildcard-serve (live portfolios only)."""

    class Meta:
        model = Portfolio
        fields = (
            "subdomain", "title", "niche",
            "generated_html", "generated_css", "generated_metadata",
        )
