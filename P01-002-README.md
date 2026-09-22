# P01-002 — Raw Data Schema

## Objective
Establish a machine-validatable raw-data contract between P01-001 source adapters and downstream normalization/intelligence layers.

## Contract
`schemas/raw_market_data.schema.json` uses JSON Schema Draft 2020-12. The canonical raw payload is `raw_market_data.json` with `schema_version: 2.0`.

Each raw metric record preserves source evidence: metric identity, category, ticker, raw numeric values, unit, provider, PRIMARY/FALLBACK/NONE provenance, observation/fetch timestamps, quality status, and provider error context.

## Compatibility
`live_market_data.json` remains schema `1.0` so the existing P01-000D frontend requires no changes. P01-002 adds a canonical raw contract; it does not yet perform P01-003 normalization.

## Validation rules
- Required fields cannot silently disappear.
- Status is restricted to FRESH / STALE / MISSING / ERROR.
- Source type is restricted to PRIMARY / FALLBACK / NONE.
- FRESH/STALE records require a numeric value and observation timestamp.
- NONE source records cannot claim FRESH/STALE.
- Date-time fields are format checked.
- Unexpected fields are rejected to prevent accidental contract drift.

## Acceptance
1. Deterministic schema tests pass.
2. Existing adapter/integration tests remain green.
3. Live pipeline creates `raw_market_data.json` and validates it before publishing.
4. `live_market_data.json` remains v1.0 frontend-compatible.
5. `pipeline_status.json` reports P01-002 and raw schema validity.
6. One provider failure remains isolated by the P01-001 adapter layer.

## Boundary
P01-002 defines and validates raw evidence. Canonical transformations, unit harmonization, derived features, and normalized records belong to P01-003.
