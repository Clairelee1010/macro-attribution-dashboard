# P03-002A · Dynamic Tokenized Equity Source & Asset Verification

Read-only intelligence layer for AAPL ↔ AAPLx and NVDA ↔ NVDAx.

- Verifies xStocks product mapping before price comparison.
- Traditional adapter: Alpaca IEX when GitHub Secrets are configured; yfinance public fallback otherwise.
- Tokenized adapter: xStocks / Backed public API.
- Missing/unavailable data remains explicit as `INSUFFICIENT_EVIDENCE`.
- `Discrepancy ≠ Arbitrage`.
- No account, order, wallet, signing, or fund execution capability.

Optional GitHub repository secrets:
- `APCA_API_KEY_ID`
- `APCA_API_SECRET_KEY`

Without these secrets the workflow still runs using the public fallback for traditional-equity context.
