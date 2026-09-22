import copy
import pytest
from jsonschema import ValidationError
from schema_validation import validate_raw_payload


def record(metric_id="VIX"):
    return {
        "metric_id": metric_id,
        "name": "CBOE Volatility Index",
        "category": "RISK",
        "ticker": "^VIX",
        "value": 15.2,
        "previous_close": 15.5,
        "change_pct": -1.94,
        "unit": "INDEX",
        "source": "Test Provider",
        "source_type": "PRIMARY",
        "observed_at": "2026-09-22T00:00:00+00:00",
        "fetched_at": "2026-09-22T00:01:00+00:00",
        "status": "FRESH",
        "error": None,
    }


def payload():
    return {
        "schema_version": "2.0",
        "generated_at": "2026-09-22T00:01:00+00:00",
        "expected_metrics": ["VIX"],
        "records": [record()],
    }


def test_valid_raw_payload_passes():
    assert validate_raw_payload(payload()) is True


def test_missing_required_field_fails():
    p = payload()
    del p["records"][0]["source_type"]
    with pytest.raises(ValueError):
        validate_raw_payload(p)


def test_invalid_status_fails():
    p = payload()
    p["records"][0]["status"] = "UNKNOWN"
    with pytest.raises(ValueError):
        validate_raw_payload(p)


def test_fresh_record_requires_numeric_value():
    p = payload()
    p["records"][0]["value"] = None
    with pytest.raises(ValueError):
        validate_raw_payload(p)


def test_none_source_cannot_be_fresh():
    p = payload()
    p["records"][0]["source_type"] = "NONE"
    with pytest.raises(ValueError):
        validate_raw_payload(p)
