# P2 — Hospitality Operations & GP Bundle (FLAGSHIP #2)

**Product file:** `P2_Hospitality_Operations_GP_Bundle.xlsx` (7 sheets, EN/SK)
**Preview file:** `P2_DEMO_Hospitality_Operations_GP_Bundle.xlsx` (watermarked, sheet-protected)
**Build:** `python3 scripts/build_p2_operations_bundle.py` · Version v1.0 · 30/05/2026
**Price (locked, Phase 8):** **€49** · **Platform:** Lemon Squeezy (primary) / Gumroad (fallback)
**DB product id:** 2 · **Bundled assets (ids):** 8, 7, 6, 9, 11 **+ 10 (added — see below)**

---

## What this is

The second flagship — the **daily-money layer that sits on top of P1's compliance floor**.
Where P1 keeps you legal, P2 keeps you profitable: live margin, labour %, cash position
and till accuracy for an owner-run café/restaurant/bar.

### Sheets
| # | Sheet | Asset (DB id) | What it does |
|---|-------|---------------|--------------|
| 00 | Start Here / Začnite tu | — | how-to + bundle map |
| 01 | Cashflow & P&L Tracker | 8 | 12-month rolling cash + monthly P&L (revenue → GP → net profit → closing cash, auto-calculated) |
| 02 | Recipe & Menu GP Costing | 7 | plate cost, suggested price from target GP%, actual GP% vs menu price, LOW-margin flag |
| 03 | Stock & Wastage Tracker | 6 | opening + purchases − closing usage, wastage value, high-shrinkage flag |
| 04 | Staff Rota & Labour-Cost | 9 | shift hours × rate → labour cost → **labour % of forecast sales** (red >35%) |
| 05 | Daily Takings & Till Reconciliation | 11 | Z-read vs counted cash + card, variance flag |
| 06 | **Staff Training & Induction Matrix** | **10** | **dated proof of training before the floor** (see note) |

### ⭐ Why sheet 06 (Training & Induction) was added
The defined P2 bundle was assets **8, 7, 6, 9, 11**. The owner correctly flagged that
**no worker should be on the floor without manual-handling and induction training** — and
an inspector wants *proof*, not just a hazard line. So asset **10 (Staff Training &
Induction Matrix)** was folded in as the "people module." It tracks each employee against
**Induction · Manual handling · Food hygiene · Allergen awareness · Fire safety · H&S/first
aid**, with the date completed and a refresher-due date. Blank cells flag a training gap.

This complements P1's H&S sheet (which lists manual handling as a *hazard with controls*);
P2 sheet 06 is the *record that the training actually happened*. Together P1 + P2 answer
both halves of an inspection. The DB `products` row for P2 was updated to
`bundled_asset_ids = "8,7,6,9,11,10"`.

### Built-in logic
Cashflow auto-rolls revenue→GP→net profit→closing cash (negative cash = red) · GP costing
suggested price = cost ÷ (1 − target GP%), LOW flag when menu price underperforms · labour
% of sales with 35% red threshold · till variance flagged beyond ±€1 · wastage value
auto-costed.

### EU conventions
€ with comma thousands · DD/MM/YYYY date cells · metric units (L, kg, g, ml).

### Bilingual (EN / SK)
Parallel EN/SK headers, instructions and notes on every sheet (from
`deliverables/asset_glossary_EN_SK.md`). ⚠️ Slovak needs a native-editor pass before
public launch (`/slovak` skill not installed here).

---

## Bundle path
Standalone €49 → **Hospitality Pro Bundle** (P1 €34 + P2 €49 → €69, the headline
hospitality offer) → cross-sell P3/P4/P5 universal compliance + money anchors.

## Launch checklist status
- [x] Product workbook built (full, editable)
- [x] Watermarked read-only demo built
- [x] Bilingual EN/SK copy
- [x] Price + platform locked (€49, Lemon Squeezy)
- [x] Training/induction evidence included (owner request)
- [ ] Preview images (capture at listing time)
- [ ] Slovak native-editor pass before public launch
- [ ] Licence text + EU 14-day-withdrawal waiver checkbox
- [ ] Re-verify platform fees live at listing time
