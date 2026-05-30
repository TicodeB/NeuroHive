#!/usr/bin/env python3
"""
ASSET-FORGE — Phase 2 seed: FOOD MANUFACTURING research rows.

Inserts food-manufacturing digital assets (NEW functions only — existing
hospitality assets that cover the same FUNCTION are reused by id, not
re-created), the scored asset_map rows (raw 0-3 axis scores per rubric [6] +
buyer tag + evidence_url) and pain points for the five food-manufacturing
business types (Bakery, Butchery/meat, Dairy, Beverage, Ready meals).

Score = (legal*3) + (revenue*2) + (pain*2) + (frequency*1), max 24.
Tier:  MUST  if score >= 16 OR legal == 3 (legal-mandatory auto-promotes)
       SHOULD 10-15 · COULD 5-9 · WON'T < 5.

Idempotent: deletes this phase's rows first (business types 6-10), then
re-inserts. New digital_assets are upserted by unique name; existing reused
assets are referenced by name and never overwritten.

Usage:
    python3 scripts/seed_manufacturing_food.py [--db PATH]
"""

import argparse
import os
import sqlite3
import sys

DEFAULT_DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "intelligence.db")

# Food-manufacturing business_type ids (seeded in Phase 0).
BAKERY, MEAT, DAIRY, BEV, READY = 6, 7, 8, 9, 10

# Department ids (Phase 0 seed).
OPS, QC, HR, FIN, SALES, PROC, MAINT, FOH, JOB, KPI = range(1, 11)

# --- Evidence URLs (verified LIVE in Phase 2) -------------------------------
FSAI_START = "https://www.fsai.ie/business-advice/starting-a-food-business/business-start-up-information-factsheet"
FSAI_853 = "https://www.fsai.ie/enforcement-and-legislation/legislation/food-legislation/food-hygiene/specific-hygiene-rules-for-food-of-animal-origin"
FSAI_APPROVAL = "https://www.fsai.ie/getattachment/380ffd12-a55b-42eb-b434-5dcd8acca1b6/final-guidance-on-the-approval-of-food-establishments.pdf?lang=en-IE&ext=.pdf"
FSAI_IDMARK = "https://www.fsai.ie/enforcement-and-legislation/legislation/food-legislation/meat-fresh-meat/identification-marking-and-labelling"
FSAI_NUTRI = "https://www.fsai.ie/business-advice/labelling/labelling-nutrition-information/nutrition-labelling"
FSAI_FIC = "https://www.fsai.ie/business-advice/labelling/food-information-to-consumers"
FSAI_ALLERGEN = "https://www.fsai.ie/business-advice/running-a-food-business/allergens"
NSAI_QTY = "https://www.nsai.ie/legal-metrology/control-of-quantities/"
NSAI_EMARK = "https://www.nsai.ie/legal-metrology/enforcement-information/inspection-types/packaged-good-inspection/emark/"
HSA_SS = "https://www.hsa.ie/eng/topics/managing_health_and_safety/safety_statement_and_risk_assessment/"

# --- NEW food-manufacturing assets (deduped by FUNCTION) --------------------
# name -> (asset_type, description). Existing hospitality assets are NOT listed
# here (they are reused by name below) so their descriptions are never clobbered.
ASSETS = {
    "Batch Production & Yield Record": ("Log book", "Per-batch production record: inputs, process parameters, output yield and wastage/variance vs theoretical — the core manufacturing run record and a HACCP evidence base."),
    "Recipe / BOM & Batch Costing Calculator": ("Calculator", "Bill-of-materials per product, batch/unit costing, ingredient-price sensitivity and gross-margin modelling at production scale."),
    "Product Label & Nutrition Declaration Generator": ("Calculator", "Builds Reg 1169/2011-compliant prepacked labels: ingredient list + QUID, emphasised allergens, nutrition declaration per 100 g/ml (tabular), net quantity, date marking."),
    "Approved Establishment File & Health-Mark Control (Reg 853/2004)": ("Form/checklist", "Compliance file for an approved establishment handling products of animal origin: approval number, identification/health-mark control, Annex III structural & process requirements (meat/dairy)."),
    "Net-Quantity & Average-Quantity (e-mark) Control Sheet": ("Spreadsheet tracker", "Average-quantity-system fill control: tare, nominal vs actual fill, TU1/TU2 tolerances and e-mark conformance evidence (Packaged Goods Act 1980 / NSAI)."),
    "Shelf-Life, Durability & Date-Coding Record": ("Log book", "Shelf-life/durability study results, use-by vs best-before assignment and date-code/batch-code issue log."),
    "Raw Material Inventory & FIFO/FEFO Stock Rotation": ("Spreadsheet tracker", "Ingredient/packaging stock with batch links, min/max reorder points and FIFO/FEFO rotation to cut spoilage."),
    "Supplier Approval & Specification Register": ("Database", "Approved-supplier list with product specs, certificates of analysis/conformance and approval status — a retail-supply prerequisite."),
    "Production Planning & Scheduling Sheet": ("Roster/scheduler", "Plans production runs against orders, capacity and ingredient availability to avoid over/under-production."),
    "Calibration Log (Scales, Thermometers, Probes)": ("Log book", "Calibration schedule and results for measuring equipment underpinning CCPs and net-quantity control."),
    "Foreign-Body & Glass/Hard-Plastic Control Register": ("Form/checklist", "Physical-contamination control: glass/hard-plastic & knife/blade registers and breakage procedure (BRCGS prerequisite)."),
    "Pest Control Monitoring Log": ("Log book", "Bait-station/EFK inspection records and trend monitoring — a HACCP prerequisite programme."),
    "Wholesale Order & B2B Invoice Tool": ("Invoice template", "Trade order capture and VAT invoicing for wholesale/foodservice/retail customers."),
    "Production KPI & Downtime (OEE) Dashboard": ("Dashboard", "Overall-equipment-effectiveness, downtime, yield and wastage KPIs for a small production line."),
    "Internal Audit & GMP Self-Inspection Checklist": ("Form/checklist", "GMP/GHP self-inspection and internal-audit programme readying a producer for BRCGS/IFS/SALSA certification."),
    "Recall / Withdrawal Plan & Mock-Recall Log": ("Form/checklist", "Product withdrawal/recall procedure, contact tree, mass-balance reconciliation and mock-recall test log (Reg 178/2002 Art 19)."),
}

# --- Reused existing hospitality assets (by name) ---------------------------
HACCP = "HACCP Food Safety Management System"
ALLERGEN = "Allergen Matrix & Menu Declaration Tool"
TMP = "Temperature Monitoring Log"
CLN = "Cleaning & Sanitation Schedule"
TRC = "Supplier & Delivery Traceability Log"
CF = "Cashflow & P&L Tracker"
TRN = "Staff Training & Induction Matrix"
PPM = "Maintenance & PPM Asset Register"
HS = "H&S Risk Assessment & Safety Statement"
FIRE = "Fire Safety Register & Checks Log"

# --- New asset short-keys ---------------------------------------------------
BATCH = "Batch Production & Yield Record"
BOM = "Recipe / BOM & Batch Costing Calculator"
LABEL = "Product Label & Nutrition Declaration Generator"
APPROVE = "Approved Establishment File & Health-Mark Control (Reg 853/2004)"
QTY = "Net-Quantity & Average-Quantity (e-mark) Control Sheet"
SHELF = "Shelf-Life, Durability & Date-Coding Record"
RAW = "Raw Material Inventory & FIFO/FEFO Stock Rotation"
SUPP = "Supplier Approval & Specification Register"
PLAN = "Production Planning & Scheduling Sheet"
CAL = "Calibration Log (Scales, Thermometers, Probes)"
FB = "Foreign-Body & Glass/Hard-Plastic Control Register"
PEST = "Pest Control Monitoring Log"
B2B = "Wholesale Order & B2B Invoice Tool"
OEE = "Production KPI & Downtime (OEE) Dashboard"
AUDIT = "Internal Audit & GMP Self-Inspection Checklist"
RECALL = "Recall / Withdrawal Plan & Mock-Recall Log"

OP, AUD, CON = "operator", "auditor", "consultant"

# --- asset_map rows ---------------------------------------------------------
# (business_type, asset_name, department, buyer, legal, revenue, pain, frequency, evidence_url, notes)
ROWS = [
    # ===== Food-safety MUST floor (Legal=3) across all five =================
    (BAKERY, HACCP, QC, OP, 3, 1, 2, 3, FSAI_START, "Documented HACCP system required of every food business."),
    (MEAT, HACCP, QC, OP, 3, 2, 3, 3, FSAI_START, ""),
    (DAIRY, HACCP, QC, OP, 3, 2, 3, 3, FSAI_START, "Pasteurisation/heat-treatment CCPs."),
    (BEV, HACCP, QC, OP, 3, 1, 2, 3, FSAI_START, ""),
    (READY, HACCP, QC, OP, 3, 2, 3, 3, FSAI_START, "Cook/chill CCP-heavy operation."),
    (READY, HACCP, QC, CON, 3, 2, 2, 2, FSAI_START, "Food-safety consultant builds HACCP for producers."),

    (BAKERY, ALLERGEN, QC, OP, 3, 2, 3, 3, FSAI_ALLERGEN, "Gluten/wheat/nuts/egg/milk dominate — high SKU allergen load."),
    (READY, ALLERGEN, QC, OP, 3, 2, 3, 3, FSAI_ALLERGEN, "Allergen matrix across many changing SKUs."),
    (MEAT, ALLERGEN, QC, OP, 2, 1, 2, 2, FSAI_ALLERGEN, "Seasoned/processed lines (sausage rusk = gluten)."),
    (DAIRY, ALLERGEN, QC, OP, 3, 1, 2, 2, FSAI_ALLERGEN, "Milk is itself a declarable allergen + cross-contact."),
    (BEV, ALLERGEN, QC, OP, 2, 1, 1, 2, FSAI_ALLERGEN, "Sulphites/other allergens declarable (incl. alcoholic)."),

    (MEAT, TMP, QC, OP, 3, 2, 3, 3, FSAI_853, "Cold chain at every step of cutting/storage."),
    (DAIRY, TMP, QC, OP, 3, 2, 3, 3, FSAI_853, "Raw-milk intake + product cold chain."),
    (READY, TMP, QC, OP, 3, 2, 3, 3, FSAI_START, "Cook/chill/reheat CCP temperatures."),
    (BAKERY, TMP, QC, OP, 2, 1, 1, 2, FSAI_START, "Chilled fillings/proving control."),
    (BEV, TMP, QC, OP, 2, 1, 1, 2, FSAI_START, "Where chilled/short-life beverages."),

    (BAKERY, CLN, QC, OP, 3, 1, 2, 3, FSAI_START, "Good-hygiene-practice evidence."),
    (MEAT, CLN, QC, OP, 3, 1, 3, 3, FSAI_853, "Sanitation critical on animal-origin lines."),
    (DAIRY, CLN, QC, OP, 3, 1, 3, 3, FSAI_853, "CIP/sanitation of plant."),
    (BEV, CLN, QC, OP, 3, 1, 2, 3, FSAI_START, ""),
    (READY, CLN, QC, OP, 3, 1, 2, 3, FSAI_START, ""),

    (BAKERY, TRC, QC, OP, 3, 1, 2, 3, FSAI_START, "One-step-back/forward (Reg 178/2002)."),
    (MEAT, TRC, QC, OP, 3, 2, 3, 3, FSAI_853, "Carcass-to-cut traceability."),
    (DAIRY, TRC, QC, OP, 3, 2, 2, 3, FSAI_853, ""),
    (BEV, TRC, QC, OP, 3, 1, 2, 2, FSAI_START, ""),
    (READY, TRC, QC, OP, 3, 2, 2, 3, FSAI_START, ""),

    # ===== H&S + fire MUST floor (Legal=3) ==================================
    (BAKERY, HS, QC, OP, 3, 1, 2, 1, HSA_SS, ""),
    (MEAT, HS, QC, OP, 3, 1, 2, 1, HSA_SS, "Blades/saws raise risk profile."),
    (DAIRY, HS, QC, OP, 3, 1, 2, 1, HSA_SS, ""),
    (BEV, HS, QC, OP, 3, 1, 2, 1, HSA_SS, ""),
    (READY, HS, QC, OP, 3, 1, 2, 1, HSA_SS, ""),

    (BAKERY, FIRE, QC, OP, 3, 0, 2, 2, HSA_SS, "Ovens raise fire load."),
    (MEAT, FIRE, QC, OP, 3, 0, 1, 2, HSA_SS, ""),
    (DAIRY, FIRE, QC, OP, 3, 0, 1, 2, HSA_SS, ""),
    (BEV, FIRE, QC, OP, 3, 0, 1, 2, HSA_SS, ""),
    (READY, FIRE, QC, OP, 3, 0, 2, 2, HSA_SS, ""),

    # ===== 853/2004 approved-establishment file (Legal=3, meat & dairy only) =
    (MEAT, APPROVE, QC, OP, 3, 2, 3, 2, FSAI_853, "Approval + health/identification mark is licence-to-operate."),
    (MEAT, APPROVE, QC, AUD, 3, 1, 2, 1, FSAI_APPROVAL, "DAFM/EHO auditor inspects against Annex III."),
    (DAIRY, APPROVE, QC, OP, 3, 2, 3, 2, FSAI_853, "Approval required for dairy products of animal origin."),
    (DAIRY, APPROVE, QC, AUD, 3, 1, 2, 1, FSAI_APPROVAL, ""),

    # ===== Label & nutrition generator (Legal=3 prepacked; alcohol=2) =======
    (BAKERY, LABEL, QC, OP, 3, 2, 3, 3, FSAI_NUTRI, "Per-SKU FIC label + nutrition; manual creation is a major pain."),
    (READY, LABEL, QC, OP, 3, 2, 3, 3, FSAI_NUTRI, "Large SKU range = biggest labelling liability."),
    (DAIRY, LABEL, QC, OP, 3, 2, 2, 2, FSAI_FIC, ""),
    (BEV, LABEL, QC, OP, 2, 2, 2, 2, FSAI_FIC, "Alcoholic exempt from nutrition; soft drinks require it."),
    (MEAT, LABEL, QC, OP, 3, 1, 2, 2, FSAI_FIC, "Prepacked retail cuts/processed lines."),

    # ===== Net-quantity / e-mark control (Packaged Goods Act 1980) ==========
    (BEV, QTY, QC, OP, 2, 2, 3, 3, NSAI_EMARK, "Fill-volume control on liquids — under/over-fill is legal + margin risk."),
    (BAKERY, QTY, QC, OP, 2, 1, 2, 2, NSAI_QTY, "Net-weight on packaged loaves/products."),
    (DAIRY, QTY, QC, OP, 2, 1, 2, 2, NSAI_QTY, ""),
    (READY, QTY, QC, OP, 2, 1, 2, 2, NSAI_QTY, ""),
    (MEAT, QTY, QC, OP, 2, 1, 2, 2, NSAI_QTY, "Prepacked weighed product."),

    # ===== Traceability sibling: recall / mock-recall (Reg 178/2002) ========
    (MEAT, RECALL, QC, OP, 2, 2, 3, 1, FSAI_START, "Animal-origin recall exposure is severe."),
    (DAIRY, RECALL, QC, OP, 2, 2, 3, 1, FSAI_START, ""),
    (READY, RECALL, QC, OP, 2, 2, 2, 1, FSAI_START, ""),
    (BAKERY, RECALL, QC, OP, 2, 1, 2, 1, FSAI_START, ""),
    (BEV, RECALL, QC, OP, 2, 1, 2, 1, FSAI_START, ""),

    # ===== Core manufacturing run record (universal-core candidate) =========
    (BAKERY, BATCH, OPS, OP, 1, 2, 3, 3, FSAI_START, "Yield/wastage per bake is the margin lever."),
    (MEAT, BATCH, OPS, OP, 1, 3, 3, 3, FSAI_START, "Cutting-yield leakage invisible without records."),
    (DAIRY, BATCH, OPS, OP, 2, 2, 2, 3, FSAI_START, "Doubles as pasteurisation-batch evidence."),
    (BEV, BATCH, OPS, OP, 1, 2, 2, 3, NSAI_QTY, "Brew/blend batch consistency."),
    (READY, BATCH, OPS, OP, 1, 2, 2, 3, FSAI_START, ""),

    # ===== Recipe / BOM & batch costing =====================================
    (BAKERY, BOM, FIN, OP, 0, 3, 3, 2, FSAI_START, "Un-costed recipes + ingredient swings destroy thin margins."),
    (MEAT, BOM, FIN, OP, 0, 3, 2, 2, FSAI_START, "Carcass-to-cut costing."),
    (READY, BOM, FIN, OP, 0, 3, 3, 2, FSAI_START, "Fixed-price B2B contracts demand accurate costing."),
    (BEV, BOM, FIN, OP, 0, 2, 2, 2, NSAI_QTY, ""),
    (DAIRY, BOM, FIN, OP, 0, 2, 2, 2, FSAI_START, ""),

    # ===== Shelf-life & date-coding =========================================
    (BAKERY, SHELF, QC, OP, 2, 1, 2, 3, FSAI_FIC, "Short shelf-life; date-marking is mandatory info."),
    (READY, SHELF, QC, OP, 2, 2, 2, 3, FSAI_FIC, "Use-by validation on cook/chill."),
    (DAIRY, SHELF, QC, OP, 2, 1, 2, 2, FSAI_FIC, ""),
    (BEV, SHELF, QC, OP, 1, 1, 1, 2, FSAI_FIC, ""),
    (MEAT, SHELF, QC, OP, 2, 1, 2, 2, FSAI_FIC, ""),

    # ===== Raw-material inventory & FIFO/FEFO ===============================
    (BAKERY, RAW, PROC, OP, 0, 2, 2, 3, FSAI_START, "Spoilage of perishable ingredients."),
    (READY, RAW, PROC, OP, 0, 2, 2, 3, FSAI_START, ""),
    (MEAT, RAW, PROC, OP, 0, 2, 2, 3, FSAI_START, ""),
    (DAIRY, RAW, PROC, OP, 0, 2, 2, 3, FSAI_START, ""),
    (BEV, RAW, PROC, OP, 0, 1, 1, 2, FSAI_START, ""),

    # ===== Supplier approval & specification register =======================
    (READY, SUPP, PROC, OP, 1, 1, 2, 2, FSAI_START, "Approved-supplier control is a retail-supply gate."),
    (MEAT, SUPP, PROC, OP, 2, 1, 2, 2, FSAI_853, "Animal-origin supplier approval."),
    (DAIRY, SUPP, PROC, OP, 2, 1, 2, 2, FSAI_853, ""),
    (BAKERY, SUPP, PROC, OP, 1, 1, 1, 1, FSAI_START, ""),
    (BEV, SUPP, PROC, OP, 1, 1, 1, 1, FSAI_START, ""),

    # ===== Calibration log (CCP + net-quantity devices) =====================
    (DAIRY, CAL, QC, OP, 2, 1, 2, 2, NSAI_QTY, "Probe/thermometer calibration underpins pasteurisation CCP."),
    (MEAT, CAL, QC, OP, 2, 1, 2, 2, NSAI_QTY, ""),
    (READY, CAL, QC, OP, 2, 1, 2, 2, NSAI_QTY, ""),
    (BEV, CAL, QC, OP, 2, 1, 1, 2, NSAI_EMARK, "Fill-line scale calibration for e-mark."),
    (BAKERY, CAL, QC, OP, 1, 0, 1, 2, NSAI_QTY, ""),

    # ===== Foreign-body / glass control (BRCGS prerequisite) ================
    (MEAT, FB, QC, OP, 1, 1, 2, 2, FSAI_START, "Knife/blade & metal control."),
    (READY, FB, QC, OP, 1, 1, 2, 2, FSAI_START, ""),
    (BAKERY, FB, QC, OP, 1, 1, 1, 2, FSAI_START, ""),
    (DAIRY, FB, QC, OP, 1, 1, 1, 2, FSAI_START, ""),
    (BEV, FB, QC, OP, 1, 1, 2, 2, FSAI_START, "Glass-bottling foreign-body risk."),

    # ===== Pest control monitoring (HACCP prerequisite) =====================
    (BAKERY, PEST, QC, OP, 2, 0, 2, 2, FSAI_START, "Flour stores attract pests."),
    (MEAT, PEST, QC, OP, 2, 0, 2, 2, FSAI_853, ""),
    (DAIRY, PEST, QC, OP, 2, 0, 1, 2, FSAI_853, ""),
    (READY, PEST, QC, OP, 2, 0, 1, 2, FSAI_START, ""),
    (BEV, PEST, QC, OP, 2, 0, 1, 2, FSAI_START, ""),

    # ===== Production planning & scheduling =================================
    (READY, PLAN, JOB, OP, 0, 2, 2, 3, FSAI_START, "Plan-to-order avoids over/under-production."),
    (BAKERY, PLAN, JOB, OP, 0, 2, 2, 3, FSAI_START, "Daily bake plan vs orders."),
    (MEAT, PLAN, JOB, OP, 0, 1, 1, 2, FSAI_START, ""),
    (BEV, PLAN, JOB, OP, 0, 1, 1, 2, FSAI_START, ""),
    (DAIRY, PLAN, JOB, OP, 0, 1, 1, 2, FSAI_START, ""),

    # ===== Cashflow / P&L (reused) ==========================================
    (BAKERY, CF, FIN, OP, 0, 3, 3, 3, FSAI_START, ""),
    (MEAT, CF, FIN, OP, 0, 3, 2, 3, FSAI_START, ""),
    (DAIRY, CF, FIN, OP, 0, 3, 2, 3, FSAI_START, "Milk-price volatility."),
    (BEV, CF, FIN, OP, 0, 3, 2, 3, FSAI_START, "Excise/duty cash impact for alcohol."),
    (READY, CF, FIN, OP, 0, 3, 2, 3, FSAI_START, ""),

    # ===== Wholesale order & B2B invoice ====================================
    (READY, B2B, SALES, OP, 0, 3, 2, 3, FSAI_START, "B2B contract-driven sales."),
    (BAKERY, B2B, SALES, OP, 0, 2, 2, 3, FSAI_START, "Wholesale rounds + counter."),
    (DAIRY, B2B, SALES, OP, 0, 2, 1, 2, FSAI_START, ""),
    (MEAT, B2B, SALES, OP, 0, 2, 1, 2, FSAI_START, ""),
    (BEV, B2B, SALES, OP, 0, 2, 1, 2, FSAI_START, "Distribution invoicing."),

    # ===== Training matrix (reused; food-safety training expected) ==========
    (MEAT, TRN, HR, OP, 2, 1, 2, 1, FSAI_START, "Food-safety + equipment training records."),
    (DAIRY, TRN, HR, OP, 2, 1, 1, 1, FSAI_START, ""),
    (READY, TRN, HR, OP, 2, 1, 2, 1, FSAI_START, ""),
    (BAKERY, TRN, HR, OP, 2, 1, 1, 1, FSAI_START, ""),
    (BEV, TRN, HR, OP, 2, 0, 1, 1, FSAI_START, ""),

    # ===== Maintenance / PPM (reused) =======================================
    (DAIRY, PPM, MAINT, OP, 1, 1, 2, 2, HSA_SS, "Plant uptime + hygienic condition."),
    (BEV, PPM, MAINT, OP, 1, 1, 2, 2, HSA_SS, "Bottling/fill line uptime."),
    (BAKERY, PPM, MAINT, OP, 1, 1, 2, 2, HSA_SS, "Oven/mixer maintenance."),
    (MEAT, PPM, MAINT, OP, 1, 1, 1, 2, HSA_SS, ""),
    (READY, PPM, MAINT, OP, 1, 1, 1, 2, HSA_SS, ""),

    # ===== Internal audit / GMP self-inspection (cert readiness) ============
    (READY, AUDIT, QC, CON, 1, 2, 2, 1, FSAI_START, "Consultant readies producer for BRCGS/IFS."),
    (BAKERY, AUDIT, QC, OP, 1, 2, 2, 1, FSAI_START, "SALSA/BRCGS self-inspection."),
    (MEAT, AUDIT, QC, OP, 1, 2, 2, 1, FSAI_START, ""),
    (DAIRY, AUDIT, QC, OP, 1, 2, 2, 1, FSAI_START, ""),
    (BEV, AUDIT, QC, OP, 1, 1, 1, 1, FSAI_START, ""),

    # ===== Production KPI / OEE dashboard ===================================
    (READY, OEE, KPI, OP, 0, 2, 2, 2, FSAI_START, "Downtime/yield visibility on the line."),
    (BEV, OEE, KPI, OP, 0, 2, 2, 2, NSAI_QTY, ""),
    (DAIRY, OEE, KPI, OP, 0, 2, 1, 2, FSAI_START, ""),
    (BAKERY, OEE, KPI, OP, 0, 1, 1, 2, FSAI_START, ""),
    (MEAT, OEE, KPI, OP, 0, 1, 1, 2, FSAI_START, ""),
]

# --- pain points ------------------------------------------------------------
# (business_type, description, severity, source_url)
PAINS = [
    (BAKERY, "Wafer-thin margins destroyed by un-costed recipes and volatile ingredient prices.", "severe", FSAI_START),
    (BAKERY, "Allergen accuracy across a wide SKU range (gluten/nuts/egg/milk) is high-liability.", "severe", FSAI_ALLERGEN),
    (BAKERY, "Daily wastage of unsold short-shelf-life stock.", "real", FSAI_START),
    (BAKERY, "Manual per-SKU label + nutrition creation is slow and error-prone.", "real", FSAI_NUTRI),
    (MEAT, "Losing the 853/2004 approval / health-mark audit halts the business.", "severe", FSAI_853),
    (MEAT, "Cutting-yield leakage is invisible without batch/yield records.", "severe", FSAI_START),
    (MEAT, "Cold-chain breaches and recall readiness on animal-origin product.", "severe", FSAI_853),
    (DAIRY, "Pasteurisation/heat-treatment CCP evidence is make-or-break at audit.", "severe", FSAI_853),
    (DAIRY, "Calibration drift invalidates CCP temperature data.", "real", NSAI_QTY),
    (DAIRY, "Thin margins amplified by milk-price volatility.", "real", FSAI_START),
    (BEV, "Under/over-fill on liquids is simultaneously legal exposure and margin loss.", "severe", NSAI_EMARK),
    (BEV, "Excise/duty admin burden for small breweries/distilleries.", "real", FSAI_START),
    (BEV, "Label compliance differs sharply between alcoholic and soft drinks.", "real", FSAI_FIC),
    (READY, "Allergen + label compliance across a large, changing SKU range is the biggest liability.", "severe", FSAI_ALLERGEN),
    (READY, "Cook/chill CCP temperature evidence across the production day.", "severe", FSAI_START),
    (READY, "Costing accuracy on fixed-price B2B contracts.", "real", FSAI_START),
    (READY, "Planning production to order without over/under-production.", "real", FSAI_START),
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
    ap = argparse.ArgumentParser(description="Seed food manufacturing (Phase 2) rows.")
    ap.add_argument("--db", default=DEFAULT_DB)
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        # Upsert NEW digital assets (unique by name). Reused assets are left untouched.
        for name, (atype, desc) in ASSETS.items():
            conn.execute(
                "INSERT INTO digital_assets (name, asset_type, description) VALUES (?,?,?) "
                "ON CONFLICT(name) DO UPDATE SET asset_type=excluded.asset_type, description=excluded.description;",
                (name, atype, desc),
            )
        conn.commit()

        name_to_id = {n: i for i, n in conn.execute("SELECT id, name FROM digital_assets")}
        # Fail loudly if a reused asset name is missing (Phase 1 not seeded).
        for n in (HACCP, ALLERGEN, TMP, CLN, TRC, CF, TRN, PPM, HS, FIRE):
            if n not in name_to_id:
                raise RuntimeError(f"Reused asset missing from DB (run Phase 1 first): {n}")

        # Idempotency: clear this phase's rows (business types 6-10).
        conn.execute("DELETE FROM asset_map WHERE business_type_id IN (6,7,8,9,10);")
        conn.execute("DELETE FROM pain_points WHERE business_type_id IN (6,7,8,9,10);")

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

        # Summary.
        n_assets = conn.execute("SELECT COUNT(*) FROM digital_assets").fetchone()[0]
        n_map = conn.execute("SELECT COUNT(*) FROM asset_map").fetchone()[0]
        n_phase = conn.execute("SELECT COUNT(*) FROM asset_map WHERE business_type_id IN (6,7,8,9,10)").fetchone()[0]
        n_pain = conn.execute("SELECT COUNT(*) FROM pain_points").fetchone()[0]
        by_tier = dict(conn.execute(
            "SELECT tier, COUNT(*) FROM asset_map WHERE business_type_id IN (6,7,8,9,10) GROUP BY tier"))
        print(f"Seeded food manufacturing: {inserted} asset_map rows (bt 6-10), {len(ASSETS)} new assets, {len(PAINS)} pain points.")
        print(f"  digital_assets total   : {n_assets}")
        print(f"  asset_map total        : {n_map}")
        print(f"  asset_map phase-2 rows : {n_phase}")
        print(f"  pain_points total      : {n_pain}")
        print(f"  phase-2 by tier        : {by_tier}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
