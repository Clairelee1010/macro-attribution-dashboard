import json
from pathlib import Path
from jsonschema import Draft202012Validator
DEFAULT_SCHEMA_PATH=Path(__file__).resolve().parent/"schemas"/"market_risk_report.schema.json"
def validate_market_risk_report(payload,schema_path=None):
    path=Path(schema_path) if schema_path is not None else DEFAULT_SCHEMA_PATH
    Draft202012Validator(json.loads(path.read_text(encoding="utf-8"))).validate(payload)
    return True
