from rest_framework import serializers

from apps.portfolios.models import Portfolio


class ShowcaseEntrySerializer(serializers.ModelSerializer):
    """Public gallery entry, projected from a Portfolio."""
    portfolio_id = serializers.UUIDField(source="id")
    username = serializers.CharField(source="user.username")
    thumbnail_url = serializers.CharField(source="avatar_url")
    deployed_url = serializers.CharField(source="published_url")
    featured = serializers.BooleanField(source="is_featured")
    view_count = serializers.IntegerField(source="views")

    class Meta:
        model = Portfolio
        fields = (
            "portfolio_id", "username", "title", "niche",
            "thumbnail_url", "deployed_url", "featured", "view_count", "created_at",
        )
