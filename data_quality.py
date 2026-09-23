import json
import math
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_RULES_PATH = Path("config/data_quality_rules.json")


def _dt(value):
    if not value:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def load_rules(path=None):
    if path is None:
        path = Path(__file__).resolve().parent / "config" / "data_quality_rules.json"
    else:
        path = Path(path)

    return json.loads(path.read_text(encoding="utf-8"))


def _expected_normalized(raw_value, transformation, precision):
    if raw_value is None:
        return None
    kind = transformation["type"]
    if kind == "PERCENT_TO_DECIMAL":
        return round(float(raw_value) / 100.0, precision)
    if kind == "IDENTITY":
        return round(float(raw_value), precision)
    raise ValueError(f"Unsupported transformation: {kind}")


def evaluate_record(record, as_of, rules):
    mid = record["metric_id"]
    provenance = record["provenance"]
    raw_value = record["raw"]["value"]
    normalized_value = record["normalized"]["value"]
    upstream_status = provenance["status"]

    available = raw_value is not None and normalized_value is not None and upstream_status not in {"MISSING", "ERROR"}

    observed = _dt(provenance.get("observed_at"))
    threshold = float(rules["freshness_threshold_hours"][mid])
    age_hours = None if observed is None else max(0.0, (as_of - observed).total_seconds() / 3600.0)
    fresh = bool(available and age_hours is not None and age_hours <= threshold)

    valid = bool(
        available
        and _finite(raw_value)
        and _finite(normalized_value)
        and isinstance(record["raw"].get("unit"), str)
        and isinstance(record["normalized"].get("unit"), str)
        and observed is not None
        and _dt(provenance.get("fetched_at")) is not None
    )

    consistent = False
    consistency_reason = None
    if valid:
        try:
            expected = _expected_normalized(raw_value, record["transformation"], record["normalized"]["precision"])
            consistent = math.isclose(float(normalized_value), float(expected), rel_tol=0.0, abs_tol=10 ** (-(record["normalized"]["precision"])))
            if not consistent:
                consistency_reason = "TRANSFORMATION_MISMATCH"
        except (KeyError, TypeError, ValueError):
            consistency_reason = "TRANSFORMATION_INVALID"
    else:
        consistency_reason = "NOT_VALID_FOR_CONSISTENCY_CHECK"

    reasons = []
    if not available: reasons.append("MISSING_OR_ERROR_VALUE")
    if available and observed is None: reasons.append("OBSERVATION_TIME_MISSING")
    if available and observed is not None and not fresh: reasons.append("STALE_OBSERVATION")
    if not valid: reasons.append("INVALID_RECORD")
    if valid and not consistent: reasons.append(consistency_reason or "TRANSFORMATION_MISMATCH")
    if provenance.get("source_type") == "FALLBACK": reasons.append("FALLBACK_SOURCE_USED")

    return {
        "metric_id": mid,
        "available": available,
        "freshness": {"is_fresh": fresh, "age_hours": None if age_hours is None else round(age_hours, 4), "threshold_hours": threshold},
        "validity": {"is_valid": valid},
        "consistency": {"is_consistent": consistent},
        "source_evidence": {
            "source": provenance.get("source"),
            "source_type": provenance.get("source_type"),
            "upstream_status": upstream_status,
            "upstream_error": provenance.get("error")
        },
        "reasons": reasons,
    }


def build_quality_report(normalized_payload, rules=None, as_of=None):
    rules = rules or load_rules()
    as_of = as_of or _dt(normalized_payload["generated_at"]) or datetime.now(timezone.utc)
    expected = list(normalized_payload["expected_metrics"])
    by_id = {r["metric_id"]: r for r in normalized_payload["records"]}

    metrics = []
    for mid in expected:
        if mid in by_id:
            metrics.append(evaluate_record(by_id[mid], as_of, rules))
        else:
            metrics.append({
                "metric_id": mid, "available": False,
                "freshness": {"is_fresh": False, "age_hours": None, "threshold_hours": float(rules["freshness_threshold_hours"][mid])},
                "validity": {"is_valid": False}, "consistency": {"is_consistent": False},
                "source_evidence": {"source": None, "source_type": "NONE", "upstream_status": "MISSING", "upstream_error": "Metric absent from normalized payload"},
                "reasons": ["MISSING_METRIC", "INVALID_RECORD"]
            })

    total = len(expected)
    def ratio(predicate):
        return round(sum(1 for m in metrics if predicate(m)) / total, 4) if total else 0.0

    components = {
        "completeness": ratio(lambda m: m["available"]),
        "freshness": ratio(lambda m: m["freshness"]["is_fresh"]),
        "validity": ratio(lambda m: m["validity"]["is_valid"]),
        "consistency": ratio(lambda m: m["consistency"]["is_consistent"]),
    }
    weights = rules["component_weights"]
    score = round(sum(components[k] * float(weights[k]) for k in components), 4)
    gate_cfg = rules["quality_gate"]
    if score >= float(gate_cfg["pass_min_score"]): gate = "PASS"
    elif score >= float(gate_cfg["degraded_min_score"]): gate = "DEGRADED"
    else: gate = "BLOCK"

    degraded = sorted({reason for m in metrics for reason in m["reasons"]})
    counts = {
        "expected": total,
        "available": sum(1 for m in metrics if m["available"]),
        "fresh": sum(1 for m in metrics if m["freshness"]["is_fresh"]),
        "valid": sum(1 for m in metrics if m["validity"]["is_valid"]),
        "consistent": sum(1 for m in metrics if m["consistency"]["is_consistent"]),
    }
    return {
        "schema_version": "4.0",
        "source_schema_version": normalized_payload["schema_version"],
        "generated_at": as_of.isoformat(),
        "rules_version": rules["version"],
        "quality_score": score,
        "quality_gate": gate,
        "components": components,
        "counts": counts,
        "degradation_reasons": degraded,
        "metrics": metrics,
    }
