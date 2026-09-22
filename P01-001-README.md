# P01-001 Multi-Source Data Adapter Layer
Routing: US10Y FRED DGS10 primary -> yfinance fallback; DXY/VIX yfinance; BTC/ETH CoinGecko public endpoint -> yfinance fallback.

Reliability: retries, HTTP timeout, per-metric failure isolation, source provenance, FRESH/STALE/MISSING/ERROR, fixed five-metric quality denominator, backward-compatible schema_version 1.0.

Run `P01-001 Adapter Acceptance` before merge to main.
