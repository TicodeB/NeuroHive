# P2 · SK Premium — Prevádzka a marža pre gastro

**Premium-Pack track pilot (Phase 13b).** A Slovak-only, premium re-skin of the
P2 Hospitality Operations & GP Bundle — built to prove the new look beats the
old "90s" spreadsheets.

- **File:** `products/P2_SK_Hospitality_Premium.xlsx` (9 sheets, Slovak only)
- **Builder:** `scripts/build_p2_sk_premium.py` (re-runnable)
- **Design system:** `scripts/design_system.py` (reusable — every future pack inherits it)

## What's new vs the old build
| Old (`build_p2_operations_bundle.py`) | New (this pilot) |
|---|---|
| Calibri 9pt, heavy grey grid on every cell | gridlines off, hairline tables, whitespace margin |
| EN \| SK crammed into one cell | clean **single-language Slovak** |
| No dashboard, no insights | **02 · Prehľad** — KPI tiles + formula-driven insights |
| No planner | **01 · Denný plán** — daily priorities, schedule, open/close |
| Ad-hoc styling per sheet | one shared **design system** (`DS` + `Theme`) |

## Sheets
`00 Metóda` (method + start here) · `01 Denný plán` · `02 Prehľad` (dashboard) ·
`03 Cash flow` · `04 Marža` · `05 Zásoby` · `06 Zmeny` · `07 Tržby` · `08 Školenia`

## The dashboard (the headline)
KPI tiles (annual revenue, gross profit, net profit, closing cash, avg margin,
labour %) pull **live** from sheets 03–07. The **Postrehy** (Insights) block
writes plain-Slovak sentences ("Podiel miezd: 38,0% — NAD cieľom 35 %…") that
update as the owner fills in their numbers. RAG conditional formatting flags
negative profit and over-target labour %.

## Validation
XML well-formed · openpyxl reload OK · zero merged-range overlaps · all tab
names ≤31 chars · every dashboard anchor resolves to the correct source cell.
(LibreOffice/soffice is non-functional in this sandbox → validated via openpyxl
+ zip/XML parse, not rendering.)

## ⚠️ Before any public listing
- **Slovak text is draft-grade** for this build proof → native-editor pass required.
- **Capture preview screenshots** from Excel/Google Sheets (no headless renderer here).
- This is the **Tier-0 offline** edition; the Google Sheets "Pro" edition
  (Apps Script automations + optional Gemini sidebar) is a later sub-phase.
