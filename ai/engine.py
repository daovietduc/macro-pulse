import json
import requests
import pandas as pd

SYSTEM = """You are a macroeconomic research analyst.
Analyze only the supplied data. Never invent missing numbers.
Separate facts from interpretation.
Return strict JSON with keys:
direction (bullish/neutral/bearish),
confidence (low/medium/high),
summary (string),
risks (array of strings),
drivers (array of strings).
"""

def _payload(df):
    cols = [c for c in ["id","region","category","name","value","date","source","unit","change_pct"] if c in df.columns]
    return df[cols].replace({float("nan"): None}).to_dict(orient="records")

def _openai(prompt, key, model):
    url = "https://api.openai.com/v1/responses"
    body = {
        "model": model,
        "input": [
            {"role":"system","content":SYSTEM},
            {"role":"user","content":prompt},
        ],
    }
    r = requests.post(url, headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"}, json=body, timeout=90)
    r.raise_for_status()
    data = r.json()
    text = data.get("output_text")
    if not text:
        parts = []
        for item in data.get("output", []):
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    parts.append(c.get("text",""))
        text = "".join(parts)
    return json.loads(text)

def _anthropic(prompt, key, model):
    url = "https://api.anthropic.com/v1/messages"
    body = {
        "model": model,
        "max_tokens": 1800,
        "system": SYSTEM,
        "messages": [{"role":"user","content":prompt}],
    }
    r = requests.post(url, headers={
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }, json=body, timeout=90)
    r.raise_for_status()
    data = r.json()
    text = "".join(x.get("text","") for x in data.get("content",[]) if x.get("type")=="text")
    return json.loads(text)

def _gemini(prompt, key, model):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = {
        "system_instruction": {"parts":[{"text":SYSTEM}]},
        "contents": [{"parts":[{"text":prompt}]}],
        "generationConfig": {"responseMimeType":"application/json"},
    }
    r = requests.post(url, params={"key":key}, json=body, timeout=90)
    r.raise_for_status()
    data = r.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)

def run_all_ai(df, api_keys, models):
    prompt = """Assess the current macro regime and the next 7 days.
Do not give personalized investment advice.
Focus on:
1) growth,
2) liquidity/credit,
3) inflation,
4) FX,
5) global rates/risk,
6) implications for Vietnamese financial markets.
Data:
""" + json.dumps(_payload(df), ensure_ascii=False, default=str)

    out = {}
    calls = [
        ("gpt", _openai, api_keys.get("OPENAI_API_KEY"), models["gpt"]),
        ("claude", _anthropic, api_keys.get("ANTHROPIC_API_KEY"), models["claude"]),
        ("gemini", _gemini, api_keys.get("GEMINI_API_KEY"), models["gemini"]),
    ]
    for name, fn, key, model in calls:
        if not key:
            out[name] = {"error": "Chưa có API key."}
            continue
        try:
            result = fn(prompt, key, model)
            result["model"] = model
            out[name] = result
        except Exception as e:
            out[name] = {"error": f"{type(e).__name__}: {e}"}
    return out

def build_consensus(analyses):
    valid = [x for x in analyses.values() if not x.get("error") and x.get("direction")]
    if not valid:
        return {"direction":"neutral","agreement":0,"summary":"Chưa có AI nào trả kết quả."}
    counts = {}
    for x in valid:
        d = x["direction"].lower()
        counts[d] = counts.get(d,0)+1
    direction = max(counts, key=counts.get)
    agreement = counts[direction] / len(valid)
    drivers = []
    risks = []
    for x in valid:
        drivers.extend(x.get("drivers",[])[:2])
        risks.extend(x.get("risks",[])[:2])

    unique_drivers = list(dict.fromkeys(drivers))[:5]
    unique_risks = list(dict.fromkeys(risks))[:5]

    return {
        "direction": direction,
        "agreement": agreement,
        "summary": (
            f"{len(valid)}/3 AI đã phản hồi. "
            f"Đồng thuận về hướng '{direction}': {agreement:.0%}."
            f"\n\n**Drivers:** " + "; ".join(unique_drivers) +
            f"\n\n**Risks:** " + "; ".join(unique_risks)
        )
    }
