# Beautification & Competitor Intelligence — Premium Pack Track (Phase 13a)

**Date:** 30/05/2026 · **Owner:** Samuel · **Branch:** `claude/cool-planck-rYR4I`
**Purpose:** Samuel's brief — *"find the GitHub repos that are sources of beautiful,
systematically grouped premade spreadsheet packs (with action scripts/automations,
per-industry), find the winners, see how they operate, and make ours even better.
Our spreadsheets look like the 90s — beautify them. Premium feel, great formulas,
automations, insights, maybe an embedded bot/AI. No SaaS-subscription hassle: you're
a butcher → you get your pack; a retailer → yours; etc. Each pack in ONE language
only (clean SK, clean CS, clean DE, HU, PL, EN), with industry jargon + a built-in
method and daily planner."*

> **Scope note (Samuel, 30/05/2026):** auditor/consultant packs are parked for LATER.
> This track is **operator-facing** premium packs.

---

## 1. THE HEADLINE FINDING (read this first)

**The commercial winners are NOT on GitHub.** GitHub hosts *free* template collections,
dashboard learning-projects and automation *snippets* — excellent as a **technique
and raw-material mine**, but almost none are polished, niche, sellable "packs."

The real money — the premium, industry-specific packs Samuel is describing — lives on
**Etsy, the Notion marketplaces, and Gumroad**. So the strategy splits cleanly:

| Source | What it actually gives us | How we use it |
|---|---|---|
| **GitHub** | VBA macros, Google Apps Script automations, dashboard layout patterns, finance formula sets (DCF/WACC/cashflow), bulk-data tooling | **Mine for technique** (formulas, automation patterns, dashboard structure). Check licences before reusing code. |
| **Etsy / Notion / Gumroad** | Proof of *demand*, *price points*, *niche framing*, and the *premium visual bar* buyers expect | **Mine for positioning** — what sells, at what price, with what design polish. |

**Implication:** we don't "fork a repo." We (a) steal the *design recipe* and *automation
patterns*, (b) encode them once into our build pipeline, then (c) stamp out
niche-specific, single-language packs — exactly the model Samuel described.

---

## 2. GITHUB — what's actually there (the technique mine)

Searched GitHub topics + repos. Representative finds (none are turn-key premium packs;
all are useful as ingredients):

- **`louiewee/Excel-BizFin-Templates-Projects`** — business & finance templates: Income
  Statement, Balance Sheet, Cash-Flow Statement, **Budget-vs-Actuals dashboards with
  variance visualisation**, DCF/WACC/Terminal-Value calculators. → *Mine: the finance
  formula spine and the budget-vs-actual dashboard pattern.*
- **`asmaklad/Excel_Tools`** — a suite of Excel templates for **automating tasks**. →
  *Mine: automation patterns.*
- **`NiveditaSureshK/HR-Analysis-DB-MSExcel`** — HR dashboard with **VBA macros** that
  show/hide cards and auto-clear filters. → *Mine: the interactive-dashboard-via-macro
  pattern (the "feels like an app" trick).*
- **`thabresh-s/Microsoft-Excel`** — basic template/dashboard collection (charts, gauges,
  tables). → *Mine: gauge/KPI-tile visuals.*
- GitHub **topics** to keep crawling: `excel-template`, `excel-dashboard`,
  `excel-automation`, `spreadsheet-automation`, `google-sheets-templates`,
  `small-business-tools`.

**Verdict:** GitHub = our **R&D parts bin**, not a competitor. The "winners" framing
Samuel used applies to the marketplaces below, not to GitHub.

---

## 3. THE MARKETPLACE WINNERS — how they operate (the model to beat)

What the best-selling operators actually do (Etsy / Notion / Gumroad evidence):

1. **Niche beats generic — hard.** Industry-specific templates (e.g. *Bakery Business
   Planner*, *Cottage Baker Income/Expense Tracker*) reportedly **convert ~40% better**
   than generic "small business" templates. This is the entire thesis behind Samuel's
   butcher / retailer / fruit-&-veg / abattoir / car-seller / airline / band / theatre split.
2. **They sell an outcome, not a grid.** Winners bundle: a clean client-facing dashboard,
   pre-built formulas (income/expense/profit, COGS, margins), category presets *in the
   buyer's language/jargon*, and a "how to use this" method page. Samuel's "method +
   daily planner built in" instinct matches the winning shape exactly.
3. **Pricing ladder (live, 30/05/2026 — re-verify at listing):**
   - Etsy single spreadsheet template: **€11–20** sweet spot (max conversions).
   - Notion **business** templates: **€45–185**; **finance/budget**: **€28–140**;
     wellness systems: up to **€140–370**.
   - Premium positioning: a €15–20 template replaces a €50–500 designer/consultant job —
     that's the value story buyers respond to.
4. **Bakery is a proven micro-niche** (multiple dedicated best-sellers: ingredient/cost
   tracking, recipe→sale traceability, market-fee expense categories) — a useful template
   for *how granular* a vertical pack should get.
5. **Format split:** winners ship **Google Sheets** (instant, shareable, automatable) and/or
   **Excel** (offline, no account). The Sheets editions are the ones that can carry live
   automations + AI; the Excel editions win the "no SaaS, no account, just open it" buyer —
   which is precisely Samuel's stated ethos.

---

## 4. THE "PREMIUM LOOK" RECIPE (this kills the "looks like the 90s" problem)

Good news: a premium spreadsheet aesthetic is **a finite, codifiable recipe** — and every
rule below is reproducible in our **openpyxl** build pipeline (or Sheets themes). This
becomes a reusable **design-system module** we apply to every pack.

**The recipe:**
1. **Limited palette — 2–3 colours only.** One primary (blue = trust/finance is the safe
   default), one accent, neutrals (soft grey/blue/green). Generate via Coolors/Adobe Color
   if no brand colours. *Encode as a named palette per pack/vertical.*
2. **Kill the grid.** Turn OFF default gridlines on client-facing tabs — the grey mesh is
   the #1 "90s" tell. Use whitespace as structure.
3. **Zebra striping** on long tables — a *very light* tint of the primary, not heavy lines.
4. **Typography:** one clean sans-serif (Lato / Montserrat / Poppins / Roboto). Titles
   **18–24pt bold**; body 10–11pt; consistent hierarchy.
5. **Dedicated dashboard / "report" tab** — a pristine, client-facing summary tab that
   *pulls* from raw-data tabs (protects raw data, looks like an app). This is the single
   biggest perceived-value lever.
6. **Minimalist charts** — few, clean, on-palette; KPI tiles/gauges for headline numbers.
7. **Set the theme FIRST**, before content, so colours/fonts/CF/charts inherit consistently.
8. **Section colour-coding** for legends/headings/data so the eye parses instantly.

**Action:** build `scripts/design_system.py` — a reusable openpyxl styling layer (palette,
fonts, header styles, zebra, gridline-off, KPI-tile helper, dashboard-tab scaffold) that
*every* pack builder calls. This is the one-time investment that makes all future packs
look premium by default. (Our current P1/P2/P13 builders predate this → they're the "90s"
files Samuel is reacting to; re-skinning them is the fastest visible win.)

---

## 5. AUTOMATIONS & "RUNNING YOUR BUSINESS FROM THE SHEET"

Two honest tiers, depending on format:

- **Excel (.xlsx, offline):** automation = **formula intelligence**, not code. Auto-rollups
  (`SUMIFS`/`AVERAGEIFS`), RAG conditional formatting, dropdown-driven status→score (we
  already do this in P13), auto-insight cells ("Your top cost is X (42%)", "Margin down 3pts
  vs last month"), data-validation guardrails. No macros (`.xlsm` scares buyers / AV flags).
- **Google Sheets edition:** unlocks **free Google Apps Script** — custom menus, sidebars,
  one-click month rollover, auto-invoice PDF, scheduled summaries. *No subscription.*

**Insights** ("gives you insights"): a dedicated **Insights** block on the dashboard tab —
formula-driven sentences that read like a tiny analyst (top cost, best day, slowest payer,
stock about to run out). Cheap to build, feels premium.

---

## 6. EMBEDDED AI / BOT — the honest feasibility verdict

Samuel: *"maybe we could embed a small bot or AI model."* Straight answer:

- ❌ **You cannot embed a live, offline AI model inside an `.xlsx` file.** A spreadsheet is a
  static document; there's no runtime. Anyone claiming otherwise is selling a cloud add-on.
- ✅ **Google Sheets + free Apps Script + Gemini (buyer's own free API key)** *can* give a
  real in-sheet **chatbot sidebar** ("ask your data a question"). Free to run, no
  subscription — but requires the Sheets edition and a one-time key paste.
- ⚠️ **Marketplace add-ons (SheetGPT, GPT-for-Sheets)** work but are third-party dependencies
  / quasi-subscriptions → **against Samuel's "no SaaS hassle" ethos.** Avoid as a core promise.
- ✅ **The pragmatic premium move:** ship (a) built-in **insight formulas** (feels smart,
  zero dependency) + (b) a **"Prompt Pack"** — copy-paste prompts the buyer drops into
  Claude/Gemini/ChatGPT to analyse their own exported data + (c) *optionally* the free Apps
  Script Gemini sidebar as a **bonus on the Sheets edition** for buyers who want it.

**Recommendation:** promise *insights* (real, built-in) now; offer the AI sidebar as an
optional Sheets bonus; never promise a magic offline embedded model.

**NotebookLM angle:** not a spreadsheet engine — irrelevant for *embedding*. But it (or
Claude) is genuinely useful to **generate the per-industry "Method" handbook + jargon
glossary** content that ships inside each pack. Use it as a content tool, not a feature.

---

## 7. STRATEGIC IMPLICATIONS → what this means for our build

1. **Single-language editions reverse our locked "Bilingual EN+SK" rule.** Samuel explicitly
   wants **one language per file** (clean SK / CS / DE / HU / PL / EN). This is a deliberate
   pivot, not a drift — recorded here; AGENTS.md bilingual rule must be amended for this track.
   *Native-quality translation per language remains non-negotiable (no machine-literal text).*
2. **Format decision gates everything** (automation + AI live on the Sheets side; "no
   account, just open it" lives on the Excel side). Likely answer: **ship both** — a clean
   offline `.xlsx` core + an optional Google Sheets "Pro" edition with automations/AI sidebar.
3. **Don't boil the matrix.** Verticals × languages × formats = hundreds of SKUs. **Pilot ONE
   cell first.** Strong recommendation: **re-skin our already-built, already-validated
   hospitality flagship (P1/P2) with the new `design_system.py`, in ONE language**, as the
   visual proof — this directly answers "looks like the 90s" with the least new surface area.
4. **Every pack's anatomy** (the winning shape) = `00 Start Here / Method` · `Daily Planner` ·
   `Dashboard (KPIs + Insights)` · `core operational tabs in the vertical's jargon` ·
   `Setup/Settings`. Standardise this skeleton, then localise + jargon-swap per vertical.
5. **Build order that compounds:** design-system module → re-skin one existing pack as proof →
   lock the pack skeleton → THEN spin up new verticals (butcher, retailer, …) and languages.

---

## 8. SOURCES

GitHub / technique:
- https://github.com/louiewee/Excel-BizFin-Templates-Projects
- https://github.com/asmaklad/Excel_Tools
- https://github.com/NiveditaSureshK/HR-Analysis-DB-MSExcel
- https://github.com/thabresh-s/Microsoft-Excel
- https://github.com/topics/excel-template · /excel-dashboard · /spreadsheet-automation · /small-business-tools

Marketplace winners / pricing / niche:
- https://www.insightagent.app/blog/best-selling-templates-etsy
- https://www.etsy.com/listing/4370151052/bakery-business-planner-template-google
- https://www.etsy.com/listing/4299814004/2025-bakery-income-expense-spreadsheet
- https://plrbizhub.com/most-profitable-notion-niches-to-sell/
- https://plrbizhub.com/best-selling-notion-template-designs-that-generate-real-sales-revenue/
- https://filtergrade.com/top-notion-templates-to-sell/

Premium-look recipe:
- https://danalyser.com/blogs/google-sheets/google-sheets-color-palette-4-theme
- https://exceloffthegrid.com/dashboard-color-palette/
- https://insightsoftware.com/blog/effective-color-schemes-for-analytics-dashboards/
- https://www.thebricks.com/resources/guide-how-to-make-google-sheets-look-aesthetic

AI-in-sheets feasibility:
- https://basescripts.com/build-a-spreadsheet-chatbot-with-google-apps-script-and-gemini
- https://workspace.google.com/marketplace/app/sheetgpt_ai_for_sheets_chatgptclaudegemi/1071108744264
- https://gptforwork.com/blog/how-to-use-ai-in-google-sheets

> Prices/fees/marketplace facts dated 30/05/2026 — **re-verify live at listing time** (AGENTS rule).
</content>
</invoke>
