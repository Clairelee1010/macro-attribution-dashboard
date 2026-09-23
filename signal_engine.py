import json
from pathlib import Path

DEFAULT_RULES_PATH = Path(__file__).resolve().parent / "config" / "signal_rules.json"


def load_signal_rules(path=None):
    path = Path(path) if path is not None else DEFAULT_RULES_PATH
    return json.loads(path.read_text(encoding="utf-8"))


def _quality_by_id(quality_report):
    return {m["metric_id"]: m for m in quality_report["metrics"]}


def _eligible(q, gate):
    if not q:
        return False
    checks = [
        ("require_available", q.get("available", False)),
        ("require_fresh", q.get("freshness", {}).get("is_fresh", False)),
        ("require_valid", q.get("validity", {}).get("is_valid", False)),
        ("require_consistent", q.get("consistency", {}).get("is_consistent", False)),
    ]
    return all((not gate.get(key, True)) or bool(value) for key, value in checks)


def _confidence(q, rules):
    if not q:
        return 0.0
    checks = [q.get("available", False), q.get("freshness", {}).get("is_fresh", False),
              q.get("validity", {}).get("is_valid", False), q.get("consistency", {}).get("is_consistent", False)]
    score = sum(bool(x) for x in checks) / 4.0
    if q.get("source_evidence", {}).get("source_type") == "FALLBACK":
        score -= float(rules.get("confidence", {}).get("fallback_source_penalty", 0.0))
    return round(max(0.0, min(1.0, score)), 4)


def _matches(value, rule):
    if "min" in rule and value < float(rule["min"]):
        return False
    if "max" in rule and value >= float(rule["max"]):
        return False
    return True


def _unknown(record, q, reason, confidence=0.0):
    p = record.get("provenance", {})
    return {"metric_id": record["metric_id"], "signal_id": reason, "direction": "UNKNOWN", "strength": "UNKNOWN",
            "confidence": confidence, "value": record.get("normalized", {}).get("value"),
            "unit": record.get("normalized", {}).get("unit"),
            "evidence": {"data_quality_gate": "BLOCKED" if reason == "DATA_QUALITY_GATE_FAILED" else "PASS",
                         "source": p.get("source"), "source_type": p.get("source_type"), "quality_reasons": [] if not q else q.get("reasons", [])},
            "reason": reason}


def classify_record(record, quality_metric, rules):
    mid = record["metric_id"]
    confidence = _confidence(quality_metric, rules)
    if not _eligible(quality_metric, rules["quality_gate"]):
        return _unknown(record, quality_metric, "DATA_QUALITY_GATE_FAILED", confidence)
    cfg = rules["metrics"].get(mid)
    if not cfg:
        return _unknown(record, quality_metric, "NO_SIGNAL_RULE", confidence)
    if cfg.get("mode") == "INSUFFICIENT_HISTORY":
        return _unknown(record, quality_metric, "INSUFFICIENT_HISTORY", confidence)
    value = record["normalized"]["value"]
    for rule in cfg.get("rules", []):
        if _matches(float(value), rule):
            p = record.get("provenance", {})
            return {"metric_id": mid, "signal_id": rule["signal_id"], "direction": rule["direction"], "strength": rule["strength"],
                    "confidence": confidence, "value": value, "unit": record["normalized"]["unit"],
                    "evidence": {"data_quality_gate":"PASS", "source":p.get("source"), "source_type":p.get("source_type"),
                                 "quality_reasons": quality_metric.get("reasons", [])}, "reason": None}
    return _unknown(record, quality_metric, "NO_RULE_MATCH", confidence)


def build_signal_report(normalized_payload, quality_report, rules=None):
    rules = rules or load_signal_rules()
    qmap = _quality_by_id(quality_report)
    signals = [classify_record(r, qmap.get(r["metric_id"]), rules) for r in normalized_payload["records"]]
    counts = {k: sum(1 for s in signals if s["direction"] == k) for k in ("RISK_ON","RISK_OFF","NEUTRAL","UNKNOWN")}
    return {"schema_version":"5.0", "source_schema_version":normalized_payload["schema_version"],
            "quality_schema_version":quality_report["schema_version"], "generated_at":normalized_payload["generated_at"],
            "engine":"P01-005", "rules_version":rules["version"], "signals":signals,
            "summary":{"total":len(signals), "risk_on":counts["RISK_ON"], "risk_off":counts["RISK_OFF"],
                       "neutral":counts["NEUTRAL"], "unknown":counts["UNKNOWN"]},
            "semantics":{"confidence":"Evidence reliability for signal classification; not probability of a market outcome.",
                         "recommendation":"Signals are descriptive classifications, not BUY/SELL/LONG/SHORT recommendations."}}
