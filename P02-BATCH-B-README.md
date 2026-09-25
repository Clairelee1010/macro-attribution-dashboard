# P02 Batch B — P02-007 + P02-008

Adds the first independent P02 GitHub Pages dashboard.

## P02-007 — Trust & Security Intelligence
- Deterministic aggregation of normalized security events.
- Empty security feed returns `UNKNOWN`, never `NORMAL`.
- `UNKNOWN` explicitly does not mean safe.
- No security incident is invented.
- Execution remains disabled.

At this milestone `data/p02/security_events.json` is optional. When no real security-event feed is configured, the dashboard honestly shows `UNKNOWN`.

## P02-008 — Dashboard
- Generates `data/p02/dashboard_payload.json`.
- Publishes `p02/index.html`.
- Bilingual EN / 中文.
- Prediction Markets and Trust & Security tabs.
- Reads the completed Batch A outputs.
- Handles zero matched events without fabricating matches.

## Upload these files
```text
p02/trust_security.py
p02/build_dashboard_payload.py
p02-web/index.html
tests/p02/test_batch_b.py
.github/workflows/p02_batch_b.yml
P02-BATCH-B-README.md
```

The Action will generate and commit:
```text
data/p02/dashboard_payload.json
p02/index.html
```

## Run
Actions → P02 Batch B Dashboard → Run workflow

## Expected
```text
P02 BATCH B
P02-007 Trust & Security     PASS
Trust Status                 UNKNOWN   # expected until a real feed exists
P02-008 Dashboard Payload    PASS
Execution                    DISABLED
P02 BATCH B: PASS
```

After GitHub Pages redeploys, the page path is:
`/macro-attribution-dashboard/p02/`

## Important
This is the Prediction Market MVP dashboard. Tokenized Markets and Yield Intelligence remain controlled P02 extensions and are not silently added to this milestone.
