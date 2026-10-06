# P02 Product Requirements Document — v1.0

**Product:** Tokenized Market & Prediction Intelligence  
**Portfolio Phase:** P02 — PREDICT / COMPARE  
**Version:** 1.0  
**Release Status:** PRODUCTION / FROZEN  
**Owner:** Claire Lee  
**Upstream:** P01 v1.0 — FROZEN  
**Downstream:** P03 — AI Agent Wallet + Policy Engine + x402  

## 1. Executive Summary

P02 extends the portfolio from understanding the current market environment to comparing how multiple markets price the same real-world event.

The production v1.0 scope focuses on prediction-market intelligence. It ingests Polymarket and Kalshi data, normalizes venue-specific contracts, attempts conservative event matching, detects cross-market discrepancies only when evidence supports comparability, links P01 macro context, preserves provenance, adds trust/security evidence, and stores historical snapshots.

P02 does not place orders, move funds, or claim that market-implied probabilities are forecasts.

## 2. Core Product Question

> Where do prediction markets disagree, what evidence supports the comparison, and is the evidence trustworthy enough to investigate further?

## 3. Product Principles

1. **Comparison before conclusion.**
2. **Same headline ≠ same contract.**
3. **Probability ≠ truth or forecast.**
4. **Discrepancy ≠ arbitrage.**
5. **Opportunity ≠ confidence.**
6. **Opportunity ≠ trust.**
7. **UNKNOWN trust status ≠ safe.**
8. **P01 context ≠ causal proof.**
9. **Intelligence before execution.**
10. **No forced matches.** Zero comparable events is a valid production state.

## 4. Target Users

- Product and technical teams researching prediction-market infrastructure.
- Analysts comparing market-implied probabilities across venues.
- Web3 / fintech teams exploring explainable market-intelligence workflows.
- Recruiters and hiring managers evaluating product architecture and technical PM execution.

## 5. Goals

- Connect multiple prediction-market venues through adapters.
- Normalize venue-specific records into a common contract.
- Match comparable events conservatively.
- Quantify cross-venue probability differences.
- Preserve liquidity, freshness, provenance, and resolution context.
- Connect P01 macro intelligence as read-only context.
- Represent trust/security evidence without implying a safety guarantee.
- Maintain historical snapshots and deterministic deltas.
- Present the system through a bilingual production dashboard.
- Keep execution disabled while exposing a future P03 handoff boundary.

## 6. Non-Goals

P02 v1.0 does not:
- execute trades or arbitrage;
- manage private keys or wallets;
- move user funds;
- guarantee venue safety;
- predict political or economic outcomes as model conclusions;
- treat probability as objective truth;
- force-match semantically different contracts;
- implement x402;
- implement tokenized-equity trading;
- implement stablecoin yield execution.

## 7. Production Architecture

```text
Polymarket ─┐
            ├─> Venue Adapters
Kalshi ─────┘
                  ↓
          Normalized Contract
                  ↓
       Canonical Event Matching
                  ↓
      Comparability Guardrails
                  ↓
         Discrepancy Engine
                  ↓
      Evidence / Data Confidence
             ↙           ↘
      P01 Context     Trust & Security
             ↘           ↙
          Intelligence Layer
                  ↓
        Historical Snapshots
                  ↓
      Bilingual Dashboard / API
                  ↓
       P03 Handoff Boundary
       execution_allowed=false
```

## 8. Functional Requirements

### FR-01 — Polymarket Adapter
The system shall retrieve Polymarket market records and normalize them into the P02 market contract.

### FR-02 — Kalshi Adapter
The system shall retrieve Kalshi market records and normalize them into the same contract.

### FR-03 — Source Provenance
Normalized records shall retain venue identity, venue market ID, source URL where available, retrieval time, freshness, and data-quality state.

### FR-04 — Canonical Event Matching
The system shall attempt to map venue contracts to a common real-world event without relying on headline similarity alone.

### FR-05 — Comparability
Matching logic shall consider event subject, outcome definition, time window, and resolution semantics. Uncertain pairs shall not be forced into a comparison.

### FR-06 — Implied Probability
The system shall preserve market-implied probability as an observed market value. It shall not label the value as a system forecast.

### FR-07 — Market Quality Context
Where available, the system shall retain volume, liquidity, bid, ask, spread, freshness, and data quality.

### FR-08 — Discrepancy Engine
For comparable events, the system shall calculate cross-venue probability differences in percentage points.

### FR-09 — Discrepancy Semantics
A discrepancy shall be presented as a difference in market pricing, not proof of arbitrage or mispricing.

### FR-10 — P01 Context Bridge
P02 shall consume P01 regime and signal outputs as read-only supporting context.

### FR-11 — Trust & Security Intelligence
The system shall expose evidence-based trust/security status. `UNKNOWN` shall remain a valid state and shall not be converted into `SAFE`.

### FR-12 — Bilingual Intelligence
The dashboard shall support Traditional Chinese and English presentation.

### FR-13 — Dashboard Payload
The intelligence pipeline shall generate a deterministic dashboard payload separated from presentation logic.

### FR-14 — Historical Snapshot
The system shall store append-only P02 snapshots containing market observations, discrepancies, P01 context, and trust/security evidence.

### FR-15 — Historical Intelligence
With at least two snapshots, the system shall calculate deterministic probability changes in percentage points. New markets without prior observations shall be labeled `INSUFFICIENT_HISTORY`.

### FR-16 — Production Acceptance
A read-only release gate shall validate all required production artifacts and conservative semantics.

### FR-17 — Execution Boundary
All P02 production outputs shall keep execution disabled. Any future execution capability belongs to P03.

## 9. Milestone Acceptance

| Milestone | Capability | Status |
|---|---|---|
| P02-001 | Foundation / schemas | COMPLETE |
| P02-002 | Polymarket adapter | COMPLETE |
| P02-003 | Kalshi adapter | COMPLETE |
| P02-004 | Event matching | COMPLETE |
| P02-005 | Discrepancy engine | COMPLETE |
| P02-006 | P01 context bridge | COMPLETE |
| P02-007 | Trust & Security | COMPLETE |
| P02-008 | Intelligence dashboard | COMPLETE |
| P02-008.1 | P01 UI alignment | COMPLETE |
| P02-008.2 | Typography / density alignment | COMPLETE |
| P02-009 | Historical intelligence | COMPLETE |
| P02-010 | Production acceptance | PASS |

Production acceptance confirmed:
- Polymarket Data — PASS
- Kalshi Data — PASS
- Event Matching — PASS
- Discrepancy Engine — PASS
- P01 Context — PASS
- Trust & Security — PASS
- Dashboard Payload — PASS
- Historical Intelligence — PASS
- Historical State — COMPARABLE
- Execution — DISABLED

`Matched Events = 0` and `Discrepancy Signals = 0` are valid states when the current sample does not contain sufficiently comparable cross-venue contracts.

## 10. Data Semantics

- **LIVE** — automated market observations.
- **GENERATED** — deterministic intelligence derived from source data.
- **EVIDENCE** — evidence-based status whose confidence depends on available support.

These labels must not be collapsed into a single “AI prediction” concept.

## 11. Risks and Mitigations

**Contract mismatch:** Similar wording can represent different settlement conditions.  
Mitigation: canonical-event and comparability checks; no forced matching.

**Thin liquidity:** Probability may be unstable or difficult to transact against.  
Mitigation: retain liquidity/spread context and avoid treating price as truth.

**Stale or missing data:** Cross-venue comparison can become misleading.  
Mitigation: freshness and data-quality states.

**Venue/security risk:** Attractive pricing does not imply a trustworthy venue.  
Mitigation: separate Trust & Security evidence layer.

**Causal overclaiming:** Macro context can be mistaken for proof of causality.  
Mitigation: P01 is read-only supporting context.

**Automation overreach:** Intelligence may be mistaken for an execution system.  
Mitigation: `execution_allowed=false`; execution belongs to P03.

## 12. KPIs / Evaluation Metrics

For the portfolio prototype:
- adapter availability;
- schema validation pass rate;
- source-provenance coverage;
- event-match precision over match volume;
- freshness coverage;
- percentage of discrepancies with adequate comparability evidence;
- historical snapshot continuity;
- production acceptance pass rate.

No KPI is defined as “number of signals generated,” because manufacturing signals would conflict with the product’s evidence-first design.

## 13. Post-v1.0 Extension Roadmap

### Tokenized Market Intelligence
- Tokenized U.S. equities / RWA
- 24/7 vs traditional-session price discovery
- weekend / off-hours repricing
- traditional open vs tokenized implied move

### Crypto / Stablecoin Yield Intelligence
- USDT / USDC yield comparison
- APY and term
- liquidity and withdrawal conditions
- counterparty / venue risk
- security incidents
- freshness
- risk-adjusted yield rather than highest-APY ranking

These are preserved roadmap items and are not part of the frozen P02 v1.0 production scope.

## 14. P03 Handoff

P03 may consume P02 intelligence through an explicit policy boundary:

```text
P02 Signal / Opportunity
        ↓
Security / Trust Check
        ↓
Risk Check
        ↓
Policy Check
        ↓
Spending Limit / Whitelist
        ↓
Human Approval
        ↓
Wallet Authorization
        ↓
x402 / Transaction
        ↓
Audit Log
```

P02 itself remains non-executing.

## 15. Release State

**P02 v1.0 — PRODUCTION / FROZEN**

Allowed after freeze:
- bug fixes;
- security fixes;
- provider/API maintenance;
- documentation corrections that do not expand product scope.

New product capabilities belong to a separately scoped extension or later portfolio phase.
