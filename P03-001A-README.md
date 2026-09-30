# P03-001A · Multi-Source API Foundation

## Scope
Public, read-only BTC/ETH spot market data from Binance, MEXC, Gate, Bitget, Bybit and Coinbase Exchange.

## Guardrails
- NO_ACCOUNT
- NO_ORDER
- NO_WALLET
- NO_SIGNING
- NO_FUND_EXECUTION
- Execution is always `DISABLED`.

## Outputs
- `p03/data/exchange_registry.json`
- `p03/data/multi_source_market.json`
- `p03/data/source_validation.json`

## Run
`python p03_multi_source.py`

The collector tolerates individual source failures. Coverage, median-price deviation, source agreement, and data quality are calculated per asset. `AWAITING_FIRST_RUN` is intentional until GitHub Actions performs the first network-enabled run.
