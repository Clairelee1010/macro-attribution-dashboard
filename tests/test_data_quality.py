import copy
from datetime import datetime, timezone
from data_quality import build_quality_report, load_rules
from data_quality_validation import validate_data_quality_report
from normalization import normalize_payload


def raw(mid, value, unit, cat, observed="2026-09-22T00:30:00+00:00", source_type="PRIMARY"):
    return {"metric_id":mid,"name":mid,"category":cat,"ticker":"T","value":value,"previous_close":value,"change_pct":0.0,"unit":unit,"source":"source","source_type":source_type,"observed_at":observed,"fetched_at":"2026-09-22T01:00:00+00:00","status":"FRESH","error":None}


def payload():
    rows=[raw("US10Y",4.95,"%","MACRO"),raw("DXY",100.2,"INDEX","FX"),raw("VIX",15.2,"INDEX","RISK"),raw("BTC",86000,"USD","CRYPTO"),raw("ETH",2700,"USD","CRYPTO")]
    return normalize_payload({"schema_version":"2.0","generated_at":"2026-09-22T01:00:00+00:00","expected_metrics":[r["metric_id"] for r in rows],"records":rows})


def report(p=None):
    return build_quality_report(p or payload(), rules=load_rules(), as_of=datetime(2026,9,22,1,0,tzinfo=timezone.utc))


def test_all_good_passes_and_validates_schema():
    out=report()
    assert validate_data_quality_report(out)
    assert out["quality_score"] == 1.0
    assert out["quality_gate"] == "PASS"
    assert out["counts"] == {"expected":5,"available":5,"fresh":5,"valid":5,"consistent":5}


def test_crypto_stale_uses_configurable_threshold():
    p=payload(); btc=next(r for r in p["records"] if r["metric_id"]=="BTC")
    btc["provenance"]["observed_at"]="2026-09-21T20:00:00+00:00"
    out=report(p); q=next(m for m in out["metrics"] if m["metric_id"]=="BTC")
    assert q["freshness"]["threshold_hours"] == 2.0
    assert q["freshness"]["is_fresh"] is False
    assert "STALE_OBSERVATION" in q["reasons"]


def test_missing_value_reduces_completeness_and_validity():
    p=payload(); eth=next(r for r in p["records"] if r["metric_id"]=="ETH")
    eth["raw"]["value"]=None; eth["normalized"]["value"]=None; eth["provenance"]["status"]="ERROR"; eth["provenance"]["error"]="test"
    out=report(p)
    assert out["components"]["completeness"] == 0.8
    assert out["components"]["validity"] == 0.8


def test_transformation_mismatch_detected():
    p=payload(); y=next(r for r in p["records"] if r["metric_id"]=="US10Y")
    y["normalized"]["value"]=0.495
    out=report(p); q=next(m for m in out["metrics"] if m["metric_id"]=="US10Y")
    assert q["consistency"]["is_consistent"] is False
    assert "TRANSFORMATION_MISMATCH" in q["reasons"]


def test_fallback_is_evidence_not_score_penalty():
    p=payload(); y=next(r for r in p["records"] if r["metric_id"]=="US10Y")
    y["provenance"]["source_type"]="FALLBACK"
    out=report(p); q=next(m for m in out["metrics"] if m["metric_id"]=="US10Y")
    assert q["source_evidence"]["source_type"] == "FALLBACK"
    assert "FALLBACK_SOURCE_USED" in q["reasons"]
    assert out["quality_score"] == 1.0
