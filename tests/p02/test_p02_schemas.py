import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2] / "p02"

PAIRS = [
    ("prediction_market.schema.json", "prediction_market.sample.json"),
    ("canonical_event.schema.json", "canonical_event.sample.json"),
    ("discrepancy.schema.json", "discrepancy.sample.json"),
    ("security_event.schema.json", "security_event.sample.json"),
]

def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_p02_demo_fixtures_validate():
    for schema_name, fixture_name in PAIRS:
        schema = _load(ROOT / "schemas" / schema_name)
        fixture = _load(ROOT / "fixtures" / fixture_name)
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(fixture))
        assert not errors, [e.message for e in errors]

def test_p02_never_allows_execution():
    fixture = _load(ROOT / "fixtures" / "discrepancy.sample.json")
    assert fixture["execution_allowed"] is False

def test_demo_fixture_is_explicitly_limited():
    fixture = _load(ROOT / "fixtures" / "discrepancy.sample.json")
    assert "DEMO_FIXTURE_NOT_LIVE_MARKET_DATA" in fixture["limitations"]

def test_topics_have_bilingual_names():
    topics = _load(ROOT / "config" / "event_topics.json")
    for topic in topics["topics"]:
        assert topic["name_en"]
        assert topic["name_zh_tw"]
