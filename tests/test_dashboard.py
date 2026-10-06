from dashboard_builder import build_dashboard_data
from dashboard_validation import validate_dashboard_data

def test_dashboard_contract():
    p=build_dashboard_data()
    assert validate_dashboard_data(p)
    assert p["schema_version"]=="10.0"
    assert p["engine"]=="P01-010"
    assert p["executive_summary"]["market_risk"]["level"] in {"LOW","MODERATE","HIGH"}
    assert p["executive_summary"]["evidence_confidence"]["level"] in {"LOW","MEDIUM","HIGH"}

def test_risk_confidence_are_separate():
    p=build_dashboard_data()
    risk=p["executive_summary"]["market_risk"]
    conf=p["executive_summary"]["evidence_confidence"]
    assert "score" in risk and "score" in conf
    assert risk["score"] <= 100 and conf["score"] <= 1
