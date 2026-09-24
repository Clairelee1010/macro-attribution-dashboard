# P01-NEWS-001A — Live Source Reliability Fix

This patch fixes the production gap observed on 2026-09-24: the NEWS-001 core passed but live ingestion returned `0 items / 11 source errors` and took ~3 minutes.

## Changes
- GDELT remains the primary source.
- Google News RSS is a keyless fallback when GDELT is unavailable.
- 11 source tasks run concurrently instead of sequentially.
- Per-request timeout is bounded to 5 seconds.
- Acceptance now has two gates: deterministic core + strict live production.
- Strict live acceptance requires at least 1 live source and 1 current feed item.
- Daily production remains graceful: if all sources fail, it writes `UNAVAILABLE` rather than stale current news.

## Upload
Replace only these files on `main` (the repository is already operating there):
1. `market_intelligence.py`
2. `.github/workflows/p01_news_001_acceptance.yml`

Do not replace `index.html`, schema, or tests for this reliability patch.

Then Actions → P01-NEWS-001 Acceptance → **Run workflow** (new run; do not re-run an old snapshot).

Expected:
- `5 passed`
- `P01-NEWS-001: AVAILABLE | >0 items | >=1/11 sources available`
- `PASS LIVE PRODUCTION`
