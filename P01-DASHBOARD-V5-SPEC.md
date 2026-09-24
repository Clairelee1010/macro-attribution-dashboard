# P01 Dashboard v5 Productization Specification

## Product Goal
Turn the existing Macro Attribution dashboard into a portfolio-ready **Macro & Web3 Risk Intelligence Engine** presentation layer without moving intelligence logic into the browser.

## Product Principle
**Backend owns intelligence logic; frontend owns presentation logic.**

The UI must distinguish:
- **LIVE** — automated market feed.
- **GENERATED** — deterministic intelligence output produced by the P01 pipeline.
- **PROTOTYPE** — illustrative legacy content that is not current market evidence.

## Scope
### P01-UI-001 Dashboard v5 Integration
- `dashboard_data.json` is the primary intelligence contract.
- `live_market_data.json` remains the live market-data contract.
- No BUY / SELL / EXECUTE decision is produced in the UI.

### P01-UI-002 Executive Intelligence Layer
Display Market Regime, Market Risk, Evidence Confidence, Data Quality, Evidence Coverage and generated timestamp.

### P01-UI-003 Attribution / Evidence UX
Display eligible signals, risk drivers, evidence items and limitations.
Attribution is evidence alignment / potential driver context, **not causal proof**.

### P01-UI-004 Provenance / Freshness UX
Display per-metric FRESH / STALE / MISSING / ERROR states, source provenance, fallback-route presence and last update.

### P01-UI-005 Responsive + EN/ZH + UX Polish
- Responsive Tailwind layout.
- EN/ZH semantic labels.
- Graceful degradation: unavailable intelligence is explicitly marked and stale analysis is not presented as current.
- Risk and confidence remain separate concepts.

### P01-UI-006 GitHub Pages Production Acceptance
Acceptance checks must verify required DOM hooks, live/generated contracts, bilingual support, provenance/freshness states and graceful-degradation copy.

## Interpretation Rules
1. **Risk ≠ Confidence.**
2. Confidence describes evidence reliability, not market direction probability.
3. Attribution describes evidence alignment, not causal proof.
4. Prototype values must never be silently presented as current live evidence.
5. The product is decision support, not investment advice.

## Acceptance Criteria
- Product title identifies Macro & Web3 Risk Intelligence Engine.
- `dashboard_data.json` and `live_market_data.json` are fetched with cache-busting.
- Executive layer renders regime/risk/confidence/quality/coverage.
- Source provenance and FRESH/STALE/MISSING/ERROR are visible.
- LIVE / GENERATED / PROTOTYPE semantics are visible.
- EN/ZH switching preserves dynamic intelligence.
- Failure to load dashboard data produces an explicit unavailable state.
- Existing dashboard content remains available and responsive.
