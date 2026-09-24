import pandas as pd

def vnindex_history(days=365):
    from vnstock3 import Vnstock
    end = pd.Timestamp.today()
    start = end - pd.Timedelta(days=days)
    stock = Vnstock().stock(symbol="VNINDEX", source="VCI")
    df = stock.quote.history(
        start=start.strftime("%Y-%m-%d"),
        end=end.strftime("%Y-%m-%d"),
    )
    if df is None or df.empty:
        return pd.DataFrame()
    close_col = "close" if "close" in df.columns else df.columns[-1]
    out = pd.DataFrame({
        "date": pd.to_datetime(df["time"] if "time" in df.columns else df.index),
        "value": pd.to_numeric(df[close_col], errors="coerce"),
    }).dropna()
    out["source"] = "VNStock"
    return out.reset_index(drop=True)
