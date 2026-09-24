import streamlit as st

from config import theme
from ai.engine import run_all_ai, build_consensus


def render_tab(df, api_keys, models):
    st.markdown('<div class="mp-section-title">Three-AI Macro Panel</div>', unsafe_allow_html=True)
    st.caption("Ba mô hình nhận cùng một snapshot dữ liệu và phân tích độc lập. Consensus chỉ tổng hợp, không thay thế dữ liệu.")

    if st.button("Chạy GPT + Claude + Gemini", type="primary"):
        with st.spinner("Đang chạy 3 AI độc lập..."):
            analyses = run_all_ai(df, api_keys=api_keys, models=models)
            st.session_state["analyses"] = analyses
            st.session_state["consensus"] = build_consensus(analyses)

    analyses = st.session_state.get("analyses", {})
    consensus = st.session_state.get("consensus")

    cols = st.columns(3)
    for col, name in zip(cols, ["gpt", "claude", "gemini"]):
        result = analyses.get(name)
        with col:
            st.markdown(f'<div class="mp-ai-card"><div class="mp-ai-name">{name.upper()}</div>', unsafe_allow_html=True)
            if not result:
                st.markdown('<div class="mp-ai-muted">Chưa chạy.</div></div>', unsafe_allow_html=True)
                continue
            if result.get("error"):
                st.markdown('</div>', unsafe_allow_html=True)
                st.error(result["error"])
                continue

            direction = result.get("direction", "—")
            color = theme.DIRECTION_COLORS.get(direction, theme.COLORS["primary"])
            st.markdown(theme.pill(direction.capitalize(), color), unsafe_allow_html=True)
            st.markdown(
                f'<div class="mp-ai-muted" style="margin:.5rem 0;">Confidence: {result.get("confidence","—")}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(result.get("summary", ""))
            if result.get("risks"):
                st.markdown("**Risks**")
                for x in result["risks"]:
                    st.write("•", x)
            st.markdown('</div>', unsafe_allow_html=True)

    if consensus:
        st.markdown('<div class="mp-section-title" style="margin-top:1.2rem;">Consensus Engine</div>', unsafe_allow_html=True)
        color = theme.DIRECTION_COLORS.get(consensus["direction"], theme.COLORS["primary"])
        st.markdown(
            theme.pill(f"{consensus['direction'].upper()} • Đồng thuận {consensus['agreement']:.0%}", color),
            unsafe_allow_html=True,
        )
        st.markdown(consensus["summary"])
        st.caption("Consensus được tính từ các kết quả độc lập; không phải xác suất thị trường.")
