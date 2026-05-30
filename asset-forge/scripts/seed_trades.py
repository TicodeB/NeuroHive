#!/usr/bin/env python3
"""
ASSET-FORGE — Phase 4 seed: TRADES research rows.

Inserts trades-specific digital assets (NEW functions only — existing assets
covering the same FUNCTION are reused by id, not re-created), the scored
asset_map rows (raw 0-3 axis scores per rubric [6] + buyer tag + evidence_url +
work-context note) and pain points for the six trades business types
(Electrician, Plumber/heating, Carpenter/joiner, Painter/decorator, Tiler,
Landscaper/groundworks). Also sets `business_types.work_context` per trade.

Score = (legal*3) + (revenue*2) + (pain*2) + (frequency*1), max 24.
Tier:  MUST  if score >= 16 OR legal == 3 (legal-mandatory auto-promotes)
       SHOULD 10-15 · COULD 5-9 · WON'T < 5.

Trades work-context modifier (Section [5]) is stored in business_types.work_context
and echoed per row in asset_map.notes (solo/team · on-site/workshop-off-site/on-the-road).

Idempotent: deletes this phase's rows first (business types 16-21), then
re-inserts. New digital_assets are upserted by unique name; existing reused
assets are referenced by name and never overwritten.

Usage:
    python3 scripts/seed_trades.py [--db PATH]
"""

import argparse
import os
import sqlite3
import sys

DEFAULT_DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "intelligence.db")

# Trades business_type ids (seeded in Phase 0).
ELECN, PLUMB, CARP, PAINT, TILE, LAND = 16, 17, 18, 19, 20, 21
TRADES_BTS = (ELECN, PLUMB, CARP, PAINT, TILE, LAND)

# Department ids (Phase 0 seed).
OPS, QC_D, HR, FIN, SALES, PROC, MAINT, FOH, JOB, KPI = range(1, 11)

# --- Work-context modifiers (Section [5]) -----------------------------------
WORK_CONTEXT = {
    ELECN: "solo or small team; on-site + on-the-road (van)",
    PLUMB: "solo or small team; on-site + on-the-road (van)",
    CARP: "solo or team; workshop/off-site + on-site",
    PAINT: "solo or team; on-site + on-the-road (van)",
    TILE: "usually solo; on-site",
    LAND: "team; on-site + yard/off-site + on-the-road",
}

# --- Evidence URLs (verified LIVE in Phase 4) -------------------------------
SAFE_ELEC = "https://safeelectric.ie/contractors/wp-content/uploads/sites/2/2017/03/Rules-of-Registration.pdf"
RGI = "https://rgi.ie/installers/about-us/certificates"
CIRI = "https://cif.ie/ciri"
CIRI_MAND = "https://dwfgroup.com/en/news-and-insights/insights/2026/3/ciri-goes-mandatory"
BCAR = "https://scsi.ie/wp-content/uploads/2020/08/BCAR-for-Project-Management-IP-.pdf"
SAFEPASS = "https://smartmovesafety.ie/what-safety-certificates-do-you-need-to-work-on-a-construction-site-in-ireland"
RCT_REV = "https://www.revenue.ie/en/tax-professionals/tdm/value-added-tax/part11-immovable-goods/construction-services/construction-servcies.pdf"
RCT_GT = "https://www.grantthornton.ie/globalassets/1.-member-firms/ireland/insights/publications/grant-thornton--relevant-contract-tax.pdf"
HSA_GENAPP = "https://www.hsa.ie/eng/legislation/regulations_and_orders/general_application_regulations_2007/"
HSA_SS = "https://www.hsa.ie/eng/topics/managing_health_and_safety/safety_statement_and_risk_assessment/"
TRADIFY = "https://www.tradifyhq.com/tradify-vs-servicem8-alternative"
SERVICEM8 = "https://www.servicem8.com/ai-job-management-software-for-trade-contractors"
VIOTRADE = "https://www.viotrade.co.uk/blog/best-tools-for-managing-trade-jobs"
LINKTLY = "https://www.linktly.com/guides/tradify-vs-servicem8"

# --- NEW trades assets (deduped by FUNCTION) --------------------------------
ASSETS = {
    "Trade Completion & Compliance Certificate Register": ("Log book", "Issues and logs statutory completion / compliance certificates per job — Safe Electric (electrical), RGI Declaration of Conformance (gas), Certs of Compliance and BCAR ancillary certs — with job, date and registration number."),
    "Job Schedule, Dispatch & Site Diary": ("Roster/scheduler", "Day/week diary scheduling multiple jobs and call-outs across sites, dispatching solo/team to addresses and tracking job status (enquiry→quoted→scheduled→in-progress→done)."),
    "Materials Take-off & Quantity Calculator": ("Calculator", "Estimates material quantities and cost per job — m² of tile/area, litres/coats of paint, cutting lists, plants/aggregate — feeding the quote and the order."),
    "RCT & Subcontractor Payment Tracker": ("Spreadsheet tracker", "Tracks Relevant Contracts Tax (RCT) on construction work: contract/site IDs, subcontractor payments, deduction rates and VAT reverse-charge narrative for Revenue."),
    "Method Statement & Risk Assessment (RAMS) Builder": ("Form/checklist", "Builds per-task/per-site method statements and risk assessments (RAMS) required on construction sites under the Construction Regs 2013."),
    "Cert, Card & Insurance Expiry Tracker": ("Spreadsheet tracker", "Tracks renewal dates for Safe Pass (4-yr), CSCS cards, Safe Electric/RGI registration, public-liability/PI insurance and other certifications so nothing lapses."),
    "Snag List & Job Sign-off / Handover Sheet": ("Form/checklist", "Records snagging items, photos, customer sign-off and handover at job completion — the evidence that releases final payment and closes disputes."),
    "Customer Enquiry & Job Pipeline CRM": ("Database", "Captures enquiries/leads and moves them through quote → job → invoice; stores customer history, addresses and follow-ups for a small trade business."),
}

# --- New asset short-keys ---------------------------------------------------
CERT = "Trade Completion & Compliance Certificate Register"
SCHED = "Job Schedule, Dispatch & Site Diary"
TAKEOFF = "Materials Take-off & Quantity Calculator"
RCT = "RCT & Subcontractor Payment Tracker"
RAMS = "Method Statement & Risk Assessment (RAMS) Builder"
CERTEXP = "Cert, Card & Insurance Expiry Tracker"
SNAG = "Snag List & Job Sign-off / Handover Sheet"
CRM = "Customer Enquiry & Job Pipeline CRM"

# --- Reused existing assets (by name) ---------------------------------------
QUOTE = "Job Quotation & Estimating Tool"               # id 39
WIP = "Production Job Card & WIP Tracker"               # id 43
CF = "Cashflow & P&L Tracker"                           # id 8
B2B = "Wholesale Order & B2B Invoice Tool"              # id 33 (reused as invoice/AR)
HS = "H&S Risk Assessment & Safety Statement"          # id 16
FIRE = "Fire Safety Register & Checks Log"             # id 17
TRN = "Staff Training & Induction Matrix"              # id 10
CAL = "Calibration Log (Scales, Thermometers, Probes)" # id 30 (test-instrument cal)
SDS = "Chemical Agents (SDS) Register & Risk Assessment"  # id 41
PPM = "Maintenance & PPM Asset Register"               # id 15 (van/tools/plant)
EQUIP = "Work Equipment & Machinery Safety/Guarding Inspection Register"  # id 40

REUSED = (QUOTE, WIP, CF, B2B, HS, FIRE, TRN, CAL, SDS, PPM, EQUIP)

OP, AUD, CON = "operator", "auditor", "consultant"

# --- asset_map rows ---------------------------------------------------------
# (business_type, asset_name, department, buyer, legal, revenue, pain, frequency, evidence_url, notes)
ROWS = [
    # ===== Statutory completion / compliance certificate (Legal=3 elec+gas) =
    (ELECN, CERT, QC_D, OP, 3, 2, 3, 3, SAFE_ELEC, "Safe Electric completion cert mandatory per job; on-site."),
    (ELECN, CERT, QC_D, AUD, 3, 1, 2, 1, SAFE_ELEC, "Safe Electric inspector audits issued certs."),
    (PLUMB, CERT, QC_D, OP, 3, 2, 3, 3, RGI, "RGI gas Declaration of Conformance mandatory for gas work."),
    (PLUMB, CERT, QC_D, AUD, 3, 1, 2, 1, RGI, "RGI inspector audits gas certs."),
    (CARP, CERT, QC_D, OP, 2, 1, 2, 1, BCAR, "BCAR ancillary completion cert on notifiable works."),
    (LAND, CERT, QC_D, OP, 1, 1, 1, 1, CIRI, "CIRI competence/records as register goes statutory."),

    # ===== Safety Statement (Legal=3, all trades — employer/self-employed) ==
    (ELECN, HS, QC_D, OP, 3, 1, 2, 1, HSA_SS, "Safety Statement (SHWW Act 2005); on-site + van."),
    (PLUMB, HS, QC_D, OP, 3, 1, 2, 1, HSA_SS, "on-site + van."),
    (CARP, HS, QC_D, OP, 3, 1, 2, 1, HSA_SS, "workshop + on-site."),
    (PAINT, HS, QC_D, OP, 3, 1, 2, 1, HSA_SS, "on-site + van."),
    (TILE, HS, QC_D, OP, 3, 1, 2, 1, HSA_SS, "solo; on-site."),
    (LAND, HS, QC_D, OP, 3, 1, 3, 1, HSA_SS, "team groundworks; higher risk profile."),
    (LAND, HS, QC_D, CON, 3, 1, 1, 1, HSA_SS, "H&S consultant prepares safety statement."),

    # ===== Chemical agents / SDS (Legal=3 painter VOC + landscaper pesticide)
    (PAINT, SDS, QC_D, OP, 3, 1, 3, 2, HSA_GENAPP, "Solvents/VOC/isocyanates — Chemical Agents Regs 2001."),
    (LAND, SDS, QC_D, OP, 3, 1, 2, 2, HSA_GENAPP, "Pesticide/plant-protection professional-user records (S.I. 155/2012)."),
    (CARP, SDS, QC_D, OP, 2, 1, 3, 2, HSA_GENAPP, "Hardwood dust (carcinogen) + lacquers/adhesives; workshop."),
    (TILE, SDS, QC_D, OP, 2, 0, 2, 2, HSA_GENAPP, "Adhesives/grouts/sealants; on-site."),
    (ELECN, SDS, QC_D, OP, 1, 0, 1, 1, HSA_GENAPP, "Minor — cleaning agents/resins."),

    # ===== Workshop fire (Legal=3 carpenter workshop; landscaper yard) ======
    (CARP, FIRE, QC_D, OP, 3, 0, 3, 2, HSA_SS, "Wood dust + finishes = high fire/explosion load; workshop premises."),
    (LAND, FIRE, QC_D, OP, 3, 0, 1, 1, HSA_SS, "Yard/fuel/store fire register."),

    # ===== Machine/equipment guarding (reuse — carpenter shop, landscaper plant)
    (CARP, EQUIP, QC_D, OP, 3, 1, 3, 2, HSA_GENAPP, "Saws/spindle moulder — high amputation risk; workshop."),
    (LAND, EQUIP, QC_D, OP, 3, 1, 2, 2, HSA_GENAPP, "Mowers/diggers/chippers guarding; on-site + yard."),

    # ===== Quote / estimating (SHOULD anchor — all six) =====================
    (ELECN, QUOTE, SALES, OP, 0, 3, 3, 2, TRADIFY, "Quoting accuracy → won/lost margin; van/office."),
    (PLUMB, QUOTE, SALES, OP, 0, 3, 3, 2, TRADIFY, "Quote call-outs/installs."),
    (CARP, QUOTE, SALES, OP, 0, 3, 3, 2, VIOTRADE, "Bespoke joinery estimating under-prices labour."),
    (PAINT, QUOTE, SALES, OP, 0, 3, 3, 2, VIOTRADE, "Coverage/coats estimating."),
    (TILE, QUOTE, SALES, OP, 0, 3, 3, 2, VIOTRADE, "m²/wastage quoting; solo."),
    (LAND, QUOTE, SALES, OP, 0, 3, 2, 2, TRADIFY, "Landscaping/groundworks estimating."),

    # ===== Job card / WIP (reuse) ==========================================
    (ELECN, WIP, JOB, OP, 0, 2, 2, 3, SERVICEM8, "Job card per call; on-site."),
    (PLUMB, WIP, JOB, OP, 0, 2, 2, 3, SERVICEM8, "Service/job card."),
    (CARP, WIP, JOB, OP, 0, 2, 2, 3, SERVICEM8, "Job through bench→install."),
    (PAINT, WIP, JOB, OP, 0, 2, 2, 2, SERVICEM8, "Per room/site."),
    (TILE, WIP, JOB, OP, 0, 1, 2, 2, SERVICEM8, "Per job; solo."),
    (LAND, WIP, JOB, OP, 0, 2, 2, 3, SERVICEM8, "Per site/phase; team."),

    # ===== Job schedule, dispatch & diary (new — daily scheduling) =========
    (ELECN, SCHED, JOB, OP, 0, 2, 3, 3, TRADIFY, "Many small jobs/day; dispatch van."),
    (PLUMB, SCHED, JOB, OP, 0, 2, 3, 3, TRADIFY, "Emergency vs planned call scheduling."),
    (LAND, SCHED, JOB, OP, 0, 2, 3, 3, TRADIFY, "Weather-driven rescheduling; team dispatch."),
    (CARP, SCHED, JOB, OP, 0, 2, 2, 2, TRADIFY, "Workshop + install scheduling."),
    (PAINT, SCHED, JOB, OP, 0, 2, 2, 2, TRADIFY, "Multiple domestic jobs."),
    (TILE, SCHED, JOB, OP, 0, 1, 2, 2, TRADIFY, "Job sequencing; solo."),

    # ===== Invoice & payment chasing (reuse B2B as invoice/AR) =============
    (ELECN, B2B, SALES, OP, 0, 3, 3, 3, LINKTLY, "Invoice on completion + chase payment; cashflow critical."),
    (PLUMB, B2B, SALES, OP, 0, 3, 3, 3, LINKTLY, "Getting paid on small jobs."),
    (CARP, B2B, SALES, OP, 0, 3, 3, 2, LINKTLY, "Stage/retention invoicing."),
    (PAINT, B2B, SALES, OP, 0, 3, 3, 2, LINKTLY, "Deposit + balance invoicing."),
    (TILE, B2B, SALES, OP, 0, 3, 3, 2, LINKTLY, "Deposit then balance; chasing."),
    (LAND, B2B, SALES, OP, 0, 3, 2, 2, LINKTLY, "Stage invoicing on contracts."),

    # ===== Cashflow / P&L (reuse) ==========================================
    (ELECN, CF, FIN, OP, 0, 3, 3, 2, LINKTLY, "Cashflow gaps from slow payers."),
    (PLUMB, CF, FIN, OP, 0, 3, 3, 2, LINKTLY, ""),
    (CARP, CF, FIN, OP, 0, 3, 3, 2, LINKTLY, "Material outlay vs staged income."),
    (PAINT, CF, FIN, OP, 0, 3, 2, 2, LINKTLY, ""),
    (TILE, CF, FIN, OP, 0, 3, 2, 2, LINKTLY, ""),
    (LAND, CF, FIN, OP, 0, 3, 3, 2, LINKTLY, "Plant finance + seasonal cashflow."),

    # ===== RCT & subcontractor tax (Legal=2 Revenue-mandated; construction) =
    (ELECN, RCT, FIN, OP, 2, 2, 2, 2, RCT_REV, "RCT + VAT reverse charge when sub/principal on construction."),
    (PLUMB, RCT, FIN, OP, 2, 2, 2, 2, RCT_REV, "Heating/construction RCT."),
    (CARP, RCT, FIN, OP, 2, 2, 2, 2, RCT_GT, "Construction RCT/reverse charge."),
    (LAND, RCT, FIN, OP, 2, 2, 2, 2, RCT_GT, "Groundworks RCT; principal deductions."),
    (PAINT, RCT, FIN, OP, 2, 1, 1, 1, RCT_REV, "RCT where sub-contracting on builds."),
    (ELECN, RCT, FIN, CON, 2, 1, 1, 1, RCT_GT, "Accountant operates RCT for the trade."),

    # ===== RAMS — method statement / risk assessment (Legal=2 site) ========
    (LAND, RAMS, QC_D, OP, 2, 1, 2, 2, SAFEPASS, "RAMS required on construction sites (Construction Regs 2013)."),
    (ELECN, RAMS, QC_D, OP, 2, 1, 2, 2, SAFEPASS, "Site RAMS for main-contractor work."),
    (PLUMB, RAMS, QC_D, OP, 2, 1, 2, 1, SAFEPASS, ""),
    (CARP, RAMS, QC_D, OP, 2, 1, 2, 1, SAFEPASS, ""),
    (PAINT, RAMS, QC_D, OP, 2, 0, 1, 1, SAFEPASS, ""),
    (LAND, RAMS, QC_D, CON, 2, 1, 1, 1, SAFEPASS, "H&S consultant authors RAMS."),

    # ===== Cert / card / insurance expiry tracker (new — SHOULD) ===========
    (ELECN, CERTEXP, HR, OP, 1, 1, 2, 1, SAFEPASS, "Safe Pass (4-yr)/CSCS/registration/insurance renewals."),
    (PLUMB, CERTEXP, HR, OP, 1, 1, 2, 1, SAFEPASS, "RGI registration + cards + insurance."),
    (CARP, CERTEXP, HR, OP, 1, 1, 2, 1, SAFEPASS, ""),
    (LAND, CERTEXP, HR, OP, 1, 1, 2, 1, SAFEPASS, "Safe Pass/CSCS/pesticide PU + insurance."),
    (PAINT, CERTEXP, HR, OP, 1, 0, 1, 1, SAFEPASS, ""),
    (TILE, CERTEXP, HR, OP, 1, 0, 1, 1, SAFEPASS, ""),

    # ===== Materials take-off & quantity calculator (new — high WTP) =======
    (TILE, TAKEOFF, FIN, OP, 0, 3, 3, 3, VIOTRADE, "m²/wastage/adhesive take-off — flagship-grade for tilers."),
    (PAINT, TAKEOFF, FIN, OP, 0, 3, 3, 3, VIOTRADE, "Area→litres/coats coverage calculator."),
    (CARP, TAKEOFF, FIN, OP, 0, 3, 2, 2, VIOTRADE, "Cutting list / material take-off."),
    (LAND, TAKEOFF, FIN, OP, 0, 2, 2, 2, VIOTRADE, "Plants/aggregate/materials take-off."),
    (ELECN, TAKEOFF, FIN, OP, 0, 2, 1, 2, VIOTRADE, "Cable/accessory take-off from quote."),
    (PLUMB, TAKEOFF, FIN, OP, 0, 2, 1, 2, VIOTRADE, "Pipe/fittings take-off."),

    # ===== Snag list & sign-off / handover (new — releases payment) ========
    (CARP, SNAG, OPS, OP, 0, 2, 2, 2, VIOTRADE, "Snagging/sign-off on installs releases final payment."),
    (PAINT, SNAG, OPS, OP, 0, 2, 2, 2, VIOTRADE, "Snag + dilapidation photos."),
    (TILE, SNAG, OPS, OP, 0, 2, 2, 2, VIOTRADE, "Sign-off after balance."),
    (LAND, SNAG, OPS, OP, 0, 2, 2, 2, VIOTRADE, "Handover/sign-off on completion."),
    (ELECN, SNAG, OPS, OP, 0, 1, 1, 2, VIOTRADE, "Job sign-off."),
    (PLUMB, SNAG, OPS, OP, 0, 1, 1, 2, VIOTRADE, "Job sign-off."),

    # ===== Customer enquiry & job pipeline CRM (new) =======================
    (ELECN, CRM, SALES, OP, 0, 2, 2, 3, SERVICEM8, "Enquiry→quote→job pipeline; repeat customers."),
    (PLUMB, CRM, SALES, OP, 0, 2, 2, 3, SERVICEM8, ""),
    (PAINT, CRM, SALES, OP, 0, 2, 2, 2, SERVICEM8, ""),
    (CARP, CRM, SALES, OP, 0, 2, 2, 2, SERVICEM8, ""),
    (LAND, CRM, SALES, OP, 0, 2, 2, 2, SERVICEM8, ""),
    (TILE, CRM, SALES, OP, 0, 1, 1, 2, SERVICEM8, "Lead/job pipeline; solo."),

    # ===== Test-instrument calibration (reuse — electrician cert validity) ==
    (ELECN, CAL, QC_D, OP, 2, 1, 2, 2, SAFE_ELEC, "Insulation/loop/PAT tester calibration underpins valid certs."),
    (PLUMB, CAL, QC_D, OP, 1, 0, 1, 2, RGI, "Gas analyser/manometer calibration."),

    # ===== Plant / vehicle / tool maintenance register (reuse PPM) =========
    (LAND, PPM, MAINT, OP, 1, 2, 3, 2, HSA_GENAPP, "Plant/machinery downtime critical; servicing log."),
    (ELECN, PPM, MAINT, OP, 1, 1, 2, 2, HSA_GENAPP, "Van + tool register/maintenance."),
    (PLUMB, PPM, MAINT, OP, 1, 1, 2, 2, HSA_GENAPP, "Van + tool register."),
    (CARP, PPM, MAINT, OP, 1, 1, 2, 2, HSA_GENAPP, "Machine + van maintenance."),
    (PAINT, PPM, MAINT, OP, 1, 0, 1, 1, HSA_GENAPP, "Sprayers/van."),
    (TILE, PPM, MAINT, OP, 1, 0, 1, 1, HSA_GENAPP, "Tools/van."),

    # ===== Training matrix (reuse — team trades, card competence) ==========
    (LAND, TRN, HR, OP, 2, 1, 2, 1, SAFEPASS, "Safe Pass/CSCS/pesticide competence records; team."),
    (ELECN, TRN, HR, OP, 1, 1, 1, 1, SAFEPASS, "Apprentice/team competence."),
    (CARP, TRN, HR, OP, 1, 1, 1, 1, SAFEPASS, "Machine competence; team."),
    (PLUMB, TRN, HR, OP, 1, 1, 1, 1, SAFEPASS, "Team competence."),
]

# --- pain points ------------------------------------------------------------
# (business_type, description, severity, source_url)
PAINS = [
    (ELECN, "Chasing payments / cashflow gaps on many small jobs.", "severe", LINKTLY),
    (ELECN, "Quoting accuracy vs won/lost margin.", "real", TRADIFY),
    (ELECN, "Safe Electric completion-cert admin and keeping registration valid.", "real", SAFE_ELEC),
    (PLUMB, "Emergency-vs-planned call scheduling chaos.", "severe", TRADIFY),
    (PLUMB, "RGI gas-cert / Declaration of Conformance compliance per job.", "severe", RGI),
    (PLUMB, "Getting paid promptly on small jobs.", "real", LINKTLY),
    (CARP, "Bespoke estimating under-prices labour; timber wastage.", "severe", VIOTRADE),
    (CARP, "Hardwood-dust (carcinogen) exposure / LEV compliance in the workshop.", "severe", HSA_GENAPP),
    (CARP, "Snagging disputes delay final payment.", "real", VIOTRADE),
    (PAINT, "Under-estimating coverage/coats erodes margin.", "severe", VIOTRADE),
    (PAINT, "Deposits and getting paid the balance.", "real", LINKTLY),
    (PAINT, "Solvent/VOC chemical-agent H&S compliance.", "real", HSA_GENAPP),
    (TILE, "Quoting m²/wastage and adhesive quantities accurately.", "severe", VIOTRADE),
    (TILE, "Chasing the balance after a materials deposit.", "real", LINKTLY),
    (LAND, "Weather-driven rescheduling and plant downtime.", "severe", TRADIFY),
    (LAND, "Pesticide professional-user records (DAFM) compliance.", "real", HSA_GENAPP),
    (LAND, "RCT / subcontractor admin on larger groundworks contracts.", "real", RCT_GT),
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
    ap = argparse.ArgumentParser(description="Seed trades (Phase 4) rows.")
    ap.add_argument("--db", default=DEFAULT_DB)
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        # Set work-context per trades business type.
        for bt, wc in WORK_CONTEXT.items():
            conn.execute("UPDATE business_types SET work_context=? WHERE id=?;", (wc, bt))

        # Upsert NEW digital assets (unique by name). Reused assets untouched.
        for name, (atype, desc) in ASSETS.items():
            conn.execute(
                "INSERT INTO digital_assets (name, asset_type, description) VALUES (?,?,?) "
                "ON CONFLICT(name) DO UPDATE SET asset_type=excluded.asset_type, description=excluded.description;",
                (name, atype, desc),
            )
        conn.commit()

        name_to_id = {n: i for i, n in conn.execute("SELECT id, name FROM digital_assets")}
        for n in REUSED:
            if n not in name_to_id:
                raise RuntimeError(f"Reused asset missing from DB (run Phases 1-3 first): {n}")

        # Idempotency: clear this phase's rows (business types 16-21).
        conn.execute(
            "DELETE FROM asset_map WHERE business_type_id IN (16,17,18,19,20,21);")
        conn.execute(
            "DELETE FROM pain_points WHERE business_type_id IN (16,17,18,19,20,21);")

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
        n_phase = conn.execute(
            "SELECT COUNT(*) FROM asset_map WHERE business_type_id IN (16,17,18,19,20,21)").fetchone()[0]
        n_pain = conn.execute("SELECT COUNT(*) FROM pain_points").fetchone()[0]
        by_tier = dict(conn.execute(
            "SELECT tier, COUNT(*) FROM asset_map WHERE business_type_id IN (16,17,18,19,20,21) GROUP BY tier"))
        by_buyer = dict(conn.execute(
            "SELECT buyer, COUNT(*) FROM asset_map WHERE business_type_id IN (16,17,18,19,20,21) GROUP BY buyer"))
        print(f"Seeded trades: {inserted} asset_map rows (bt 16-21), {len(ASSETS)} new assets, {len(PAINS)} pain points.")
        print(f"  digital_assets total    : {n_assets}")
        print(f"  asset_map total         : {n_map}")
        print(f"  asset_map phase-4 rows  : {n_phase}")
        print(f"  pain_points total       : {n_pain}")
        print(f"  phase-4 by tier         : {by_tier}")
        print(f"  phase-4 by buyer        : {by_buyer}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
