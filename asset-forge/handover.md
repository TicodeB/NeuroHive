## STATE — 30/05/2026 20:45
Project: ASSET-FORGE
Phase last completed: 10 - 🎁 Standards & audit research ✅ COMPLETE (B). Did A+B this session at Samuel's request. A = built 2nd flagship P2; B = compliance/audit research → `research/compliance.md` + DB extension (`standards` 21, `compliance_assets` 19, `v_audit_packs` view 115 rows, `products` extended with audience+standard_ids). All 21 standard versions VERIFIED LIVE via Tavily.
Checkpoint score: A) 2 flagships shipped (P1 8 sheets · P2 7 sheets) + B) 21 standards + 19 compliance assets mapped, live-verified | ~85% complete (11 of 13 sessions). ▶️ NEXT = Phase 11 — Audit & compliance productisation.

### 🔎 PHASE 10 (B) — KEY LIVE FINDINGS (versions move — verified 30/05/2026 Tavily)
- **FSSC 22000 → V7** published **May 2026** (v6 valid to 30/04/2027, upgrade by Apr 2028) — was v6 in my memory. Timely "v7 transition pack" upsell.
- **BRCGS Food Safety → Issue 9** still current; **Issue 10 in development** (TWG Apr 2026).
- **IFS Food → Version 8** (Doctrine v5, Apr 2026).
- **ISO 9001:2015 + Amd 1:2024** (climate); same climate amendment on 14001/45001/22000/27001; **ISO 9001:2026 at FDIS** (coming).
- TÜV (SÜD/Rheinland/NORD) = certification *body*, NOT a standard → list packs as "audit-ready for a TÜV-style certifier auditing you to ISO/BRCGS", never "TÜV templates" (brief §15 framing rule honoured).
- **Two-buyer leverage** captured: 11 operator assets + 8 auditor/consultant assets; several reuse existing catalogue ids (1,5,10,28,30) → build once, sell twice. Flagship for Phase 12 = Gap-Analysis Tool + Mock-Audit Self-Assessment.

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
- **BRANCH:** Phases 0–10 now run on **`claude/modest-cori-cZ7cI`** (PR #9). Continue from this branch.
- Open a FRESH session and run **/goal 11 — 🎁 Audit & compliance productisation** (BONUS). Per brief §15.5: add auditor toolkits + auditee compliance packs to `PRODUCT_ROADMAP.md`. Use `v_audit_packs` for per-standard bundle definitions ("HACCP Readiness Pack for Cafés", "ISO 22000 Internal Audit Kit", "BRCGS Document-Control Suite", "FSSC 22000 v7 Transition Pack", "Auditor Edition"). Tier: free gap-analysis-lite (lead magnet) → paid standard kit (€49–€99) → full audit suite (auditor edition, €149+). Add new product rows (audience auditor/consultant + standard_ids). Planning tier.
- Then **Phase 12 — Build a flagship compliance pack**: the **Gap-Analysis Tool + Mock-Audit / Readiness Self-Assessment** (compliance_assets ids 1 + 2) — cheapest to build, clearest pain-killer, seeds every per-standard bundle. Code tier (openpyxl).

### ➕ STANDING ADD-ONS (carry forward)
- **openpyxl required** for any .xlsx build/inspection — not vendored; `pip install openpyxl` in each fresh session. P1 builder + `export_catalogue.py` both need it.
- **Bilingual EN+SK** binding rule (AGENTS.md). P1 used `asset_glossary_EN_SK.md` directly. **34 food/non-food/trades assets (ids 21–54) still need SK names/microcopy** — backfill before listing P6–P12. Slovak in P1 listing copy still needs a **native-editor pass before public launch** (`/slovak` skill NOT installed here).
- **Platform LOCKED (Phase 8):** Lemon Squeezy primary / Gumroad fallback / Etsy discovery. Switch trigger: LS drops MoR VAT, fee >~8% effective, or payout breakage. Don't quote LS "5%" — effective ~6.5%+$0.50.
- **Prices LOCKED (Phase 8):** P1 €34. `products.platform` = "Lemon Squeezy" on all 12 rows. `existing_solutions` populated (8 rows).
- **Listing-time TODO for P1:** export preview screenshots (no headless renderer here — open in Excel/Sheets to capture), licence text + EU 14-day-withdrawal waiver checkbox (LS provides), re-verify fees live.
- **Research tooling:** Tavily MCP, Semantic Scholar, Consensus.
- **Script set:** init_db, classify, validate, export_catalogue, seed_* (hospitality/food/nonfood/trades/products/existing_solutions/**compliance** new), **build_p1_compliance_pack**, **build_p2_operations_bundle** (new), set_secret.
- **DB now has:** `standards` (21), `compliance_assets` (19), view `v_audit_packs` (115 rows), `products` extended (audience + standard_ids). Re-seed: `python3 scripts/seed_compliance.py`.
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
