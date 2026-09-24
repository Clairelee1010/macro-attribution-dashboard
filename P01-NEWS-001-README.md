# P01-NEWS-001 — Multi-Source Market & Social Intelligence Feed

## Goal
Replace static prototype news cards with a current, provenance-aware intelligence feed.

## Sources
- GDELT DOC 2.0 ArticleList metadata for current market/Web3 news.
- Official-company domain queries for Binance, OKX, Coinbase, Circle, Bybit, Bitget, Gate and MEXC.
- X adapter is intentionally `NOT_CONFIGURED`; Threads is `PHASE_2`. Social API availability never blocks P01.

## Product rules
1. Official company announcements are first-party evidence, not independent verification.
2. FRESH <= 36h; STALE <= 7d; older items are not rendered as current.
3. Topic and P01-context matching are deterministic keyword/rule mappings.
4. News association does not prove causality.
5. No BUY/SELL, stock recommendations, or execution logs are produced.
6. Source failure degrades to `UNAVAILABLE`; stale prototype content is never substituted.

## Artifact
`market_intelligence_feed.json` using `schemas/market_intelligence_feed.schema.json`.

## Local / Actions
```bash
python market_intelligence.py
pytest -q tests/test_market_intelligence.py
```

The daily workflow runs this after the P01-010 pipeline and commits the generated feed with the other production artifacts.
