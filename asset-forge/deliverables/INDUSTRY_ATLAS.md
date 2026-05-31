# INDUSTRY ATLAS + PACK QUEUE — the subagent dispatch board

**Phase 13e · 31/05/2026 · branch `claude/cool-planck-rYR4I`**

Captures "all industries and sub-businesses" in `intelligence.db` so packs can be
produced **in parallel by subagents** (Samuel, 31/05). Built on **NACE Rev.2**
(EU official classification) with a **plain trade name** on every row.

Built by `scripts/seed_atlas.py` (idempotent — only touches the 3 new tables +
view; never the existing Phase 0–12 schema).

---

## 1. The three tables

| Table | What it holds | Rows |
|---|---|---|
| `industries` | NACE **sections** (broad sectors) + friendly plain names | 12 |
| `business_types_atlas` | specific **sub-businesses** (the customer): plain name · NACE class · section · existing-vertical link · `module_set` | 64 |
| `pack_queue` | **the dispatch board**: one row per (business × language) with `status` · `spec_key` · `assignee` · scores · `module_set` | 24 (seed wave, `sk`) |

`status ∈ {planned, in_progress, built, listed}` · `spec_key` → `scripts/pack_spec.py`
REGISTRY · `UNIQUE(business_type_id, language)` stops duplicate work.

Extensible by design: NACE has ~600 classes; we seeded the SME-relevant spine and
subagents/future phases can add rows (more business types, more languages) without
schema change.

---

## 2. The ranking view — `v_pack_candidates`

Orders the queue by **status** (planned first) then **priority = market × reuse ×
ease** (each 1–5), so a subagent just takes the top `planned` row.

- **market** — reach / demand of the niche
- **reuse** — how much of the existing module set fits as-is (build cheapness)
- **ease** — build difficulty (5 = trivial)

**Top of the queue right now** (planned, by priority):

| Priority | Business | Sector | Modules |
|---|---|---|---|
| 100 | Bar / pub | Hospitality & stays | full 6 |
| 100 | Greengrocer (fruit & veg) | Retail & motor | full 6 |
| 100 | Patisserie / confectioner | Making & production | full 6 |
| 80 | Beauty salon | Personal & other services | service 5 |
| 80 | Hairdresser | Personal & other services | service 5 |
| 64 | B&B / guesthouse · Barber · Convenience store | — | — |

**Built (proof):** Café/Coffee shop + Restaurant → `hospitality_sk`; Baker →
`baker_sk`; Butcher → `butcher_sk`.

---

## 3. How a subagent uses it (13f)

```
1. SELECT * FROM v_pack_candidates WHERE status='planned' LIMIT 1;   -- claim top row
2. UPDATE pack_queue SET status='in_progress', assignee='<agent>' WHERE id=?;
3. author a PackSpec (terminology + palette) in scripts/pack_spec.py for that trade
4. python3 scripts/build_pack.py <spec_key>      -- generic builder + design system + ds.fit()
5. validate (XML well-formed · no merged overlaps · tabs ≤31 · anchors resolve)
6. UPDATE pack_queue SET status='built', spec_key='<key>' WHERE id=?;
```

`module_set` on each row tells the agent which skeleton modules that trade needs
(food/retail = full 6; services = 5, no STOCK; trades = job-oriented set). The
agent's only creative work is the **terminology** (correct trade vocabulary) and
the **palette** — structure, formulas, dashboard and legibility come for free.

Many agents run at once safely: each claims a distinct `pack_queue` row
(`UNIQUE(business_type_id, language)` + the `in_progress` lock prevent collisions).

---

## 4. Languages

Seed wave is **`sk`** only (one language per pack — Premium-Pack carve-out). The
same queue extends to `cs / de / hu / pl / en` by inserting rows per language;
localisation is a later sub-phase (native-quality pass required per language).

---

## 5. Rebuild / query
```
python3 scripts/seed_atlas.py            # rebuild atlas + queue (idempotent)
# inspect (no sqlite3 CLI in sandbox — use Python sqlite3):
python3 -c "import sqlite3;[print(r) for r in sqlite3.connect('asset-forge/intelligence.db').execute('SELECT business,priority,status FROM v_pack_candidates LIMIT 15')]"
```
