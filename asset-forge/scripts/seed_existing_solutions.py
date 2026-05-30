#!/usr/bin/env python3
"""
Phase 8 — Monetization: populate `existing_solutions` with live-verified (30/05/2026)
sales-platform fees/VAT facts + representative template-marketplace comparables, and
lock `products.platform` to the chosen primary (Lemon Squeezy).

Idempotent + re-runnable: clears the Phase-8 rows it owns, re-inserts, then overwrites
the products.platform placeholder. All fee/VAT facts are sourced (see source_url) and
were re-verified live — never stated from memory (brief §3).

Run:  python3 scripts/seed_existing_solutions.py
"""
import os
import sqlite3

DB = os.path.join(os.path.dirname(__file__), os.pardir, "intelligence.db")

# (name, category, price_eur, key_gaps, source_url)
# price_eur: for platforms this is the *fixed monthly* cost (0.0 = free tier / no monthly);
# fee % + per-tx detail lives in key_gaps because the schema has no fee column.
ROWS = [
    # --- Sales platforms (MoR / EU-VAT verified live 30/05/2026) ---
    ("Lemon Squeezy", "Sales platform — Merchant of Record", 0.0,
     "CHOSEN PRIMARY. Full MoR: collects+remits EU VAT/global tax, seller never files. "
     "Fee 5% + $0.50 BUT +1.5% intl (non-US) card, +1.5% PayPal, +0.5% subs -> ~6.5%+$0.50 "
     "effective for an Irish seller to EU buyers. No monthly cost. Twice-monthly payout via "
     "Stripe (SEPA ok). No built-in discovery. Risk: acquired by Stripe Jul-2024, roadmap "
     "uncertainty (Stripe Managed Payments in beta).",
     "https://www.swell.is/content/gumroad-pricing"),
    ("Gumroad", "Sales platform — Merchant of Record", 0.0,
     "CHOSEN FALLBACK. Full MoR SINCE 01/01/2025 (collects+remits global tax). Flat 10% + "
     "$0.50 all-in (processing bundled), NO intl/PayPal surcharges -> predictable. Weekly "
     "(Fri) payout via Stripe. Built-in Discover traffic BUT Discover-sourced sales cost "
     "30%. Higher fee than LS; switch-to target if LS degrades.",
     "https://www.wearefounders.uk/gumroad-fees-2026-what-sellers-actually-pay-per-sale"),
    ("Payhip", "Sales platform — partial MoR", 0.0,
     "REJECTED on the heavily-weighted criterion. Only PARTIAL MoR: collects EU/UK VAT but "
     "seller stays legal seller-of-record (sources disagree on remittance) -> re-introduces "
     "EU VAT filing risk for an Irish seller. Free 5% + separate ~2.9%+$0.30 processing "
     "(~7.9%); Plus $29/mo +2%; Pro $99/mo +0%. Instant payout.",
     "https://www.scaleuphere.com/guides/payhip-pricing-fees-2025"),
    ("Etsy", "Marketplace — discovery channel", 0.0,
     "DISCOVERY CHANNEL ONLY (not MoR storefront). Unmatched template buyer intent (1,000+ "
     "restaurant + 5,000+ spreadsheet templates listed). Fees: $0.20 listing + 6.5% tx + "
     "~3-4% processing + optional ads. Acts as supplier for EU VAT on digital items. Gap: "
     "static files only -> needs PDF + Google-Sheets 'make a copy' link workaround.",
     "https://www.etsy.com/market/restaurant_spreadsheet_template"),
    ("Ko-fi", "Sales platform — no MoR", 0.0,
     "REJECTED. No VAT handling / not a MoR; tip-led. 0% on free tier but fails the decisive "
     "EU-VAT zero-admin bar for an Ireland-based digital-goods seller.",
     "https://www.thinkific.com/blog/best-marketplace-sell-digital-products/"),

    # --- Template-marketplace comparables (price benchmarks for our products) ---
    ("Etsy HACCP / allergen template bundles", "Comparable product — hospitality compliance", 34.0,
     "Benchmark band EUR 19-49 for HACCP/allergen template bundles. Our P1 (EUR 34) sits "
     "mid-band. Gap in comparables: static PDFs, not linked live sheets; rarely bilingual; "
     "rarely Ireland/EU-reg-specific (852/2004 + 1169/2011).",
     "https://www.etsy.com/market/restaurant_spreadsheet_template"),
    ("Advanced Catering Business Digital Planner (12-in-1)", "Comparable product — hospitality ops", 49.0,
     "Live direct competitor in our niche (hospitality ops planner). Benchmarks our P2 "
     "(EUR 49) ops-bundle band EUR 39-59. Gap: generic planner, not GP/labour-% costing "
     "engine tied to forecast sales.",
     "https://www.etsy.com/listing/893928336/advanced-catering-business-digital"),
    ("Etsy staff rota / finance tracker templates", "Comparable product — ops/finance", 24.0,
     "Finance/rota trackers benchmark EUR 15-35; our P4 Cashflow (EUR 24) and rota assets "
     "sit inside. Gap: single-sheet, no P&L roll-up or scenario toggle.",
     "https://www.etsy.com/market/staff_rota_template"),
]

PLATFORM_PRIMARY = "Lemon Squeezy"
# Phase-8 owned categories (so re-runs are idempotent without nuking other phases' rows).
OWNED_CATEGORIES = (
    "Sales platform — Merchant of Record",
    "Sales platform — partial MoR",
    "Sales platform — no MoR",
    "Marketplace — discovery channel",
    "Comparable product — hospitality compliance",
    "Comparable product — hospitality ops",
    "Comparable product — ops/finance",
)


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # Idempotent: clear the rows this script owns, then re-insert.
    placeholders = ",".join("?" for _ in OWNED_CATEGORIES)
    cur.execute(f"DELETE FROM existing_solutions WHERE category IN ({placeholders})",
                OWNED_CATEGORIES)
    cur.executemany(
        "INSERT INTO existing_solutions (name, category, price_eur, key_gaps, source_url) "
        "VALUES (?,?,?,?,?)", ROWS)

    # Lock the platform: overwrite the "Lemon Squeezy (TBD Phase 8)" placeholder.
    cur.execute("UPDATE products SET platform = ?", (PLATFORM_PRIMARY,))

    con.commit()

    n_sol = cur.execute("SELECT COUNT(*) FROM existing_solutions").fetchone()[0]
    n_prod = cur.execute("SELECT COUNT(*) FROM products WHERE platform = ?",
                         (PLATFORM_PRIMARY,)).fetchone()[0]
    print(f"existing_solutions rows: {n_sol}")
    print(f"products on platform '{PLATFORM_PRIMARY}': {n_prod}")
    print("\nexisting_solutions:")
    for r in cur.execute("SELECT id, name, category, price_eur FROM existing_solutions "
                         "ORDER BY id"):
        print("  ", r)
    con.close()


if __name__ == "__main__":
    main()
