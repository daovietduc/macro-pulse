from datetime import datetime

import streamlit as st

from config.settings import get_secret
from config import theme
from data.collector import collect_all
from models.scoring import build_macro_scores
from dashboard import overview, macro, markets, ai_panel, reports

st.set_page_config(
    page_title="MacroPulse AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto",
)

theme.inject()

st.markdown('<div class="mp-title">📈 MacroPulse AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="mp-tagline">Macro Intelligence Terminal • Việt Nam + Mỹ + Trung Quốc + Global • GPT × Claude × Gemini</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("⚙️ Settings")
    st.caption("API keys được đọc từ Streamlit Secrets hoặc biến môi trường.")
    st.divider()

    openai_key = st.text_input("OpenAI API Key", value=get_secret("OPENAI_API_KEY", ""), type="password")
    anthropic_key = st.text_input("Anthropic API Key", value=get_secret("ANTHROPIC_API_KEY", ""), type="password")
    gemini_key = st.text_input("Gemini API Key", value=get_secret("GEMINI_API_KEY", ""), type="password")
    fred_key = st.text_input("FRED API Key", value=get_secret("FRED_API_KEY", ""), type="password")

    st.divider()
    st.subheader("AI Models")
    gpt_model = st.text_input("GPT model", get_secret("OPENAI_MODEL", "gpt-5.6"))
    claude_model = st.text_input("Claude model", get_secret("ANTHROPIC_MODEL", "claude-sonnet-4-5"))
    gemini_model = st.text_input("Gemini model", get_secret("GEMINI_MODEL", "gemini-3.8-flash"))

    st.divider()
    if st.button("🔄 Làm mới dữ liệu", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.caption("Nguồn: Yahoo Finance / VNStock / FRED / nguồn chính thức khi adapter khả dụng.")
    st.caption("AI không phải nguồn dữ liệu gốc; AI chỉ phân tích dữ liệu đã thu thập.")

api_keys = {
    "OPENAI_API_KEY": openai_key,
    "ANTHROPIC_API_KEY": anthropic_key,
    "GEMINI_API_KEY": gemini_key,
    "FRED_API_KEY": fred_key,
}
models = {"gpt": gpt_model, "claude": claude_model, "gemini": gemini_model}


@st.cache_data(ttl=900, show_spinner=False)
def get_data(fred_key_):
    # fred_key_ được truyền làm tham số (thay vì đọc qua closure) để Streamlit
    # tự tính lại cache khi người dùng đổi FRED key ở Settings.
    return collect_all(fred_key=fred_key_)


with st.spinner("Đang thu thập và chuẩn hóa dữ liệu..."):
    bundle = get_data(fred_key)

df = bundle["snapshot"]
history = bundle["history"]
scores = build_macro_scores(df)

overview.render_hero(scores)
st.caption(f"{len(df)} điểm dữ liệu • Cập nhật {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

tabs = st.tabs(["📊 Dashboard", "🌐 Macro", "📈 Markets", "🤖 AI Consensus", "🧾 Reports"])

with tabs[0]:
    overview.render_tab(df, scores)

with tabs[1]:
    macro.render_tab(df)

with tabs[2]:
    markets.render_tab(df, history)

with tabs[3]:
    ai_panel.render_tab(df, api_keys, models)

with tabs[4]:
    reports.render_tab(df, scores)

st.divider()
st.caption("MacroPulse AI là công cụ nghiên cứu, không phải khuyến nghị đầu tư.")
