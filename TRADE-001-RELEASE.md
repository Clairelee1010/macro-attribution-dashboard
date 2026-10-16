# TRADE-001 · Integrated Product Lab release · 2026-10-17

## What is included

Merged the supplied `(45)(1).zip` repository with `Web3_Fieldwork_Product_Patch_2026-10-16(1).zip`, then added:

- `/product-lab/`: bilingual product case, scope, design decisions, validation plan, contribution disclosure, resume notes and links to executable prototypes.
- `/trade-clarity/`: fixture-based BTC/USD spot-order simulator with buy/sell, Market/Limit, BTC quantity / reference USD inputs, preview and explicit confirmation.
- Execution across book levels, weighted average, quote-relative deviation, explicit demo fees, partial fills, resting limits, reserved funds and cancellation.
- Scripted normal / lower / higher / thin scenarios. A market remainder is cancelled; limit remainder stays open. Changing scenarios replenishes external fixture liquidity and checks the working order.
- Integer accounting, cumulative rounding, stale-preview invalidation and single-use confirmation.
- Home and learning navigation links; expanded automated and CI browser acceptance coverage.

The previous learning world, evidence desk, journal and policy sandbox remain included. No generated market JSON or API key is changed by this release.

## Correctness checks

47 Node/jsdom tests pass: 29 existing product/learning tests plus 12 matching-engine tests and 6 Product Lab/UI tests. See `docs/TRADE-001-TEST-RESULTS.txt`.

Validated: source failure handling, bilingual drafts, learning progress events, driving paths and collision, policy budgets and approval, plus buy/sell cash flows, fee rounding, limits, reservations, partial execution, cancellation, repeated confirmation, stale previews, explicit review and reset isolation.

Browser and mobile visual QA have not run in the delivery environment. The supplied GitHub Actions workflow runs Playwright at 320 / 375 / 768 / 1280 widths, including Trade Clarity and learning flows. This script is supplied for execution, not claimed as passed. No local preview or browser was launched.

Old UI-specific workflows and Python/research DOM tests may still assert retired pages. They are retained and are not a claim of a passing full-repository suite. Run **Web3 Fieldwork acceptance** for the new product.

## Deployment options

**Full source ZIP:** extract it and use the contents of `macro-attribution-dashboard-main/` as the repository contents. Keep `.github/` when uploading. Do not upload the ZIP itself as the website. This includes repository data snapshots supplied by you; use the patch option if newer data may already exist on GitHub.

**Patch ZIP:** copy everything *inside* `repository-files/` to the matching repository paths. The patch includes both PRODUCT-001 and TRADE-001, so you do not need to apply the previous patch first. No deletions are required. Generated data snapshots are excluded.

Commit, wait for GitHub Pages deployment, refresh without cache, and run **Actions → Web3 Fieldwork acceptance → Run workflow**. The delivery does not deploy to your GitHub account or execute Actions.

## Manual acceptance

1. Home → Product Lab → Trade Clarity. Switch EN / 中文; verify labels, preview and composed values remain coherent.
2. Preview default 0.005 BTC market buy. It must not spend until confirmation. Expected fills: 0.003 × $60,000 and 0.002 × $60,060; notional $300.12, fee $0.31, total $300.43, remaining USD $699.57.
3. Load limit scenario (resets round). Buy 0.005 at $59,900: Open, reserve $299.80. Apply lower-price scenario: fills at better prices, total cost $299.42, remaining USD $700.58, reserve released.
4. Load thin-liquidity scenario (resets round). Market 0.005: 0.003 fills, 0.002 cancels; total cost $180.37, remaining USD $819.63. No funds remain reserved.
5. For partial limit: normal scenario, limit $60,000 / quantity 0.005. Only 0.003 fills initially. Cancel remainder; filled BTC stays and unused reserves release.
6. Switch to Sell and inspect BTC availability. Try more BTC than available: it must reject. For insufficient USD, use a limit commitment greater than the balance; a large market order may instead partially fill the finite book and cancel its remainder.
7. Change amount or scenario after preview: require a new preview. Double confirmation cannot execute twice.
8. Revisit learning world, policy sandbox and evidence journal. Trade resets must not clear their stored progress or notes.

## Portfolio limitations

No wallet, exchange connection, live prices, trading recommendations or generative AI calls. Explanations are rule templates. Fixtures, balances and 0.10% fees are fictional. No customer research, adoption metrics, performance or uplift is claimed. The previous Word/PDF study is not included in this upload and has not been silently altered or represented as the prototype’s research evidence.
