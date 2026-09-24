# P01-010 — Dashboard v5.0

## Product goal
Turn the validated P01-001–009 intelligence pipeline into a recruiter-ready decision-support interface without moving analytical logic into the browser.

## Architecture
Validated intelligence artifacts → `dashboard_builder.py` → `dashboard_data.json` (schema 10.0) → `index.html`.

## Product semantics
- **Market Risk** is a deterministic current-environment assessment, not a return forecast.
- **Evidence Confidence** measures reliability/support of available evidence, not causal probability.
- **Attribution** describes relative evidence alignment, not causal proof.
- Dashboard v5.0 emits no BUY/SELL/LONG/SHORT/PAY/EXECUTE recommendation.

## UX
Executive cards: Market Regime, Market Risk, Evidence Confidence, Data Quality, Last Updated.
Supporting panels: signals, attribution/risk drivers, evidence/limitations and provenance. Chinese/English switching is preserved. Missing dashboard data degrades to an explicit unavailable state rather than silently presenting stale intelligence as current.

## Acceptance
`P01-010 Dashboard v5 Acceptance` validates repository structure, deterministic tests, full pipeline generation, schema 10.0, and required dashboard artifacts.
