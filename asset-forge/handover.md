## STATE — 29/05/2026 21:30
Project: ASSET-FORGE
Phase last completed: 2 - Food manufacturing research
Checkpoint score: 130 asset-map rows mapped this session (16 new assets, 17 pain points) | ~23% complete (3 of 13 sessions)

### ✅ DONE THIS SESSION
- Wrote `research/manufacturing_food.md` — 5 research questions answered for Bakery, Butchery/meat, Dairy, Beverage, Ready meals/catering (business_type ids 6–10), plus a regulatory MUST-floor table.
- Verified the food-manufacturing legal floor LIVE (not from memory): HACCP (Reg 852/2004); **Reg 853/2004 approval + health/identification mark for products of animal origin** (meat & dairy; retail-butcher marginal/local/restricted exemption); FIC labelling + **mandatory nutrition declaration** (Reg 1169/2011, since 13/12/2016; alcohol exempt from nutrition); allergens (1169/2011); traceability/recall (Reg 178/2002 Arts 18–19); **net-quantity / average-quantity 'e' mark** (Packaged Goods (Quantity Control) Act 1980 / Metrology Act 1996 / NSAI); HSA Safety Statement + fire. Sources: FSAI + NSAI (cited in research doc + DB `evidence_url`).
- Wrote `scripts/seed_manufacturing_food.py` (idempotent on bt 6–10; computes score+tier; refuses MUST/SHOULD rows without evidence_url; reuses existing hospitality assets by name without clobbering them).
- Inserted into `intelligence.db`: **16 new `digital_assets`** (total 36), **130 `asset_map`** rows for bt 6–10 (raw axis scores + buyer tag + evidence_url), 17 `pain_points` (total 34).
- Phase-2 tier split: **48 MUST · 62 SHOULD · 20 COULD**. Buyer dimension captured (126 operator, 2 auditor, 2 consultant).
- `v_universal_core` now spans hospitality+food: HACCP/Cleaning/Traceability/H&S/Fire = MUST across **all 10** business types; Allergen + Temp across 8; **new Product Label & Nutrition Generator** MUST across 5; Batch/Yield Record across 3.
- Deduped by FUNCTION: reused 10 existing assets (HACCP, Allergen, Temp, Cleaning, Traceability, Cashflow/P&L, Training, PPM, H&S, Fire) rather than re-creating them.
- All Phase 2 quality gates [12] passed: 0 MUST/SHOULD missing evidence; 0 legal=3 rows off-MUST; 0 score mismatches; 0 null tiers.

### ▶️ NEXT SMALLEST ACTION
- Open a FRESH session for **Phase 3 — Non-food manufacturing research** (mid model tier).
- Produce `research/manufacturing_nonfood.md` answering the 5 questions in [7] for: Metal/engineering, Plastics/injection, Packaging/print, Joinery/furniture, Light electronics (business_type ids 11–15).
- Mirror the Phase 1/2 pattern: write `scripts/seed_manufacturing_nonfood.py`, insert NEW `digital_assets` + scored `asset_map` rows (+ buyer tag + evidence_url) + `pain_points` for bt 11–15. Reuse existing assets where the function recurs (Batch/Yield Record, BOM/costing, Production Planning, Calibration, Supplier Approval, H&S, Fire, Maintenance/PPM, Cashflow, B2B invoice, OEE dashboard, Internal Audit). NOTE: non-food legal floor differs — expect ISO 9001/45001 (voluntary but commercial), CE marking / product-safety, machinery/PUWER, COSHH/chemicals rather than food law. Verify live.

### ➕ STANDING ADD-ONS (carry forward)
- **Bilingual EN+SK** binding rule (AGENTS.md). `deliverables/asset_glossary_EN_SK.md` currently covers the 20 hospitality assets — the 16 new food-mfg assets still need SK names/microcopy (do in synthesis/Phase 6 or before launch; route through native editor). `/slovak` chief-editor skill NOT installed here.
- **Market validation**: `research/market_validation.md`. Preliminary platform pick: **Lemon Squeezy** primary / **Gumroad** fallback / **Etsy** discovery (EU-VAT weighted; final lock Phase 8 with fees re-verified live).
- **Secrets plumbing** ready: root `.gitignore` excludes `.env`; `asset-forge/.env.example`; `scripts/set_secret.sh`. Preferred: set `OPENROUTER_API_KEY` as a Claude Code environment secret.

### ❓ OPEN QUESTIONS / DECISIONS NEEDED FROM SAMUEL
- `OPENROUTER_API_KEY` + free model name still needed before Phase 5 — provide via env secret or `scripts/set_secret.sh` (NOT in chat).
- **Excise/duty (alcoholic beverage)** was folded into Cashflow/P&L for Phase 2 to avoid scope creep. Confirm whether you want a dedicated excise/duty tracker asset (likely a Phase 8/10 product) or to keep it inside cashflow.
- Confirm `asset-forge/` living inside the `NeuroHive` repo is intended.
- [RESOLVED earlier] Inline per-row scoring OK → Phase 5 = spot-check/normalisation.
- [RESOLVED earlier] `guest register` legal=2 → revisit Phase 10 compliance track.

### ⚠️ RISKS / WATCHOUTS
- Do NOT state platform fees / VAT / SaaS prices from memory — verify live (Phases 8/11).
- Dedupe assets by FUNCTION, not label — Phase 3+ should reuse the 36 existing assets where they recur, not re-create them.
- Legal-mandatory (Legal=3) auto-promotes to MUST — sanity-check each session (Phases 1 & 2: passed).
- One phase per session; if a phase looks like >~15 tool calls, propose splitting.
- `scripts/classify.py` exists (Phase 5 runner) but `scripts/export_catalogue.py` still NOT written (built in Phase 6).
- No `sqlite3` CLI in this environment — use Python (`sqlite3` module) for DB inspection.
- 16 new food-mfg assets are EN-only so far — Slovak glossary backfill outstanding (see add-ons).
</content>
