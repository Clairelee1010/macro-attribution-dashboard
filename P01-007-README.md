# P01-007 Attribution Engine

P01-007 converts the deterministic P01-006 market-regime evidence into an explainable attribution report.

## Pipeline

Raw Data → Normalization → Data Quality → Signals → Market Regime → Attribution

## Responsibilities

- identify eligible regime drivers;
- calculate relative evidence contribution shares;
- separate supporting, conflicting, and contextual evidence;
- expose attribution confidence and evidence agreement;
- preserve excluded/unknown evidence;
- emit `attribution_report.json` for downstream explanation/UI layers.

## Product semantics

**Attribution is not causality.** Contribution share is the relative share of absolute weighted evidence among eligible drivers. It is not a causal-effect estimate and is not an outcome probability.

**Confidence is evidence reliability, not causal probability.**

P01-007 emits no BUY/SELL/LONG/SHORT/PAY/EXECUTE recommendation.
