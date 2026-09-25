import json

from integration.dashboard_payload import ALLOWED_RELATIONSHIPS, build_dashboard_payload


def test_int003_contract():
    d = build_dashboard_payload()
    assert d["version"] == "INT-003"
    assert d["execution_allowed"] is False
    assert d["architecture"]["p01"] == "UNDERSTAND"
    assert d["architecture"]["p02"] == "PREDICT_COMPARE"
    assert d["architecture"]["int003"] == "PRESENT_INTEGRATED_INTELLIGENCE"
    assert isinstance(d["cards"], list)
    assert len(d["cards"]) <= 20
    assert sum(d["relationship_counts"].values()) == len(d["cards"])


def test_relationships_and_execution_guardrail():
    d = build_dashboard_payload()
    for card in d["cards"]:
        assert card["relationship"] in ALLOWED_RELATIONSHIPS
        assert card["execution_allowed"] is False


def test_political_cards_are_observation_only():
    d = build_dashboard_payload()
    for card in d["cards"]:
        if card["category"]["key"] == "politics":
            assert card["relationship"] == "NOT_APPLICABLE"
            assert card["p01_evidence"] == []


def test_dashboard_preserves_market_probability_without_creating_new_probability():
    d = build_dashboard_payload()
    source = json.load(open("data/integration/context_intelligence.json", encoding="utf-8"))
    source_by_id = {x["event_id"]: x for x in source["context_intelligence"]}
    for card in d["cards"]:
        src = source_by_id[card["event_id"]]
        assert card["market_implied_probability"] == src["market_implied_probability"]


def test_system_status_is_read_only():
    d = build_dashboard_payload()
    s = d["system_status"]
    assert s["int001_integration"] == "PASS"
    assert s["int002_context"] == "PASS"
    assert s["political_guardrail"] == "PASS"
    assert s["execution"] == "DISABLED"
