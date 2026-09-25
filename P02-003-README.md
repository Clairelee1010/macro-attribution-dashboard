# P02-003 — Kalshi Adapter

Adds a read-only Kalshi public market-data adapter to the existing P02 architecture.

## Files
- `p02/adapters/kalshi_adapter.py`
- `tests/p02/test_kalshi_adapter.py`
- `.github/workflows/p02_kalshi.yml`
- `P02-003-README.md`

Keep all P01, P02-001, and P02-002 files.

## Output
`data/p02/kalshi_markets.json`

## Expected Action
```text
P02-003 KALSHI ADAPTER
API Connectivity       PASS
Markets Retrieved      > 0
Normalization          PASS
Schema Validation      PASS
Source Provenance      PASS
Execution              DISABLED
P02-003: PASS
```

## Next
P02-004 — Canonical Event Matching.
