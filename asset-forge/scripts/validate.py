#!/usr/bin/env python3
"""
ASSET-FORGE — Phase 5 deterministic validation pass.

The brief's Phase 5 is a "validation/second-opinion" pass on the 442 asset_map
rows scored in Phases 1-4. Two halves:

  1) MODEL pass (cheap OpenRouter free model)  → scripts/classify.py
  2) DETERMINISTIC pass (algebraic + rubric)   → this script

This script re-derives every row's score from its raw axes, re-derives the
tier from (score, legal) per Section [6], and runs the Section [12] quality
gates. Divergences and quality-gate violations are persisted to
`validation_audit` and printed. It NEVER overwrites curated scores — it only
flags anomalies for a human to fix.

It is independent of the network (no API), so it always runs. The OpenRouter
half (`classify.py`) is a complementary second opinion and can be re-run
whenever the API key host-allowlist permits.

Usage:
    python3 scripts/validate.py
    python3 scripts/validate.py --db intelligence.db --out validation_report.md
"""

import argparse
import os
import sqlite3
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_DB = os.path.join(ROOT, "intelligence.db")
DEFAULT_OUT = os.path.join(ROOT, "deliverables", "phase5_validation.md")


def weighted(legal, revenue, pain, frequency):
    return legal * 3 + revenue * 2 + pain * 2 + frequency


def expected_tier(legal, score):
    if legal == 3 or score >= 16:
        return "MUST"
    if score >= 10:
        return "SHOULD"
    if score >= 5:
        return "COULD"
    return "WON'T"


def ensure_audit_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS validation_audit (
            asset_map_id   INTEGER PRIMARY KEY REFERENCES asset_map(id),
            issue_code     TEXT NOT NULL,
            issue_detail   TEXT,
            stored_score   INTEGER,
            expected_score INTEGER,
            stored_tier    TEXT,
            expected_tier  TEXT
        );
        """
    )
    conn.execute("DELETE FROM validation_audit;")
    conn.commit()


def run(conn):
    rows = conn.execute(
        """
        SELECT am.id, v.name, bt.name, da.name, da.asset_type, am.buyer,
               am.legal, am.revenue, am.pain, am.frequency,
               am.score, am.tier, am.evidence_url, COALESCE(am.notes, ''),
               COALESCE(bt.work_context, '')
        FROM asset_map am
        JOIN business_types bt ON bt.id = am.business_type_id
        JOIN verticals v       ON v.id = bt.vertical_id
        JOIN digital_assets da ON da.id = am.asset_id
        ORDER BY am.id
        """
    ).fetchall()

    counters = defaultdict(int)
    findings = []

    for (amid, vert, btype, asset, atype, buyer,
         L, R, P, F, score, tier, evidence, notes, work_ctx) in rows:
        issues = []
        # axis range
        for axname, axval in [("legal", L), ("revenue", R), ("pain", P), ("frequency", F)]:
            if axval is None or not (0 <= axval <= 3):
                issues.append(("AXIS_RANGE", f"{axname}={axval}"))
        # score recompute
        exp_score = weighted(L or 0, R or 0, P or 0, F or 0)
        if score != exp_score:
            issues.append(("SCORE_MISMATCH", f"stored={score} expected={exp_score}"))
        # tier recompute
        exp_tier = expected_tier(L or 0, exp_score)
        if tier != exp_tier:
            issues.append(("TIER_MISMATCH", f"stored={tier} expected={exp_tier}"))
        # legal=3 auto-MUST
        if (L or 0) == 3 and tier != "MUST":
            issues.append(("LEGAL3_OFF_MUST", f"legal=3 but tier={tier}"))
        # MUST/SHOULD evidence_url required ([12])
        if tier in ("MUST", "SHOULD") and not (evidence or "").strip():
            issues.append(("MISSING_EVIDENCE", f"tier={tier} evidence_url empty"))
        # buyer dimension required ([5])
        if not (buyer or "").strip():
            issues.append(("MISSING_BUYER", "buyer empty"))
        if buyer and buyer not in ("operator", "auditor", "consultant"):
            issues.append(("BAD_BUYER", f"buyer={buyer}"))
        # trades work-context required ([5]) — accept either business_types.work_context
        # (canonical, set per-trade) OR an explicit tag echoed in asset_map.notes.
        if vert == "Trades":
            ctx_blob = ((work_ctx or "") + " " + (notes or "")).lower()
            ctx_axis_a = any(t in ctx_blob for t in ("solo", "team"))
            ctx_axis_b = any(t in ctx_blob for t in ("on-site", "off-site", "on-the-road", "workshop", "mobile", "yard"))
            if not (ctx_axis_a and ctx_axis_b):
                issues.append(("MISSING_WORK_CONTEXT", "trades row lacks solo/team + site context tag"))
        # null tier
        if not tier:
            issues.append(("NULL_TIER", ""))

        for code, detail in issues:
            counters[code] += 1
            findings.append((amid, code, detail, score, exp_score, tier, exp_tier,
                             vert, btype, asset))

    # duplicate asset name check ([12])
    dups = conn.execute(
        "SELECT lower(name), COUNT(*) FROM digital_assets GROUP BY lower(name) HAVING COUNT(*)>1"
    ).fetchall()
    for n, c in dups:
        counters["DUPLICATE_ASSET_NAME"] += 1
        findings.append((None, "DUPLICATE_ASSET_NAME", f"name={n} count={c}",
                         None, None, None, None, None, None, n))

    # persist
    ensure_audit_table(conn)
    for (amid, code, detail, sc, esc, tr, etr, *_rest) in findings:
        if amid is None:
            continue
        conn.execute(
            "INSERT OR REPLACE INTO validation_audit "
            "(asset_map_id, issue_code, issue_detail, stored_score, expected_score, stored_tier, expected_tier) "
            "VALUES (?,?,?,?,?,?,?);",
            (amid, code, detail, sc, esc, tr, etr),
        )
    conn.commit()
    return counters, findings, len(rows)


def write_report(out_path, counters, findings, total):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    lines = []
    lines.append("# Phase 5 — Validation report (deterministic pass)")
    lines.append("")
    lines.append(f"- asset_map rows scanned: **{total}**")
    issue_total = sum(counters.values())
    lines.append(f"- issues raised: **{issue_total}**")
    lines.append("")
    if not counters:
        lines.append("All Section [12] gates PASS. No anomalies found.")
        with open(out_path, "w") as fh:
            fh.write("\n".join(lines) + "\n")
        return

    lines.append("## Summary by issue code")
    lines.append("")
    lines.append("| Code | Count | Meaning |")
    lines.append("|---|---:|---|")
    explain = {
        "AXIS_RANGE": "axis value outside 0-3",
        "SCORE_MISMATCH": "stored score != 3L+2R+2P+F",
        "TIER_MISMATCH": "stored tier != rubric tier for (score, legal)",
        "LEGAL3_OFF_MUST": "legal=3 row not tier MUST",
        "MISSING_EVIDENCE": "MUST/SHOULD row missing evidence_url",
        "MISSING_BUYER": "asset_map.buyer empty (required by [5])",
        "BAD_BUYER": "buyer not in operator/auditor/consultant",
        "MISSING_WORK_CONTEXT": "trades row lacks work-context tag in notes",
        "NULL_TIER": "tier is NULL",
        "DUPLICATE_ASSET_NAME": "two digital_assets share a normalised name",
    }
    for code, n in sorted(counters.items(), key=lambda x: -x[1]):
        lines.append(f"| {code} | {n} | {explain.get(code, '')} |")

    lines.append("")
    lines.append("## Findings detail (first 50 per code)")
    by_code = defaultdict(list)
    for f in findings:
        by_code[f[1]].append(f)
    for code in sorted(by_code):
        lines.append("")
        lines.append(f"### {code}")
        lines.append("")
        lines.append("| asset_map_id | vertical | business type | asset | detail |")
        lines.append("|---:|---|---|---|---|")
        for (amid, _, detail, _, _, _, _, vert, btype, asset) in by_code[code][:50]:
            lines.append(f"| {amid or '-'} | {vert or '-'} | {btype or '-'} | {asset or '-'} | {detail} |")
    with open(out_path, "w") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    try:
        counters, findings, total = run(conn)
    finally:
        conn.close()

    print(f"asset_map rows scanned : {total}")
    print(f"issues raised          : {sum(counters.values())}")
    if counters:
        for code, n in sorted(counters.items(), key=lambda x: -x[1]):
            print(f"  {code:<24} {n}")
    else:
        print("All [12] quality gates PASS — no anomalies.")
    write_report(args.out, counters, findings, total)
    print(f"\nReport written: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
