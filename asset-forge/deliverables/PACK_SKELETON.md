# PACK SKELETON — the reusable spine for every Premium Pack

**Phase 13c · 31/05/2026 · branch `claude/cool-planck-rYR4I`**

Locks the structure proven by the P2 SK premium pilot so a new vertical =
**swap the terminology + the palette**, not a rebuild. Pairs with:
- `scripts/design_system.py` — the look (palette, gridless canvas, tables, KPI tiles)
- `scripts/pack_spec.py` — the mechanism (`PackSpec` + validator + registry)
- `scripts/build_p2_sk_premium.py` — the reference build (becomes spec-driven in 13d)

> **Why a fixed skeleton?** Consistency *is* the premium signal, and it means we
> build the formulas/dashboard once and resell across butcher, retailer, baker,
> dealer, … — the universal-core logic from the brief, applied to packaging.

---

## 1. The two axes (keep them separate)

A pack is one cell of a matrix:

| Axis | Varies | Where it lives |
|---|---|---|
| **Vertical** | terminology + which modules + palette | `PackSpec` (`pack_spec.py`) |
| **Language** | the words' language (one per file) | `PackSpec.language` (sk/cs/de/hu/pl/en) |

The **structure and every formula stay constant.** Only labels/line-items and
colours change per vertical; only the language changes per edition.

> **Terminology, not slang (Samuel, 31/05):** use the *correct professional
> vocabulary of the trade* — a butcher's "carcass / primal cut / trim loss /
> bone-out yield", a dealer's "units / gross per unit / aged stock / recon". The
> register is professional, not insider jokes.

---

## 2. The fixed spine (every pack, always)

| # | Sheet | module_type | Purpose |
|---|---|---|---|
| 00 | Method / Start Here | `METHOD` | what's inside · the daily/weekly rhythm · colour legend · disclaimer |
| 01 | Daily Planner | `PLANNER` | 3 priorities · time-blocked day · open/close checklist |
| 02 | Dashboard | `DASHBOARD` | KPI tiles + plain-language **Insights**, pulled live from the modules below |

The dashboard is the hero. Its KPI tiles and insight sentences **cite metrics**
exposed by the operational modules (validated: a KPI can't reference an absent
module/metric).

---

## 3. Operational module catalogue (pick per vertical)

Each is a reusable template; a vertical includes the ones it needs and supplies
the trade terms. Metrics in the last column are what the dashboard may cite.

| module_type | What it is | Trade terms it exposes | Metrics |
|---|---|---|---|
| `LEDGER_12M` | 12-month cash flow + P&L | revenue_lines · cos_lines · overhead_lines | revenue_total · gross · net · cash_close |
| `MARGIN` | per-unit costing & margin | unit_label · seed_items | avg · below_target |
| `STOCK` | stock / yield / loss | item_label · loss_label · seed_items | loss_value |
| `LABOUR` | rota & labour-% of sales | role_label · target_pct | pct · cost |
| `TAKINGS` | daily takings & reconciliation | source_label | variance_total |
| `TRAINING` | training / competency matrix | topics | — |

Catalogue is **extensible** (future: `JOBS`, `BOOKINGS`, `FLEET`, `BOX_OFFICE`
for trades/airlines/theatres/bands) — add a `module_type` + its required term
keys in `MODULE_SLOTS`, and the validator + builder pick it up.

---

## 4. How a vertical plugs in (`PackSpec`)

```python
PackSpec(
  key="butcher_sk", vertical="Mäsiarstvo", language="sk",
  palette={"primary": "7A2E2E", "accent": "A23E3E", "ink": "2B1A1A"},
  modules=[ Module("METHOD", {...}), Module("PLANNER", {...}),
            Module("DASHBOARD", {...}), Module("LEDGER_12M", {...}),
            Module("MARGIN", {...}), Module("STOCK", {...}), ... ],
)
```

`validate(spec)` enforces: the 3 fixed modules present · ≥1 operational module ·
2-letter language · palette has primary/accent/ink · every module's required term
keys non-empty · every dashboard KPI cites a real `module.metric`.

### The swap, proven (STOCK module, same slot)
| | item label | loss label | first seed item |
|---|---|---|---|
| `hospitality_sk` | Položka | Straty | Čapované pivo |
| `butcher_sk` | Diel / surovina | Orez a strata | Jatočné telo bravčové (polovica) |

Butcher also gains a vertical-specific KPI — **Hodnota orezu a strát** — by
citing `STOCK.loss_value`, and a meat-red palette. Same formulas underneath.

---

## 5. Build flow (13d wires this)

```
PackSpec  ─┐
           ├─►  generic builder  ─►  design_system.py  ─►  <vertical>_<lang>.xlsx
Theme(pal) ─┘     (one per module_type, formulas fixed)        (+ PNG preview)
```

Today's `build_p2_sk_premium.py` is the reference implementation of those
per-module builders; 13d refactors it to read a `PackSpec` (starting by feeding
it `hospitality_sk` and reproducing the pilot byte-for-functionality), then
builds `butcher_sk` as the first net-new vertical with zero new layout code.

---

## 6. Standing rules carried in
- **One language per file** (Premium-Pack carve-out; AGENTS.md). Native-quality
  translation per language; native-editor pass before any public listing.
- **Settings** sheet is optional (business name / year / targets) — fold into
  `METHOD` unless a vertical needs standalone config.
- Validate every pack: `python3 scripts/pack_spec.py` (specs) + the xlsx
  integrity check (openpyxl reload · XML well-formed · no merged-range overlaps ·
  tabs ≤31 · dashboard anchors resolve) — soffice is broken in this sandbox.
