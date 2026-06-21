from rest_framework import serializers

from .models import ShowcaseEntry


class ShowcaseEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowcaseEntry
        fields = (
            "portfolio_id", "username", "title", "niche",
            "thumbnail_url", "deployed_url", "featured", "view_count", "created_at",
        )
