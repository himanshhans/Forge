"""
Clerk JWT authentication for DRF.

Clerk issues the JWT (frontend via Clerk SDK). Django only VERIFIES it using
Clerk's JWKS public keys. Django never issues tokens.

On valid token, maps `sub` (Clerk user id) to a local User row. The row is
normally created by the Clerk webhook (user.created); if missing, we lazily
create a minimal row from token claims so first request doesn't 401.
"""
import jwt
from jwt import PyJWKClient
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User

# Cache one JWKS client per process (it caches keys internally).
_jwks_client = None


def _get_jwks_client():
    global _jwks_client
    if _jwks_client is None:
        if not settings.CLERK_JWKS_URL:
            raise exceptions.AuthenticationFailed("CLERK_JWKS_URL not configured")
        _jwks_client = PyJWKClient(settings.CLERK_JWKS_URL)
    return _jwks_client


class ClerkJWTAuthentication(authentication.BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None  # no credentials -> let other auth / AnonymousUser
        if len(auth) != 2:
            raise exceptions.AuthenticationFailed("Invalid Authorization header")

        token = auth[1].decode()
        claims = self._decode(token)
        user = self._get_or_create_user(claims)
        return (user, token)

    def _decode(self, token):
        try:
            signing_key = _get_jwks_client().get_signing_key_from_jwt(token)
            return jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                issuer=settings.CLERK_ISSUER or None,
                options={"verify_aud": False},  # Clerk session tokens have no fixed aud
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.PyJWTError as e:
            raise exceptions.AuthenticationFailed(f"Token invalid: {e}")

    def _get_or_create_user(self, claims):
        clerk_id = claims.get("sub")
        if not clerk_id:
            raise exceptions.AuthenticationFailed("Token missing sub claim")
        email = claims.get("email", "") or f"{clerk_id}@placeholder.clerk"
        username = claims.get("username") or claims.get("email") or clerk_id
        user, _ = User.objects.get_or_create(
            clerk_user_id=clerk_id,
            defaults={"email": email, "username": username[:150]},
        )
        return user

    def authenticate_header(self, request):
        return self.keyword
