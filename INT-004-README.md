# INT-004 · Cross-Market Trend Intelligence

## Goal
Differentiate Integrated Intelligence from P02 by adding cross-market context before relationship analysis.

## Added
- Cross-Market Snapshot: BTC, ETH, S&P 500, DXY, US10Y, VIX.
- 1D / 7D change where source history is sufficient.
- 7D / 30D indexed-performance chart (first available point = 100).
- Explicit `UNAVAILABLE` / `INSUFFICIENT_HISTORY` states.
- Daily artifact: `data/integration/cross_market_trends.json`.

## Guardrails
- Read-only context; no trade recommendation or execution.
- INT-004 does not modify P01 regime/risk/signal calculations.
- Different units are never plotted on one raw-price axis; the comparison chart uses indexed performance.
- Missing history is shown explicitly rather than fabricated.

## Data sources
- BTC / ETH: CoinGecko public market-chart API.
- DXY / VIX / US10Y / S&P 500: Yahoo Finance via `yfinance`.

## Product flow
Executive Intelligence → Cross-Market Snapshot → Cross-Market Trend → Context Relationship Intelligence.
