# MASTER INTELLIGENCE REPORT — ASSET-FORGE

**Project:** SME Digital-Asset Intelligence → Productisation Pipeline
**Owner:** Samuel Vyhnanek · **Context:** EU (Ireland) seller
**Phase:** 6 — Synthesis · **Date:** 30/05/2026
**Sources:** `intelligence.db` (442 asset×business-type rows, 54 assets, 21 business
types, 4 verticals) · `research/*.md` (Phases 1–4) · `deliverables/phase5_validation.md`

> This is the human-readable synthesis of the catalogue (deliverable #2 of the
> brief's definition-of-done). Its companion is `asset_catalogue.xlsx` — the flat,
> skim-able export of the same data. Everything here is **traceable to the DB**;
> tiers are final per the Phase 5 deterministic validation (0 anomalies, all
> Section [12] gates pass).

---

## 1. Executive summary

We mapped the digital assets that real SMEs in **hospitality, food manufacturing,
non-food manufacturing and trades** keep, redo, or lose money on — and scored each
**asset × business-type** pairing on the four-axis rubric (Legal, Revenue, Pain,
Frequency → weighted /24). The catalogue holds **442 scored pairings** across **54
deduped digital assets** and **21 business types**.

**The headline finding:** the highest-leverage products are **not** vertical-specific.
A small spine of **compliance and money-control assets is MUST-HAVE across many
business types at once** — build once, sell many. The single broadest asset, the
**H&S Risk Assessment & Safety Statement, is MUST in all 21/21 business types**; the
**Cashflow & P&L Tracker is wanted (MUST/SHOULD) in all 21**. These "universal-core"
assets are the commercial foundation; vertical-specific assets are the differentiated
upsell.

**Tier mix (all 442 rows):**

| Tier | Rows | Share | Meaning |
|---|---:|---:|---|
| **MUST** | 129 | 29.2% | needed — legal floor or survival-critical |
| **SHOULD** | 218 | 49.3% | *wanted, sells well* — the willingness-to-pay zone |
| **COULD** | 95 | 21.5% | bundle filler / nice extras |
| **WON'T** | 0 | 0.0% | excluded (none reached the catalogue) |

The **SHOULD band is the largest single tier (49%)** — exactly the brief's "good to
have, not needed but wanted" zone, where buyers reach for the wallet because the asset
is *desired, not dreaded*. MUST sells the listing (it's the can't-trade-without-it
anchor); SHOULD/COULD is where margin and bundle size grow.

**115 of 129 MUST rows are legally mandated** (Legal = 3 → auto-MUST). That is the
defensible floor: these aren't opinions, they're statutory duties (food hygiene,
fire, H&S, e-mark, health-mark, completion certs). Every MUST/SHOULD row carries an
`evidence_url`.

---

## 2. The catalogue at a glance

**Verticals → business types (21):**

- **Hospitality (5):** Bar/pub · Café/coffee shop · Restaurant · B&B/guesthouse · Hotel
- **Food manufacturing (5):** Bakery · Butchery/meat · Dairy · Beverage · Ready meals/catering
- **Non-food manufacturing (5):** Metal/engineering · Plastics/injection · Packaging/print · Joinery/furniture · Light electronics
- **Trades (6):** Electrician · Plumber/heating · Carpenter/joiner · Painter/decorator · Tiler · Landscaper/groundworks

**Tier × vertical:**

| Vertical | MUST | SHOULD | COULD | MUST-fraction |
|---|---:|---:|---:|---:|
| **Hospitality** | 37 | 31 | 22 | **41%** (densest) |
| Food manufacturing | 48 | 62 | 20 | 37% |
| Non-food manufacturing | 22 | 65 | 35 | 18% |
| Trades | 22 | 60 | 18 | 22% |

**Read-out:**
- **Hospitality is the densest MUST-fraction (41%)** → confirms the brief's
  priority-vertical pick. Hospitality buyers face a compact, legally-forced asset
  set (HACCP, allergens, temperature, fire, H&S) → clean, demonstrable pain → ship
  here first.
- **Food manufacturing carries the most MUST rows in absolute terms (48)** → the
  regulatory load is heaviest (Reg. 853/2004 health-mark, e-mark, recall, traceability).
  Highest-value compliance bundles live here, but the buyer pool is smaller.
- **Non-food manufacturing and trades are SHOULD-heavy** → demand is *commercial*, not
  legally forced: the Quote → Job → Invoice → Cert spine is **wanted** (highest
  willingness-to-pay), matching Phase 4's owner-voice evidence.

---

## 3. Universal-core vs niche-specific — the productisation split

This is the central analytical output of Phase 6: **which assets to build once and
sell across many business types (universal core), versus which are deep but narrow
(niche).** The roadmap (Phase 7) is built on this split.

### 3.1 Universal core — MUST across ≥3 business types (`v_universal_core`)

These twelve are the **build-once / sell-many** spine. Each is a single product that
is *legally needed* by many different SMEs, so one build amortises across the widest
audience.

| # | Asset | MUST in N business types | Cross-vertical reach |
|---:|---|---:|---|
| 1 | **H&S Risk Assessment & Safety Statement** | **21 / 21** | every vertical |
| 2 | **Fire Safety Register & Checks Log** | 17 | every vertical |
| 3 | HACCP Food Safety Management System | 10 | hospitality + food mfg |
| 4 | Cleaning & Sanitation Schedule | 10 | hospitality + food mfg |
| 5 | Supplier & Delivery Traceability Log | 10 | hospitality + food mfg |
| 6 | Allergen Matrix & Menu Declaration Tool | 8 | hospitality + food mfg |
| 7 | Temperature Monitoring Log | 8 | hospitality + food mfg |
| 8 | Work Equipment & Machinery Safety/Guarding Inspection Register | 7 | manufacturing + trades |
| 9 | Product Label & Nutrition Declaration Generator | 5 | food mfg |
| 10 | Chemical Agents (SDS) Register & Risk Assessment | 5 | manufacturing + trades |
| 11 | RCT & Subcontractor Payment Tracker | 4 | trades + construction |
| 12 | Batch Production & Yield Record | 3 | food + non-food mfg |

**Two tiers within the core:**

- **Truly horizontal (sell to anyone):** #1 H&S Safety Statement and #2 Fire Safety
  Register apply across *every* vertical. These are the broadest possible products —
  an SME of any kind in Ireland has a statutory Safety Statement duty (Safety, Health
  and Welfare at Work Act 2005) and fire-safety obligations. **The H&S Safety Statement
  is the single highest-leverage asset in the entire catalogue.**
- **Food-cluster core (#3–#7):** the HACCP/allergen/temperature/traceability/cleaning
  block is MUST across all of hospitality *and* food manufacturing (10 business types).
  This is the spine of every food bundle and the reason hospitality and food-mfg share
  product DNA.

### 3.2 Commercial core — widest MUST **+** SHOULD reach (willingness-to-pay)

MUST reach alone undersells products that are *wanted everywhere but legally forced
nowhere*. Ranking by combined MUST+SHOULD breadth surfaces the true commercial
all-rounders:

| Asset | Wanted in N business types | Note |
|---|---:|---|
| **H&S Risk Assessment & Safety Statement** | 21 | also #1 on MUST |
| **Cashflow & P&L Tracker** | **21** | wanted everywhere, mandated nowhere — pure WTP |
| Fire Safety Register & Checks Log | 17 | |
| Wholesale Order & B2B Invoice Tool | 12 | |
| Maintenance & PPM Asset Register | 12 | |
| Job Quotation & Estimating Tool | 11 | trades/mfg money-maker |
| Staff Training & Induction Matrix | 11 | |
| Recipe / BOM & Batch Costing Calculator | 10 | |

The **Cashflow & P&L Tracker** is the standout: **wanted (MUST/SHOULD) in all 21
business types but legally mandated in none** — the textbook "desired, not dreaded"
high-WTP product. It belongs near the top of the roadmap as the universal **money**
companion to the universal **compliance** anchor (H&S).

### 3.3 Niche-specific — deep but narrow (MUST in only 1–2 business types)

These are the **differentiated upsells**: high value to a specific buyer, low reuse.
They don't anchor a horizontal product; they make a *vertical bundle* feel bespoke and
justify a premium per-vertical price.

| Asset | MUST in N | Belongs to |
|---|---:|---|
| Approved Establishment File & Health-Mark Control (Reg 853/2004) | 2 | butchery, dairy (animal-origin food) |
| CE Marking, Declaration of Conformity & Technical File Register | 2 | non-food mfg (machinery/electronics) |
| Recall / Withdrawal Plan & Mock-Recall Log | 2 | food mfg |
| Trade Completion & Compliance Certificate Register | 2 | electrician, plumber/gas |
| Net-Quantity & Average-Quantity (e-mark) Control Sheet | 1 | packaged food/beverage |
| Shelf-Life, Durability & Date-Coding Record | 1 | food mfg |
| Quality Control Inspection & Non-Conformance Record | 1 | precision manufacturing |
| Environmental, Waste & Producer-Responsibility (EPR) Register | 1 | packaging/print |

**Productisation rule (feeds Phase 7):** anchor every product on a **universal-core**
asset (broad reach = volume), then bolt on **niche-specific** assets per vertical to
differentiate and lift price. Standalone → vertical bundle → "everything" kit.

---

## 4. Priority vertical — HOSPITALITY (ship first)

Per the brief, hospitality is productised first. Its MUST set is compact and entirely
legally-forced — the cleanest pain story to sell against. **Seven assets are MUST
across all five hospitality business types** (bar, café, restaurant, B&B, hotel):

1. HACCP Food Safety Management System
2. Allergen Matrix & Menu Declaration Tool
3. Temperature Monitoring Log
4. Cleaning & Sanitation Schedule
5. Supplier & Delivery Traceability Log
6. Fire Safety Register & Checks Log
7. H&S Risk Assessment & Safety Statement

These seven *are* the hospitality flagship: a **"Café / Restaurant Compliance Pack"**
that satisfies an EHO inspection (Reg. 852/2004 hygiene + Reg. 1169/2011 allergens +
fire + Safety Statement) in one EU-formatted spreadsheet bundle. Six of the seven are
universal-core, so the same build seeds the food-manufacturing line later.

**Hospitality owner-voice pain (severe, from `pain_points`):**

- *Bar/pub:* "Stock shrinkage, over-pour and wastage quietly erode GP; hard to spot
  without nightly variance." → **Stock & Wastage Tracker** (the SHOULD-tier upsell).
- *Café:* "Allergen accuracy on a changing daily-specials menu — high liability, easy
  to get wrong." → **Allergen Matrix** (MUST anchor).
- *Restaurant:* "Food-cost % / GP erosion; no live view of margin per dish." +
  "Labour-cost % runs away from covers without a rota tied to forecast sales." →
  **Recipe & Menu GP Costing Calculator** + **Staff Rota & Labour-Cost Scheduler**.
- *B&B:* "OTA commission vs direct bookings squeezes margin." → **Room Bookings &
  Occupancy Dashboard**.
- *Hotel:* "Revenue management (RevPAR/ADR) across channels is opaque." → dashboard.

The compliance MUST anchors the sale (you legally must have it); the GP/wastage/rota
SHOULD assets are where hospitality owners actually *feel* daily money pain — the
high-WTP upsells that turn a €19 compliance pack into a €49 operations bundle.

---

## 5. Department & buyer shape

**Where the MUST weight sits (by department):** 122 of 129 MUST rows fall in **Quality
& Compliance** — the legal floor *is* the compliance department. Finance and
Operations carry the rest. This concentration is exactly why the universal-core
compliance assets are the product foundation: compliance is where "needed" lives, and
"needed" is what converts a browser into a buyer.

**Buyer dimension:** 428 rows are tagged `operator` (owner/staff running the business),
8 `consultant`, 6 `auditor`. Operator dominates by design — the auditor/consultant
demand is the **bonus track (Phases 10–12)**; the 14 captured rows are seeds (Safe
Electric/RGI inspectors, H&S consultants, accountants). The same compliance artefacts
double as auditor tooling later — build-once value extends across both sides of the
audit.

---

## 6. Existing solutions & the gap (carry-forward)

`existing_solutions` is intentionally empty at Phase 6 — competitor fee/feature facts
must be **verified live** (brief [3]/[11]) and are gathered in the Phase 8 monetization
pass, not stated from memory here. The Phase 1 `research/market_validation.md` already
evidences the demand side: spreadsheet/template products demonstrably sell on Etsy /
Gumroad / Lemon Squeezy, and the complaints about niche SaaS (EPOS, HACCP apps, job-
management tools) *are* the product brief. Preliminary (non-final) platform lean:
**Lemon Squeezy** primary / **Gumroad** fallback / **Etsy** discovery — EU-VAT weighted,
locked in Phase 8 with fees re-verified live.

---

## 7. What Phase 6 locks for the roadmap (Phase 7)

1. **Anchor on universal core.** Rank products that sit on a MUST-across-many asset to
   the top. The two horizontal anchors are **H&S Safety Statement** (compliance) and
   **Cashflow & P&L Tracker** (money).
2. **Ship hospitality first.** The seven-asset hospitality compliance pack is the first
   flagship (Phase 9) — compact, legally-forced, demonstrable, and 6/7 universal-core.
3. **Bundle path:** universal-core MUST anchor → vertical-specific niche upsells →
   "everything" kit. Standalone €, vertical bundle €€, full kit €€€.
4. **High-WTP upsells are SHOULD, not MUST.** GP costing, wastage, rota, quote/estimate
   — these are what owners feel daily; price the bundle on them.
5. **Bonus compliance track (10–12)** reuses the same artefacts for auditor/consultant
   buyers — second revenue line, no new builds.

---

## 8. Provenance & integrity

- **Data:** `intelligence.db` — 442 `asset_map` rows, 54 `digital_assets`,
  21 `business_types`, 67 `pain_points`.
- **Validation:** Phase 5 deterministic pass = **0 anomalies, all Section [12] gates
  PASS** (score = 3L+2R+2P+F re-derived on every row; tier per rubric [6]; 115/115
  legal=3 rows are MUST; every MUST/SHOULD row has evidence; no duplicate asset
  functions). Tiers are **final**; re-cut later by reading the raw axis columns.
- **Companion export:** `deliverables/asset_catalogue.xlsx` (7 sheets — Overview,
  Asset_Map, Digital_Assets, Universal_Core, MUST_Haves, Pain_Points, Tier_Summary),
  regenerate any time with `python3 scripts/export_catalogue.py`.
- **Optional, non-blocking:** the OpenRouter model second-opinion (`classify.py`)
  remains deferred (environment egress blocks `openrouter.ai`). It does not gate the
  tiers — the deterministic pass finalises them.

---

*End of Master Intelligence Report — Phase 6. Next: Phase 7 — Productisation
(`PRODUCT_ROADMAP.md`).*
