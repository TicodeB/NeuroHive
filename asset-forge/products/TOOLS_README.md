# P3 · P4 · P5 · P12 — À-la-carte tools (value-ladder Rung 1)

**Built:** 09/06/2026 · `python3 scripts/build_alacarte_tools.py` (re-runnable) · v1.0
**Pattern:** each tool = its already-validated sheet from the P1/P2 flagship builders
(+ its own bilingual Start-Here sheet + safe DEMO: notice sheet + sheet protection,
never `insert_rows` — P13 v1.1 postmortem rule). All files validated: zip/XML
well-formed, tab names ≤ 31 chars, zero merged-range overlaps.

| # | Product | Price (locked §2) | Source sheet | Parent (Omnibus: child < parent) |
|---|---|---|---|---|
| P3 | H&S Risk Assessment & Safety Statement Builder | **€19** | P1 `build_hs` | P1 €34 |
| P4 | Cashflow & P&L Tracker | **€24** | P2 `build_cashflow` | P2 €49 |
| P5 | Fire Safety Register & Checks Log | **€15** | P1 `build_fire` | P1 €34 |
| P12 | Staff Training & Induction Matrix | **€15** | P2 `build_training` | P2 €49 |

**Files:** `P{3,4,5,12}_*.xlsx` (full) + `P{3,4,5,12}_DEMO_*.xlsx` (locked preview;
demos also copied to site `/downloads/`).

**Bilingual EN/SK:** inherited from the flagship builders (already shipped in P1/P2).
Same standing caveat: Slovak needs the native-editor pass before SK *marketing copy*
is published — the in-file SK shipped with P1/P2 v1.0 applies here identically.

**Listing copy:** see `marketing/listings_etsy_gumroad.md` (per-SKU titles, tags,
descriptions) and the product page `products/tools.html` on the site.

**Funnel role (MONETIZATION_BRIEF §7):** bite-priced entry (Rung 1) → upsell to the
parent pack (Rung 2: P1/P2) → Hospitality Pro Bundle €69 (Rung 3). Each tool page
cross-sells its parent; genuine sum-of-parts savings keep it Omnibus-safe.
