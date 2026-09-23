import json
from pathlib import Path

DEFAULT_RULES_PATH = Path(__file__).resolve().parent / "config" / "confidence_evidence_rules.json"

def load_confidence_evidence_rules(path=None):
    path = Path(path) if path is not None else DEFAULT_RULES_PATH
    return json.loads(path.read_text(encoding="utf-8"))

def _clamp(value):
    return max(0.0, min(1.0, float(value)))

def _level(score, levels):
    if score < float(levels["LOW"]["max_exclusive"]):
        return "LOW"
    if score < float(levels["MEDIUM"]["max_exclusive"]):
        return "MEDIUM"
    return "HIGH"

def _source_reliability(quality, rules):
    metrics = quality.get("metrics", [])
    if not metrics:
        return 0.0
    mapping = rules["source_reliability"]
    scores = []
    for metric in metrics:
        source_type = metric.get("source_evidence", {}).get("source_type", "NONE")
        scores.append(float(mapping.get(source_type, 0.0)))
    return _clamp(sum(scores) / len(scores))

def build_confidence_evidence_report(quality, regime, attribution, risk, rules=None):
    rules = rules or load_confidence_evidence_rules()
    weights = rules["weights"]
    data_quality = _clamp(quality.get("quality_score", 0))
    coverage = _clamp(risk.get("evidence_coverage", regime.get("coverage", 0)))
    source_reliability = _source_reliability(quality, rules)
    signal_agreement = _clamp(attribution.get("evidence_agreement", 0))
    attribution_support = _clamp(attribution.get("attribution_confidence", 0))
    risk_confidence = _clamp(risk.get("confidence", 0))
    components = {
        "data_quality": round(data_quality, 4),
        "evidence_coverage": round(coverage, 4),
        "source_reliability": round(source_reliability, 4),
        "signal_agreement": round(signal_agreement, 4),
        "attribution_support": round(attribution_support, 4),
        "risk_confidence": round(risk_confidence, 4),
    }
    score = round(sum(components[key] * float(weights[key]) for key in weights), 4)
    expected = int(quality.get("counts", {}).get("expected", 0))
    eligible = int(attribution.get("summary", {}).get("eligible_drivers", 0))
    excluded = int(attribution.get("summary", {}).get("excluded_signals", 0))
    missing = max(0, expected - eligible)
    evidence = [
        {"evidence_id":"DATA_QUALITY","upstream_engine":"P01-004","artifact":"data_quality_report.json","status":quality.get("quality_gate", "UNKNOWN"),"value":round(data_quality,4)},
        {"evidence_id":"MARKET_REGIME","upstream_engine":"P01-006","artifact":"regime_report.json","status":regime.get("regime", "UNKNOWN"),"value":round(_clamp(regime.get("confidence",0)),4)},
        {"evidence_id":"ATTRIBUTION","upstream_engine":"P01-007","artifact":"attribution_report.json","status":"AVAILABLE" if attribution.get("drivers") else "LIMITED","value":round(attribution_support,4)},
        {"evidence_id":"MARKET_RISK","upstream_engine":"P01-008","artifact":"market_risk_report.json","status":risk.get("risk_level", "UNKNOWN"),"value":round(risk_confidence,4)},
    ]
    limitations = []
    if quality.get("degradation_reasons"):
        limitations.extend(quality["degradation_reasons"])
    if excluded:
        limitations.append("EXCLUDED_SIGNALS_PRESENT")
    if coverage < 0.8:
        limitations.append("LIMITED_EVIDENCE_COVERAGE")
    if attribution_support < 0.5:
        limitations.append("LOW_ATTRIBUTION_SUPPORT")
    return {
        "schema_version":"9.0",
        "source_schema_version":risk["schema_version"],
        "generated_at":risk["generated_at"],
        "engine":"P01-009",
        "rules_version":rules["version"],
        "confidence_score":score,
        "confidence_level":_level(score, rules["levels"]),
        "evidence_coverage":round(coverage,4),
        "components":components,
        "evidence":evidence,
        "traceability":{
            "data_quality":"data_quality_report.json",
            "market_regime":"regime_report.json",
            "attribution":"attribution_report.json",
            "market_risk":"market_risk_report.json"
        },
        "limitations":sorted(set(limitations)),
        "summary":{"expected_observations":expected,"eligible_evidence":eligible,"missing_or_excluded":max(missing,excluded),"excluded_signals":excluded},
        "semantics":rules["semantics"]
    }
