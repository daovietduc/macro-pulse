import streamlit as st

from config import theme
from config.indicators import MARKET_PULSE, get as get_indicator


def render_hero(scores):
    """Phần đầu trang: Macro Score lớn + gauge + 4 chỉ số phụ. Hiển thị ở mọi tab."""
    regime_color = theme.REGIME_COLORS.get(scores["regime"], theme.COLORS["primary"])

    st.markdown(
        f"""
        <div class="mp-hero">
          <div>
            <div class="mp-hero-label">Macro Score</div>
            <div class="mp-hero-score">{scores['macro_score']:.0f}<span class="mp-hero-score-unit">/100</span></div>
            {theme.pill(scores['regime'], regime_color)}
          </div>
          <div class="mp-hero-col">
            {theme.gauge(scores['macro_score'])}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    kpis = [
        ("Growth", scores["growth"], theme.COLORS["up"]),
        ("Liquidity", scores["liquidity"], theme.COLORS["info"]),
        ("Inflation", scores["inflation"], theme.COLORS["warn"]),
        ("Risk", scores["risk"], theme.COLORS["down"]),
    ]
    for col, (label, val, accent) in zip(cols, kpis):
        col.markdown(theme.kpi_card(label, f"{val:.0f}/100", accent=accent), unsafe_allow_html=True)


def render_tab(df, scores):
    """Nội dung tab Dashboard: Market Pulse + Macro Regime."""
    st.markdown('<div class="mp-section-title">Market Pulse</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, ind_id in enumerate(MARKET_PULSE):
        ind = get_indicator(ind_id)
        row = df[df["id"] == ind_id]
        if row.empty or row.iloc[0]["value"] is None:
            value, delta = "—", None
        else:
            value = row.iloc[0]["value_display"]
            delta = row.iloc[0]["change_display"]
        accent = theme.delta_accent(delta)
        sub = f'<span style="color:{accent};">{delta}</span>' if delta and delta != "—" else None
        cols[i % 4].markdown(
            theme.kpi_card(ind.name if ind else ind_id, value, accent=accent, sub=sub),
            unsafe_allow_html=True,
        )

    st.markdown('<div class="mp-section-title" style="margin-top:1.3rem;">Macro Regime</div>', unsafe_allow_html=True)
    r1, r2, r3, r4 = st.columns(4)
    r1.markdown(theme.kpi_card("Regime", scores["regime"], accent=theme.REGIME_COLORS.get(scores["regime"])), unsafe_allow_html=True)
    r2.markdown(theme.kpi_card("Inflation", f"{scores['inflation']:.0f}/100", accent=theme.COLORS["warn"]), unsafe_allow_html=True)
    r3.markdown(theme.kpi_card("FX Pressure", f"{scores['fx_pressure']:.0f}/100", accent=theme.COLORS["info"]), unsafe_allow_html=True)
    r4.markdown(theme.kpi_card("Credit", f"{scores['credit']:.0f}/100", accent=theme.COLORS["up"]), unsafe_allow_html=True)

    st.info(scores["explanation"])
