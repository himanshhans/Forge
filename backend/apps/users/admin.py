from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "plan", "clerk_user_id", "created_at")
    search_fields = ("username", "email", "clerk_user_id")
    list_filter = ("plan", "is_public")
