# Claire Lee · Product Lab portfolio notes

## Trade Clarity

**Status:** executable bilingual portfolio prototype, not a production trading service.

**Problem hypothesis:** first-time users may confuse order acceptance with complete execution, miss slippage and fees, or misunderstand a partially filled order. This hypothesis has not yet been validated through user interviews.

**Product objective:** make order intent, estimated impact and actual status understandable within one short flow.

**Core flow:** choose buy/sell and Market/Limit → enter BTC quantity or reference USD amount → preview depth, average, fees and reserves → explicitly confirm → inspect fills and remaining quantity → cancel a resting order or advance a fixture scenario.

**Implemented controls:** integer accounting, limit-price conditions, cumulative fee rounding, reserved funds, one working order, stale-preview rejection and single-use confirmation. Scenario controls are manual and deterministic.

**Supported outcomes:** Filled; Open; Partially filled with remainder open; Partially filled with market remainder cancelled; Cancelled remainder.

**Demo assumptions:** initial USD 1,000 and 0.02 BTC; 0.10% cumulative demo fee rounded up to cents; BTC atoms of 10^-8; single BTC/USD pair; at most 1 BTC per order; limit price at most USD 100,000; 3 external book levels; at most one working order. Session resets on reload. Buy notional rounds up to cents; sell notional rounds down. These are simulator rules, not a venue’s implementation or fees.

## Ownership statement

Claire requested the portfolio direction and product scope. Codex assisted with interface code, matching simulation, automated tests and documentation. Claire’s next acceptance task is to personally complete the test scenarios on the deployed site and document her design decisions. Do not claim interviews, engagement improvements, commercial adoption, smart-contract execution or live AI explanations that have not occurred.

## Resume draft — use after deployment and personal acceptance

Developed an AI-assisted trading UX prototype with order previews, simulated market and limit execution, fee and slippage explanations, and order lifecycle tracking. Documented design tradeoffs and validated core behavior with automated tests.

Here, “AI-assisted” describes the development workflow. The prototype’s explanations are deterministic templates, not model-generated answers. Adjust ownership verbs to actual participation.

## Interview walkthrough

1. Explain the comprehension problem as a hypothesis, not a proven customer finding.
2. Demonstrate a market buy that crosses two price levels, with visible fees and baseline-relative slippage.
3. Demonstrate a limit buy at USD 59,900 waiting against the default USD 60,000 best ask. Apply the lower-price fixture and inspect fills.
4. Demonstrate 0.005 BTC against the thin fixture: 0.003 BTC fills and the unfilled 0.002 BTC is cancelled for a market order.
5. Explain why active limit orders reserve funds, why a preview expires after a market change, and why a cancelled remainder does not undo executed fills.
6. State the simplified scope, automated checks and remaining browser/user validation honestly.

## Next research task (not completed)

Ask participants to explain the above three outcomes in their own words. Record task completion, comprehension accuracy, unintended actions and time. Preserve anonymized observations, consent and protocol. Establish a baseline before claiming improvements.

## Official mechanism references

- https://help.coinbase.com/en/coinbase/trading-and-funding/advanced-trade/order-management
- https://www.coinbase.com/legal/trading_rules

References checked 2026-10-17 Taiwan time for conceptual grounding. They do not validate this simulator’s fictional data or define its fee schedule.
