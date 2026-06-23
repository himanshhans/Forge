"""
Avatar image generation.

Providers (in order of preference):
  1. Replicate (SDXL) — if REPLICATE_API_KEY set (paid, highest quality).
  2. Pollinations.ai — free, NO API KEY, returns the image directly. Default.

Each provider returns raw image bytes; generate_avatar persists them to storage
(R2/local) and returns the stored public URL.
"""
import logging
import time
import urllib.parse

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

REPLICATE_URL = "https://api.replicate.com/v1/predictions"
REPLICATE_SD_VERSION = "stability-ai/sdxl"
POLLINATIONS_URL = "https://image.pollinations.ai/prompt/"
TIMEOUT = 90


class AvatarError(Exception):
    pass


def _pollinations_bytes(prompt: str) -> bytes:
    """Free, keyless text->image. The GET returns the PNG directly."""
    q = urllib.parse.quote(prompt)
    url = f"{POLLINATIONS_URL}{q}?width=512&height=512&nologo=true&model=flux"
    r = requests.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    if not r.headers.get("content-type", "").startswith("image/"):
        raise AvatarError("Pollinations did not return an image")
    return r.content


def _replicate_bytes(prompt: str) -> bytes:
    headers = {
        "Authorization": f"Bearer {settings.REPLICATE_API_KEY}",
        "Content-Type": "application/json",
    }
    start = time.time()
    resp = requests.post(
        REPLICATE_URL, headers=headers,
        json={"version": REPLICATE_SD_VERSION, "input": {"prompt": prompt}},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    pred = resp.json()
    poll = pred["urls"]["get"]
    while pred["status"] not in ("succeeded", "failed", "canceled"):
        if time.time() - start > TIMEOUT:
            raise AvatarError("Replicate timed out")
        time.sleep(2)
        pred = requests.get(poll, headers=headers, timeout=TIMEOUT).json()
    if pred["status"] != "succeeded":
        raise AvatarError(f"Replicate failed: {pred.get('error')}")
    out = pred.get("output")
    img_url = out[0] if isinstance(out, list) else out
    return requests.get(img_url, timeout=TIMEOUT).content


def generate_avatar(avatar_type: str, description: str) -> dict:
    """Generate an avatar image, persist it, return {url, provider}."""
    # Lightly steer the prompt by type.
    if avatar_type == "2d_illustrated":
        prompt = f"flat vector illustrated avatar portrait, {description}, clean, centered"
    else:
        prompt = f"professional headshot portrait, {description}, soft lighting, centered"

    start = time.time()
    if settings.REPLICATE_API_KEY:
        provider = "replicate"
        img_bytes = _replicate_bytes(prompt)
    else:
        provider = "pollinations"
        try:
            img_bytes = _pollinations_bytes(prompt)
        except requests.RequestException as e:
            raise AvatarError(f"Image generation failed: {e}") from e

    from .storage import save_avatar
    return {
        "url": save_avatar(img_bytes),
        "provider": provider,
        "generation_time_ms": int((time.time() - start) * 1000),
    }
