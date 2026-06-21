"""
Avatar generation. 3D = ReadyPlayer.me, 2D/AI-photo = Replicate (Stable Diffusion).
Returns generated image/avatar URL + provider metadata. Image upload to R2 done
by storage layer (wired later); for now returns provider URL.
"""
import logging
import time

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

REPLICATE_URL = "https://api.replicate.com/v1/predictions"
# Stable Diffusion model version — verify/replace with current Replicate version id.
REPLICATE_SD_VERSION = "stability-ai/sdxl"
TIMEOUT = 90


class AvatarError(Exception):
    pass


def generate_replicate_image(prompt: str) -> dict:
    """Call Replicate, poll until done. Returns {url, provider, provider_id, cost_cents}."""
    if not settings.REPLICATE_API_KEY:
        raise AvatarError("REPLICATE_API_KEY not configured")

    headers = {
        "Authorization": f"Bearer {settings.REPLICATE_API_KEY}",
        "Content-Type": "application/json",
    }
    start = time.time()
    resp = requests.post(
        REPLICATE_URL,
        headers=headers,
        json={"version": REPLICATE_SD_VERSION, "input": {"prompt": prompt}},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    pred = resp.json()
    poll_url = pred["urls"]["get"]

    # Poll for completion (Replicate is async).
    while pred["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(2)
        if time.time() - start > TIMEOUT:
            raise AvatarError("Replicate timed out")
        pred = requests.get(poll_url, headers=headers, timeout=TIMEOUT).json()

    if pred["status"] != "succeeded":
        raise AvatarError(f"Replicate failed: {pred.get('error')}")

    output = pred.get("output")
    url = output[0] if isinstance(output, list) else output
    return {
        "url": url,
        "provider": "replicate",
        "provider_id": pred["id"],
        "cost_cents": None,
        "generation_time_ms": int((time.time() - start) * 1000),
    }


def generate_avatar(avatar_type: str, description: str) -> dict:
    """Dispatch by avatar type. 3d handled client-side via ReadyPlayer; here we
    cover server-side image generation (2d_illustrated / ai_photo)."""
    if avatar_type in ("2d_illustrated", "ai_photo"):
        return generate_replicate_image(description)
    raise AvatarError(f"Server-side gen not supported for type: {avatar_type}")
