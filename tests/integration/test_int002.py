import json
from integration.context_intelligence_engine import build_context_intelligence
from integration.divergence_engine import evaluate_relationship
from integration.context_mapper import load_rules


def p(category, question):
    return {"category": {"key": category}, "question": question}


def p01(regime="RISK_OFF"):
    return {
        "regime": regime,
        "risk_level": "HIGH",
        "evidence_confidence": "MEDIUM",
        "evidence_confidence_score": 0.63,
        "drivers": [
            {"metric_id": "US10Y", "signal_id": "VERY_HIGH_YIELD", "direction": "RISK_OFF", "strength": "STRONG"},
            {"metric_id": "DXY", "signal_id": "FIRM_DOLLAR", "direction": "RISK_OFF", "strength": "MODERATE"}
        ]
    }


def test_macro_directional_context_is_deterministic():
    rules = load_rules()
    assert evaluate_relationship(p("macro", "Will the Fed increase interest rates by 25 bps?"), p01(), rules)["relationship"] == "SUPPORTED_CONTEXT"
    assert evaluate_relationship(p("macro", "Will the Fed decrease interest rates by 25 bps?"), p01(), rules)["relationship"] == "DIVERGENT_CONTEXT"
    assert evaluate_relationship(p("macro", "Will there be no change in Fed interest rates?"), p01(), rules)["relationship"] == "MIXED_CONTEXT"


def test_crypto_uses_broad_regime_with_guardrail():
    rules = load_rules()
    assert evaluate_relationship(p("crypto", "Will Bitcoin dip to $65,000 in September?"), p01("RISK_OFF"), rules)["relationship"] == "SUPPORTED_CONTEXT"
    assert evaluate_relationship(p("crypto", "Will Bitcoin reach $90,000 in September?"), p01("RISK_OFF"), rules)["relationship"] == "DIVERGENT_CONTEXT"


def test_political_contracts_are_not_interpreted():
    rules = load_rules()
    x = evaluate_relationship(p("politics", "Will Candidate X win the presidential nomination?"), p01(), rules)
    assert x["relationship"] == "NOT_APPLICABLE"
    assert x["evidence"] == []


def test_unmapped_market_categories_do_not_get_forced_alignment():
    rules = load_rules()
    assert evaluate_relationship(p("energy", "Will WTI reach $100?"), p01(), rules)["relationship"] == "INSUFFICIENT_EVIDENCE"
    assert evaluate_relationship(p("metals", "Will gold reach a new high?"), p01(), rules)["relationship"] == "INSUFFICIENT_EVIDENCE"


def test_full_int002_contract():
    d = build_context_intelligence()
    assert d["version"] == "INT-002"
    assert d["execution_allowed"] is False
    assert d["input"]["predictions_evaluated"] <= 20
    allowed = {"SUPPORTED_CONTEXT", "MIXED_CONTEXT", "DIVERGENT_CONTEXT", "INSUFFICIENT_EVIDENCE", "NOT_APPLICABLE"}
    assert all(x["relationship"] in allowed for x in d["context_intelligence"])
    assert all(x["execution_allowed"] is False for x in d["context_intelligence"])
    for x in d["context_intelligence"]:
        key = (x.get("category") or {}).get("key")
        if key == "politics":
            assert x["relationship"] == "NOT_APPLICABLE"


def test_no_recommendation_or_own_probability():
    d = build_context_intelligence()
    s = json.dumps(d).lower()
    assert '"execution_allowed": false' in s
    for x in d["context_intelligence"]:
        assert "forecast" not in x["relationship"].lower()
        assert "recommendation" not in x["relationship"].lower()
