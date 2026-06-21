"""
Publish = wildcard-serve (Model B). No external deploy: HTML already stored in
DB. "Publishing" just computes the live URL and flips status to live. The
Next.js catch-all route serves stored HTML on {subdomain}.{wildcard_domain}.

Custom domains (Pro) handled separately later (Cloudflare for SaaS / Netlify).
"""
from django.conf import settings
from django.utils import timezone


def publish_portfolio(portfolio):
    """Make a portfolio live. Returns the live URL."""
    if portfolio.has_custom_domain and portfolio.custom_domain:
        url = f"https://{portfolio.custom_domain}"
    else:
        url = f"https://{portfolio.subdomain}.{settings.PORTFOLIO_WILDCARD_DOMAIN}"

    portfolio.published_url = url
    portfolio.deployment_status = "live"
    portfolio.generation_status = "live"
    portfolio.last_deployed_at = timezone.now()
    portfolio.save(update_fields=[
        "published_url", "deployment_status", "generation_status", "last_deployed_at",
    ])
    return url
