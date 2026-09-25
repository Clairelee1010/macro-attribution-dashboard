# P02-009 — Historical Intelligence

## Purpose
P02-009 adds a historical evidence layer to the existing P02 production pipeline without changing P01, P02-001–008.2, or the current dashboard UI.

It answers a new product question:

> How did market-implied probabilities, discrepancies, P01 macro context, and trust evidence change over time?

## Components
- `p02/historical_snapshot.py` — creates a compact append-only snapshot from current P02 outputs.
- `p02/historical_intelligence.py` — compares the latest snapshot with the previous snapshot and builds deterministic deltas.
- `tests/p02/test_historical_intelligence.py` — validates semantics and percentage-point changes.
- `.github/workflows/p02_historical_intelligence.yml` — manual + daily historical collection.

## Data outputs
- `data/p02/history/YYYY-MM-DD/HHMMSS.json`
- `data/p02/historical_intelligence.json`

The first run is expected to return `BASELINE_ONLY`. That is correct: one observation is not enough to calculate historical change.

From the second snapshot onward, unchanged market IDs can produce:
- current probability
- previous probability
- probability change in percentage points
- direction: `UP_STRONG`, `UP`, `STABLE`, `DOWN`, `DOWN_STRONG`

If a market did not exist in the previous snapshot, its direction is `INSUFFICIENT_HISTORY`; the system does not invent a comparison.

## Guardrails
- Market-implied probability is an observation, not a forecast.
- Historical movement does not prove causality.
- Discrepancy is not proof of arbitrage.
- P01 remains read-only context.
- Execution remains disabled.

## Schedule
The workflow runs daily at `01:35 UTC` and can also be triggered manually.

## Acceptance
Expected workflow output:

`P02-009 HISTORICAL INTELLIGENCE: PASS`

On first run:
- `Snapshot Count: 1`
- `History State: BASELINE_ONLY`

On later runs:
- `Snapshot Count: >= 2`
- `History State: COMPARABLE`

## Recommended commit
`Add P02-009 historical intelligence`
