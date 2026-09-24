# P01-NEWS-001 Batch Upload

Recommended branch: `feature/p01-news-001-market-intelligence`

Upload/replace these files while preserving paths:

- `market_intelligence.py`
- `market_intelligence_feed.json`
- `schemas/market_intelligence_feed.schema.json`
- `index.html`
- `tests/test_market_intelligence.py`
- `.github/workflows/p01_news_001_acceptance.yml`
- `.github/workflows/daily_update.yml`
- `P01-NEWS-001-README.md`

## Expected GitHub flow
1. Create the feature branch from latest `main`.
2. Upload this package preserving folders.
3. Open Actions → **P01-NEWS-001 Acceptance** → Run workflow if it did not trigger automatically.
4. Expected deterministic result: `5 passed`.
5. The live ingestion smoke test may return `AVAILABLE` with current articles or `UNAVAILABLE` when GDELT is temporarily unreachable. Source failure must not resurrect prototype news.
6. Open PR to `main`; merge only after Acceptance is green.
7. Run **Daily Data Update** on `main`.
8. Confirm `market_intelligence_feed.json` is generated/committed and GitHub Pages shows current feed cards or an explicit UNAVAILABLE state.

## Production acceptance
- Market & Web3 Intelligence Feed is visible.
- Feed shows source provenance, publication time, freshness, topic, Why It Matters, Linked P01 Context, evidence note, limitation, original-source link.
- Company-origin content is marked OFFICIAL and is not described as independent verification.
- FRESH / STALE are explicit.
- Old prototype news is never shown as CURRENT.
- No stock recommendation matrix or Soft Robi execution log is rendered in the feed.
- EN/ZH switching preserves the feed.
- GDELT/source outage produces UNAVAILABLE instead of stale-current content.
