# Localisation pipeline — one vertical → many languages

**Phase 13h** · Premium-Pack track. How a locked pack becomes a clean,
single-language edition in any language, with **zero builder changes**.

> **Rule (Samuel, 30/05):** one language per file (no bilingual cramming). Each
> edition must read natively. **English is authored in-house**; SK/CS/DE/HU/PL
> public copy needs a **native-editor pass before listing** (standing rule).

---

## The two axes (kept separate by design)

A pack = **vertical** (what trade) × **language** (what words). They live apart:

| Axis | Where it lives | Example |
|---|---|---|
| **Vertical terminology** (trade words: revenue lines, seed items, role labels) | a `PackSpec` in `scripts/pack_spec.py` | `bar_sk` → "Čapované pivo 0,5 l" |
| **UI chrome** (section headers, column headers, help notes, dropdowns, status words, dashboard insight sentences) | a language block in `scripts/i18n.py` | `EN["ledger_gross"]` = "GROSS MARGIN" |

The builder (`build_pack.py`) holds **only** the layout + formulas. It reads the
language block via `get_strings(spec.language)` and the trade words from the
spec. So a new language is a **data** change, never a code change.

```
  PackSpec (vertical, language, palette, trade terms)
        │
        ├── i18n.get_strings(language)  →  UI chrome strings
        ▼
  build_pack.build(spec_key)  →  products/pack_<key>.xlsx   (one language, premium)
```

---

## How to add a language (e.g. German `de`)

1. **`scripts/i18n.py`** — copy the `SK` block to a new `DE = {…}`, translate
   **every value** natively (keep the `{…}` placeholders in the `ins_*` /
   `*_tmpl` strings intact — they carry live cell refs/numbers). Add it to
   `STRINGS`. Run `python3 scripts/i18n.py` → must print "✅ de: 75 keys,
   complete" (the parity check fails the build if a key is missing).
2. **`scripts/pack_spec.py`** — add a `PackSpec` for the vertical in that
   language (`language="de"`), translating the trade terminology. Register it.
3. `python3 scripts/build_pack.py <key>` → the localised pack.
4. **Native-editor pass** on all visible copy before listing (non-English).

That's it — no `build_pack.py` edit. The legibility guarantee (`ds.fit`),
FP&A spine (plan/variance), drill-down and validation all carry over for free.

---

## What's shipped now

| Pack | Lang | Status |
|---|---|---|
| hospitality, bar, butcher, baker, greengrocer, patisserie | `sk` | built (Slovak reference) |
| **hospitality** | **`en`** | **built — first localisation, English authored in-house** |

**Regression proof:** after externalising the chrome, all six `*_sk.xlsx` rebuild
**0 cell diffs** vs their committed versions — the refactor changed nothing for
Slovak. `pack_hospitality_en.xlsx` validated: 15 XML parts well-formed · 0
merged-range overlaps · tabs ≤31 · 7 KPI tiles all drill-down-linked · English
variance narrative present · ledger headers `Year · Plan (year) · Variance € ·
Variance %` · **0 Slovak-diacritic leaks** in the chrome.

## Language coverage of the string table (`scripts/i18n.py`)
- `sk` — Slovenčina (reference, 75 keys)
- `en` — English (75 keys, native)
- *next candidates:* `cs` (Czech — closest to SK, fastest), then `de` / `pl` /
  `hu` by market demand. Each needs the native-editor pass before launch.

## Notes / honest limits
- **Currency:** all editions use the € format from `design_system.Theme`. A
  non-Eurozone language edition (e.g. a future GBP/PLN/HUF variant) would need a
  currency override on the Theme — not done here; flag at listing.
- **Numbers/dates** already follow EU conventions (DD/MM/YYYY, comma thousands)
  across languages, which suits the EU target market.
- Machine translation is **not** acceptable for public SK/CS/DE/HU/PL copy — the
  pipeline makes the swap trivial, but quality is a human gate.
