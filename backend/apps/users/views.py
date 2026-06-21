import base64
import hashlib
import hmac
import json

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class MeView(RetrieveUpdateAPIView):
    """GET/PATCH the authenticated user's own record."""
    serializer_class = UserSerializer
    http_method_names = ["get", "patch"]

    def get_object(self):
        return self.request.user


def _verify_svix(request) -> bool:
    """Verify Clerk (Svix) webhook signature. Returns True if valid."""
    secret = settings.CLERK_WEBHOOK_SECRET
    if not secret:
        return False
    svix_id = request.headers.get("svix-id", "")
    svix_ts = request.headers.get("svix-timestamp", "")
    svix_sig = request.headers.get("svix-signature", "")
    if not (svix_id and svix_ts and svix_sig):
        return False

    body = request.body.decode()
    signed = f"{svix_id}.{svix_ts}.{body}".encode()
    key = base64.b64decode(secret.split("_", 1)[1])  # strip "whsec_"
    expected = base64.b64encode(hmac.new(key, signed, hashlib.sha256).digest()).decode()

    # Header may carry multiple space-separated "v1,<sig>" entries.
    for part in svix_sig.split():
        _, _, sig = part.partition(",")
        if hmac.compare_digest(sig, expected):
            return True
    return False


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def clerk_webhook(request):
    """Sync Clerk users -> local rows. Handles user.created/updated/deleted."""
    if not _verify_svix(request):
        return Response({"error": "Invalid signature"}, status=status.HTTP_401_UNAUTHORIZED)

    payload = json.loads(request.body)
    event = payload.get("type", "")
    data = payload.get("data", {})
    clerk_id = data.get("id")
    if not clerk_id:
        return Response({"error": "Missing user id"}, status=status.HTTP_400_BAD_REQUEST)

    if event == "user.deleted":
        User.objects.filter(clerk_user_id=clerk_id).delete()
        return Response({"status": "deleted"})

    if event in ("user.created", "user.updated"):
        emails = data.get("email_addresses", [])
        email = emails[0]["email_address"] if emails else f"{clerk_id}@placeholder.clerk"
        username = data.get("username") or email.split("@")[0]
        User.objects.update_or_create(
            clerk_user_id=clerk_id,
            defaults={"email": email, "username": username[:150]},
        )
        return Response({"status": "synced"})

    return Response({"status": "ignored"})
