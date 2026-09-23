import json
from pathlib import Path
from jsonschema import Draft202012Validator

DEFAULT_SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "confidence_evidence_report.schema.json"

def validate_confidence_evidence_report(payload, schema_path=None):
    path = Path(schema_path) if schema_path is not None else DEFAULT_SCHEMA_PATH
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(payload)
    return True
