#!/usr/bin/env python3
"""
ASSET-FORGE · Turnkey Startup Packs — benchmark seeding
=======================================================
Phase 0 (Market Validation) and Phase 2 (Capital) need quantified TARGET
benchmarks the core `intelligence.db` does not carry. This creates a
`startup_benchmarks` table and seeds the boutique-hotel figures, each with a
low / typical / high band and a CITED source (researched live, 2024–2025).

    python3 scripts/seed_startup_benchmarks.py        # create + seed (idempotent)
    python3 scripts/seed_startup_benchmarks.py --show  # print the table

Safe & additive: only ever CREATE TABLE IF NOT EXISTS + REPLACE the pack's rows.
The 24-pack catalogue tables are untouched.
"""
from __future__ import annotations
import os, sqlite3, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "intelligence.db"))

DDL = """
CREATE TABLE IF NOT EXISTS startup_benchmarks (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    vertical  TEXT NOT NULL,
    metric_key TEXT NOT NULL,
    label     TEXT NOT NULL,
    unit      TEXT NOT NULL,           -- 'eur' | 'pct' | 'num'
    low       REAL,
    typical   REAL,
    high      REAL,
    source    TEXT NOT NULL,
    source_url TEXT,
    as_of     TEXT,
    UNIQUE(vertical, metric_key)
);
"""

# (metric_key, label, unit, low, typical, high, source, url, as_of)
HOTEL = [
    ("adr", "ADR — 4★ average daily rate", "eur", 127, 144, 241,
     "Fáilte Ireland Hotel Survey Nov/Dec 2024 (4★ ADR €143.50–€144.49; county range €127–€241)",
     "https://www.failteireland.ie/Research-Insights.aspx", "2024"),
    ("occupancy", "Occupancy — 4★", "pct", 0.602, 0.70, 0.741,
     "Fáilte Ireland Hotel Survey 2024 (4★ occ 60.2% Dec → 74.1% Nov)",
     "https://www.failteireland.ie/Research-Insights.aspx", "2024"),
    ("revpar", "RevPAR — 4★", "eur", 86.42, 97, 107.07,
     "Fáilte Ireland Hotel Survey 2024 (4★ RevPAR €86.42 Dec → €107.07 Nov)",
     "https://www.failteireland.ie/Research-Insights.aspx", "2024"),
    ("payroll_pct", "Labour cost (% of total revenue)", "pct", 0.25, 0.31, 0.35,
     "Hospitality labour benchmark 25–35% of revenue; US long-run 31.2% (Mandelbaum/CBRE; altametrics)",
     "https://altametrics.com/cost-of-labor/calculate-labor-cost.html", "2024"),
    ("fb_cost_pct", "F&B cost (% of F&B revenue)", "pct", 0.18, 0.28, 0.35,
     "USALI F&B cost-of-sales; academic luxury 17.86% (US) – 23.87% (Asia)",
     "https://ira.lib.polyu.edu.hk/bitstream/10397/89565/1/a0667-n11_858.pdf", "2023"),
    ("rooms_cost_pct", "Rooms dept cost ex-payroll (% of rooms rev)", "pct", 0.08, 0.12, 0.18,
     "USALI rooms departmental expense (rooms expense ~27–28% incl. labour; ex-labour ~8–18%)",
     "https://ira.lib.polyu.edu.hk/bitstream/10397/89565/1/a0667-n11_858.pdf", "2023"),
    ("gop_margin", "GOP margin (% of total revenue)", "pct", 0.30, 0.36, 0.383,
     "HotelData Q4-2025 full-year GOP margin 38.3%; academic luxury 33.2–36.7%",
     "https://hoteldata.com/reports/q4-2025-labor-costs-report", "2025"),
]


def seed(conn, vertical, rows):
    conn.execute(DDL)
    conn.executemany(
        """INSERT INTO startup_benchmarks
           (vertical, metric_key, label, unit, low, typical, high, source, source_url, as_of)
           VALUES (?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(vertical, metric_key) DO UPDATE SET
             label=excluded.label, unit=excluded.unit, low=excluded.low,
             typical=excluded.typical, high=excluded.high, source=excluded.source,
             source_url=excluded.source_url, as_of=excluded.as_of""",
        [(vertical, *r) for r in rows])
    conn.commit()


def show(conn):
    try:
        rows = conn.execute(
            "SELECT vertical, metric_key, label, unit, low, typical, high, as_of "
            "FROM startup_benchmarks ORDER BY vertical, metric_key").fetchall()
    except sqlite3.OperationalError:
        print("(table not created yet)"); return
    for r in rows:
        print(f"  {r[0]:>22} · {r[1]:<14} {r[5]} [{r[4]}–{r[6]}] {r[3]:<3} ({r[7]})  {r[2]}")


def main():
    conn = sqlite3.connect(DB)
    if "--show" in sys.argv:
        show(conn); return
    seed(conn, "boutique_hotel_4star", HOTEL)
    n = conn.execute("SELECT COUNT(*) FROM startup_benchmarks").fetchone()[0]
    print(f"✓ startup_benchmarks seeded — {n} rows total")
    show(conn)


if __name__ == "__main__":
    main()
