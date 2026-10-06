#!/usr/bin/env python3
"""Validate P02-001 configuration and demo fixtures.

Fixtures are synthetic and must never be presented as live market evidence.
"""
from pathlib import Path
import json
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent
PAIRS = [
    ("prediction_market.schema.json", "prediction_market.sample.json"),
    ("canonical_event.schema.json", "canonical_event.sample.json"),
    ("discrepancy.schema.json", "discrepancy.sample.json"),
    ("security_event.schema.json", "security_event.sample.json"),
]

def load(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)

def validate_all():
    errors = []
    for schema_name, fixture_name in PAIRS:
        schema = load(ROOT / "schemas" / schema_name)
        fixture = load(ROOT / "fixtures" / fixture_name)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        fixture_errors = sorted(validator.iter_errors(fixture), key=lambda e: list(e.path))
        if fixture_errors:
            for error in fixture_errors:
                errors.append(f"{fixture_name}: {error.message}")
        else:
            print(f"PASS {fixture_name}")

    # Config sanity
    topics = load(ROOT / "config" / "event_topics.json")
    thresholds = load(ROOT / "config" / "thresholds.json")
    assert topics["version"] == "1.0"
    assert any(t["enabled"] for t in topics["topics"])
    assert 0 <= thresholds["comparability"]["medium_min"] <= thresholds["comparability"]["high_min"] <= 1
    print("PASS configuration")

    if errors:
        raise SystemExit("\n".join(errors))
    print("P02-001 FOUNDATION: PASS")

if __name__ == "__main__":
    validate_all()
