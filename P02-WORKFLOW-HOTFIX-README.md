# P02-002 / P02-003 Workflow Hotfix

Replace only these two existing workflow files:

- `.github/workflows/p02_polymarket.yml`
- `.github/workflows/p02_kalshi.yml`

## Fix

The original workflow checked `git diff` before staging generated JSON. Brand-new untracked files are not included in that check, so the workflow could incorrectly print `No generated data changes to commit`.

The hotfix now does:

```bash
git add -f data/p02/<generated-file>.json
git diff --cached --quiet
```

This makes new generated JSON files visible to Git before deciding whether a commit is required.

## Run order

1. Upload/replace both workflow files.
2. Run `P02 Polymarket Data Update`.
3. Confirm `data/p02/polymarket_markets.json` exists on `main`.
4. Run `P02 Kalshi Data Update`.
5. Confirm `data/p02/kalshi_markets.json` exists on `main`.
6. Re-run `P02 Batch A Intelligence`.

Do not modify P01 or the Batch A Python code.
