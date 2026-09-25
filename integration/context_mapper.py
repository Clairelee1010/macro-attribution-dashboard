from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "config" / "integration_context_rules.json"


def load_rules():
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))


def _category_key(prediction):
    cat = prediction.get("category", "other")
    return (cat.get("key") if isinstance(cat, dict) else cat) or "other"


def _contains_any(text, terms):
    t = (text or "").lower()
    return any(term.lower() in t for term in terms)


def classify_scenario(prediction, rules=None):
    """Classify only scenario direction needed for contextual comparison.

    This does not classify truth, likelihood, desirability, or recommendation.
    """
    rules = rules or load_rules()
    category = _category_key(prediction)
    question = prediction.get("question", "")

    if category == "macro":
        r = rules["macro"]
        if _contains_any(question, r["rate_hike_terms"]):
            return "RATE_HIKE"
        if _contains_any(question, r["rate_cut_terms"]):
            return "RATE_CUT"
        if _contains_any(question, r["no_change_terms"]):
            return "RATE_HOLD"
        return "UNMAPPED"

    if category == "crypto":
        r = rules["crypto"]
        if _contains_any(question, r["down_terms"]):
            return "CRYPTO_DOWNSIDE"
        if _contains_any(question, r["up_terms"]):
            return "CRYPTO_UPSIDE"
        return "UNMAPPED"

    return "UNMAPPED"


def relevant_p01_evidence(prediction, p01, rules=None):
    rules = rules or load_rules()
    category = _category_key(prediction)
    drivers = p01.get("drivers", [])

    if category == "macro":
        return [d for d in drivers if d.get("metric_id") in {"US10Y", "DXY"}]
    if category == "crypto":
        # P01 BTC/ETH may be excluded for insufficient history. Use only broad
        # regime/risk context and expose the limitation rather than inventing
        # asset-specific evidence.
        return [
            {"metric_id": "MARKET_REGIME", "signal_id": p01.get("regime"), "direction": p01.get("regime"), "strength": None},
            {"metric_id": "MARKET_RISK", "signal_id": p01.get("risk_level"), "direction": None, "strength": None},
        ]
    return []
