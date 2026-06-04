# Boutique Hotel · 4-Star Turnkey Startup Pack

A complete, formula-driven toolkit that takes an entrepreneur from idea to a
profitable **4-star, 20–30-room boutique hotel** across 7 phases. Every workbook is
a real, validated `.xlsx` — no mockups: figures are linked to an editable
**Assumptions** sheet, dashboards use 🟢🟡🔴 traffic lights, and worked sample data
is included so the calculations prove out the moment you open the file.

## What's included

| File | Phase | What it does |
|------|-------|--------------|
| `00_Market_Validation.xlsx` | 0 | TAM/SAM/SOM demand sizing, competitor matrix, weighted location score, go/no-go gate |
| `01_Business_Plan.xlsx` | 1 | Exec summary, service definition, **3-scenario P&L** (Low/Base/High) with GOP margin, go/no-go gate |
| `02_Capital_Raising.xlsx` | 2 | Uses vs sources, debt-service (PMT), **12-month cash-flow with occupancy ramp**, runway & DSCR |
| `03_Procurement.xlsx` | 3 | Vendor master, **RFQ comparison (auto-flags lowest quote)**, PO register vs capex budget |
| `04_Team_Building.xlsx` | 4 | Staffing plan & **payroll budget** (PRSI + pension on-cost), recruitment + interview tracker |
| `05_Operations.xlsx` | 5 | **Daily data-entry sheet** → **live 15-KPI dashboard** with status + headline scorecard + trend chart |
| `06_Launch_100Days.xlsx` | 6 | Launch timeline, **100-day scorecard**, contingency triggers, scale-up go/no-go |

Each file also carries its own orange-input **Assumptions** sheet — the single
source of truth (rooms, ADR, occupancy, cost ratios, capex breakdown, funding mix).
Change a number there and every linked figure updates.

## The 15 operations KPIs (Phase 5)
Occupancy · ADR · RevPAR · GOPPAR · Guest NPS · Labour % · F&B % · Repeat guest % ·
ALOS · Direct-booking % · Room turnaround (min) · Maintenance response (hrs) ·
Staff turnover % · Complaints / 100 stays · Payment collection %.
Each has a target and 🟢 On target / 🟡 Watch / 🔴 Action threshold.

## Headline model (editable seed assumptions)
- 24 rooms · ADR €135 · occupancy 72% → **RevPAR €97**
- Total revenue ≈ **€1.09m/yr** · capex **€600k** (leased, fit-out led)
- Funding stack: founder equity (incl. SURE refund) + LEO grant + term loan + MFI

> Figures are **seed assumptions** sense-checked against published Irish 4-star/
> boutique benchmarks. Replace the orange cells with your own quotes and verified
> local data before relying on them. Sources are cited on each Assumptions sheet.

## How to customise
1. Open any phase file and edit the **Assumptions** sheet (orange cells only).
2. Work the phases in order — each ends with a go/no-go gate.
3. For funding, pair this with the **grant-application pack** in
   `products/templates/grant-applications/` (LEO, Microfinance Ireland, Fáilte
   Ireland, SURE tax refund, and Slovak ÚPSVaR/eurofondy templates).

## Validation
Run the Definition-of-Done gate from the repo root:

```
python3 products/validation/test_all_formulas.py
```

## Tiers
T2 Starter €149 · T3 Full €599 · T4 Concierge €1,699.
