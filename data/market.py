import time
import pandas as pd
import requests

def yahoo_history(ticker, days=365):
    end = int(time.time())
    start = end - days * 86400
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    params = {"period1": start, "period2": end, "interval": "1d", "events": "history"}
    r = requests.get(url, params=params, timeout=15, headers={"User-Agent":"Mozilla/5.0"})
    r.raise_for_status()
    data = r.json()["chart"]["result"][0]
    ts = data.get("timestamp", [])
    closes = data["indicators"]["quote"][0].get("close", [])
    rows = []
    for t, v in zip(ts, closes):
        if v is not None:
            rows.append({"date": pd.to_datetime(t, unit="s"), "value": float(v), "source":"Yahoo Finance"})
    return pd.DataFrame(rows)

def yahoo_latest(ticker):
    h = yahoo_history(ticker, 10)
    return h.iloc[-1]["value"] if not h.empty else None
