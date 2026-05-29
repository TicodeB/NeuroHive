#!/usr/bin/env python3
"""
ASSET-FORGE — Phase 5 classification / spot-check pass (OpenRouter free model).

Phase 1 scored every asset_map row INLINE (defensible per-row scores). This
script does the brief's cheap bulk pass WITHOUT touching premium tokens: it
routes an independent re-score of each asset×business-type pairing through a
FREE OpenRouter model, then compares the model's tier to the stored tier and
reports divergences for a human spot-check. It never overwrites the curated
scores — model output lands in a separate `classification_audit` table so we
can re-cut later (brief [3]/[6]).

Secrets: the API key is read from the environment first (OPENROUTER_API_KEY),
then from a git-ignored asset-forge/.env. It is NEVER printed or committed.
Set it via your Claude Code environment variables, or:
    bash asset-forge/scripts/set_secret.sh

Usage:
    python3 scripts/classify.py --dry-run        # check setup, no API calls
    python3 scripts/classify.py                  # spot-check a 10% sample
    python3 scripts/classify.py --all            # score every row
    python3 scripts/classify.py --limit 25       # cap rows this run
    python3 scripts/classify.py --sample 0.2     # 20% sample
"""

import argparse
import json
import os
import random
import sqlite3
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_DB = os.path.join(ROOT, "intelligence.db")
ENV_FILE = os.path.join(ROOT, ".env")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# A $0 model is the default; override with OPENROUTER_MODEL or --model.
DEFAULT_MODEL = "deepseek/deepseek-chat-v3-0324:free"

RUBRIC = (
    "Score this business asset on four axes, integers 0-3 only.\n"
    "Legal/Regulatory: 0 none, 1 advisory, 2 expected, 3 legally mandatory.\n"
    "Revenue/Cash impact: 0 none, 1 minor, 2 material, 3 survival-critical.\n"
    "Pain severity (hurts without it): 0 none, 1 mild, 2 real, 3 severe.\n"
    "Frequency of use: 0 rare, 1 monthly, 2 weekly, 3 daily.\n"
    "Context: EU (Ireland) small/medium business.\n"
    'Return ONLY compact JSON: {"legal":n,"revenue":n,"pain":n,"frequency":n}'
)


def load_env():
    """Populate os.environ from .env for any keys not already set (no override)."""
    if not os.path.exists(ENV_FILE):
        return
    with open(ENV_FILE) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def score_to_tier(legal, score):
    if legal == 3 or score >= 16:
        return "MUST"
    if score >= 10:
        return "SHOULD"
    if score >= 5:
        return "COULD"
    return "WON'T"


def weighted(legal, revenue, pain, frequency):
    return legal * 3 + revenue * 2 + pain * 2 + frequency


def ensure_audit_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS classification_audit (
            asset_map_id  INTEGER PRIMARY KEY REFERENCES asset_map(id),
            model         TEXT,
            legal_m       INTEGER, revenue_m INTEGER, pain_m INTEGER, frequency_m INTEGER,
            score_m       INTEGER, tier_m TEXT,
            tier_stored   TEXT,
            agrees        INTEGER,            -- 1 if model tier == stored tier
            raw           TEXT
        );
        """
    )
    conn.commit()


def fetch_rows(conn, sample, limit, do_all):
    rows = conn.execute(
        """
        SELECT am.id, v.name, bt.name, da.name, da.asset_type, am.buyer,
               am.legal, am.revenue, am.pain, am.frequency, am.score, am.tier,
               COALESCE(am.notes, '')
        FROM asset_map am
        JOIN business_types bt ON bt.id = am.business_type_id
        JOIN verticals v       ON v.id = bt.vertical_id
        JOIN digital_assets da ON da.id = am.asset_id
        ORDER BY am.id
        """
    ).fetchall()
    if not do_all and not limit:
        k = max(1, round(len(rows) * sample))
        rows = random.sample(rows, min(k, len(rows)))
    if limit:
        rows = rows[:limit]
    return rows


def call_openrouter(api_key, model, asset, asset_type, vertical, btype, buyer, notes):
    prompt = (
        f"{RUBRIC}\n\n"
        f"Asset: {asset} (type: {asset_type})\n"
        f"Vertical: {vertical} | Business type: {btype} | Buyer: {buyer}\n"
        f"Notes: {notes or 'n/a'}"
    )
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }).encode()
    req = urllib.request.Request(
        OPENROUTER_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/TicodeB/NeuroHive",
            "X-Title": "ASSET-FORGE classification",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())
    content = data["choices"][0]["message"]["content"].strip()
    # Be tolerant of code fences / stray prose: extract the first {...} block.
    start, end = content.find("{"), content.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON in model reply: {content[:120]}")
    parsed = json.loads(content[start:end + 1])
    return {k: int(parsed[k]) for k in ("legal", "revenue", "pain", "frequency")}, content


def main():
    ap = argparse.ArgumentParser(description="ASSET-FORGE classification spot-check.")
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--model", default=None, help="OpenRouter model slug (else $OPENROUTER_MODEL or default free model)")
    ap.add_argument("--sample", type=float, default=0.10, help="fraction to spot-check (default 0.10)")
    ap.add_argument("--limit", type=int, default=None, help="hard cap on rows this run")
    ap.add_argument("--all", action="store_true", help="score every row")
    ap.add_argument("--dry-run", action="store_true", help="check setup only; no API calls")
    args = ap.parse_args()

    load_env()
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    model = args.model or os.environ.get("OPENROUTER_MODEL") or DEFAULT_MODEL

    conn = sqlite3.connect(args.db)
    try:
        total = conn.execute("SELECT COUNT(*) FROM asset_map").fetchone()[0]
        rows = fetch_rows(conn, args.sample, args.limit, args.all)

        print(f"DB: {args.db}")
        print(f"asset_map rows total : {total}")
        scope = "all" if args.all else f"{args.sample:.0%} sample"
        if args.limit:
            scope += f", limit {args.limit}"
        print(f"rows selected this run : {len(rows)}  ({scope})")
        print(f"model                : {model}")
        print(f"API key present      : {'yes' if api_key else 'NO'}")

        if args.dry_run or not api_key:
            if not api_key and not args.dry_run:
                print("\n[!] No OPENROUTER_API_KEY found. Set it via your Claude Code")
                print("    environment variables, or run: bash asset-forge/scripts/set_secret.sh")
                print("    Then re-run. (Showing dry-run summary; no API calls made.)")
            print("\nDry run OK — setup is wired correctly, no API calls made.")
            return 0

        ensure_audit_table(conn)
        agree = disagree = errors = 0
        for (amid, vert, btype, asset, atype, buyer,
             L, R, P, F, stored_score, stored_tier, notes) in rows:
            try:
                axes, raw = call_openrouter(api_key, model, asset, atype, vert, btype, buyer, notes)
            except (urllib.error.URLError, urllib.error.HTTPError, ValueError, KeyError) as e:
                errors += 1
                print(f"  [err] id={amid} {asset} / {btype}: {e}")
                continue
            ms = weighted(**axes)
            mt = score_to_tier(axes["legal"], ms)
            ok = 1 if mt == stored_tier else 0
            agree += ok
            disagree += (1 - ok)
            conn.execute(
                "INSERT INTO classification_audit "
                "(asset_map_id, model, legal_m, revenue_m, pain_m, frequency_m, score_m, tier_m, tier_stored, agrees, raw) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?) "
                "ON CONFLICT(asset_map_id) DO UPDATE SET "
                "model=excluded.model, legal_m=excluded.legal_m, revenue_m=excluded.revenue_m, "
                "pain_m=excluded.pain_m, frequency_m=excluded.frequency_m, score_m=excluded.score_m, "
                "tier_m=excluded.tier_m, tier_stored=excluded.tier_stored, agrees=excluded.agrees, raw=excluded.raw;",
                (amid, model, axes["legal"], axes["revenue"], axes["pain"], axes["frequency"], ms, mt, stored_tier, ok, raw),
            )
            flag = "ok " if ok else "DIFF"
            print(f"  [{flag}] id={amid:>3} {btype} / {asset[:34]:34} model={mt:6}(={ms:>2}) stored={stored_tier}")
        conn.commit()

        n = agree + disagree
        rate = (agree / n * 100) if n else 0
        print(f"\nScored {n} rows · agree {agree} · disagree {disagree} · errors {errors} · agreement {rate:.0f}%")
        print("Divergences saved to classification_audit (tier_m != tier_stored) — review these by hand.")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
