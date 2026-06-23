import uuid

from django.conf import settings
from django.db import models


class Niche(models.TextChoices):
    INDIE_HACKER = "indie_hacker", "Indie Hacker"
    FREELANCER = "freelancer", "Freelancer"
    CREATOR = "creator", "Creator"
    COACH = "coach", "Coach/Consultant"
    AGENCY = "agency", "Agency"


class Portfolio(models.Model):
    AVATAR_TYPES = [
        ("photo", "Photo"),
        ("3d", "3D"),
        ("2d_illustrated", "2D Illustrated"),
        ("ai_photo", "AI Photo"),
    ]
    # Granular async pipeline status
    GEN_STATUS = [
        ("text_pending", "Text Pending"),
        ("text_done", "Text Done"),
        ("avatar_pending", "Avatar Pending"),
        ("avatar_done", "Avatar Done"),
        ("publishing", "Publishing"),
        ("live", "Live"),
        ("failed", "Failed"),
    ]
    DEPLOY_STATUS = [
        ("pending", "Pending"),
        ("live", "Live"),
        ("failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolios",
    )
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    subdomain = models.CharField(max_length=100, unique=True)
    custom_domain = models.CharField(max_length=255, blank=True, null=True)

    # Niche
    niche = models.CharField(max_length=50, choices=Niche.choices)
    niche_config = models.JSONField(default=dict, blank=True)

    # Generation
    questionnaire = models.JSONField(default=dict, blank=True)
    generated_html = models.TextField(blank=True)   # stored in DB (wildcard-serve)
    generated_css = models.TextField(blank=True)
    generated_metadata = models.JSONField(default=dict, blank=True)  # SEO/OG/JSON-LD

    # Avatar & intro card
    avatar_type = models.CharField(max_length=50, choices=AVATAR_TYPES, blank=True)
    avatar_url = models.CharField(max_length=500, blank=True)
    avatar_generation_data = models.JSONField(default=dict, blank=True)
    intro_card = models.JSONField(default=dict, blank=True)
    intro_card_features = models.JSONField(default=dict, blank=True)

    # Serving / deployment (Model B wildcard-serve default)
    published_url = models.CharField(max_length=255, blank=True)
    has_custom_domain = models.BooleanField(default=False)
    custom_domain_status = models.CharField(max_length=50, blank=True)  # pending/verified/failed
    custom_domain_token = models.CharField(max_length=64, blank=True)  # TXT challenge value
    netlify_site_id = models.CharField(max_length=255, blank=True)

    generation_status = models.CharField(
        max_length=50, choices=GEN_STATUS, default="text_pending"
    )
    deployment_status = models.CharField(
        max_length=50, choices=DEPLOY_STATUS, default="pending"
    )
    last_deployed_at = models.DateTimeField(null=True, blank=True)

    # Stats
    views = models.IntegerField(default=0)
    visits = models.IntegerField(default=0)

    # Showcase
    is_featured = models.BooleanField(default=False)
    featured_at = models.DateTimeField(null=True, blank=True)
    in_showcase = models.BooleanField(default=True)
    showcase_rank = models.IntegerField(null=True, blank=True)

    llm_provider = models.CharField(max_length=50, default="groq")  # groq, together

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "portfolios"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["niche"]),
            models.Index(fields=["in_showcase"]),
        ]

    def __str__(self):
        return f"{self.title or self.slug} [{self.niche}]"


class AvatarGeneration(models.Model):
    """History of avatar gen calls — cost tracking + iteration."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="avatar_generations"
    )
    avatar_type = models.CharField(max_length=50)  # 3d / 2d_illustrated / ai_photo
    provider = models.CharField(max_length=50)     # readyplayer / replicate
    provider_id = models.CharField(max_length=255, blank=True)
    prompt = models.TextField(blank=True)
    generated_url = models.CharField(max_length=500, blank=True)
    cost_cents = models.IntegerField(null=True, blank=True)
    generation_time_ms = models.IntegerField(null=True, blank=True)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "avatar_generations"
        indexes = [models.Index(fields=["portfolio"])]


class PortfolioAnalytics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="analytics"
    )
    date = models.DateField()
    views = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "portfolio_analytics"
        unique_together = [("portfolio", "date")]
