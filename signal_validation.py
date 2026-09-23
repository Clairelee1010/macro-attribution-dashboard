import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "signal_report.schema.json"

def validate_signal_report(payload, schema_path=None):
    path = Path(schema_path) if schema_path else SCHEMA_PATH
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(payload)
    total = payload["summary"]["total"]
    assert total == len(payload["signals"])
    assert total == sum(payload["summary"][k] for k in ("risk_on","risk_off","neutral","unknown"))
    return True
