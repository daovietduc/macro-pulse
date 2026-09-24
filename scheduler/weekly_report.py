from data.collector import collect_all
from models.scoring import build_macro_scores
from ai.engine import run_all_ai, build_consensus

def generate_report(api_keys, models, fred_key=""):
    bundle = collect_all(fred_key)
    scores = build_macro_scores(bundle["snapshot"])
    analyses = run_all_ai(bundle["snapshot"], api_keys, models)
    consensus = build_consensus(analyses)
    return {"scores": scores, "analyses": analyses, "consensus": consensus}
