# CLAUDE CODE PROJECT BRIEF — "ASSET-FORGE"
### SME Digital Asset Intelligence → Productisation Pipeline
**Owner:** Samuel Vyhnanek · **Context:** EU (Ireland) seller · **Date:** DD/MM/YYYY

> 🎯 **PRIORITY VERTICAL: HOSPITALITY** (bars · restaurants · B&B). Research all four verticals for the intelligence base, but when ranking the product roadmap (Phase 7) and building flagships (Phase 9), **ship a hospitality product first.** Other verticals are catalogued now, productised later.

---

## [0] HOW TO USE THIS BRIEF

You are running a multi-session research-and-build project. **Do not attempt the whole thing in one session.** Read `handover.md`, do exactly ONE phase, update `handover.md`, then stop and tell me to open a fresh session. Section [9] is your session map.

If any single session looks like it will exceed ~15 tool calls, say so up front and propose splitting it further.

---

## [1] MISSION & END STATE (anchor — do not drift)

**Mission:** Discover, classify and package the digital assets (spreadsheets, trackers, log books, diaries, checklists, quote/invoice tools, dashboards) that real SMEs in **hospitality, manufacturing (food + non-food) and trades** actually need — separating MUST-HAVE from NICE-TO-HAVE — then turn the highest-value ones into sellable digital products on the cheapest EU-VAT-compliant platform.

**Visible end state (definition of done for the whole project):**
1. `intelligence.db` (SQLite) — a queryable catalogue of every business type, department, workflow, digital asset, MUST/NICE tier, score and pain point, with evidence sources.
2. `MASTER_INTELLIGENCE_REPORT.md` — human-readable synthesis.
3. `asset_catalogue.xlsx` — flat export of the full asset map for skimming.
4. `PRODUCT_ROADMAP.md` — prioritised list of products to build, each with a one-page build spec.
5. `MONETIZATION_BRIEF.md` — chosen sales platform + pricing + bundle architecture + launch checklist.
6. `/products/` — 1–2 fully built flagship spreadsheets as proof-of-concept.

---

## [2] YOUR ROLE

Act as a **business operations analyst + product strategist + data engineer**. You understand Lean Six Sigma, management accounting, food safety/HACCP, hospitality operations and trades workflows. You are sceptical: an asset only earns "MUST-HAVE" if you can evidence *why*. You prefer free/open tooling and the lowest running cost that does not compromise quality.

---

## [3] OPERATING CONSTRAINTS (non-negotiable)

**Cost & models**
- Use the cheapest tier that fits the job: reading/running → cheapest model; writing code → mid tier; architecture/planning → top tier only.
- For **bulk classification** (scoring hundreds of asset×business-type rows), do NOT burn premium tokens. Generate the rows, then route the scoring pass through a **free OpenRouter model** via a script (`scripts/classify.py`). Premium model only spot-checks 10% for quality.
- Use `web_search` deliberately, not reflexively. Batch related lookups. Prefer one good source over five mediocre ones.
- Never use Explore-style subagents here. Use Glob/Grep/direct file reads.

**Currency of facts**
- Platform fees, VAT rules and SaaS prices change. **Always verify these live via web search** — never state them from memory.

**EU context (apply throughout)**
- Metric units (kg, minutes, units/min). EU dates (DD/MM/YYYY). Comma separators above 999 (1,067,558).
- Seller is in Ireland → EU VAT on digital goods is in scope. Flag it; do not ignore it.

**Session discipline**
- `handover.md` is the single source of truth between sessions. Every session ends by updating it.

---

## [4] PROJECT STRUCTURE (create in Phase 0)

```
asset-forge/
├── handover.md                  # state, last action, next action, open questions
├── AGENTS.md                    # this brief, condensed to the rules an agent must obey
├── intelligence.db              # SQLite master DB
├── /research/
│   ├── hospitality.md
│   ├── manufacturing_food.md
│   ├── manufacturing_nonfood.md
│   └── trades.md
├── /scripts/
│   ├── init_db.py
│   ├── classify.py              # OpenRouter free-model scoring pass
│   └── export_catalogue.py      # DB → asset_catalogue.xlsx
├── /deliverables/
│   ├── MASTER_INTELLIGENCE_REPORT.md
│   ├── asset_catalogue.xlsx
│   ├── PRODUCT_ROADMAP.md
│   └── MONETIZATION_BRIEF.md
└── /products/                   # built flagship spreadsheets
```

---

## [5] THE RESEARCH TAXONOMY (the analytical spine)

Map everything to this hierarchy. Consistency here is what makes the DB useful.

**Vertical → Business type → Department → Workflow → Digital asset → Tier → Pain point**

**Verticals & business types**

| Vertical | Business types to cover |
|---|---|
| Hospitality | Bar/pub · Café/coffee shop · Restaurant · B&B/guesthouse · Hotel |
| Food manufacturing | Bakery · Butchery/meat · Dairy · Beverage · Ready meals/catering production |
| Non-food manufacturing | Metal/engineering · Plastics/injection · Packaging/print · Joinery/furniture · Light electronics |
| Trades | Electrician · Plumber/heating · Carpenter/joiner · Painter/decorator · Tiler · Landscaper/groundworks |

**Trades work-context modifiers (tag every trades asset with these):** solo vs team · on-site vs workshop/off-site vs on-the-road (van/mobile).

**BUYER dimension (tag every asset):** `operator` (owner/staff running the business) vs `auditor` (the professional inspecting/certifying it) vs `consultant` (helps a business get audit-ready). The same premise generates demand from both sides of the audit — capture both.

**Department spine (common backbone — score relevance per business type):**
Operations/Production · Quality & Compliance (HACCP, H&S, certifications) · HR & People (rostering, onboarding, training, contracts) · Finance & Management Accounting (cashflow, P&L, costing, payroll) · Sales/Marketing/CRM · Procurement & Inventory · Maintenance & Asset Management · Front-of-house/Bookings/Customer · Job & Schedule Management (esp. trades) · Reporting/KPIs/Dashboards.

**Digital asset types:** Spreadsheet tracker · Calculator · Dashboard · Form/checklist template · SOP template · Log book · Diary/planner · Quote generator · Invoice template · Roster/scheduler · Database.

---

## [6] CLASSIFICATION RUBRIC (MUST vs NICE — make it defensible)

Score every **asset × business-type** pairing on four axes, 0–3 each:

| Axis | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **Legal/Regulatory** | none | advisory | expected | legally mandatory |
| **Revenue/Cash impact** | none | minor | material | survival-critical |
| **Pain severity** (hurts without it) | none | mild | real | severe |
| **Frequency of use** | rare | monthly | weekly | daily |

**Weighted score** = (Legal ×3) + (Revenue ×2) + (Pain ×2) + (Frequency ×1) → max **24**.

**Tiers:**
- **MUST** — score ≥ 16 **OR** Legal = 3 (anything legally mandated is automatically a MUST).
- **SHOULD** — 10–15 (the "wanted, sells well" zone).
- **COULD** — 5–9 (nice extras / bundle filler).
- **WON'T** — < 5 (exclude).

"Good to have, not needed but wanted" = **SHOULD + COULD**. These are often where willingness-to-pay is highest because they're desired, not dreaded — capture them carefully.

Store the raw axis scores in the DB, not just the tier, so we can re-cut later.

---

## [7] RESEARCH METHODOLOGY & SOURCES

For each business type, answer in `/research/<vertical>.md`:
1. What departments/functions exist, even informally? (A solo plumber still "does HR" and "does finance.")
2. For each department, what recurring workflows produce or consume records?
3. What digital asset would serve each workflow? Score it (Section 6).
4. What are the **top pain points** — what do owners hate, redo, or lose money on?
5. What existing SaaS/tools already serve this, and what do users complain about? (Capterra/G2 reviews, "switching away from X" threads.)

**Source priorities (cheap, high-signal):**
- Regulatory/official: food safety authorities, H&S authority, trade licensing bodies → defines the MUST floor.
- Owner-voice: trade subreddits, industry Facebook groups, forums (e.g. tradesperson forums, restaurant owner communities), "I built this in Excel" posts.
- Competitor gap analysis: review sites for niche SaaS (job management, EPOS, HACCP apps) — the complaints ARE the product brief.
- Template marketplaces (Etsy, Gumroad, Notion, Template.net) — what already sells tells you demand + price points.

Cite the source for any MUST/SHOULD classification in the DB `evidence` field.

---

## [8] DATA MODEL (`scripts/init_db.py`)

Normalised SQLite. Suggested tables:

- `verticals` (id, name)
- `business_types` (id, vertical_id, name, work_context)
- `departments` (id, name)
- `workflows` (id, department_id, name, description)
- `digital_assets` (id, name, asset_type, description)
- `asset_map` (id, business_type_id, department_id, asset_id, legal, revenue, pain, frequency, score, tier, evidence_url, notes)
- `pain_points` (id, business_type_id, description, severity, source_url)
- `existing_solutions` (id, name, category, price_eur, key_gaps, source_url)
- `products` (id, name, target_business_type, bundled_asset_ids, price_eur, platform)

Add helper views: `v_must_haves`, `v_universal_core` (assets that are MUST across ≥3 business types — these are your highest-leverage products).

---

## [9] SESSION PLAN (one phase per session)

| # | Session | One deliverable | Model tier |
|---|---|---|---|
| 0 | **Setup** | Folder tree, `init_db.py`, empty DB, `AGENTS.md`, `handover.md`, taxonomy + rubric locked in | planning |
| 1 | **Hospitality research** | `research/hospitality.md` + rows inserted for bar, café, restaurant, B&B, hotel | mid |
| 2 | **Food manufacturing research** | `research/manufacturing_food.md` + rows | mid |
| 3 | **Non-food manufacturing research** | `research/manufacturing_nonfood.md` + rows | mid |
| 4 | **Trades research** | `research/trades.md` + rows (tag solo/team, on/off-site/road) | mid |
| 5 | **Classification pass** | Run `classify.py` via OpenRouter free model; spot-check 10%; tiers finalised | cheap + spot-check |
| 6 | **Synthesis** | `MASTER_INTELLIGENCE_REPORT.md` + `asset_catalogue.xlsx`; identify universal core vs niche-specific | mid |
| 7 | **Productisation** | `PRODUCT_ROADMAP.md` — rank products by (demand × price × build-ease); one-page build spec each | planning |
| 8 | **Monetization** | `MONETIZATION_BRIEF.md` — platform decision (EU VAT!), pricing, bundles, launch checklist | mid |
| 9 | **Build flagships** | 1–2 top **hospitality** products built in `/products/` as proof | code |
| 10 | **🎁 Standards & audit research** (BONUS) | `research/compliance.md` + standards/clauses/compliance-assets rows (see [15]) | mid |
| 11 | **🎁 Audit & compliance productisation** (BONUS) | Auditor toolkits + auditee compliance packs added to `PRODUCT_ROADMAP.md` | planning |
| 12 | **🎁 Build a flagship compliance pack** (BONUS) | One audit-ready pack built in `/products/` | code |

After each session: update `handover.md` with ✅ done / ▶️ next / ❓ open questions, and award yourself a checkpoint score (assets mapped this session, % project complete).

---

## [10] PRODUCTISATION SPEC (Phase 7 output shape)

For each candidate product, produce a one-pager:
- **Name + target** (e.g. "Bar Stock & Wastage Tracker — for independent pubs")
- **Bundled assets** (asset IDs from DB)
- **Tier mix** (MUST anchor + SHOULD/COULD upsells)
- **Pain it kills** (quote the owner-voice evidence)
- **Build complexity** (S/M/L) and **estimated build time**
- **Suggested price (€)** benchmarked against marketplace comparables
- **Bundle path** (standalone → vertical bundle → "everything" kit)

Prioritise products that sit on a **universal-core** asset (sells across multiple business types = build once, sell many). **Within that, rank hospitality products to the top of the roadmap** — the first shippable product must be a bar/restaurant/B&B asset.

---

## [11] MONETIZATION RESEARCH BRIEF (Phase 8)

Compare digital-product platforms in a weighted table. **Verify all fees and VAT handling live.** Score on:
- ✅/❌ **Merchant-of-Record / handles EU VAT for the seller** (heavily weighted — seller is in Ireland)
- Transaction fee % and any fixed/monthly cost
- Free tier viability
- Payout method/speed to an EU/Irish bank
- File hosting, licensing, update delivery to buyers
- Ease of running with **0 employees** (automation-friendly)

Candidates to evaluate (not exhaustive): Gumroad, Payhip, Lemon Squeezy, Sellfy, Ko-fi, Etsy (templates), Notion-based selling. Pick ONE primary winner and one fallback, and state why. Then: pricing strategy, bundle architecture, and a launch checklist (listing copy, preview images, licence text, refund policy).

---

## [12] QUALITY GATES & VERIFICATION

Before marking any session done:
- Every MUST/SHOULD row has an `evidence_url`. No evidence → downgrade or flag.
- No duplicate assets under different names (dedupe by function, not label).
- Legal-mandatory items are tier MUST regardless of score (sanity-check this query each session).
- Numbers formatted EU-style; units metric.
- Run `export_catalogue.py` and eyeball the xlsx for gaps/null tiers.

---

## [13] HANDOVER PROTOCOL (`handover.md` template)

```
## STATE — <DD/MM/YYYY HH:MM>
Project: ASSET-FORGE
Phase last completed: <n - name>
Checkpoint score: <assets mapped this session> | <% complete>

### ✅ DONE THIS SESSION
- ...

### ▶️ NEXT SMALLEST ACTION
- <exact first command/task for next session>

### ❓ OPEN QUESTIONS / DECISIONS NEEDED FROM SAMUEL
- ...

### ⚠️ RISKS / WATCHOUTS
- ...
```

---

## [14] FIRST ACTION (do this now, then stop)

Run **Phase 0 only**: create the folder tree, write `AGENTS.md` (condense Sections [1]–[3] + [6] into agent rules), build `scripts/init_db.py`, initialise `intelligence.db` with the schema in [8], seed `handover.md`. Then report the checkpoint and tell me to open a fresh session for Phase 1.

Do not start research in this session.

---

## [15] 🎁 EXTENSION PACK — COMPLIANCE & AUDIT (BONUS TRACK, Phases 10–12)

**Run only after the core hospitality product has shipped.** This track turns the catalogue into a second revenue line serving compliance buyers, who pay more because failure = lost certification or licence.

> **Framing accuracy (do not get this wrong in listings):** TÜV (SÜD / Rheinland / NORD) is a *certification body*, not a standard. It audits businesses *against* standards such as ISO. So products are positioned as **"audit-ready packs that satisfy a TÜV-style certifier auditing you to ISO 9001 / 22000 / BRCGS"**, never "TÜV templates."

### 15.1 Standards to map (verify current versions/numbers live)

| Family | Standards / schemes |
|---|---|
| Management systems (ISO) | ISO 9001 (quality) · ISO 14001 (environment) · ISO 45001 (occupational H&S) · ISO 22000 (food safety) · ISO 27001 (info-sec, niche) · ISO 50001 (energy, niche) |
| Food sector | HACCP (Codex principles) · BRCGS Food Safety · IFS Food · FSSC 22000 · SALSA (small producers) · GMP/GHP |
| EU legal floor | Reg. 852/2004 (food hygiene) · Reg. 1169/2011 (allergens/FIC) · fire & H&S statutory duties |
| Trades / construction | ISO 9001 + 45001 · Safe-T-Cert / CIRI (IE) · CHAS / SafeContractor / Constructionline (UK) · Safe Electric / RGI (IE) · NICEIC / Gas Safe (UK) |
| Hospitality | HACCP + 852/2004 + allergens · Fáilte Ireland accommodation standards |

Map each standard → the **business types** it applies to → the **assets** needed to satisfy it. A standard mandated by law auto-promotes its assets to MUST (rubric [6], Legal = 3).

### 15.2 Auditor / consultant assets (BUYER = auditor/consultant)
Audit checklist/protocol per standard · audit scoring & grading sheet · non-conformance (NC) register · CAPA tracker · audit-schedule planner (surveillance + recertification cycles) · objective-evidence register · audit-report generator · auditor competency log · findings dashboard.

### 15.3 Auditee / compliance assets (BUYER = operator)
Clause-by-clause **gap-analysis tool** (current state vs standard) · document-control register / master document list · internal-audit programme & log · management-review template + minutes log · corrective-action log · training matrix / competency records · supplier-approval register · calibration log · traceability log (food) · HACCP plan template + CCP monitoring logs + PRP checklists · **mock-audit / readiness self-assessment** (high willingness-to-pay — it answers "will I pass?").

### 15.4 Data-model additions
- `standards` (id, name, family, scope, certifying_bodies, current_version, source_url)
- `compliance_assets` (id, name, asset_type, buyer_role[auditor/operator/consultant], standard_ids, business_type_ids, tier, notes)
- extend `products` with `audience` (operator / auditor / consultant) and `standard_ids`.
- view `v_audit_packs` = compliance_assets grouped by standard → instant bundle definitions.

### 15.5 Productisation logic
- **Per-standard bundles** sell best: "ISO 22000 Internal Audit Kit", "HACCP Readiness Pack for Cafés", "BRCGS Document-Control Suite."
- The **gap-analysis tool + mock-audit self-assessment** is the flagship — build that first in Phase 12. It is the cheapest to build, the easiest to demo, and the clearest pain-killer.
- Tier the offer: free gap-analysis lite (lead magnet) → paid standard-specific kit → full audit suite (auditor edition).

> **Reuse value:** these compliance assets are the same artefacts a HACCP/ISO consultancy bills for. Build once; they double as productised IP and as delivery tooling for advisory work.

