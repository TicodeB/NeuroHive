# Fees & EU-VAT live re-verification — 31/05/2026

Pre-launch hardening task (1 of 3). Re-verifies the platform fees and EU-VAT/MoR
assumptions in `deliverables/MONETIZATION_BRIEF.md` (figures previously dated
30/05/2026). **Verdict: all assumptions HOLD — verification confirmed, nothing
overturned.** Re-verify again immediately before any public listing (these move).

## Method
Live web search (Tavily) against primary sources (the platforms' own pricing /
help pages) plus an independent MoR explainer and the European Commission VAT
page. One good source per fact, cross-checked.

## 1. Lemon Squeezy (primary) — CONFIRMED
- **Base fee: 5% + 50¢ per transaction.** (lemonsqueezy.com/pricing)
- **Surcharges (NEW detail, not previously captured):**
  - international cards **+1.5%**
  - subscriptions **+0.5%**
  - PayPal **+1.5%**
  (lemonsqueezy.com/help/billing/fees)
- **Merchant of Record:** collects + remits taxes (incl. EU VAT) on the seller's
  behalf — seller is paid out net.
- **All-in budgeting:** on a typical one-off EU card sale, 5% + 50¢ + the 1.5%
  intl-card surcharge ⇒ **~6.5% + 50¢** — matches the brief's "~6.5%+ all-in".
  On a €25 pack that's ≈ €1.13 + €0.50 ≈ **€1.63 (~6.5%)**; on a €49 pack ≈
  €3.19 + €0.50 ≈ **€3.69 (~7.5%)** (fixed 50¢ weighs heavier on cheaper packs —
  relevant to the €19 teaser tier).
- **Stripe-acquisition status:** Lemon Squeezy joined Stripe (Jul 2024) but
  **continues to operate as a standalone MoR platform; new signups remain open.**
  (lemonsqueezy.com/blog/lemon-squeezy-joins-stripe; /help) → the handover
  "post-Stripe uncertainty" watch-out is **lower risk** than feared, but keep
  Gumroad pre-vetted as fallback (both host the same files; migration =
  re-upload, not rebuild).

## 2. Gumroad (fallback) — CONFIRMED
- **Flat 10% per sale + payment processing.** (gumroad.com/pricing)
- **Merchant of Record for EU VAT on digital products** — collects + remits EU
  VAT automatically. (help.gumroad.com — sales tax)
- Still the right fallback: simpler/flat but ~1.5–3.5pp more expensive than LS at
  our price points; only switch if LS access changes.

## 3. EU VAT / MoR strategy — CONFIRMED
- When a platform acts as **Merchant of Record it is the legal seller** and takes
  on the VAT liability: registering, charging the correct per-country rate, and
  remitting. **The creator does not need to register for EU VAT OSS/MOSS** for
  those sales. (Quaderno — Merchant of Record)
- European Commission: B2C digital services are taxed in the **customer's**
  country (since 2015); where a **platform/marketplace is the deemed supplier the
  platform accounts for the VAT**. (taxation-customs.ec.europa.eu/vat-digital_en)
- → The brief's strategy — **stay VAT-non-registered + rely on the platform as
  MoR** — remains valid for an Irish microbusiness. **Still confirm with the
  accountant before launch** (Irish domestic VAT-registration thresholds and any
  non-MoR/direct sales are out of scope of MoR cover).

## Net effect on the brief
- Fee figures unchanged (5%+50¢ LS / 10% Gumroad) → **no pricing change needed.**
- Added nuance to fold into pricing: the **+1.5% international-card** surcharge is
  the usual real-world add-on for EU buyers, and the **fixed 50¢ hurts the €19
  teaser most** — keep the cheapest tier ≥ €19 so the fixed fee stays < ~3%.
- Lowered the LS-discontinuity risk (signups open, standalone post-Stripe).

## Sources (re-verify live at listing)
- lemonsqueezy.com/pricing · lemonsqueezy.com/help/billing/fees
- lemonsqueezy.com/blog/lemon-squeezy-joins-stripe · lemonsqueezy.com/help
- gumroad.com/pricing · help.gumroad.com (sales tax / VAT)
- quaderno.io/blog/merchant-of-record · taxation-customs.ec.europa.eu/vat-digital_en
