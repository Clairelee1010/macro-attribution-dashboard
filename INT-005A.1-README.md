# INT-005A.1 — Watchlist Rendering Hotfix

## Scope
Hotfix only. No change to P01/P02 intelligence logic, INT-004 market data pipeline, or execution policy.

## Fixes
1. Declare `WATCH`, `WATCH_FILTER`, and `WATCH_QUERY` before render functions execute.
2. Restore the missing **Multi-Asset Market Watchlist** DOM section.
3. Keep the 30-asset representative universe and existing `multi_asset_watchlist.json` pipeline unchanged.
4. Keep **Top Relationship Insights** capped at 5 records with navigation to full P02.

## Expected UI order
Executive Intelligence → Cross-Market Snapshot → Cross-Market Trend → Multi-Asset Market Watchlist → Context Relationship → Top Relationship Insights → System & Evidence Status.

## Guardrails
- Representative universe, not a popularity ranking.
- No investment recommendation.
- No synthetic price/history data.
- Execution remains disabled.
