"""Avatar image handling — process + persist to the configured storage
(R2 in prod, local filesystem in dev). Returns a public URL."""
import io
import uuid

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image

AVATAR_SIZE = 512


def _square(img: Image.Image) -> Image.Image:
    w, h = img.size
    side = min(w, h)
    left, top = (w - side) // 2, (h - side) // 2
    return img.crop((left, top, left + side, top + side))


def save_avatar(data: bytes) -> str:
    """Center-crop to square, resize to 512², save as JPEG, return public URL."""
    img = Image.open(io.BytesIO(data))
    img = _square(img).resize((AVATAR_SIZE, AVATAR_SIZE), Image.LANCZOS).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85)
    name = f"avatars/{uuid.uuid4().hex}.jpg"
    saved = default_storage.save(name, ContentFile(buf.getvalue()))
    url = default_storage.url(saved)
    # Local FileSystemStorage returns a relative "/media/..." path; absolutize it
    # so it loads inside portfolio/card pages served from a different host.
    if url.startswith("/"):
        url = settings.BACKEND_BASE_URL.rstrip("/") + url
    return url
