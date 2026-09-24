import os
import streamlit as st

def get_secret(name, default=""):
    try:
        value = st.secrets.get(name, "")
        if value:
            return value
    except Exception:
        pass
    return os.getenv(name, default)

DATA_CACHE_TTL = 900
FRED_BASE = "https://api.stlouisfed.org/fred"
YAHOO_BASE = "https://query1.finance.yahoo.com"
