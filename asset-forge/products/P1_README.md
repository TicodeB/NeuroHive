# P1 — Café / Restaurant Compliance Pack ⭐ (FLAGSHIP)

**Product file:** `P1_Cafe_Restaurant_Compliance_Pack.xlsx` (8 sheets, EN/SK)
**Preview file:** `P1_DEMO_Cafe_Restaurant_Compliance_Pack.xlsx` (watermarked, sheet-protected)
**Build:** `python3 scripts/build_p1_compliance_pack.py` · Version v1.0 · 30/05/2026
**Price (locked, Phase 8):** **€34** · **Platform:** Lemon Squeezy (primary) / Gumroad (fallback)
**DB product id:** 1 · **Bundled assets (ids):** 1, 2, 3, 4, 5, 16, 17

---

## What this is

The hospitality-first flagship from the ASSET-FORGE roadmap (Phase 9 build target).
One workbook that turns an EHO inspection from dread into a one-folder answer. All
**7 bundled assets are MUST across all 5 hospitality business types** (café, restaurant,
bar, B&B, hotel) — the legally-forced compliance floor, not optional nice-to-haves.

### Sheets
| # | Sheet | Asset (DB id) | Legal basis |
|---|-------|---------------|-------------|
| 00 | Start Here / Začnite tu | — | how-to + legal map |
| 01 | HACCP FSMS | 1 | Reg. (EC) 852/2004 |
| 02 | Allergen Matrix & Menu Declaration | 2 | Reg. (EU) 1169/2011 |
| 03 | Temperature Monitoring Log | 3 | 852/2004 (HACCP CCP) |
| 04 | Cleaning & Sanitation Schedule | 4 | 852/2004 (GHP) |
| 05 | Supplier & Delivery Traceability Log | 5 | 852/2004 / 178/2002 |
| 06 | H&S Risk Assessment & Safety Statement | 16 | Safety, Health & Welfare at Work Act 2005 |
| 07 | Fire Safety Register & Checks Log | 17 | Fire Services Acts 1981 & 2003 |

### Built-in logic (not just blank tables)
- **Allergen matrix**: 14 statutory EU allergens × menu items; conditional formatting flags
  `Y` (contains → red) and `T` (traces → amber); dropdown data-validation.
- **Temperature log**: auto `Pass?` (OK/CHECK) from reading vs target, direction-aware
  (cold units ≤ target, hot units ≥ target); CHECK highlighted red.
- **Cleaning schedule**: `COUNTA` day-tick roll-up (Done /7).
- **H&S**: risk rating = Likelihood × Severity with Low/Med/High colour bands.
- **Fire register**: `Status` auto-flags OVERDUE / DUE SOON / OK from the next-due date.
- **Traceability**: reject rows highlighted; EU comma-thousands on quantity.

### EU conventions applied
Metric units (°C, kg, minutes) · DD/MM/YYYY date cells · comma thousands separator ·
Ireland/EU regulatory references.

### Bilingual (EN / SK)
Every sheet ships parallel English + Slovak headers, instructions and guidance notes
(per the AGENTS.md binding rule and `deliverables/asset_glossary_EN_SK.md`).
⚠️ Before public launch route the Slovak through a native editor (the `/slovak` skill is
not installed here) — see handover standing add-on.

---

## Listing copy (draft — re-verify fees at listing time)

### English
**Café & Restaurant Compliance Pack — pass your EHO inspection with one folder**

Everything an Irish/EU food business is legally required to keep — HACCP, allergens
(all 14), temperature logs, cleaning schedule, supplier traceability, health & safety
statement and fire register — in one bilingual (EN/SK) Excel workbook. Pre-built with
sample rows, dropdowns and automatic pass/fail flags. Fill the amber cells, print or
keep on screen, and walk into any inspection with your records in order.

- ✅ 7 statutory records in one file (Reg. 852/2004 · 1169/2011 · Fire Acts · SHWWA 2005)
- ✅ Smart allergen matrix + auto temperature & fire-due flags
- ✅ Works in Excel, Google Sheets and LibreOffice — no subscription, no login
- ✅ English + Slovak throughout

*Template only — not legal advice. Adapt to your premises.*

### Slovenčina
**Súbor pre súlad pre kaviarne a reštaurácie — obstojte pri kontrole hygieny s jedným súborom**

Všetko, čo musí prevádzka s potravinami zo zákona viesť — HACCP, alergény (všetkých 14),
záznamy teplôt, harmonogram čistenia, vysledovateľnosť dodávateľov, bezpečnostné
vyhlásenie BOZP a register požiarnej ochrany — v jednom dvojjazyčnom (EN/SK) zošite
Excel. Pripravené so vzorovými riadkami, rozbaľovacími zoznamami a automatickými
upozorneniami. Vyplňte oranžové bunky a na kontrolu prídete s poriadkom v záznamoch.

- ✅ 7 zákonných záznamov v jednom súbore
- ✅ Inteligentná matica alergénov + automatické upozornenia na teploty a termíny
- ✅ Funguje v Exceli, Google Sheets aj LibreOffice — bez predplatného
- ✅ Kompletne v angličtine aj slovenčine

*Šablóna — nie je právne poradenstvo. Prispôsobte svojej prevádzke.*

---

## Launch checklist status (brief §4 / MONETIZATION_BRIEF §4)
- [x] Product workbook built (full, editable)
- [x] Watermarked read-only demo built (sheet-protected, "DEMO — not for resale" banner)
- [x] Bilingual EN/SK copy (headers, instructions, listing draft)
- [x] Price + platform locked (€34, Lemon Squeezy)
- [ ] Preview images (export sheet screenshots — do at listing time)
- [ ] Slovak copy native-editor pass before public launch
- [ ] Licence text + EU 14-day-withdrawal waiver checkbox (LS provides)
- [ ] Re-verify platform fees live at listing time (figures dated 30/05/2026)

## Bundle path
Standalone €34 → **Hospitality Pro Bundle** (+P2 Operations & GP) €69 →
cross-sell into **Compliance Everything** kit €149.
