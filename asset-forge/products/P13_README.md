# P13 — Compliance Gap-Analysis & Mock-Audit *(Lite)* ⭐ (FLAGSHIP · FREE lead magnet)

**Product file:** `P13_Compliance_Gap_Analysis_Mock_Audit.xlsx` (5 sheets, EN/SK)
**Preview file:** `P13_DEMO_Compliance_Gap_Analysis_Mock_Audit.xlsx` (watermarked, sheet-protected)
**Build:** `python3 scripts/build_p13_gap_analysis_pack.py` · Version v1.0 · 30/05/2026
**Price (Phase 11 strategy):** **€0** — FREE email-capture lead magnet · **Platform:** Lemon Squeezy (primary) / Gumroad (fallback)
**DB product id:** 13 · **Bundled assets:** `CA:1` (Clause-by-clause Gap-Analysis Tool) · `CA:2` (Mock-Audit / Readiness Self-Assessment)
**Audience:** operator · **Standards touched:** ISO 9001 · ISO 22000 · HACCP · BRCGS · IFS · FSSC 22000 (generic structure)

---

## What this is

The Phase-12 bonus-track flagship from the ASSET-FORGE roadmap. It answers the single
highest-willingness-to-pay question in compliance — **"will I pass?"** — in about 15
minutes, then routes the buyer to the paid kit that closes their gaps (P14–P18).

**"Lite"** = one *generic* clause set across the common management-system spine (Annex SL
high-level structure shared by ISO 9001 / 14001 / 45001 / 22000, plus the food-safety
floor of HACCP / 852/2004 / 1169/2011). No per-standard depth — that fuller, per-standard
version becomes the **scoring engine reused inside every paid kit (P14–P18)**: build once,
sell many.

> **Framing (brief §15):** positioned as an **audit-ready readiness check that satisfies a
> TÜV-style certifier auditing you to ISO / HACCP / BRCGS / IFS** — never a "TÜV template".
> TÜV is a *certification body*, not a standard.

### Sheets
| # | Sheet | Asset | Purpose |
|---|-------|-------|---------|
| 00 | Start Here / Začnite tu | — | how-to + what-it-is + legal disclaimer |
| 01 | Gap Analysis / Analýza | CA 1 | 26 clauses × 8 sections; Status → auto Conf.% + Priority |
| 02 | Mock Audit / Skúšobný audit | CA 2 | 20 "could you show…?" questions; auto readiness % |
| 03 | Readiness / Pripravenosť | — | combined % + RAG verdict + section breakdown + open-gap counts |
| 04 | Next Steps / Ďalšie kroky | — | sector → matching paid kit (P14–P18) upsell routing |

### Built-in logic (not just blank tables)
- **Gap analysis**: per-clause Status dropdown (Conform / Partial / Not in place / N/A) →
  auto **Conformance %** (100 / 50 / 0 / excluded) and auto **Priority** (HIGH for *Not in
  place*, MEDIUM for *Partial*); RAG conditional formatting; non-food rows (section 8F) set
  to N/A self-exclude from the average.
- **Section roll-up**: `AVERAGEIFS` per section on the dashboard, RAG-banded.
- **Overall conformance**: `AVERAGE` of all applicable clause scores (blanks/N-A ignored).
- **Mock audit**: Yes / Partly / No → 100 / 50 / 0 %, averaged to a readiness score.
- **Overall readiness**: mean of gap-analysis % and mock-audit % (handles either side blank).
- **Verdict ("will I pass?")**: RAG bands — 🟢 ≥85% *Likely to pass* · 🟠 60–84% *At risk* ·
  🔴 <60% *Not ready* — driven by formula, no manual judgement.
- **Open-gap counters**: live `COUNTIF` of HIGH and MEDIUM gaps.

### EU conventions applied
DD/MM/YYYY date cells · metric framing · percentages for all scores · Ireland/EU
regulatory references (852/2004, 1169/2011, Amd 1:2024 climate action).

### Bilingual (EN / SK)
Every sheet ships parallel English + Slovak titles, instructions, clause requirements,
questions and verdict text (per the AGENTS.md binding rule and
`deliverables/asset_glossary_EN_SK.md`).
⚠️ Before public launch route the Slovak through a native editor (the `/slovak` skill is
not installed here) — see handover standing add-on.

---

## Listing copy (draft — re-verify fees at listing time)

### English
**Free Compliance Readiness Check — "Will I pass my audit?" in 15 minutes**

A free, bilingual (EN/SK) Excel tool that scores how audit-ready you really are. Set a
status against each requirement, answer 20 mock-audit questions, and the workbook
auto-calculates your conformance %, a traffic-light verdict, and your highest-priority
gaps — across the structure shared by ISO 9001, ISO 22000, HACCP, BRCGS, IFS and FSSC
22000. Then it points you to the exact ready-made kit that closes those gaps.

- ✅ Clause-by-clause gap analysis with automatic scoring
- ✅ 20-question mock-audit self-assessment
- ✅ Traffic-light "will I pass?" verdict + section breakdown
- ✅ Works in Excel, Google Sheets and LibreOffice — no subscription, no login
- ✅ English + Slovak throughout · 100% free

*Template only — not legal advice nor a guarantee of certification. Audit-ready support for
a TÜV-style certifier auditing you to ISO / HACCP / BRCGS / IFS — not affiliated with TÜV.*

### Slovenčina
**Bezplatná kontrola pripravenosti na audit — „Prejdem auditom?“ za 15 minút**

Bezplatný dvojjazyčný (EN/SK) nástroj v Exceli, ktorý ohodnotí, ako veľmi ste pripravení na
audit. Nastavte stav ku každej požiadavke, odpovedzte na 20 otázok skúšobného auditu a zošit
automaticky vypočíta % zhody, semaforový verdikt a vaše najdôležitejšie medzery — naprieč
štruktúrou spoločnou pre ISO 9001, ISO 22000, HACCP, BRCGS, IFS a FSSC 22000. Potom vás
nasmeruje na presný hotový balík, ktorý tieto medzery vyrieši.

- ✅ Analýza nedostatkov po jednotlivých bodoch s automatickým hodnotením
- ✅ Sebahodnotenie skúšobného auditu (20 otázok)
- ✅ Semaforový verdikt „prejdem?“ + rozpis po sekciách
- ✅ Funguje v Exceli, Google Sheets aj LibreOffice — bez predplatného
- ✅ Kompletne v angličtine aj slovenčine · úplne zadarmo

*Šablóna — nie je právne poradenstvo ani záruka certifikácie. Podpora pripravenosti na audit
certifikačným orgánom (štýl TÜV) podľa ISO / HACCP / BRCGS / IFS — bez väzby na TÜV.*

---

## Launch checklist status (brief §4 / MONETIZATION_BRIEF §4, §7)
- [x] Product workbook built (full, editable, free download)
- [x] Watermarked read-only demo built (sheet-protected, "DEMO — enter email to download" banner)
- [x] Bilingual EN/SK copy (titles, instructions, clauses, questions, listing draft)
- [x] Price + platform set (€0 free lead magnet, Lemon Squeezy email capture)
- [x] Real scoring logic verified (Conf.% / Priority / readiness / RAG verdict)
- [ ] Email-capture funnel wired (Lemon Squeezy free product + email list) at listing time
- [ ] Preview images (export sheet screenshots — do at listing time)
- [ ] Slovak copy native-editor pass before public launch
- [ ] Licence text + EU immediate-delivery / 14-day-withdrawal waiver (LS provides) — even for free
- [ ] GDPR consent on the email-capture step (lawful basis, privacy notice)

## Funnel / bundle path (MONETIZATION_BRIEF §7 value-ladder)
**Rung 0 (this product, €0)** → captures the email and the "will I pass?" verdict →
upsell to the matching **Rung 2 standard kit**:
- Hospitality (HACCP) → **P14** €49
- Food mfg ISO 22000 / FSSC 22000 → **P15** €99
- Food mfg BRCGS / IFS → **P16** €89
- Non-food mfg ISO 9001 → **P17** €79
- FSSC v6→v7 transition → **P18** €49
- Auditors / consultants → **P19 / P20** from €149

This free engine is the same scoring logic embedded (per-standard) inside each paid kit —
the lead magnet *is* a slice of the product it sells.
