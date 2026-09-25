# P02-002 — Polymarket Adapter

This milestone connects P02 to **public Polymarket market data** through the Gamma API and normalizes the response into the existing P02-001 prediction-market contract.

## Add these files to the existing repository

- `p02/adapters/__init__.py`
- `p02/adapters/polymarket_adapter.py`
- `tests/p02/test_polymarket_adapter.py`
- `.github/workflows/p02_polymarket.yml`

Do **not** replace the P02-001 schemas/configuration and do not modify P01.

## Output

The GitHub Action generates:

`data/p02/polymarket_markets.json`

The adapter is read-only and has no wallet, authentication, order placement, or execution capability.

## Important semantic note

For P02-002, the existing generic field `volume_usd` is populated from Polymarket's documented `volume24hr` value. This mapping is explicitly recorded in the generated document as `volume_semantics`.

`canonical_event` is deliberately written as `UNMATCHED:POLYMARKET:<market_id>` until P02-004 Event Matching assigns a real canonical event.

## Expected Action output

```text
P02-002 POLYMARKET ADAPTER
API Connectivity       PASS
Markets Retrieved      <n>
Normalization          PASS
Schema Validation      PASS
Source Provenance      PASS
Execution              DISABLED
P02-002: PASS
```

## Next milestone

P02-003 — Kalshi Adapter.
