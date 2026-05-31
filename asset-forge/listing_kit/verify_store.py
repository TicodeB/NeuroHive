#!/usr/bin/env python3
"""
ASSET-FORGE · listing_kit/verify_store.py
Post-publish READ-ONLY checker. After you create the listings in the dashboard
(neither platform supports creating products via API), run this to confirm each
product is live and priced correctly — so you don't have to eyeball the dashboard.

Reads credentials from the environment first, then asset-forge/.env (git-ignored):
  - Lemon Squeezy:  LEMONSQUEEZY_API_KEY
  - Gumroad:        GUMROAD_ACCESS_TOKEN
Whichever is set is checked. Keys are never printed or committed.

Expected products + prices (EUR):
  P13  Compliance Gap-Analysis & Mock-Audit   €29
  P1   Café / Restaurant Compliance Pack      €34
  P2   Hospitality Operations & GP Bundle     €49

Usage:  python3 listing_kit/verify_store.py
Stdlib only (urllib) — no pip installs.
"""
from __future__ import annotations
import json
import os
import sys
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.normpath(os.path.join(HERE, "..", ".env"))

# Expected catalogue: match on a keyword in the product title -> expected EUR price.
EXPECTED = [
    ("P13", "Gap-Analysis", 29.0),
    ("P1", "Compliance Pack", 34.0),
    ("P2", "Operations", 49.0),
]


def load_env_file(path: str) -> dict:
    vals = {}
    if os.path.isfile(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            vals[k.strip()] = v.strip().strip('"').strip("'")
    return vals


def get_secret(name: str, env_file_vals: dict) -> str | None:
    return os.environ.get(name) or env_file_vals.get(name)


def http_get_json(url: str, headers: dict) -> dict:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def match_expected(title: str):
    t = (title or "").lower()
    for tag, kw, price in EXPECTED:
        if kw.lower() in t:
            return tag, price
    return None, None


def report(found: list[tuple[str, float]]):
    """found = list of (title, price_eur). Cross-check against EXPECTED."""
    print(f"\n  Found {len(found)} product(s) in the store:\n")
    seen = set()
    for title, price in found:
        tag, exp = match_expected(title)
        if tag:
            seen.add(tag)
            ok = (exp is None) or (abs(price - exp) < 0.005)
            flag = "✓" if ok else f"✗ expected €{exp:.2f}"
            print(f"   {flag}  [{tag}] {title} — €{price:.2f}")
        else:
            print(f"   ·  (unmatched) {title} — €{price:.2f}")
    missing = [tag for tag, _, _ in EXPECTED if tag not in seen]
    if missing:
        print(f"\n  ⚠️  Not yet live: {', '.join(missing)}")
    else:
        print("\n  ✅ All three expected products are live.")


def check_lemonsqueezy(key: str):
    print("== Lemon Squeezy ==")
    headers = {
        "Authorization": f"Bearer {key}",
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
    }
    try:
        data = http_get_json("https://api.lemonsqueezy.com/v1/products?page[size]=100", headers)
    except urllib.error.HTTPError as e:
        print(f"  API error {e.code}: {e.reason} (check the key + that a store exists)")
        return
    except Exception as e:  # noqa: BLE001
        print(f"  Could not reach Lemon Squeezy: {e}")
        return
    found = []
    for item in data.get("data", []):
        attr = item.get("attributes", {})
        title = attr.get("name", "")
        # price is in cents; prefer price_formatted if present, else price/100
        cents = attr.get("price")
        price = (cents / 100.0) if isinstance(cents, (int, float)) else 0.0
        found.append((title, price))
    report(found)


def check_gumroad(token: str):
    print("== Gumroad ==")
    try:
        data = http_get_json(
            f"https://api.gumroad.com/v2/products?access_token={token}", {"Accept": "application/json"}
        )
    except urllib.error.HTTPError as e:
        print(f"  API error {e.code}: {e.reason} (check the access token)")
        return
    except Exception as e:  # noqa: BLE001
        print(f"  Could not reach Gumroad: {e}")
        return
    if not data.get("success", False):
        print(f"  Gumroad returned success=false: {data}")
        return
    found = []
    for p in data.get("products", []):
        title = p.get("name", "")
        cents = p.get("price")  # Gumroad price is in cents of the product currency
        price = (cents / 100.0) if isinstance(cents, (int, float)) else 0.0
        found.append((title, price))
    report(found)


def main():
    env_vals = load_env_file(ENV_FILE)
    ls = get_secret("LEMONSQUEEZY_API_KEY", env_vals)
    gr = get_secret("GUMROAD_ACCESS_TOKEN", env_vals)

    if not ls and not gr:
        print(
            "No API credentials found.\n"
            "  Set ONE of these (env var or asset-forge/.env):\n"
            "    LEMONSQUEEZY_API_KEY=...      (Lemon Squeezy, Settings » API)\n"
            "    GUMROAD_ACCESS_TOKEN=...      (Gumroad, Settings » Advanced / OAuth app)\n"
            "  Then re-run:  python3 listing_kit/verify_store.py"
        )
        sys.exit(1)

    if ls:
        check_lemonsqueezy(ls)
    if gr:
        check_gumroad(gr)


if __name__ == "__main__":
    main()
