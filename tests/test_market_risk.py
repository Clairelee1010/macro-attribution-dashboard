from market_risk import build_market_risk_report
from market_risk_validation import validate_market_risk_report
def sample(regime="NEUTRAL",confidence=0.8):
    return {"schema_version":"7.0","generated_at":"2026-09-23T00:00:00+00:00","regime":regime,"attribution_confidence":confidence,"drivers":[{"metric_id":"VIX","signal_id":"HIGH_VOL","direction":"RISK_OFF","strength":"STRONG","signal_confidence":1.0,"contribution_share":0.6},{"metric_id":"BTC","signal_id":"RISK_APPETITE","direction":"RISK_ON","strength":"MODERATE","signal_confidence":0.8,"contribution_share":0.4}],"excluded":[],"summary":{"eligible_drivers":2,"excluded_signals":0}}
def test_contract_valid(): assert validate_market_risk_report(build_market_risk_report(sample()))
def test_score_bounds(): 
    r=build_market_risk_report(sample()); assert 0<=r["risk_score"]<=100 and r["risk_level"] in {"LOW","MODERATE","HIGH"}
def test_regime_order(): assert build_market_risk_report(sample("RISK_OFF"))["risk_score"]>build_market_risk_report(sample("RISK_ON"))["risk_score"]
def test_evidence_buckets():
    r=build_market_risk_report(sample()); assert r["risk_drivers"][0]["metric_id"]=="VIX" and r["protective_factors"][0]["metric_id"]=="BTC"
def test_coverage():
    x=sample(); x["excluded"]=[{"metric_id":"ETH","reason":"INSUFFICIENT_HISTORY"}]; x["summary"]["excluded_signals"]=1
    assert build_market_risk_report(x)["evidence_coverage"]==0.6667
