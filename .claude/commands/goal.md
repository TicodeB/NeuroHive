---
description: Run one ASSET-FORGE phase with a locked end state and scored checkpoint
argument-hint: [phase number, default 0]
---

# /goal — ASSET-FORGE phase runner

Read `ASSET-FORGE_claude_code_brief.md` in full. It is the project charter — obey it.

**Target phase:** $ARGUMENTS (if empty, default to **Phase 0 — Scaffold**).

## RULES (non-negotiable)
- Execute **ONLY** the target phase. Do not start the next one.
- Cheapest model tier that fits: this is setup/scaffolding work.
- No research, no marketing content, no generated copy in Phase 0.
- If the phase will exceed ~15 tool calls, stop and tell me to split it.

## VISIBLE END STATE — Phase 0 is DONE when ALL exist:
1. Folder tree from Section [4] created.
2. `scripts/init_db.py` written; `intelligence.db` initialised with the Section [8] schema (~10 tables) + views `v_must_haves`, `v_universal_core`.
3. `AGENTS.md` written — Sections [1]–[3] + rubric [6] condensed into agent rules.
4. `handover.md` seeded from the Section [13] template, with ▶️ NEXT = "Phase 1 — Hospitality".
5. Taxonomy [5] + scoring rubric [6] recorded in the repo.
6. Priority vertical = **HOSPITALITY** noted in `handover.md`.

## SELF-VERIFY before declaring done
- Run `sqlite3 intelligence.db ".tables"` → confirm tables present.
- Confirm no null/placeholder files; every file above exists and is non-empty.
- Confirm nothing from Phase 1+ was started.

## REPORT (then STOP)
Output a checkpoint:
- ✅ What was created (file list)
- 📊 Score: tables created / target, % project complete
- ⚠️ Any blockers or decisions needed from Samuel
- ▶️ Exact next action: "Open fresh session, run /goal 1"

Then STOP. Do not continue past the target phase.
