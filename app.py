"""Mercados Musicales — app Streamlit con la identidad visual del mockup.

Diseño basado en GUIA_DISENO_MOCKUPS_SPOTIFY.md: navbar flotante, sidebar
blanca, banners menta con foto de concierto, gráficos horizontales y estados.
La lógica de datos se mantiene en pipeline.py.
"""

from __future__ import annotations

import base64
import re
from pathlib import Path

import streamlit as st

from pipeline import (
    GENEROS,
    REGIONES,
    normalizar_entrada,
    ranking_por_region,
    recomendar_region,
)

st.set_page_config(page_title="Mercados Musicales", layout="wide")

# ---------------------------------------------------------------------------
# Recursos
# ---------------------------------------------------------------------------
SPOTIFY_LOGO = """<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
<circle cx="12" cy="12" r="12" fill="#00C96B"/>
<path d="M6.4 9.1c3.7-1.1 7.8-.6 11.2 1.2" stroke="#fff" stroke-width="1.7" stroke-linecap="round"/>
<path d="M6.9 12.2c3.1-.9 6.5-.5 9.4 1" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/>
<path d="M7.5 15.2c2.4-.7 5-.4 7.2.8" stroke="#fff" stroke-width="1.4" stroke-linecap="round"/>
</svg>"""

ICON_NOTE = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
<path d="M9 18V5l10-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="16" cy="16" r="3"/></svg>"""

ICON_BARS = """<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
<rect x="4" y="12" width="4" height="8" rx="1.4"/><rect x="10" y="7" width="4" height="13" rx="1.4"/><rect x="16" y="3" width="4" height="17" rx="1.4"/></svg>"""

ICON_ARROW = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
<path d="M5 12h14M13 6l6 6-6 6"/></svg>"""

ICON_GLOBE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#626D73" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 2.6 15.4 0 18M12 3c-2.6 2.6-2.6 15.4 0 18"/></svg>"""

ICON_INFO = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
<circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><circle cx="12" cy="8" r=".8" fill="currentColor" stroke="none"/></svg>"""

ICON_WARNING = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
<path d="M10.3 3.7 2.5 17.2A2 2 0 0 0 4.2 20h15.6a2 2 0 0 0 1.7-2.8L13.7 3.7a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4"/><circle cx="12" cy="16.5" r=".8" fill="currentColor" stroke="none"/></svg>"""

ICON_CURSOR = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
<path d="M4 3l7 17 2.4-6.6L20 11 4 3Z"/></svg>"""

ICON_MUSIC = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
<path d="M9 18V5l10-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="16" cy="16" r="3"/></svg>"""


def _svg_uri(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode()


@st.cache_data
def _concert_uri() -> str:
    path = Path(__file__).parent / "assets" / "concert.jpg"
    if path.exists():
        return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()
    return ""


CONCERT = f"url('{_concert_uri()}')" if _concert_uri() else "linear-gradient(120deg,#0B5E3B,#00C96B)"
GLOBE_CSS = _svg_uri(ICON_GLOBE)
NOTE_CSS = _svg_uri(ICON_NOTE.replace("currentColor", "#25E68D"))
BARS_CSS = _svg_uri(ICON_BARS.replace("currentColor", "#007A4B"))

# ---------------------------------------------------------------------------
# Sistema de diseño
# ---------------------------------------------------------------------------
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
  --green-primary:#00C96B; --green-bright:#25E68D; --green-deep:#007A4B;
  --green-dark:#103A2F; --mint-100:#E6FAF1; --mint-200:#CEF6E5;
  --canvas:#F3FBF7; --surface:#FFFFFF; --ink:#10191D;
  --text-secondary:#626D73; --chart-neutral:#D0D2D4; --chart-dot:#667078;
  --border:#E5EDE9; --warning:#E5A33E; --warning-bg:#FFF4DC;
  --shadow:0 12px 35px rgba(17,64,43,.07);
}

html, body, [class*="css"], .stApp { font-family:'Inter', Arial, sans-serif; color:var(--ink); }
.stApp {
  background-color:var(--canvas);
  background-image:
    radial-gradient(900px 600px at 6% 18%, rgba(206,246,229,.55), transparent 62%),
    radial-gradient(820px 540px at 96% 26%, rgba(230,250,241,.85), transparent 62%),
    radial-gradient(720px 520px at 50% 102%, rgba(206,246,229,.45), transparent 62%);
  background-attachment:fixed;
}
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer { display:none !important; }
.block-container { max-width:1440px; padding:1.1rem 2rem 2.4rem; position:relative; z-index:1; }
h1, h2, h3, h4 { font-family:'Inter', sans-serif !important; letter-spacing:-.02em; color:var(--ink); }

.mm-bg { position:fixed; inset:0; z-index:-1; pointer-events:none; overflow:hidden; }
.mm-blob { position:absolute; border-radius:50%; background:radial-gradient(circle at 35% 35%, rgba(206,246,229,.85), rgba(206,246,229,0) 70%); }
.mm-blob-1 { width:540px; height:540px; left:-190px; top:6%; }
.mm-blob-2 { width:640px; height:640px; right:-230px; bottom:-140px; }
.mm-eq { position:absolute; bottom:12%; display:flex; align-items:flex-end; gap:6px; opacity:.45; }
.mm-eq-left { left:2.5%; } .mm-eq-right { right:2.5%; }
.mm-eq span { width:8px; border-radius:999px; background:linear-gradient(180deg,var(--mint-200),var(--green-bright)); }
.mm-eq span:nth-child(1){height:24px} .mm-eq span:nth-child(2){height:44px}
.mm-eq span:nth-child(3){height:64px} .mm-eq span:nth-child(4){height:36px}
.mm-eq span:nth-child(5){height:52px} .mm-eq span:nth-child(6){height:22px}
.mm-home-photo {
  position:absolute; right:-80px; top:27%; width:340px; height:340px; border-radius:50%;
  background-image:linear-gradient(160deg, rgba(0,122,75,.55), rgba(37,230,141,.22)), var(--concert);
  background-size:cover; background-position:center; background-blend-mode:multiply;
  box-shadow:0 30px 70px rgba(16,58,47,.18);
}
.mm-cover { position:absolute; width:148px; height:188px; border-radius:14px; padding:10px; background:#fff; box-shadow:0 18px 40px rgba(16,58,47,.18); overflow:hidden; }
.mm-cover svg { width:18px; height:18px; position:absolute; left:12px; bottom:10px; }
.mm-cover-a { left:-32px; bottom:10%; transform:rotate(-12deg); }
.mm-cover-b { left:98px; bottom:1%; transform:rotate(8deg); }
.mm-cover-art { width:100%; height:78%; border-radius:9px; }
.art-a { background:linear-gradient(150deg,#0E5A3C,#25E68D); }
.art-b { background:linear-gradient(150deg,#0B3B2C,#5CD9A0 60%,#D8FAE9); }

.st-key-topnav {
  position:sticky; top:14px; z-index:1000; background:var(--surface);
  border:1px solid var(--border); border-radius:26px; padding:10px 22px;
  box-shadow:var(--shadow); margin-bottom:26px;
}
.mm-brand { display:flex; align-items:center; gap:10px; font-size:16px; font-weight:800; letter-spacing:-.02em; white-space:nowrap; }
.mm-brand svg { width:34px; height:34px; flex:0 0 34px; }
.mm-brand-text { display:flex; flex-direction:column; line-height:1.15; min-width:0; }
.mm-brand-line { display:block; }
.mm-brand-year { color:var(--text-secondary); font-weight:700; }
.mm-mobile-view { display:none; }
.mm-nav-active { position:relative; text-align:center; font-size:14px; font-weight:700; color:var(--ink); padding-bottom:6px; }
.mm-nav-active::after { content:""; position:absolute; left:50%; bottom:0; width:44px; height:3px; border-radius:999px; background:linear-gradient(100deg,#00B862,#27E68A); transform:translateX(-50%); }
.st-key-topnav [data-testid="stPopover"] { display:flex; justify-content:flex-end; }
.st-key-topnav [data-testid="stPopover"] button {
  display:flex; align-items:center; gap:8px; margin-left:auto; padding:4px 0;
  background:transparent !important; border:none !important; box-shadow:none !important;
  color:var(--text-secondary) !important; font-size:13px !important; font-weight:600 !important;
}
.st-key-topnav [data-testid="stPopover"] button::before {
  content:"i"; display:inline-flex; align-items:center; justify-content:center;
  width:18px; height:18px; border-radius:50%; border:1.5px solid var(--text-secondary);
  font-size:11px; font-weight:800;
}
.st-key-topnav [data-testid="stPopover"] button:hover { color:var(--green-deep) !important; }

.mm-home-hero { text-align:center; max-width:940px; margin:4.2rem auto 2.4rem; }
.mm-home-title { font-size:clamp(38px,4.6vw,58px); font-weight:900; line-height:1.06; letter-spacing:-.045em; margin:0 0 16px; }
.mm-grad { background:linear-gradient(100deg,#00B862 0%,#007A4B 100%); -webkit-background-clip:text; background-clip:text; color:transparent; }
.mm-home-sub { font-size:17px; font-weight:500; color:var(--text-secondary); margin:0; }

[class*="st-key-cardlink_genero"], [class*="st-key-cardlink_mercado"] {
  width:100% !important; max-width:860px; margin:0 auto 24px !important;
}
[class*="st-key-cardlink_genero"] button, [class*="st-key-cardlink_mercado"] button {
  width:100% !important; min-height:124px !important; border-radius:22px !important;
  padding:24px 30px !important; display:flex !important; align-items:center !important;
  justify-content:flex-start !important; gap:18px !important; text-align:left !important;
  white-space:normal !important; cursor:pointer !important;
  -webkit-appearance:none !important; appearance:none !important; text-decoration:none !important;
  transition:transform .2s ease, box-shadow .2s ease, background .18s ease !important;
  position:relative !important; overflow:hidden !important;
}
[class*="st-key-cardlink_genero"] button {
  background:radial-gradient(600px 300px at 92% 20%, rgba(37,230,141,.22), transparent 60%), linear-gradient(115deg,#103A2F 0%,#0B2A22 60%,#124C39 100%) !important;
  border:none !important; color:#fff !important;
  box-shadow:0 18px 40px rgba(16,58,47,.18) !important;
}
[class*="st-key-cardlink_mercado"] button {
  background:var(--surface) !important; border:1px solid var(--border) !important;
  color:var(--ink) !important; box-shadow:var(--shadow) !important;
}
[class*="st-key-cardlink_genero"] button:hover, [class*="st-key-cardlink_mercado"] button:hover {
  transform:translateY(-2px) !important;
  box-shadow:0 18px 44px rgba(17,64,43,.16) !important;
}
[class*="st-key-cardlink_genero"] button::before, [class*="st-key-cardlink_mercado"] button::before {
  content:""; width:58px; height:58px; flex:0 0 58px; border-radius:16px;
  background-position:center; background-size:28px 28px; background-repeat:no-repeat;
}
[class*="st-key-cardlink_genero"] button::before {
  background-color:rgba(37,230,141,.12); border:1px solid rgba(37,230,141,.25);
  background-image:url("__NOTE_ICON__");
}
[class*="st-key-cardlink_mercado"] button::before {
  background-color:var(--mint-100); border:1px solid transparent;
  background-image:url("__BARS_ICON__");
}
[class*="st-key-cardlink_genero"] button::after, [class*="st-key-cardlink_mercado"] button::after {
  content:"→"; width:56px; height:56px; flex:0 0 56px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-size:24px; font-weight:800; line-height:1; margin-left:auto;
}
[class*="st-key-cardlink_genero"] button::after {
  background:linear-gradient(100deg,#00B862,#27E68A); color:#062318;
}
[class*="st-key-cardlink_mercado"] button::after {
  background:var(--mint-100); color:var(--green-deep);
}
[class*="st-key-cardlink_genero"] button [data-testid="stMarkdownContainer"],
[class*="st-key-cardlink_mercado"] button [data-testid="stMarkdownContainer"] {
  flex:1 1 auto !important; text-align:left !important; min-width:0 !important;
  font-size:clamp(20px,2.2vw,27px) !important; font-weight:800 !important;
  letter-spacing:-.03em !important; line-height:1.15 !important;
}
[class*="st-key-cardlink_genero"] button [data-testid="stMarkdownContainer"] { color:#fff !important; }
[class*="st-key-cardlink_mercado"] button [data-testid="stMarkdownContainer"] { color:var(--ink) !important; }
[class*="st-key-cardlink_genero"] button p,
[class*="st-key-cardlink_mercado"] button p {
  font-size:inherit !important; font-weight:inherit !important;
  letter-spacing:inherit !important; line-height:inherit !important; margin:0 !important;
  text-align:left !important; white-space:normal !important;
}
[class*="st-key-cardlink_genero"] button p { color:#fff !important; }
[class*="st-key-cardlink_mercado"] button p { color:var(--ink) !important; }
[class*="st-key-cardlink_genero"] button:focus-visible,
[class*="st-key-cardlink_mercado"] button:focus-visible {
  outline:3px solid rgba(0,201,107,.55) !important; outline-offset:-4px !important;
  border-radius:22px !important;
}

.stButton > button, .stFormSubmitButton > button {
  font-family:'Inter', sans-serif; font-weight:700; border-radius:10px;
  border:1px solid var(--border); background:var(--surface); color:var(--ink);
  transition:all .18s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover { border-color:var(--green-primary); color:var(--green-deep); }
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
  background:linear-gradient(100deg,#00B862,#27E68A) !important; border:none !important;
  color:#062318 !important; box-shadow:0 8px 20px rgba(0,184,98,.18);
}
.stButton > button:focus-visible, .stFormSubmitButton > button:focus-visible,
.stSelectbox div[data-baseweb="select"]:focus-within, .stTextInput input:focus {
  outline:3px solid rgba(0,201,107,.35) !important; outline-offset:2px;
}
.st-key-sidebar {
  background:var(--surface); border:1px solid var(--border); border-radius:22px;
  padding:26px 24px; box-shadow:var(--shadow); min-height:620px; position:sticky; top:104px;
}
.mm-field-label { font-size:13px; font-weight:700; color:var(--text-secondary); margin:0 0 8px; }
.mm-second { font-size:15px; font-weight:700; color:var(--ink); line-height:1.4; }
.mm-second span { color:var(--text-secondary); font-weight:500; }
.mm-muted { color:var(--text-secondary); font-weight:500; }
.mm-sep { height:1px; background:var(--border); margin:20px 0; }
.mm-sidebar-spacer { height:clamp(50px, 12vh, 130px); }
.mm-sidebar-deco { position:relative; height:120px; margin-top:16px; border-radius:16px; overflow:hidden; background:linear-gradient(180deg,rgba(230,250,241,0),rgba(230,250,241,.75)); }
.mm-deco-eq { position:absolute; left:18px; bottom:14px; display:flex; align-items:flex-end; gap:5px; opacity:.65; }
.mm-deco-eq span { width:7px; border-radius:999px; background:linear-gradient(180deg,var(--mint-200),var(--green-bright)); }
.mm-deco-circle { position:absolute; right:-40px; top:-30px; width:130px; height:130px; border-radius:50%; border:1px solid rgba(0,122,75,.15); }
.mm-help, .mm-warning-note { display:flex; gap:9px; align-items:flex-start; font-size:13px; line-height:1.45; margin:14px 0 0; }
.mm-help { color:var(--text-secondary); }
.mm-help svg, .mm-warning-note svg { width:17px; height:17px; flex:0 0 17px; margin-top:1px; }
.mm-warning-note { color:#7A5714; background:var(--warning-bg); border:1px solid rgba(229,163,62,.35); border-radius:10px; padding:10px 11px; }

[data-baseweb="select"] > div { background:var(--surface) !important; border:1px solid var(--border) !important; border-radius:10px !important; min-height:46px; }
[data-baseweb="select"] > div:focus-within { border-color:var(--green-primary) !important; box-shadow:0 0 0 3px rgba(0,201,107,.15) !important; }
[data-baseweb="popover"] [role="listbox"] { border-radius:10px; border:1px solid var(--border); box-shadow:var(--shadow); }
[data-baseweb="popover"] [role="option"]:hover, [aria-selected="true"] { background:var(--mint-100) !important; color:var(--ink) !important; }
#stFloatingOverlayPortal { background:transparent !important; }
[data-testid="stPopoverBody"] {
  background:var(--surface) !important; color:var(--ink) !important;
  border-radius:14px !important; border:1px solid var(--border) !important;
  box-shadow:var(--shadow) !important;
}
[data-testid="stPopoverBody"] * { color:#26332D !important; }
[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"],
[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] { background:transparent !important; }
[data-testid="stPopoverBody"] strong, [data-testid="stPopoverBody"] b { color:var(--ink) !important; }
[data-testid="stPopoverBody"] li::marker { color:var(--green-primary) !important; }
.stTextInput input {
  background:var(--surface) !important; border:1px solid var(--border) !important;
  border-radius:10px !important; font-size:14px; color:var(--ink) !important;
  -webkit-text-fill-color:var(--ink) !important;
}
.stTextInput input::placeholder { color:#4F5B56 !important; opacity:1 !important; -webkit-text-fill-color:#4F5B56 !important; }
[data-baseweb="select"] > div, [data-baseweb="select"] span { color:var(--ink) !important; }
.st-key-sidebar .stFormSubmitButton > button { height:38px; min-height:38px; font-size:13px; background:var(--mint-100) !important; border:none !important; color:var(--green-deep) !important; }
.st-key-sidebar [class*="st-key-back_"] button {
  background:transparent !important; border:none !important; box-shadow:none !important;
  color:var(--text-secondary) !important; padding:0 !important; min-height:auto !important;
  height:auto !important; font-size:14px !important; font-weight:600 !important; justify-content:flex-start !important;
}
.st-key-sidebar [class*="st-key-back_"] button:hover { color:var(--green-deep) !important; background:transparent !important; }
.st-key-sidebar [class*="st-key-ver_evidencia"] button {
  background:var(--surface) !important; border:1.8px solid var(--green-dark) !important;
  color:var(--green-dark) !important; height:46px; border-radius:10px !important; font-weight:800 !important;
}
.st-key-sidebar [class*="st-key-ver_evidencia"] button:hover { background:var(--mint-100) !important; }
.st-key-sidebar [class*="st-key-explorar_region"] button {
  background:transparent !important; border:none !important; box-shadow:none !important;
  color:var(--text-secondary) !important; font-size:13px !important; font-weight:600 !important;
  padding:0 !important; min-height:auto !important; height:auto !important;
  justify-content:flex-start !important; display:flex; align-items:center; gap:8px;
}
.st-key-sidebar [class*="st-key-explorar_region"] button::before { content:""; width:16px; height:16px; flex:0 0 16px; background:url("__GLOBE__") center / contain no-repeat; }
.st-key-sidebar [class*="st-key-explorar_region"] button:hover { color:var(--green-deep) !important; }

.mm-banner {
  position:relative; overflow:hidden; border-radius:20px; min-height:232px;
  padding:32px 36px; display:flex; align-items:center;
  background:linear-gradient(110deg,#F0FFF8 0%,#D8FAE9 58%,#B9F4D8 100%);
  box-shadow:var(--shadow);
}
.mm-banner::after { content:""; position:absolute; right:16%; top:-42%; width:380px; height:380px; border-radius:50%; border:1px solid rgba(0,122,75,.15); z-index:0; }
.mm-banner-photo {
  position:absolute; right:0; top:0; bottom:0; width:42%; z-index:1;
  background-image:linear-gradient(115deg, rgba(7,58,43,.58), rgba(0,201,107,.22)), var(--concert);
  background-size:cover; background-position:center; background-blend-mode:multiply;
  border-top-left-radius:220px; border-bottom-left-radius:220px;
}
.mm-banner-photo::after { content:""; position:absolute; inset:0; background:radial-gradient(circle at 70% 20%, rgba(37,230,141,.25), transparent 60%); }
.mm-banner-copy { position:relative; z-index:2; max-width:62%; }
.mm-banner-title { font-size:clamp(30px,3.4vw,52px); font-weight:900; line-height:1.06; letter-spacing:-.045em; margin:0 0 12px; color:var(--ink); }
.mm-green { color:var(--green-deep); }
.mm-banner-sub { font-size:16px; font-weight:500; line-height:1.45; color:#3D4A44; margin:0 0 16px; max-width:620px; }
.mm-chip {
  display:inline-flex; align-items:center; gap:9px; padding:9px 14px; border-radius:999px;
  font-size:13px; font-weight:600; line-height:1.3; color:#16352A;
  background:rgba(255,255,255,.8); border:1px solid rgba(0,201,107,.22);
  box-shadow:0 6px 18px rgba(17,64,43,.06);
}
.mm-chip b { font-weight:800; }
.mm-chip svg { width:16px; height:16px; flex:0 0 16px; color:var(--green-primary); }
.mm-chip.amber { background:var(--warning-bg); border-color:rgba(229,163,62,.4); color:#5A4214; }
.mm-chip.amber svg { color:var(--warning); }

.st-key-chart_afinidad, .st-key-chart_evidencia, .st-key-chart_ranking {
  background:var(--surface); border:1px solid var(--border); border-radius:20px;
  padding:28px 30px; box-shadow:var(--shadow);
}
.mm-card-head { display:flex; justify-content:space-between; align-items:flex-start; gap:16px; margin-bottom:22px; }
.mm-card-title { font-size:22px; font-weight:800; letter-spacing:-.02em; line-height:1.2; }
.mm-card-note { font-size:12px; color:var(--text-secondary); white-space:nowrap; padding-top:4px; }
.mm-bars { display:flex; flex-direction:column; }
.mm-bar-row { display:grid; grid-template-columns:150px 1fr 112px; align-items:center; gap:18px; padding:9px 0; }
.mm-bar-label { font-size:15px; font-weight:600; color:var(--ink); }
.mm-bar-track { position:relative; height:44px; }
.mm-bar-track::before { content:""; position:absolute; left:var(--ref); top:-14px; bottom:-14px; border-left:1.5px dashed #667078; opacity:.45; z-index:2; }
.mm-bar { height:100%; border-radius:6px; position:relative; z-index:1; transition:filter .18s ease; }
.mm-bar-row:hover .mm-bar { filter:brightness(1.06); }
.mm-bar-value { font-size:15px; font-weight:800; font-variant-numeric:tabular-nums; white-space:nowrap; }
.mm-bar-value span { margin-left:6px; font-size:12px; font-weight:500; color:var(--text-secondary); }

.mm-ev-chart { margin-top:4px; }
.mm-ev-row { display:grid; grid-template-columns:140px 1fr 180px; align-items:center; gap:18px; height:54px; }
.mm-ev-track { position:relative; height:100%; }
.mm-ev-track::before { content:""; position:absolute; left:var(--ref); top:0; bottom:0; border-left:1.5px dashed #667078; opacity:.5; z-index:1; }
.mm-ev-seg { position:absolute; top:50%; transform:translateY(-50%); height:8px; border-radius:999px; opacity:.45; z-index:2; }
.mm-ev-dot { position:absolute; top:50%; transform:translate(-50%,-50%); width:14px; height:14px; border-radius:50%; border:3px solid #fff; box-shadow:0 0 0 1px #fff; z-index:3; }
.mm-ev-meta { font-size:12px; color:var(--text-secondary); text-align:right; line-height:1.4; }
.mm-ev-meta b { font-weight:800; }
.mm-ev-axis-row { display:grid; grid-template-columns:140px 1fr 180px; gap:18px; margin-top:2px; }
.mm-ev-axis { position:relative; height:26px; border-top:1px solid var(--border); }
.mm-ev-axis span { position:absolute; top:5px; transform:translateX(-50%); font-size:11px; color:var(--text-secondary); }
.mm-ev-axis-title { margin:4px 0 0 158px; font-size:12px; color:var(--text-secondary); }

.mm-info-note { display:flex; gap:10px; align-items:flex-start; margin-top:20px; padding:13px 15px; border-radius:12px; background:var(--mint-100); border:1px solid rgba(0,201,107,.18); color:#16352A; font-size:13px; line-height:1.5; }
.mm-info-note svg { width:18px; height:18px; flex:0 0 18px; margin-top:1px; color:var(--green-deep); }
.mm-final-note { margin-top:12px; font-size:12px; color:var(--text-secondary); }

[class*="st-key-rankrow_"] { padding:3px 8px; border-radius:12px; transition:background .18s ease; }
[class*="st-key-rankrow_"]:hover { background:var(--canvas); }
.mm-rank-label { font-size:14px; font-weight:700; color:var(--ink); }
.mm-rank-track { height:30px; }
.mm-rank-bar { height:100%; border-radius:5px; transition:filter .18s ease; }
[class*="st-key-rankrow_"]:hover .mm-rank-bar { filter:brightness(1.05); }
.mm-rank-value { font-size:14px; font-weight:800; font-variant-numeric:tabular-nums; white-space:nowrap; }
.mm-rank-value span { margin-left:7px; font-size:12px; font-weight:500; color:var(--text-secondary); }
.mm-mini-warn { display:flex; align-items:center; gap:4px; margin-top:2px; font-size:11px; font-weight:700; color:#8A6219; }
.mm-mini-warn svg { width:13px; height:13px; }
[class*="st-key-ir_"] button {
  width:32px !important; height:32px !important; min-height:32px !important; padding:0 !important;
  border-radius:50% !important; background:var(--surface) !important; border:1px solid var(--border) !important;
  color:var(--green-deep) !important; font-size:15px !important;
}
[class*="st-key-ir_"] button:hover { background:var(--mint-100) !important; border-color:var(--green-primary) !important; }

.mm-note { display:flex; gap:10px; align-items:flex-start; margin:14px 0; padding:13px 15px; border-radius:12px; background:var(--mint-100); border:1px solid rgba(0,201,107,.2); color:#16352A; font-size:14px; line-height:1.45; }
.mm-note svg { width:18px; height:18px; flex:0 0 18px; margin-top:1px; }
.mm-note-warn { background:var(--warning-bg); border-color:rgba(229,163,62,.4); color:#5A4214; }
.mm-chip-row { display:flex; flex-wrap:wrap; gap:8px; margin-top:4px; }
.mm-chip-mini { padding:5px 10px; border-radius:999px; background:var(--mint-100); border:1px solid rgba(0,201,107,.2); font-size:12px; font-weight:600; color:#16352A; }
.mm-empty { background:var(--surface); border:1px solid var(--border); border-radius:20px; padding:52px 30px; text-align:center; box-shadow:var(--shadow); }
.mm-empty-icon { width:64px; height:64px; margin:0 auto 16px; border-radius:50%; background:var(--mint-100); display:flex; align-items:center; justify-content:center; color:var(--green-deep); }
.mm-empty-icon svg { width:28px; height:28px; }
.mm-empty-title { font-size:22px; font-weight:800; letter-spacing:-.02em; margin:0 0 8px; }
.mm-empty-desc { font-size:14px; color:var(--text-secondary); margin:0; }

.mm-footer { display:flex; align-items:center; gap:14px; justify-content:center; max-width:920px; margin:48px auto 8px; text-align:center; color:var(--text-secondary); font-size:12px; }
.mm-footer::before, .mm-footer::after { content:""; height:1px; background:var(--border); flex:1; min-width:30px; }

@media (max-width: 1200px) { .mm-home-photo, .mm-cover { display:none; } }
@media (max-width: 900px) {
  .st-key-topnav { padding:8px 14px; border-radius:20px; }
  .mm-brand { font-size:14px; gap:8px; } .mm-brand svg { width:28px; height:28px; flex-basis:28px; }
  .mm-brand-year { display:none; } .mm-nav-active { font-size:12px; }
  .mm-banner { min-height:auto; padding:26px 22px; } .mm-banner-copy { max-width:100%; }
  .mm-banner-photo { width:55%; opacity:.32; } .mm-banner-title { font-size:clamp(28px,6vw,40px); }
  .st-key-sidebar { position:static; min-height:auto; } .mm-sidebar-spacer { height:24px; }
  .mm-home-title { font-size:clamp(34px,8vw,46px); }
  .mm-bar-row { grid-template-columns:110px 1fr 94px; gap:10px; }
  .mm-ev-row { grid-template-columns:100px 1fr 120px; gap:10px; }
  .mm-ev-axis-row { grid-template-columns:100px 1fr 120px; gap:10px; }
  .mm-ev-axis-title { margin-left:110px; }
  .mm-eq { display:none; }
}
@media (max-width: 640px) {
  .block-container { padding:.8rem .9rem 2rem; }
  .mm-banner-title { font-size:30px; } .mm-banner-sub { font-size:14px; }
  .mm-chip { font-size:12px; padding:8px 11px; }
  .mm-bar-row { grid-template-columns:88px 1fr 80px; gap:8px; }
  .mm-bar-label { font-size:13px; } .mm-bar-track { height:34px; }
  .mm-ev-row { grid-template-columns:86px 1fr; } .mm-ev-meta { grid-column:1 / -1; text-align:left; margin-top:-8px; }
  .mm-ev-axis-row { grid-template-columns:86px 1fr; } .mm-ev-axis-row > div:last-child { display:none; }
  .mm-ev-axis-title { margin-left:96px; }
  .mm-card-head { flex-direction:column; gap:4px; } .mm-card-note { white-space:normal; }
  [class*="st-key-cardlink_genero"] button, [class*="st-key-cardlink_mercado"] button {
    min-height:104px !important; padding:18px 16px !important; gap:12px !important; border-radius:18px !important;
  }
  [class*="st-key-cardlink_genero"] button::before, [class*="st-key-cardlink_mercado"] button::before {
    width:48px !important; height:48px !important; flex-basis:48px !important; background-size:24px 24px !important;
  }
  [class*="st-key-cardlink_genero"] button::after, [class*="st-key-cardlink_mercado"] button::after {
    width:46px !important; height:46px !important; flex-basis:46px !important; font-size:20px !important;
  }
  [class*="st-key-cardlink_genero"] button p, [class*="st-key-cardlink_mercado"] button p { font-size:18px !important; }
  .st-key-chart_afinidad, .st-key-chart_evidencia, .st-key-chart_ranking { padding:22px 16px; }
  .st-key-topnav [data-testid="stPopover"] button { font-size:0 !important; }
  .st-key-topnav [data-testid="stPopover"] button::before { font-size:13px; }
}
@media (max-width: 640px) {
  .st-key-topnav { top:8px; padding:8px 12px; border-radius:18px; }
  .st-key-topnav [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; align-items:center !important; gap:6px !important; }
  .st-key-topnav [data-testid="stColumn"]:nth-child(1) { flex:1 1 auto !important; width:auto !important; min-width:0 !important; }
  .st-key-topnav [data-testid="stColumn"]:nth-child(2) { display:none !important; }
  .st-key-topnav [data-testid="stColumn"]:nth-child(3) { flex:0 0 auto !important; width:auto !important; }
  .mm-brand { white-space:normal; }
  .mm-brand-line { font-size:13px; }
  .mm-mobile-view { display:block; font-size:10.5px; color:var(--text-secondary); font-weight:600; }

  .mm-home-hero { margin:2.4rem auto 1.6rem; }
  .mm-home-title { font-size:clamp(30px,9vw,40px); }
  .mm-home-sub { font-size:15px; }

  .mm-banner { padding:24px 18px; border-radius:18px; }
  .mm-banner-photo, .mm-banner::after { display:none; }
  .mm-banner-copy { max-width:100%; }
  .mm-banner-title { font-size:clamp(26px,8vw,34px); }
  .mm-banner-sub { font-size:14px; margin-bottom:12px; }
  .mm-chip { display:flex; width:100%; border-radius:14px; align-items:flex-start; }

  .st-key-sidebar { padding:18px 16px; border-radius:18px; }
  .mm-sidebar-deco { height:86px; }

  .mm-bar-row { grid-template-columns:82px 1fr 74px; gap:7px; }
  .mm-bar-label { font-size:12px; }
  .mm-bar-value { font-size:12px; }
  .mm-bar-value span { display:block; margin-left:0; font-size:10px; }
  .mm-bar-track { height:30px; }

  .mm-ev-row { grid-template-columns:76px 1fr; gap:8px; height:48px; }
  .mm-ev-meta { font-size:10.5px; }
  .mm-ev-axis-row { grid-template-columns:76px 1fr; }
  .mm-ev-axis-title { margin-left:84px; font-size:11px; }

  [class*="st-key-rankrow_"] [data-testid="stHorizontalBlock"] { flex-wrap:nowrap !important; gap:4px !important; align-items:center !important; }
  [class*="st-key-rankrow_"] [data-testid="stColumn"] { min-width:0 !important; }
  [class*="st-key-rankrow_"] [data-testid="stColumn"]:nth-child(1) { flex:0 0 56px !important; width:56px !important; }
  [class*="st-key-rankrow_"] [data-testid="stColumn"]:nth-child(2) { flex:1 1 auto !important; width:auto !important; }
  [class*="st-key-rankrow_"] [data-testid="stColumn"]:nth-child(3) { flex:0 0 76px !important; width:76px !important; }
  [class*="st-key-rankrow_"] [data-testid="stColumn"]:nth-child(4) { flex:0 0 30px !important; width:30px !important; }
  .mm-rank-label { font-size:11.5px; }
  .mm-rank-value { font-size:11.5px; }
  .mm-rank-value span { display:block; margin-left:0; font-size:10px; }
  .mm-rank-track { height:22px; }
  [class*="st-key-ir_"] button { width:28px !important; height:28px !important; min-height:28px !important; font-size:13px !important; }

  [data-testid="stPopoverBody"] { max-width:calc(100vw - 28px) !important; max-height:72vh; overflow:auto; }
  [data-testid="stPopoverBody"] p, [data-testid="stPopoverBody"] li { font-size:13px !important; line-height:1.45 !important; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition:none !important; animation:none !important; }
}
""".replace("__GLOBE__", GLOBE_CSS).replace("__NOTE_ICON__", NOTE_CSS).replace("__BARS_ICON__", BARS_CSS)

st.markdown(
    f"<style>{CSS}\n:root{{--concert:{CONCERT};}}</style>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Estado y navegación
# ---------------------------------------------------------------------------
for _key, _default in {
    "pantalla": "P0",
    "historial": [],
    "genero": None,
    "entrada_texto": "",
    "pending_genero": None,
}.items():
    if _key not in st.session_state:
        st.session_state[_key] = _default


def navegar(destino: str) -> None:
    actual = st.session_state.pantalla
    if actual != destino:
        st.session_state.historial.append(actual)
        st.session_state.pantalla = destino
    st.rerun()


def ir_inicio() -> None:
    st.session_state.historial = []
    st.session_state.pantalla = "P0"
    st.rerun()


def abrir_recomendacion(genero: str | None = None) -> None:
    if genero:
        st.session_state.genero = genero
        st.session_state.sel_genero = genero
        st.session_state.entrada_texto = ""
    navegar("P1")


def _cambiar_genero() -> None:
    st.session_state.genero = st.session_state.sel_genero
    st.session_state.entrada_texto = ""


def _cambiar_genero_ev() -> None:
    st.session_state.genero = st.session_state.sel_genero_ev


def _aceptar_genero(valor: str) -> None:
    st.session_state.genero = valor
    st.session_state.sel_genero = valor
    st.session_state.entrada_texto = ""


def _slug(texto: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", texto.lower()).strip("_")


def porcentaje(valor: float) -> str:
    return f"{valor:+.0f} %"


def fmt_millones(valor: float) -> str:
    return f"{valor / 1_000_000:.3f}".replace(".", ",")


# ---------------------------------------------------------------------------
# Piezas visuales
# ---------------------------------------------------------------------------
def fondo(home: bool = False) -> None:
    eq = "".join("<span></span>" for _ in range(6))
    covers = ""
    photo = ""
    if home:
        covers = (
            f'<div class="mm-cover mm-cover-a"><div class="mm-cover-art art-a"></div>{SPOTIFY_LOGO}</div>'
            f'<div class="mm-cover mm-cover-b"><div class="mm-cover-art art-b"></div>{SPOTIFY_LOGO}</div>'
        )
        photo = '<div class="mm-home-photo" aria-hidden="true"></div>'
    st.markdown(
        f'<div class="mm-bg" aria-hidden="true">'
        f'<div class="mm-eq mm-eq-left">{eq}</div><div class="mm-eq mm-eq-right">{eq}</div>'
        f'<div class="mm-blob mm-blob-1"></div><div class="mm-blob mm-blob-2"></div>'
        f"{covers}{photo}</div>",
        unsafe_allow_html=True,
    )


def barra_superior(vista: str) -> None:
    with st.container(key="topnav"):
        izq, centro, der = st.columns([1.6, 2.2, 1.6], vertical_alignment="center")
        with izq:
            st.markdown(
                f'<div class="mm-brand">{SPOTIFY_LOGO}<span class="mm-brand-text">'
                f'<span class="mm-brand-line">Mercados Musicales '
                f'<span class="mm-brand-year">· Spotify 2024</span></span>'
                f'<span class="mm-mobile-view">{vista}</span></span></div>',
                unsafe_allow_html=True,
            )
        with centro:
            st.markdown(f'<div class="mm-nav-active">{vista}</div>', unsafe_allow_html=True)
        with der:
            with st.popover("Acerca de los datos"):
                st.markdown(
                    "**Mercados Musicales** compara 10 géneros en 4 regiones culturales "
                    "(Latinoamérica, Anglosajón, Asia y Europa continental).\n\n"
                    "- Base: 500 registros sintéticos de Spotify 2024 (Kaggle, Apache 2.0).\n"
                    "- Índice de afinidad: 100 = promedio del género.\n"
                    "- Probabilidad: 5.000 escenarios bootstrap precalculados.\n\n"
                    "Los datos son sintéticos y los resultados son exploratorios: "
                    "no describen el mercado real."
                )


def nota(kind: str, texto: str) -> None:
    icono = ICON_WARNING if kind in ("warning", "error") else ICON_INFO
    clase = "mm-note mm-note-warn" if kind in ("warning", "error") else "mm-note"
    st.markdown(
        f'<div class="{clase}">{icono}<span>{texto}</span></div>',
        unsafe_allow_html=True,
    )


def empty_state(titulo: str, descripcion: str, icono: str) -> None:
    st.markdown(
        f'<div class="mm-empty"><div class="mm-empty-icon">{icono}</div>'
        f'<h2 class="mm-empty-title">{titulo}</h2><p class="mm-empty-desc">{descripcion}</p></div>',
        unsafe_allow_html=True,
    )


def evidence_chip(evidencia: str, prob: int) -> str:
    variant = "" if evidencia == "Alta" else " amber"
    return (
        f'<div class="mm-chip{variant}">{ICON_BARS}<span><b>Evidencia {evidencia.lower()}</b> '
        f"· mejor región en {prob} % de 5.000 escenarios simulados</span></div>"
    )


def banner(titulo_html: str, subtitulo: str, chip_html: str = "") -> None:
    st.markdown(
        f'<div class="mm-banner"><div class="mm-banner-photo" aria-hidden="true"></div>'
        f'<div class="mm-banner-copy"><h1 class="mm-banner-title">{titulo_html}</h1>'
        f'<p class="mm-banner-sub">{subtitulo}</p>{chip_html}</div></div>',
        unsafe_allow_html=True,
    )


def sidebar_deco() -> None:
    alturas = [22, 38, 54, 30, 44, 18, 36]
    bars = "".join(f'<span style="height:{h}px"></span>' for h in alturas)
    st.markdown(
        f'<div class="mm-sidebar-deco" aria-hidden="true"><div class="mm-deco-eq">{bars}</div>'
        f'<div class="mm-deco-circle"></div></div>',
        unsafe_allow_html=True,
    )


def affinity_chart(rec: dict) -> None:
    detalle = sorted(rec["detalle"], key=lambda d: d["afinidad"], reverse=True)
    scale = max(160.0, max(d["afinidad"] for d in detalle) + 10)
    ref = 100 / scale * 100
    baja = rec["evidencia"] == "Baja"
    filas = []
    for i, d in enumerate(detalle):
        verde = i < 2 if baja else d["region"] == rec["region_recomendada"]
        color = "var(--green-primary)" if verde else "var(--chart-neutral)"
        valor_color = "var(--green-deep)" if verde else "var(--ink)"
        ancho = d["afinidad"] / scale * 100
        filas.append(
            f'<div class="mm-bar-row" title="{d["region"]}: afinidad {d["afinidad"]:.0f} · n={d["n_registros"]}">'
            f'<div class="mm-bar-label">{d["region"]}</div>'
            f'<div class="mm-bar-track" style="--ref:{ref:.2f}%">'
            f'<div class="mm-bar" style="width:{ancho:.2f}%; background:{color};"></div></div>'
            f'<div class="mm-bar-value" style="color:{valor_color};">{d["afinidad"]:.0f}'
            f'<span>n={d["n_registros"]}</span></div></div>'
        )
    st.markdown(
        '<div class="mm-card-head"><div class="mm-card-title">Índice de afinidad por región</div>'
        '<div class="mm-card-note">promedio del género = 100</div></div>'
        f'<div class="mm-bars">{"".join(filas)}</div>',
        unsafe_allow_html=True,
    )


def evidence_chart(rec: dict) -> None:
    detalle = sorted(rec["detalle"], key=lambda d: d["afinidad"], reverse=True)
    lo = min(60, int(min(d["intervalo_inf"] for d in detalle) // 10 * 10))
    hi = max(160, int((max(d["intervalo_sup"] for d in detalle) + 9) // 10 * 10))
    span = hi - lo
    ref = (100 - lo) / span * 100
    filas = []
    for d in detalle:
        verde = d["region"] == rec["region_recomendada"]
        color = "var(--green-primary)" if verde else "var(--chart-dot)"
        left = (d["intervalo_inf"] - lo) / span * 100
        width = (d["intervalo_sup"] - d["intervalo_inf"]) / span * 100
        dot = (d["afinidad"] - lo) / span * 100
        prob = round(d["prob_mejor"] * 100)
        prob_color = "var(--green-deep)" if verde else "var(--ink)"
        filas.append(
            f'<div class="mm-ev-row"><div class="mm-bar-label">{d["region"]}</div>'
            f'<div class="mm-ev-track" style="--ref:{ref:.2f}%">'
            f'<div class="mm-ev-seg" style="left:{left:.2f}%; width:{width:.2f}%; background:{color};"></div>'
            f'<div class="mm-ev-dot" style="left:{dot:.2f}%; background:{color};"></div></div>'
            f'<div class="mm-ev-meta">mejor región en <b style="color:{prob_color};">{prob} %</b> · n={d["n_registros"]}</div></div>'
        )
    ticks = list(range(int(lo), int(hi) + 1, 20))
    if ticks[-1] != int(hi):
        ticks.append(int(hi))
    tick_html = "".join(
        f'<span style="left:{(t - lo) / span * 100:.2f}%">{t}</span>' for t in ticks
    )
    st.markdown(
        '<div class="mm-card-head"><div class="mm-card-title">Índice de afinidad por región</div>'
        '<div class="mm-card-note">intervalo del 90 %</div></div>'
        f'<div class="mm-ev-chart">{"".join(filas)}'
        f'<div class="mm-ev-axis-row"><div></div><div class="mm-ev-axis">{tick_html}</div><div></div></div>'
        '<div class="mm-ev-axis-title">Índice de afinidad (intervalo del 90 %)</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="mm-info-note">{ICON_INFO}<span><b>Cómo leerlo:</b> el punto es la afinidad observada; '
        "la línea, el rango en el 90 % de los 5.000 remuestreos. Si la línea cruza 100, la región no se "
        "distingue claramente del promedio del género.</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="mm-final-note">Datos sintéticos (Kaggle, Apache 2.0). Resultados exploratorios, '
        "no representan el mercado real.</div>",
        unsafe_allow_html=True,
    )


def ranking_chart(ranking) -> None:
    max_v = float(ranking["promedio_streams"].max())
    lider = ranking.iloc[0]["genero"]
    with st.container(key="chart_ranking"):
        st.markdown(
            '<div class="mm-card-head"><div class="mm-card-title">Promedio de Total Streams '
            'por registro (millones)</div><div class="mm-card-note">ordenado de mayor a menor</div></div>',
            unsafe_allow_html=True,
        )
        for _, fila in ranking.iterrows():
            genero = fila["genero"]
            n = int(fila["n_registros"])
            valor = float(fila["promedio_streams"])
            slug = _slug(genero)
            with st.container(key=f"rankrow_{slug}"):
                c1, c2, c3, c4 = st.columns([1.35, 4.0, 1.25, 0.42], vertical_alignment="center", gap="small")
                with c1:
                    st.markdown(f'<div class="mm-rank-label">{genero}</div>', unsafe_allow_html=True)
                with c2:
                    ancho = valor / max_v * 100
                    color = (
                        "linear-gradient(90deg,#00B862,#27E68A)"
                        if genero == lider
                        else "var(--chart-neutral)"
                    )
                    st.markdown(
                        f'<div class="mm-rank-track"><div class="mm-rank-bar" '
                        f'style="width:{ancho:.2f}%; background:{color};"></div></div>',
                        unsafe_allow_html=True,
                    )
                with c3:
                    aviso = (
                        f'<div class="mm-mini-warn">{ICON_WARNING}<span>n&lt;5</span></div>'
                        if n < 5
                        else ""
                    )
                    st.markdown(
                        f'<div class="mm-rank-value">{fmt_millones(valor)}<span>n={n}</span></div>{aviso}',
                        unsafe_allow_html=True,
                    )
                with c4:
                    if st.button("→", key=f"ir_{slug}", help=f"Ver recomendación de {genero}"):
                        abrir_recomendacion(genero)


def pie() -> None:
    st.markdown(
        '<div class="mm-footer"><span>Basado en 500 registros de Spotify 2024 agrupados en 4 regiones '
        "· Datos sintéticos (Kaggle, licencia Apache 2.0)</span></div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Pantalla A — Inicio
# ---------------------------------------------------------------------------
def pantalla_inicio() -> None:
    fondo(home=True)
    barra_superior("Inicio")
    st.markdown(
        '<div class="mm-home-hero"><h1 class="mm-home-title">¿Qué quieres '
        '<span class="mm-grad">decidir hoy</span>?</h1>'
        '<p class="mm-home-sub">Elige el punto de partida de tu decisión de promoción.</p></div>',
        unsafe_allow_html=True,
    )
    if st.button("Tengo un género  →  ¿dónde lo promuevo?", key="cardlink_genero"):
        abrir_recomendacion()
    if st.button("Tengo un mercado  →  ¿qué géneros funcionan allí?", key="cardlink_mercado"):
        navegar("P3")


# ---------------------------------------------------------------------------
# Pantalla B — Recomendación por género
# ---------------------------------------------------------------------------
def _sidebar_recomendacion() -> None:
    with st.container(key="sidebar"):
        if st.button("← Inicio", key="back_inicio_p1"):
            ir_inicio()
        st.markdown('<div class="mm-field-label">Género</div>', unsafe_allow_html=True)
        if "sel_genero" not in st.session_state and st.session_state.genero:
            st.session_state.sel_genero = st.session_state.genero
        st.selectbox(
            "Género", GENEROS, index=None, key="sel_genero", placeholder="Elige un género",
            on_change=_cambiar_genero, label_visibility="collapsed",
        )
        with st.form("buscar_genero", clear_on_submit=False, border=False):
            texto = st.text_input(
                "Buscar género, país o región", placeholder="Género, país o región",
                label_visibility="collapsed",
            )
            buscar = st.form_submit_button("Buscar", width="stretch")
        if buscar:
            norm = normalizar_entrada(texto)
            if norm["tipo"] == "genero":
                st.session_state.pending_genero = norm["valor"]
                st.session_state.entrada_texto = ""
            else:
                st.session_state.entrada_texto = texto
            st.rerun()
        st.markdown('<div class="mm-sep"></div>', unsafe_allow_html=True)
        genero = st.session_state.get("sel_genero") or st.session_state.get("genero")
        if genero:
            rec = recomendar_region(genero)
            segunda = rec["segunda_opcion"] or "—"
            fila = next((d for d in rec["detalle"] if d["region"] == segunda), None)
            afinidad = f"{fila['afinidad']:.0f}" if fila else "—"
            st.markdown(
                f'<div class="mm-field-label">Segunda opción</div>'
                f'<div class="mm-second">{segunda} <span>(afinidad {afinidad})</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="mm-field-label">Segunda opción</div>'
                '<div class="mm-second mm-muted">—</div>',
                unsafe_allow_html=True,
            )
        st.markdown('<div class="mm-sidebar-spacer"></div>', unsafe_allow_html=True)
        if st.button("Ver evidencia →", key="ver_evidencia", width="stretch", disabled=not genero):
            navegar("P2")
        if st.button("Explorar por región", key="explorar_region", width="stretch"):
            navegar("P3")


def _main_recomendacion() -> None:
    genero = st.session_state.get("sel_genero") or st.session_state.get("genero")
    entrada = (st.session_state.get("entrada_texto") or "").strip()
    if entrada:
        norm = normalizar_entrada(entrada)
        tipo = norm["tipo"]
        if tipo == "sugerencia":
            valor = norm["valor"]
            if valor in REGIONES:
                nota("info", f"«{entrada}» corresponde a la región <b>{valor}</b>.")
                if st.button(f"Ver ranking de {valor}", type="primary", key="ir_region_sug"):
                    st.session_state.sel_region = valor
                    st.session_state.entrada_texto = ""
                    navegar("P3")
            else:
                nota("info", f"¿Quisiste decir <b>{valor}</b>?")
                st.button(
                    f"Sí, usar {valor}", type="primary", key="aceptar_sug",
                    on_click=_aceptar_genero, args=(valor,),
                )
            return
        if tipo == "region":
            region = norm["valor"]
            nota("info", f"«{entrada}» corresponde a la región <b>{region}</b>.")
            if st.button(f"Ver ranking de {region}", type="primary", key="ir_region"):
                st.session_state.sel_region = region
                st.session_state.entrada_texto = ""
                navegar("P3")
            return
        if tipo == "lista":
            nota("warning", norm["mensaje"])
            chips = "".join(f'<span class="mm-chip-mini">{g}</span>' for g in norm["generos"])
            st.markdown(f'<div class="mm-chip-row">{chips}</div>', unsafe_allow_html=True)
            return
        if tipo == "vacio":
            empty_state(
                "Elige un género para ver la recomendación",
                "Selecciona un género de la lista o escríbelo en el buscador.",
                ICON_MUSIC,
            )
            return
        if tipo == "genero":
            genero = norm["valor"]
            st.session_state.genero = genero
            st.session_state.entrada_texto = ""

    if not genero:
        empty_state(
            "Elige un género para ver la recomendación",
            "Selecciona un género de la lista o escríbelo en el buscador.",
            ICON_MUSIC,
        )
        return

    rec = recomendar_region(genero)
    detalle = rec["detalle"]
    baja = rec["evidencia"] == "Baja"
    if baja:
        r1, r2 = detalle[0]["region"], detalle[1]["region"]
        titulo = (
            f'Sin región dominante: compara <span class="mm-green">{r1}</span> '
            f'y <span class="mm-green">{r2}</span>'
        )
    else:
        titulo = f'Prioriza <span class="mm-green">{rec["region_recomendada"]}</span>'
    sub = f"{genero} tiene {porcentaje(rec['afinidad'] - 100)} de streams por registro frente a su promedio global."
    prob = round(rec["prob_mejor"] * 100)
    banner(titulo, sub, evidence_chip(rec["evidencia"], prob))
    if detalle[0]["n_registros"] < 5:
        st.markdown(
            f'<div class="mm-note mm-note-warn">{ICON_WARNING}'
            "<span>Menos de 5 registros · interpretar con cautela.</span></div>",
            unsafe_allow_html=True,
        )
    with st.container(key="chart_afinidad"):
        affinity_chart(rec)


def pantalla_recomendacion() -> None:
    if st.session_state.get("pending_genero"):
        st.session_state.genero = st.session_state.pending_genero
        st.session_state.sel_genero = st.session_state.pending_genero
        st.session_state.pending_genero = None
    fondo()
    barra_superior("Recomendación por género")
    filtros, resultados = st.columns([1, 2.9], gap="large")
    with filtros:
        _sidebar_recomendacion()
    with resultados:
        _main_recomendacion()


# ---------------------------------------------------------------------------
# Pantalla C — Evidencia de la recomendación
# ---------------------------------------------------------------------------
def pantalla_evidencia() -> None:
    genero = st.session_state.get("genero")
    if not genero:
        st.session_state.pantalla = "P1"
        st.rerun()
        return
    if st.session_state.get("sel_genero_ev") != genero:
        st.session_state.sel_genero_ev = genero
    fondo()
    barra_superior("Evidencia de la recomendación")
    filtros, resultados = st.columns([1, 2.9], gap="large")
    with filtros:
        with st.container(key="sidebar"):
            if st.button("← Volver a la recomendación", key="back_evidencia"):
                navegar("P1")
            st.markdown('<div class="mm-field-label">Género</div>', unsafe_allow_html=True)
            st.selectbox(
                "Género", GENEROS, key="sel_genero_ev", on_change=_cambiar_genero_ev,
                label_visibility="collapsed",
            )
            st.markdown('<div class="mm-sidebar-spacer"></div>', unsafe_allow_html=True)
            sidebar_deco()
    with resultados:
        genero = st.session_state.genero
        rec = recomendar_region(genero)
        prob = round(rec["prob_mejor"] * 100)
        titulo = (
            f'¿Qué tan segura es la recomendación para '
            f'<span class="mm-green">{genero}</span>?'
        )
        sub = (
            f'{rec["region_recomendada"]} es la mejor región en {prob} % de los escenarios '
            f'simulados · evidencia {rec["evidencia"].lower()}.'
        )
        banner(titulo, sub, evidence_chip(rec["evidencia"], prob))
        with st.container(key="chart_evidencia"):
            evidence_chart(rec)


# ---------------------------------------------------------------------------
# Pantalla D — Ranking por región
# ---------------------------------------------------------------------------
def pantalla_ranking() -> None:
    fondo()
    barra_superior("Ranking por región")
    filtros, resultados = st.columns([1, 2.9], gap="large")
    with filtros:
        with st.container(key="sidebar"):
            if st.button("← Inicio", key="back_inicio_p3"):
                ir_inicio()
            st.markdown('<div class="mm-field-label">Región</div>', unsafe_allow_html=True)
            st.selectbox(
                "Región", REGIONES, index=None, key="sel_region",
                placeholder="Elige una región", label_visibility="collapsed",
            )
            st.markdown(
                f'<div class="mm-help">{ICON_CURSOR}<span>Toca un género para ver en qué '
                "región conviene promoverlo.</span></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="mm-warning-note">{ICON_WARNING}<span>= menos de 5 registros; '
                "interpretar con cautela.</span></div>",
                unsafe_allow_html=True,
            )
            st.markdown('<div class="mm-sidebar-spacer"></div>', unsafe_allow_html=True)
            sidebar_deco()
    with resultados:
        region = st.session_state.get("sel_region")
        if not region:
            empty_state(
                "Elige una región para ver el ranking",
                "Selecciona una región para comparar el promedio de streams de sus géneros.",
                ICON_BARS,
            )
            return
        ranking = ranking_por_region(region)
        lider = ranking.iloc[0]["genero"]
        titulo = f'En {region} lidera <span class="mm-green">{lider}</span>'
        sub = "Promedio de Total Streams por registro de los 10 géneros de la región."
        banner(titulo, sub)
        ranking_chart(ranking)


# ---------------------------------------------------------------------------
# Enrutador
# ---------------------------------------------------------------------------
PANTALLAS = {
    "P0": pantalla_inicio,
    "P1": pantalla_recomendacion,
    "P2": pantalla_evidencia,
    "P3": pantalla_ranking,
}

_pantalla = st.session_state.get("pantalla", "P0")
if _pantalla not in PANTALLAS:
    st.session_state.pantalla = "P0"
    _pantalla = "P0"

PANTALLAS[_pantalla]()
pie()
