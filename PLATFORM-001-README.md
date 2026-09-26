# PLATFORM-001 v2 — Unified Platform Home & Navigation

## Goal
Create one product-level landing page while preserving P01, P02, and INT-003 as independent modules.

## Routes
- `/` — Unified Platform Home
- `/p01/` — P01 UNDERSTAND
- `/p02/` — P02 PREDICT / COMPARE
- `/intelligence/` — INT-003 CONTEXTUALIZE
- P03 — Coming Soon, execution disabled

## Visual revision
This v2 intentionally reduces heavy typography. Primary headings, module titles, metrics, and navigation use restrained 500–600 weights where practical. The warm-white product family and restrained indigo accent are retained.

## Important implementation detail
P01 is moved from the repository root to `/p01/`. Its live/generated JSON remains at repository root, and the P01 fetch paths are updated to `../...` so the existing data pipeline does not need to duplicate output.

## Acceptance
Run `PLATFORM-001 Unified Home & Navigation` in GitHub Actions.
