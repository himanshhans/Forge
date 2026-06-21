from django.contrib import admin

from .models import AvatarGeneration, Portfolio, PortfolioAnalytics


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = (
        "title", "slug", "niche", "user",
        "generation_status", "deployment_status", "is_featured", "created_at",
    )
    list_filter = ("niche", "generation_status", "deployment_status", "is_featured", "in_showcase")
    search_fields = ("title", "slug", "subdomain", "user__username")
    readonly_fields = ("created_at", "updated_at")


@admin.register(AvatarGeneration)
class AvatarGenerationAdmin(admin.ModelAdmin):
    list_display = ("portfolio", "avatar_type", "provider", "success", "cost_cents", "created_at")
    list_filter = ("avatar_type", "provider", "success")


@admin.register(PortfolioAnalytics)
class PortfolioAnalyticsAdmin(admin.ModelAdmin):
    list_display = ("portfolio", "date", "views", "unique_visitors")
    list_filter = ("date",)
