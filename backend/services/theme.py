"""
Theme system. The design agent produces a brief (palette, fonts, layout, radius);
build_css turns it into a real stylesheet. The coding agent only emits semantic
HTML using CLASS_VOCAB, so output is always well-structured AND visually varied.
"""

CLASS_VOCAB = """
Use ONLY these semantic classes (no inline styles, no <style>, no <script>):
- <header class="hero">  hero with <h1> name, <p class="tagline">, <p class="lead"> bio, <div class="cta-row">
- <a class="btn">primary action</a>  and  <a class="btn ghost">secondary</a>
- <section class="section"><div class="wrap"> ... </div></section>  (every section wraps content in .wrap)
- <h2 class="eyebrow">SECTION LABEL</h2> for small uppercase section labels
- <div class="grid"> with <article class="card"><div class="thumb"></div><h3></h3><p></p></article>  (work/projects/services)
- <div class="stats"> with <div class="stat"><span class="num">$4k</span><span class="label">MRR</span></div>  (metrics)
- <blockquote class="quote"><p>...</p><cite>Name, Role</cite></blockquote>  (testimonials)
- <ul class="tags"><li>Skill</li></ul>  (tags/skills/stack)
- <section class="contact"><div class="wrap"> ... </div></section>  closing CTA/contact
Rules: NEVER use <img> (no real image URLs) — use <div class="thumb"> blocks instead.
Write real, specific, compelling copy from the user's details. Keep sections that have content; omit empty ones.
"""

# Structural CSS — all visual values come from CSS variables set per-brief.
BASE_CSS = """
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--fg);
  font:17px/1.65 var(--font-body),ui-sans-serif,system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;
}
h1,h2,h3{font-family:var(--font-display),Georgia,serif; font-weight:700; line-height:1.12; letter-spacing:-0.01em; margin:0}
a{color:var(--accent); text-decoration:none}
p{margin:0}

.wrap{max-width:var(--maxw); margin:0 auto; padding:0 24px}

.hero{max-width:var(--maxw); margin:0 auto; padding:96px 24px 56px; text-align:var(--hero-align)}
.hero .avatar{display:block; width:96px; height:96px; border-radius:50%; object-fit:cover; margin:0 0 22px; border:1px solid var(--border)}
.hero h1{font-size:clamp(40px,7vw,66px)}
.hero .tagline{margin-top:14px; font-size:20px; color:var(--accent); font-weight:600}
.hero .lead{margin:18px 0 0; max-width:54ch; color:var(--muted); font-size:18px}
.hero[style] .lead{margin-inline:auto}
.cta-row{display:flex; gap:12px; justify-content:var(--cta-justify); flex-wrap:wrap; margin-top:32px}

.btn{display:inline-block; padding:12px 22px; border-radius:var(--radius); font-weight:600; font-size:15px;
  background:var(--accent); color:var(--accent-fg); border:1px solid var(--accent); transition:opacity .15s}
.btn:hover{opacity:.9}
.btn.ghost{background:transparent; color:var(--fg); border-color:var(--border)}

.section{padding:56px 0; border-top:1px solid var(--border)}
.section .wrap>h2:not(.eyebrow){font-size:30px; margin-bottom:24px}
.eyebrow{font-size:12px; font-weight:700; letter-spacing:.16em; text-transform:uppercase;
  color:var(--accent); font-family:var(--font-body); margin-bottom:10px}

.grid{display:grid; grid-template-columns:repeat(2,1fr); gap:18px}
.card{background:var(--card); border:1px solid var(--border); border-radius:var(--radius); padding:18px; overflow:hidden}
.card .thumb{aspect-ratio:16/10; border-radius:calc(var(--radius) - 4px); margin:-18px -18px 14px;
  background:linear-gradient(135deg,color-mix(in srgb,var(--accent) 24%,transparent),color-mix(in srgb,var(--accent) 6%,transparent))}
.card h3{font-size:18px; margin-bottom:6px}
.card p{color:var(--muted); font-size:15px}

.stats{display:flex; flex-wrap:wrap; gap:40px}
.stat{display:flex; flex-direction:column}
.stat .num{font-family:var(--font-display),serif; font-size:42px; color:var(--accent); line-height:1}
.stat .label{margin-top:6px; font-size:13px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted)}

.quote{margin:0; padding:22px 24px; background:var(--card); border-left:3px solid var(--accent); border-radius:0 var(--radius) var(--radius) 0}
.quote p{font-size:18px; font-style:italic}
.quote cite{display:block; margin-top:12px; font-style:normal; font-size:14px; color:var(--muted)}
.quote+.quote{margin-top:16px}

.tags{list-style:none; padding:0; margin:0; display:flex; flex-wrap:wrap; gap:8px}
.tags li{padding:6px 12px; border:1px solid var(--border); border-radius:999px; font-size:14px; color:var(--muted)}

.contact{padding:72px 0; border-top:1px solid var(--border); text-align:center}
.contact h2{font-size:32px; margin-bottom:8px}
.contact p{color:var(--muted); margin-bottom:24px}

footer,.footnote{padding:32px 24px; text-align:center; color:var(--muted); font-size:13px; border-top:1px solid var(--border)}

@media (max-width:600px){
  .hero{padding:64px 20px 40px}
  .grid{grid-template-columns:1fr}
  .stats{gap:28px}
}
"""

# Per-layout overrides.
LAYOUT_CSS = {
    "centered": ":root{--maxw:760px;--hero-align:center;--cta-justify:center}.hero .avatar{margin-inline:auto}",
    "left": ":root{--maxw:860px;--hero-align:left;--cta-justify:flex-start}",
    "editorial": (
        ":root{--maxw:720px;--hero-align:left;--cta-justify:flex-start}"
        ".hero h1{font-size:clamp(44px,8vw,76px)}"
        ".section{padding:64px 0}"
        ".card{background:transparent;border:0;border-top:1px solid var(--border);border-radius:0;padding:18px 0}"
        ".card .thumb{display:none}"
    ),
    "bold": (
        ":root{--maxw:900px;--hero-align:left;--cta-justify:flex-start}"
        ".hero h1{font-size:clamp(48px,9vw,88px);letter-spacing:-0.03em;text-transform:uppercase}"
        ".eyebrow{color:var(--fg)}"
    ),
}


def _font_query(name: str) -> str:
    return f"family={name.replace(' ', '+')}:wght@400;600;700"


def _import_fonts(display: str, body: str) -> str:
    fams = _font_query(display)
    if body != display:
        fams += "&" + _font_query(body)
    return f"@import url('https://fonts.googleapis.com/css2?{fams}&display=swap');"


def _contrast_fg(hex_accent: str) -> str:
    """Pick black/white text on the accent button by luminance."""
    h = hex_accent.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    try:
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return "#ffffff"
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#111111" if lum > 0.6 else "#ffffff"


def _root_and_fonts(brief: dict) -> tuple[str, str, dict]:
    """Return (font @import, :root vars block, resolved fonts) from a brief."""
    pal = brief.get("palette", {})
    fonts = brief.get("fonts", {"display": "Fraunces", "body": "Inter"})
    radius = brief.get("radius_px", 12)
    accent = pal.get("accent", "#1f5c45")
    root = (
        ":root{"
        f"--bg:{pal.get('bg', '#ffffff')};"
        f"--fg:{pal.get('fg', '#181816')};"
        f"--muted:{pal.get('muted', '#6b6b66')};"
        f"--accent:{accent};"
        f"--accent-fg:{_contrast_fg(accent)};"
        f"--card:{pal.get('card', '#fafaf7')};"
        f"--border:{pal.get('border', '#ececE6')};"
        f"--radius:{radius}px;"
        f"--font-display:'{fonts['display']}';"
        f"--font-body:'{fonts['body']}';"
        "}"
    )
    return _import_fonts(fonts["display"], fonts["body"]), root, fonts


def build_css(brief: dict) -> str:
    """Compose the full portfolio stylesheet from a design brief."""
    imp, root, _ = _root_and_fonts(brief)
    layout_css = LAYOUT_CSS.get(brief.get("layout", "centered"), LAYOUT_CSS["centered"])
    return "\n".join([imp, root, BASE_CSS, layout_css])


# Contact-card stylesheet: one centered card. Reuses the same brief tokens.
CARD_CSS = """
*{box-sizing:border-box}
body{margin:0;min-height:100vh;display:grid;place-items:center;padding:32px 20px;
  background:var(--bg);color:var(--fg);
  font:16px/1.6 var(--font-body),ui-sans-serif,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.card{width:100%;max-width:400px;background:var(--card);border:1px solid var(--border);
  border-radius:calc(var(--radius) + 8px);padding:32px;text-align:center;
  box-shadow:0 24px 60px -24px rgba(0,0,0,.25)}
.avatar{width:88px;height:88px;border-radius:50%;margin:0 auto 18px;object-fit:cover;
  display:grid;place-items:center;font-family:var(--font-display),serif;font-size:34px;font-weight:700;
  color:var(--accent-fg);background:linear-gradient(135deg,var(--accent),color-mix(in srgb,var(--accent) 55%,#000))}
.name{font-family:var(--font-display),serif;font-size:26px;font-weight:700;margin:0;line-height:1.15}
.headline{color:var(--accent);font-weight:600;margin:6px 0 0}
.bio{color:var(--muted);font-size:15px;margin:14px 0 0}
.meta{color:var(--muted);font-size:13px;margin-top:10px}
.links{display:flex;flex-direction:column;gap:10px;margin-top:24px}
.links a{display:block;padding:13px 16px;border-radius:var(--radius);font-weight:600;font-size:15px;
  background:var(--accent);color:var(--accent-fg);transition:opacity .15s}
.links a.secondary{background:transparent;color:var(--fg);border:1px solid var(--border)}
.links a:hover{opacity:.9}
.qr{margin:24px auto 0;width:140px;height:140px;background:#fff;padding:10px;border-radius:12px}
.qr svg{width:100%;height:100%;display:block}
.qr svg path{fill:#000}
.foot{margin-top:22px;font-size:12px;color:var(--muted)}
.foot a{color:var(--muted);text-decoration:underline}
"""


def build_card_css(brief: dict) -> str:
    imp, root, _ = _root_and_fonts(brief)
    return "\n".join([imp, root, CARD_CSS])
