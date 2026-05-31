#!/usr/bin/env python3
"""
ASSET-FORGE · Phase 13e — Industry Atlas + pack_queue (subagent dispatch board)
================================================================================
Adds a comprehensive industry classifier to intelligence.db so we can capture
"all industries and sub-businesses" and let subagents drain a ranked queue of
packs to build (Samuel, 31/05). Based on **NACE Rev.2** (EU official) with a
**plain trade name** on every row (the word the owner uses).

Creates (idempotent — only touches these objects, never the existing schema):
  · industries           — NACE sections (broad sectors) + plain names
  · business_types_atlas — specific sub-businesses (baker, Airbnb host, …)
  · pack_queue           — the dispatch board: one row per (business × language)
                           with status + scores + assignee + module_set
  · v_pack_candidates    — ranked view: what to build next (market×reuse×ease)

Run:  python3 scripts/seed_atlas.py
"""
from __future__ import annotations
import os, sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "intelligence.db"))

# NACE Rev.2 sections — broad sectors (code, official name, plain name)
SECTIONS = [
    ("A", "Agriculture, forestry and fishing", "Farming & growing"),
    ("C", "Manufacturing", "Making & production"),
    ("F", "Construction", "Building & trades"),
    ("G", "Wholesale and retail trade; repair of motor vehicles", "Retail & motor"),
    ("H", "Transportation and storage", "Transport & delivery"),
    ("I", "Accommodation and food service activities", "Hospitality & stays"),
    ("M", "Professional, scientific and technical activities", "Professional services"),
    ("N", "Administrative and support service activities", "Admin & support"),
    ("P", "Education", "Education & training"),
    ("Q", "Human health and social work activities", "Health & care"),
    ("R", "Arts, entertainment and recreation", "Arts, events & leisure"),
    ("S", "Other service activities", "Personal & other services"),
]

# Specific sellable sub-businesses: (plain name, NACE class, section, existing_vertical, module_set)
# module_set = which skeleton modules the pack would carry (default food/retail 6).
F6 = "LEDGER_12M,MARGIN,STOCK,LABOUR,TAKINGS,TRAINING"           # food/retail standard
SVC = "LEDGER_12M,MARGIN,LABOUR,TAKINGS,TRAINING"                # service (no stock)
JOB = "LEDGER_12M,MARGIN,LABOUR,TAKINGS,TRAINING"                # trades (quotes/jobs later)
ATLAS = [
    # Hospitality & stays (I)
    ("Café / coffee shop", "56.10", "I", "Hospitality", F6),
    ("Restaurant", "56.10", "I", "Hospitality", F6),
    ("Bar / pub", "56.30", "I", "Hospitality", F6),
    ("Takeaway / fast food", "56.10", "I", "Hospitality", F6),
    ("Caterer", "56.21", "I", "Hospitality", F6),
    ("Hotel", "55.10", "I", "Hospitality", F6),
    ("B&B / guesthouse", "55.20", "I", "Hospitality", F6),
    ("Airbnb / short-stay host", "55.20", "I", "Hospitality", F6),
    ("Campsite / glamping", "55.30", "I", "Hospitality", F6),
    # Retail & motor (G)
    ("Baker (shop)", "47.24", "G", "Food manufacturing", F6),
    ("Butcher", "47.22", "G", "Food manufacturing", F6),
    ("Greengrocer (fruit & veg)", "47.21", "G", None, F6),
    ("Convenience store", "47.11", "G", None, F6),
    ("Clothing boutique", "47.71", "G", None, F6),
    ("Florist", "47.76", "G", None, F6),
    ("Bookshop", "47.61", "G", None, F6),
    ("Pet shop", "47.76", "G", None, F6),
    ("Hardware / DIY store", "47.52", "G", None, F6),
    ("Wine shop / off-licence", "47.25", "G", None, F6),
    ("Online shop / e-commerce", "47.91", "G", None, F6),
    ("Car dealer", "45.11", "G", None, F6),
    ("Garage / car repair", "45.20", "G", None, JOB),
    # Making & production (C)
    ("Bakery (production)", "10.71", "C", "Food manufacturing", F6),
    ("Meat processing", "10.13", "C", "Food manufacturing", F6),
    ("Dairy / cheesemaker", "10.51", "C", "Food manufacturing", F6),
    ("Brewery / craft beer", "11.05", "C", "Food manufacturing", F6),
    ("Patisserie / confectioner", "10.72", "C", "Food manufacturing", F6),
    ("Joinery / furniture maker", "31.00", "C", "Non-food manufacturing", JOB),
    ("Metal fabrication", "25.00", "C", "Non-food manufacturing", JOB),
    ("Print shop", "18.12", "C", "Non-food manufacturing", JOB),
    # Building & trades (F)
    ("Electrician", "43.21", "F", "Trades", JOB),
    ("Plumber / heating", "43.22", "F", "Trades", JOB),
    ("Carpenter / joiner", "43.32", "F", "Trades", JOB),
    ("Painter / decorator", "43.34", "F", "Trades", JOB),
    ("Tiler", "43.33", "F", "Trades", JOB),
    ("Plasterer", "43.31", "F", "Trades", JOB),
    ("Roofer", "43.91", "F", "Trades", JOB),
    ("Landscaper / groundworks", "43.12", "F", "Trades", JOB),
    ("General builder", "41.20", "F", "Trades", JOB),
    # Personal & other services (S)
    ("Hairdresser", "96.02", "S", None, SVC),
    ("Barber", "96.02", "S", None, SVC),
    ("Beauty salon", "96.02", "S", None, SVC),
    ("Nail salon", "96.02", "S", None, SVC),
    ("Spa / wellness", "96.04", "S", None, SVC),
    ("Tattoo studio", "96.09", "S", None, SVC),
    # Health & care (Q)
    ("Dental practice", "86.23", "Q", None, SVC),
    ("Physiotherapy clinic", "86.90", "Q", None, SVC),
    ("Veterinary practice", "75.00", "Q", None, SVC),
    # Arts, events & leisure (R)
    ("Gym / fitness studio", "93.13", "R", None, SVC),
    ("Yoga / pilates studio", "85.51", "R", None, SVC),
    ("Theatre", "90.04", "R", None, SVC),
    ("Music band / artist", "90.01", "R", None, SVC),
    ("Event / wedding planner", "82.30", "R", None, SVC),
    ("Photographer", "74.20", "R", None, SVC),
    ("Dance / music school", "85.52", "R", None, SVC),
    # Transport & delivery (H)
    ("Taxi / private hire", "49.32", "H", None, SVC),
    ("Courier / last-mile", "53.20", "H", None, SVC),
    ("Driving school", "85.53", "P", None, SVC),
    # Professional services (M)
    ("Bookkeeper / accountant", "69.20", "M", None, SVC),
    ("Architect", "71.11", "M", None, SVC),
    ("Graphic / web designer", "74.10", "M", None, SVC),
    ("Marketing agency", "73.11", "M", None, SVC),
    # Farming & growing (A)
    ("Farm shop / small farm", "01.50", "A", None, F6),
    ("Winery / vineyard", "01.21", "A", "Food manufacturing", F6),
]

# pack_queue first wave (language=sk). scores 1-5: market reach, module-reuse, build-ease.
# status: planned / in_progress / built / listed.  spec_key links to scripts/pack_spec.py.
# (business plain name, market, reuse, ease, status, spec_key)
QUEUE_SK = [
    ("Café / coffee shop", 5, 5, 5, "built", "hospitality_sk"),
    ("Restaurant", 5, 5, 5, "built", "hospitality_sk"),
    ("Baker (shop)", 5, 5, 5, "built", "baker_sk"),
    ("Butcher", 4, 5, 5, "built", "butcher_sk"),
    ("Bar / pub", 4, 5, 5, "planned", None),
    ("B&B / guesthouse", 4, 4, 4, "planned", None),
    ("Airbnb / short-stay host", 5, 3, 4, "planned", None),
    ("Greengrocer (fruit & veg)", 4, 5, 5, "planned", None),
    ("Convenience store", 4, 4, 4, "planned", None),
    ("Hairdresser", 5, 4, 4, "planned", None),
    ("Beauty salon", 5, 4, 4, "planned", None),
    ("Barber", 4, 4, 4, "planned", None),
    ("Patisserie / confectioner", 4, 5, 5, "planned", None),
    ("Florist", 3, 4, 5, "planned", None),
    ("Gym / fitness studio", 4, 3, 4, "planned", None),
    ("Caterer", 3, 5, 4, "planned", None),
    ("Brewery / craft beer", 3, 4, 4, "planned", None),
    ("Car dealer", 4, 3, 3, "planned", None),
    ("Electrician", 5, 3, 3, "planned", None),
    ("Plumber / heating", 5, 3, 3, "planned", None),
    ("Carpenter / joiner", 4, 3, 3, "planned", None),
    ("Photographer", 4, 3, 4, "planned", None),
    ("Dental practice", 3, 3, 3, "planned", None),
    ("Bookkeeper / accountant", 3, 4, 4, "planned", None),
]


def main():
    c = sqlite3.connect(DB)
    c.executescript("""
        DROP VIEW  IF EXISTS v_pack_candidates;
        DROP TABLE IF EXISTS pack_queue;
        DROP TABLE IF EXISTS business_types_atlas;
        DROP TABLE IF EXISTS industries;

        CREATE TABLE industries (
            nace_code     TEXT PRIMARY KEY,   -- NACE section letter
            level         TEXT NOT NULL,      -- 'section'
            name_official TEXT NOT NULL,
            name_plain    TEXT NOT NULL
        );
        CREATE TABLE business_types_atlas (
            id            INTEGER PRIMARY KEY,
            name_plain    TEXT NOT NULL UNIQUE,   -- the word the owner uses
            nace_class    TEXT NOT NULL,          -- 4-digit NACE class
            section_code  TEXT NOT NULL REFERENCES industries(nace_code),
            existing_vertical TEXT,               -- link to Phase 0-12 verticals (or NULL)
            module_set    TEXT NOT NULL           -- skeleton modules this pack carries
        );
        CREATE TABLE pack_queue (
            id            INTEGER PRIMARY KEY,
            business_type_id INTEGER NOT NULL REFERENCES business_types_atlas(id),
            language      TEXT NOT NULL,           -- sk/cs/de/hu/pl/en (one per pack)
            spec_key      TEXT,                    -- -> scripts/pack_spec.py REGISTRY
            status        TEXT NOT NULL DEFAULT 'planned'
                          CHECK(status IN ('planned','in_progress','built','listed')),
            assignee      TEXT,                    -- subagent id / owner
            market_score  INTEGER, reuse_score INTEGER, ease_score INTEGER,
            module_set    TEXT,
            notes         TEXT,
            UNIQUE(business_type_id, language)
        );
    """)

    c.executemany("INSERT INTO industries(nace_code,level,name_official,name_plain) VALUES(?,?,?,?)",
                  [(s[0], "section", s[1], s[2]) for s in SECTIONS])
    c.executemany("""INSERT INTO business_types_atlas
                     (name_plain,nace_class,section_code,existing_vertical,module_set)
                     VALUES(?,?,?,?,?)""", ATLAS)

    bt = {r[0]: r[1] for r in c.execute("SELECT name_plain,id FROM business_types_atlas")}
    rows = []
    for name, mk, ru, ea, status, spec in QUEUE_SK:
        ms = next((a[4] for a in ATLAS if a[0] == name), F6)
        rows.append((bt[name], "sk", spec, status, mk, ru, ea, ms))
    c.executemany("""INSERT INTO pack_queue
                     (business_type_id,language,spec_key,status,market_score,reuse_score,ease_score,module_set)
                     VALUES(?,?,?,?,?,?,?,?)""", rows)

    c.executescript("""
        CREATE VIEW v_pack_candidates AS
        SELECT q.id, b.name_plain AS business, i.name_plain AS sector,
               b.nace_class, q.language, q.status, q.spec_key,
               q.market_score AS market, q.reuse_score AS reuse, q.ease_score AS ease,
               (q.market_score*q.reuse_score*q.ease_score) AS priority,
               q.module_set, q.assignee
        FROM pack_queue q
        JOIN business_types_atlas b ON b.id = q.business_type_id
        JOIN industries i ON i.nace_code = b.section_code
        ORDER BY CASE q.status WHEN 'planned' THEN 0 WHEN 'in_progress' THEN 1
                               WHEN 'built' THEN 2 ELSE 3 END,
                 priority DESC, business;
    """)
    c.commit()

    # report
    print("Industry Atlas seeded.")
    print("  industries (NACE sections):", c.execute("SELECT COUNT(*) FROM industries").fetchone()[0])
    print("  business_types_atlas:", c.execute("SELECT COUNT(*) FROM business_types_atlas").fetchone()[0])
    print("  pack_queue rows:", c.execute("SELECT COUNT(*) FROM pack_queue").fetchone()[0],
          "| built:", c.execute("SELECT COUNT(*) FROM pack_queue WHERE status='built'").fetchone()[0],
          "| planned:", c.execute("SELECT COUNT(*) FROM pack_queue WHERE status='planned'").fetchone()[0])
    print("\nTop 10 NEXT-TO-BUILD (v_pack_candidates, planned, by priority):")
    for r in c.execute("""SELECT business, sector, priority, module_set FROM v_pack_candidates
                          WHERE status='planned' LIMIT 10"""):
        print(f"  {r[2]:>3}  {r[0]:<26} {r[1]:<22} [{r[3]}]")
    c.close()


if __name__ == "__main__":
    main()
