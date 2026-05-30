## STATE — 30/05/2026 14:10
Project: ASSET-FORGE
Phase last completed: 5 - Classification / validation pass (deterministic half ✅, OpenRouter model half BLOCKED on host allowlist)
Checkpoint score: 442 asset_map rows audited · 0 anomalies · 100% Section [12] gates pass | ~46% complete (6 of 13 sessions)

### ✅ DONE THIS SESSION
- Wrote `scripts/validate.py` — the **deterministic half** of Phase 5: re-derives every row's weighted score `3L+2R+2P+F` from raw axes, re-derives tier per rubric [6], and runs every Section [12] quality gate (legal=3→MUST, MUST/SHOULD evidence required, buyer ∈ {operator/auditor/consultant}, trades work-context tag present, no duplicate asset-by-function, no null tiers, axes ∈ 0–3). Persists anomalies to a new `validation_audit` table; never overwrites curated scores.
- Ran it across all **442** `asset_map` rows: **0 issues, all gates PASS**. Catalogue is arithmetically clean and tier-final.
- Confirmed the structural shape: tier mix MUST 129 (29%) · SHOULD 218 (49%) · COULD 95 (22%) · WON'T 0. Hospitality is densest MUST-fraction at 41% (priority-vertical pick stands). Universal-core leader: H&S Safety Statement = MUST across all 21 business types (single broadest build-once/sell-many product).
- Wrote `deliverables/phase5_validation.md` — full validation report (deterministic + summary stats + universal-core shortlist + OpenRouter blocker note + "what's locked" section).
- Attempted the **model half** (`classify.py` → OpenRouter free model `deepseek/deepseek-chat-v3-0324:free`). Dry-run passed; live call returned **HTTP 403 "Host not in allowlist"** on `auth/key`. The provided `OPENROUTER_API_KEY` has an IP/host allowlist that excludes this remote runner's egress IP. No tokens spent. `classify.py` is unchanged and ready to run from a whitelisted host.

### ▶️ NEXT SMALLEST ACTION
- Open a FRESH session for **Phase 6 — Synthesis** on `claude/beautiful-knuth-cHRjU` (or the rolling successor — see ⚠️ branch note below). Phase 6 produces `deliverables/MASTER_INTELLIGENCE_REPORT.md` + `deliverables/asset_catalogue.xlsx` and identifies the universal-core-vs-niche split for the Phase 7 roadmap.
- ⚠️ BRANCH NOTE: this session's commits landed on `claude/eloquent-turing-zX5eA` (the rolling-branch successor per session-specific instructions). Before starting Phase 6, decide rolling-branch policy: continue on this branch, or rebase/merge it onto `claude/beautiful-knuth-cHRjU`. Both branches share the Phase 0→4 history; only the Phase 5 commits diverge.
- **Side-quest (any session, any host on the OpenRouter allowlist):** run `python3 scripts/classify.py` (10% sample) and then `--all` for the full 442-row second opinion. Divergences land in `classification_audit`; review by hand and re-cut only with human decision. Not a Phase 6 prerequisite — the deterministic half already finalises the tiers.

### ➕ STANDING ADD-ONS (carry forward)
- **Bilingual EN+SK** binding rule (AGENTS.md). `deliverables/asset_glossary_EN_SK.md` covers the 20 hospitality assets; the **34 new food + non-food + trades assets (ids 21–54) still need SK names/microcopy** — backfill in Phase 6 synthesis or before launch; route through a native editor. `/slovak` chief-editor skill NOT installed here.
- **Market validation**: `research/market_validation.md`. Preliminary platform pick: **Lemon Squeezy** primary / **Gumroad** fallback / **Etsy** discovery (EU-VAT weighted; final lock Phase 8 with fees re-verified live).
- **Secrets plumbing** ready: root `.gitignore` excludes `.env`; `asset-forge/.env.example`; `scripts/set_secret.sh`. Preferred: set `OPENROUTER_API_KEY` as a Claude Code environment secret with this runner's egress IP on the allowlist (or remove the host restriction on OpenRouter).
- **Research tooling available**: Tavily MCP (search/extract/research), Semantic Scholar paper search, Consensus (auth handshake). Used Tavily for Phase 4 live verification; available for Phase 8/11.

### ❓ OPEN QUESTIONS / DECISIONS NEEDED FROM SAMUEL
- **OpenRouter key host allowlist** — either widen it on openrouter.ai so this remote runner can call it, or run `classify.py` from a whitelisted host. Until then the model half of Phase 5 sits queued. (Deterministic half is already complete and finalises the tiers, so this does not block Phase 6.)
- **Branch policy reconciliation** — session-specific instructions for this remote runner mandated `claude/eloquent-turing-zX5eA`; handover policy mandates the rolling `claude/beautiful-knuth-cHRjU`. Pick one canonical branch for Phase 6+ and either merge/rebase the Phase 5 commits across, or accept the split.
- **Excise/duty (alcoholic beverage)** folded into Cashflow/P&L in Phase 2 — confirm dedicated excise tracker (Phase 8/10) vs keep in cashflow.
- Confirm `asset-forge/` living inside the `NeuroHive` repo is intended.
- ✅ RESOLVED (Samuel, 30/05/2026): single rolling branch policy → `claude/beautiful-knuth-cHRjU` (draft PR #4) is canonical for Phases 0→4. (Phase 5 forked onto `claude/eloquent-turing-zX5eA` per remote-runner instructions — see branch reconciliation above.)

### ⚠️ RISKS / WATCHOUTS
- Do NOT state platform fees / VAT / SaaS prices / licensing-body rules from memory — verify live (Phases 8, 11).
- Dedupe assets by FUNCTION, not label — Phase 6+ must reuse the 54 existing assets where they recur.
- Legal-mandatory (Legal=3) auto-promotes to MUST — sanity-check each session (Phases 1–5: passed).
- One phase per session; if a phase looks like >~15 tool calls, propose splitting.
- `scripts/classify.py` and `scripts/validate.py` exist (Phase 5 runners); `scripts/export_catalogue.py` still NOT written (built in Phase 6).
- No `sqlite3` CLI in this environment — use Python (`sqlite3` module) for DB inspection.
- 34 new food + non-food + trades assets are EN-only — Slovak glossary backfill outstanding.
- Phase 5 model pass is queued, not run — when it lands, review divergences manually before any tier write-back. The script intentionally does NOT auto-overwrite.
