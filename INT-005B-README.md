# INT-005B — Tokenization Mapping + Product Language Cleanup

## Scope
1. Adds an evidence-ready Traditional ↔ Tokenized Asset Mapping section.
2. Removes P01/P02/INT implementation codes from user-facing copy where they are not needed.
3. Keeps internal payload/schema keys unchanged to avoid breaking the pipeline.

## Evidence rule
- `NOT_VERIFIED`: no verified mapping source is bundled in this release.
- `RESEARCH_QUEUE`: a thematic mapping candidate worth verifying next.
- `NOT_APPLICABLE`: native crypto asset; not a traditional-asset tokenization mapping.
- Do not upgrade any item to `VERIFIED` without provider/venue/chain/rights/source/last_verified evidence.

## Upload these files
- `intelligence/index.html` — replace
- `data/integration/tokenization_mapping.json` — add
- `INT-005B-README.md` — add

## Acceptance
- Badge shows `INT-005B · TOKENIZATION`.
- Tokenization Mapping renders after Multi-Asset Watchlist.
- No user-facing P01/P02 labels remain in the Executive/Relationship cards/buttons/system labels.
- Existing P01/P02 internal data keys remain untouched.
