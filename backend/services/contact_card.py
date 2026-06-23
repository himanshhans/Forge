"""
Contact-card rendering: template HTML + random design + QR + vCard.
No LLM — the content is structured, so we render deterministically.
"""
from io import BytesIO
from urllib.parse import quote

import qrcode
import qrcode.image.svg

from .design_agent import design
from .theme import build_card_css


def _esc(s: str) -> str:
    return (
        (s or "")
        .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )


def _vcf_esc(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def build_vcard(card) -> str:
    lines = ["BEGIN:VCARD", "VERSION:3.0", f"FN:{_vcf_esc(card.name)}"]
    if card.headline:
        lines.append(f"TITLE:{_vcf_esc(card.headline)}")
    if card.email:
        lines.append(f"EMAIL;TYPE=INTERNET:{_vcf_esc(card.email)}")
    if card.phone:
        lines.append(f"TEL:{_vcf_esc(card.phone)}")
    if card.location:
        lines.append(f"ADR;TYPE=WORK:;;{_vcf_esc(card.location)};;;;")
    for link in card.links or []:
        if link.get("url"):
            lines.append(f"URL:{_vcf_esc(link['url'])}")
    if card.bio:
        lines.append(f"NOTE:{_vcf_esc(card.bio)}")
    lines.append("END:VCARD")
    return "\r\n".join(lines)


def qr_svg(data: str) -> str:
    qr = qrcode.QRCode(border=1, box_size=10)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    buf = BytesIO()
    img.save(buf)
    return buf.getvalue().decode()


def _monogram(name: str) -> str:
    parts = [p for p in name.split() if p]
    return ((parts[0][0] + (parts[1][0] if len(parts) > 1 else "")) or "?").upper()


def render_card_html(card, published_url: str) -> str:
    avatar = (
        f'<img class="avatar" src="{_esc(card.avatar_url)}" alt="{_esc(card.name)}" />'
        if card.avatar_url
        else f'<div class="avatar">{_esc(_monogram(card.name))}</div>'
    )
    meta = []
    if card.location:
        meta.append(_esc(card.location))
    meta_html = f'<p class="meta">{" · ".join(meta)}</p>' if meta else ""

    link_items = []
    for i, link in enumerate(card.links or []):
        if not link.get("url"):
            continue
        cls = "" if i == 0 else ' class="secondary"'
        link_items.append(f'<a href="{_esc(link["url"])}"{cls} target="_blank" rel="noreferrer">{_esc(link.get("label") or link["url"])}</a>')
    if card.email:
        link_items.append(f'<a href="mailto:{_esc(card.email)}" class="secondary">Email</a>')

    vcf = quote(build_vcard(card))
    qr = qr_svg(published_url) if published_url else ""

    return (
        '<div class="card">'
        f"{avatar}"
        f'<h1 class="name">{_esc(card.name)}</h1>'
        + (f'<p class="headline">{_esc(card.headline)}</p>' if card.headline else "")
        + (f'<p class="bio">{_esc(card.bio)}</p>' if card.bio else "")
        + meta_html
        + f'<div class="links">{"".join(link_items)}'
        f'<a href="data:text/vcard;charset=utf-8,{vcf}" download="{_esc(card.name)}.vcf" class="secondary">Save contact</a>'
        "</div>"
        + (f'<div class="qr">{qr}</div>' if qr else "")
        + '<p class="foot">Made with <a href="https://forge.app">Forge</a></p>'
        "</div>"
    )


def generate_card(card, published_url: str) -> dict:
    """Render a card's html/css using a random design brief. Returns dict."""
    brief = design()
    return {
        "html": render_card_html(card, published_url),
        "css": build_card_css(brief),
        "design": {k: brief[k] for k in ("mode", "layout", "fonts", "palette", "seed")},
    }
