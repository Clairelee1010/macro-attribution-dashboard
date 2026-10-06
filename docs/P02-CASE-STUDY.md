# P02 Case Study — From Market Probabilities to Explainable Cross-Market Intelligence

## Executive Summary

P02 began with a simple portfolio idea: aggregate prediction-market data from Polymarket and Kalshi and show where probabilities differ.

The product challenge quickly became more interesting.

A 62% price on one venue and 55% on another is not automatically a meaningful seven-point discrepancy. The two contracts may resolve on different dates, use different wording, depend on different settlement sources, or have very different liquidity. A dashboard that ignores those differences can look sophisticated while producing misleading intelligence.

P02 was therefore designed around a stricter question:

> Can the system compare market expectations without pretending that every similar-looking contract is equivalent?

The result is an evidence-driven, bilingual cross-market intelligence prototype that connects live prediction-market observations, conservative event matching, discrepancy analysis, P01 macro context, trust/security evidence, and historical intelligence—while deliberately keeping execution disabled.

## The Product Problem

Prediction markets turn event contracts into observable market-implied probabilities. That makes them useful as an intelligence source, but aggregation introduces several risks:

- venue APIs expose different structures;
- similar headlines can represent different contracts;
- liquidity affects how meaningful a quoted probability is;
- stale data can create false discrepancies;
- venue/security risk is separate from opportunity;
- a market probability is not an objective forecast;
- a discrepancy is not automatically an arbitrage opportunity.

The PM problem was therefore not “how do I show more data?” It was “how do I make cross-market comparison defensible?”

## My Role

For this portfolio project I acted as Product / Technical PM across:
- product framing;
- PRD and milestone design;
- data-contract definition;
- architecture;
- acceptance criteria;
- implementation planning;
- GitHub Actions automation;
- bilingual UX;
- production validation;
- release/freeze governance.

## Decision 1 — Normalize Before Comparing

Polymarket and Kalshi are different products with different data structures. P02 first converts venue-specific records into a shared contract containing fields such as venue, market ID, question, outcome, implied probability, volume, liquidity, bid/ask, spread, resolution information, provenance, freshness, and data quality.

This creates a stable product boundary between data ingestion and intelligence logic.

## Decision 2 — Same Headline Does Not Mean Same Contract

The biggest design risk was false comparability.

Instead of matching contracts because their text looks similar, P02 introduced canonical-event matching and comparability guardrails. Event subject, outcome definition, date/window, and resolution semantics matter.

This led to an important production decision:

> Zero matched events is better than a fabricated match.

At production acceptance, the current sample contained 20 Polymarket markets and 20 Kalshi markets but no sufficiently comparable cross-venue event. The system correctly returned `Matched Events = 0` and `Discrepancy Signals = 0`.

That was treated as a valid production state, not a failure.

## Decision 3 — Probability Is an Observation, Not a Forecast

P02 reports market-implied probabilities as market observations.

It does not transform them into statements such as “the event will happen.” This distinction is especially important for macroeconomic, policy, and political-event contracts.

The product therefore separates:
- what a market currently prices;
- how two venues differ;
- how strong the supporting evidence is;
- what the broader P01 context shows.

## Decision 4 — Discrepancy Is Not Arbitrage

If two genuinely comparable contracts price the same event differently, the raw difference is useful intelligence. It is still not sufficient to claim an executable arbitrage.

Transaction costs, spread, liquidity, settlement rules, venue access, counterparty risk, and timing all matter.

P02 therefore treats discrepancy as an investigation signal, not a trading recommendation.

## Decision 5 — Connect P01 Without Claiming Causality

P01 answers “what is the current macro and Web3 risk environment?”

P02 answers “how are markets pricing future events, and where do comparable markets disagree?”

The P01 Context Bridge lets P02 read regime and signal outputs as supporting context. It does not say that a P01 signal caused a prediction-market move.

This preserves the portfolio narrative:

```text
P01 — UNDERSTAND
        ↓
P02 — PREDICT / COMPARE
        ↓
P03 — GOVERN / ACT
```

## Decision 6 — Opportunity and Trust Are Separate

A venue can show an interesting price, high yield, or strong liquidity and still carry operational, custody, counterparty, or security risk.

P02 therefore introduced a Trust & Security layer instead of burying security inside an opportunity score.

A particularly important semantic rule is:

> `UNKNOWN` does not mean safe.

The product reports the evidence state that is actually available rather than converting missing evidence into a reassuring label.

## Decision 7 — Add Time, Not Just a Snapshot

A single dashboard only shows the current state.

P02-009 added historical snapshots and deterministic change intelligence. The system now stores observations over time and, once at least two snapshots exist, calculates probability changes in percentage points.

If a market is new and has no previous observation, the system returns `INSUFFICIENT_HISTORY` rather than inventing a comparison.

This moves the product from a static aggregator toward an intelligence system capable of answering:

> What changed?

## Production Architecture

```text
Polymarket + Kalshi
        ↓
Venue Adapters
        ↓
Normalized Market Contract
        ↓
Canonical Event Matching
        ↓
Comparability Guardrails
        ↓
Discrepancy Engine
        ↓
Evidence / Data Confidence
      ↙                 ↘
P01 Macro Context    Trust & Security
      ↘                 ↙
       Intelligence Layer
              ↓
      Historical Layer
              ↓
      Bilingual Dashboard
```

## Production Outcome

P02 v1.0 reached the following release state:

- Polymarket live adapter — PASS
- Kalshi live adapter — PASS
- normalized production datasets — PASS
- event-matching pipeline — PASS
- discrepancy engine — PASS
- P01 context bridge — PASS
- Trust & Security — PASS
- bilingual dashboard — PASS
- historical intelligence — PASS
- historical state — COMPARABLE
- production acceptance — PASS
- execution — DISABLED

The release gate explicitly accepts zero matched events when evidence does not justify a comparison.

## What Changed From the Initial Idea

The initial concept could have become a conventional “prediction market aggregator.”

The final product is more defensible because it focuses on:
- semantic comparability;
- evidence quality;
- provenance;
- graceful handling of missing matches;
- trust/security separation;
- historical change;
- explicit execution boundaries.

That change reflects a broader product lesson: intelligence products create value not only by finding signals, but also by knowing when **not** to produce one.

## Tradeoffs

### Precision over coverage
Conservative matching reduces the number of cross-venue signals but lowers the risk of misleading comparisons.

### Deterministic core over black-box conclusions
The intelligence path remains inspectable and testable.

### Evidence state over safety labels
Trust/security reporting avoids claiming more than the available evidence supports.

### Production boundary over feature accumulation
Tokenized equities and crypto/stablecoin yield remain in the roadmap instead of being rushed into v1.0.

## Next Product Opportunities

### Tokenized Market Intelligence
A future extension can compare tokenized U.S. equity / RWA pricing with traditional market sessions and study off-hours price discovery.

### Crypto / Stablecoin Yield Intelligence
A future extension can compare USDT/USDC opportunities using APY, term, liquidity, counterparty risk, venue/security evidence, and freshness—producing risk-adjusted intelligence rather than simply ranking the highest advertised yield.

### P03 — AI Agent Wallet + Policy Engine + x402
P03 moves from intelligence to governed action. Signals would pass through security, risk, policy, spending-limit, whitelist, human-approval, wallet-authorization, and audit controls before any transaction.

## Portfolio Takeaway

P01 demonstrates how to **understand** a market environment.

P02 demonstrates how to **compare** forward-looking market expectations without overclaiming what the data means.

P03 will demonstrate how to **govern and act** on intelligence under explicit authorization and risk controls.

## Final Status

**P02 v1.0 — PRODUCTION / FROZEN**

The product is frozen for feature development. Future changes to v1.0 are limited to bug fixes, security fixes, provider/API maintenance, and documentation corrections.
