"""
Theme cho MacroPulse AI: bảng màu, font, CSS, và các hàm dựng HTML nhỏ
(kpi_card, pill, gauge) dùng chung cho mọi tab.

Sửa giao diện (màu sắc, bo góc, khoảng cách...) chỉ cần sửa file này —
các file dashboard/*.py không chứa CSS.
"""

import streamlit as st

COLORS = {
    "bg": "#0B1220",
    "panel": "#131B2C",
    "panel_alt": "#16213A",
    "border": "rgba(148,163,184,.16)",
    "text": "#E8ECF2",
    "muted": "#8A93A8",
    "primary": "#6366F1",
    "up": "#2DD4BF",
    "down": "#FB7185",
    "warn": "#F5B841",
    "info": "#60A5FA",
}

REGIME_COLORS = {
    "Expansion / supportive": COLORS["up"],
    "Neutral / mixed": COLORS["warn"],
    "Late-cycle / tightening risk": "#F0924A",
    "Contraction / stress": COLORS["down"],
}

DIRECTION_COLORS = {
    "bullish": COLORS["up"],
    "bearish": COLORS["down"],
    "neutral": COLORS["warn"],
}

_FONT_LINK = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
"""

_CSS = f"""
<style>
html, body, [class*="css"] {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }}
.block-container {{ padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1440px; }}

.mp-title {{ font-size: 1.85rem; font-weight: 800; letter-spacing: -.02em; margin-bottom: .05rem; }}
.mp-tagline {{ color: {COLORS['muted']}; font-size: .9rem; margin-bottom: 1.1rem; }}
.mp-section-title {{ font-weight: 650; font-size: 1.02rem; margin: .1rem 0 .7rem; }}

.mp-hero {{
    display: flex; gap: 2.2rem; align-items: center; flex-wrap: wrap;
    border: 1px solid {COLORS['border']}; border-radius: 18px;
    background: linear-gradient(155deg, {COLORS['panel']} 0%, {COLORS['panel_alt']} 100%);
    padding: 1.5rem 1.7rem; margin-bottom: .6rem;
}}
.mp-hero-label {{ color: {COLORS['muted']}; font-size: .8rem; margin-bottom: .25rem; }}
.mp-hero-score {{ font-size: 3.1rem; font-weight: 800; line-height: 1; font-variant-numeric: tabular-nums; }}
.mp-hero-score-unit {{ font-size: 1.05rem; color: {COLORS['muted']}; font-weight: 600; }}
.mp-hero-col {{ flex: 1 1 260px; min-width: 220px; }}

.mp-pill {{
    display: inline-flex; align-items: center; gap: .4rem;
    padding: .3rem .75rem; border-radius: 999px; font-size: .82rem; font-weight: 650;
    margin-top: .55rem;
}}

.mp-gauge-track {{
    position: relative; height: 8px; border-radius: 999px;
    background: linear-gradient(90deg, {COLORS['down']}, {COLORS['warn']}, {COLORS['up']});
}}
.mp-gauge-marker {{
    position: absolute; top: -4px; width: 3px; height: 16px;
    background: {COLORS['text']}; border-radius: 2px; transform: translateX(-50%);
}}
.mp-gauge-labels {{
    display: flex; justify-content: space-between; font-size: .68rem;
    color: {COLORS['muted']}; margin-top: .35rem;
}}

.mp-kpi {{
    border: 1px solid {COLORS['border']}; border-left: 3px solid var(--accent, {COLORS['primary']});
    border-radius: 12px; padding: .75rem .95rem; background: {COLORS['panel']};
    height: 100%; margin-bottom: .6rem;
}}
.mp-kpi-label {{ color: {COLORS['muted']}; font-size: .74rem; margin-bottom: .2rem; }}
.mp-kpi-value {{ font-size: 1.3rem; font-weight: 700; font-variant-numeric: tabular-nums; word-break: break-word; }}
.mp-kpi-sub {{ font-size: .76rem; margin-top: .2rem; }}

.mp-ai-card {{
    border: 1px solid {COLORS['border']}; border-radius: 14px; padding: 1rem 1.1rem;
    background: {COLORS['panel']}; height: 100%; margin-bottom: .6rem;
}}
.mp-ai-name {{ font-weight: 700; font-size: .92rem; margin-bottom: .5rem; letter-spacing: .01em; }}
.mp-ai-muted {{ color: {COLORS['muted']}; font-size: .85rem; }}

/* Mobile */
@media (max-width: 640px) {{
    .block-container {{ padding-left: .65rem; padding-right: .65rem; }}
    .mp-hero {{ padding: 1.1rem 1.15rem; gap: 1.2rem; }}
    .mp-hero-score {{ font-size: 2.2rem; }}
    .mp-title {{ font-size: 1.45rem; }}
    .mp-kpi-value {{ font-size: 1.1rem; }}
}}
</style>
"""


def inject():
    st.markdown(_FONT_LINK, unsafe_allow_html=True)
    st.markdown(_CSS, unsafe_allow_html=True)


def pill(text, color):
    return (
        f'<span class="mp-pill" style="background:{color}22; color:{color}; '
        f'border:1px solid {color}55;">{text}</span>'
    )


def kpi_card(label, value, accent=None, sub=None):
    style = f' style="--accent:{accent};"' if accent else ""
    sub_html = f'<div class="mp-kpi-sub">{sub}</div>' if sub else ""
    return (
        f'<div class="mp-kpi"{style}>'
        f'<div class="mp-kpi-label">{label}</div>'
        f'<div class="mp-kpi-value">{value}</div>'
        f'{sub_html}</div>'
    )


def gauge(score, zones=("Suy thoái", "Cuối chu kỳ", "Trung tính", "Mở rộng")):
    pct = max(0, min(100, score))
    return (
        f'<div class="mp-gauge-track"><div class="mp-gauge-marker" style="left:{pct}%;"></div></div>'
        f'<div class="mp-gauge-labels">'
        f'<span>{zones[0]}</span><span>{zones[1]}</span><span>{zones[2]}</span><span>{zones[3]}</span>'
        f'</div>'
    )


def delta_accent(delta_display):
    """Suy ra màu accent (tăng/giảm/trung tính) từ chuỗi hiển thị kiểu '+1.23%'."""
    if not delta_display or delta_display == "—":
        return COLORS["primary"]
    if delta_display.startswith("+"):
        return COLORS["up"]
    if delta_display.startswith("-"):
        return COLORS["down"]
    return COLORS["primary"]
