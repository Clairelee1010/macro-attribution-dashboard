import json
from pathlib import Path

DEFAULT_RULES_PATH = Path(__file__).resolve().parent / "config" / "attribution_rules.json"


def load_attribution_rules(path=None):
    path = Path(path) if path is not None else DEFAULT_RULES_PATH
    return json.loads(path.read_text(encoding="utf-8"))


def _relation(direction, regime):
    if regime not in {"RISK_ON", "RISK_OFF"}:
        return "CONTEXT"
    if direction == regime:
        return "SUPPORTING"
    if direction in {"RISK_ON", "RISK_OFF"} and direction != regime:
        return "CONFLICTING"
    return "NEUTRAL"


def build_attribution_report(regime_report, rules=None):
    rules = rules or load_attribution_rules()
    regime = regime_report["regime"]
    drivers = regime_report.get("drivers", [])
    total_abs = sum(abs(float(d.get("weighted_score", 0.0))) for d in drivers)

    attributed = []
    for d in drivers:
        abs_score = abs(float(d.get("weighted_score", 0.0)))
        share = round(abs_score / total_abs, 4) if total_abs else 0.0
        attributed.append({
            "metric_id": d["metric_id"],
            "signal_id": d.get("signal_id"),
            "direction": d.get("direction", "UNKNOWN"),
            "strength": d.get("strength", "UNKNOWN"),
            "signal_confidence": round(float(d.get("confidence", 0.0)), 4),
            "weight": round(float(d.get("weight", 0.0)), 4),
            "weighted_score": round(float(d.get("weighted_score", 0.0)), 4),
            "contribution_share": share,
            "relation_to_regime": _relation(d.get("direction"), regime),
        })

    attributed.sort(key=lambda x: (-x["contribution_share"], x["metric_id"]))
    minimum_share = float(rules.get("minimum_driver_share", 0.0))
    primary = [d for d in attributed if d["contribution_share"] >= minimum_share]
    supporting = [d for d in primary if d["relation_to_regime"] == "SUPPORTING"]
    conflicting = [d for d in primary if d["relation_to_regime"] == "CONFLICTING"]
    contextual = [d for d in primary if d["relation_to_regime"] in {"CONTEXT", "NEUTRAL"}]

    evidence_total = sum(d["contribution_share"] for d in supporting + conflicting)
    support_share = sum(d["contribution_share"] for d in supporting)
    agreement = round(support_share / evidence_total, 4) if evidence_total else 0.0
    confidence = float(regime_report.get("confidence", 0.0)) * float(regime_report.get("coverage", 0.0))
    if conflicting:
        confidence -= float(rules.get("confidence", {}).get("contradiction_penalty", 0.0))
    if regime == "UNKNOWN":
        confidence = min(confidence, float(rules.get("confidence", {}).get("unknown_regime_cap", 0.25)))
    confidence = round(max(0.0, min(1.0, confidence)), 4)

    return {
        "schema_version": "7.0",
        "source_schema_version": regime_report["schema_version"],
        "generated_at": regime_report["generated_at"],
        "engine": "P01-007",
        "rules_version": rules["version"],
        "regime": regime,
        "regime_score": regime_report.get("score", 0.0),
        "regime_confidence": regime_report.get("confidence", 0.0),
        "attribution_confidence": confidence,
        "evidence_agreement": agreement,
        "drivers": primary,
        "supporting_evidence": supporting,
        "conflicting_evidence": conflicting,
        "contextual_evidence": contextual,
        "excluded": regime_report.get("excluded", []),
        "summary": {
            "eligible_drivers": len(attributed),
            "reported_drivers": len(primary),
            "supporting_drivers": len(supporting),
            "conflicting_drivers": len(conflicting),
            "contextual_drivers": len(contextual),
            "excluded_signals": len(regime_report.get("excluded", [])),
            "contribution_share_total": round(sum(d["contribution_share"] for d in attributed), 4),
        },
        "semantics": rules["semantics"],
    }
