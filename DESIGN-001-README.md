# DESIGN-001 — P01 Visual System Alignment

## Goal
Use P01 as the visual master and soften Home, P02, INT-003, and the P03 preview without changing product/data logic.

## Design rules
- P01 remains the reference and is not modified by this package.
- Warm background `#fcfbf9`, soft border `#f0eae1`, low-shadow white cards.
- Body 400, navigation 400/500, titles and key metrics 500.
- Avoid heavy 700–900 emphasis in the new alignment layer.
- P03 keeps the same light intelligence-product language; no neon/dark Web3 treatment.

## Files
- `index.html` — Home + P03 preview alignment
- `p02/index.html` — P02 visual alignment
- `intelligence/index.html` — INT-003 visual alignment
- `tests/design/test_design001.py`
- `.github/workflows/design001_visual_alignment.yml`

## Non-goals
No changes to P01/P02 engines, prediction ranking, political guardrails, INT-002 context logic, data sources, or execution state.
