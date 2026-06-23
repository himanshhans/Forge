"""
Custom-domain management: ownership verification (DNS TXT challenge) and
optional SSL provisioning via Cloudflare for SaaS.

Flow:
  1. user adds domain -> we store a random TXT challenge token.
  2. user adds DNS records (TXT challenge + CNAME to our edge).
  3. verify() resolves the TXT record and confirms the token -> domain verified.
  4. provision_ssl() (if Cloudflare configured) registers the custom hostname.
"""
import logging
import re
import secrets

import dns.resolver
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

_DOMAIN_RE = re.compile(r"^(?!-)[a-z0-9-]{1,63}(?<!-)(\.(?!-)[a-z0-9-]{1,63}(?<!-))+$")
CHALLENGE_PREFIX = "_forge-challenge"


def normalize_domain(raw: str) -> str:
    d = (raw or "").strip().lower()
    d = re.sub(r"^https?://", "", d).split("/")[0].split(":")[0]
    return d


def is_valid_domain(domain: str) -> bool:
    return bool(_DOMAIN_RE.match(domain)) and len(domain) <= 253


def make_token() -> str:
    return "forge-verify-" + secrets.token_hex(16)


def dns_instructions(domain: str, token: str) -> dict:
    return {
        "verification": {
            "type": "TXT",
            "name": f"{CHALLENGE_PREFIX}.{domain}",
            "value": token,
        },
        "routing": {
            "type": "CNAME",
            "name": domain,
            "value": settings.CUSTOM_DOMAIN_CNAME_TARGET,
        },
    }


def verify_txt(domain: str, token: str) -> bool:
    """Resolve the TXT challenge record and confirm it contains the token."""
    name = f"{CHALLENGE_PREFIX}.{domain}"
    try:
        answers = dns.resolver.resolve(name, "TXT", lifetime=8)
    except Exception as e:  # NXDOMAIN, timeout, no answer
        logger.info("TXT verify failed for %s: %s", name, e)
        return False
    for rdata in answers:
        txt = b"".join(rdata.strings).decode(errors="ignore") if hasattr(rdata, "strings") else str(rdata).strip('"')
        if token in txt:
            return True
    return False


def provision_ssl(domain: str) -> bool:
    """Register the custom hostname with Cloudflare for SaaS (prod). No-op if
    Cloudflare isn't configured (platform/edge handles TLS some other way)."""
    if not (settings.CLOUDFLARE_API_TOKEN and settings.CLOUDFLARE_ZONE_ID):
        logger.info("Cloudflare not configured; skipping SSL provision for %s", domain)
        return True
    try:
        resp = requests.post(
            f"https://api.cloudflare.com/client/v4/zones/{settings.CLOUDFLARE_ZONE_ID}/custom_hostnames",
            headers={"Authorization": f"Bearer {settings.CLOUDFLARE_API_TOKEN}"},
            json={"hostname": domain, "ssl": {"method": "http", "type": "dv"}},
            timeout=15,
        )
        return resp.ok
    except requests.RequestException as e:
        logger.error("Cloudflare provision failed for %s: %s", domain, e)
        return False
