## STATE — 29/05/2026 20:30
Project: ASSET-FORGE
Phase last completed: 1 - Hospitality research
Checkpoint score: 90 asset-map rows mapped this session (20 assets, 17 pain points) | ~15% complete (2 of 13 sessions)

### ✅ DONE THIS SESSION
- Wrote `research/hospitality.md` — 5 research questions answered for Bar/pub, Café, Restaurant, B&B/guesthouse, Hotel, with a regulatory MUST-floor section.
- Verified the legal floor LIVE (not from memory): FSAI HACCP + allergens (Reg 852/2004, Reg 1169/2011 / S.I. 489/2014→656/2024), HSA Safety Statement (S.19 Act 2005) + hospitality fire duty, Fáilte Ireland registration/Welcome Standard. Competitor gaps + price benchmarks via Capterra/Startups (EPOS) and Etsy/7shifts (templates).
- Wrote `scripts/seed_hospitality.py` (idempotent; computes score+tier; refuses MUST/SHOULD rows without evidence_url).
- Inserted into `intelligence.db`: 20 `digital_assets`, **90 `asset_map`** rows (raw axis scores + buyer tag + evidence_url), 17 `pain_points`.
- Tier split: 37 MUST · 31 SHOULD · 22 COULD. Buyer dimension captured (88 operator, 1 auditor, 1 consultant).
- `v_universal_core` now shows **7 hospitality assets MUST across all 5 business types** (HACCP, allergen matrix, temp log, cleaning schedule, traceability log, H&S safety statement, fire register) — the highest-leverage product candidates.
- All Phase 1 quality gates [12] passed: 0 MUST/SHOULD missing evidence; 0 legal=3 rows off-MUST; 0 score mismatches; 0 null tiers.

### ▶️ NEXT SMALLEST ACTION
- Open a FRESH session for **Phase 2 — Food manufacturing research** (mid model tier).
- Produce `research/manufacturing_food.md` answering the 5 questions in [7] for: Bakery, Butchery/meat, Dairy, Beverage, Ready meals/catering production (business_type ids 6–10).
- Mirror the Phase 1 pattern: write a `scripts/seed_manufacturing_food.py`, insert `digital_assets` + scored `asset_map` rows (+ buyer tag + evidence_url) + `pain_points`. Reuse existing universal-core assets where they apply (HACCP/temp/traceability) rather than duplicating.

### ❓ OPEN QUESTIONS / DECISIONS NEEDED FROM SAMUEL
- `scripts/classify.py` needs an OpenRouter API key + chosen free model name (Phase 5). Provide before Phase 5.
- Phase 1 scored rows INLINE (defensible per-row scores) rather than deferring all scoring to Phase 5. Confirm OK — Phase 5 can then become a spot-check/normalisation pass rather than a from-scratch scoring run.
- `guest register` legal weight set to 2 (expected) not 3 — clean statutory source for a mandatory guest register wasn't confirmed live; revisit in Phase 10 (compliance track) if needed.
- Confirm `asset-forge/` living inside the `NeuroHive` repo is intended.

### ⚠️ RISKS / WATCHOUTS
- Do NOT state platform fees / VAT / SaaS prices from memory — verify live (Phases 8/11).
- Dedupe assets by FUNCTION, not label — Phase 2+ should reuse the 20 existing assets where they recur, not re-create them.
- Legal-mandatory (Legal=3) auto-promotes to MUST — sanity-check each session (Phase 1: passed).
- One phase per session; if a phase looks like >~15 tool calls, propose splitting.
- `scripts/classify.py` and `scripts/export_catalogue.py` still NOT written (built in Phase 5 / Phase 6).
- No `sqlite3` CLI in this environment — use Python (`sqlite3` module) for DB inspection.
