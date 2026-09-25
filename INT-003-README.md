# INT-003 — Integrated Intelligence Dashboard

## Purpose

INT-003 is the read-only presentation layer that brings the existing P01 and P02 product story together:

`P01 UNDERSTAND → P02 PREDICT / COMPARE → INT-002 CONTEXTUALIZE → INT-003 PRESENT`

It does **not** replace P01, P02, INT-001, or INT-002. It consumes their deterministic outputs and turns them into a recruiter-friendly integrated intelligence view.

## Inputs

- `data/integration/intelligence_overview.json` — INT-001 normalized P01 × P02 overview
- `data/integration/context_intelligence.json` — INT-002 context relationship output

## Outputs

- `data/integration/dashboard_payload.json` — INT-003 presentation payload
- `intelligence/index.html` — integrated bilingual dashboard

## Dashboard layers

1. Integrated Market Context — P01 regime/risk/evidence + P02 coverage
2. Context Relationship Summary — supported / divergent / mixed / insufficient / not applicable
3. P01 × P02 Intelligence Cards — venue probability + P01 evidence + deterministic explanation
4. System & Evidence Status — integration, guardrails, trust status, execution disabled

## Guardrails

- Venue probability is an observation, not an INT-003 forecast.
- P01 context is evidence/context, not causal proof.
- Candidate-specific political contracts remain `NOT_APPLICABLE` to P01 directional inference.
- Activity rank is not political preference, endorsement, or an election forecast.
- INT-003 produces no trading/payment recommendation and cannot execute actions.
- `execution_allowed` must remain `false`.

## Acceptance

Expected workflow summary:

```text
P01 Context Loaded          PASS
P02 Predictions Loaded      PASS
INT-002 Intelligence Loaded PASS
Relationship Rendering      PASS
Evidence Rendering          PASS
Political Guardrail         PASS
Execution                   DISABLED
INT-003: PASS
```
