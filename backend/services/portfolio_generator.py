"""
Two-agent generation:
  1. design agent  -> design brief (palette, fonts, layout, radius)  [varied per run]
  2. coding agent  -> semantic HTML using the class vocabulary
We then compose the CSS from the brief (theme.build_css). We own the CSS, so
output is always well-built; variety comes from the brief.
"""
import json
from pathlib import Path

from apps.portfolios.niches import get_niche
from .design_agent import design
from .llm_service import LLMError, generate_text
from .theme import CLASS_VOCAB, build_css

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

BASE_SYSTEM = f"""You are a senior portfolio copywriter and front-end developer. Produce a
single-page portfolio as STRICT JSON with exactly these keys:
{{
  "html": "<semantic body markup using the class vocabulary below>",
  "metadata": {{
    "title": "<SEO title>",
    "description": "<=160 char meta description",
    "og_title": "...",
    "og_description": "...",
    "json_ld": {{ "@context":"https://schema.org", "@type":"Person", ... }}
  }}
}}

{CLASS_VOCAB}

The "html" MUST follow this skeleton exactly (fill/repeat/omit inner parts as the
content needs, but keep these classes and start with the hero):

<header class="hero"><h1>NAME</h1><p class="tagline">TAGLINE</p><p class="lead">BIO</p><div class="cta-row"><a class="btn" href="...">PRIMARY</a><a class="btn ghost" href="...">SECONDARY</a></div></header>
<section class="section"><div class="wrap"><h2 class="eyebrow">WORK</h2><div class="grid"><article class="card"><div class="thumb"></div><h3>PROJECT</h3><p>RESULT</p></article></div></div></section>
<section class="contact"><div class="wrap"><h2>CLOSING CTA</h2><p>...</p><a class="btn" href="...">ACTION</a></div></section>

A DESIGN BRIEF is provided (mood, layout, palette). Match tone to it:
- "editorial" → fewer cards, more prose. "bold" → punchy short hero. "centered"/"left" → balanced.
Rules: the html MUST begin with <header class="hero">. Use the exact class names above.
If an AVATAR URL is given, make it the first child of the hero: <img class="avatar" src="URL" alt="name" />.
Otherwise use NO images. Write polished, specific copy — never lorem ipsum or placeholders.
Build only the sections the user's details support. Output ONLY the JSON object."""


def _load_niche_prompt(prompt_key: str) -> str:
    path = PROMPTS_DIR / f"{prompt_key}.txt"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _coding_prompt(niche_cfg, questionnaire, intro_card, brief, avatar_url):
    return (
        f"Niche: {niche_cfg['display_name']}\n"
        f"SEO schema: {niche_cfg['seo_schema']}\n"
        f"Suggested CTAs: {', '.join(niche_cfg['default_ctas'])}\n"
        f"Design brief: mood='{brief['seed']}', layout='{brief['layout']}', mode='{brief['mode']}'\n"
        f"Avatar URL: {avatar_url or '(none — use no images)'}\n"
        f"Intro card: {json.dumps(intro_card)}\n"
        f"Questionnaire answers: {json.dumps(questionnaire)}\n\n"
        "Generate the portfolio JSON now."
    )


def generate_portfolio(niche_id, questionnaire, intro_card=None, avatar_url=""):
    """Returns (result_dict, provider). result_dict = {html, css, metadata, design}."""
    niche_cfg = get_niche(niche_id)
    if not niche_cfg:
        raise LLMError(f"Unknown niche: {niche_id}")
    intro_card = intro_card or {}

    # 1) design agent
    brief = design(niche_cfg, questionnaire, intro_card)

    # 2) coding agent
    system = BASE_SYSTEM + "\n\n" + _load_niche_prompt(niche_cfg["generation_prompt"])
    user = _coding_prompt(niche_cfg, questionnaire, intro_card, brief, avatar_url)
    content, provider = generate_text(system, user, json_mode=True)
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise LLMError(f"LLM returned invalid JSON: {e}") from e

    return {
        "html": data.get("html", ""),
        "css": build_css(brief),
        "metadata": data.get("metadata", {}),
        "design": {k: brief[k] for k in ("mode", "layout", "fonts", "palette", "seed")},
    }, provider
