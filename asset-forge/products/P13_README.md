# P13 — Compliance Gap-Analysis & Mock-Audit *(Lite)* ⭐ (FLAGSHIP)

**Product file:** `P13_Compliance_Gap_Analysis_Mock_Audit.xlsx` (5 sheets, EN/SK)
**Preview file:** `P13_DEMO_Compliance_Gap_Analysis_Mock_Audit.xlsx` (locked; dedicated "DEMO Preview" notice sheet)
**Build:** `python3 scripts/build_p13_gap_analysis_pack.py` · Version v1.1 · 30/05/2026
**Price:** **€29 launch test** — *sell as much as the market takes* (§41, Samuel 30/05/2026); A/B €19 → €29 → €39 and hold at the conversion-maximising point. · **Platform:** Lemon Squeezy (primary) / Gumroad (fallback)
**DB product id:** 13 · **Bundled assets:** `CA:1` (Clause-by-clause Gap-Analysis Tool) · `CA:2` (Mock-Audit / Readiness Self-Assessment)
**Audience:** operator · **Standards touched:** ISO 9001 · ISO 22000 · HACCP · BRCGS · IFS · FSSC 22000 (generic structure)

---

## What this is

The Phase-12 bonus-track flagship. It answers compliance's highest-willingness-to-pay
question — **"will I pass?"** — in about 15 minutes, then routes the buyer to the deeper
per-standard kit that closes their gaps (P14–P18).

**"Lite"** = one *generic* clause set across the common management-system spine (Annex SL
high-level structure shared by ISO 9001 / 14001 / 45001 / 22000, plus the food-safety floor
of HACCP / 852/2004 / 1169/2011). No per-standard depth — that fuller, per-standard version
becomes the **scoring engine reused inside every paid kit (P14–P18)**: build once, sell many.

> **Framing (brief §15):** an **audit-ready readiness check that satisfies a TÜV-style
> certifier auditing you to ISO / HACCP / BRCGS / IFS** — never a "TÜV template". TÜV is a
> *certification body*, not a standard.

### Sheets
| # | Sheet | Asset | Purpose |
|---|-------|-------|---------|
| 00 | Start Here / Začnite tu | — | how-to + what-it-is + legal disclaimer |
| 01 | Gap Analysis / Analýza | CA 1 | 26 clauses × 8 sections; Status → auto Conf.% + Priority |
| 02 | Mock Audit / Skúška | CA 2 | 20 "could you show…?" questions; auto readiness % |
| 03 | Readiness / Pripravenosť | — | combined % + RAG verdict + section breakdown + open-gap counts |
| 04 | Next Steps / Ďalšie kroky | — | sector → matching paid kit (P14–P18) upsell routing |

### Built-in logic (not just blank tables)
- **Gap analysis**: per-clause Status dropdown (Conform / Partial / Not in place / N/A) →
  auto **Conformance %** (100 / 50 / 0 / excluded) and auto **Priority** (HIGH for *Not in
  place*, MEDIUM for *Partial*); RAG conditional formatting; non-food rows (section 8F) set
  to N/A self-exclude.
- **Section roll-up**: `AVERAGEIFS` per section on the dashboard, RAG-banded.
- **Overall conformance**: `AVERAGE` of applicable clause scores (blanks/N-A ignored).
- **Mock audit**: Yes / Partly / No → 100 / 50 / 0 %, averaged to a readiness score.
- **Overall readiness**: mean of gap-analysis % and mock-audit % (handles either side blank).
- **Verdict ("will I pass?")**: RAG bands — 🟢 ≥85% · 🟠 60–84% · 🔴 <60% — formula-driven.
- **Open-gap counters**: live `COUNTIF` of HIGH and MEDIUM gaps.

### EU conventions applied
DD/MM/YYYY date cells · metric framing · percentages for all scores · Ireland/EU
regulatory references (852/2004, 1169/2011, Amd 1:2024 climate action).

### Bilingual (EN / SK)
Every sheet ships parallel English + Slovak titles, instructions, clause requirements,
questions and verdict text (AGENTS.md binding rule + `deliverables/asset_glossary_EN_SK.md`).
⚠️ Route the Slovak through a native editor before public launch (the `/slovak` skill is not
installed here).

### File integrity (v1.1 fix)
v1.0 produced an Excel "we found a problem with content" error. Two root causes, both fixed:
1. **Sheet name > 31 chars** ("02 · Mock Audit · Skúšobný audit" = 32) — Excel's hard limit;
   shortened to "02 · Mock Audit · Skúška". The builder now `assert`s every tab ≤ 31 chars.
2. **DEMO used `insert_rows()`** — openpyxl shifts cell values but not merged-cell ranges, so
   the watermarked preview ended up with overlapping merges. Replaced with a non-destructive
   dedicated **"DEMO Preview · Ukážka"** notice sheet + read-only protection.
Both files now validate: all XML well-formed, all tab names ≤ 31, zero merged-range overlaps.

---

## Listing copy (draft — re-verify fees at listing time)

### English
**Compliance Readiness Check — "Will I pass my audit?" in 15 minutes**

A bilingual (EN/SK) Excel tool that scores how audit-ready you really are. Set a status
against each requirement, answer 20 mock-audit questions, and the workbook auto-calculates
your conformance %, a traffic-light verdict, and your highest-priority gaps — across the
structure shared by ISO 9001, ISO 22000, HACCP, BRCGS, IFS and FSSC 22000. Then it points
you to the exact ready-made kit that closes those gaps.

- ✅ Clause-by-clause gap analysis with automatic scoring
- ✅ 20-question mock-audit self-assessment
- ✅ Traffic-light "will I pass?" verdict + section breakdown
- ✅ Works in Excel, Google Sheets and LibreOffice — no subscription, no login
- ✅ English + Slovak throughout

*Template only — not legal advice nor a guarantee of certification. Audit-ready support for a
TÜV-style certifier auditing you to ISO / HACCP / BRCGS / IFS — not affiliated with TÜV.*

### Slovenčina
**Kontrola pripravenosti na audit — „Prejdem auditom?“ za 15 minút**

Dvojjazyčný (EN/SK) nástroj v Exceli, ktorý ohodnotí, ako veľmi ste pripravení na audit.
Nastavte stav ku každej požiadavke, odpovedzte na 20 otázok skúšobného auditu a zošit
automaticky vypočíta % zhody, semaforový verdikt a vaše najdôležitejšie medzery — naprieč
štruktúrou spoločnou pre ISO 9001, ISO 22000, HACCP, BRCGS, IFS a FSSC 22000. Potom vás
nasmeruje na presný hotový balík, ktorý tieto medzery vyrieši.

- ✅ Analýza nedostatkov po jednotlivých bodoch s automatickým hodnotením
- ✅ Sebahodnotenie skúšobného auditu (20 otázok)
- ✅ Semaforový verdikt „prejdem?“ + rozpis po sekciách
- ✅ Funguje v Exceli, Google Sheets aj LibreOffice — bez predplatného
- ✅ Kompletne v angličtine aj slovenčine

*Šablóna — nie je právne poradenstvo ani záruka certifikácie. Podpora pripravenosti na audit
certifikačným orgánom (štýl TÜV) podľa ISO / HACCP / BRCGS / IFS — bez väzby na TÜV.*

---

## Launch checklist status (brief §4 / MONETIZATION_BRIEF §4, §7)
- [x] Product workbook built (full, editable) — **v1.1, Excel-valid**
- [x] Watermarked read-only DEMO built (non-destructive notice sheet + sheet protection)
- [x] File integrity verified (XML well-formed · tab names ≤31 · no merged-range overlaps)
- [x] Bilingual EN/SK copy (titles, instructions, clauses, questions, listing draft)
- [x] Price set in DB (€29 launch test, paid) + platform (Lemon Squeezy)
- [x] Real scoring logic verified (Conf.% / Priority / readiness / RAG verdict)
- [ ] Preview images (export sheet screenshots at listing time — no headless renderer in env)
- [ ] Price experiment: list at €29, test €19/€29/€39, hold at the conversion-maximising point
- [ ] Slovak copy native-editor pass before public launch
- [ ] Licence text + EU immediate-delivery / 14-day-withdrawal waiver (LS provides)

## Funnel / bundle path (MONETIZATION_BRIEF §7 value-ladder)
**Entry-priced flagship (€29)** → upsell to the matching per-standard kit:
- Hospitality (HACCP) → **P14** €49
- Food mfg ISO 22000 / FSSC 22000 → **P15** €99
- Food mfg BRCGS / IFS → **P16** €89
- Non-food mfg ISO 9001 → **P17** €79
- FSSC v6→v7 transition → **P18** €49
- Auditors / consultants → **P19 / P20** from €149

Top-of-funnel discovery is now served by the cheaper à-la-carte module **P21** (Gap-Analysis
only, €19) or a future cut-down free teaser — P13 itself earns from the first sale.
