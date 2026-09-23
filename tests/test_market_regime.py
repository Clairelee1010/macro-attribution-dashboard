from market_regime import build_regime_report
from regime_validation import validate_regime_report


def report(signals):
    return {"schema_version":"5.0","generated_at":"2026-09-23T00:00:00+00:00","signals":signals}

def s(mid,direction,strength="MODERATE",confidence=1.0,reason=None):
    return {"metric_id":mid,"signal_id":"TEST","direction":direction,"strength":strength,"confidence":confidence,"reason":reason}

def test_risk_off_regime():
    r=build_regime_report(report([s("US10Y","RISK_OFF"),s("DXY","RISK_OFF"),s("VIX","RISK_OFF")]))
    assert r["regime"] == "RISK_OFF"
    assert r["score"] < 0
    assert validate_regime_report(r)

def test_risk_on_regime():
    r=build_regime_report(report([s("US10Y","RISK_ON"),s("DXY","RISK_ON"),s("VIX","RISK_ON")]))
    assert r["regime"] == "RISK_ON"
    assert r["score"] > 0

def test_mixed_signals_are_contradiction_aware():
    r=build_regime_report(report([s("US10Y","RISK_OFF"),s("DXY","RISK_OFF"),s("VIX","RISK_ON")]))
    assert r["contradiction"] is True
    assert r["confidence"] < 1.0

def test_unknown_signals_are_excluded():
    r=build_regime_report(report([s("US10Y","RISK_OFF"),s("DXY","RISK_OFF"),s("VIX","RISK_ON"),s("BTC","UNKNOWN","UNKNOWN",0.0,"INSUFFICIENT_HISTORY"),s("ETH","UNKNOWN","UNKNOWN",0.0,"INSUFFICIENT_HISTORY")]))
    assert r["summary"]["eligible_signals"] == 3
    assert r["summary"]["excluded_signals"] == 2
    assert r["coverage"] == 0.6

def test_low_coverage_returns_unknown():
    r=build_regime_report(report([s("US10Y","RISK_OFF"),s("DXY","UNKNOWN","UNKNOWN",0.0),s("VIX","UNKNOWN","UNKNOWN",0.0),s("BTC","UNKNOWN","UNKNOWN",0.0),s("ETH","UNKNOWN","UNKNOWN",0.0)]))
    assert r["regime"] == "UNKNOWN"
