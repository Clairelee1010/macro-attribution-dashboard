import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "attribution_report.schema.json"


def validate_attribution_report(payload, schema_path=None):
    path = Path(schema_path) if schema_path else SCHEMA_PATH
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(payload)
    assert 0.0 <= payload["attribution_confidence"] <= 1.0
    assert 0.0 <= payload["evidence_agreement"] <= 1.0
    assert payload["summary"]["reported_drivers"] == len(payload["drivers"])
    assert payload["summary"]["supporting_drivers"] == len(payload["supporting_evidence"])
    assert payload["summary"]["conflicting_drivers"] == len(payload["conflicting_evidence"])
    for d in payload["drivers"]:
        assert 0.0 <= d["contribution_share"] <= 1.0
    return True
