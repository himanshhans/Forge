"""pytest fixtures. DB/cache/celery configured by config.settings_test."""
import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


@pytest.fixture(scope="session")
def rsa_keys():
    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    priv_pem = priv.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    pub_pem = priv.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return priv_pem, pub_pem


@pytest.fixture
def mint_token(rsa_keys, settings):
    """Factory -> a signed Clerk-style RS256 JWT for a given clerk sub."""
    priv_pem, _ = rsa_keys

    def _make(sub="clerk_user_123", email=None, username="tester"):
        return jwt.encode(
            {
                "sub": sub,
                "email": email or f"{sub}@example.com",  # unique per sub
                "username": username,
                "iss": settings.CLERK_ISSUER,
            },
            priv_pem,
            algorithm="RS256",
        )

    return _make


@pytest.fixture(autouse=True)
def patch_jwks(rsa_keys, monkeypatch):
    """Patch Clerk JWKS lookup to return our test public key."""
    _, pub_pem = rsa_keys

    class _FakeKey:
        key = pub_pem

    class _FakeClient:
        def get_signing_key_from_jwt(self, _token):
            return _FakeKey()

    monkeypatch.setattr(
        "apps.users.authentication._get_jwks_client", lambda: _FakeClient()
    )


@pytest.fixture
def auth_client(mint_token):
    """DRF APIClient with a valid bearer token (lazy-creates the user)."""
    from rest_framework.test import APIClient

    def _client(sub="clerk_user_123", email=None, username="tester"):
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=f"Bearer {mint_token(sub, email, username)}")
        return c

    return _client
