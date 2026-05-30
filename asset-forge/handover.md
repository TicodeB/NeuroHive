## STATE — 30/05/2026 19:05
Project: ASSET-FORGE
Phase last completed: 11 — 🎁 Audit & compliance productisation (BONUS) ✅ COMPLETE
Checkpoint score: 8 new compliance products mapped (P13–P20: 1 free lead magnet · 5 operator standard kits · 2 auditor/consultant pro suites) | ~90% complete (12 of 13 sessions). ▶️ NEXT = Phase 12 — Build a flagship compliance pack (P13 Gap-Analysis + Mock-Audit).

### ✅ DONE THIS SESSION (Phase 11 productisation + Funnel/Monetization extension)

**Sales funnel & conversion architecture (Samuel-requested, planning tier):**
- Samuel's frame: *"only starting up; digital products to the right audience = passive income."* → automation-first, free-tier-only, niche-targeted.
- Added **MONETIZATION_BRIEF.md §7** — the value-ladder (Rung 0 free teaser → Rung 1 à-la-carte module → Rung 2 pack → Rung 3 everything-kit), the conversion stack that **legally replaces Samuel's "exit timer" idea** (order bump · post-purchase one-time upsell · abandoned-cart recovery code · 3–5 email nurture), the marketing playbook, EU **Omnibus** legal guardrails (no fake/resetting timers — Amazon fined €7.48M; real sum-of-parts savings only; GDPR consent), and the lead-magnet decision.
- **Lead-magnet decision (Samuel): no-code interactive quiz NOW (Tally/Typeform, free, GDPR-ready) delivering the existing "Lite" file; dedicated web app DEFERRED** until traffic/conversion is proven (needs a hosted front-end — none in repo — + GDPR setup). "Module" = both levels (sheets buyable AND packs buyable inside kits).
- **DB:** added `products.pricing_tier` (free/module/pack/kit) + `products.parent_product` (rolls-up-into). Backfilled all base + audit rows; added **4 representative à-la-carte compliance modules** (Rung 1) to prove the structure — rest of catalogue is a documented roll-out, not hand-authored. **Now 24 products** (1 free · 8 module · 13 pack · 2 kit). Verified: no NULL tiers, no dup names, no dangling CA refs, **every child priced below its parent (Omnibus-safe)**, base enrichment intact.
- **Deferred (documented, NOT built):** custom lead-magnet web app + funnel page (interactive assessment, exit-intent, on-page timer) — future phase, gated on proven volume + GDPR + hosting.

### ✅ DONE THIS SESSION (Phase 11 — planning tier)
- Extended `deliverables/PRODUCT_ROADMAP.md` with **PART B — Audit & Compliance Productisation** (§4–§8): the tiered offer, per-standard bundle definitions from `v_audit_packs`, 8 one-page build specs, bundle architecture, and the Phase-12 handoff.
- Added **8 new product rows (P13–P20)** to the `products` table via `scripts/seed_products.py` (now **20 products total**). Each carries `audience` (operator/auditor/consultant) + `standard_ids` (→ `standards` table). Re-seeded & verified.
- **Tier ladder (brief §15.5):** ① FREE gap-analysis-lite lead magnet (P13, €0) → ② operator standard kits €49–99 (P14 HACCP Café/Restaurant €49 · P15 ISO 22000/FSSC 22000 €99 · P16 BRCGS/IFS Doc-Control €89 · P17 ISO 9001 €79 · P18 FSSC 22000 V7 Transition €49) → ③ pro audit suite €149+ (P19 Auditor Edition €149 · P20 Consultant Multi-Client Console €149).
- **Two-sided demand captured:** same audit premise sells an operator readiness pack AND an auditor protocol — `compliance_assets.buyer_role` already carries both → incremental revenue, zero new research.
- **No new builds invented:** every compliance product bundles existing `compliance_assets` by ID. Their `bundled_asset_ids` carry a **`CA:` prefix** to disambiguate from `digital_assets` IDs (Phase-7 rows).
- **Pricing grounded live (Tavily, 30/05/2026):** single templates €10–60 (Etsy/Gumroad) vs consultant ISO toolkits €300–800+ (Advisera) → our €49–99 kits + €149+ auditor editions sit in the defensible middle. Prices INDICATIVE — re-verify at listing.
- **Framing rule honoured (brief §15):** packs positioned "audit-ready for a TÜV-style certifier auditing you to ISO/BRCGS/IFS", NEVER "TÜV templates."

### ▶️ NEXT SMALLEST ACTION
- **BRANCH:** continue on **`claude/modest-hopper-CeONK`** (this branch already carries Phases 0–11; a PR is open for it). Run the next `/goal` on this branch.
- Open a FRESH session and run **/goal 12 — 🎁 Build a flagship compliance pack** (BONUS, final phase). Build **P13 — Gap-Analysis Tool + Mock-Audit / Readiness Self-Assessment** (`compliance_assets` ids 1 + 2). Cheapest to build, clearest pain-killer, the engine reused inside every paid standard kit (P14–P18). Code tier (openpyxl). Write `scripts/build_p13_gap_analysis_pack.py` (re-runnable, full + DEMO outputs) following the P1/P2 builder pattern. Real logic: clause-by-clause % conformance roll-up + prioritised action list + mock-audit Pass/Fail readiness score with RAG bands. Bilingual EN/SK headers + instructions (use `deliverables/asset_glossary_EN_SK.md`; backfill SK terms where missing). EU formatting (DD/MM/YYYY, metric, comma thousands). Write `products/P13_README.md` (product sheet + listing copy + launch-checklist status). Price = €0 free lead magnet (Lemon Squeezy email capture) → upsell to P14–P18.

### ➕ STANDING ADD-ONS (carry forward)
- **openpyxl required** for any .xlsx build/inspection — not vendored; `pip install openpyxl` in each fresh session (3.1.5 used). P1/P2 builders + `export_catalogue.py` need it. **Phase 12 P13 builder will need it.**
- **Bilingual EN+SK** binding rule (AGENTS.md). **34 food/non-food/trades assets (ids 21–54) still need SK names/microcopy**; compliance_assets (19) also need an SK pass — backfill before listing P6–P20. Slovak in all listing copy needs a **native-editor pass before public launch** (`/slovak` skill NOT installed here).
- **Platform LOCKED (Phase 8):** Lemon Squeezy primary / Gumroad fallback / Etsy discovery. Don't quote LS "5%" — effective ~6.5%+$0.50. All 20 `products.platform` = "Lemon Squeezy".
- **Prices LOCKED/INDICATIVE:** P1 €34, P2 €49 (locked). P13–P20 indicative (see roadmap §4) — re-verify live at listing.
- **DB now has:** `standards` (21), `compliance_assets` (19), view `v_audit_packs` (115 rows), `products` (**24 rows** — 12 base + 8 audit P13–P20 + 4 à-la-carte compliance modules; columns `audience`, `standard_ids`, `pricing_tier`, `parent_product` populated). **Re-seed ORDER MATTERS:** `python3 scripts/seed_products.py` (12 base — wipes `products`, adds pricing_tier/parent_product cols + base ladder) **THEN** `python3 scripts/seed_compliance.py` (re-enriches base + adds 8 audit rows + 4 module rows = 24). Audit products live in `seed_compliance.py` (`AUDIT_PRODUCTS`/`AUDIT_MODULES`/`AUDIT_LADDER`), base ladder in `seed_products.py` (`LADDER`).
- **Value-ladder columns:** `pricing_tier` ∈ {free,module,pack,kit}; `parent_product` = name of the pack/kit a module/pack rolls into (NULL for top-level). Invariant to keep (Omnibus-safe): every child price < its parent price. MONETIZATION_BRIEF §7 is the funnel source of truth.
- **CA-prefix convention:** audit/compliance products store `bundled_asset_ids` as `CA:<ids>` referencing `compliance_assets`; Phase-7 products store plain ids referencing `digital_assets`. Phase-12 build + any export must respect this split.
- **Research tooling:** Tavily MCP, Semantic Scholar, Consensus.
- **Script set:** init_db, classify, validate, export_catalogue, seed_* (hospitality/food/nonfood/trades/products/existing_solutions/compliance), build_p1_compliance_pack, build_p2_operations_bundle, set_secret. (Phase 12 adds build_p13_gap_analysis_pack.)
- No `sqlite3` CLI — use Python `sqlite3` module for DB inspection.

### ❓ OPEN QUESTIONS / DECISIONS NEEDED FROM SAMUEL
- **P13 as a FREE lead magnet — confirm strategy?** Roadmap sets P13 (Gap-Analysis + Mock-Audit Lite) at €0 to capture emails and funnel into the €49–99 paid kits. If you'd rather sell P13 outright (e.g. €19), say so before the Phase-12 build sets the pricing. (Default if silent: free lead magnet.)
- ✅ RESOLVED (Samuel, 30/05/2026): VAT — stay non-registered + rely on MoR (Lemon Squeezy is legal seller, handles per-sale EU VAT). Confirm specifics with accountant before launch.
- ✅ RESOLVED (Samuel, 30/05/2026): Excise/duty (alcohol) — KEEP FOLDED into Cashflow/P&L (P2/P4). No dedicated excise tracker.
- Confirm `asset-forge/` living inside the `NeuroHive` repo is intended. (Unchanged.)

### ⚠️ RISKS / WATCHOUTS
- **Slovak copy not yet native-edited** — do NOT publish any listing SK text before a native pass.
- **Compliance prices indicative** — re-verify marketplace comparables + LS fees live at listing time (figures dated 30/05/2026).
- **Standard versions move** — BRCGS Issue 10 (in development) and ISO 9001:2026 (at FDIS) will trigger "transition pack" upsells (mirror P18) and listing-copy updates when they publish.
- **Preview images not generated** (no headless spreadsheet renderer in this env) — capture screenshots at listing time from Excel/Google Sheets.
- **Lemon Squeezy post-Stripe-acquisition uncertainty** — Gumroad fallback pre-vetted; both host the same files, migration = re-upload not rebuild.
- **EU digital-goods withdrawal right** — listings must include the immediate-delivery / 14-day-waiver checkbox (LS provides). Free P13 still needs correct licence/terms.
- One phase per session; if a phase looks like >~15 tool calls, propose splitting.
- Legal-mandatory (Legal=3) auto-promotes to MUST — held since Phase 5 (115/115). Phases 7–11 did not alter tiers.
