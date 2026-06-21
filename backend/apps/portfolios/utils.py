import uuid

from django.utils.text import slugify

from .models import Portfolio


def unique_subdomain(base: str) -> str:
    """Slugify base; ensure unique across portfolios by appending short suffix."""
    root = slugify(base) or "site"
    candidate = root
    while Portfolio.objects.filter(subdomain=candidate).exists():
        candidate = f"{root}-{uuid.uuid4().hex[:5]}"
    return candidate


def unique_slug(base: str) -> str:
    root = slugify(base) or "portfolio"
    candidate = root
    while Portfolio.objects.filter(slug=candidate).exists():
        candidate = f"{root}-{uuid.uuid4().hex[:5]}"
    return candidate
