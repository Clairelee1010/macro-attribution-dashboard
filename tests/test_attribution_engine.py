from attribution_engine import build_attribution_report
from attribution_validation import validate_attribution_report


def regime(name="RISK_OFF", drivers=None, confidence=0.8, coverage=1.0):
    return {
        "schema_version":"6.0", "generated_at":"2026-09-23T00:00:00+00:00",
        "regime":name, "score":-0.5 if name == "RISK_OFF" else 0.5,
        "confidence":confidence, "coverage":coverage,
        "drivers":drivers or [], "excluded":[]
    }


def d(mid, direction, weighted, confidence=1.0):
    return {"metric_id":mid,"signal_id":"TEST","direction":direction,"strength":"MODERATE","confidence":confidence,"weight":1.0,"weighted_score":weighted}


def test_supporting_and_conflicting_evidence():
    r=build_attribution_report(regime(drivers=[d("VIX","RISK_OFF",-1.0),d("DXY","RISK_OFF",-0.5),d("BTC","RISK_ON",0.25)]))
    assert len(r["supporting_evidence"]) == 2
    assert len(r["conflicting_evidence"]) == 1
    assert r["drivers"][0]["metric_id"] == "VIX"
    assert validate_attribution_report(r)


def test_contribution_shares_are_relative_evidence_weights():
    r=build_attribution_report(regime(drivers=[d("VIX","RISK_OFF",-1.0),d("DXY","RISK_OFF",-1.0)]))
    assert r["drivers"][0]["contribution_share"] == 0.5
    assert r["drivers"][1]["contribution_share"] == 0.5


def test_conflict_reduces_attribution_confidence():
    clean=build_attribution_report(regime(drivers=[d("VIX","RISK_OFF",-1.0),d("DXY","RISK_OFF",-1.0)]))
    mixed=build_attribution_report(regime(drivers=[d("VIX","RISK_OFF",-1.0),d("DXY","RISK_ON",1.0)]))
    assert mixed["attribution_confidence"] < clean["attribution_confidence"]


def test_unknown_regime_does_not_claim_supporting_causality():
    r=build_attribution_report(regime(name="UNKNOWN", drivers=[d("VIX","RISK_OFF",-1.0)], confidence=0.4, coverage=0.2))
    assert r["supporting_evidence"] == []
    assert r["drivers"][0]["relation_to_regime"] == "CONTEXT"
    assert r["attribution_confidence"] <= 0.25
