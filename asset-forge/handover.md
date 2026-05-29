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

### ➕ POST-PHASE-1 ADD-ONS (per Samuel's directives)
- **Bilingual EN+SK** is now a binding rule (AGENTS.md). `deliverables/asset_glossary_EN_SK.md` holds native-quality SK names + microcopy for all 20 hospitality assets. NOTE: `/slovak` chief-editor skill is NOT installed here — SK authored directly; route through native editor before launch.
- **Market validation** done: `research/market_validation.md` — evidence these assets sell ($280k Etsy spreadsheet case; 1,000+ restaurant + 5,000+ general templates on Etsy) + channel landscape + most-pros-wins platform benchmark. Preliminary winner: **Lemon Squeezy** primary / **Gumroad** fallback / **Etsy** discovery (EU-VAT weighted; final lock Phase 8).
- **Secrets plumbing** ready: root `.gitignore` (excludes `.env`), `asset-forge/.env.example`, `scripts/set_secret.sh` (hidden input → git-ignored `.env`). Preferred: set `OPENROUTER_API_KEY` as a Claude Code environment secret.

### ❓ OPEN QUESTIONS / DECISIONS NEEDED FROM SAMUEL
- `OPENROUTER_API_KEY` + free model name still needed before Phase 5 — provide via env secret or `scripts/set_secret.sh` (NOT in chat).
- [RESOLVED] Inline per-row scoring OK → Phase 5 becomes spot-check/normalisation. (Samuel: "use your best judgment".)
- [RESOLVED] `guest register` legal=2 → revisit in Phase 10 compliance track. (Samuel: "ok as soon as you revisit in phase 10".)
- Confirm `asset-forge/` living inside the `NeuroHive` repo is intended.

### ⚠️ RISKS / WATCHOUTS
- Do NOT state platform fees / VAT / SaaS prices from memory — verify live (Phases 8/11).
- Dedupe assets by FUNCTION, not label — Phase 2+ should reuse the 20 existing assets where they recur, not re-create them.
- Legal-mandatory (Legal=3) auto-promotes to MUST — sanity-check each session (Phase 1: passed).
- One phase per session; if a phase looks like >~15 tool calls, propose splitting.
- `scripts/classify.py` and `scripts/export_catalogue.py` still NOT written (built in Phase 5 / Phase 6).
- No `sqlite3` CLI in this environment — use Python (`sqlite3` module) for DB inspection.
