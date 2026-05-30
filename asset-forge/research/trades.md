# Trades — Research (Phase 4)

**Vertical:** Trades · **Business types (DB ids 16–21):** Electrician · Plumber/heating ·
Carpenter/joiner · Painter/decorator · Tiler · Landscaper/groundworks.
**Context:** EU / Ireland seller. Metric units, EU dates (DD/MM/YYYY), € amounts.
**Method:** Section [7] of the brief — 5 questions per business type, scored to rubric [6].
**Work-context tagging (Section [5], trades-specific):** every trades asset is tagged
**solo vs team · on-site vs workshop/off-site vs on-the-road (van/mobile)** in
`business_types.work_context` and per-row in `asset_map.notes`.

> **Spine confirmed live:** trades run a **Quote → Job/Schedule → Invoice → Compliance-Certificate**
> loop. The legal floor is **sector licensing/registration + statutory completion
> certificates**, not a single food-style regulator. This produces a *narrow* auto-MUST
> floor (certs, H&S, sector-specific chemical/fire) and a *large* SHOULD "wanted, sells
> well" zone (quoting, job tracking, scheduling, invoicing/getting-paid) — the highest
> willingness-to-pay band for a trade.

---

## 0. Regulatory MUST-floor (verified LIVE, Ireland)

| Floor item | Who it binds | Effect on tier | Source |
|---|---|---|---|
| **Safe Electric / RECI** registration + **Completion Certificate** for all Controlled Works | Electricians (legally only registered contractors may do controlled electrical work) | Completion-cert register → **Legal = 3 → MUST** | safeelectric.ie Rules of Registration |
| **RGI** (Registered Gas Installer) + **Declaration of Conformance / Completion Certificate** mandatory for all "Gas Work" (2006 Act, I.S. 813) | Plumbers/heating doing gas work | Cert register → **Legal = 3 → MUST** | rgi.ie/installers/about-us/certificates |
| **CIRI** (Construction Industry Register Ireland) — moving from voluntary to **statutory/mandatory** registration of competent builders/trades (Reg. of Providers of Building Works Act 2022; mandatory rollout 2026) | Carpenters/joiners, landscaper/groundworks & other building-works trades (electrical & gas excluded — own registers) | Registration + competence records → expected→mandatory | cif.ie/ciri · dwfgroup.com (CIRI goes mandatory, 2026) |
| **BC(A)R 2014 / BCAR** — design, inspection & **ancillary completion certification** for works needing a Fire Safety Cert | Trades acting as builder / ancillary certifier on notifiable works | Cert/compliance records → Legal = 2–3 | scsi.ie BCAR guide |
| **Safe Pass** (SOLAS) mandatory for **anyone** on a construction site (incl. self-employed), renew every 4 yrs; **CSCS** for high-risk plant | All site-working trades | Card/expiry tracking is high-value (cards are statutory) | smartmovesafety.ie |
| **Safety, Health & Welfare at Work Act 2005** + **Construction Regs 2013** — Safety Statement / risk assessment; **RAMS** (method statements) on site | All trades (employer & self-employed duties) | Safety Statement → **Legal = 3 → MUST**; RAMS → Legal = 2 | smartmovesafety.ie · HSA |
| **Chemical Agents Regs 2001 / REACH** — SDS + risk assessment for solvents, paints, adhesives, grouts, lacquers, wood dust (carcinogen) | Painter/decorator, tiler, carpenter | Legal = 2–3 where solvent/dust exposure | HSA Chemical Agents |
| **Sustainable Use of Pesticides (S.I. 155/2012)** — professional-user registration (DAFM) + records for plant-protection products | Landscaper/groundworks | Pesticide/SDS records → **Legal = 3 → MUST** | DAFM PU register |
| **RCT (Relevant Contracts Tax)** + **VAT reverse charge** on construction services (principal accounts for VAT; subbie invoices without VAT, narrative required) | Electrician, plumber, carpenter, landscaper acting as principal/sub | RCT/subcontractor tracker → Legal = 2 (Revenue-mandated) | revenue.ie VAT-construction TDM · grantthornton.ie RCT |

EU-VAT note (seller side, carried from earlier phases): products are **digital goods**; EU
VAT on digital goods is in scope — handled at the platform layer (Phase 8), not by these
operator tools. The **RCT reverse-charge** point above is the *buyer's* (the tradesperson's)
VAT concern and is what the RCT tracker addresses.

---

## 1. Electrician (id 16) — *solo or small team · on-site + on-the-road (van)*

1. **Departments (even informal):** Ops (install/test), Quality & Compliance (certs,
   instrument calibration), Job & Schedule Mgmt, Finance (quote/invoice/RCT/cashflow),
   Sales/CRM (enquiries), Procurement (van stock), HR (Safe Pass/cards), Maintenance (van/tools).
2. **Recurring record-producing workflows:** issue a **Completion/Test Certificate** per job
   (statutory); quote → job card → invoice; schedule day's calls; test-instrument calibration;
   RCT on subcontracted work; card/insurance renewals.
3. **Assets & scores:** Completion & Compliance Cert Register (**MUST, Legal=3**); Test-Instrument
   Calibration Log (SHOULD); Quote/Estimating, Job Card/WIP, Schedule & Dispatch, Invoice &
   Payment, Cashflow (SHOULD — the getting-paid spine); RCT tracker (MUST/SHOULD); Safety
   Statement (**MUST, Legal=3**).
4. **Top pains:** chasing payments / cashflow gaps; quoting accuracy vs won/lost margin;
   certificate admin and keeping registration valid; juggling multiple small jobs/day.
5. **Existing tools & gaps:** Tradify, ServiceM8 — strong on quote→job→invoice + payment
   reminders, **weak on Irish cert templates (Safe Electric), RCT, and instrument calibration**;
   per-seat monthly cost resented by solo sparks. Spreadsheet packs fill the cert/RCT/calibration gap.

## 2. Plumber/heating (id 17) — *solo or small team · on-site + on-the-road (van)*

1. **Departments:** Ops, Quality & Compliance (gas cert/RGI), Job & Schedule, Finance, CRM,
   Procurement, HR, Maintenance.
2. **Workflows:** **Gas Completion / Declaration of Conformance Cert** (statutory for gas work);
   boiler-service records; quote→job→invoice; scheduling emergency + planned calls; RCT.
3. **Assets & scores:** Completion & Compliance Cert Register (**MUST, Legal=3** — RGI gas);
   Service/Job Card; Quote, Invoice, Schedule, Cashflow (SHOULD); RCT (MUST/SHOULD); Safety
   Statement (**MUST**).
4. **Top pains:** emergency-vs-planned scheduling chaos; getting paid on small jobs; gas-cert
   and RGI compliance; parts/van-stock on the road.
5. **Existing tools & gaps:** same SaaS field (Tradify/ServiceM8/Joblogic); **gas-cert templates,
   RGI declarations, RCT not localised** → spreadsheet opportunity.

## 3. Carpenter/joiner (id 18) — *solo or team · workshop/off-site + on-site*

1. **Departments:** Ops (bench + install), Procurement (timber/board/ironmongery), Finance,
   Job & Schedule, Quality (BCAR ancillary, snagging), HR, Maintenance (machines), Compliance
   (workshop fire/dust).
2. **Workflows:** **cutting list / materials take-off**; quote→job→install→snag/sign-off; BCAR
   ancillary certs on notifiable works; workshop fire & wood-dust (carcinogen) controls.
3. **Assets & scores:** Materials Take-off & Cutting-list Calculator (SHOULD — high); Quote, Job
   Card, Schedule, Invoice, Cashflow (SHOULD); Snag/Sign-off (SHOULD); Workshop Fire Register
   (**MUST, Legal=3**); Chemical Agents/Dust SDS (**MUST/SHOULD** — hardwood dust carcinogen);
   Safety Statement (**MUST**); Machine Safety/Guarding (reuse — **MUST**).
4. **Top pains:** bespoke estimating under-prices labour; timber wastage; snagging disputes
   delay final payment; dust-extraction (LEV) compliance.
5. **Existing tools & gaps:** generic job apps + manual cutting lists; **no integrated take-off +
   snag + cert pack** for small joinery shops.

## 4. Painter/decorator (id 19) — *solo or team · on-site + on-the-road*

1. **Departments:** Ops, Finance, Job & Schedule, CRM, Procurement (paint), Quality (snagging),
   Compliance (solvent/VOC SDS), HR.
2. **Workflows:** **area take-off (m² → litres)**; quote→job→snag/sign-off→invoice; solvent &
   VOC chemical-agent risk assessment.
3. **Assets & scores:** Materials Take-off & Coverage Calculator (SHOULD — high); Quote, Job Card,
   Schedule, Invoice, Cashflow, Snag/Sign-off, CRM (SHOULD); Chemical Agents/VOC SDS (**MUST**,
   Legal=3 — solvents/isocyanates); Safety Statement (**MUST**).
4. **Top pains:** under-estimating coverage/coats; deposits & getting paid; managing several
   domestic jobs; solvent/dust H&S.
5. **Existing tools & gaps:** job apps thin on **coverage take-off + dilapidation/snag photos**;
   spreadsheet calculators sell well on Etsy/Gumroad.

## 5. Tiler (id 20) — *usually solo · on-site*

1. **Departments:** Ops, Finance, Job & Schedule, CRM, Procurement (tile/adhesive/grout),
   Quality (snag), Compliance (adhesive/sealant SDS).
2. **Workflows:** **m² + wastage + adhesive/grout take-off**; quote→job→sign-off→invoice; deposit
   on materials.
3. **Assets & scores:** Materials Take-off & m²/Adhesive Calculator (SHOULD — flagship-grade for
   tilers); Quote, Invoice, Cashflow, Schedule, Snag (SHOULD/COULD); Chemical Agents SDS
   (SHOULD); Safety Statement (**MUST**).
4. **Top pains:** quoting m²/wastage accurately; chasing balances after deposit; material
   ordering errors.
5. **Existing tools & gaps:** mostly manual/spreadsheet already — **demonstrates the exact
   product-market fit** for a tiler take-off + quote sheet (cheap to build, clear pain).

## 6. Landscaper/groundworks (id 21) — *team · on-site + yard/off-site + on-the-road*

1. **Departments:** Ops (planting + groundworks), Plant/Maintenance, Finance, Job & Schedule,
   CRM, Procurement, HR (Safe Pass/CSCS), Compliance (pesticide PU register, RCT, RAMS).
2. **Workflows:** **pesticide/plant-protection records (DAFM professional user)**; plant/machinery
   maintenance & guarding; quote→job→invoice; RCT on groundworks (construction); RAMS on site.
3. **Assets & scores:** Pesticide/Chemical Agents Register (**MUST, Legal=3** — Sustainable Use
   Regs); Plant & Equipment Maintenance/Guarding (reuse — SHOULD/MUST); RCT Tracker (MUST/SHOULD);
   RAMS (SHOULD); Safety Statement (**MUST**); Quote, Schedule, Invoice, Cashflow, CRM (SHOULD).
4. **Top pains:** weather-driven rescheduling; plant downtime; pesticide compliance records;
   RCT/subcontractor admin on bigger groundworks contracts.
5. **Existing tools & gaps:** field-service apps exist but **pesticide records, plant guarding,
   RCT and RAMS are unserved** by generic tools → compliance + scheduling spreadsheet packs.

---

## Cross-trade synthesis

- **Universal trades core (build once, sell many):** Quote/Estimating · Job Card/WIP ·
  Job Schedule & Dispatch · Invoice & Payment-chasing · Cashflow/P&L · Safety Statement —
  every one of the six needs them. These are the SHOULD "wanted, sells well" anchors and the
  natural **hospitality-first → trades-next** roadmap fuel.
- **Legal auto-MUST floor (narrow, sector-specific):** Completion/Compliance Cert Register
  (electrician & plumber/gas, Legal=3) · Safety Statement (all) · Chemical/Pesticide SDS
  (painter, landscaper) · Workshop Fire (carpenter). Anything Legal=3 auto-promotes (rubric [6]).
- **Highest willingness-to-pay SHOULD/COULD:** Materials Take-off calculators (tiler, painter,
  carpenter), Snag/Sign-off, RCT tracker, Cert/Card/Insurance expiry tracker — desired, not
  dreaded, and unserved by generic SaaS.
- **Buyer dimension:** mostly `operator`; `auditor` appears on cert registers (Safe Electric/RGI
  inspectors) and `consultant` on Safety Statement / RAMS / RCT (H&S consultants, accountants).

### Sources (live-verified, 30/05/2026)
- Safe Electric Rules of Registration (completion cert mandatory) — safeelectric.ie
- RGI completion/conformance certificates (2006 Act) — rgi.ie/installers/about-us/certificates
- CIRI statutory/mandatory register — cif.ie/ciri ; dwfgroup.com "CIRI goes mandatory" (2026)
- BC(A)R 2014 / ancillary certs — scsi.ie BCAR guide
- Safe Pass / CSCS mandatory on site — smartmovesafety.ie
- RCT + VAT reverse charge (construction) — revenue.ie VAT-construction TDM ; grantthornton.ie RCT
- Trade job-management SaaS (Quote→Job→Invoice, payment chasing) — tradifyhq.com ; servicem8.com ;
  viotrade.co.uk ; linktly.com
