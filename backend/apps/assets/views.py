from django.conf import settings
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from services.avatar_service import AvatarError, generate_avatar
from services.storage import save_avatar
from apps.portfolios.throttles import AvatarGenThrottle


class AvatarUploadView(APIView):
    """Upload a profile image -> stored (R2/local) -> returns public URL."""
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        f = request.FILES.get("file")
        if not f:
            return Response({"detail": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        if not (f.content_type or "").startswith("image/"):
            return Response({"detail": "File must be an image"}, status=status.HTTP_400_BAD_REQUEST)
        if f.size > settings.MAX_AVATAR_BYTES:
            return Response({"detail": "Image too large (max 5 MB)"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            url = save_avatar(f.read())
        except Exception:
            return Response({"detail": "Could not process image"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"url": url}, status=status.HTTP_201_CREATED)


class AvatarGenerateView(APIView):
    """Generate an AI avatar from a description (Pollinations free / Replicate if keyed)."""
    throttle_classes = [AvatarGenThrottle]

    def post(self, request):
        description = (request.data.get("description") or "").strip()
        if not description:
            return Response({"detail": "description required"}, status=status.HTTP_400_BAD_REQUEST)
        if len(description) > 500:
            return Response({"detail": "description too long (max 500)"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            out = generate_avatar("ai_photo", description)
        except AvatarError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        return Response({"url": out["url"]})
