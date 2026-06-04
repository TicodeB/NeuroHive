# CODEX BRIEF — Turnkey Startup Packs (ASSET-FORGE v2.0)

> Source-of-truth brief for the LEANTA "Turnkey Startup Pack" product line.
> Owner: Samuel Vyhnánek · Saved: 2026-06-04 · Status: Sprint 1 (Boutique Hotel) built.

## 1. Business & product
**LEANTA** sells industry-specific, step-by-step **turnkey startup packs** that take an
entrepreneur from **0 → profitable in 90–180 days**. Distinct from the existing
ASSET-FORGE "operate-an-existing-business" packs — this line is the **pre-launch /
launch** journey.

The journey is a fixed **7-phase** spine:

| Phase | Name | Outcome |
|------|------|---------|
| 0 | Market Validation | Prove demand before committing capital |
| 1 | Business Plan | Service definition + 3-scenario P&L + go/no-go |
| 2 | Capital Raising | Capex, funding mix, debt service, runway |
| 3 | Procurement | Vendors, fit-out budget, RFQ compare, POs |
| 4 | Team Building | Org design, hiring, payroll budget |
| 5 | Operations | Daily playbooks + live KPI dashboard |
| 6 | Launch / First 100 Days | Soft open → grand open → scorecard |
| (7) | Scaling | Premium/optional add-on |

## 2. Delivery shape
- **One `.xlsx` per phase**, named `NN_Name.xlsx` (`00_…` → `06_…`).
- Folder: `products/industries/<vertical>/<pack>/` + a pack `README.md`.
- Shared template assets live in `products/templates/`; guides in `products/guides/`;
  the Definition-of-Done validator in `products/validation/`.
- Non-spreadsheet artefacts (setup guide, org chart, pitch deck, job descriptions,
  branded checklists) are produced via the **Gamma / Canva** MCP servers as
  `.pdf` / `.pptx` / `.docx`.

## 3. Pilots
- **Boutique Hotel — 4★, 20–30 rooms** *(Sprint 1, BUILT)*: ~€600k capex (leased,
  fit-out led), ADR €135, occupancy 72%, RevPAR €97; **15 KPIs** (Occupancy, ADR,
  RevPAR, GOPPAR, Guest NPS, Labour %, F&B %, Repeat %, ALOS, Direct-booking %,
  Room turnaround, Maintenance response, Staff turnover, Complaints/100 stays,
  Payment collection %). Tiers: T2 €149 · T3 €599 · T4 €1,699.
- **Artisan Bakery — 5–10k units/wk** *(next sprint)*: ~€200k equipment; 15 KPIs
  (OEE = Availability×Performance×Quality, defect %, waste %, labour productivity,
  labour %, material %, OTD %, inventory turns, GM %, retention, product-mix, batch
  consistency, shelf-life, downtime, traceability). Tiers: T2 €99 · T3 €499 · T4 €1,499.

## 4. Definition of Done (HARD GATE — Part C)
A pack is only "done" when every workbook:
1. Opens cleanly as a real `.xlsx` (zip + XML well-formed).
2. Has **all dashboard figures LINKED** to source sheets — **no hard-coded numbers**.
3. Shows **🟢🟡🔴 traffic lights** against target thresholds.
4. Exposes **≥ 15 specific, measurable metrics** for the industry.
5. Contains **no `#REF!`/`#DIV/0!`**; cross-sheet references resolve.
6. Ships **pre-formatted data-entry templates** with auto-calc.
7. Includes **sample data** proving the calcs.
8. Carries an Assumptions / data-dictionary sheet.

Rejected: conceptual mockups, broken formulas, missing sheets, vague metrics,
hard-coded values. Enforced by `products/validation/test_all_formulas.py`.

## 5. Funding & grant layer (cross-vertical, EN + SK)
A reusable **grant & funding application pack** under
`products/templates/grant-applications/`, grounded in the REAL published forms:
- **Ireland:** LEO Priming / Business Expansion grant, Microfinance Ireland loan,
  Fáilte Ireland tourism capital schemes, and the **SURE** founder income-tax refund
  (up to 41 % of capital invested, reclaiming PAYE tax over the prior 6 years).
- **Slovakia:** ÚPSVaR §49 príspevok na SZČ + eurofondy / grant.sk podnikateľský-plán
  structure (Finančný plán as povinná príloha).
The boutique hotel is the worked example; SURE feeds the Phase-2 equity line.

## 6. Engine reuse
Built on the existing ASSET-FORGE engine — `scripts/design_system.py` (premium
styling), the dashboard/ledger builder patterns in `scripts/build_pack.py`, and
`intelligence.db`. New parallel modules: `scripts/startup_spec.py`,
`scripts/startup_build.py`, `scripts/grant_build.py`. The 24-pack
`pack_spec.py`/`build_pack.py` system is untouched.

## 7. Roadmap / open opportunities
- **Education edition** (sell to schools/colleges/universities as project material):
  researched — see `research/education_market_opportunity.md`. Verdict: cautious-go;
  best paid fit is universities/FE; secondary has the biggest audience but a free
  state/charity incumbent (Student Enterprise Programme, JA) owns the slot.
- Artisan Bakery pack; per-pack listing kits; remaining verticals; a quantified
  `startup_benchmarks` table.
