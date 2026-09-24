import pandas as pd
import streamlit as st

from config.indicators import HISTORY_OPTIONS, get as get_indicator


def render_tab(df, history):
    st.markdown('<div class="mp-section-title">Market History</div>', unsafe_allow_html=True)

    options = [i for i in HISTORY_OPTIONS if i in history] or HISTORY_OPTIONS
    labels = {i: (get_indicator(i).name if get_indicator(i) else i) for i in options}
    selected = st.selectbox("Chọn chỉ số", options, format_func=lambda i: labels.get(i, i))

    h = history.get(selected)
    if h is not None and not h.empty:
        h2 = h.copy()
        h2["date"] = pd.to_datetime(h2["date"])
        h2 = h2.set_index("date")
        st.line_chart(h2["value"], color="#6366F1")
        st.caption(f"Nguồn: {h2['source'].iloc[-1] if 'source' in h2.columns else 'data provider'}")
    else:
        st.info("Chưa có chuỗi lịch sử cho chỉ số này.")
