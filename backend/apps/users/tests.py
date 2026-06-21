import pytest
from rest_framework.test import APIClient

from .models import User

pytestmark = pytest.mark.django_db


def test_me_requires_auth():
    resp = APIClient().get("/api/v1/users/me/")
    assert resp.status_code == 401


def test_me_lazy_creates_user(auth_client):
    resp = auth_client(sub="clerk_abc", email="a@b.com", username="alice").get(
        "/api/v1/users/me/"
    )
    assert resp.status_code == 200
    assert resp.data["username"] == "alice"
    assert resp.data["plan"] == "free"
    assert User.objects.filter(clerk_user_id="clerk_abc").exists()


def test_me_patch_is_public(auth_client):
    c = auth_client(sub="clerk_abc")
    resp = c.patch("/api/v1/users/me/", {"is_public": False}, format="json")
    assert resp.status_code == 200
    assert resp.data["is_public"] is False


def test_invalid_token_rejected():
    c = APIClient()
    c.credentials(HTTP_AUTHORIZATION="Bearer not.a.jwt")
    resp = c.get("/api/v1/users/me/")
    assert resp.status_code == 401
