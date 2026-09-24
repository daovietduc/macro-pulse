def _latest(df, key):
    x = df[df["id"] == key]
    if x.empty or x.iloc[0]["value"] is None:
        return None
    return float(x.iloc[0]["value"])

def build_macro_scores(df):
    # Transparent first-pass scores. They are indicators, not forecasts.
    growth = 50.0
    inflation = 50.0
    liquidity = 50.0
    fx = 50.0
    credit = 50.0
    risk = 50.0

    pmi = _latest(df, "PMI")
    unrate = _latest(df, "UNRATE")
    fed = _latest(df, "FEDFUNDS")
    us10 = _latest(df, "US10Y")
    cpi = _latest(df, "USCPI")

    if pmi is not None:
        growth = max(0, min(100, 50 + (pmi - 50) * 5))
    if unrate is not None:
        risk = max(0, min(100, 50 + (unrate - 4) * 8))
    if fed is not None:
        liquidity = max(0, min(100, 100 - fed * 10))
    if us10 is not None:
        risk = max(0, min(100, risk + max(0, us10 - 4) * 4))
    if cpi is not None:
        inflation = max(0, min(100, 100 - max(0, cpi - 2) * 15))

    macro = 0.30*growth + 0.25*liquidity + 0.15*inflation + 0.15*(100-fx) + 0.15*credit
    if macro >= 65:
        regime = "Expansion / supportive"
    elif macro >= 50:
        regime = "Neutral / mixed"
    elif macro >= 35:
        regime = "Late-cycle / tightening risk"
    else:
        regime = "Contraction / stress"

    return {
        "macro_score": macro,
        "growth": growth,
        "liquidity": liquidity,
        "inflation": inflation,
        "fx_pressure": fx,
        "credit": credit,
        "risk": risk,
        "regime": regime,
        "explanation": "Score hiện tại là lớp định lượng ban đầu; khi bổ sung dữ liệu Việt Nam như M2, tín dụng, CPI, PMI và OMO, trọng số sẽ được nâng cấp."
    }
