#!/usr/bin/env python3
"""
ASSET-FORGE — Phase 1 seed: HOSPITALITY research rows.

Inserts the hospitality digital assets, the scored asset_map rows (raw 0-3 axis
scores per rubric [6] + buyer tag + evidence_url) and pain points for the five
hospitality business types (Bar/pub, Café, Restaurant, B&B/guesthouse, Hotel).

Score = (legal*3) + (revenue*2) + (pain*2) + (frequency*1), max 24.
Tier:  MUST  if score >= 16 OR legal == 3 (legal-mandatory auto-promotes)
       SHOULD 10-15 · COULD 5-9 · WON'T < 5.

Idempotent: deletes this phase's hospitality asset_map + pain_point rows first
(business types 1-5), then re-inserts. digital_assets are upserted by unique name.

Usage:
    python3 scripts/seed_hospitality.py [--db PATH]
"""

import argparse
import os
import sqlite3
import sys

DEFAULT_DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "intelligence.db")

# Hospitality business_type ids (seeded in Phase 0): see SELECT below for the map.
BAR, CAFE, REST, BNB, HOTEL = 1, 2, 3, 4, 5

# Department ids (Phase 0 seed).
OPS, QC, HR, FIN, SALES, PROC, MAINT, FOH, JOB, KPI = range(1, 11)

# --- Evidence URLs (verified live in Phase 1) -------------------------------
FSAI_HACCP = "https://www.fsai.ie/business-advice/starting-a-food-business/business-start-up-information-factsheet"
FSAI_ALLERGEN = "https://www.fsai.ie/business-advice/running-a-food-business/allergens"
HSA_SS = "https://www.hsa.ie/eng/topics/managing_health_and_safety/safety_statement_and_risk_assessment/"
HSA_HOSP = "https://www.hsa.ie/eng/your_industry/catering_and_hospitality/the_law/"
FAILTE_GH = "https://www.failteireland.ie/Supports/registration-and-grading/national-quality-assurance-framework/Guest-Houses.aspx"
FAILTE_WS = "https://www.failteireland.ie/welcomestandard.aspx"
EPOS_REV = "https://www.capterra.com/p/152638/Epos-Now/reviews/"
POS_BAR = "https://startups.co.uk/payment-processing/best-pos-systems-bars-and-pubs/"
TPL_7SHIFTS = "https://www.7shifts.com/resources/templates/"
ETSY_ROTA = "https://www.etsy.com/market/staff_rota_template"
ETSY_SHEET = "https://www.etsy.com/market/restaurant_spreadsheet_template"

# --- Digital assets (deduped by FUNCTION, not label) ------------------------
# name -> (asset_type, description). Inserted with INSERT OR IGNORE (name unique).
ASSETS = {
    "HACCP Food Safety Management System": ("Log book", "HACCP plan + CCP monitoring logs and prerequisite programmes — the documented food safety system every food business must keep (Reg 852/2004)."),
    "Allergen Matrix & Menu Declaration Tool": ("Form/checklist", "Maps the 14 EU allergens (Reg 1169/2011) to every menu item and generates customer-facing allergen declarations."),
    "Temperature Monitoring Log": ("Log book", "Daily fridge/freezer/hot-hold/cook/delivery temperature records — core HACCP CCP evidence."),
    "Cleaning & Sanitation Schedule": ("Form/checklist", "Daily/weekly/periodic cleaning rota with sign-off — required good-hygiene-practice evidence."),
    "Supplier & Delivery Traceability Log": ("Log book", "Incoming-goods checks plus batch/lot traceability ('one step back') for recall readiness."),
    "Stock & Wastage Tracker": ("Spreadsheet tracker", "Opening/closing stock counts, usage, wastage and variance vs theoretical — bar and kitchen."),
    "Recipe & Menu GP Costing Calculator": ("Calculator", "Dish/drink ingredient costing, gross-profit % and price-point modelling for menu engineering."),
    "Cashflow & P&L Tracker": ("Spreadsheet tracker", "Daily takings, running cashflow forecast and monthly P&L for an owner-run venue."),
    "Staff Rota & Labour-Cost Scheduler": ("Roster/scheduler", "Shift planning with live labour-cost-% against forecast sales."),
    "Staff Training & Induction Matrix": ("Spreadsheet tracker", "Records induction, food-safety and manual-handling training per employee with refresh dates."),
    "Daily Takings & Till Reconciliation Sheet": ("Spreadsheet tracker", "Z-read vs cash/card banking reconciliation; flags till variances."),
    "Table Booking & Covers Diary": ("Diary/planner", "Reservation diary with covers forecasting and no-show tracking."),
    "Room Bookings & Occupancy Dashboard": ("Dashboard", "Room availability, occupancy %, ADR and RevPAR for accommodation."),
    "Guest Register & Check-in Log": ("Log book", "Register of guests and check-in record for a registered accommodation premises."),
    "Maintenance & PPM Asset Register": ("Log book", "Planned preventive-maintenance schedule and equipment service history."),
    "H&S Risk Assessment & Safety Statement": ("Form/checklist", "Workplace risk assessments, safety statement and accident/incident log (S.19 Act 2005)."),
    "Fire Safety Register & Checks Log": ("Log book", "Fire-equipment checks, drills and emergency-lighting records (fire safety statutory duty)."),
    "Customer Feedback & Review Tracker": ("Spreadsheet tracker", "Logs reviews/complaints by theme to drive service recovery."),
    "Function & Event Quote Generator": ("Quote generator", "Builds priced quotes for functions, parties and group bookings."),
    "Cellar & Beer-Line Cleaning Log": ("Log book", "Beer-line and cellar cleaning records — product quality plus hygiene."),
}

# --- asset_map rows ---------------------------------------------------------
# (business_type, asset_name, department, buyer, legal, revenue, pain, frequency, evidence_url, notes)
A = "HACCP Food Safety Management System"
AL = "Allergen Matrix & Menu Declaration Tool"
TMP = "Temperature Monitoring Log"
CLN = "Cleaning & Sanitation Schedule"
TRC = "Supplier & Delivery Traceability Log"
STK = "Stock & Wastage Tracker"
GP = "Recipe & Menu GP Costing Calculator"
CF = "Cashflow & P&L Tracker"
ROTA = "Staff Rota & Labour-Cost Scheduler"
TRN = "Staff Training & Induction Matrix"
TILL = "Daily Takings & Till Reconciliation Sheet"
BOOK = "Table Booking & Covers Diary"
ROOM = "Room Bookings & Occupancy Dashboard"
GUEST = "Guest Register & Check-in Log"
PPM = "Maintenance & PPM Asset Register"
HS = "H&S Risk Assessment & Safety Statement"
FIRE = "Fire Safety Register & Checks Log"
FB = "Customer Feedback & Review Tracker"
EVT = "Function & Event Quote Generator"
LINE = "Cellar & Beer-Line Cleaning Log"

OP, AUD, CON = "operator", "auditor", "consultant"

ROWS = [
    # --- Food-safety MUST floor (Legal=3) across all five -------------------
    (BAR, A, QC, OP, 3, 1, 2, 3, FSAI_HACCP, "Bar serving food is a food business."),
    (CAFE, A, QC, OP, 3, 1, 3, 3, FSAI_HACCP, "High-allergen bakery/deli handling."),
    (REST, A, QC, OP, 3, 2, 3, 3, FSAI_HACCP, "Highest-stakes food operation."),
    (BNB, A, QC, OP, 3, 1, 2, 3, FSAI_HACCP, "HACCP-lite scaled to breakfast service."),
    (HOTEL, A, QC, OP, 3, 2, 3, 3, FSAI_HACCP, "Full kitchen + multiple outlets."),
    (REST, A, QC, CON, 3, 2, 2, 2, FSAI_HACCP, "Food-safety consultant builds HACCP for clients."),

    (BAR, AL, QC, OP, 3, 1, 2, 2, FSAI_ALLERGEN, ""),
    (CAFE, AL, QC, OP, 3, 2, 3, 3, FSAI_ALLERGEN, "Changing daily-specials menu raises allergen pain."),
    (REST, AL, QC, OP, 3, 2, 3, 3, FSAI_ALLERGEN, ""),
    (BNB, AL, QC, OP, 3, 1, 2, 2, FSAI_ALLERGEN, ""),
    (HOTEL, AL, QC, OP, 3, 2, 3, 3, FSAI_ALLERGEN, ""),
    (REST, AL, QC, AUD, 3, 1, 2, 2, FSAI_ALLERGEN, "EHO/auditor inspects allergen declarations."),

    (BAR, TMP, QC, OP, 3, 1, 2, 3, FSAI_HACCP, ""),
    (CAFE, TMP, QC, OP, 3, 1, 2, 3, FSAI_HACCP, ""),
    (REST, TMP, QC, OP, 3, 2, 3, 3, FSAI_HACCP, ""),
    (BNB, TMP, QC, OP, 3, 1, 2, 3, FSAI_HACCP, ""),
    (HOTEL, TMP, QC, OP, 3, 2, 3, 3, FSAI_HACCP, ""),

    (BAR, CLN, QC, OP, 3, 1, 2, 3, FSAI_HACCP, ""),
    (CAFE, CLN, QC, OP, 3, 1, 2, 3, FSAI_HACCP, ""),
    (REST, CLN, QC, OP, 3, 1, 2, 3, FSAI_HACCP, ""),
    (BNB, CLN, QC, OP, 3, 1, 2, 3, FSAI_HACCP, ""),
    (HOTEL, CLN, QC, OP, 3, 2, 3, 3, FSAI_HACCP, ""),

    (BAR, TRC, QC, OP, 3, 1, 1, 2, FSAI_HACCP, "Traceability one-step-back (Reg 178/2002)."),
    (CAFE, TRC, QC, OP, 3, 1, 1, 2, FSAI_HACCP, ""),
    (REST, TRC, QC, OP, 3, 1, 2, 3, FSAI_HACCP, ""),
    (BNB, TRC, QC, OP, 3, 1, 1, 2, FSAI_HACCP, ""),
    (HOTEL, TRC, QC, OP, 3, 2, 2, 3, FSAI_HACCP, ""),

    # --- H&S + fire MUST floor (Legal=3) ------------------------------------
    (BAR, HS, QC, OP, 3, 1, 2, 1, HSA_SS, ""),
    (CAFE, HS, QC, OP, 3, 1, 2, 1, HSA_SS, ""),
    (REST, HS, QC, OP, 3, 1, 2, 1, HSA_SS, ""),
    (BNB, HS, QC, OP, 3, 0, 1, 1, HSA_SS, "Small/solo but still an employer duty."),
    (HOTEL, HS, QC, OP, 3, 1, 2, 1, HSA_SS, ""),

    (BAR, FIRE, QC, OP, 3, 0, 2, 2, HSA_HOSP, ""),
    (CAFE, FIRE, QC, OP, 3, 0, 2, 2, HSA_HOSP, ""),
    (REST, FIRE, QC, OP, 3, 0, 2, 2, HSA_HOSP, ""),
    (BNB, FIRE, QC, OP, 3, 0, 2, 2, HSA_HOSP, "Overnight occupancy raises fire stakes."),
    (HOTEL, FIRE, QC, OP, 3, 1, 3, 2, HSA_HOSP, "Highest fire pain — guest volume/overnight."),

    # --- "Wanted, sells well" SHOULD/COULD zone -----------------------------
    (BAR, STK, PROC, OP, 0, 3, 3, 3, POS_BAR, "Shrinkage/over-pour is the classic profit leak."),
    (CAFE, STK, PROC, OP, 0, 2, 2, 3, EPOS_REV, "Perishable wastage."),
    (REST, STK, PROC, OP, 0, 3, 3, 3, EPOS_REV, ""),
    (HOTEL, STK, PROC, OP, 0, 3, 2, 2, EPOS_REV, ""),
    (BNB, STK, PROC, OP, 0, 1, 1, 1, EPOS_REV, "Small breakfast stock only."),

    (REST, GP, FIN, OP, 0, 3, 3, 2, EPOS_REV, "Menu engineering is the main margin lever."),
    (CAFE, GP, FIN, OP, 0, 3, 2, 2, EPOS_REV, ""),
    (BAR, GP, FIN, OP, 0, 2, 2, 1, POS_BAR, ""),
    (HOTEL, GP, FIN, OP, 0, 2, 2, 1, EPOS_REV, ""),
    (BNB, GP, FIN, OP, 0, 1, 1, 1, EPOS_REV, ""),

    (BAR, CF, FIN, OP, 0, 3, 3, 3, TPL_7SHIFTS, ""),
    (CAFE, CF, FIN, OP, 0, 3, 3, 3, TPL_7SHIFTS, ""),
    (REST, CF, FIN, OP, 0, 3, 3, 3, TPL_7SHIFTS, ""),
    (BNB, CF, FIN, OP, 0, 3, 2, 2, TPL_7SHIFTS, "Seasonality/occupancy cashflow."),
    (HOTEL, CF, FIN, OP, 0, 3, 2, 2, TPL_7SHIFTS, ""),

    (REST, ROTA, HR, OP, 0, 3, 3, 3, ETSY_ROTA, "Labour-cost % vs covers."),
    (BAR, ROTA, HR, OP, 0, 2, 3, 3, ETSY_ROTA, ""),
    (CAFE, ROTA, HR, OP, 0, 2, 2, 3, ETSY_ROTA, ""),
    (HOTEL, ROTA, HR, OP, 0, 3, 3, 3, ETSY_ROTA, "Multi-department rota."),
    (BNB, ROTA, HR, OP, 0, 1, 1, 2, ETSY_ROTA, ""),

    (REST, TRN, HR, OP, 2, 1, 2, 1, FSAI_HACCP, "Food-safety training records expected."),
    (CAFE, TRN, HR, OP, 2, 1, 2, 1, FSAI_HACCP, ""),
    (BAR, TRN, HR, OP, 2, 1, 1, 1, FSAI_HACCP, ""),
    (HOTEL, TRN, HR, OP, 2, 1, 2, 1, FSAI_HACCP, ""),
    (BNB, TRN, HR, OP, 1, 0, 1, 1, FSAI_HACCP, ""),

    (BAR, TILL, FIN, OP, 0, 2, 2, 3, EPOS_REV, ""),
    (CAFE, TILL, FIN, OP, 0, 2, 2, 3, EPOS_REV, ""),
    (REST, TILL, FIN, OP, 0, 2, 2, 3, EPOS_REV, ""),
    (HOTEL, TILL, FIN, OP, 0, 2, 1, 3, EPOS_REV, ""),
    (BNB, TILL, FIN, OP, 0, 1, 1, 2, EPOS_REV, ""),

    (REST, BOOK, FOH, OP, 0, 3, 3, 3, ETSY_SHEET, "No-shows are direct lost revenue."),
    (BAR, BOOK, FOH, OP, 0, 1, 1, 2, ETSY_SHEET, ""),
    (CAFE, BOOK, FOH, OP, 0, 1, 1, 2, ETSY_SHEET, ""),
    (HOTEL, BOOK, FOH, OP, 0, 2, 1, 3, ETSY_SHEET, "In-house restaurant covers."),

    (BNB, ROOM, FOH, OP, 0, 3, 3, 3, FAILTE_WS, "Direct-booking vs OTA is the core revenue workflow."),
    (HOTEL, ROOM, FOH, OP, 0, 3, 3, 3, FAILTE_WS, "RevPAR/ADR revenue management."),

    (BNB, GUEST, FOH, OP, 2, 1, 2, 3, FAILTE_GH, "Register of guests for a registered premises."),
    (HOTEL, GUEST, FOH, OP, 2, 1, 2, 3, FAILTE_GH, ""),

    (HOTEL, PPM, MAINT, OP, 1, 1, 2, 2, HSA_HOSP, "PPM across rooms + plant."),
    (REST, PPM, MAINT, OP, 1, 1, 2, 1, HSA_HOSP, ""),
    (BAR, PPM, MAINT, OP, 1, 1, 1, 1, HSA_HOSP, ""),
    (CAFE, PPM, MAINT, OP, 1, 1, 1, 1, HSA_HOSP, ""),
    (BNB, PPM, MAINT, OP, 1, 1, 1, 1, HSA_HOSP, ""),

    (HOTEL, EVT, SALES, OP, 0, 3, 2, 1, ETSY_SHEET, "Functions are high-margin revenue."),
    (REST, EVT, SALES, OP, 0, 2, 2, 1, ETSY_SHEET, ""),
    (BAR, EVT, SALES, OP, 0, 2, 1, 1, ETSY_SHEET, ""),

    (HOTEL, FB, SALES, OP, 0, 2, 1, 2, FAILTE_WS, ""),
    (BNB, FB, SALES, OP, 0, 2, 1, 2, FAILTE_WS, "Reviews drive direct bookings."),
    (REST, FB, SALES, OP, 0, 1, 1, 2, FAILTE_WS, ""),
    (CAFE, FB, SALES, OP, 0, 1, 1, 2, FAILTE_WS, ""),
    (BAR, FB, SALES, OP, 0, 1, 1, 1, FAILTE_WS, ""),

    (BAR, LINE, QC, OP, 1, 2, 2, 2, POS_BAR, "Beer-line cleaning ~weekly: quality + hygiene."),
    (HOTEL, LINE, QC, OP, 1, 1, 1, 2, POS_BAR, "Hotel bar."),
]

# --- pain points ------------------------------------------------------------
# (business_type, description, severity, source_url)
PAINS = [
    (BAR, "Stock shrinkage, over-pour and wastage quietly erode GP; hard to spot without nightly variance.", "severe", POS_BAR),
    (BAR, "Till Z-read vs cash/card banking variances; reconciliation is manual and error-prone.", "real", EPOS_REV),
    (BAR, "EPOS stock modules are complex and contract-locked; owners want a simple sheet they own.", "real", EPOS_REV),
    (CAFE, "Allergen accuracy on a changing daily-specials menu — high liability, easy to get wrong.", "severe", FSAI_ALLERGEN),
    (CAFE, "Thin margins on food + coffee; pricing is guesswork without recipe costing.", "real", EPOS_REV),
    (CAFE, "Fresh/perishable wastage on unsold stock.", "real", EPOS_REV),
    (REST, "Food-cost % / GP erosion; no live view of margin per dish.", "severe", EPOS_REV),
    (REST, "Labour-cost % runs away from covers without a rota tied to forecast sales.", "severe", ETSY_ROTA),
    (REST, "Reservation no-shows are direct lost revenue.", "real", ETSY_SHEET),
    (REST, "Allergen liability across a full menu; EHO inspection risk.", "severe", FSAI_ALLERGEN),
    (BNB, "OTA commission vs direct bookings squeezes margin.", "severe", FAILTE_WS),
    (BNB, "Occupancy/seasonality makes cashflow lumpy and hard to forecast.", "real", TPL_7SHIFTS),
    (BNB, "Double-bookings and manual availability tracking across channels.", "real", FAILTE_WS),
    (HOTEL, "Revenue management (RevPAR/ADR) across channels is opaque without a dashboard.", "severe", FAILTE_WS),
    (HOTEL, "Preventive maintenance across rooms and plant is reactive, not planned.", "real", HSA_HOSP),
    (HOTEL, "Coordinating multi-department rotas to a labour-cost target.", "real", ETSY_ROTA),
    (HOTEL, "Slow function/event quoting loses high-margin bookings.", "real", ETSY_SHEET),
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
    ap = argparse.ArgumentParser(description="Seed hospitality (Phase 1) rows.")
    ap.add_argument("--db", default=DEFAULT_DB)
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        # Upsert digital assets (unique by name).
        for name, (atype, desc) in ASSETS.items():
            conn.execute(
                "INSERT INTO digital_assets (name, asset_type, description) VALUES (?,?,?) "
                "ON CONFLICT(name) DO UPDATE SET asset_type=excluded.asset_type, description=excluded.description;",
                (name, atype, desc),
            )
        conn.commit()

        name_to_id = {n: i for i, n in conn.execute("SELECT id, name FROM digital_assets")}

        # Idempotency: clear this phase's hospitality rows (business types 1-5).
        conn.execute("DELETE FROM asset_map WHERE business_type_id IN (1,2,3,4,5);")
        conn.execute("DELETE FROM pain_points WHERE business_type_id IN (1,2,3,4,5);")

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
        n_pain = conn.execute("SELECT COUNT(*) FROM pain_points").fetchone()[0]
        by_tier = dict(conn.execute("SELECT tier, COUNT(*) FROM asset_map GROUP BY tier"))
        print(f"Seeded hospitality: {inserted} asset_map rows, {len(ASSETS)} assets, {len(PAINS)} pain points.")
        print(f"  digital_assets total : {n_assets}")
        print(f"  asset_map total      : {n_map}")
        print(f"  pain_points total    : {n_pain}")
        print(f"  by tier              : {by_tier}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
