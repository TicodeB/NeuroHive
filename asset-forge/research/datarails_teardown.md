# Datarails teardown → design lessons for our packs

**Date:** 31/05/2026 · **Owner:** Samuel · **Track:** Premium-Pack (Phase 13)
**Task:** study how Datarails designs its Excel assets + insight engine, extract the
transferable principles, and turn them into a concrete design spec for our packs.

> **Method note:** built from Datarails' own product + **support/KB** pages (feature
> mechanics) and third-party reviews (Cube, f9finance, CFO Shortlist), captured via
> search on 31/05/2026. Feature *names* and the formula structure below are
> Datarails' own (verified). Re-verify exact mechanics live before quoting in a
> listing. (Marketing pages 403 the fetcher; the KB articles are the gold source.)

---

## 1. What Datarails is (the one-liner)

An **Excel-native, AI-powered FP&A / "FinanceOS"** for mid-market & SMB finance
teams: *keep working in Excel, but every spreadsheet is wired into a central cloud
data engine* so numbers consolidate, refresh, drill down, and get analysed by AI.
Positioning: *"We enhance Excel rather than replace it."*

| Surface | Datarails name | What it is (verified) |
|---|---|---|
| Excel add-in | **Datarails Flex** | the ribbon/add-in; live two-way link between a workbook and the Datarails DB |
| Link a file | **Connect** → a **Filebox** | binds a local Excel file into the Datarails environment |
| Live cells | **DR Formulas** (Datarails Connect) | three-part formulas that *query* the central DB into a cell |
| Slices | **Datarails Excel Table** | a filtered, dimensional extract of the DB pulled into any sheet |
| Reporting | **Dashboards** (widgets) | graphs/tables built on DB data; one-click refresh; drill-down |
| Narrative | **Storyboards** | 2-click AI turns the data into a board-ready story (visuals + commentary) |
| AI | **FP&A Genius** ("ChatGPT for the CFO's office") | NL Q&A + auto insights grounded in the company's own numbers |

---

## 2. How the asset is actually built (the architecture lessons)

The genius is the **separation of a data engine from the Excel front-end**. The
transferable mechanics:

1. **Data layer ≠ presentation layer.** Raw data lives once in a central store
   (200+ source connectors + spreadsheets). Excel sheets don't *hold* the numbers
   — they **query** them. One source, many views.
2. **A cell = a query.** A **DR Formula** has three parts — *(a)* the DR Formula
   (opens the DB connection + retrieval type), *(b)* the **Function** (aggregation),
   *(c)* **fields + values** = the filter. Crucially the filter dimensions are
   **timeframe · scenario · account ID** (+ entity/department). That's the
   dimensional model: *tag once, slice infinitely.*
3. **Drill-down is first-class.** Any aggregated cell can be expanded to the rows
   behind it ("total sales of a department → deals per salesperson"). Trust =
   traceability from headline number to source.
4. **Consolidation + version control + intercompany eliminations** roll many files
   into one truth, all from inside Excel.
5. **Budget-vs-Actual / Forecast-vs-Actual is the spine.** "Scenario" is a primary
   dimension; every view compares **plan vs reality** and surfaces the **variance**.
6. **Refresh, don't rebuild.** Dashboards/reports are permanent templates that
   re-read the DB on one click — you never redraw them each month.

## 3. Dashboards & Storyboards — the design philosophy
- **Board-ready, branded, few high-signal KPIs** (revenue, margin, cash, BvA
  variance, burn). "Easy to read; avoid unnecessary design elements."
- **Widgets on shared data** — charts (column/line/pie + gauges/spider) and tables,
  drag-and-drop, filterable, **one-click refresh**.
- **Variance-first**: the eye is steered to what's off-plan.
- **Narrative attached to numbers** ("storytelling with data") — Storyboards add
  AI commentary *"explaining why revenue dipped or expenses spiked,"* so the report
  *says something*, it isn't a data dump.

## 4. FP&A Genius — the insight engine (three functions, verified)
1. **Insights** — scheduled + instant analysis: trend ID, **variance analysis**,
   predictions, **Budget-vs-Actual** and **Forecast-vs-Actual**.
2. **Storyboards** — 2 clicks → presentation-ready narrative + visuals.
3. **Chat** — plain-English Q&A answered **exclusively from the company's own
   data**. Verified example questions: *"How is our revenue trending vs last
   year?"*, *"Which customers drove our revenue variance to budget last month?"*
- The grounding (only real, consolidated data) + NLP explaining the **"why"** (e.g.
  a travel-spend spike linked to a sales initiative) is what makes it trustworthy.

---

## 5. What we already do right (alignment — don't rebuild)

Our Phase 13 stack maps onto Datarails' patterns more than expected:

| Datarails pattern | Our existing equivalent | Status |
|---|---|---|
| Dashboard + KPI widgets | `design_system.py` `kpi()` + `build_dashboard()` (02 · Prehľad) | ✅ have |
| Narrative next to numbers | dashboard **Postrehy** insight formulas | ✅ have (basic) |
| FP&A Genius **Chat** (grounded NL Q&A) | **Gemini sidebar** (13g), grounded in live KPIs + Postrehy | ✅ have |
| One-click **refresh** / scheduled Insights | **Apps Script triggers** (13g, nightly/weekly briefing) | ✅ have |
| Version / audit trail | **Denník journal** append-only snapshots (13g) | ✅ have |
| Board-ready, branded look | `design_system` palette + clean canvas + `fit()` | ✅ have |

**The gaps are structural, not cosmetic** — and they're the high-value bit.

---

## 6. What we should ADOPT (the concrete design spec)

Ranked by value-per-effort; each maps to a specific script.

### A. Budget vs Actual vs Variance — the #1 missing pattern  ⭐
Today `LEDGER_12M` and `MARGIN` capture **actuals only**. Add a **Plán** input next
to actuals and compute **Odchýlka € / %** with RAG + a plain-language "why" — this
is literally Datarails' spine.
- `build_pack.py` `build_ledger()`/`build_margin()`: add `Plán` column per line +
  `Odchýlka €`/`Odchýlka %` + RAG conditional formatting on variance.
- `build_dashboard()`: add variance KPIs (*Tržby vs plán*, *Odchýlka nákladov*) and
  upgrade a Postreh to a **variance narrative**:
  *"Tržby €X — o 12 % POD plánom, ťahá to nápojový predaj."*
- `pack_spec.py`: add `plan_label` term + metrics `variance`, `variance_pct` to
  `MODULE_METRICS`.

### B. A normalized data backbone (the dimensional / DR-Formula lesson)  ⭐
Our wide 12-month layout is friendly for entry but rigid to re-slice. Add one
hidden **`Dáta`** sheet, long format:
`dátum · kategória · položka · scenár(Plán/Skutočnosť) · suma`. The dashboard then
rolls up with **`SUMIFS`** keyed on those dimensions — our offline equivalent of a
DR Formula's *timeframe × scenario × account* filter. Kills fragile cell anchors,
makes new cuts trivial, and gives the Gemini sidebar clean tagged rows.
- *SME caveat:* keep the friendly entry sheets as the face; `Dáta` is the engine
  behind them. Pilot on **one** vertical first.

### C. Drill-down by hyperlink (cheap, high-trust)
Each dashboard KPI tile → `HYPERLINK` to its source cell/sheet. Datarails
drill-down, offline, in ~10 lines of `build_dashboard()`.

### D. Board-ready report page (Storyboard analog)
Formalise a **print-ready one-pager**: set `print_area`, branded report header
(new `design_system.report_header()`), KPIs + variance narrative + one chart.
*"A page the owner can hand to the bank."*

### E. Storytelling upgrade (FP&A Genius parity, offline)
Make Postrehy *plan-aware*: every insight = **number → vs plan/last period → why →
action**. Feed the same plan-vs-actual context into the sidebar's
`afBuildContext()` (13g) so the AI answers like Genius **Chat**.

### F. In-cell micro-trends
A `REPT("▮", …)` mini-bar / 12-month sparkline per line — trend at a glance, zero
chart overhead, fits the offline `.xlsx` ethos.

---

## 7. Honest constraints (don't over-promise)
- We **cannot** (and shouldn't) replicate a live multi-file cloud warehouse in one
  offline `.xlsx` — our buyers are micro-SMEs, not finance teams. We **emulate the
  patterns** (layer separation, dimensions via SUMIFS, plan-vs-actual, narrative,
  grounded AI) at single-file scale. That's the right altitude.
- Datarails is enterprise FP&A at enterprise price. Our edge = the *same thinking*
  in a one-off, no-SaaS, per-trade pack. Position as **"FP&A-grade thinking for a
  corner shop,"** never "a Datarails clone."

## 8. Recommended next phase
**Phase 13i — "FP&A-grade" pack upgrade (code):** implement §6A (Budget vs Actual +
variance) + §6C (drill-down) + §6E (plan-aware Postrehy & sidebar context) on **one
pilot vertical** (`hospitality_sk`), validate, then roll the pattern through the
generic builder so every queued pack inherits it. §6B (normalized backbone) as a
follow-on once the variance pattern is proven. Keep one language; keep the
legibility + validation gates.

## Sources (re-verify live before listing)
- KB · Flex add-in: https://support.datarails.com/hc/en-us/articles/8236849348381-2-2-Flex-the-Excel-Add-In
- KB · DR Formulas (3-part): https://support.datarails.com/hc/en-us/articles/8240921388573-2-3-Datarails-Formulas
- KB · Connect formulas + drill-down: https://support.datarails.com/hc/en-us/articles/12624521414940-Creating-Formulas-in-Datarails-Connect-A-Step-by-Step-Guide
- KB · Dashboards/widgets: https://support.datarails.com/hc/en-us/articles/8884140838941-3-3-Dashboards-Creating-new-widgets
- FP&A Genius: https://www.datarails.com/solutions-fpna-genius/ · press: https://www.prnewswire.com/news-releases/datarails-announces-full-rollout-of-fpa-genius-the-chatgpt-for-the-cfos-office-301880753.html
- Financial dashboards for FP&A: https://www.datarails.com/financial-dashboards-for-fpa-professionals/
- Budget variance analysis guide: https://www.datarails.com/budget-variance-analysis-guide/
- 3rd-party reviews: https://www.cubesoftware.com/blog/datarails-reviews · https://www.f9finance.com/datarails/ · https://www.cfoshortlist.com/vendors/datarails
