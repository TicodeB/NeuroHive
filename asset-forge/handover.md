## STATE — 29/05/2026 22:10
Project: ASSET-FORGE
Phase last completed: 3 - Non-food manufacturing research
Checkpoint score: 122 asset-map rows mapped this session (10 new assets, 16 pain points) | ~31% complete (4 of 13 sessions)

### ✅ DONE THIS SESSION
- Wrote `research/manufacturing_nonfood.md` — 5 research questions answered for Metal/engineering, Plastics/injection, Packaging/print, Joinery/furniture, Light electronics (business_type ids 11–15), plus a regulatory MUST-floor table.
- Verified the non-food legal floor LIVE (entirely different from food — no FSAI): **CE marking** (manufacturer conformity assessment, technical file kept 10 yrs, EU Declaration of Conformity; Machinery / LVD / EMC / RoHS); **S.I. 299/2007 General Application Regs** (work-equipment inspection, guarding, control devices) + **Chemical Agents Regs 2001** / REACH (SDS, hardwood dust = carcinogen, solvents/inks); HSA Safety Statement + fire; **EPR** (Repak packaging — major producer ≥ €1,000,000 turnover **and** ≥ 10 t; WEEE + RoHS for electronics). Sources: EC single-market, Your Europe, HSA, Repak (cited in research doc + DB `evidence_url`). Also pulled commercial/owner-voice evidence (machine-shop quoting/QC software + Practical Machinist forum) for non-regulatory MUST/SHOULD rows.
- Wrote `scripts/seed_manufacturing_nonfood.py` (idempotent on bt 11–15; computes score+tier; refuses MUST/SHOULD rows without evidence_url; reuses existing assets by name without clobbering them).
- Inserted into `intelligence.db`: **10 new `digital_assets`** (total 46), **122 `asset_map`** rows for bt 11–15 (raw axis scores + buyer tag + evidence_url), 16 `pain_points` (total 50).
- Phase-3 tier split: **22 MUST · 65 SHOULD · 35 COULD** (note: non-food has a *narrower legal floor* than food → fewer auto-MUSTs, a much larger "wanted, sells well" SHOULD zone — exactly the high-willingness-to-pay band).
- Buyer dimension captured (119 operator, 1 auditor, 2 consultant).
- `v_universal_core` now spans all three verticals: **H&S + Fire = MUST across all 15** business types; **Work-Equipment Safety/Guarding Register** MUST across all 5 non-food; manufacturing ops-core (Batch/Yield, BOM costing, Calibration, Supplier Approval, OEE, PPM, Cashflow, B2B invoice) confirmed as broadest build-once/sell-many base.
- Deduped by FUNCTION: reused 14 existing assets, added only 10 genuinely-new non-food functions.
- All Phase 3 quality gates [12] passed: 0 MUST/SHOULD missing evidence; 0 legal=3 rows off-MUST; 0 score mismatches; 0 null tiers.

### ▶️ NEXT SMALLEST ACTION
- Open a FRESH session for **Phase 4 — Trades research** (mid model tier).
- Produce `research/trades.md` answering the 5 questions in [7] for: Electrician, Plumber/heating, Carpenter/joiner, Painter/decorator, Tiler, Landscaper/groundworks (business_type ids 16–21).
- **Trades-specific requirement (Section [5]):** tag every trades asset with the **work-context modifier** — solo vs team · on-site vs workshop/off-site vs on-the-road (van/mobile). Store it (e.g. in `asset_map.notes` and/or `business_types.work_context`).
- Mirror the Phase 1–3 pattern: write `scripts/seed_trades.py`, insert NEW `digital_assets` + scored `asset_map` rows (+ buyer tag + evidence_url + work-context) + `pain_points` for bt 16–21. Reuse existing assets where the function recurs (Job Quotation & Estimating, Production Job Card/WIP, Cashflow, B2B invoice, Supplier Approval, Training, H&S, Fire, Calibration, Chemical Agents/SDS). NOTE: trades legal floor = sector licensing/registration — **Safe Electric / RECI (electrical), RGI/Gas (gas), Safe Pass / CSCS, Building Control (BCAR), CIRI** — verify live. Expect a Quote→Job→Invoice→Compliance-Cert spine.

### ➕ STANDING ADD-ONS (carry forward)
- **Bilingual EN+SK** binding rule (AGENTS.md). `deliverables/asset_glossary_EN_SK.md` covers the 20 hospitality assets; the **26 new food + non-food assets (ids 21–46) still need SK names/microcopy** — backfill in synthesis/Phase 6 or before launch; route through a native editor. `/slovak` chief-editor skill NOT installed here.
- **Market validation**: `research/market_validation.md`. Preliminary platform pick: **Lemon Squeezy** primary / **Gumroad** fallback / **Etsy** discovery (EU-VAT weighted; final lock Phase 8 with fees re-verified live).
- **Secrets plumbing** ready: root `.gitignore` excludes `.env`; `asset-forge/.env.example`; `scripts/set_secret.sh`. Preferred: set `OPENROUTER_API_KEY` as a Claude Code environment secret.
- **Research tooling available** (per Samuel): Tavily MCP (search/extract/research), Semantic Scholar paper search, and Consensus (needs auth handshake) — use alongside free WebSearch/WebFetch for Phase 4+ live verification.

### ❓ OPEN QUESTIONS / DECISIONS NEEDED FROM SAMUEL
- `OPENROUTER_API_KEY` + free model name still needed before Phase 5 — provide via env secret or `scripts/set_secret.sh` (NOT in chat).
- **Excise/duty (alcoholic beverage)** folded into Cashflow/P&L in Phase 2 — confirm dedicated excise tracker (Phase 8/10) vs keep in cashflow.
- Confirm `asset-forge/` living inside the `NeuroHive` repo is intended.
- All Phase 2–3 work is on branch `claude/bold-noether-TutEY` → **draft PR #3** (now carries Phases 2 + 3).

### ⚠️ RISKS / WATCHOUTS
- Do NOT state platform fees / VAT / SaaS prices / licensing-body rules from memory — verify live (Phases 4, 8, 11).
- Dedupe assets by FUNCTION, not label — Phase 4 should reuse the 46 existing assets where they recur, not re-create them.
- Legal-mandatory (Legal=3) auto-promotes to MUST — sanity-check each session (Phases 1–3: passed).
- One phase per session; if a phase looks like >~15 tool calls, propose splitting.
- `scripts/classify.py` exists (Phase 5 runner); `scripts/export_catalogue.py` still NOT written (built in Phase 6).
- No `sqlite3` CLI in this environment — use Python (`sqlite3` module) for DB inspection.
- 26 new food + non-food assets are EN-only — Slovak glossary backfill outstanding.
</content>
