import pandas as pd

from config.indicators import INDICATORS
from .market import yahoo_history
from .vn import vnindex_history
from .fred import fred_series

_SOURCE_LABEL = {"yahoo": "Yahoo Finance", "vnstock": "VNStock", "fred": "FRED", "manual": "—"}


def _fmt(v, unit=""):
    if v is None:
        return "—"
    if unit == "%":
        return f"{v:.2f}%"
    return f"{v:,.2f}"


def _row(ind, value, date, source, change_pct=None, note=None):
    return {
        "id": ind.id,
        "region": ind.region,
        "category": ind.category,
        "name": ind.name,
        "value": value,
        "date": date,
        "source": note or source,
        "unit": ind.unit,
        "change_pct": change_pct,
        "value_display": _fmt(value, ind.unit),
        "change_display": "—" if change_pct is None else f"{change_pct:+.2f}%",
    }


def _fetch_history(ind, fred_key):
    if ind.source == "yahoo":
        return yahoo_history(ind.symbol, 365)
    if ind.source == "vnstock":
        return vnindex_history(365)
    if ind.source == "fred":
        if not fred_key:
            return None
        return fred_series(ind.symbol, fred_key, 365 * 5)
    return None  # "manual": chưa nối nguồn


def collect_all(fred_key=""):
    rows = []
    histories = {}

    for ind in INDICATORS:
        if ind.requires == "fred_key" and not fred_key:
            rows.append(_row(ind, None, "", "", note="chưa có API key"))
            continue

        if ind.source == "manual":
            rows.append(_row(ind, None, "", "", note="chưa có nguồn dữ liệu"))
            continue

        try:
            h = _fetch_history(ind, fred_key)
            if h is None or h.empty:
                rows.append(_row(ind, None, "", "", note="không có dữ liệu"))
                continue

            histories[ind.id] = h
            last = float(h["value"].iloc[-1])
            prev = float(h["value"].iloc[-2]) if len(h) > 1 else None
            ch = ((last / prev) - 1) * 100 if prev not in (None, 0) else None
            date = str(h["date"].iloc[-1])[:10]
            rows.append(_row(ind, last, date, _SOURCE_LABEL.get(ind.source, ind.source), ch))
        except Exception:
            rows.append(_row(ind, None, "", "", note="error"))

    df = pd.DataFrame(rows)
    if df.empty:
        df = pd.DataFrame(columns=[
            "id", "region", "category", "name", "value", "date", "source",
            "unit", "change_pct", "value_display", "change_display",
        ])

    return {"snapshot": df, "history": histories}
