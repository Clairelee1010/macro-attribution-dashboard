import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_PATH = Path(__file__).parent / "schemas" / "normalized_market_data.schema.json"


def load_normalized_schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_normalized_payload(payload):
    validator = Draft202012Validator(load_normalized_schema(), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    if errors:
        details = "; ".join(f"{'.'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors)
        raise ValueError(f"Normalized data schema validation failed: {details}")
    return True
