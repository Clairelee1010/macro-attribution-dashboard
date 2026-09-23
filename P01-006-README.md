# P01-006 Market Regime Engine

P01-006 aggregates quality-gated P01-005 signals into an explainable market regime.

Pipeline: Raw → Normalized → Data Quality → Signals → Market Regime.

## Outputs
- `regime_report.json`
- Regime: `RISK_ON`, `NEUTRAL`, `RISK_OFF`, or `UNKNOWN`
- Deterministic score in `[-1, 1]`
- Evidence confidence, coverage, drivers, contradictions, and excluded signals

## Product semantics
- Regime score is a deterministic cross-signal balance, not a forecast probability.
- Confidence measures evidence reliability, not probability of a market outcome.
- `RISK_ON` is not a BUY recommendation; `RISK_OFF` is not a SELL recommendation.
- Unknown or insufficient-history signals are excluded rather than silently forced into a regime.
- Contradictory evidence is preserved and reduces confidence.

## Design
The engine is deterministic and rule-based. LLMs may explain a regime later, but they do not assign it.
