# Signup & auth checklist — the part only you can do

Goal: a publish-ready seller account + an API key, on whichever platform you choose. Both are
**Merchant-of-Record** → they collect & remit EU VAT for you (you're an Irish seller, so this
matters). Do ONE platform first; the listing kits cover both.

> Verify fees/terms live at signup — they change. Figures below checked 30/05/2026.

---

## Option A — Lemon Squeezy (Phase-8 primary)

Status (30/05/2026): owned by Stripe, **still operating and accepting new sellers**;
"Stripe Managed Payments" is a future migration path, no action needed now. Fee ~5% + 50¢
(effective ~6.5%+ with card costs) — confirm at signup.

- [ ] 1. Create account at **lemonsqueezy.com** → verify email.
- [ ] 2. Create your **Store** (name = your brand). Country = **Ireland**.
- [ ] 3. **Identity / KYC**: sole-trader or business details. As a non-VAT-registered Irish
      sole trader you can still sell — LS is the merchant of record. (Confirm your own VAT
      position with an accountant; you chose to stay non-registered + rely on MoR.)
- [ ] 4. **Payout**: connect your Irish bank (IBAN).
- [ ] 5. Settings » **API** → create an API key. Copy it once (shown only once).
- [ ] 6. Store the key as a secret (see "API key handling").
- [ ] 7. (Optional) Set the store refund policy + the digital "no withdrawal right after
      download" terms (LS provides the checkout checkbox).

→ Then open `P13_listing.md` » "Lemon Squeezy" and create the first product.

---

## Option B — Gumroad (Phase-8 fallback)

Status (30/05/2026): operating; also Merchant-of-Record for EU VAT. Fee ~10% flat — confirm
at signup. Create-product is **dashboard-only** (API 404s on create); API/CLI can upload files
and read your store.

- [ ] 1. Create account at **gumroad.com** → verify email.
- [ ] 2. Settings » **Payments**: country = **Ireland**, connect Irish bank (IBAN).
- [ ] 3. Complete identity verification (KYC) if prompted.
- [ ] 4. **API access token**: gumroad.com/settings/advanced (or gumroad.com/oauth/applications)
      → create an application → "Generate access token". Copy it.
- [ ] 5. Store the token as a secret (see "API key handling").
- [ ] 6. (Optional) Install the Gumroad CLI for automated file re-uploads later.

→ Then open `P13_listing.md` » "Gumroad" and create the first product.

---

## API key handling (do NOT commit keys)

Keys are secrets — never paste them into chat or commit them. Use ONE of:

- **Preferred — environment variable / Claude Code environment secret:**
  - Lemon Squeezy: `LEMONSQUEEZY_API_KEY`
  - Gumroad: `GUMROAD_ACCESS_TOKEN`
- **Or — local git-ignored .env** via the existing helper:
  `bash scripts/set_secret.sh` (writes to `asset-forge/.env`, which `.gitignore` excludes).

`verify_store.py` reads the env var first, then `.env`.

---

## After you publish — confirm it worked
```
python3 listing_kit/verify_store.py     # auto-detects whichever key is set
```
Lists what's live in your store and flags any product whose price ≠ expected
(P13 €29 · P1 €34 · P2 €49) or that's missing. That's your "did it work?" check — no need to
eyeball the dashboard.
