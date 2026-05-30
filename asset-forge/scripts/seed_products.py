#!/usr/bin/env python3
"""
ASSET-FORGE · Phase 7 — Productisation
Seeds the `products` table from PRODUCT_ROADMAP.md so the roadmap is queryable in the DB.

Schema (init_db.py): products(id, name, target_business_type, bundled_asset_ids, price_eur, platform)

- bundled_asset_ids : comma-separated digital_assets.id values (the asset map is the source of truth).
- price_eur         : INDICATIVE vs marketplace comparables — final pricing locked in Phase 8 (verify live).
- platform          : preliminary lean (Lemon Squeezy) — final platform decision is Phase 8.

Idempotent: clears and re-inserts. Run:  python3 scripts/seed_products.py
"""
import sqlite3
import os

DB = os.path.join(os.path.dirname(__file__), "..", "intelligence.db")

# Roadmap order (hospitality-first override applied). Tuple:
# (name, target_business_type, bundled_asset_ids, price_eur, platform)
PRODUCTS = [
    ("Café / Restaurant Compliance Pack",
     "Hospitality (café, restaurant, bar, B&B, hotel)",
     "1,2,3,4,5,16,17", 34, "Lemon Squeezy (TBD Phase 8)"),
    ("Hospitality Operations & GP Bundle",
     "Hospitality (bar, café, restaurant, hotel)",
     "6,7,8,9,11", 49, "Lemon Squeezy (TBD Phase 8)"),
    ("H&S Risk Assessment & Safety Statement Builder",
     "Universal (all 21 business types)",
     "16,51", 19, "Lemon Squeezy (TBD Phase 8)"),
    ("Cashflow & P&L Tracker",
     "Universal (all 21 business types)",
     "8", 24, "Lemon Squeezy (TBD Phase 8)"),
    ("Fire Safety Register & Checks Log",
     "Universal (premises-based, 17 business types)",
     "17", 15, "Lemon Squeezy (TBD Phase 8)"),
    ("Trades Quote → Job → Invoice Suite",
     "Trades (electrician, plumber, carpenter, painter, tiler, landscaper)",
     "39,48,53,54,8,52", 39, "Lemon Squeezy (TBD Phase 8)"),
    ("Recipe / BOM & Batch Costing Calculator",
     "Food mfg + hospitality kitchens",
     "22,7", 29, "Lemon Squeezy (TBD Phase 8)"),
    ("Food-Manufacturing Compliance Core",
     "Food mfg (bakery, butchery, dairy, beverage, ready-meals)",
     "1,3,4,5,30,31,32,35,36", 59, "Lemon Squeezy (TBD Phase 8)"),
    ("Staff Training & Induction Matrix",
     "Cross-vertical HR (hospitality, food mfg, mfg)",
     "10", 15, "Lemon Squeezy (TBD Phase 8)"),
    ("Manufacturing ISO 9001 / Quality Pack",
     "Non-food mfg (metal, plastics, packaging, joinery, electronics)",
     "38,46,30,28,42", 49, "Lemon Squeezy (TBD Phase 8)"),
    ("Electrician / Gas Compliance Cert Pack",
     "Trades — regulated (electrician/Safe Electric, plumber-gas/RGI)",
     "47,51,16,52,41", 34, "Lemon Squeezy (TBD Phase 8)"),
    ("Product Label & Nutrition Declaration Generator",
     "Food mfg (bakery, ready-meals, beverage)",
     "23,26", 29, "Lemon Squeezy (TBD Phase 8)"),
]


# Value-ladder tier per base product (MONETIZATION_BRIEF §7).
# pricing_tier: free | module | pack | kit. parent_product = the pack/kit a row rolls
# up into (NULL for top-level). Single-asset utilities are the standalone "modules"
# that also sell à-la-carte; multi-asset products are "packs"; broad bundles are "kits".
# Keyed by product name so it survives id changes.
LADDER = {
    # name: (pricing_tier, parent_product or None)
    "Café / Restaurant Compliance Pack": ("pack", "Compliance Everything"),
    "Hospitality Operations & GP Bundle": ("pack", "Hospitality Pro Bundle"),
    "H&S Risk Assessment & Safety Statement Builder": ("module", "Safety Starter"),
    "Cashflow & P&L Tracker": ("module", "Money Toolkit"),
    "Fire Safety Register & Checks Log": ("module", "Safety Starter"),
    "Trades Quote → Job → Invoice Suite": ("pack", "Money Toolkit"),
    "Recipe / BOM & Batch Costing Calculator": ("module", "Money Toolkit"),
    "Food-Manufacturing Compliance Core": ("pack", "Compliance Everything"),
    "Staff Training & Induction Matrix": ("module", None),  # high-attach à-la-carte / order-bump
    "Manufacturing ISO 9001 / Quality Pack": ("pack", "Compliance Everything"),
    "Electrician / Gas Compliance Cert Pack": ("pack", "Compliance Everything"),
    "Product Label & Nutrition Declaration Generator": ("module", None),
}


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("DELETE FROM products")
    cur.executemany(
        "INSERT INTO products (name, target_business_type, bundled_asset_ids, price_eur, platform) "
        "VALUES (?,?,?,?,?)",
        PRODUCTS,
    )

    # Value-ladder columns (guarded — same idempotent pattern seed_compliance.py uses).
    cols = [d[1] for d in cur.execute("PRAGMA table_info(products)")]
    if "pricing_tier" not in cols:
        cur.execute("ALTER TABLE products ADD COLUMN pricing_tier TEXT")
    if "parent_product" not in cols:
        cur.execute("ALTER TABLE products ADD COLUMN parent_product TEXT")
    for name, (tier, parent) in LADDER.items():
        cur.execute("UPDATE products SET pricing_tier=?, parent_product=? WHERE name=?",
                    (tier, parent, name))
    con.commit()

    n = cur.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    print(f"Seeded products table: {n} products.")
    # Integrity: every bundled asset id must exist in digital_assets
    valid = {r[0] for r in cur.execute("SELECT id FROM digital_assets")}
    bad = []
    for pid, name, ids in cur.execute("SELECT id, name, bundled_asset_ids FROM products"):
        for a in ids.split(","):
            if int(a) not in valid:
                bad.append((name, a))
    if bad:
        print("WARNING — bundled asset ids not in digital_assets:", bad)
    else:
        print("Integrity OK — all bundled_asset_ids resolve to existing digital_assets.")
    con.close()


if __name__ == "__main__":
    main()
