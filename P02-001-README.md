# P02-001 — Foundation

This package creates the data-contract foundation for **P02 — Tokenized Market & Prediction Intelligence**.

## What this milestone does

- Defines normalized prediction-market data.
- Defines canonical-event matching output.
- Defines cross-market discrepancy output.
- Defines Trust & Security event data.
- Adds configurable topics and thresholds.
- Adds synthetic fixtures for validation.
- Adds local validation, tests, and a GitHub Actions workflow.

## Important

All files under `p02/fixtures/` are **synthetic demo data**. They are not current Polymarket, Kalshi, or security-event observations.

P02-001 does **not** connect to live APIs and does **not** execute trades.

## Validate locally

```bash
python -m pip install jsonschema pytest
python p02/validate_p02.py
pytest -q tests/p02
```

Expected result:

```text
PASS prediction_market.sample.json
PASS canonical_event.sample.json
PASS discrepancy.sample.json
PASS security_event.sample.json
PASS configuration
P02-001 FOUNDATION: PASS
```

## Next milestone

**P02-002 — Polymarket Adapter**

It will map live/public Polymarket market data into `prediction_market.schema.json` without changing the downstream data contract.
