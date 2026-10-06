from __future__ import annotations
from integration.context_mapper import classify_scenario, load_rules, relevant_p01_evidence


def _category_key(prediction):
    cat = prediction.get("category", "other")
    return (cat.get("key") if isinstance(cat, dict) else cat) or "other"


def evaluate_relationship(prediction, p01, rules=None):
    rules = rules or load_rules()
    category = _category_key(prediction)
    scenario = classify_scenario(prediction, rules)
    evidence = relevant_p01_evidence(prediction, p01, rules)

    if category in rules.get("category_policy", {}):
        state = rules["category_policy"][category]
        return {"relationship": state, "scenario": scenario, "evidence": evidence}

    if scenario == "UNMAPPED":
        return {"relationship": "INSUFFICIENT_EVIDENCE", "scenario": scenario, "evidence": evidence}

    if category == "macro":
        signal_ids = {x.get("signal_id") for x in evidence}
        restrictive = bool(signal_ids & set(rules["macro"]["restrictive_signal_ids"]))
        easing = bool(signal_ids & set(rules["macro"]["easing_signal_ids"]))
        if restrictive and easing:
            state = "MIXED_CONTEXT"
        elif scenario == "RATE_HIKE" and restrictive:
            state = "SUPPORTED_CONTEXT"
        elif scenario == "RATE_CUT" and restrictive:
            state = "DIVERGENT_CONTEXT"
        elif scenario == "RATE_HOLD" and restrictive:
            state = "MIXED_CONTEXT"
        elif scenario == "RATE_CUT" and easing:
            state = "SUPPORTED_CONTEXT"
        elif scenario == "RATE_HIKE" and easing:
            state = "DIVERGENT_CONTEXT"
        else:
            state = "INSUFFICIENT_EVIDENCE"
        return {"relationship": state, "scenario": scenario, "evidence": evidence}

    if category == "crypto":
        regime = p01.get("regime", "UNKNOWN")
        if regime == "RISK_OFF":
            state = "SUPPORTED_CONTEXT" if scenario == "CRYPTO_DOWNSIDE" else "DIVERGENT_CONTEXT"
        elif regime == "RISK_ON":
            state = "SUPPORTED_CONTEXT" if scenario == "CRYPTO_UPSIDE" else "DIVERGENT_CONTEXT"
        else:
            state = "INSUFFICIENT_EVIDENCE"
        return {"relationship": state, "scenario": scenario, "evidence": evidence}

    return {"relationship": "INSUFFICIENT_EVIDENCE", "scenario": scenario, "evidence": evidence}
