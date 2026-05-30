# Standards & Audit Research — ASSET-FORGE (Phase 10, BONUS)

**Project:** SME Digital-Asset Intelligence → Productisation · **Owner:** Samuel Vyhnanek
**Context:** EU (Ireland) seller · **Phase:** 10 (🎁 bonus track) · **Date:** 30/05/2026
**Source of truth:** `intelligence.db` → tables `standards` (21), `compliance_assets` (19),
view `v_audit_packs` (115 standard×asset rows). Regenerate: `python3 scripts/seed_compliance.py`.

> This track turns the catalogue into a **second revenue line** serving compliance buyers,
> who pay more because failure = lost certification or licence. It runs only after the core
> hospitality product shipped (P1 + P2 are built — Phase 9 ✅).

> ⚠️ **Framing accuracy (do NOT get this wrong in listings):** TÜV (SÜD / Rheinland / NORD)
> is a **certification body, not a standard**. It audits a business *against* a standard such
> as ISO 9001 / 22000. Products are positioned as **"audit-ready packs that satisfy a
> TÜV-style certifier auditing you to ISO 9001 / 22000 / BRCGS"** — never "TÜV templates."

---

## 1. Standards mapped (versions verified LIVE 30/05/2026 via Tavily)

All versions were checked live this session because standard editions move (FSSC jumped to
v7 in May 2026; ISO added a climate amendment in 2024). Full rows + source URLs are in the
`standards` table.

| # | Standard | Family | Current version (verified 30/05/2026) | Legal? |
|---|---|---|---|:--:|
| 1 | ISO 9001 | ISO mgmt | **2015 + Amd 1:2024** (climate); **ISO 9001:2026 at FDIS** | customer-required |
| 2 | ISO 14001 | ISO mgmt | 2015 + Amd 1:2024 | voluntary |
| 3 | ISO 45001 | ISO mgmt | 2018 + Amd 1:2024 | voluntary |
| 4 | ISO 22000 | ISO mgmt | 2018 + Amd 1:2024 | customer-required |
| 5 | ISO 27001 | ISO mgmt | 2022 | niche |
| 6 | ISO 50001 | ISO mgmt | 2018 | niche |
| 7 | HACCP (Codex) | Food | **Codex CXC 1-1969, Rev. 2022** | ✅ legal floor |
| 8 | BRCGS Food Safety | Food (GFSI) | **Issue 9** (2022); **Issue 10 in development**, TWG started Apr 2026 | customer-required |
| 9 | IFS Food | Food (GFSI) | **Version 8** (Doctrine v5, Apr 2026) | customer-required |
| 10 | FSSC 22000 | Food (GFSI) | **Version 7** (published May 2026; v6→v7 upgrade by Apr 2028) | customer-required |
| 11 | SALSA | Food | current (entry-level, small producers) | voluntary |
| 12 | GMP / GHP | Food | per Codex GHP + sector codes | ✅ underpins legal |
| 13 | Reg. (EC) 852/2004 | EU legal floor | consolidated, as amended | ✅ mandatory (EU) |
| 14 | Reg. (EU) 1169/2011 (FIC) | EU legal floor | consolidated, as amended | ✅ mandatory (EU) |
| 15 | Fáilte Ireland accommodation | Hospitality | current registration/grading | registration (IE) |
| 16 | Safe-T-Cert | Trades/construction | current (IE/NI) | client-required |
| 17 | CIRI | Trades/construction | statutory register (IE) | ✅ statutory (IE) |
| 18 | Safe Electric | Trades/construction | current (IE) | ✅ legally required (IE) |
| 19 | RGI | Trades/construction | current (IE) | ✅ legally required (IE) |
| 20 | CHAS / SafeContractor / Constructionline | Trades/construction | current SSIP schemes (UK) | client-required (UK) |
| 21 | NICEIC / Gas Safe | Trades/construction | current (UK) | ✅ legally required (UK) |

**Rubric link (brief §6):** a standard mandated by law auto-promotes its assets to **MUST**
(Legal = 3). HACCP / 852/2004 / 1169/2011 / Safe Electric / RGI / Gas Safe / CIRI are the
legal-floor standards; the rest are customer- or client-driven (high willingness-to-pay
because losing the cert loses the contract, not the licence).

### Standard → business-type applicability
- **Hospitality (1–5):** HACCP + 852/2004 + 1169/2011 (legal); Fáilte Ireland (accommodation).
- **Food manufacturing (6–10):** HACCP + 852/2004 + 1169/2011 (legal floor) **plus** the
  GFSI commercial layer — BRCGS / IFS / FSSC 22000 / ISO 22000 (retail-required), SALSA for
  micro-producers, GMP/GHP underpinning all.
- **Non-food manufacturing (11–15):** ISO 9001 (quality, customer-required), ISO 14001 /
  45001 (environment & H&S), ISO 27001/50001 niche.
- **Trades (16–21):** ISO 9001 + 45001; IE schemes Safe-T-Cert, CIRI, Safe Electric, RGI;
  UK schemes CHAS/SafeContractor/Constructionline, NICEIC, Gas Safe.

---

## 2. Two buyers, same artefacts (the leverage)

The brief's key insight: the **same compliance documents** are bought by **both sides of an
audit**. Every asset is tagged `buyer_role` in `compliance_assets`.

### 2.1 Auditee / operator assets (buyer = the business being audited) — 11 assets
Gap-Analysis Tool · Mock-Audit / Readiness Self-Assessment · Document-Control Register ·
Internal-Audit Programme & Log · Management-Review Template + Minutes · Corrective-Action
(CAPA) Log · Training Matrix / Competency Records · Supplier-Approval Register · Calibration
Log · Traceability Log (food) · HACCP Plan + CCP Monitoring + PRP Checklists.

> Several reuse the **core catalogue assets already built**: HACCP plan → asset 1 (P1
> flagship); traceability → asset 5; calibration → asset 30; training matrix → asset 10
> (now shipped in P2 sheet 06); supplier approval → assets 5/28. **Build once, sell twice.**

### 2.2 Auditor / consultant assets (buyer = the professional inspecting/advising) — 8 assets
Audit Checklist / Protocol (per standard) · Audit Scoring & Grading Sheet · Non-Conformance
(NC) Register · Audit-Schedule Planner (surveillance + recertification) · Objective-Evidence
Register · Audit-Report Generator · Auditor Competency Log · Findings Dashboard.

> These are the same artefacts a HACCP/ISO **consultancy bills for** — so they double as
> productised IP *and* as delivery tooling for advisory work (brief §15 reuse value).

---

## 3. Pain points & willingness-to-pay (why compliance buyers pay more)

- **"Will I pass?" anxiety** — the single biggest pain. The **Mock-Audit / Readiness
  Self-Assessment** answers it directly → highest WTP, and the flagship to build (Phase 12).
- **Cost of failure is existential, not annoying** — losing BRCGS/IFS/FSSC certification can
  lose a retail contract overnight; losing Safe Electric/RGI/Gas Safe registration halts
  trading. Buyers price against that downside, not against a €30 template.
- **Consultants charge €600–€2,000+** to run a gap analysis or write a management system; a
  guided template that does 80% of it for €49–€99 is an easy sell.
- **Version churn is a recurring trigger** — FSSC v6→v7 (by Apr 2028) and the coming BRCGS
  Issue 10 / ISO 9001:2026 each force a re-documentation wave → natural update/upsell cadence.
  (Listings must state which version they target and offer free version updates.)

---

## 4. Productisation logic (hands to Phase 11)

`v_audit_packs` groups every compliance asset under each standard → **instant per-standard
bundle definitions**. Per the brief, per-standard bundles sell best:

- **"HACCP Readiness Pack for Cafés"** (operator; standards 7/13/14) — extends the P1 flagship.
- **"ISO 22000 Internal Audit Kit"** (operator; standard 4) — internal-audit + NC + CAPA +
  management-review + document-control.
- **"BRCGS Document-Control Suite"** (operator; standard 8) — Issue 9 now, Issue 10-ready.
- **"FSSC 22000 v7 Transition Pack"** (operator; standard 10) — timely: v7 transition to Apr 2028.
- **Auditor Edition** (auditor/consultant) — checklist + scoring + NC register + report
  generator + findings dashboard, sold per standard at a premium.

**Tiered offer (brief §15.5):** free **gap-analysis lite** (lead magnet) → paid
**standard-specific kit** (€49–€99) → full **audit suite (auditor edition)** (€149+).

**Flagship to build first (Phase 12):** the **Gap-Analysis Tool + Mock-Audit
Self-Assessment** — cheapest to build, easiest to demo, clearest pain-killer, and it seeds
every per-standard bundle.

### Products table now carries `audience` + `standard_ids`
All 12 roadmap products defaulted to `audience='operator'`; standard-linked ones mapped:
P1→7,13,14 · P8→7,13,4,8,10 · P10→14 · P11→1 · P7→18,19. Phase 11 will add the
auditor/consultant products and the per-standard bundles.

---

## 5. EU / Ireland notes
- Allergen + hygiene legal floor (852/2004, 1169/2011) is **non-negotiable** and already the
  spine of P1 — the compliance track layers the **voluntary-but-commercially-forced** GFSI
  and ISO schemes on top.
- Metric units, DD/MM/YYYY, comma thousands carried throughout (consistent with P1/P2).
- VAT/platform unchanged from Phase 8 (Lemon Squeezy MoR; €-pricing).

---

## 6. Integrity & verification
- All 21 standard versions **verified live 30/05/2026** (Tavily); `source_url` stored per row.
- Legal-mandated standards flagged → their assets are tier MUST (rubric Legal=3).
- No duplicate assets invented — compliance assets cross-reference existing catalogue asset
  ids where the artefact already exists (1, 5, 10, 28, 30).
- `v_audit_packs` self-verified: 115 standard×asset rows; ISO 22000 pack sample printed by the
  seed script.

*End of Phase 10 research. Next: Phase 11 — Audit & compliance productisation (auditor
toolkits + auditee compliance packs added to `PRODUCT_ROADMAP.md`).*
