from confidence_evidence import build_confidence_evidence_report
from confidence_evidence_validation import validate_confidence_evidence_report

def fixtures(fallback=False, excluded=0):
    quality={"quality_score":1.0,"quality_gate":"PASS","counts":{"expected":5},"degradation_reasons":(["FALLBACK_SOURCE_USED"] if fallback else []),"metrics":[{"source_evidence":{"source_type":"FALLBACK" if fallback and i==0 else "PRIMARY"}} for i in range(5)]}
    regime={"coverage":0.8,"confidence":0.7,"regime":"RISK_OFF"}
    attribution={"evidence_agreement":0.9,"attribution_confidence":0.7,"drivers":[{"metric_id":"VIX"}],"summary":{"eligible_drivers":5-excluded,"excluded_signals":excluded}}
    risk={"schema_version":"8.0","generated_at":"2026-09-24T00:00:00+00:00","evidence_coverage":round((5-excluded)/5,4),"confidence":0.7,"risk_level":"HIGH"}
    return quality,regime,attribution,risk

def test_contract_valid():
    assert validate_confidence_evidence_report(build_confidence_evidence_report(*fixtures()))

def test_score_bounds_and_level():
    report=build_confidence_evidence_report(*fixtures())
    assert 0 <= report["confidence_score"] <= 1
    assert report["confidence_level"] in {"LOW","MEDIUM","HIGH"}

def test_fallback_reduces_source_reliability():
    primary=build_confidence_evidence_report(*fixtures(False))
    fallback=build_confidence_evidence_report(*fixtures(True))
    assert fallback["components"]["source_reliability"] < primary["components"]["source_reliability"]

def test_excluded_evidence_reduces_coverage():
    full=build_confidence_evidence_report(*fixtures(False,0))
    limited=build_confidence_evidence_report(*fixtures(False,2))
    assert limited["evidence_coverage"] < full["evidence_coverage"]
    assert "EXCLUDED_SIGNALS_PRESENT" in limited["limitations"]

def test_traceability():
    report=build_confidence_evidence_report(*fixtures())
    assert report["traceability"]["market_risk"] == "market_risk_report.json"
    assert {x["upstream_engine"] for x in report["evidence"]} == {"P01-004","P01-006","P01-007","P01-008"}
