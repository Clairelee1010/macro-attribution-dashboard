# INT-005C · Tokenization Comparison Intelligence

## Scope
- Adds a comparison layer after Traditional ↔ Tokenized Asset Mapping.
- Compares a traditional-market baseline with verified tokenized mappings for the selected asset.
- Surfaces Structure, Backing, Chain, Rights, Evidence, and Last Verified when present in the mapping artifact.
- Does not rank providers, recommend products, or imply identical legal rights.
- Cleans product-facing `P01 evidence` wording in relationship explanations at render time.

## Files
- `intelligence/index.html` — overwrite current file.

## Guardrails
- Evidence-first: only VERIFIED mapping records are eligible for tokenized comparison cards.
- Missing rights information remains explicit and must be verified against issuer terms.
- Comparison is descriptive, not an investment recommendation.
- Execution remains disabled.

## Commit
`INT-005C: add tokenization comparison intelligence and product-language cleanup`
