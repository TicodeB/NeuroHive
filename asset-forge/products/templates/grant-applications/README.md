# Grant & Funding Application Pack (reusable · EN + SK)

A standalone, **cross-vertical** set of funding-application workbooks, structured to
mirror the **real published application forms** of each body. Every figure links to
an embedded **Assumptions** sheet (the boutique-hotel worked example), so the
expenditure and cash-flow tables are auto-calculated, not hard-coded. Swap the
Assumptions for any other business and the applications re-compute.

## Workbooks

| File | Body | What it produces |
|------|------|------------------|
| `IE_LEO_Priming_Business_Expansion.xlsx` | **Local Enterprise Office** | Full application mirroring the LEO e-form (applicant/legal, background, product, market & competitors, **Year-1 eligible expenditure** auto-linked, 50%-match grant calc with €80k/€150k cap + €15k/FTE), attachments checklist |
| `IE_Microfinance_Ireland_Loan.xlsx` | **Microfinance Ireland** | Business-plan questionnaire + **month-by-month cash-flow forecast** (required >€5,000) with runway check |
| `IE_Failte_Ireland_Capital.xlsx` | **Fáilte Ireland** | Two-stage tourism capital-grant outline: eligibility/State-Aid screen, project rationale, capital schedule (linked), match-funding |
| `IE_SURE_Tax_Refund.xlsx` | **Revenue (SURE)** | Eligibility gate, **refund calculator** (up to 41% of capital invested; reclaims PAYE tax over the prior 6 years; €140k/yr cap), claim process + documents |
| `SK_UPSVaR_Eurofondy_Podnikatelsky_Plan.xlsx` | **ÚPSVaR / eurofondy (SK)** | Slovak podnikateľský plán (kap. 1–5) + **Finančný plán** (5-ročný výhľad, povinná príloha) + §49 kalkulácia nákladov + prílohy & čestné vyhlásenia |

## The funding stack (how they combine for the ~€600k hotel)

| Source | Type | Indicative € | Notes |
|--------|------|-------------|-------|
| Founder equity incl. **SURE refund** | Equity | 180,000 | SURE returns up to 41% of invested capital as a tax refund |
| **LEO** Priming / Business Expansion | Grant | 80,000 | 50% match of eligible non-salary costs |
| **Bank / SBCI** term loan | Debt | 300,000 | Debt-service modelled in Phase 2 |
| **Microfinance Ireland** | Debt | 40,000 | €2k–€50k; apply via LEO for −1% rate |
| (large projects) **Fáilte Ireland** | Grant | 200k+ | Two-stage capital scheme, alternative to the above |

## Eligibility & caps at a glance
- **LEO Priming**: micro-enterprise (≤10 staff), first 18 months; 50% / max €80k (€150k exceptional).
- **LEO Business Expansion**: growth phase after 18 months; same caps; 12-month gap after Priming.
- **Microfinance Ireland**: €2,000–€50,000; business plan + cash-flow for loans >€5,000.
- **SURE**: mainly-PAYE prior 4 yrs; new ordinary shares; full-time within 6 months; hold 4 yrs.
- **Fáilte Ireland**: tourism capital projects, typically €200k+, two-stage, State-Aid rules.
- **ÚPSVaR §49 (SK)**: SZČ run ≥2 yrs; 60% paid after 12 months, balance after 24.

## Sources
localenterprise.ie · microfinanceireland.ie · failteireland.ie · revenue.ie (IT15) /
sure.gov.ie · upsvr.gov.sk · eurofondy.praca.gov.sk. Figures are seed assumptions —
verify current limits and terms with each body before submitting.

## Build & validate
```
python3 scripts/grant_build.py
python3 products/validation/test_all_formulas.py
```
