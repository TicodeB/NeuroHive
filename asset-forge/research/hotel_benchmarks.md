# Boutique Hotel — benchmark reference (cited)

Quantified target benchmarks for the 4-star boutique-hotel pack, researched live
(2024–2025) and seeded into the `startup_benchmarks` table
(`scripts/seed_startup_benchmarks.py`). The Phase-0 workbook renders these as a
"benchmark band" and the Assumptions sheet cites them.

| Metric | Low | Typical | High | As of | Source |
|--------|-----|---------|------|-------|--------|
| ADR (4★) | €127 | €144 | €241 | 2024 | Fáilte Ireland Hotel Survey (4★ €143.50–€144.49; county range €127–€241) |
| Occupancy (4★) | 60.2% | 70% | 74.1% | 2024 | Fáilte Ireland Hotel Survey (60.2% Dec → 74.1% Nov) |
| RevPAR (4★) | €86.42 | €97 | €107.07 | 2024 | Fáilte Ireland Hotel Survey (€86.42 Dec → €107.07 Nov) |
| Labour cost (% revenue) | 25% | 31% | 35% | 2024 | Hospitality norm 25–35%; US long-run 31.2% (Mandelbaum/CBRE; altametrics) |
| F&B cost (% F&B revenue) | 18% | 28% | 35% | 2023 | USALI; academic luxury 17.86% (US)–23.87% (Asia) |
| Rooms dept cost ex-payroll (% rooms rev) | 8% | 12% | 18% | 2023 | USALI rooms departmental expense |
| GOP margin (% revenue) | 30% | 36% | 38.3% | 2025 | HotelData Q4-2025 FY GOP 38.3%; academic luxury 33.2–36.7% |

## How the pack's seed assumptions sit against the band
- ADR €135 → within band, slightly below the 4★ typical €144 (conservative for a
  regional boutique).
- Occupancy 72% → within band (Nov 74.1%, annualised ~70%).
- RevPAR €97 → equals the typical (between winter €86 and autumn €107).
- Payroll 30%, F&B cost 30%, rooms cost 10% → all inside the published bands.
- Resulting GOP margin lands ~30–35%, consistent with the 36–38% sector band
  (a new boutique ramping in year 1 sits at the lower edge — expected).

## Sources
- Fáilte Ireland Hotel Survey, Nov & Dec 2024 — failteireland.ie/Research-Insights
- altametrics.com — hospitality labour-cost benchmark
- HotelData Q4-2025 Labor/Profit report — hoteldata.com
- Academic: "Importance of F&B operation in luxury hotels" (PolyU IRA)
- Cross-checks: Northern Ireland Hotels Federation 2025; Savills Ireland Hotel Market

> Bands are decision-aids, not guarantees. Re-verify current-year figures with the
> latest Fáilte Ireland survey before relying on them for a live application.
