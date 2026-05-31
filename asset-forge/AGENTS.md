# AGENTS.md — ASSET-FORGE operating rules

Condensed from the project brief Sections [1]–[3] and [6]. These are the rules
every session must obey. The full brief is the source of truth; this is the
quick contract.

---

## Mission (Section [1] — do not drift)

Discover, classify and package the **digital assets** (spreadsheets, trackers,
log books, diaries, checklists, quote/invoice tools, dashboards) that real SMEs
in **hospitality, food manufacturing, non-food manufacturing and trades**
actually need — separating **MUST-HAVE from NICE-TO-HAVE** — then turn the
highest-value ones into sellable digital products on the cheapest
**EU-VAT-compliant** platform.

🎯 **Priority vertical: HOSPITALITY** (bars · restaurants · B&B). Research all
four verticals for the intelligence base, but **ship a hospitality product
first** (Phase 7 roadmap ranking + Phase 9 flagship build).

**Definition of done (whole project):**
1. `intelligence.db` — queryable catalogue (business type → department →
   workflow → asset → MUST/NICE tier → score → pain point + evidence).
2. `deliverables/MASTER_INTELLIGENCE_REPORT.md` — human-readable synthesis.
3. `deliverables/asset_catalogue.xlsx` — flat export.
4. `deliverables/PRODUCT_ROADMAP.md` — prioritised products + one-page specs.
5. `deliverables/MONETIZATION_BRIEF.md` — platform + pricing + bundles + launch.
6. `products/` — 1–2 fully built flagship spreadsheets (hospitality first).

## Role (Section [2])

Business operations analyst + product strategist + data engineer. Fluent in
Lean Six Sigma, management accounting, food safety/HACCP, hospitality ops and
trades workflows. **Be sceptical:** an asset earns MUST-HAVE only with
evidenced *why*. Prefer free/open tooling and lowest running cost.

## Operating constraints (Section [3] — non-negotiable)

**Cost & models**
- Cheapest tier that fits: reading/running → cheapest; writing code → mid;
  architecture/planning → top tier only.
- **Bulk classification** (scoring hundreds of asset×business-type rows): do NOT
  burn premium tokens. Generate rows, then route the scoring pass through a
  **free OpenRouter model** via `scripts/classify.py`. Premium model spot-checks
  only ~10% for quality.
- Use `web_search` deliberately, not reflexively. Batch related lookups. One
  good source beats five mediocre ones.
- **Never use Explore-style subagents.** Use Glob/Grep/direct file reads.

**Currency of facts**
- Platform fees, VAT rules, SaaS prices change → **always verify live via web
  search**, never from memory.

**EU context (apply throughout)**
- Metric units (kg, minutes, units/min). EU dates (DD/MM/YYYY). Comma thousands
  separators (1,067,558). Seller is in **Ireland** → EU VAT on digital goods is
  in scope; flag it, never ignore it.

**Session discipline**
- One phase per session. Read `handover.md` first; do exactly ONE phase; update
  `handover.md`; then STOP and tell Samuel to open a fresh session.
- If a session looks like it will exceed ~15 tool calls, say so up front and
  propose splitting further.
- **ALWAYS state the exact git branch Samuel should run the next `/goal` on** —
  both in the chat report AND in the `handover.md` ▶️ NEXT action. Never leave the
  branch implicit (Samuel's standing instruction, 30/05/2026).

## Classification rubric (Section [6] — make it defensible)

Score every **asset × business-type** pairing on four axes, 0–3 each, and store
the **raw axis scores** in `asset_map` (not just the tier) so we can re-cut later.

| Axis | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **Legal/Regulatory** | none | advisory | expected | legally mandatory |
| **Revenue/Cash impact** | none | minor | material | survival-critical |
| **Pain severity** | none | mild | real | severe |
| **Frequency of use** | rare | monthly | weekly | daily |

**Weighted score** = (Legal ×3) + (Revenue ×2) + (Pain ×2) + (Frequency ×1) → **max 24**.

**Tiers:**
- **MUST** — score ≥ 16 **OR** Legal = 3 (anything legally mandated is auto-MUST).
- **SHOULD** — 10–15 ("wanted, sells well").
- **COULD** — 5–9 (nice extras / bundle filler).
- **WON'T** — < 5 (exclude).

"Good to have, not needed but wanted" = **SHOULD + COULD** — often highest
willingness-to-pay (desired, not dreaded). Capture carefully.

## Quality gates (Section [12]) — check before marking a session done
- Every MUST/SHOULD row has an `evidence_url`. No evidence → downgrade or flag.
- No duplicate assets under different names (dedupe by **function**, not label).
- Legal-mandatory items are MUST regardless of score (sanity-check each session).
- Numbers EU-formatted; units metric.
- Run `export_catalogue.py` and eyeball the xlsx for gaps/null tiers.

## Taxonomy spine (Section [5]) — already seeded in `intelligence.db`
Vertical → Business type → Department → Workflow → Digital asset → Tier → Pain point.
Tag every asset with the **BUYER** dimension: `operator` · `auditor` ·
`consultant` (stored in `asset_map.buyer`). Tag every trades asset with work
context: solo/team · on-site/off-site/on-the-road.

## Bilingual rule (EN + SK) — non-negotiable for the CORE catalogue
Every **core-catalogue** asset/product (Phases 0–12: P1, P2, P13…) ships in
**English AND Slovak**. Slovak must be native-quality: correct grammar,
diacritics, punctuation and marketing tone — never machine-literal. Canonical
EN↔SK names + microcopy live in `deliverables/asset_glossary_EN_SK.md`.

> **⚠️ CARVE-OUT — Premium-Pack track (Phase 13+):** Samuel's explicit decision
> (30/05/2026) is **one language per file** (clean SK / CS / DE / HU / PL / EN
> editions), NOT bilingual. The bilingual rule does **not** apply to Premium-Pack
> deliverables — do not re-add EN to a Slovak premium pack. Native-quality
> translation per language still required; route public SK copy through a native
> editor before launch. See `research/beautification_and_competitors.md` §7.

## Market & channel facts (Phase 1 add-on)
Demand is evidenced (`research/market_validation.md`): spreadsheet/template
products demonstrably sell (Etsy/Gumroad/Lemon Squeezy). Preliminary platform
pick (most-pros-wins benchmark, EU-VAT heavily weighted): **Lemon Squeezy**
primary, **Gumroad** fallback, **Etsy** as discovery channel — final lock in
Phase 8 with fees re-verified live.

## Secrets handling — non-negotiable
API keys (e.g. `OPENROUTER_API_KEY`) are **never** committed or printed in chat.
Provide them as environment variables / Claude Code environment secrets
(preferred), or via `scripts/set_secret.sh` (hidden input → git-ignored
`asset-forge/.env`). `.gitignore` excludes `.env`; only `.env.example` (no
values) is committed. Phase 5 `classify.py` reads env first, then `.env`.
