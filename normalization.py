from datetime import datetime, timezone

METRIC_REGISTRY = {
    "US10Y": {"canonical_name": "US 10-Year Treasury Yield", "canonical_unit": "DECIMAL", "precision": 8, "rule": "PERCENT_TO_DECIMAL"},
    "DXY": {"canonical_name": "US Dollar Index", "canonical_unit": "INDEX", "precision": 6, "rule": "IDENTITY"},
    "VIX": {"canonical_name": "CBOE Volatility Index", "canonical_unit": "INDEX", "precision": 6, "rule": "IDENTITY"},
    "BTC": {"canonical_name": "Bitcoin", "canonical_unit": "USD", "precision": 4, "rule": "IDENTITY"},
    "ETH": {"canonical_name": "Ethereum", "canonical_unit": "USD", "precision": 4, "rule": "IDENTITY"},
}


def _utc_iso(value):
    if value is None:
        return None
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


def _transform(value, rule, precision):
    if value is None:
        return None
    if rule == "PERCENT_TO_DECIMAL":
        return round(float(value) / 100.0, precision)
    if rule == "IDENTITY":
        return round(float(value), precision)
    raise ValueError(f"Unsupported normalization rule: {rule}")


def normalize_record(record):
    metric_id = record["metric_id"]
    if metric_id not in METRIC_REGISTRY:
        raise ValueError(f"Unknown metric_id: {metric_id}")
    cfg = METRIC_REGISTRY[metric_id]
    rule = cfg["rule"]
    precision = cfg["precision"]
    return {
        "metric_id": metric_id,
        "canonical_name": cfg["canonical_name"],
        "category": record["category"],
        "raw": {"value": record["value"], "unit": record["unit"]},
        "normalized": {
            "value": _transform(record["value"], rule, precision),
            "unit": cfg["canonical_unit"],
            "precision": precision,
        },
        "transformation": {
            "type": rule,
            "formula": "raw_value / 100" if rule == "PERCENT_TO_DECIMAL" else "raw_value",
            "deterministic": True,
        },
        "provenance": {
            "ticker": record["ticker"],
            "source": record["source"],
            "source_type": record["source_type"],
            "observed_at": _utc_iso(record["observed_at"]),
            "fetched_at": _utc_iso(record["fetched_at"]),
            "status": record["status"],
            "error": record["error"],
        },
    }


def normalize_payload(raw_payload):
    records = [normalize_record(r) for r in raw_payload["records"]]
    return {
        "schema_version": "3.0",
        "source_schema_version": raw_payload["schema_version"],
        "generated_at": _utc_iso(raw_payload["generated_at"]),
        "expected_metrics": list(raw_payload["expected_metrics"]),
        "records": records,
    }
