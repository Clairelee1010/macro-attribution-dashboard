import json
from pathlib import Path

DEFAULT_RULES_PATH = Path(__file__).resolve().parent / "config" / "regime_rules.json"


def load_regime_rules(path=None):
    path = Path(path) if path is not None else DEFAULT_RULES_PATH
    return json.loads(path.read_text(encoding="utf-8"))


def _contribution(signal, rules):
    direction = signal.get("direction", "UNKNOWN")
    strength = signal.get("strength", "UNKNOWN")
    if direction not in rules["direction_scores"] or strength not in rules["strength_weights"]:
        return None
    metric_weight = float(rules["metric_weights"].get(signal["metric_id"], 1.0))
    strength_weight = float(rules["strength_weights"][strength])
    signed = float(rules["direction_scores"][direction])
    confidence = float(signal.get("confidence", 0.0))
    max_weight = metric_weight * strength_weight
    return {
        "metric_id": signal["metric_id"],
        "direction": direction,
        "strength": strength,
        "signal_id": signal.get("signal_id"),
        "confidence": confidence,
        "weight": round(max_weight, 4),
        "weighted_score": round(signed * max_weight * confidence, 4),
    }


def build_regime_report(signal_report, rules=None):
    rules = rules or load_regime_rules()
    contributions = []
    excluded = []
    for signal in signal_report["signals"]:
        item = _contribution(signal, rules)
        if item is None:
            excluded.append({
                "metric_id": signal["metric_id"],
                "direction": signal.get("direction", "UNKNOWN"),
                "reason": signal.get("reason") or "NOT_REGIME_ELIGIBLE",
            })
        else:
            contributions.append(item)

    total_expected_weight = sum(float(rules["metric_weights"].get(s["metric_id"], 1.0)) *
                                float(rules["strength_weights"].get(s.get("strength"), 0.0))
                                for s in signal_report["signals"] if s.get("strength") in rules["strength_weights"])
    eligible_weight = sum(x["weight"] for x in contributions)
    weighted_sum = sum(x["weighted_score"] for x in contributions)
    score = round(weighted_sum / eligible_weight, 4) if eligible_weight else 0.0

    coverage = round(len(contributions) / max(1, len(signal_report["signals"])), 4)
    avg_confidence = round(sum(x["confidence"] for x in contributions) / len(contributions), 4) if contributions else 0.0
    has_on = any(x["direction"] == "RISK_ON" for x in contributions)
    has_off = any(x["direction"] == "RISK_OFF" for x in contributions)
    contradiction = has_on and has_off
    confidence = coverage * avg_confidence
    if contradiction:
        confidence -= float(rules["confidence"].get("contradiction_penalty", 0.0))
    confidence = round(max(0.0, min(1.0, confidence)), 4)

    minimum_coverage = float(rules["confidence"].get("minimum_coverage", 0.0))
    if coverage < minimum_coverage or not contributions:
        regime = "UNKNOWN"
    elif score >= float(rules["thresholds"]["risk_on_min"]):
        regime = "RISK_ON"
    elif score <= float(rules["thresholds"]["risk_off_max"]):
        regime = "RISK_OFF"
    else:
        regime = "NEUTRAL"

    supporting = [x for x in contributions if x["direction"] == regime] if regime in ("RISK_ON", "RISK_OFF") else []
    contradicting = [x for x in contributions if regime in ("RISK_ON", "RISK_OFF") and x["direction"] not in (regime, "NEUTRAL")]

    return {
        "schema_version":"6.0",
        "source_schema_version":signal_report["schema_version"],
        "generated_at":signal_report["generated_at"],
        "engine":"P01-006",
        "rules_version":rules["version"],
        "regime":regime,
        "score":score,
        "confidence":confidence,
        "coverage":coverage,
        "contradiction":contradiction,
        "drivers":contributions,
        "supporting":supporting,
        "contradicting":contradicting,
        "excluded":excluded,
        "summary":{
            "eligible_signals":len(contributions),
            "excluded_signals":len(excluded),
            "total_signals":len(signal_report["signals"]),
            "eligible_weight":round(eligible_weight,4),
            "weighted_sum":round(weighted_sum,4),
        },
        "semantics":rules["semantics"],
    }
