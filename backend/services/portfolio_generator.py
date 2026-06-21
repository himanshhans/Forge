"""
Niche-aware portfolio generation.

The LLM produces semantic HTML (using a fixed class vocabulary) + an accent
color + SEO metadata. It does NOT write CSS — we inject a baked-in theme so the
output is always well-designed. See services/theme.py.
"""
import json
from pathlib import Path

from apps.portfolios.niches import get_niche
from .llm_service import LLMError, generate_text
from .theme import CLASS_VOCAB, build_css

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

BASE_SYSTEM = f"""You are a senior portfolio designer and copywriter. Produce a single-page
portfolio as STRICT JSON with exactly these keys:
{{
  "html": "<semantic body markup using the class vocabulary below>",
  "accent": "#RRGGBB (one color that fits this person's niche and vibe)",
  "metadata": {{
    "title": "<SEO title>",
    "description": "<=160 char meta description",
    "og_title": "...",
    "og_description": "...",
    "json_ld": {{ "@context":"https://schema.org", "@type":"Person", ... }}
  }}
}}

{CLASS_VOCAB}

Write polished, specific copy — not lorem ipsum, not placeholders. Open with a
strong hero. Build the sections that the user's details actually support.
Output ONLY the JSON object — no markdown, no code fences, no prose.
"""


def _load_niche_prompt(prompt_key: str) -> str:
    path = PROMPTS_DIR / f"{prompt_key}.txt"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def build_user_prompt(niche_cfg, questionnaire, intro_card, avatar_url):
    return (
        f"Niche: {niche_cfg['display_name']}\n"
        f"SEO schema: {niche_cfg['seo_schema']}\n"
        f"Suggested CTAs: {', '.join(niche_cfg['default_ctas'])}\n"
        f"Intro card: {json.dumps(intro_card)}\n"
        f"Questionnaire answers: {json.dumps(questionnaire)}\n\n"
        "Generate the portfolio JSON now."
    )


def generate_portfolio(niche_id, questionnaire, intro_card=None, avatar_url=""):
    """Returns (result_dict, provider). result_dict = {html, css, metadata}."""
    niche_cfg = get_niche(niche_id)
    if not niche_cfg:
        raise LLMError(f"Unknown niche: {niche_id}")

    system = BASE_SYSTEM + "\n\n" + _load_niche_prompt(niche_cfg["generation_prompt"])
    user = build_user_prompt(niche_cfg, questionnaire, intro_card or {}, avatar_url)

    content, provider = generate_text(system, user, json_mode=True)
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise LLMError(f"LLM returned invalid JSON: {e}") from e

    return {
        "html": data.get("html", ""),
        "css": build_css(data.get("accent")),
        "metadata": data.get("metadata", {}),
    }, provider
