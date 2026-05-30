# PRODUCT ROADMAP — ASSET-FORGE

**Project:** SME Digital-Asset Intelligence → Productisation Pipeline
**Owner:** Samuel Vyhnanek · **Context:** EU (Ireland) seller
**Phase:** 7 — Productisation · **Date:** 30/05/2026
**Source of truth:** `intelligence.db` (442 asset×business-type rows, 54 deduped assets,
21 business types) · `deliverables/MASTER_INTELLIGENCE_REPORT.md` (§3 universal-core
split, §4 hospitality deep-dive) · `pain_points` table (owner-voice evidence).

> Deliverable #4 of the project DoD. This ranks the catalogue's assets into **sellable
> products**, each with a one-page build spec (brief §10). Products are **anchored on
> universal-core assets** (build once, sell many) and **hospitality is ranked to the top**
> per the priority-vertical mandate. The first shippable product (Phase 9) is the
> **Café / Restaurant Compliance Pack**. Every product reuses the **existing 54 assets by
> ID** — no new near-duplicate assets were invented (brief §12 dedupe rule).

---

## 1. Ranking method — demand × price × build-ease

Each product is scored on three transparent axes, then composite-ranked. The roadmap
order then applies the **hospitality-first override** (brief §0/§10): hospitality
products lead regardless of raw composite, because the priority vertical ships first.

| Axis | What it measures | Scale |
|---|---|---|
| **Demand (D)** | breadth of want — how many of the 21 business types have the anchor asset at MUST/SHOULD (from `asset_map`) | 1 (1–2 types) … 5 (all 21) |
| **Price potential (P)** | revenue per sale vs marketplace comparables (Phase 1 `market_validation.md`; **indicative — re-verify live in Phase 8**) | 1 (€15) … 5 (€59) |
| **Build-ease (B)** | inverse of build complexity (asset count, formula depth, cross-sheet logic) | S=3 · M=2 · L=1 |

**Composite = D × P × B.** Higher = build sooner / amortises faster.

| # | Product | Anchor (universal-core?) | D | P | B | **Composite** |
|---:|---|---|:-:|:-:|:-:|:-:|
| P1 | Café / Restaurant Compliance Pack ⭐ | HACCP+H&S+Fire (✅ core) | 4 | 3 | 2 | 24 |
| P2 | Hospitality Operations & GP Bundle | Cashflow+GP+Rota (✅ core) | 4 | 4 | 2 | **32** |
| P3 | H&S Safety Statement Builder | H&S #1 (✅ core, 21/21) | 5 | 2 | 3 | 30 |
| P4 | Cashflow & P&L Tracker | Cashflow (✅ core, 21/21) | 5 | 2 | 2 | 20 |
| P5 | Fire Safety Register & Checks Log | Fire #2 (✅ core, 17) | 4 | 2 | 3 | 24 |
| P6 | Trades Quote → Job → Invoice Suite | Quote/Job spine | 4 | 3 | 2 | 24 |
| P7 | Electrician / Gas Compliance Cert Pack | Trade Cert (niche) | 2 | 3 | 2 | 12 |
| P8 | Food-Manufacturing Compliance Core | HACCP cluster (✅ core) | 3 | 5 | 1 | 15 |
| P9 | Recipe / BOM & Batch Costing Calculator | Costing (✅ core, 10) | 3 | 3 | 2 | 18 |
| P10 | Product Label & Nutrition Generator | Label gen (✅ core, 5) | 2 | 3 | 1 | 6 |
| P11 | Manufacturing ISO 9001 / Quality Pack | NC+Audit+Calibration | 3 | 4 | 1 | 12 |
| P12 | Staff Training & Induction Matrix | Training (cross-vertical, 11) | 3 | 2 | 3 | 18 |

**Roadmap order (hospitality-first override applied):**
P1 → P2 → P3 → P4 → P5 → P6 → P9 → P8 → P12 → P11 → P7 → P10.

Hospitality (P1, P2) leads; the three **horizontal universal anchors** (P3 H&S, P4
Cashflow, P5 Fire) follow because they amortise across all 21 business types; vertical
packs (trades, food-mfg, non-food-mfg) trail as differentiated per-vertical revenue.

**Bundle architecture (standalone → vertical bundle → everything kit):**

```
Hospitality:   P1 (€34) ──┐
                          ├─► Hospitality Pro Bundle  (P1+P2, €69)
               P2 (€49) ──┘        │
                                   └─► + P3/P4/P5 cross-sell
Compliance:    P3 ─┐
               P5 ─┴─► Safety Starter (P3+P5, €29) ─► Compliance Everything (P1+P8+P11+P7, €149)
Money:         P4 ─┐
               P9 ─┴─► Money Toolkit (P4+P9+P6 trades, €79)
```

---

## 2. Product build specs (one-pager each, brief §10 shape)

Asset IDs reference `digital_assets`. Tier source = `asset_map` (MUST anchor / SHOULD
upsell). Prices are **indicative vs marketplace comparables** and are **locked in Phase 8**
once platform + EU-VAT-inclusive pricing is verified live.

---

### ⭐ P1 — Café / Restaurant Compliance Pack  *(FLAGSHIP — Phase 9 build target)*

- **Target:** independent cafés, restaurants, bars, B&Bs (hospitality, 5 business types). Built once, satisfies an EHO inspection.
- **Bundled assets (IDs):** 1 (HACCP FSMS) · 2 (Allergen Matrix) · 3 (Temperature Log) · 4 (Cleaning & Sanitation Schedule) · 5 (Supplier & Delivery Traceability Log) · 17 (Fire Safety Register) · 16 (H&S Risk Assessment & Safety Statement).
- **Tier mix:** all **7 = MUST across all 5 hospitality business types** (legally forced floor — Reg. 852/2004 hygiene + Reg. 1169/2011 allergens + Fire Services Act + Safety, Health & Welfare at Work Act 2005). Pure can't-trade-without-it anchor.
- **Pain it kills:** *"Allergen accuracy on a changing daily-specials menu — high liability, easy to get wrong"* (café); *"Allergen liability across a full menu; EHO inspection risk"* (restaurant). The pack turns inspection dread into a one-folder answer.
- **Build complexity:** **M** · est. **2–3 days** (7 linked sheets, allergen matrix lookup logic, date-stamped log structures, EU formatting). 6 of 7 are universal-core, so the build seeds the food-manufacturing line (P8).
- **Suggested price:** **€34** (vs Etsy/Gumroad HACCP/allergen template bundles €19–€49).
- **Bundle path:** standalone €34 → Hospitality Pro Bundle (+P2) €69 → cross-sell into Compliance Everything kit.

---

### P2 — Hospitality Operations & GP Bundle

- **Target:** bars, cafés, restaurants, hotels — the daily money-pain layer that sits on top of P1's compliance floor.
- **Bundled assets (IDs):** 8 (Cashflow & P&L Tracker) · 7 (Recipe & Menu GP Costing Calculator) · 6 (Stock & Wastage Tracker) · 9 (Staff Rota & Labour-Cost Scheduler) · 11 (Daily Takings & Till Reconciliation).
- **Tier mix:** **SHOULD-heavy** (the high-WTP "wanted, not dreaded" zone) — anchored by Cashflow (wanted 21/21). These are *desired*, so willingness-to-pay is highest here.
- **Pain it kills:** *"Food-cost % / GP erosion; no live view of margin per dish"* and *"Labour-cost % runs away from covers without a rota tied to forecast sales"* (restaurant); *"Stock shrinkage, over-pour and wastage quietly erode GP"* (bar).
- **Build complexity:** **M–L** · est. **3–4 days** (GP costing engine, labour-% vs forecast-sales rota logic, nightly variance, P&L roll-up).
- **Suggested price:** **€49** (operations bundles benchmark €39–€59).
- **Bundle path:** sold beside P1; together = Hospitality Pro Bundle €69 (the headline hospitality offer).

---

### P3 — H&S Risk Assessment & Safety Statement Builder  *(UNIVERSAL #1 — highest leverage)*

- **Target:** **every** SME in Ireland (all 21 business types). Statutory Safety Statement duty under the Safety, Health & Welfare at Work Act 2005.
- **Bundled assets (IDs):** 16 (H&S Risk Assessment & Safety Statement) · optional upsell 51 (Method Statement & RAMS Builder) for site-based trades.
- **Tier mix:** **MUST in 21/21 business types** — the single broadest asset in the catalogue. Legally mandated (Legal=3 → auto-MUST).
- **Pain it kills:** every business legally needs one, few have a current one; consultants charge €300–€800 to write it. A guided template kills that cost.
- **Build complexity:** **S** · est. **1 day** (hazard library + prompts + auto-compiled statement). Cheapest horizontal to build.
- **Suggested price:** **€19** standalone (lead-magnet-adjacent; drives every vertical bundle).
- **Bundle path:** standalone €19 → Safety Starter (+P5 Fire) €29 → embedded in every vertical compliance pack.

---

### P4 — Cashflow & P&L Tracker  *(UNIVERSAL money anchor)*

- **Target:** all 21 business types (the universal money companion to P3's universal compliance).
- **Bundled assets (IDs):** 8 (Cashflow & P&L Tracker).
- **Tier mix:** **wanted (MUST/SHOULD) in all 21 business types but legally mandated in none** — the textbook "desired, not dreaded" pure-WTP product.
- **Pain it kills:** *"Occupancy/seasonality makes cashflow lumpy and hard to forecast"* (B&B); *"Chasing payments / cashflow gaps on many small jobs"* (electrician) — lumpy cash is the cross-vertical owner nightmare.
- **Build complexity:** **M** · est. **1–2 days** (12-month rolling cashflow, P&L roll-up, scenario toggle).
- **Suggested price:** **€24** (finance trackers benchmark €15–€35).
- **Bundle path:** standalone €24 → Money Toolkit (+P9 +P6) €79 → in every vertical bundle.

---

### P5 — Fire Safety Register & Checks Log  *(UNIVERSAL #2)*

- **Target:** all premises-based business types (MUST in 17/21).
- **Bundled assets (IDs):** 17 (Fire Safety Register & Checks Log).
- **Tier mix:** **MUST in 17 business types** (Fire Services Acts — statutory). Auto-MUST.
- **Pain it kills:** fire-register upkeep is a recurring inspection item that owners forget until an audit; a structured log + reminder cadence removes the scramble.
- **Build complexity:** **S** · est. **0.5–1 day** (register + scheduled-checks log + expiry reminders).
- **Suggested price:** **€15** standalone; primarily a **cross-sell / bundle filler**.
- **Bundle path:** Safety Starter (P3+P5) €29 → folded into every compliance pack.

---

### P6 — Trades Quote → Job → Invoice Suite

- **Target:** the 6 trades (electrician, plumber, carpenter, painter, tiler, landscaper) — the commercial spine, SHOULD-heavy / highest WTP.
- **Bundled assets (IDs):** 39 (Job Quotation & Estimating Tool) · 48 (Job Schedule, Dispatch & Site Diary) · 53 (Snag List & Job Sign-off / Handover) · 54 (Customer Enquiry & Job Pipeline CRM) · 8 (Cashflow & P&L) · 52 (Cert, Card & Insurance Expiry Tracker).
- **Tier mix:** SHOULD anchor (Quote tool wanted in 11 types) + COULD fillers; legally-mandatory items handled in P7.
- **Pain it kills:** *"Chasing payments / cashflow gaps on many small jobs"* and *"Quoting is slow and inconsistent → won/lost margin"* (trades). The quote-to-cash chain is the single biggest trades money leak.
- **Build complexity:** **M** · est. **3 days** (estimating calculator, pipeline board, snag sign-off, invoice link).
- **Suggested price:** **€39** (job-management template suites benchmark €29–€49; positioned against contract-locked SaaS like Tradify that owners resent).
- **Bundle path:** standalone €39 → +P7 cert pack for regulated trades → Money Toolkit cross-sell.

---

### P7 — Electrician / Gas Compliance Cert Pack

- **Target:** electricians (Safe Electric) and plumber/gas (RGI) — niche but legally forced, high per-buyer intensity.
- **Bundled assets (IDs):** 47 (Trade Completion & Compliance Certificate Register) · 51 (Method Statement & RAMS Builder) · 16 (H&S Safety Statement) · 52 (Cert, Card & Insurance Expiry Tracker) · 41 (Chemical Agents/SDS Register).
- **Tier mix:** MUST anchor (Trade Completion Cert = MUST in electrician + plumber; Legal=3) + H&S MUST.
- **Pain it kills:** *"RGI gas-cert / Declaration of Conformance compliance per job"* (plumber); *"Safe Electric completion-cert admin and keeping registration valid"* (electrician).
- **Build complexity:** **M** · est. **2 days**.
- **Suggested price:** **€34** (regulated-trade buyers pay a premium — losing registration halts trading).
- **Bundle path:** sold beside P6 (Trades Suite); together = regulated-trade everything kit.

---

### P8 — Food-Manufacturing Compliance Core

- **Target:** bakery, butchery, dairy, beverage, ready-meals (food mfg, 5 types) — heaviest regulatory load, smaller pool, highest per-unit value.
- **Bundled assets (IDs):** 1 (HACCP FSMS) · 3 (Temperature Log) · 4 (Cleaning Schedule) · 5 (Traceability Log) · 30 (Calibration Log) · 31 (Foreign-Body Control) · 32 (Pest Control Log) · 35 (Internal Audit / GMP Self-Inspection) · 36 (Recall / Mock-Recall Log).
- **Tier mix:** dense **MUST** stack (Reg. 852/853/2004 + HACCP Codex). Reuses 4 of P1's core assets — same build, deeper compliance.
- **Pain it kills:** *"Cook/chill CCP temperature evidence across the production day"* (ready meals); *"Losing the 853/2004 approval / health-mark audit halts the business"* (butchery).
- **Build complexity:** **L** · est. **4–5 days** (9 linked compliance sheets + calibration/recall logic).
- **Suggested price:** **€59** (highest single-product price — failure = lost approval).
- **Bundle path:** add niche 24 (Health-Mark Control) for animal-origin, 25 (e-mark) for packaged → vertical premium → Compliance Everything kit.

---

### P9 — Recipe / BOM & Batch Costing Calculator

- **Target:** food mfg (bakery, ready meals) + hospitality kitchens — the costing universal-core.
- **Bundled assets (IDs):** 22 (Recipe / BOM & Batch Costing Calculator) · cross-link 7 (Menu GP Costing) for hospitality.
- **Tier mix:** SHOULD/MUST across 10 types (wanted everywhere food is made).
- **Pain it kills:** *"Wafer-thin margins destroyed by un-costed recipes and volatile ingredient prices"* (bakery); *"Pricing is guesswork without recipe costing"* (café).
- **Build complexity:** **M** · est. **2 days** (ingredient cost roll-up, yield %, price-volatility scenario).
- **Suggested price:** **€29**.
- **Bundle path:** Money Toolkit (+P4 +P6) → food-mfg bundle.

---

### P10 — Product Label & Nutrition Declaration Generator

- **Target:** food mfg producers needing FIC-compliant labels (bakery, ready meals, beverage).
- **Bundled assets (IDs):** 23 (Product Label & Nutrition Declaration Generator) · 26 (Shelf-Life / Date-Coding) upsell.
- **Tier mix:** MUST in 5 food-mfg types (Reg. 1169/2011 FIC — legally mandated).
- **Pain it kills:** *"Manual per-SKU label + nutrition creation is slow and error-prone"* (bakery).
- **Build complexity:** **L** · est. **3–4 days** (nutrition calc engine, allergen emphasis, QUID, label layout).
- **Suggested price:** **€29**.
- **Bundle path:** add to P8 Food-Mfg Compliance Core as the labelling module.

---

### P11 — Manufacturing ISO 9001 / Quality Pack

- **Target:** non-food manufacturing (metal/engineering, plastics, packaging, joinery, electronics).
- **Bundled assets (IDs):** 38 (QC Inspection & Non-Conformance Record) · 46 (ISO 9001 Internal Audit & Management-Review Log) · 30 (Calibration Log) · 28 (Supplier Approval & Specification Register) · 42 (Material Certificate & Batch Traceability).
- **Tier mix:** SHOULD-heavy commercial demand (ISO 9001 is customer-required, not law) + 40/41 safety MUST cross-sell.
- **Pain it kills:** *"Un-tracked non-conformances and rework quietly destroy job profit"* and *"ISO 9001 audit document load"* (metal/engineering).
- **Build complexity:** **L** · est. **4 days**.
- **Suggested price:** **€49**.
- **Bundle path:** + CE Marking register (37) for machinery/electronics → non-food-mfg everything kit. *(Reuses the same artefacts the bonus audit track P10–12 will resell to auditors/consultants — build once, two markets.)*

---

### P12 — Staff Training & Induction Matrix

- **Target:** cross-vertical HR (wanted in 11 business types — hospitality, food mfg, mfg).
- **Bundled assets (IDs):** 10 (Staff Training & Induction Matrix).
- **Tier mix:** SHOULD/MUST (food-safety training is a legal expectation in food businesses; HR good-practice elsewhere).
- **Pain it kills:** proving who is trained on what at audit; onboarding consistency. Low pain individually but a high-attach bundle filler.
- **Build complexity:** **S** · est. **0.5–1 day**.
- **Suggested price:** **€15** — primarily a bundle attach to P1 / P8.
- **Bundle path:** attach to every compliance pack as the "people" module.

---

## 3. What Phase 7 hands to Phases 8–9

1. **Phase 9 builds P1 first** — the Café / Restaurant Compliance Pack is the flagship: compact, legally-forced, demonstrable, 6/7 universal-core (seeds the food line).
2. **Phase 8 (Monetization)** locks: platform (preliminary lean Lemon Squeezy / Gumroad — **re-verify EU-VAT handling + fees live**), the prices above (currently indicative), and the bundle architecture in §1.
3. **Twelve products** are seeded into the `products` DB table (name, target, bundled_asset_ids, indicative price) — queryable, regenerate with `python3 scripts/seed_products.py`.
4. **Bonus track (P10–12 of the session plan)** reuses P8/P11 artefacts for auditor/consultant buyers — a second revenue line with no new builds.

**Integrity:** every product anchors on existing catalogue assets (no invented
duplicates); every MUST claim traces to a Legal=3 row in `asset_map`; every pain quote
traces to a `pain_points` row with an `evidence_url`. Prices are indicative pending the
Phase 8 live pricing pass.

*End of Product Roadmap — Phase 7. Next: Phase 8 — Monetization (`MONETIZATION_BRIEF.md`).*
