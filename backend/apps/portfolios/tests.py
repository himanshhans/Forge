import pytest
from rest_framework.test import APIClient

from .models import Portfolio

pytestmark = pytest.mark.django_db


# --- Niches (public) ---

def test_niches_list_public():
    resp = APIClient().get("/api/v1/niches/")
    assert resp.status_code == 200
    ids = [n["niche_id"] for n in resp.data["niches"]]
    assert "indie_hacker" in ids and "freelancer" in ids
    assert len(ids) == 5


def test_niche_detail_unknown_404():
    resp = APIClient().get("/api/v1/niches/nope/")
    assert resp.status_code == 404


# --- Generate (mock LLM so no live call) ---

@pytest.fixture
def mock_generate(monkeypatch):
    def fake(niche_id, questionnaire, intro_card=None, avatar_url=""):
        return (
            {"html": "<h1>hi</h1>", "css": "h1{}", "metadata": {"title": "x"}},
            "groq",
        )
    monkeypatch.setattr("apps.portfolios.tasks.generate_portfolio", fake)


def test_generate_creates_and_publishes(auth_client, mock_generate):
    c = auth_client(sub="u1", username="builder")
    payload = {
        "niche": "freelancer",
        "questionnaire": {"name": "Jo"},
        "avatar_type": "photo",
        "intro_card": {"name": "Jo"},
    }
    resp = c.post("/api/v1/portfolios/generate/", payload, format="json")
    assert resp.status_code == 202
    pid = resp.data["id"]
    p = Portfolio.objects.get(id=pid)
    # eager pipeline ran: text -> avatar_done(photo) -> publish -> live
    assert p.generation_status == "live"
    assert p.deployment_status == "live"
    assert p.published_url.endswith(".forge.app")
    assert p.generated_html == "<h1>hi</h1>"


def test_generate_rejects_unknown_niche(auth_client, mock_generate):
    c = auth_client(sub="u1")
    resp = c.post(
        "/api/v1/portfolios/generate/",
        {"niche": "nope", "questionnaire": {}, "intro_card": {}},
        format="json",
    )
    assert resp.status_code == 400


def test_free_tier_blocks_second_portfolio(auth_client, mock_generate):
    c = auth_client(sub="u1", username="builder")
    body = {"niche": "freelancer", "questionnaire": {"name": "Jo"}, "intro_card": {"name": "Jo"}}
    assert c.post("/api/v1/portfolios/generate/", body, format="json").status_code == 202
    resp = c.post("/api/v1/portfolios/generate/", body, format="json")
    assert resp.status_code == 403
    assert "Free plan" in str(resp.data)


def test_input_cap_bio_too_long(auth_client, mock_generate):
    c = auth_client(sub="u1")
    resp = c.post(
        "/api/v1/portfolios/generate/",
        {"niche": "freelancer", "questionnaire": {}, "intro_card": {"bio": "x" * 1001}},
        format="json",
    )
    assert resp.status_code == 400


def test_custom_domain_add_verify_serve(auth_client, mock_generate, monkeypatch):
    from rest_framework.test import APIClient
    c = auth_client(sub="ud", username="ud")
    pid = c.post(
        "/api/v1/portfolios/generate/",
        {"niche": "freelancer", "questionnaire": {}, "intro_card": {"name": "D"}},
        format="json",
    ).data["id"]

    # add domain -> pending + DNS instructions
    add = c.post(f"/api/v1/portfolios/{pid}/domain/", {"domain": "me.example.com"}, format="json")
    assert add.status_code == 200
    assert add.data["status"] == "pending"
    assert add.data["dns"]["verification"]["type"] == "TXT"

    # verify fails when TXT missing
    monkeypatch.setattr("services.domains.verify_txt", lambda d, t: False)
    assert c.post(f"/api/v1/portfolios/{pid}/domain/verify/").status_code == 400

    # verify succeeds when TXT present
    monkeypatch.setattr("services.domains.verify_txt", lambda d, t: True)
    ok = c.post(f"/api/v1/portfolios/{pid}/domain/verify/")
    assert ok.status_code == 200 and ok.data["status"] == "verified"

    # served publicly by domain
    site = APIClient().get("/api/v1/sites/by-domain/?host=me.example.com")
    assert site.status_code == 200
    assert "generated_html" in site.data

    # unknown domain -> 404
    assert APIClient().get("/api/v1/sites/by-domain/?host=nope.com").status_code == 404


def test_site_serves_live_only(auth_client, mock_generate):
    from rest_framework.test import APIClient
    from .models import Portfolio
    from apps.users.models import User

    u = User.objects.create(clerk_user_id="cs", username="cs", email="cs@e.com")
    live = Portfolio.objects.create(
        user=u, title="Live", slug="cs1", subdomain="cs1", niche="freelancer",
        deployment_status="live", generated_html="<h1>hi</h1>", generated_css="h1{}",
        generated_metadata={"title": "Live"},
    )
    Portfolio.objects.create(
        user=u, title="Draft", slug="cs2", subdomain="cs2", niche="freelancer",
        deployment_status="pending",
    )
    c = APIClient()
    ok = c.get(f"/api/v1/sites/{live.subdomain}/")
    assert ok.status_code == 200
    assert ok.data["generated_html"] == "<h1>hi</h1>"
    # draft (not live) -> 404
    assert c.get("/api/v1/sites/cs2/").status_code == 404


def test_user_scoped_list(auth_client, mock_generate):
    a = auth_client(sub="ua", username="aa")
    b = auth_client(sub="ub", username="bb")
    a.post("/api/v1/portfolios/generate/",
           {"niche": "freelancer", "questionnaire": {}, "intro_card": {"name": "A"}},
           format="json")
    # b sees none of a's portfolios
    resp = b.get("/api/v1/portfolios/")
    assert resp.status_code == 200
    assert resp.data == [] or resp.data.get("results", []) == []
