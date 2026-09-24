import json
from pathlib import Path
from jsonschema import Draft202012Validator

def validate_dashboard_data(payload, schema_path="schemas/dashboard_data.schema.json"):
    schema=json.loads(Path(schema_path).read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(payload)
    ex=payload["executive_summary"]
    assert 0 <= ex["market_risk"]["score"] <= 100
    assert 0 <= ex["market_risk"]["confidence"] <= 1
    assert 0 <= ex["evidence_confidence"]["score"] <= 1
    assert 0 <= ex["data_quality"]["score"] <= 1
    return True
