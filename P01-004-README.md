# P01-004 — Data Quality Engine

P01-004 determines whether normalized market observations are reliable enough for downstream intelligence. It is intentionally separate from market risk: **data quality answers “Can I trust the input?”, not “Is the market risky?”**

## Scope

- Completeness: expected observations are present and usable.
- Freshness: observation age is evaluated against metric-specific, configurable thresholds.
- Validity: values are finite, timestamps parse, units exist, and upstream status is usable.
- Consistency: deterministic Raw → Normalized transformations are re-checked.
- Source evidence: PRIMARY/FALLBACK/NONE and upstream errors are preserved without arbitrary vendor scoring.
- Quality score: deterministic weighted score in `[0,1]`.
- Quality gate: `PASS`, `DEGRADED`, or `BLOCK`.

## Configurable MVP rules

Rules live in `config/data_quality_rules.json`. Thresholds and weights are portfolio engineering defaults, not financial-industry standards. They can be tuned after empirical validation.

Default freshness thresholds: US10Y/DXY/VIX 36h; BTC/ETH 2h. Default component weights are equal (25% each). Gate thresholds: PASS ≥ 0.90, DEGRADED ≥ 0.60, otherwise BLOCK.

## Pipeline

`raw_market_data.json` → P01-003 normalization → `normalized_market_data.json` → P01-004 quality engine → `data_quality_report.json` → future P01-005 Signal Engine.

The current `live_market_data.json` v1.0 remains backward compatible for the existing dashboard.

## Output contract

`data_quality_report.json` uses schema version 4.0 and includes component scores, counts, per-metric evidence/reasons, overall score, and quality gate.

## Design principles

- Deterministic core; no LLM is required for quality decisions.
- Never silently treat stale data as current.
- Explain every degradation reason.
- Preserve provenance.
- Do not equate quality score with market risk or investment confidence.
