import streamlit as st

from config.indicators import MACRO_TABLE


def render_tab(df):
    st.markdown('<div class="mp-section-title">Chỉ số vĩ mô</div>', unsafe_allow_html=True)
    mdf = df[df["id"].isin(MACRO_TABLE)].copy()
    if mdf.empty:
        st.warning(
            "Chưa có dữ liệu macro tương ứng. FRED API key sẽ mở rộng dữ liệu Mỹ; "
            "dữ liệu Việt Nam (PMI, tăng trưởng tín dụng...) cần thêm nguồn/API phù hợp — "
            "khai báo trong config/indicators.py khi có nguồn."
        )
        return
    st.dataframe(
        mdf[["region", "category", "name", "value_display", "change_display", "date", "source"]],
        use_container_width=True,
        hide_index=True,
    )
