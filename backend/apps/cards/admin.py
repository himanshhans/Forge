from django.contrib import admin

from .models import ContactCard


@admin.register(ContactCard)
class ContactCardAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "user", "is_published", "views", "created_at")
    search_fields = ("name", "slug", "user__username")
    list_filter = ("is_published",)
