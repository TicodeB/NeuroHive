# Launch listing kit — START HERE

This folder makes publishing your products **pure copy-paste + upload + click**.

## Why it works this way (a hard constraint, verified live 30/05/2026)
> **Neither Lemon Squeezy nor Gumroad lets you create a listing via API.**
> Lemon Squeezy's product API is **read-only** (no create/update endpoint); Gumroad's
> create-product endpoint **returns 404** (dashboard-only — the API can upload *files* to a
> product that already exists). Etsy gates listing-creation behind manual app approval.
> So the "new product → upload file → publish" step is **manual in the dashboard everywhere**
> — which is exactly the auth-gated part that's yours to own.

This kit automates everything *around* that step.

## Files
| File | What | Who |
|---|---|---|
| `signup_checklist.md` | Exact account / KYC / payout / API-key steps (Lemon Squeezy + Gumroad) | **You** (auth) |
| `P13_listing.md` | Paste-ready bilingual (EN/SK) listing copy for both platforms — **publish this first** | You copy-paste |
| `P1_listing.md` | Same, for the Café/Restaurant Compliance Pack | You copy-paste |
| `P2_listing.md` | Same, for the Hospitality Operations & GP Bundle *(to be added)* | You copy-paste |
| `shared/licence_EN_SK.txt` | Reusable licence block (template, not legal advice) | You paste |
| `shared/refund_withdrawal_EN_SK.txt` | Reusable refund / EU-withdrawal block | You paste |
| `verify_store.py` | After publishing, reads your store via API and checks each product is live + priced right | You run once with your key |

## The plan (decided: sell P13 in English first, then localize)
1. **You (auth, ~30–45 min once):** follow `signup_checklist.md` → create the seller account,
   pass KYC, connect your Irish IBAN for payouts, generate an API key, store it as a secret.
2. **You (publish P13, ~5 min, pure copy-paste):** dashboard → New Product → upload the **full**
   `../products/P13_Compliance_Gap_Analysis_Mock_Audit.xlsx` → paste the fields from
   `P13_listing.md` → set price €29 → publish. (The `*_DEMO_*.xlsx` is for the preview image
   only — never the deliverable.)
3. **Verify:** `python3 listing_kit/verify_store.py` confirms it's live at €29.
4. **Then:** add P1 (€34) and P2 (€49) the same way. Localize P13 to DE/FR/ES only **after**
   the English listing proves it converts (with native + legal review per language).

## The 3 products (files live in `../products/`)
| Product | Price | Full file to upload | Preview file |
|---|---|---|---|
| **P13** — Compliance Gap-Analysis & Mock-Audit | €29 | `P13_Compliance_Gap_Analysis_Mock_Audit.xlsx` | `P13_DEMO_…xlsx` |
| P1 — Café / Restaurant Compliance Pack | €34 | `P1_Cafe_Restaurant_Compliance_Pack.xlsx` | `P1_DEMO_…xlsx` |
| P2 — Hospitality Operations & GP Bundle | €49 | `P2_Hospitality_Operations_GP_Bundle.xlsx` | `P2_DEMO_…xlsx` |

## ⚠️ Before you publish
- **Slovak copy needs a native-speaker proofread** (flagged at the top of each SK section). Publishing English first sidesteps this for launch.
- **Capture preview screenshots** from Excel/Google Sheets (no headless renderer in this env) — the thumbnail is the #1 conversion lever.
- **Re-verify platform fees + VAT handling live** at listing time (figures dated 30/05/2026).

## Platform pick
Both are Merchant-of-Record (handle your EU VAT as an Irish seller). Phase-8 lock:
**Lemon Squeezy primary, Gumroad fallback, Etsy as a discovery channel.** Start with Lemon
Squeezy unless signup is gated when you try — then Gumroad. Both kits are ready.
