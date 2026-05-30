## STATE — 30/05/2026 20:10
Project: ASSET-FORGE
Phase last completed: 9 - Build flagships ✅ COMPLETE — **TWO** hospitality flagships built in `products/` (Samuel asked for A=P2 in addition to P1). P1 Café/Restaurant Compliance Pack (8 sheets) + P2 Hospitality Operations & GP Bundle (7 sheets), each bilingual EN/SK with watermarked DEMO + README.
Checkpoint score: 2 flagship products shipped (P1 7 assets/8 sheets · P2 6 assets/7 sheets) + 2 demos + 2 READMEs | ~78% complete (10 of 13 sessions). ▶️ NEXT = Phase 10 (B, bonus research) — Samuel asked to run A then B.

### 🔧 OWNER NOTE RESOLVED (manual-handling / training)
- Samuel flagged: nobody on the floor without manual-handling + induction training, and an inspector wants *proof*. P1's H&S sheet lists manual handling as a **hazard + control** but holds no training *record*. Fix: folded asset **10 (Staff Training & Induction Matrix)** into **P2 as sheet 06** (Induction · Manual handling · Food hygiene · Allergen · Fire · H&S/first-aid, dated + refresher-due). DB `products` P2 `bundled_asset_ids` updated 8,7,6,9,11 → **8,7,6,9,11,10**. P1 (risk) + P2 (training record) now cover both halves.

### ✅ DONE THIS SESSION
- Built **P1 — Café / Restaurant Compliance Pack** (deliverable #6 of the project DoD: `/products/` flagship proof-of-concept). Hospitality-first mandate satisfied — the first shippable product is a café/restaurant asset.
- Wrote `scripts/build_p1_compliance_pack.py` (re-runnable; needs `openpyxl` — `pip install openpyxl`, 3.1.5 used). Generates both the full product and the demo from one builder.
- Output `products/P1_Cafe_Restaurant_Compliance_Pack.xlsx` — **8 sheets**: 00 Start-Here/Návod · 01 HACCP FSMS (id 1) · 02 Allergen Matrix 14×menu (id 2) · 03 Temperature Log (id 3) · 04 Cleaning Schedule (id 4) · 05 Supplier/Delivery Traceability (id 5) · 06 H&S Risk Assessment & Safety Statement + accident log (id 16) · 07 Fire Safety Register + drill log (id 17).
- **All 7 = MUST across all 5 hospitality types** (Reg. 852/2004 + 1169/2011 + Fire Services Acts 1981/2003 + SHWWA 2005). Legal floor = the whole pack.
- **Real logic, not blank tables:** allergen Y/T conditional formatting + dropdowns; temperature auto Pass?/CHECK (direction-aware cold≤ / hot≥ target); cleaning COUNTA done/7; H&S risk = L×S with Low/Med/High bands; fire Status OVERDUE/DUE SOON/OK from next-due date; traceability reject-row flag + EU comma-thousands.
- **EU conventions:** metric (°C/kg/min), DD/MM/YYYY date cells, comma thousands. **Bilingual EN/SK** parallel headers + instructions on every sheet (sourced from `deliverables/asset_glossary_EN_SK.md`).
- Built `products/P1_DEMO_Cafe_Restaurant_Compliance_Pack.xlsx` — red "DEMO — not for resale" banner on every sheet + sheet protection (read-only preview for the listing per launch-checklist §4).
- Wrote `products/P1_README.md` — product sheet, sheet→asset→legal-basis map, built-in-logic list, **bilingual EN/SK listing copy draft**, and launch-checklist status. Price/platform carried from Phase 8: **€34 / Lemon Squeezy**.

### ▶️ NEXT SMALLEST ACTION
- **BRANCH:** this phase ran on **`claude/modest-cori-cZ7cI`** (carries Phases 0–9). Continue the next session from this branch (or the consolidated tip).
- Open a FRESH session and run **/goal 10 — 🎁 Standards & audit research** (BONUS track). Per brief §15: write `research/compliance.md`; add `standards` + `compliance_assets` tables (data-model additions §15.4); map ISO 9001/14001/45001/22000, HACCP/BRCGS/IFS/FSSC, EU legal floor (852/2004, 1169/2011), trades & hospitality schemes → business types → assets; **verify current standard versions live**. Mid tier. Legal-mandated standards auto-promote assets to MUST (Legal=3).
- *(Optional before P10–12: build a second flagship — P2 Hospitality Operations & GP Bundle — if Samuel wants two proofs in `/products/` before moving to the bonus track. Brief §9 allows 1–2 flagships; one is shipped.)*

### ➕ STANDING ADD-ONS (carry forward)
- **openpyxl required** for any .xlsx build/inspection — not vendored; `pip install openpyxl` in each fresh session. P1 builder + `export_catalogue.py` both need it.
- **Bilingual EN+SK** binding rule (AGENTS.md). P1 used `asset_glossary_EN_SK.md` directly. **34 food/non-food/trades assets (ids 21–54) still need SK names/microcopy** — backfill before listing P6–P12. Slovak in P1 listing copy still needs a **native-editor pass before public launch** (`/slovak` skill NOT installed here).
- **Platform LOCKED (Phase 8):** Lemon Squeezy primary / Gumroad fallback / Etsy discovery. Switch trigger: LS drops MoR VAT, fee >~8% effective, or payout breakage. Don't quote LS "5%" — effective ~6.5%+$0.50.
- **Prices LOCKED (Phase 8):** P1 €34. `products.platform` = "Lemon Squeezy" on all 12 rows. `existing_solutions` populated (8 rows).
- **Listing-time TODO for P1:** export preview screenshots (no headless renderer here — open in Excel/Sheets to capture), licence text + EU 14-day-withdrawal waiver checkbox (LS provides), re-verify fees live.
- **Research tooling:** Tavily MCP, Semantic Scholar, Consensus.
- **Script set:** init_db, classify, validate, export_catalogue, seed_* (hospitality/food/nonfood/trades/products/existing_solutions), **build_p1_compliance_pack** (new), set_secret.
- No `sqlite3` CLI — use Python `sqlite3` module for DB inspection.

### ❓ OPEN QUESTIONS / DECISIONS NEEDED FROM SAMUEL
- **One flagship or two before the bonus track?** P1 is shipped (hospitality-first mandate met). Brief §9 allows 1–2. Build P2 (Hospitality Operations & GP Bundle) next as a second proof, or proceed to Phase 10 bonus research? (Default if silent: proceed to Phase 10.)
- ✅ RESOLVED (Samuel, 30/05/2026): VAT — stay non-registered + rely on MoR (Lemon Squeezy is legal seller, handles per-sale EU VAT). Confirm specifics with accountant before launch.
- ✅ RESOLVED (Samuel, 30/05/2026): Excise/duty (alcohol) — KEEP FOLDED into Cashflow/P&L (P2/P4). No dedicated excise tracker.
- Confirm `asset-forge/` living inside the `NeuroHive` repo is intended. (Unchanged.)

### ⚠️ RISKS / WATCHOUTS
- **Slovak copy not yet native-edited** — do NOT publish P1 listing SK text before a native pass.
- **P1 preview images not generated** (no headless spreadsheet renderer in this env) — capture screenshots at listing time from Excel/Google Sheets.
- **Lemon Squeezy post-Stripe-acquisition uncertainty** — Gumroad fallback pre-vetted; both host the same files, migration = re-upload not rebuild.
- **Etsy = static files only** → if listed there, ship PDF + "make a copy" Sheets link, never raw editable .xlsx where the licence forbids redistribution.
- **EU digital-goods withdrawal right** — listings must include the immediate-delivery / 14-day-waiver checkbox (LS provides).
- **Re-verify all platform fees at listing time** — figures dated 30/05/2026.
- One phase per session; if a phase looks like >~15 tool calls, propose splitting.
- Legal-mandatory (Legal=3) auto-promotes to MUST — held since Phase 5 (115/115). Phases 7–9 did not alter tiers.
