## STATE — 29/05/2026 00:00
Project: ASSET-FORGE
Phase last completed: 0 - Setup
Checkpoint score: 0 assets mapped this session | ~8% complete (1 of 13 sessions)

### ✅ DONE THIS SESSION
- Created folder tree per brief [4]: `research/`, `scripts/`, `deliverables/`, `products/`.
- Wrote `scripts/init_db.py` (schema [8] + idempotent; supports `--reset`).
- Initialised `intelligence.db`: 9 tables, 2 views (`v_must_haves`, `v_universal_core`), integrity check OK.
- Locked in taxonomy [5] as seeded reference data: 4 verticals, 21 business types, 10 departments.
- Locked in rubric [6] (axes, weighted score /24, MUST/SHOULD/COULD/WON'T) via `asset_map` raw-score columns + `tier`.
- Wrote `AGENTS.md` (condensed brief [1]–[3] + [6]).
- Added `asset_map.buyer` column (operator/auditor/consultant) to honour the [5] BUYER dimension.

### ▶️ NEXT SMALLEST ACTION
- Open a FRESH session for **Phase 1 — Hospitality research** (mid model tier).
- Produce `research/hospitality.md` answering the 5 questions in [7] for: Bar/pub, Café/coffee shop, Restaurant, B&B/guesthouse, Hotel.
- Insert `digital_assets` + `asset_map` rows (with raw axis scores + buyer tag + `evidence_url`) and `pain_points` for those 5 business types.
- Leave the bulk tier-scoring finalisation to Phase 5 (`classify.py`); Phase 1 captures rows + evidence.

### ❓ OPEN QUESTIONS / DECISIONS NEEDED FROM SAMUEL
- `scripts/classify.py` needs an OpenRouter API key + chosen free model name (used in Phase 5). Provide before Phase 5.
- Confirm `asset-forge/` living inside the `NeuroHive` repo is intended (that's where it was created).
- Phase 5 scoring stays raw-rows-now / score-later — confirm OK, or score inline during research instead.

### ⚠️ RISKS / WATCHOUTS
- Do NOT state platform fees / VAT / SaaS prices from memory — verify live (Phases 8/11).
- Dedupe assets by function, not label, to avoid catalogue bloat.
- Legal-mandatory (Legal=3) auto-promotes to MUST — sanity-check each session.
- One phase per session; if a phase looks like >~15 tool calls, propose splitting.
- `scripts/classify.py` and `scripts/export_catalogue.py` are referenced in [4] but NOT yet written (built in Phase 5 / Phase 6).
