# P01-005 — Signal Engine

P01-005 converts normalized, quality-gated market observations into deterministic descriptive signals for downstream intelligence modules.

## Pipeline
`raw_market_data.json → normalized_market_data.json → data_quality_report.json → signal_report.json`

## Design rules
- Signal ≠ recommendation. No BUY/SELL/LONG/SHORT/PAY/EXECUTE outputs.
- Bad or stale data must not silently become intelligence; failed metric-level quality gates produce `UNKNOWN`.
- Confidence measures evidence reliability for classification, **not** probability of a future market outcome.
- Thresholds in `config/signal_rules.json` are configurable prototype heuristics, not validated predictive thresholds or universal financial truths.
- BTC/ETH latest-price snapshots intentionally return `INSUFFICIENT_HISTORY`; trend/momentum requires historical features.
- P01-005 summarizes signal directions but does **not** declare a market regime. That responsibility belongs to P01-006.

## Taxonomy
Directions: `RISK_ON`, `RISK_OFF`, `NEUTRAL`, `UNKNOWN`.
Strengths: `WEAK`, `MODERATE`, `STRONG`, `UNKNOWN`.

## Output
`signal_report.json` schema version 5.0, preserving value, unit, source evidence, quality reasons, signal direction/strength, and evidence confidence.
