#!/usr/bin/env python3
"""
ASSET-FORGE — Phase 3 seed: NON-FOOD MANUFACTURING research rows.

Inserts non-food-manufacturing digital assets (NEW functions only — existing
hospitality/food assets that cover the same FUNCTION are reused by id, not
re-created), the scored asset_map rows (raw 0-3 axis scores per rubric [6] +
buyer tag + evidence_url) and pain points for the five non-food-manufacturing
business types (Metal/engineering, Plastics/injection, Packaging/print,
Joinery/furniture, Light electronics).

Score = (legal*3) + (revenue*2) + (pain*2) + (frequency*1), max 24.
Tier:  MUST  if score >= 16 OR legal == 3 (legal-mandatory auto-promotes)
       SHOULD 10-15 · COULD 5-9 · WON'T < 5.

Idempotent: deletes this phase's rows first (business types 11-15), then
re-inserts. New digital_assets are upserted by unique name; existing reused
assets are referenced by name and never overwritten.

Usage:
    python3 scripts/seed_manufacturing_nonfood.py [--db PATH]
"""

import argparse
import os
import sqlite3
import sys

DEFAULT_DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "intelligence.db")

# Non-food-manufacturing business_type ids (seeded in Phase 0).
METAL, PLAST, PACK, JOIN, ELEC = 11, 12, 13, 14, 15

# Department ids (Phase 0 seed).
OPS, QC_D, HR, FIN, SALES, PROC, MAINT, FOH, JOB, KPI = range(1, 11)

# --- Evidence URLs (verified LIVE in Phase 3) -------------------------------
CE_EU = "https://single-market-economy.ec.europa.eu/single-market/goods/ce-marking/manufacturers_en"
CE_TECH = "https://europa.eu/youreurope/business/product-requirements/compliance/preparing-technical-documentation/index_en.htm"
HSA_GENAPP = "https://www.hsa.ie/eng/legislation/regulations_and_orders/general_application_regulations_2007/"
HSA_EQUIP = "https://www.hsa.ie/eng/publications_and_forms/publications/general_application_regulations/gen_apps_work_equipment.pdf"
HSA_SS = "https://www.hsa.ie/eng/topics/managing_health_and_safety/safety_statement_and_risk_assessment/"
REPAK = "https://repak.ie/images/uploads/downloads/Summary_of_EU_PPWR_February_2025.pdf"
EPR_IE = "https://www.lizenzero.eu/en/blog/compliance-in-ireland-how-to-fulfil-your-epr-obligations/"
WEEE_EU = "https://europa.eu/youreurope/business/product-requirements/recycling-waste-management/weee-responsibilities/index_en.htm"
EST_SW = "https://softwareconnect.com/roundups/best-manufacturing-estimating-quoting-software/"
PAPERLESS = "https://www.paperlessparts.com/"
PM_FORUM = "https://www.practicalmachinist.com/forum/threads/quality-management-plan-template.429078/"
QC_SW = "https://www.alphasoftware.com/quality-control-software-for-manufacturing"

# --- NEW non-food-manufacturing assets (deduped by FUNCTION) ----------------
ASSETS = {
    "CE Marking, Declaration of Conformity & Technical File Register": ("Form/checklist", "Tracks CE conformity assessment, the technical file (retained 10 years), the EU Declaration of Conformity and applied directives (Machinery, LVD, EMC, RoHS) per product placed on the EU market."),
    "Quality Control Inspection & Non-Conformance Record": ("Form/checklist", "Incoming/in-process/final inspection results, first-article and dimensional/visual checks, plus a non-conformance (NC) and corrective-action log."),
    "Job Quotation & Estimating Tool": ("Quote generator", "Builds priced quotes/estimates for custom jobs from materials + labour + overhead + margin; tracks won/lost outcomes for an engineering/joinery/print shop."),
    "Work Equipment & Machinery Safety/Guarding Inspection Register": ("Log book", "Statutory work-equipment inspections, guarding/control-device checks and energy-isolation records (S.I. 299/2007 General Application Regs)."),
    "Chemical Agents (SDS) Register & Risk Assessment": ("Database", "Safety-Data-Sheet register and hazardous-chemical-agent risk assessment (solvents/inks/adhesives/cutting fluids/wood dust) per Chemical Agents Regs 2001 + REACH."),
    "Material Certificate & Batch Traceability Register": ("Log book", "Logs material/mill certificates (heat/lot numbers) and component batch traceability for recall and safety-critical/CE work."),
    "Production Job Card & WIP Tracker": ("Spreadsheet tracker", "Tracks each job/order through production stages (work-in-progress), capturing labour, materials and status."),
    "Dispatch, Delivery-Note & Goods-Out Log": ("Log book", "Records finished-goods dispatch, delivery notes and goods-out for traceability and proof of delivery."),
    "Environmental, Waste & Producer-Responsibility (EPR) Register": ("Form/checklist", "Logs packaging placed on market (Repak), WEEE/RoHS obligations and waste streams for producer-responsibility reporting."),
    "ISO 9001 Internal Audit & Management-Review Log": ("Form/checklist", "Internal-audit programme, audit findings, management-review minutes and improvement actions for an ISO 9001 quality management system."),
}

# --- Reused existing assets (by name) ---------------------------------------
BATCH = "Batch Production & Yield Record"
BOM = "Recipe / BOM & Batch Costing Calculator"
PLAN = "Production Planning & Scheduling Sheet"
CAL = "Calibration Log (Scales, Thermometers, Probes)"
SUPP = "Supplier Approval & Specification Register"
RAW = "Raw Material Inventory & FIFO/FEFO Stock Rotation"
CF = "Cashflow & P&L Tracker"
B2B = "Wholesale Order & B2B Invoice Tool"
OEE = "Production KPI & Downtime (OEE) Dashboard"
PPM = "Maintenance & PPM Asset Register"
TRN = "Staff Training & Induction Matrix"
HS = "H&S Risk Assessment & Safety Statement"
FIRE = "Fire Safety Register & Checks Log"
RECALL = "Recall / Withdrawal Plan & Mock-Recall Log"

# --- New asset short-keys ---------------------------------------------------
CE = "CE Marking, Declaration of Conformity & Technical File Register"
QCINSP = "Quality Control Inspection & Non-Conformance Record"
QUOTE = "Job Quotation & Estimating Tool"
EQUIP = "Work Equipment & Machinery Safety/Guarding Inspection Register"
SDS = "Chemical Agents (SDS) Register & Risk Assessment"
MATCERT = "Material Certificate & Batch Traceability Register"
WIP = "Production Job Card & WIP Tracker"
DISPATCH = "Dispatch, Delivery-Note & Goods-Out Log"
ENV = "Environmental, Waste & Producer-Responsibility (EPR) Register"
AUDIT9001 = "ISO 9001 Internal Audit & Management-Review Log"

OP, AUD, CON = "operator", "auditor", "consultant"

# --- asset_map rows ---------------------------------------------------------
# (business_type, asset_name, department, buyer, legal, revenue, pain, frequency, evidence_url, notes)
ROWS = [
    # ===== Work-equipment safety MUST floor (Legal=3) across all five =======
    (METAL, EQUIP, QC_D, OP, 3, 1, 2, 2, HSA_EQUIP, "Lathes/mills/press/weld bays — guarding + inspection."),
    (PLAST, EQUIP, QC_D, OP, 3, 1, 2, 2, HSA_EQUIP, "Injection presses — guarding/interlocks."),
    (PACK, EQUIP, QC_D, OP, 3, 1, 2, 2, HSA_EQUIP, "Print/convert machinery nip points."),
    (JOIN, EQUIP, QC_D, OP, 3, 1, 3, 2, HSA_EQUIP, "Saws/spindle moulders — high amputation risk."),
    (ELEC, EQUIP, QC_D, OP, 3, 0, 1, 2, HSA_EQUIP, "Bench/SMT line equipment."),

    # ===== H&S safety statement + fire MUST floor (Legal=3) =================
    (METAL, HS, QC_D, OP, 3, 1, 2, 1, HSA_SS, ""),
    (PLAST, HS, QC_D, OP, 3, 1, 2, 1, HSA_SS, ""),
    (PACK, HS, QC_D, OP, 3, 1, 2, 1, HSA_SS, ""),
    (JOIN, HS, QC_D, OP, 3, 1, 2, 1, HSA_SS, ""),
    (ELEC, HS, QC_D, OP, 3, 1, 2, 1, HSA_SS, ""),

    (METAL, FIRE, QC_D, OP, 3, 0, 2, 2, HSA_SS, "Hot work/welding fire load."),
    (PLAST, FIRE, QC_D, OP, 3, 0, 2, 2, HSA_SS, "Polymer fire load."),
    (PACK, FIRE, QC_D, OP, 3, 0, 3, 2, HSA_SS, "Solvent/paper high fire load."),
    (JOIN, FIRE, QC_D, OP, 3, 0, 3, 2, HSA_SS, "Wood dust + finishes high fire/explosion risk."),
    (ELEC, FIRE, QC_D, OP, 3, 0, 1, 2, HSA_SS, ""),

    # ===== Chemical agents / SDS (Legal varies; high where solvents/dust) ===
    (PACK, SDS, QC_D, OP, 3, 1, 3, 2, HSA_GENAPP, "Inks/solvents/VOCs — Chemical Agents Regs 2001."),
    (JOIN, SDS, QC_D, OP, 3, 1, 3, 2, HSA_GENAPP, "Hardwood dust is a carcinogen + adhesives/lacquers."),
    (METAL, SDS, QC_D, OP, 2, 1, 2, 2, HSA_GENAPP, "Cutting fluids/degreasers/weld fume."),
    (PLAST, SDS, QC_D, OP, 2, 1, 2, 2, HSA_GENAPP, "Polymers/additives/purge fume."),
    (ELEC, SDS, QC_D, OP, 2, 0, 1, 1, HSA_GENAPP, "Solder/flux/cleaning agents."),

    # ===== CE marking / DoC / technical file (Legal=3 electronics; varies) ==
    (ELEC, CE, QC_D, OP, 3, 2, 3, 2, CE_EU, "LVD + EMC + RoHS — technical file kept 10 years."),
    (ELEC, CE, QC_D, CON, 3, 1, 2, 1, CE_TECH, "Compliance consultant compiles CE files."),
    (METAL, CE, QC_D, OP, 3, 2, 2, 1, CE_EU, "Machinery Reg/Directive where building machinery."),
    (PLAST, CE, QC_D, OP, 2, 1, 2, 1, CE_EU, "Where moulded item is an in-scope finished product."),
    (JOIN, CE, QC_D, OP, 2, 1, 2, 1, CE_EU, "CPR/CE for construction joinery (windows/doors)."),
    (PACK, CE, QC_D, OP, 1, 0, 1, 1, CE_EU, "Packaging generally out of CE scope (food-contact = 1935/2004)."),

    # ===== Producer responsibility / environmental (EPR) ====================
    (PACK, ENV, QC_D, OP, 3, 1, 3, 2, REPAK, "Packaging producers must report/join Repak (major producer ≥€1m & ≥10t)."),
    (ELEC, ENV, QC_D, OP, 2, 1, 2, 1, WEEE_EU, "WEEE producer registration + RoHS declarations."),
    (PLAST, ENV, QC_D, OP, 2, 1, 2, 1, EPR_IE, "Packaging + SUP obligations where applicable."),
    (METAL, ENV, QC_D, OP, 1, 0, 1, 1, EPR_IE, "Waste-metal/permit + any packaging placed."),
    (JOIN, ENV, QC_D, OP, 1, 0, 1, 1, EPR_IE, "Wood-waste streams + packaging."),

    # ===== Quote / estimating tool (high revenue/pain across all) ===========
    (METAL, QUOTE, SALES, OP, 0, 3, 3, 3, EST_SW, "Quoting is slow/inconsistent → won/lost margin."),
    (JOIN, QUOTE, SALES, OP, 0, 3, 3, 3, EST_SW, "Bespoke joinery estimating under-prices labour."),
    (PACK, QUOTE, SALES, OP, 0, 3, 3, 3, EST_SW, "Variable print-job quoting."),
    (PLAST, QUOTE, SALES, OP, 0, 2, 2, 2, PAPERLESS, "Tooling + part-price quoting."),
    (ELEC, QUOTE, SALES, OP, 0, 2, 2, 2, PAPERLESS, "Build/assembly quoting from BOM."),

    # ===== QC inspection & non-conformance (revenue/pain across all) ========
    (METAL, QCINSP, QC_D, OP, 1, 3, 3, 3, QC_SW, "Un-tracked NCs/rework destroy job profit."),
    (PLAST, QCINSP, QC_D, OP, 1, 2, 2, 3, QC_SW, "Dimensional/SPC + scrap NCs."),
    (PACK, QCINSP, QC_D, OP, 1, 2, 2, 3, QC_SW, "Colour/registration NCs."),
    (JOIN, QCINSP, QC_D, OP, 1, 2, 2, 2, QC_SW, "Snagging/rework on installs."),
    (ELEC, QCINSP, QC_D, OP, 1, 2, 2, 3, QC_SW, "Functional/AOI test + NC."),
    (METAL, QCINSP, QC_D, AUD, 1, 1, 1, 1, PM_FORUM, "ISO 9001 auditor reviews NC/CAPA."),

    # ===== Production job card / WIP tracker ================================
    (METAL, WIP, JOB, OP, 0, 2, 3, 3, PM_FORUM, "WIP visibility from quote to invoice."),
    (JOIN, WIP, JOB, OP, 0, 2, 2, 3, PM_FORUM, ""),
    (PACK, WIP, JOB, OP, 0, 2, 2, 3, PM_FORUM, "Pre-press→print→finish stages."),
    (ELEC, WIP, JOB, OP, 0, 2, 2, 3, PM_FORUM, "Per build/serial."),
    (PLAST, WIP, JOB, OP, 0, 1, 2, 3, PM_FORUM, ""),

    # ===== Material certificate & traceability ==============================
    (METAL, MATCERT, QC_D, OP, 1, 2, 2, 2, PM_FORUM, "Mill certs/heat numbers for safety-critical work."),
    (ELEC, MATCERT, QC_D, OP, 1, 2, 2, 2, WEEE_EU, "Component traceability + RoHS evidence."),
    (PLAST, MATCERT, QC_D, OP, 1, 1, 1, 2, PM_FORUM, "Resin lot traceability."),
    (PACK, MATCERT, QC_D, OP, 1, 1, 1, 1, PM_FORUM, ""),
    (JOIN, MATCERT, QC_D, OP, 1, 1, 1, 1, PM_FORUM, "Timber source/EUTR where relevant."),

    # ===== Recall / withdrawal (product safety — reused) ====================
    (ELEC, RECALL, QC_D, OP, 2, 1, 2, 1, CE_EU, "Consumer-product safety recall capability (GPSR)."),
    (PLAST, RECALL, QC_D, OP, 1, 1, 1, 1, CE_EU, "Finished consumer products."),
    (METAL, RECALL, QC_D, OP, 1, 1, 1, 1, CE_EU, ""),
    (JOIN, RECALL, QC_D, OP, 1, 1, 1, 1, CE_EU, ""),

    # ===== Batch / yield (scrap) — reused ===================================
    (PLAST, BATCH, OPS, OP, 0, 3, 3, 3, EST_SW, "Scrap/short-shot rate erodes margin invisibly."),
    (METAL, BATCH, OPS, OP, 0, 2, 2, 3, EST_SW, "Batch/run output + scrap."),
    (PACK, BATCH, OPS, OP, 0, 2, 2, 3, EST_SW, "Make-ready waste per run."),
    (ELEC, BATCH, OPS, OP, 0, 2, 2, 3, EST_SW, "Build output + test yield."),
    (JOIN, BATCH, OPS, OP, 0, 1, 2, 2, EST_SW, "Batch/run for repeat product."),

    # ===== BOM & costing — reused ===========================================
    (ELEC, BOM, FIN, OP, 0, 3, 3, 2, PAPERLESS, "Component BOM cost + obsolescence."),
    (METAL, BOM, FIN, OP, 0, 3, 2, 2, EST_SW, "Material+labour cost per part."),
    (JOIN, BOM, FIN, OP, 0, 3, 2, 2, EST_SW, "Cutting-list/material cost."),
    (PLAST, BOM, FIN, OP, 0, 2, 2, 2, EST_SW, ""),
    (PACK, BOM, FIN, OP, 0, 2, 2, 2, EST_SW, ""),

    # ===== Production planning & scheduling — reused ========================
    (METAL, PLAN, JOB, OP, 0, 2, 3, 3, PM_FORUM, "Capacity/lead-time scheduling of jobs."),
    (PLAST, PLAN, JOB, OP, 0, 2, 2, 3, PM_FORUM, "Press scheduling vs orders."),
    (PACK, PLAN, JOB, OP, 0, 2, 2, 3, PM_FORUM, ""),
    (JOIN, PLAN, JOB, OP, 0, 2, 2, 2, PM_FORUM, ""),
    (ELEC, PLAN, JOB, OP, 0, 1, 2, 2, PM_FORUM, ""),

    # ===== OEE / downtime dashboard — reused ================================
    (PLAST, OEE, KPI, OP, 0, 2, 3, 2, QC_SW, "Cycle-time/OEE blind spots; mould downtime."),
    (METAL, OEE, KPI, OP, 0, 2, 2, 2, QC_SW, "Machine utilisation/downtime."),
    (PACK, OEE, KPI, OP, 0, 2, 2, 2, QC_SW, ""),
    (ELEC, OEE, KPI, OP, 0, 1, 1, 2, QC_SW, ""),
    (JOIN, OEE, KPI, OP, 0, 1, 1, 2, QC_SW, ""),

    # ===== Maintenance / PPM — reused (moulds/tools/plant) ==================
    (PLAST, PPM, MAINT, OP, 1, 2, 3, 2, HSA_EQUIP, "Mould/tool maintenance critical to uptime."),
    (METAL, PPM, MAINT, OP, 1, 1, 2, 2, HSA_EQUIP, "CNC/press maintenance."),
    (PACK, PPM, MAINT, OP, 1, 1, 2, 2, HSA_EQUIP, "Press maintenance."),
    (JOIN, PPM, MAINT, OP, 1, 1, 1, 2, HSA_EQUIP, ""),
    (ELEC, PPM, MAINT, OP, 1, 0, 1, 2, HSA_EQUIP, ""),

    # ===== Calibration log — reused (measuring/test equipment) ==============
    (METAL, CAL, QC_D, OP, 1, 1, 2, 2, QC_SW, "Gauge/CMM calibration for dimensional QC."),
    (ELEC, CAL, QC_D, OP, 1, 1, 2, 2, QC_SW, "Test-equipment calibration."),
    (PLAST, CAL, QC_D, OP, 1, 1, 1, 2, QC_SW, ""),
    (PACK, CAL, QC_D, OP, 1, 0, 1, 1, QC_SW, ""),
    (JOIN, CAL, QC_D, OP, 1, 0, 1, 1, QC_SW, ""),

    # ===== Supplier approval — reused =======================================
    (ELEC, SUPP, PROC, OP, 1, 2, 2, 2, WEEE_EU, "Component supplier + RoHS conformity."),
    (METAL, SUPP, PROC, OP, 1, 1, 2, 2, PM_FORUM, "Material supplier approval (ISO 9001)."),
    (PLAST, SUPP, PROC, OP, 1, 1, 1, 2, PM_FORUM, ""),
    (PACK, SUPP, PROC, OP, 1, 1, 1, 1, PM_FORUM, ""),
    (JOIN, SUPP, PROC, OP, 1, 1, 1, 1, PM_FORUM, ""),

    # ===== Raw-material inventory — reused ==================================
    (METAL, RAW, PROC, OP, 0, 2, 2, 3, EST_SW, "Steel/consumable stock + reorder."),
    (PLAST, RAW, PROC, OP, 0, 2, 2, 3, EST_SW, "Polymer/masterbatch stock."),
    (JOIN, RAW, PROC, OP, 0, 2, 2, 2, EST_SW, "Timber/board/ironmongery stock."),
    (PACK, RAW, PROC, OP, 0, 2, 2, 2, EST_SW, "Board/film/ink stock."),
    (ELEC, RAW, PROC, OP, 0, 2, 2, 2, EST_SW, "Component stock + kitting."),

    # ===== Dispatch / delivery note — reused-new ============================
    (METAL, DISPATCH, SALES, OP, 0, 1, 2, 3, PM_FORUM, "Proof of delivery + traceability."),
    (PACK, DISPATCH, SALES, OP, 0, 1, 2, 3, PM_FORUM, ""),
    (PLAST, DISPATCH, SALES, OP, 0, 1, 1, 3, PM_FORUM, ""),
    (ELEC, DISPATCH, SALES, OP, 0, 1, 2, 3, PM_FORUM, "Serial-linked dispatch."),
    (JOIN, DISPATCH, SALES, OP, 0, 1, 1, 2, PM_FORUM, ""),

    # ===== Cashflow / P&L — reused ==========================================
    (METAL, CF, FIN, OP, 0, 3, 3, 3, EST_SW, ""),
    (PLAST, CF, FIN, OP, 0, 3, 2, 3, EST_SW, "Material-cost volatility."),
    (PACK, CF, FIN, OP, 0, 3, 2, 3, EST_SW, ""),
    (JOIN, CF, FIN, OP, 0, 3, 3, 3, EST_SW, ""),
    (ELEC, CF, FIN, OP, 0, 3, 2, 3, EST_SW, ""),

    # ===== Wholesale order & B2B invoice — reused ===========================
    (METAL, B2B, SALES, OP, 0, 3, 2, 3, EST_SW, "OEM/contract B2B invoicing."),
    (PLAST, B2B, SALES, OP, 0, 3, 1, 3, EST_SW, ""),
    (PACK, B2B, SALES, OP, 0, 3, 2, 3, EST_SW, ""),
    (ELEC, B2B, SALES, OP, 0, 2, 1, 2, EST_SW, ""),
    (JOIN, B2B, SALES, OP, 0, 2, 2, 2, EST_SW, ""),

    # ===== Training matrix — reused (machinery competence) ==================
    (METAL, TRN, HR, OP, 2, 1, 2, 1, HSA_EQUIP, "Machinery/abrasive-wheel competence records."),
    (JOIN, TRN, HR, OP, 2, 1, 2, 1, HSA_EQUIP, "Woodworking-machine competence."),
    (PLAST, TRN, HR, OP, 2, 0, 1, 1, HSA_EQUIP, ""),
    (PACK, TRN, HR, OP, 2, 0, 1, 1, HSA_EQUIP, ""),
    (ELEC, TRN, HR, OP, 1, 0, 1, 1, HSA_EQUIP, "ESD/soldering competence."),

    # ===== ISO 9001 internal audit & management review — new ================
    (METAL, AUDIT9001, QC_D, OP, 1, 2, 2, 1, PM_FORUM, "ISO 9001 is a frequent customer/tender requirement."),
    (PLAST, AUDIT9001, QC_D, OP, 1, 2, 2, 1, PM_FORUM, ""),
    (ELEC, AUDIT9001, QC_D, OP, 1, 2, 2, 1, PM_FORUM, ""),
    (PACK, AUDIT9001, QC_D, OP, 1, 1, 1, 1, PM_FORUM, ""),
    (JOIN, AUDIT9001, QC_D, OP, 1, 1, 1, 1, PM_FORUM, ""),
    (METAL, AUDIT9001, QC_D, CON, 1, 2, 2, 1, PM_FORUM, "ISO consultant readies shop for certification."),
]

# --- pain points ------------------------------------------------------------
# (business_type, description, severity, source_url)
PAINS = [
    (METAL, "Quoting is slow and inconsistent (spreadsheet guesswork) → won/lost margin.", "severe", EST_SW),
    (METAL, "Un-tracked non-conformances and rework quietly destroy job profit.", "severe", QC_SW),
    (METAL, "ISO 9001 audit document load (NC/CAPA, calibration, supplier approval).", "real", PM_FORUM),
    (METAL, "Material/mill-cert traceability for safety-critical work.", "real", PM_FORUM),
    (PLAST, "Scrap/short-shot rate erodes margin invisibly without batch records.", "severe", EST_SW),
    (PLAST, "Mould/tool downtime and cycle-time/OEE blind spots.", "real", QC_SW),
    (PLAST, "Material-cost volatility on polymer/masterbatch.", "real", EST_SW),
    (PACK, "Quoting accuracy on highly variable print jobs.", "severe", EST_SW),
    (PACK, "EPR/Repak packaging reporting burden.", "real", REPAK),
    (PACK, "Solvent/VOC chemical-agent compliance and make-ready waste.", "real", HSA_GENAPP),
    (JOIN, "Bespoke estimating is slow and under-prices labour.", "severe", EST_SW),
    (JOIN, "Hardwood-dust exposure compliance (LEV) — wood dust is a carcinogen.", "severe", HSA_GENAPP),
    (JOIN, "Timber wastage / cutting optimisation and CE/CPR paperwork for windows/doors.", "real", CE_EU),
    (ELEC, "CE/RoHS/EMC technical-file burden for small product runs.", "severe", CE_EU),
    (ELEC, "Component traceability and obsolescence management.", "real", WEEE_EU),
    (ELEC, "Test-yield / non-conformance tracking and WEEE registration admin.", "real", WEEE_EU),
]


def tier_for(legal, score):
    if legal == 3 or score >= 16:
        return "MUST"
    if score >= 10:
        return "SHOULD"
    if score >= 5:
        return "COULD"
    return "WON'T"


def main():
    ap = argparse.ArgumentParser(description="Seed non-food manufacturing (Phase 3) rows.")
    ap.add_argument("--db", default=DEFAULT_DB)
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        # Upsert NEW digital assets (unique by name). Reused assets untouched.
        for name, (atype, desc) in ASSETS.items():
            conn.execute(
                "INSERT INTO digital_assets (name, asset_type, description) VALUES (?,?,?) "
                "ON CONFLICT(name) DO UPDATE SET asset_type=excluded.asset_type, description=excluded.description;",
                (name, atype, desc),
            )
        conn.commit()

        name_to_id = {n: i for i, n in conn.execute("SELECT id, name FROM digital_assets")}
        for n in (BATCH, BOM, PLAN, CAL, SUPP, RAW, CF, B2B, OEE, PPM, TRN, HS, FIRE, RECALL):
            if n not in name_to_id:
                raise RuntimeError(f"Reused asset missing from DB (run Phases 1-2 first): {n}")

        # Idempotency: clear this phase's rows (business types 11-15).
        conn.execute("DELETE FROM asset_map WHERE business_type_id IN (11,12,13,14,15);")
        conn.execute("DELETE FROM pain_points WHERE business_type_id IN (11,12,13,14,15);")

        inserted = 0
        for bt, aname, dept, buyer, L, R, P, F, ev, notes in ROWS:
            score = L * 3 + R * 2 + P * 2 + F
            tier = tier_for(L, score)
            if tier in ("MUST", "SHOULD") and not ev:
                raise ValueError(f"MUST/SHOULD row without evidence: bt={bt} asset={aname}")
            conn.execute(
                "INSERT INTO asset_map "
                "(business_type_id, department_id, asset_id, buyer, legal, revenue, pain, frequency, score, tier, evidence_url, notes) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?);",
                (bt, dept, name_to_id[aname], buyer, L, R, P, F, score, tier, ev, notes or None),
            )
            inserted += 1

        for bt, desc, sev, src in PAINS:
            conn.execute(
                "INSERT INTO pain_points (business_type_id, description, severity, source_url) VALUES (?,?,?,?);",
                (bt, desc, sev, src),
            )
        conn.commit()

        n_assets = conn.execute("SELECT COUNT(*) FROM digital_assets").fetchone()[0]
        n_map = conn.execute("SELECT COUNT(*) FROM asset_map").fetchone()[0]
        n_phase = conn.execute("SELECT COUNT(*) FROM asset_map WHERE business_type_id IN (11,12,13,14,15)").fetchone()[0]
        n_pain = conn.execute("SELECT COUNT(*) FROM pain_points").fetchone()[0]
        by_tier = dict(conn.execute(
            "SELECT tier, COUNT(*) FROM asset_map WHERE business_type_id IN (11,12,13,14,15) GROUP BY tier"))
        print(f"Seeded non-food manufacturing: {inserted} asset_map rows (bt 11-15), {len(ASSETS)} new assets, {len(PAINS)} pain points.")
        print(f"  digital_assets total    : {n_assets}")
        print(f"  asset_map total         : {n_map}")
        print(f"  asset_map phase-3 rows  : {n_phase}")
        print(f"  pain_points total       : {n_pain}")
        print(f"  phase-3 by tier         : {by_tier}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
