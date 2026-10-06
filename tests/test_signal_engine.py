from copy import deepcopy
from signal_engine import build_signal_report, load_signal_rules
from signal_validation import validate_signal_report


def normalized():
    vals={"US10Y":(0.049,"DECIMAL"),"DXY":(106.0,"INDEX"),"VIX":(14.0,"INDEX"),"BTC":(80000.0,"USD"),"ETH":(2500.0,"USD")}
    return {"schema_version":"3.0","generated_at":"2026-09-23T00:00:00+00:00","expected_metrics":list(vals),"records":[
        {"metric_id":m,"normalized":{"value":v,"unit":u},"provenance":{"source":"Test","source_type":"PRIMARY"}} for m,(v,u) in vals.items()]}


def quality():
    return {"schema_version":"4.0","metrics":[{"metric_id":m,"available":True,"freshness":{"is_fresh":True},"validity":{"is_valid":True},"consistency":{"is_consistent":True},"source_evidence":{"source":"Test","source_type":"PRIMARY"},"reasons":[]} for m in ["US10Y","DXY","VIX","BTC","ETH"]]}


def test_deterministic_classification():
    r=build_signal_report(normalized(),quality())
    by={s["metric_id"]:s for s in r["signals"]}
    assert by["US10Y"]["signal_id"] == "ELEVATED_YIELD" and by["US10Y"]["direction"] == "RISK_OFF"
    assert by["DXY"]["signal_id"] == "STRONG_DOLLAR"
    assert by["VIX"]["signal_id"] == "LOW_VOLATILITY" and by["VIX"]["direction"] == "RISK_ON"
    assert by["BTC"]["signal_id"] == "INSUFFICIENT_HISTORY" and by["BTC"]["direction"] == "UNKNOWN"
    assert by["ETH"]["direction"] == "UNKNOWN"
    assert validate_signal_report(r)


def test_quality_gate_blocks_bad_data():
    q=quality(); q["metrics"][0]["freshness"]["is_fresh"]=False
    s=build_signal_report(normalized(),q)["signals"][0]
    assert s["signal_id"] == "DATA_QUALITY_GATE_FAILED" and s["direction"] == "UNKNOWN"


def test_fallback_reduces_evidence_confidence():
    n=normalized(); n["records"][0]["provenance"]["source_type"]="FALLBACK"
    q=quality(); q["metrics"][0]["source_evidence"]["source_type"]="FALLBACK"
    s=build_signal_report(n,q)["signals"][0]
    assert s["confidence"] == 0.9


def test_summary_counts():
    r=build_signal_report(normalized(),quality())
    assert r["summary"] == {"total":5,"risk_on":1,"risk_off":2,"neutral":0,"unknown":2}
