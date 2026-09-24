import json
from pathlib import Path

from jsonschema import validate


BASE_DIR = Path(__file__).resolve().parent

DEFAULT_SCHEMA_PATH = (
    BASE_DIR
    / "schemas"
    / "dashboard_data.schema.json"
)


def validate_dashboard_data(
    payload,
    schema_path=None,
):
    """
    Validate P01-010 dashboard data payload.

    The default schema path is resolved relative to this
    module rather than the current working directory.
    This keeps validation stable when tests or callers
    change the working directory.
    """

    if schema_path is None:
        schema_path = DEFAULT_SCHEMA_PATH
    else:
        schema_path = Path(schema_path)

    schema = json.loads(
        schema_path.read_text(encoding="utf-8")
    )

    validate(
        instance=payload,
        schema=schema,
    )

    return True
