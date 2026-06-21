import pytest
from rest_framework.test import APIClient

from apps.portfolios.models import Portfolio
from apps.users.models import User

pytestmark = pytest.mark.django_db


def _live_portfolio(username="creator1", niche="freelancer", title="Live One"):
    user = User.objects.create(
        clerk_user_id=f"clerk_{username}", username=username,
        email=f"{username}@e.com", is_public=True,
    )
    return Portfolio.objects.create(
        user=user, title=title, slug=username, subdomain=username,
        niche=niche, in_showcase=True, deployment_status="live",
        published_url=f"https://{username}.forge.app",
    )


def test_gallery_lists_only_live_public():
    live = _live_portfolio("alice")
    # a non-live one must NOT appear
    Portfolio.objects.create(
        user=live.user, title="Draft", slug="draft", subdomain="draft",
        niche="freelancer", in_showcase=True, deployment_status="pending",
    )
    resp = APIClient().get("/api/v1/gallery/")
    assert resp.status_code == 200
    titles = [p["title"] for p in resp.data["portfolios"]]
    assert "Live One" in titles
    assert "Draft" not in titles
    assert len(resp.data["niches"]) == 5


def test_gallery_niche_filter():
    _live_portfolio("ih", niche="indie_hacker", title="IH")
    _live_portfolio("fl", niche="freelancer", title="FL")
    resp = APIClient().get("/api/v1/gallery/?niche=indie_hacker")
    titles = [p["title"] for p in resp.data["portfolios"]]
    assert titles == ["IH"]


def test_view_count_increment():
    p = _live_portfolio("bob")
    resp = APIClient().post(f"/api/v1/gallery/{p.id}/view/")
    assert resp.status_code == 200
    assert resp.data["view_count"] == 1
    p.refresh_from_db()
    assert p.views == 1


def test_view_count_unknown_404():
    import uuid
    resp = APIClient().post(f"/api/v1/gallery/{uuid.uuid4()}/view/")
    assert resp.status_code == 404
