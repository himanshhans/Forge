import uuid

from django.conf import settings
from django.db import models


class ContactCard(models.Model):
    """A shareable digital contact card (served at /c/{slug})."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cards"
    )
    slug = models.SlugField(max_length=100, unique=True)

    # Content
    name = models.CharField(max_length=120)
    headline = models.CharField(max_length=160, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.CharField(max_length=500, blank=True)
    links = models.JSONField(default=list, blank=True)   # [{"label","url"}]
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    location = models.CharField(max_length=120, blank=True)

    # Render
    design = models.JSONField(default=dict, blank=True)  # design brief used
    generated_html = models.TextField(blank=True)
    generated_css = models.TextField(blank=True)

    # Publish
    is_published = models.BooleanField(default=True)
    published_url = models.CharField(max_length=255, blank=True)

    views = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "contact_cards"
        indexes = [models.Index(fields=["user"]), models.Index(fields=["slug"])]

    def __str__(self):
        return f"{self.name} ({self.slug})"
