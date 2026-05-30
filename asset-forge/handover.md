## STATE — 30/05/2026 18:05
Project: ASSET-FORGE
Phase last completed: 8 - Monetization ✅ COMPLETE (`MONETIZATION_BRIEF.md` written — platform locked w/ LIVE-verified fees+VAT, pricing finalised, bundle architecture confirmed, launch checklist; `existing_solutions` table 0→8 rows; `products.platform` placeholder → "Lemon Squeezy" on all 12 rows)
Checkpoint score: platform decision locked + 8 existing_solutions rows seeded (5 platforms live-verified + 3 marketplace comparables) | ~69% complete (9 of 13 sessions)

### ✅ DONE THIS SESSION
- Wrote `deliverables/MONETIZATION_BRIEF.md` (deliverable #5 of the project DoD). All platform fees + VAT handling **re-verified LIVE 30/05/2026 via Tavily** (brief §3 — never from memory). Sources cited inline + stored in `existing_solutions.source_url`.
- **Platform decision LOCKED:** 🥇 **Lemon Squeezy** (primary) / 🥈 **Gumroad** (fallback) / 📣 **Etsy** (discovery). EU-VAT/full-MoR is the decisive heavily-weighted criterion (Ireland seller → zero tax-filing admin).
- **Live findings that refined the Phase 1 lean:** (1) Lemon Squeezy acquired by **Stripe (Jul-2024)** — still full MoR but fee 5%+$0.50 **+1.5% intl card** → **~6.5%+$0.50 effective** for EU sales; roadmap uncertainty. (2) **Gumroad is full MoR since 01/01/2025** (flat 10%+$0.50 all-in, no surcharges, weekly payout, built-in Discover but 30% on Discover sales). (3) **Payhip only PARTIAL MoR** (EU/UK VAT, seller stays SoR) → **dropped** on the decisive bar.
- **Pricing finalised** (§2): the 12 Phase-7 indicative prices confirmed as launch list prices (gross to buyer; MoR handles VAT on top, fee deducted). Net-after-fee table included. Strategy: anchor+ladder, free gap-analysis-lite lead magnet, hospitality-first (P1 → P2).
- **Bundle architecture confirmed** (§3): Hospitality Pro €69 / Safety Starter €29 / Money Toolkit €79 / Compliance Everything €149 — each with visible vs-parts discount.
- **Launch checklist** (§4): account+tax, per-listing (bilingual EN/SK copy, previews, demo link, licence, refund/EU-withdrawal-waiver, delivery), QA, post-launch.
- **EU VAT mechanics** documented (§1.4): MoR is legal seller → collects+remits per-country VAT → seller does NOT register OSS/file on these sales. Flagged: confirm overall Irish VAT position w/ accountant.
- Wrote + ran `scripts/seed_existing_solutions.py` → `existing_solutions` 0→8 rows (5 platforms live-verified + 3 marketplace comparables w/ fees, gaps, source_url) and **overwrote `products.platform`** "Lemon Squeezy (TBD Phase 8)" → **"Lemon Squeezy"** on all 12. Idempotent + re-runnable. Verified.

### ▶️ NEXT SMALLEST ACTION
- **BRANCH:** run the next phase on **`claude/charming-carson-tVntE`** (= PR #8, the current tip carrying Phases 0–8). Start the fresh session from this branch.
- Open a FRESH session and run **/goal 9 — Build flagships**. Phase 9 builds the **P1 Café / Restaurant Compliance Pack** flagship in `products/` (hospitality-first mandate). Bundled assets = ids **1,2,3,4,5,16,17** (HACCP FSMS · Allergen Matrix · Temperature Log · Cleaning Schedule · Supplier/Delivery Traceability · H&S Risk Assessment/Safety Statement · Fire Safety Register) — all 7 MUST across the 5 hospitality types (satisfies EHO: Reg. 852/2004 + 1169/2011 + Fire Services Act + Safety Health & Welfare at Work Act 2005). Build complexity M, ~2–3 days. Ship **bilingual EN/SK** (parallel headers, instructions, listing copy) with EU formatting (metric, DD/MM/YYYY, comma thousands). Code tier.
- Carry into Phase 9: prices/platform are now LOCKED (P1 = €34, Lemon Squeezy). Build a read-only demo + watermarked previews per launch checklist §4.

### ➕ STANDING ADD-ONS (carry forward)
- **Bilingual EN+SK** binding rule (AGENTS.md). `deliverables/asset_glossary_EN_SK.md` covers the 20 hospitality assets — **P1 build can use it directly.** The **34 food/non-food/trades assets (ids 21–54) still need SK names/microcopy** — backfill before listing P6–P12 (route through native editor; `/slovak` skill NOT installed here).
- **Platform LOCKED (Phase 8):** Lemon Squeezy primary / Gumroad fallback / Etsy discovery. Switch trigger to Gumroad: LS drops MoR VAT, fee >~8% effective, or payout/onboarding breakage. Gumroad store name should be reserved as fallback prep.
- **`existing_solutions` now populated** (8 rows). `products.platform` = "Lemon Squeezy", prices final.
- **Research tooling**: Tavily MCP (used this session for live fee/VAT verification), Semantic Scholar, Consensus.
- **Secrets plumbing** ready: root `.gitignore` excludes `.env`; `asset-forge/.env.example`; `scripts/set_secret.sh`.
- **xlsx tooling note**: `export_catalogue.py` needs `openpyxl` (`pip install openpyxl`). Phase 9 flagship .xlsx build will need openpyxl (or build in Google Sheets). Not vendored — re-install in a fresh session.
- **Script set**: init_db, classify, validate, export_catalogue, seed_* (hospitality/food/nonfood/trades/products), **seed_existing_solutions** (new), set_secret.

### ❓ OPEN QUESTIONS / DECISIONS NEEDED FROM SAMUEL
- ✅ RESOLVED (Samuel, 30/05/2026): **VAT status — Samuel is NOT VAT-registered but can register if better.** Decision: **stay non-registered for now + rely on the MoR.** With a full MoR (Lemon Squeezy) the platform is the legal seller and handles all per-sale EU VAT, so registration is NOT required to sell EU-wide compliantly, and would not improve these B2C template sales (only adds filing + lets you reclaim input VAT on purchases). Still confirm the specifics with an accountant before launch (general mechanism, not tax advice).
- ✅ RESOLVED (Samuel, 30/05/2026): **Excise/duty (alcohol) — KEEP FOLDED** into Cashflow/P&L (P2/P4). No dedicated excise tracker product.
- ✅ RESOLVED earlier (Samuel): pricing researched live in Phase 8 and finalised (done this session).
- Confirm `asset-forge/` living inside the `NeuroHive` repo is intended. (Unchanged.)

### ⚠️ RISKS / WATCHOUTS
- **Lemon Squeezy post-Stripe-acquisition uncertainty** is the main platform risk — Gumroad fallback pre-vetted; both host same files so migration = re-upload, not rebuild.
- **Don't quote LS "5%"** in projections — real effective fee ~6.5%+$0.50 (intl-card surcharge). Modelled in brief §2.
- **Etsy = static files only** → Google-Sheets products need PDF + "make a copy" link; never raw .xlsx where licence forbids redistribution.
- **EU digital-goods withdrawal right** — listings must include the "consent to immediate delivery / waive 14-day withdrawal" checkbox (LS provides it).
- **Re-verify fees at listing time** — all figures dated 30/05/2026; platforms change pricing frequently.
- 34 food/non-food/trades assets are EN-only — SK glossary backfill outstanding before listing P6–P12.
- One phase per session; if a phase looks like >~15 tool calls, propose splitting.
- No `sqlite3` CLI in this environment — use Python (`sqlite3` module) for DB inspection.
- Legal-mandatory (Legal=3) auto-promotes to MUST — held since Phase 5 (115/115). Phases 7–8 did not alter tiers.
