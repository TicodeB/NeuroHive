# Non-spreadsheet artifacts — Gamma / Canva generation manifest

The `.xlsx` workbooks are generated in-repo (openpyxl + `design_system.py`). The
polished **decks, documents and PDFs** are produced via the **Gamma / Canva MCP
servers** (per product decision) and exported alongside the pack. This manifest
records exactly what to generate so each artifact is reproducible.

## Generated

| Artifact | Type | Tool | Status |
|----------|------|------|--------|
| Boutique Hotel Setup Guide | PDF document | Gamma `generate` (format=document, exportAs=pdf) | ✅ generated — see `artifacts_manifest.json` for the Gamma URL / export link |

## To generate (prompts ready)

Each entry is a ready-to-run Gamma/Canva prompt. Run with the LEANTA brand theme;
export pptx/docx/pdf as noted; save the export link into `artifacts_manifest.json`.

### Investor Pitch Deck (`pptx`, Gamma `generate`, format=presentation)
> A 12-slide investor pitch for a 4-star, 24-room boutique hotel seeking €600k.
> Cover the opportunity, market (ADR €135, occupancy 72%, RevPAR €97), the design-
> led + direct-booking-first positioning, the €1.09m revenue model and 3-scenario
> P&L, the €600k uses-vs-sources funding stack (founder equity incl. SURE refund,
> LEO grant, term loan, MFI), debt service & DSCR, the 15-KPI operations dashboard,
> the 100-day launch plan, the team, and the ask. Audience: investors/lenders.

### Org Chart (`pptx` / diagram, Gamma `generate` or Canva)
> A one-page org chart for a 24-room boutique hotel (~10 FTE): General Manager at
> top; Front Office (Front Office Manager → Receptionists), Housekeeping (Head
> Housekeeper → Room Attendants), F&B (Head Chef → Chef de Partie/KP, Bar/F&B
> Attendants), Facilities (Maintenance). Clean, branded, print-ready.

### Job Description Library + Recruitment Ad + Interview Guide (`docx`, Gamma, format=document)
> A recruitment document set for a boutique hotel: full job descriptions for GM,
> Front Office Manager, Receptionist, Head Housekeeper, Room Attendant, Head Chef,
> F&B/Bar Attendant, Maintenance (purpose, duties, requirements, KPIs); a reusable
> job-advert template; and a structured interview scoring guide (competencies,
> 1–10 scale, scenario questions). Aligns with the Phase-4 payroll budget.

### Branded Checklists (`pdf`, Gamma/Canva)
> Print-ready Daily / Weekly / Monthly operations playbooks, a 100-Day Scorecard,
> and a Contingency Playbook — one page each, on-brand, derived from the Phase-5
> and Phase-6 workbooks.

### Grant Narrative Documents — English set (`docx`/`pdf`, Gamma, format=document)
> The prose answers for the LEO, Microfinance Ireland, Fáilte Ireland and SURE
> applications, formatted to each body's real headings, pulling the worked hotel
> figures. One document per body.

### Grant Narrative Documents — Slovak set (`docx`/`pdf`, Gamma, language=sk)
> Slovenské naratívne dokumenty k žiadosti pre ÚPSVaR (§49) a eurofondy —
> podnikateľský plán a finančný plán podľa oficiálnej štruktúry.

## Notes
- Gamma outputs are hosted and editable in the Gamma editor; the `exportUrl` from a
  generation is signed and **expires in ~1 week** — download promptly and store the
  file, or re-export.
- These are one-off generations, not committed build scripts. If reproducible,
  in-repo generation is later required, revisit local python-pptx/python-docx.
