import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "regime_report.schema.json"

def validate_regime_report(payload, schema_path=None):
    path = Path(schema_path) if schema_path else SCHEMA_PATH
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(payload)
    summary = payload["summary"]
    assert summary["total_signals"] == summary["eligible_signals"] + summary["excluded_signals"]
    assert summary["eligible_signals"] == len(payload["drivers"])
    assert -1.0 <= payload["score"] <= 1.0
    assert 0.0 <= payload["confidence"] <= 1.0
    assert 0.0 <= payload["coverage"] <= 1.0
    return True
