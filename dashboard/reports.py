from datetime import datetime

import streamlit as st


def _report_markdown(scores, analyses, consensus):
    lines = [
        f"# MacroPulse AI — Báo cáo {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "",
        f"**Macro Score:** {scores['macro_score']:.0f}/100 — {scores['regime']}",
        f"- Growth: {scores['growth']:.0f}/100",
        f"- Liquidity: {scores['liquidity']:.0f}/100",
        f"- Inflation: {scores['inflation']:.0f}/100",
        f"- Risk: {scores['risk']:.0f}/100",
        "",
        "## AI Consensus",
    ]
    if consensus:
        lines.append(f"Direction: **{consensus['direction'].upper()}** ({consensus['agreement']:.0%} đồng thuận)")
        lines.append("")
        lines.append(consensus["summary"])
    else:
        lines.append("_Chưa chạy AI Consensus — mở tab AI Consensus và bấm chạy trước khi xuất báo cáo để có phần này._")

    for name, result in (analyses or {}).items():
        lines.append(f"\n### {name.upper()}")
        if not result or result.get("error"):
            lines.append(f"- {result.get('error', 'Chưa chạy.') if result else 'Chưa chạy.'}")
            continue
        lines.append(f"- Direction: {result.get('direction','—')} (Confidence: {result.get('confidence','—')})")
        if result.get("summary"):
            lines.append(result["summary"])

    return "\n".join(lines)


def render_tab(df, scores):
    st.markdown('<div class="mp-section-title">Xuất báo cáo</div>', unsafe_allow_html=True)

    analyses = st.session_state.get("analyses", {})
    consensus = st.session_state.get("consensus")
    report_md = _report_markdown(scores, analyses, consensus)

    st.download_button(
        "⬇️ Tải báo cáo (.md)",
        data=report_md,
        file_name=f"macropulse_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
        mime="text/markdown",
        type="primary",
    )
    with st.expander("Xem trước báo cáo"):
        st.markdown(report_md)

    st.markdown('<div class="mp-section-title" style="margin-top:1.4rem;">Normalized Data</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
