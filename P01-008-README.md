# P01-008 — Market Risk Engine

Deterministic market-risk assessment built on P01-007 Attribution Engine.

Pipeline: Raw → Normalized → Data Quality → Signal → Regime → Attribution → Market Risk.

Output: `market_risk_report.json` schema 8.0.

The score is descriptive rather than predictive. Thresholds are configurable. Missing evidence reduces coverage/confidence. The engine emits no trading or execution recommendation.
