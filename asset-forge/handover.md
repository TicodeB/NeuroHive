## STATE — 30/05/2026 11:40
Project: ASSET-FORGE
Phase last completed: 4 - Trades research
Checkpoint score: 100 asset-map rows mapped this session (8 new assets, 17 pain points) | ~38% complete (5 of 13 sessions)

### ✅ DONE THIS SESSION
- Wrote `research/trades.md` — 5 research questions answered for Electrician, Plumber/heating, Carpenter/joiner, Painter/decorator, Tiler, Landscaper/groundworks (business_type ids 16–21), plus a LIVE-verified regulatory MUST-floor table and a cross-trade synthesis.
- Verified the trades legal floor LIVE (sector licensing/registration, NOT a single regulator): **Safe Electric / RECI** completion certificate mandatory per electrical job; **RGI** gas Declaration of Conformance / Completion Cert mandatory for all "Gas Work" (2006 Act, I.S. 813); **CIRI** moving voluntary→**statutory/mandatory** (Reg. of Providers of Building Works Act 2022, 2026 rollout); **BC(A)R 2014/BCAR** ancillary completion certs; **Safe Pass** (SOLAS) mandatory for all site workers + **CSCS** for high-risk plant; **SHWW Act 2005 + Construction Regs 2013** Safety Statement/RAMS; **Chemical Agents Regs 2001** (painter VOC, carpenter hardwood-dust carcinogen, tiler adhesives); **Sustainable Use of Pesticides S.I. 155/2012** (landscaper professional-user records); **RCT + VAT reverse charge** on construction (Revenue). Sources cited in research doc + DB `evidence_url`. Owner-voice/SaaS-gap evidence from Tradify/ServiceM8/VioTrade/Linktly (Quote→Job→Invoice spine; cert/RCT/calibration/take-off unserved by generic tools).
- Wrote `scripts/seed_trades.py` (idempotent on bt 16–21; computes score+tier; refuses MUST/SHOULD rows without evidence_url; reuses existing assets by name without clobbering; sets `business_types.work_context`).
- **Set work-context modifier (Section [5])** on all six trades in `business_types.work_context` AND echoed per-row in `asset_map.notes` (solo/team · on-site/workshop-off-site/on-the-road).
- Inserted into `intelligence.db`: **8 new `digital_assets`** (total 54), **100 `asset_map`** rows for bt 16–21 (raw axis scores + buyer tag + evidence_url + work-context), **17 `pain_points`** (total 67).
- Phase-4 tier split: **22 MUST · 60 SHOULD · 18 COULD** — confirms the trades thesis: *narrow* legal MUST floor (completion certs, Safety Statement, painter/landscaper chemical/pesticide SDS, carpenter workshop fire/guarding) and a *large* SHOULD "wanted, sells well" zone (quoting, job card, scheduling, invoicing/getting-paid, take-off, snag, CRM) = highest willingness-to-pay band.
- Buyer dimension captured (95 operator, 2 auditor [Safe Electric/RGI inspectors], 3 consultant [H&S/accountant]).
- `v_universal_core` now shows **H&S Safety Statement = MUST across all 21** business types (the single broadest build-once/sell-many asset); **RCT & Subcontractor Payment Tracker = MUST across 4** trades; Work-Equipment Safety/Guarding MUST across 7.
- New trades assets (deduped by FUNCTION): Trade Completion & Compliance Certificate Register · Job Schedule/Dispatch & Site Diary · Materials Take-off & Quantity Calculator · RCT & Subcontractor Payment Tracker · Method Statement & RAMS Builder · Cert/Card/Insurance Expiry Tracker · Snag List & Job Sign-off · Customer Enquiry & Job Pipeline CRM. Reused 11 existing assets (Quote, Job Card/WIP, Cashflow, B2B invoice, Safety Statement, Fire, Training, Calibration, Chemical Agents/SDS, PPM, Equipment Guarding).
- All Phase 4 quality gates [12] passed: 0 MUST/SHOULD missing evidence; 0 legal=3 rows off-MUST; 0 score mismatches; 0 null tiers; 0 duplicate asset names.

### ▶️ NEXT SMALLEST ACTION
- **Research phase is COMPLETE (all 4 verticals, 21 business types mapped).** Open a FRESH session for **Phase 5 — Classification pass** (cheap model + 10% spot-check).
- Provide `OPENROUTER_API_KEY` + a free model name FIRST (env secret or `scripts/set_secret.sh`, NOT in chat) — `scripts/classify.py` already exists and reads env then `.env`.
- Phase 5 task: route the full `asset_map` (442 rows) scoring pass through the free OpenRouter model via `classify.py`, premium-spot-check ~10% (44 rows) for quality, finalise tiers, re-run the [12] quality-gate queries. NOTE: rows already carry deterministic rubric scores+tiers from Phases 1–4 — Phase 5 is a *validation/second-opinion* pass to catch mis-scores, not a from-scratch scoring.

### ➕ STANDING ADD-ONS (carry forward)
- **Bilingual EN+SK** binding rule (AGENTS.md). `deliverables/asset_glossary_EN_SK.md` covers the 20 hospitality assets; the **34 new food + non-food + trades assets (ids 21–54) still need SK names/microcopy** — backfill in synthesis/Phase 6 or before launch; route through a native editor. `/slovak` chief-editor skill NOT installed here.
- **Market validation**: `research/market_validation.md`. Preliminary platform pick: **Lemon Squeezy** primary / **Gumroad** fallback / **Etsy** discovery (EU-VAT weighted; final lock Phase 8 with fees re-verified live).
- **Secrets plumbing** ready: root `.gitignore` excludes `.env`; `asset-forge/.env.example`; `scripts/set_secret.sh`. Preferred: set `OPENROUTER_API_KEY` as a Claude Code environment secret.
- **Research tooling available** (per Samuel): Tavily MCP (search/extract/research), Semantic Scholar paper search, Consensus (needs auth handshake) — used Tavily for Phase 4 live verification; available for Phase 8/11.

### ❓ OPEN QUESTIONS / DECISIONS NEEDED FROM SAMUEL
- `OPENROUTER_API_KEY` + free model name needed before Phase 5 — provide via env secret or `scripts/set_secret.sh` (NOT in chat).
- **Excise/duty (alcoholic beverage)** folded into Cashflow/P&L in Phase 2 — confirm dedicated excise tracker (Phase 8/10) vs keep in cashflow.
- Confirm `asset-forge/` living inside the `NeuroHive` repo is intended.
- Phase 4 work is on branch `claude/beautiful-knuth-cHRjU` → new draft PR (Phase 4). Phases 2+3 were on `claude/bold-noether-TutEY` (draft PR #3). Confirm whether to keep one branch/PR per phase or consolidate.

### ⚠️ RISKS / WATCHOUTS
- Do NOT state platform fees / VAT / SaaS prices / licensing-body rules from memory — verify live (Phases 8, 11).
- Dedupe assets by FUNCTION, not label — Phase 5+ must reuse the 54 existing assets where they recur.
- Legal-mandatory (Legal=3) auto-promotes to MUST — sanity-check each session (Phases 1–4: passed).
- One phase per session; if a phase looks like >~15 tool calls, propose splitting.
- `scripts/classify.py` exists (Phase 5 runner); `scripts/export_catalogue.py` still NOT written (built in Phase 6).
- No `sqlite3` CLI in this environment — use Python (`sqlite3` module) for DB inspection.
- 34 new food + non-food + trades assets are EN-only — Slovak glossary backfill outstanding.
