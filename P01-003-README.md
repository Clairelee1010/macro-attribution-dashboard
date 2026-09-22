# P01-003 — Normalization Layer

P01-003 converts the validated P01-002 raw market observations into a deterministic canonical representation for downstream intelligence modules.

## Boundary

`raw_market_data.json` remains the immutable ingestion contract. P01-003 does **not** calculate signals, market regimes, risk scores, attribution, or investment actions.

## Pipeline

`Adapters → Raw schema v2.0 → Normalization → Normalized schema v3.0 → P01-004 Data Quality`

## Current rules

- US10Y: percent → decimal (`raw_value / 100`)
- DXY: identity, INDEX
- VIX: identity, INDEX
- BTC: identity, USD
- ETH: identity, USD
- timestamps are canonicalized to UTC ISO-8601
- raw value/unit are retained beside normalized value/unit
- every record includes deterministic transformation lineage and source provenance

## Output

`normalized_market_data.json`

The existing `live_market_data.json` v1.0 remains unchanged for frontend backward compatibility.

## Acceptance

- five expected metrics normalized
- raw values preserved
- canonical units validated
- deterministic transformation rules validated
- timestamps canonicalized
- transformation lineage present
- normalized schema v3.0 validated
- raw schema v2.0 remains compatible
- live schema v1.0 remains compatible
