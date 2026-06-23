import pytest
from rest_framework.test import APIClient

from .models import ContactCard

pytestmark = pytest.mark.django_db


def _payload(name="Jordan Lee"):
    return {
        "name": name,
        "headline": "Product designer",
        "bio": "I help startups look credible.",
        "email": "jordan@example.com",
        "links": [{"label": "Site", "url": "https://x.com/jordan"}],
    }


def test_generate_card(auth_client):
    c = auth_client(sub="u1", username="u1")
    r = c.post("/api/v1/cards/generate/", _payload(), format="json")
    assert r.status_code == 201
    assert r.data["slug"]
    card = ContactCard.objects.get(id=r.data["id"])
    assert "Jordan Lee" in card.generated_html
    assert card.generated_css.startswith("@import")
    assert card.design  # random design captured


def test_card_requires_auth():
    assert APIClient().post("/api/v1/cards/generate/", _payload(), format="json").status_code == 401


def test_free_tier_blocks_second_card(auth_client):
    c = auth_client(sub="u1", username="u1")
    assert c.post("/api/v1/cards/generate/", _payload(), format="json").status_code == 201
    r = c.post("/api/v1/cards/generate/", _payload("Other"), format="json")
    assert r.status_code == 403
    assert "Free plan" in str(r.data)


def test_card_site_public_and_vcard(auth_client):
    c = auth_client(sub="u1", username="u1")
    slug = c.post("/api/v1/cards/generate/", _payload(), format="json").data["slug"]

    pub = APIClient()
    site = pub.get(f"/api/v1/card-sites/{slug}/")
    assert site.status_code == 200
    assert "Jordan Lee" in site.data["generated_html"]

    vcf = pub.get(f"/api/v1/card-sites/{slug}/vcard/")
    assert vcf.status_code == 200
    assert vcf["Content-Type"] == "text/vcard"
    assert b"BEGIN:VCARD" in vcf.content


def test_cards_user_scoped(auth_client):
    auth_client(sub="ua", username="ua").post("/api/v1/cards/generate/", _payload(), format="json")
    other = auth_client(sub="ub", username="ub").get("/api/v1/cards/")
    assert other.status_code == 200
    assert other.data == [] or other.data.get("results", []) == []
