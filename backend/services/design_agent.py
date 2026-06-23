"""
Design agent — fully random art direction, no LLM. Every generation gets a
random layout, font pairing, light/dark mode, corner radius, and an
algorithmically-generated palette (HSL-constrained so contrast stays legible).
A random style seed is still passed to the coding agent to vary copy tone.

Quality is guaranteed because theme.build_css owns the CSS system; the brief
only fills tokens within it.
"""
import colorsys
import random

# Curated, weight-safe Google Font pairings (display, body). All have 400/600/700.
FONT_PAIRINGS = [
    {"display": "Fraunces", "body": "Inter"},
    {"display": "Playfair Display", "body": "Inter"},
    {"display": "Space Grotesk", "body": "Inter"},
    {"display": "Newsreader", "body": "Manrope"},
    {"display": "Source Serif 4", "body": "Sora"},
    {"display": "Syne", "body": "Inter"},
    {"display": "Sora", "body": "Sora"},
    {"display": "Fraunces", "body": "Manrope"},
]

LAYOUTS = ["centered", "left", "editorial", "bold"]

STYLE_SEEDS = [
    "minimal swiss — lots of whitespace, restraint, precise",
    "warm editorial — paper tones, serif headlines, inviting",
    "bold modern — large type, strong accent, confident",
    "elegant — moody, refined, high contrast",
    "playful & friendly — rounded, approachable, lively",
    "corporate clean — trustworthy, calm, professional",
    "refined luxury — understated, generous spacing",
    "tech minimal — crisp, grotesk type, cool neutrals",
]


def _hex(r: float, g: float, b: float) -> str:
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


def _hsl(h: float, s: float, lum: float) -> str:
    r, g, b = colorsys.hls_to_rgb(h, lum, s)
    return _hex(r, g, b)


def random_palette() -> tuple[str, dict]:
    """Random but legible palette. Returns (mode, palette)."""
    mode = random.choice(["light", "dark"])
    tint = random.random()          # shared faint hue for neutrals
    accent_h = random.random()      # independent vivid accent hue
    accent = _hsl(accent_h, random.uniform(0.62, 0.92), random.uniform(0.46, 0.58))

    if mode == "light":
        pal = {
            "bg": _hsl(tint, random.uniform(0.04, 0.16), random.uniform(0.955, 0.99)),
            "fg": _hsl(tint, random.uniform(0.05, 0.20), random.uniform(0.10, 0.16)),
            "muted": _hsl(tint, 0.08, random.uniform(0.40, 0.48)),
            "card": _hsl(tint, random.uniform(0.05, 0.14), random.uniform(0.90, 0.95)),
            "border": _hsl(tint, 0.10, random.uniform(0.84, 0.90)),
            "accent": accent,
        }
    else:
        pal = {
            "bg": _hsl(tint, random.uniform(0.10, 0.22), random.uniform(0.05, 0.10)),
            "fg": _hsl(tint, random.uniform(0.04, 0.14), random.uniform(0.90, 0.96)),
            "muted": _hsl(tint, 0.08, random.uniform(0.55, 0.66)),
            "card": _hsl(tint, random.uniform(0.10, 0.20), random.uniform(0.11, 0.16)),
            "border": _hsl(tint, 0.12, random.uniform(0.18, 0.26)),
            "accent": accent,
        }
    return mode, pal


def design(niche_cfg=None, questionnaire=None, intro_card=None) -> dict:
    """Return a fully random design brief. Args accepted for signature compatibility."""
    mode, palette = random_palette()
    return {
        "mode": mode,
        "palette": palette,
        "fonts": random.choice(FONT_PAIRINGS),
        "layout": random.choice(LAYOUTS),
        "radius_px": random.randint(0, 20),
        "seed": random.choice(STYLE_SEEDS),
    }
