#!/usr/bin/env python3
"""
ASSET-FORGE — intelligence.db initialiser (Phase 0).

Creates the normalised SQLite schema from brief Section [8] and seeds the
fixed analytical taxonomy from Section [5] (verticals, business types,
departments). It seeds ONLY the structural spine — no asset rows, no scores,
no research content. Those are produced in Phase 1+.

Idempotent: safe to re-run. Uses CREATE TABLE IF NOT EXISTS and INSERT OR
IGNORE against natural keys, so re-running will not duplicate the taxonomy.

Usage:
    python3 scripts/init_db.py [--db PATH] [--reset]

    --reset   drop all tables first (destructive), then rebuild + reseed.
"""

import argparse
import os
import sqlite3
import sys

# DB lives at the project root (one level up from scripts/).
DEFAULT_DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "intelligence.db")

# --- Schema (brief Section [8]) ---------------------------------------------
# asset_map carries the raw 0-3 axis scores from rubric [6] so tiers can be
# re-cut later, plus a `buyer` column to satisfy the BUYER dimension that
# Section [5] requires on every asset (operator/auditor/consultant).
SCHEMA = """
CREATE TABLE IF NOT EXISTS verticals (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS business_types (
    id           INTEGER PRIMARY KEY,
    vertical_id  INTEGER NOT NULL REFERENCES verticals(id),
    name         TEXT NOT NULL,
    work_context TEXT,                       -- solo/team · on-site/off-site/on-the-road (esp. trades)
    UNIQUE (vertical_id, name)
);

CREATE TABLE IF NOT EXISTS departments (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS workflows (
    id            INTEGER PRIMARY KEY,
    department_id INTEGER NOT NULL REFERENCES departments(id),
    name          TEXT NOT NULL,
    description   TEXT,
    UNIQUE (department_id, name)
);

CREATE TABLE IF NOT EXISTS digital_assets (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    asset_type  TEXT,                          -- Spreadsheet tracker · Calculator · Dashboard · Form/checklist · SOP · Log book · Diary/planner · Quote generator · Invoice · Roster/scheduler · Database
    description TEXT
);

CREATE TABLE IF NOT EXISTS asset_map (
    id               INTEGER PRIMARY KEY,
    business_type_id INTEGER NOT NULL REFERENCES business_types(id),
    department_id    INTEGER REFERENCES departments(id),
    asset_id         INTEGER NOT NULL REFERENCES digital_assets(id),
    buyer            TEXT,                      -- operator | auditor | consultant  (Section [5] BUYER dimension)
    legal            INTEGER CHECK (legal     BETWEEN 0 AND 3),
    revenue          INTEGER CHECK (revenue   BETWEEN 0 AND 3),
    pain             INTEGER CHECK (pain      BETWEEN 0 AND 3),
    frequency        INTEGER CHECK (frequency BETWEEN 0 AND 3),
    score            INTEGER,                   -- (legal*3)+(revenue*2)+(pain*2)+(frequency*1), max 24
    tier             TEXT,                      -- MUST | SHOULD | COULD | WON'T
    evidence_url     TEXT,
    notes            TEXT,
    UNIQUE (business_type_id, asset_id, buyer)
);

CREATE TABLE IF NOT EXISTS pain_points (
    id               INTEGER PRIMARY KEY,
    business_type_id INTEGER NOT NULL REFERENCES business_types(id),
    description      TEXT NOT NULL,
    severity         TEXT,
    source_url       TEXT
);

CREATE TABLE IF NOT EXISTS existing_solutions (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    category    TEXT,
    price_eur   REAL,
    key_gaps    TEXT,
    source_url  TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id                 INTEGER PRIMARY KEY,
    name               TEXT NOT NULL,
    target_business_type TEXT,
    bundled_asset_ids  TEXT,                    -- comma-separated digital_assets.id list
    price_eur          REAL,
    platform           TEXT
);
"""

# Helper views (brief Section [8]).
VIEWS = """
DROP VIEW IF EXISTS v_must_haves;
CREATE VIEW v_must_haves AS
SELECT am.id, v.name AS vertical, bt.name AS business_type,
       da.name AS asset, am.buyer, am.score, am.tier, am.evidence_url
FROM asset_map am
JOIN business_types bt ON bt.id = am.business_type_id
JOIN verticals v       ON v.id = bt.vertical_id
JOIN digital_assets da ON da.id = am.asset_id
WHERE am.tier = 'MUST'
ORDER BY v.name, bt.name, am.score DESC;

-- Assets that are MUST across >= 3 business types: highest-leverage products
-- (build once, sell many).
DROP VIEW IF EXISTS v_universal_core;
CREATE VIEW v_universal_core AS
SELECT da.id AS asset_id, da.name AS asset,
       COUNT(DISTINCT am.business_type_id) AS must_in_n_business_types
FROM asset_map am
JOIN digital_assets da ON da.id = am.asset_id
WHERE am.tier = 'MUST'
GROUP BY da.id, da.name
HAVING COUNT(DISTINCT am.business_type_id) >= 3
ORDER BY must_in_n_business_types DESC;
"""

# --- Taxonomy seed (brief Section [5]) --------------------------------------
TAXONOMY = {
    "Hospitality": [
        "Bar/pub", "Café/coffee shop", "Restaurant", "B&B/guesthouse", "Hotel",
    ],
    "Food manufacturing": [
        "Bakery", "Butchery/meat", "Dairy", "Beverage", "Ready meals/catering production",
    ],
    "Non-food manufacturing": [
        "Metal/engineering", "Plastics/injection", "Packaging/print",
        "Joinery/furniture", "Light electronics",
    ],
    "Trades": [
        "Electrician", "Plumber/heating", "Carpenter/joiner",
        "Painter/decorator", "Tiler", "Landscaper/groundworks",
    ],
}

# Department spine (brief Section [5]).
DEPARTMENTS = [
    "Operations/Production",
    "Quality & Compliance",
    "HR & People",
    "Finance & Management Accounting",
    "Sales/Marketing/CRM",
    "Procurement & Inventory",
    "Maintenance & Asset Management",
    "Front-of-house/Bookings/Customer",
    "Job & Schedule Management",
    "Reporting/KPIs/Dashboards",
]

TABLES = [
    "products", "existing_solutions", "pain_points", "asset_map",
    "digital_assets", "workflows", "departments", "business_types", "verticals",
]


def reset(conn):
    conn.executescript("DROP VIEW IF EXISTS v_universal_core; DROP VIEW IF EXISTS v_must_haves;")
    for t in TABLES:
        conn.execute(f"DROP TABLE IF EXISTS {t};")
    conn.commit()


def build(conn):
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.executescript(SCHEMA)
    conn.executescript(VIEWS)
    conn.commit()


def seed_taxonomy(conn):
    for vertical, types in TAXONOMY.items():
        conn.execute("INSERT OR IGNORE INTO verticals (name) VALUES (?);", (vertical,))
        vid = conn.execute("SELECT id FROM verticals WHERE name = ?;", (vertical,)).fetchone()[0]
        for bt in types:
            conn.execute(
                "INSERT OR IGNORE INTO business_types (vertical_id, name) VALUES (?, ?);",
                (vid, bt),
            )
    for dept in DEPARTMENTS:
        conn.execute("INSERT OR IGNORE INTO departments (name) VALUES (?);", (dept,))
    conn.commit()


def summarise(conn):
    counts = {}
    for t in ("verticals", "business_types", "departments", "digital_assets", "asset_map"):
        counts[t] = conn.execute(f"SELECT COUNT(*) FROM {t};").fetchone()[0]
    print("ASSET-FORGE intelligence.db initialised.")
    print(f"  verticals      : {counts['verticals']}")
    print(f"  business_types : {counts['business_types']}")
    print(f"  departments    : {counts['departments']}")
    print(f"  digital_assets : {counts['digital_assets']}  (filled in Phase 1+)")
    print(f"  asset_map rows : {counts['asset_map']}  (filled in Phase 1+)")
    views = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='view' ORDER BY name;").fetchall()]
    print(f"  views          : {', '.join(views)}")


def main():
    ap = argparse.ArgumentParser(description="Initialise ASSET-FORGE intelligence.db")
    ap.add_argument("--db", default=DEFAULT_DB, help="path to SQLite DB (default: project-root/intelligence.db)")
    ap.add_argument("--reset", action="store_true", help="drop all tables first (destructive)")
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    try:
        if args.reset:
            reset(conn)
        build(conn)
        seed_taxonomy(conn)
        summarise(conn)
    finally:
        conn.close()
    print(f"  db path        : {args.db}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
