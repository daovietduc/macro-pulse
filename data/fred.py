import pandas as pd
import requests

def fred_series(series_id, api_key, days=1825):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": (pd.Timestamp.today() - pd.Timedelta(days=days)).strftime("%Y-%m-%d"),
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    obs = r.json().get("observations", [])
    rows = []
    for x in obs:
        try:
            rows.append({"date": pd.to_datetime(x["date"]), "value": float(x["value"]), "source":"FRED"})
        except (ValueError, TypeError):
            continue
    return pd.DataFrame(rows)
