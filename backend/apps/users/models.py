import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Identity owned by Clerk. Django stores no usable password.
    Row synced via Clerk webhook (user.created / user.deleted).
    """
    PLAN_FREE = "free"
    PLAN_PRO = "pro"
    PLAN_CHOICES = [(PLAN_FREE, "Free"), (PLAN_PRO, "Pro")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clerk_user_id = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(unique=True)
    plan = models.CharField(max_length=50, choices=PLAN_CHOICES, default=PLAN_FREE)
    is_public = models.BooleanField(default=True)

    # Stripe fields added in Phase 3 (stripe_customer_id, subscription_status...).

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.username} ({self.plan})"

    @property
    def is_pro(self):
        return self.plan == self.PLAN_PRO
