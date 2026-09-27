# INT-005A · Multi-Asset Market Watchlist + Relationship Cleanup

## Goal
Differentiate Integrated Intelligence from P02 by adding a representative cross-asset watchlist and reducing duplicated prediction-market cards.

## Scope
- 30 representative assets: 15 US equities, 6 equity ETFs, 4 US Treasury ETFs, 2 gold ETFs, 3 crypto assets.
- Current price plus 1D / 7D / 30D change when source history is available.
- Filters: US Equity / ETF / US Treasury / Gold / Crypto and symbol/name search.
- Relationship Intelligence is limited to the first 5 upstream relationship cards; the full prediction-market view remains in P02.
- Existing INT-004 snapshot and indexed trend remain unchanged.

## Guardrails
- The 30-asset universe is representative, not a popularity, performance, or investment ranking.
- No BUY / SELL / LONG / SHORT / execution output.
- No synthetic price history. Unavailable data remains explicit.
- Political prediction-market observations remain venue observations only; INT does not forecast election outcomes.
- Tokenization mapping is intentionally deferred to INT-005B and must be source-verifiable.

## Data artifact
`data/integration/multi_asset_watchlist.json`

## Generator
`multi_asset_watchlist.py`

## UI
`intelligence/index.html`
