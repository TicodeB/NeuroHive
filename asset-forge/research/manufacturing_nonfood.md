# Research — NON-FOOD MANUFACTURING (Phase 3)

**Vertical:** Non-food manufacturing · **Business types:** Metal/engineering,
Plastics/injection, Packaging/print, Joinery/furniture, Light electronics
(business_type ids 11–15).
**Context:** EU / Ireland seller. Metric units, EU dates (DD/MM/YYYY), comma thousands.
**Method:** Brief Section [7] — 5 questions per business type, scored to rubric [6],
buyer dimension tagged, every MUST/SHOULD row carries an `evidence_url`.

> Dedupe rule honoured: where a hospitality/food asset already covers the same *function*
> (Batch/Yield Record, BOM & costing, Production Planning, Calibration, Supplier Approval,
> Raw-material inventory, Cashflow/P&L, B2B invoicing, OEE/KPI dashboard, Maintenance/PPM,
> Training matrix, H&S safety statement, Fire register, Recall/Withdrawal), Phase 3 **reuses
> the existing `digital_assets` row**. Only genuinely new non-food functions get new rows.

---

## [A] REGULATORY MUST-FLOOR (verified LIVE, not from memory)

The non-food floor is **entirely different from food** — no FSAI/HACCP. It is built on
product-conformity (CE), workplace-equipment & chemical-safety law, and producer-responsibility
(EPR). These are what auto-promote assets to MUST (rubric [6], Legal = 3).

| Obligation | Who it binds | Source (verified 29/05/2026) |
|---|---|---|
| **CE marking** — manufacturer performs conformity assessment, compiles a **technical file (kept 10 years)**, issues the **EU Declaration of Conformity**, affixes CE | Anyone placing in-scope products on the EU market — esp. **Light electronics** (LVD + EMC + RoHS), **Metal/engineering** building machinery (Machinery Reg/Directive), some **Plastics** finished goods | [EC — Manufacturers / CE marking](https://single-market-economy.ec.europa.eu/single-market/goods/ce-marking/manufacturers_en) · [Your Europe — Technical documentation](https://europa.eu/youreurope/business/product-requirements/compliance/preparing-technical-documentation/index_en.htm) |
| **Work-equipment safety**: use, inspection, guarding, control devices, energy isolation (S.I. 299/2007, Safety Health & Welfare at Work (General Application) Regulations 2007) | all 5 (any workshop with machinery) | [HSA — General Application Regulations 2007](https://www.hsa.ie/eng/legislation/regulations_and_orders/general_application_regulations_2007/) · [HSA — Work Equipment guide (PDF)](https://www.hsa.ie/eng/publications_and_forms/publications/general_application_regulations/gen_apps_work_equipment.pdf) |
| **Chemical agents**: duty to identify hazardous chemical agents and assess risk; SDS-driven controls (Safety Health & Welfare at Work (Chemical Agents) Regulations 2001 + REACH) | esp. **Packaging/print** (inks/solvents/VOCs), **Joinery** (adhesives/lacquers + **hardwood dust = carcinogen**), **Metal** (cutting fluids/degreasers/weld fume), **Plastics** (polymers/additives/fume) | [HSA — General Application Regulations 2007](https://www.hsa.ie/eng/legislation/regulations_and_orders/general_application_regulations_2007/) |
| **Safety Statement + risk assessment** (S.19 Act 2005) and **fire safety** statutory duty | all 5 (employers) | [HSA — Safety Statement & Risk Assessment](https://www.hsa.ie/eng/topics/managing_health_and_safety/safety_statement_and_risk_assessment/) |
| **Extended Producer Responsibility — packaging** (Repak; *major producer* = ≥ €1,000,000 turnover **and** ≥ 10 tonnes packaging on the Irish market → must join Repak, self-compliance closed since Jan 2023) | **Packaging/print** primarily; any of the 5 that put packaging on the market | [Repak — Summary of EU PPWR (PDF)](https://repak.ie/images/uploads/downloads/Summary_of_EU_PPWR_February_2025.pdf) · [EPR in Ireland](https://www.lizenzero.eu/en/blog/compliance-in-ireland-how-to-fulfil-your-epr-obligations/) |
| **WEEE producer responsibility** (electrical/electronic equipment) + **RoHS** substance restriction | **Light electronics** | [EC — WEEE responsibilities](https://europa.eu/youreurope/business/product-requirements/recycling-waste-management/weee-responsibilities/index_en.htm) |

**Voluntary-but-commercially-decisive standards:** **ISO 9001** (quality), **ISO 14001**
(environment), **ISO 45001** (occupational H&S). Not law, but B2B/OEM customers and public
tenders routinely require them — so the underlying documents (internal-audit programme,
NC/CAPA, calibration, supplier approval, management review) are SHOULD-tier with high
willingness-to-pay. Mapped in depth in the Phase 10 bonus track.

---

## [B] BUSINESS-TYPE DEEP DIVES (5 questions each)

### 11 — Metal/engineering (fabrication, machining, welding)
1. **Departments:** Production (machining/fab/weld), Quality (inspection, ISO 9001, CE on
   machinery), Procurement (steel/consumables), Finance (job costing), Sales (quoting),
   Job & Schedule mgmt, Maintenance.
2. **Workflows:** estimating/quoting custom parts; work-equipment safety + guarding (legal);
   first-article/dimensional **inspection + non-conformance**; **material/mill-cert
   traceability** (heat numbers); WIP through job stages; CE technical file where building
   machinery; chemical/SDS control (cutting fluids, weld fume).
3. **Assets:** Job Quotation & Estimating Tool, QC Inspection & NC Record, Material Cert &
   Traceability Register, Work-Equipment Safety/Guarding Register (legal), CE/DoC/Technical
   File Register, Production Job Card/WIP, plus reused BOM costing, Production Planning,
   Calibration, Supplier Approval, H&S, Fire, Cashflow, B2B invoice, OEE.
4. **Pain points:** quoting is slow and inconsistent (spreadsheet guesswork) → won/lost
   margin; un-tracked NCs and rework destroy job profit; ISO 9001 audit document load;
   material traceability for safety-critical work.
5. **Tools & gaps:** machine-shop ERP/quoting SaaS (Paperless Parts, ProShop, QuickWorks)
   is powerful but priced for scale; small shops still run spreadsheets and want an owned,
   affordable quote + QC + traceability kit.

### 12 — Plastics / injection moulding
1. **Departments:** Production (moulding), Quality (dimensional/SPC, CE where finished
   goods), Procurement (polymer/masterbatch), Finance, Sales, Maintenance (moulds/tools).
2. **Workflows:** batch/shot production & yield/scrap; **mould/tool maintenance** (reused
   PPM); QC dimensional + NC; SDS/chemical control (polymers, additives, purge); CE/DoC
   where the moulded item is an in-scope finished product; food-contact (Reg 1935/2004) if
   applicable; production planning vs orders.
3. **Assets:** QC Inspection & NC Record, Work-Equipment Safety Register (legal), Chemical
   Agents/SDS Register (legal), Batch/Yield (scrap), CE/DoC Register (where applicable),
   plus reused BOM costing, Production Planning, Calibration, Supplier Approval, Raw-material
   inventory, PPM (moulds), H&S, Fire, OEE, Cashflow.
4. **Pain points:** scrap/short-shot rate erodes margin invisibly; mould downtime; cycle-time
   & OEE blind spots; material cost volatility; documenting CE/food-contact where required.
5. **Tools & gaps:** plastics MES is enterprise-grade; small moulders want a scrap/OEE +
   QC sheet they own.

### 13 — Packaging / print
1. **Departments:** Production (print/convert), Quality (colour/registration QC), Procurement
   (board/film/inks), Finance (job costing), Sales (quoting), **Environmental/EPR**, Maintenance.
2. **Workflows:** estimating/quoting print jobs; ink/solvent **chemical-agent control**
   (legal, high — VOCs); **packaging EPR / Repak** reporting (legal — they ARE packaging
   producers); QC (colour, registration, NC); WIP through pre-press→print→finish; waste/make-ready.
3. **Assets:** Environmental/Waste/EPR Register (legal — Repak), Chemical Agents/SDS Register
   (legal — inks/solvents), Job Quotation & Estimating Tool, QC Inspection & NC Record,
   Work-Equipment Safety Register, Production Job Card/WIP, plus reused Production Planning,
   Supplier Approval, H&S, Fire, Cashflow, B2B invoice, OEE.
4. **Pain points:** quoting accuracy on variable jobs; make-ready waste; **EPR/Repak reporting
   burden**; solvent/VOC compliance; colour-consistency NCs.
5. **Tools & gaps:** print MIS exists but is costly; small printers want quote + waste +
   EPR-tracking sheets.

### 14 — Joinery / furniture
1. **Departments:** Production (machining/assembly/finishing), Quality (CE/CPR on
   construction joinery, fire-rating on furniture), Procurement (timber/board/ironmongery),
   Finance (job costing), Sales (quoting), Maintenance.
2. **Workflows:** estimating/quoting bespoke joinery; **hardwood-dust + finish/adhesive
   chemical control** (legal, high — wood dust is a carcinogen); work-equipment/guarding on
   saws/spindles (legal); **CE/CPR** for construction joinery (windows/doors) + furniture
   fire-safety; cutting-list/material optimisation; WIP per job.
3. **Assets:** Chemical Agents/SDS Register (legal — dust/finishes), Work-Equipment Safety
   Register (legal — saws/spindle moulders), CE/DoC & CPR Register (windows/doors), Job
   Quotation & Estimating Tool, QC Inspection & NC Record, Production Job Card/WIP, plus
   reused BOM/cutting-cost, Production Planning, Supplier Approval, Raw-material inventory,
   H&S, Fire, Cashflow, B2B invoice.
4. **Pain points:** bespoke quoting/estimating is slow and under-prices labour; timber
   wastage/cutting optimisation; **wood-dust exposure compliance** (LEV); CE/CPR paperwork
   for windows/doors; snagging/rework on installs.
5. **Tools & gaps:** joinery/cabinet software (cutting optimisers, CAD-MRP) is costly; small
   workshops want an estimating + cutting-cost + compliance kit they own.

### 15 — Light electronics (assembly / small EEE products)
1. **Departments:** Production (SMT/assembly/test), Quality (functional test, CE incl.
   LVD/EMC/RoHS), Procurement (components/BOM), Finance, Sales, **Environmental/WEEE**, Maintenance.
2. **Workflows:** **CE technical file + DoC** (LVD + EMC + RoHS — legal=3); functional/AOI
   test + NC; component **BOM costing** and traceability; **WEEE producer registration +
   RoHS** declarations (legal); SDS/chemical control (solder/flux); WIP per build/serial.
3. **Assets:** CE/DoC & Technical File Register (legal=3), Environmental/WEEE/RoHS Register
   (legal), QC Inspection & NC Record, Material/Component Traceability Register, Chemical
   Agents/SDS Register, Production Job Card/WIP, plus reused BOM costing, Production Planning,
   Calibration, Supplier Approval, H&S, Fire, Cashflow, B2B invoice, OEE.
4. **Pain points:** CE/RoHS/EMC technical-file burden for small product runs; component
   traceability + obsolescence; test-yield/NC tracking; WEEE registration admin.
5. **Tools & gaps:** electronics PLM/ERP is enterprise-grade; small product makers want a
   CE/RoHS file + BOM + test-yield kit they own.

---

## [C] CROSS-TYPE INSIGHTS (feeds Phase 6/7)
- **New universal-core candidates within non-food** (MUST/near-MUST across ≥3 of the 5):
  **Work-Equipment Safety/Guarding Register** (legal across all 5), **Chemical Agents/SDS
  Register** (legal across most), **QC Inspection & NC Record** and **Job Quotation &
  Estimating Tool** (high revenue/pain across all 5). These are the build-once/sell-many
  products for the manufacturing verticals.
- **CE/DoC & Technical File Register** is a high-value *niche* MUST anchored on Light
  electronics (Legal=3) and machinery-building Metal shops — low competition, high pain.
- **EPR/Repak register** is a Packaging/print-anchored MUST; **WEEE register** is the
  electronics analogue → a "Producer-Responsibility & Environmental Compliance" mini-suite.
- The reused **Batch/Yield, BOM costing, Production Planning, Calibration, Supplier Approval,
  OEE, Maintenance, Cashflow, B2B invoice** assets now span hospitality(partial)+food+non-food
  manufacturing — confirming the manufacturing "ops core" as the broadest sell-many base.

## [D] EU/Ireland notes
- Units metric (mm, kg, °C, minutes, units/min). Dates DD/MM/YYYY. Comma thousands (1,067,558).
- Repak "major producer" threshold expressed in EU style: ≥ €1,000,000 turnover **and** ≥ 10 t packaging.
- EU VAT on digital goods remains in scope for the seller (Ireland) — locked in Phase 8.
</content>
