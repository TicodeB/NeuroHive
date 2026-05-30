# Phase 5 — Classification validation pass

**Date:** 30/05/2026
**Scope:** all 442 `asset_map` rows across 21 business types and 54 digital assets.

## What Phase 5 is

The brief's Phase 5 is the cheap "validation / second-opinion" pass on the
rubric scores already laid down in Phases 1–4 — not a from-scratch re-score
(see [`handover.md`](../handover.md), Phase 4 note). It has two halves:

1. **Deterministic pass** — `scripts/validate.py`: algebraic re-derivation of
   every row's score and tier from its raw axes, plus every Section [12]
   quality gate (legal=3 → MUST, MUST/SHOULD evidence required, buyer dim
   tagged, trades work-context tagged, no duplicate asset functions, no null
   tiers, axes in 0–3).
2. **Model pass** — `scripts/classify.py`: an independent re-score routed
   through the **free** OpenRouter model `deepseek/deepseek-chat-v3-0324:free`,
   landing divergences in `classification_audit` for human review. Free model
   so we don't burn premium tokens on bulk scoring (brief [3]).

The two halves are complementary: the deterministic pass catches *data
integrity* breaks (the rubric must always equal itself); the model pass
catches *judgement* drift (does an independent reader see the same tier?).

## Result — deterministic pass

```
asset_map rows scanned : 442
issues raised          : 0
All [12] quality gates PASS — no anomalies.
```

- Score recompute (`3L + 2R + 2P + F`) matches stored score on **all 442 rows**.
- Tier recompute (rubric [6]) matches stored tier on **all 442 rows**.
- All **115 legal=3 rows are tier MUST** (Legal-mandatory auto-promotion holds).
- All **347 MUST/SHOULD rows carry an `evidence_url`** (no naked claims).
- All **442 rows have a buyer tag** in {operator, auditor, consultant}.
- All **100 trades rows carry the Section [5] work-context modifier** on the
  parent `business_types.work_context` (solo/team · on-site/workshop/road).
- No duplicate `digital_assets` rows (dedupe-by-function gate from [12]).

The deterministic pass IS the only authority on rubric arithmetic. With it
green, the 442 rows are **arithmetically clean and tier-final** modulo the
judgement second-opinion below.

## Result — model pass (BLOCKED for this session)

`scripts/classify.py --dry-run` reports the wiring is correct and the API
key loads. The live call returns:

```
auth/key HTTPError 403 Host not in allowlist
```

The provided `OPENROUTER_API_KEY` carries an **IP / host allowlist** that
excludes this remote runner's egress IP. No tokens were spent. The script is
unchanged and ready to run from any host on the allowlist:

```bash
# from a whitelisted host (or after widening the key's allowlist on OpenRouter):
python3 asset-forge/scripts/classify.py            # 10% sample (44 rows)
python3 asset-forge/scripts/classify.py --all      # full pass (442 rows)
```

Divergences will land in `classification_audit` for review. Per the brief,
the model pass NEVER overwrites curated scores — it only flags judgement
disagreements for a human spot-check.

## Summary stats from the audited DB

### Tier distribution (overall)

| Tier   | Rows | Share |
|--------|-----:|------:|
| MUST   | 129  | 29.2% |
| SHOULD | 218  | 49.3% |
| COULD  |  95  | 21.5% |
| WON'T  |   0  |  0.0% |

The "wanted, sells well" SHOULD band is the largest single tier (218 / 442 =
49%) — the brief's [6] willingness-to-pay zone. MUST sits at 29%; COULD at
22% gives meaningful bundle filler.

### Tier × vertical

| Vertical                | MUST | SHOULD | COULD |
|-------------------------|-----:|-------:|------:|
| Hospitality             |  37  |   31   |   22  |
| Food manufacturing      |  48  |   62   |   20  |
| Non-food manufacturing  |  22  |   65   |   35  |
| Trades                  |  22  |   60   |   18  |

Hospitality is the densest MUST-fraction (41% MUST) — confirms the brief's
priority-vertical choice (ship hospitality first). Trades and non-food
manufacturing are SHOULD-heavy: that is the highest willingness-to-pay band
per [6], and aligns with Phase 4's owner-voice finding (Quote→Job→Invoice
spine is *wanted*, not legally forced).

### Buyer dimension

| Buyer       | Rows |
|-------------|-----:|
| operator    | 428  |
| consultant  |   8  |
| auditor     |   6  |

Operator dominates today, by design — auditor/consultant assets are the
Phase 10–12 bonus track ([15]); the 14 rows already captured are seeds
(Safe Electric/RGI inspectors, H&S consultants, accountants).

### Universal-core assets (MUST across ≥3 business types)

The build-once/sell-many shortlist `v_universal_core` returns 12 assets,
topped by:

| Asset                                            | MUST in N business types |
|--------------------------------------------------|-------------------------:|
| H&S Risk Assessment & Safety Statement           | **21** (all of them) |
| Fire Safety Register & Checks Log                | 17 |
| HACCP Food Safety Management System              | 10 |
| Cleaning & Sanitation Schedule                   | 10 |
| Supplier & Delivery Traceability Log             | 10 |
| Allergen Matrix & Menu Declaration Tool          | 8 |
| Temperature Monitoring Log                       | 8 |
| Work Equipment & Machinery Safety/Guarding Reg.  | 7 |
| Product Label & Nutrition Declaration Generator  | 5 |
| Chemical Agents (SDS) Register & Risk Assessment | 5 |
| RCT & Subcontractor Payment Tracker              | 4 |
| Batch Production & Yield Record                  | 3 |

The H&S Safety Statement asset (MUST in 21/21 business types) is the single
broadest leverage product in the catalogue — Phase 7 should rank a
hospitality-flavoured H&S pack near the top of the roadmap regardless of
vertical priority.

## What's locked at end of Phase 5

- Tier finalisation: **442 / 442 rows tier-final** (the rubric is internally
  consistent and every gate passes). Re-cut later by reading the raw
  `legal/revenue/pain/frequency` columns.
- `validation_audit` table created and (correctly) empty.
- `classification_audit` table created by `classify.py` schema; rows pending
  the model pass.

## Next

- Run `classify.py` from a host whose IP is on the OPENROUTER_API_KEY
  allowlist (or widen the allowlist on OpenRouter). Review divergences and
  re-cut any rows where the model + a human reviewer disagree with stored
  tiers (write-back is a manual decision, never automatic).
- Then advance to **Phase 6 — Synthesis** (`MASTER_INTELLIGENCE_REPORT.md`
  + `asset_catalogue.xlsx`).
