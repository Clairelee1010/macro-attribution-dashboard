# P03-003A · Dynamic Market Hot Zones

## Product intent
Visual-first investigation layer for P03. It ranks **market attention / activity heat**, not investment attractiveness.

## Semantics
- Heat Score ≠ investment recommendation.
- Attention / momentum ≠ capital flow.
- Only direct net-flow evidence may be labeled `OBSERVED_FLOW`.
- Contextual relationships remain `CONTEXT_LINK` / inferred.
- Missing direct RWA flow evidence remains `EVIDENCE_PENDING`.
- Political prediction-market contracts are excluded from Hot Zone scoring.
- Execution remains disabled.

## UI
- Animated bubble Hot Zone map.
- 24H / 7D / 30D switching.
- Click a bubble to inspect evidence and route context to Robi.
- Capital Flow Radar clearly distinguishes context/inferred links from observed flows.
- API Health and Agent Trace are preserved under collapsed System Evidence.

## Data
`p03_hot_zone.py` consumes existing generated artifacts and writes:
`p03/data/hot_zone_intelligence.json`.

No P02 UI/template files are modified by P03-003A.
