"""
Baked-in portfolio theme. The LLM only emits semantic HTML using the class
vocabulary below + picks an accent color; we always inject this stylesheet so
output looks designed regardless of the model's CSS ability.
"""

# Class vocabulary handed to the LLM (keep in sync with BASE_CSS).
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
Rules: NEVER use <img> (you have no real image URLs) — use <div class="thumb"> blocks instead.
Write real, specific, compelling copy from the user's details. Keep sections that have content; omit empty ones.
"""

BASE_CSS = """
:root{
  --bg:#ffffff; --fg:#181816; --muted:#6b6b66; --border:#ececE6;
  --card:#fafaf7; --accent:#1f5c45; --accent-fg:#ffffff; --maxw:760px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--fg);
  font:17px/1.65 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased;
}
h1,h2,h3{font-family:Georgia,"Times New Roman",serif; font-weight:600; line-height:1.15; letter-spacing:-0.01em; margin:0}
a{color:var(--accent); text-decoration:none}
p{margin:0}

.wrap{max-width:var(--maxw); margin:0 auto; padding:0 24px}

/* hero */
.hero{max-width:var(--maxw); margin:0 auto; padding:96px 24px 56px; text-align:center}
.hero h1{font-size:clamp(40px,7vw,64px)}
.hero .tagline{margin-top:14px; font-size:20px; color:var(--accent); font-weight:500}
.hero .lead{margin:18px auto 0; max-width:52ch; color:var(--muted); font-size:18px}
.cta-row{display:flex; gap:12px; justify-content:center; flex-wrap:wrap; margin-top:32px}

/* buttons */
.btn{display:inline-block; padding:12px 22px; border-radius:10px; font-weight:600; font-size:15px;
  background:var(--accent); color:var(--accent-fg); border:1px solid var(--accent); transition:opacity .15s}
.btn:hover{opacity:.9}
.btn.ghost{background:transparent; color:var(--fg); border-color:var(--border)}

/* sections */
.section{padding:56px 0; border-top:1px solid var(--border)}
.section .wrap>h2:not(.eyebrow){font-size:30px; margin-bottom:24px}
.eyebrow{font-size:12px; font-weight:700; letter-spacing:.16em; text-transform:uppercase;
  color:var(--accent); font-family:inherit; margin-bottom:10px}

/* work grid */
.grid{display:grid; grid-template-columns:repeat(2,1fr); gap:18px}
.card{background:var(--card); border:1px solid var(--border); border-radius:14px; padding:18px; overflow:hidden}
.card .thumb{aspect-ratio:16/10; border-radius:9px; margin:-18px -18px 14px;
  background:linear-gradient(135deg,color-mix(in srgb,var(--accent) 22%,transparent),color-mix(in srgb,var(--accent) 6%,transparent))}
.card h3{font-size:18px; margin-bottom:6px}
.card p{color:var(--muted); font-size:15px}

/* stats */
.stats{display:flex; flex-wrap:wrap; gap:40px}
.stat{display:flex; flex-direction:column}
.stat .num{font-family:Georgia,serif; font-size:40px; color:var(--accent); line-height:1}
.stat .label{margin-top:6px; font-size:13px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted)}

/* quote */
.quote{margin:0; padding:22px 24px; background:var(--card); border-left:3px solid var(--accent); border-radius:0 12px 12px 0}
.quote p{font-size:18px; font-style:italic}
.quote cite{display:block; margin-top:12px; font-style:normal; font-size:14px; color:var(--muted)}
.quote+.quote{margin-top:16px}

/* tags */
.tags{list-style:none; padding:0; margin:0; display:flex; flex-wrap:wrap; gap:8px}
.tags li{padding:6px 12px; border:1px solid var(--border); border-radius:999px; font-size:14px; color:var(--muted)}

/* contact */
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


def build_css(accent: str | None) -> str:
    """Return full stylesheet with the LLM-chosen accent injected."""
    accent = (accent or "").strip()
    if not (accent.startswith("#") and len(accent) in (4, 7)):
        accent = "#1f5c45"  # forest fallback
    return f":root{{--accent:{accent}}}\n{BASE_CSS}"
