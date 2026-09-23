# P01-009 — Confidence & Evidence Engine

P01-009 adds a deterministic reliability layer after P01-008 Market Risk. It answers **how well the current intelligence assessment is supported by available evidence**, without treating confidence as a forecast probability.

## Inputs
- `data_quality_report.json` (P01-004)
- `regime_report.json` (P01-006)
- `attribution_report.json` (P01-007)
- `market_risk_report.json` (P01-008)

## Output
- `confidence_evidence_report.json`, schema version `9.0`

## Deterministic components
The score combines data quality, evidence coverage, source reliability, signal agreement, attribution support, and upstream market-risk confidence. Weights are configurable in `config/confidence_evidence_rules.json`.

## Product semantics
`confidence_score` is evidence reliability, **not** the probability of a future market outcome and not causal certainty. The engine emits no BUY/SELL/LONG/SHORT/PAY/EXECUTE recommendation. Evidence items preserve upstream engine and artifact references for auditability.

## Acceptance
The GitHub Actions workflow `test_confidence_evidence.yml` verifies repository structure, imports, deterministic tests, live pipeline execution, JSON artifacts, schema version, score bounds, evidence coverage, and confidence level.
