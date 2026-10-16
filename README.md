# Claire’s Web3 Intelligence — Cross-Market Research

跨市場情報研究工作台：整合宏觀、預測市場與代幣化資產，回查來源、時間與證據限制。

Evidence-first research across macro conditions, prediction markets and tokenized assets.

- Public project: https://clairelee1010.github.io/macro-attribution-dashboard/
- Main reading flow: `daily/`
- Frozen research case and methodology: `research/`
- Release / acceptance / deployment: [RELEASE-2026-10-16.md](RELEASE-2026-10-16.md)

## Current scope / 目前範圍

| Module | Implemented behavior | Boundary |
|---|---|---|
| P01 | Public market observations, deterministic signals, regime, risk, attribution and evidence confidence | Rules describe evidence alignment, not causality or validated forecast accuracy |
| P02 | Polymarket / Kalshi data, topic discovery, ranking, event matching and historical artifacts | Zero matches is valid; title similarity alone does not prove identical contracts |
| P03 | Public read-only tokenized-equity and activity-zone research | Context links are not observed net fund flows; missing evidence stays missing |
| Daily | EN / 繁中 controls, followed assets, tracking, rule briefs, cited Gemini questions, visible source health | Local browser storage; no member accounts or cross-device sync |
| Research | Dated October 2026 FOMC case with five copied contract observations, frozen input evidence and SHA-256 provenance | Not live odds; no independently verified cross-venue counterpart or settlement-rule equivalence |

This is a research MVP / portfolio project, not a fully accepted production trading platform.

這是研究 MVP 與作品集。不能把「程式存在」「附件驗收通過」或「已填服務網址」當成完整正式上線驗收。

## Rules, Gemini and prototypes / 哪些結果來自哪裡

**Deterministic rules:** Python normalization, freshness, P01 signals / regime / risk / attribution, P02 ranking and matching, P03 heat, and Daily quick briefs. Their output does not require a Gemini call. Risk scores and evidence confidence are different concepts.

**Gemini:** Only Daily’s submitted free-form Robi question calls the separate Worker. The Worker reads fixed public project JSON, limits evidence size, requests structured output and validates citation IDs. It does not verify that every sentence is entailed by its cited source. Missing sources and stale observation times must remain visible. No Gemini text is stored in the frozen research case.

**Roadmap / unimplemented:** Wallet authorization, signing, Account Abstraction, x402 payments, spending policies and trade execution. Current P03 is read-only research, rather than a completed autonomous wallet. P03’s built-in keyword responses are rule-based, not a general Gemini agent.

**Prototype visuals:** City animation is decorative; inferred relationships and heat are not observed capital flow or trading recommendations.

## Data quality policy / 資料品質

- Main Daily and P01/P02/P03/INT pages expose source health.
- File generation time, observation time and retrieval time have different meanings.
- The new quality panel recalculates age against the current clock. Missing / future timestamps and observations older than 36 hours are flagged. This is a UI review threshold, not a claim about provider freshness standards. Traditional-market holidays are not silently treated as fresh.
- The denominator for core P01 completeness is five: US10Y, DXY, VIX, BTC, ETH. Missing metrics cannot inflate coverage.
- Fallback prices retain primary failure information. News error records are shown separately from successfully collected items.
- Contract probability is a venue observation, not the product’s forecast. Different topic-discovery and raw-feed coverage must not be treated as equivalent datasets.
- Missing or failed evidence does not become zero price, zero risk or a successful comparison.

## Frozen research case / 完整研究案例

`research/case-study.json` preserves the supplied snapshot, with archived source files in `research/evidence/`. It includes:

1. Federal Reserve official meeting calendar: October 27–28, 2026; calendar checked October 16, 2026.
2. P01 observations and deterministic regime context, with their original timestamps.
3. Five supplied Polymarket contracts about that October meeting, including YES probabilities, source URLs and retrieval times.
4. Withheld cross-venue comparison: no verified counterpart in the snapshot; topic rows lack full resolution terms; raw feeds and topic discovery differ in coverage.
5. Uncertainty, subsequent verification steps and exact archived input hashes.

Values are copied from the supplied repository artifacts, **not independently certified exchange data**. Retrieval timestamps are not necessarily exchange quote timestamps. Opening the case later does not relabel historical probabilities as current. The official calendar verifies the meeting dates only, not quotes or settlement rules.

To deliberately publish a new frozen case, review the source inputs and run `python scripts/build_research_case.py`. Do not add this command to recurring market-data updates: that would silently rewrite an archival case.

## Architecture

External public sources → scheduled Python fetch / normalization → JSON artifacts → rule-based research → source-aware pages.

Daily free-form question → separate Cloudflare Worker → fixed public evidence → Gemini → citation validation → cited answer or explicit error.

A failed news source does not automatically block all other usable question evidence. Failed model output is withheld; it is never replaced with an invented AI answer.

## Robi deployment and current verification

The frontend endpoint remains `https://claire-market-robi.claire-web3.workers.dev` in `daily/ai-config.js`; it contains no API key.

This update adds:

- Read-only `GET /health`, which reports configuration status and explicitly sets `provider_verified: false`.
- Distinct error codes for entry blocks, origin denial, application daily limits, Gemini limits / authentication / model failures, timeouts, missing evidence, invalid output and invalid citations.
- User cancellation, EN / 中文 question language, structured model output, source-level partial failure and safe text rendering.
- P02 topic observations and P01 regime evidence in the question context, alongside market observations and news.

**Observed on October 16:** live OPTIONS and POST requests from this test environment received HTTP 403 with Cloudflare error 1010, without the Worker’s JSON / CORS response. This establishes an entry-layer block for this connection; it does not prove that every user browser is blocked or identify the exact account rule. Cloudflare account logs and a browser Network response are needed for that determination. This update cannot modify account-level security settings.

The new Worker still needs deployment by the account owner, followed by a real cited model response. A configured endpoint or passing mock test is not real model acceptance. See the release guide.

The application cap remains 50 requests globally per UTC day and 5 per IP per UTC day; failed and cancelled requests already sent may count. These are application limits, not Gemini’s provider quota. Origin filtering is not authentication. Only public market questions should be submitted.

## Run checks

```bash
python -m pip install -r requirements.txt
python -m pytest -q tests/research/test_fred_dates.py tests/test_adapters.py
npm ci
npm run test:research
```

Browser layout / interactions, on a machine supporting Chromium:

```bash
npx playwright install --with-deps chromium
npm run test:browser
```

`research_acceptance.yml` runs the new regression suite and Chromium acceptance at 320, 375, 768 and 1280px. The browser test mocks the AI backend: it validates UI behavior, not the real Gemini service. It does not submit credentials or place trades.

The pre-existing Python suite had 21 failures before these edits (mostly earlier homepage / navigation / text contracts). This release does not claim that entire legacy suite passes. See `qa/` and the release acceptance notes.

## Authorship / 作者與 AI 協作

Claire Lee is the project owner. Requirements and priorities for this update are recorded in the project conversation. Implementation, research framing, documentation and test development include AI assistance. This repository does **not** claim all code was independently hand-written.

Personal claims about independently designed modules, manual source review, deployment and acceptance should be supported by the author’s records. Automated checks performed for this update and checks still pending are listed in the release report. No invented performance, user adoption, investment returns or manual-validation claims are used.

## Limitations

Public provider availability, delayed snapshots, source errors and incomplete contracts can constrain conclusions. Translation covers interface controls and available bilingual fields; original source titles, raw evidence, saved historical source text and an existing model answer retain their original language. Asking again requests a model answer in the selected language.

There is no portfolio-account connection, trading execution, signing, fund custody or push subscription. Tracked price changes are observations, not verified investment performance.

Author: Claire Lee · https://medium.com/@claireli_79034
