# MONETIZATION BRIEF — ASSET-FORGE

**Project:** SME Digital-Asset Intelligence → Productisation Pipeline
**Owner:** Samuel Vyhnanek · **Context:** EU (Ireland) seller
**Phase:** 8 — Monetization · **Date:** 30/05/2026
**Deliverable #5 of the project DoD.** Locks the **sales platform** (EU-VAT-aware),
**pricing**, **bundle architecture** and a **launch checklist** for the 12 products in
`deliverables/PRODUCT_ROADMAP.md` / the `products` DB table.

> **Accuracy note (brief §3):** all platform fees + VAT handling below were **re-verified
> live on 30/05/2026** (not stated from memory). Sources are cited inline and recorded in
> the `existing_solutions` DB table. Fees change — re-check the cited pages before launch.

---

## 1. Platform decision (brief §11 — EU-VAT / Merchant-of-Record heavily weighted)

### 1.1 What changed since the Phase 1 preliminary view

The Phase 1 lean (`research/market_validation.md`) was **Lemon Squeezy primary / Gumroad
fallback**, tie-broken on a headline "5% + $0.50 beats 10% + $0.50". Live re-verification
**materially refines** that picture:

1. **Lemon Squeezy was acquired by Stripe (July 2024).** It is still a full Merchant of
   Record in 2026, but its headline 5% + $0.50 **stacks surcharges**: **+1.5% on
   international (non-US) cards, +1.5% on PayPal, +0.5% on subscriptions**, pushing the
   effective rate to ~6.5–8.9%. For an **Irish seller selling to EU/global buyers, the
   +1.5% international-card surcharge applies to essentially every sale**, so the real fee
   is ~**6.5% + $0.50**, not 5%. There is also documented post-acquisition roadmap
   uncertainty (Stripe's own "Managed Payments" MoR is in beta).
2. **Gumroad became a full Merchant of Record on 01/01/2025.** Earlier sources (and the
   Phase 1 table) predate this. Its **10% + $0.50 is now genuinely all-in** (card
   processing + global VAT/GST/sales-tax collection **and remittance** bundled), with **no
   international/PayPal surcharges** and **weekly (Friday) payouts**.
3. **Payhip is only a *partial* MoR** — it collects EU/UK VAT but the **seller remains the
   legal seller of record** for everything else (and sources disagree on whether it even
   remits the EU VAT or merely collects it). This **fails the heavily-weighted
   zero-tax-admin bar** for an Ireland-based solo operator and is dropped from contention.

### 1.2 Weighted comparison (live-verified, 30/05/2026)

EU-VAT / full-MoR is the decisive, heavily-weighted criterion (seller is in Ireland →
digital-goods VAT must be handled *for* us, with **zero** filing admin and **zero** monthly
cost while volume is low).

| Criterion (weight) | **Lemon Squeezy** | **Gumroad** | Payhip (free) | Etsy |
|---|:--:|:--:|:--:|:--:|
| **Full MoR — collects *and remits* EU VAT, zero filing (×3 — decisive)** | ✅ full MoR | ✅ full MoR (since 01/2025) | ⚠️ partial (EU/UK VAT only; seller stays SoR) | ✅ acts as supplier for EU VAT on digital items |
| **All-in fee on a low-ticket (€15–€59) EU sale** | 5% + $0.50 **+1.5% intl card** ≈ **~6.5% + $0.50** | **10% + $0.50 flat, all-in** | 5% + ~2.9%+$0.30 processing ≈ **~7.9%** | listing $0.20 + **6.5%** + 3–4% processing + optional ads |
| **No monthly cost / free tier** | ✅ | ✅ | ✅ (Free plan) | ❌ (per-listing + fees) |
| **Payout to an Irish/EU (SEPA) bank** | ✅ via Stripe; **twice-monthly** | ✅ via Stripe; **weekly (Fri)** | ✅ instant (Stripe/PayPal) | ✅ (Payoneer/bank) |
| **Spreadsheet / file delivery + license keys + update delivery** | ✅ | ✅ | ✅ | ❌ static files only (PDF-link workaround) |
| **Built-in buyer discovery** | ❌ (bring your own traffic) | ✅ Discover (but Discover sales cost **30%**) | ❌ | ✅ (huge buyer intent) |
| **Runs with 0 employees (automation)** | ✅ | ✅ | ✅ | ✅ |
| **Platform stability / roadmap** | ⚠️ post-Stripe-acquisition uncertainty | ✅ stable, established | ✅ stable | ✅ stable |

### 1.3 Decision

> 🥇 **PRIMARY — Lemon Squeezy.** It clears the decisive bar (full MoR: collects **and
> remits** EU VAT in 100+ countries, seller never files), has **no monthly cost**, delivers
> spreadsheets + license keys + buyer update-delivery, and even with the +1.5%
> international-card surcharge its **~6.5% + $0.50 all-in is the lowest real fee** of the
> full-MoR options — the best margin on €15–€59 templates sold solo.
>
> 🥈 **FALLBACK — Gumroad.** Also a **full MoR since Jan 2025**, with two advantages that
> make it the deliberate fallback rather than an afterthought: (a) **flat 10% + $0.50 with
> no surcharges** → fully predictable, and (b) **built-in Discover traffic** for a seller
> with no audience. The fee is higher, but Gumroad is the **switch-to target** if Lemon
> Squeezy's post-acquisition roadmap degrades (see §6 watchouts) — migration is low-cost
> because both are MoR storefronts hosting the same files.
>
> 📣 **DISCOVERY CHANNEL — Etsy.** Unchanged from Phase 1. Despite higher fees and
> Google-Sheets delivery friction (static files → deliver a PDF with a "make a copy" link),
> its buyer intent for "restaurant / spreadsheet templates" is unmatched (1,000+ restaurant
> templates, 5,000+ spreadsheet templates already listed). Use it as **top-of-funnel** and
> to read competitor price/sales signals — **not** as the MoR storefront of record.

**Why not Payhip / Ko-fi:** Payhip is only a partial MoR (re-introduces EU VAT filing risk
for an Irish seller); Ko-fi handles no VAT and is tip-led. Both fail the decisive criterion.

### 1.4 EU VAT — how it actually works for this seller (the heavily-weighted point)

- Digital products (templates/spreadsheets) are **TBE / electronically-supplied services**:
  EU B2C VAT is due in the **buyer's country of residence** (destination principle), via the
  **OSS** scheme once pan-EU B2C sales exceed **€10,000/year** (below that, home-country
  Irish VAT may apply).
- **Because Lemon Squeezy (and Gumroad) act as Merchant of Record, the *platform* is the
  legal seller to the buyer.** It calculates the correct local VAT per buyer country, charges
  it at checkout, and **remits it to the tax authorities**. The seller receives a net payout
  and **does not register for VAT-OSS or file VAT returns on these sales.** This is the entire
  reason a full MoR is the decisive, heavily-weighted criterion here.
- Practical pricing consequence: set the **list price as the gross the buyer pays**; the MoR
  extracts/handles the VAT component and the platform fee, and pays out the remainder.
- ⚠️ **Confirm with an accountant** how these MoR sales interact with Samuel's *overall*
  Irish VAT-registration position (the MoR handles the per-sale VAT, not the seller's wider
  business registration). VAT rules change — re-verify before launch.

---

## 2. Pricing — locked launch prices (EU, gross to buyer)

Phase 7 prices were *indicative vs marketplace comparables*; they are **confirmed as the
launch list prices** here (benchmarks re-checked: Etsy/Gumroad HACCP/allergen bundles
€19–€49; ops bundles €39–€59; finance trackers €15–€35 — the roadmap prices sit correctly
inside these bands). Prices are the **gross the buyer pays**; the MoR handles VAT on top of /
within this, and the platform fee is deducted from it.

| # | Product | List € (gross) | Approx. net after ~6.5%+$0.50 MoR fee* |
|---:|---|:--:|:--:|
| P1 | Café / Restaurant Compliance Pack ⭐ | **€34** | ≈ €31.3 |
| P2 | Hospitality Operations & GP Bundle | **€49** | ≈ €45.3 |
| P3 | H&S Risk Assessment & Safety Statement Builder | **€19** | ≈ €17.3 |
| P4 | Cashflow & P&L Tracker | **€24** | ≈ €22.0 |
| P5 | Fire Safety Register & Checks Log | **€15** | ≈ €13.6 |
| P6 | Trades Quote → Job → Invoice Suite | **€39** | ≈ €36.0 |
| P7 | Electrician / Gas Compliance Cert Pack | **€34** | ≈ €31.3 |
| P8 | Food-Manufacturing Compliance Core | **€59** | ≈ €54.7 |
| P9 | Recipe / BOM & Batch Costing Calculator | **€29** | ≈ €26.7 |
| P10 | Product Label & Nutrition Declaration Generator | **€29** | ≈ €26.7 |
| P11 | Manufacturing ISO 9001 / Quality Pack | **€49** | ≈ €45.3 |
| P12 | Staff Training & Induction Matrix | **€15** | ≈ €13.6 |

\* Illustrative net = list − (6.5% + ~€0.46). VAT is collected/remitted **by the MoR on top**,
so it does not reduce the seller's net. Net is indicative; exact FX/surcharge varies per sale.

**Pricing strategy**

- **Anchor + ladder.** Cheap universal leaders (P3 €19, P5 €15, P12 €15) act as low-friction
  entry points and bundle attach; mid-tier hospitality/trades (€29–€49) are the volume core;
  P8 €59 is the premium (failure = lost approval → high willingness-to-pay).
- **Lead magnet.** Ship a **free "gap-analysis lite / readiness self-check"** as the funnel's
  Rung 0 — launched as a **no-code interactive quiz** (Tally/Typeform) that emails the result
  + the downloadable Lite, funnelling to the paid packs. **See §7 for the full value-ladder,
  conversion stack (order bump / post-purchase upsell / abandoned-cart / nurture) and the EU
  legal guardrails that replace the original "exit timer" idea.**
- **Charm vs round.** Launch at the round € figures above for a clean compliance/"tool"
  positioning; A/B test €X.99 charm pricing on the discovery channel (Etsy) only.
- **Hospitality-first.** P1 is the first listing; P2 the immediate cross-sell.

---

## 3. Bundle architecture (standalone → vertical bundle → everything kit)

Carried from PRODUCT_ROADMAP §1 and confirmed. Bundle prices give a visible discount vs
buying parts, pushing average order value up.

```
HOSPITALITY (ship first):
  P1 Café/Restaurant Compliance Pack (€34) ─┐
                                            ├─► Hospitality Pro Bundle  (P1+P2)  €69   (vs €83)
  P2 Hospitality Ops & GP Bundle    (€49) ─┘            │
                                                        └─► cross-sell P3/P4/P5

COMPLIANCE / SAFETY (universal anchors):
  P3 H&S Safety Statement (€19) ─┐
  P5 Fire Register        (€15) ─┴─► Safety Starter  (P3+P5)  €29  (vs €34)
                                          │
                                          └─► Compliance Everything  (P1+P8+P11+P7)  €149  (vs €176)

MONEY (desired / high-WTP):
  P4 Cashflow & P&L (€24) ─┐
  P9 Recipe/BOM Costing (€29) ─┤
  P6 Trades Quote→Job→Invoice (€39) ─┴─► Money Toolkit  (P4+P9+P6)  €79  (vs €92)
```

- **Vertical packs** sell best (focused buyer intent): "HACCP Readiness Pack for Cafés",
  "ISO 9001 Internal Audit Kit" (bonus track). Build once, list per-vertical.
- **Path:** standalone → vertical bundle → "everything" kit. Always show the bundle on each
  standalone listing as the upsell.

---

## 4. Launch checklist (solo, 0-employee, automatable)

**Account & tax**
- [ ] Create Lemon Squeezy store; connect Irish bank (SEPA) for payouts; verify identity.
- [ ] Confirm MoR/VAT handling is ON (default) and check a test EU-buyer invoice shows VAT
      collected by Lemon Squeezy as MoR.
- [ ] Accountant sign-off on how MoR sales sit alongside Samuel's Irish VAT position (§1.4).
- [ ] (Fallback prep) Reserve the Gumroad store name so a switch is instant if needed.
- [ ] Create Etsy shop for discovery; note Etsy delivers static files only (PDF + copy-link).

**Per-product listing (start with P1, then P2)**
- [ ] **Listing copy** — EN **and** SK (bilingual rule, AGENTS.md): title, "pain it kills"
      hook (quote owner-voice from `pain_points`), feature list = bundled asset names,
      "satisfies EHO / Reg. 852/2004 + 1169/2011 + fire + Safety Statement" trust line.
- [ ] **Preview images** — 3–5 screenshots of the actual sheets (allergen matrix, temp log,
      dashboard) + a "what's inside" contents slide. Watermark previews.
- [ ] **Demo / read-only** Google-Sheets preview link (no edit) as proof.
- [ ] **License text** — single-business / personal-use licence; no resale/redistribution.
- [ ] **Refund policy** — digital-goods: state "no refunds once downloaded" where legal;
      offer goodwill replacement for faulty files (EU consumer law: buyer waives the 14-day
      withdrawal right for instant digital delivery — include the explicit consent checkbox
      Lemon Squeezy provides).
- [ ] **Delivery** — upload .xlsx + a Google-Sheets "make a copy" link + a 1-page PDF setup
      guide (EN/SK). Enable license keys + buyer update-delivery for versioned files.
- [ ] **Categories/tags** — "HACCP template", "restaurant spreadsheet", "allergen matrix",
      "cafe compliance" (mirror the Etsy search terms proven in `market_validation.md`).

**Pre-launch QA**
- [ ] Test-purchase each product as an EU buyer; confirm VAT line, file delivery, copy-link.
- [ ] Verify EU formatting in every shipped sheet (metric units, DD/MM/YYYY, comma
      thousands) and that SK headers/microcopy are native-quality (route through editor).
- [ ] Bundle links resolve and apply the discounted price.

**Post-launch**
- [ ] Etsy listings live as discovery → link buyers to Lemon Squeezy for bundles.
- [ ] Seed the free lead-magnet self-check; capture emails.
- [ ] Read top competitor listings' visible sales/reviews to recalibrate price/units.
- [ ] Backfill SK names/microcopy for asset ids 21–54 (still EN-only) before listing the
      food/non-food/trades products (P6–P12).

---

## 5. Competitor / platform intelligence captured to DB

The `existing_solutions` table (previously empty) is now populated with the **live-verified
platform fees + the MoR/VAT facts** above, plus representative **template-marketplace
comparables** (the price points our products are benchmarked against). Regenerate with
`python3 scripts/seed_existing_solutions.py`. `products.platform` is updated from the
"TBD Phase 8" placeholder to **"Lemon Squeezy"** for all 12 rows; prices in §2 confirmed.

---

## 6. Risks / watchouts

- ⚠️ **Lemon Squeezy post-Stripe-acquisition uncertainty** is the main platform risk. Mitigation:
  Gumroad fallback is pre-vetted (full MoR, store name reserved). **Switch trigger:** any
  removal of MoR VAT handling, a fee increase past ~8% effective, or payout/onboarding
  breakage. Both host the same files → migration is a re-upload, not a rebuild.
- ⚠️ **+1.5% international-card surcharge** means the real Lemon Squeezy fee is ~6.5%, not 5% —
  modelled into §2. Don't quote 5% in financial projections.
- ⚠️ **Etsy delivers static files only** — Google-Sheets products need the PDF + "make a copy"
  link workaround; never the raw .xlsx where the licence forbids redistribution.
- ⚠️ **EU digital-goods withdrawal right** — include the explicit "I consent to immediate
  delivery and waive my 14-day withdrawal right" checkbox (Lemon Squeezy provides this).
- ⚠️ **SK copy for ids 21–54 outstanding** — bilingual rule blocks launch of P6–P12 until the
  Slovak glossary is backfilled and editor-checked.
- ⚠️ **Re-verify fees at listing time** — all figures dated 30/05/2026; platforms change pricing.

---

## 7. Sales funnel & conversion architecture (added 30/05/2026)

> **Operating frame (Samuel):** *"I am only starting up. Selling digital products to the
> right audience could be good passive income."* Every choice below is filtered by three
> rules that frame demands: **(1) automation-first** — nothing that needs ongoing manual
> work; **(2) zero/low upfront cost** — free tiers until something proves it earns;
> **(3) right audience > big audience** — win by being *specific*, not by reaching everyone.
> The product is not where the money is made — **the funnel is.** A great spreadsheet listed
> flat sells a handful of copies; the same asset inside an automated value-ladder compounds.

### 7.1 The value ladder (Samuel's idea, expressed 1:1)

```
RUNG 0 — FREE TEASER (the hook)          interactive "Will I pass?" quiz → emails the result
   │                                     + the downloadable "Lite" (deliberately incomplete)
   ▼
RUNG 1 — À-LA-CARTE MODULE (bite price)  any single tool/sheet on its own  ≈ €9–19
   │                                     (e.g. just the CAPA Log, just the Allergen Matrix)
   ▼
RUNG 2 — FULL PACK (the discount)        pack price < sum of its modules → genuine saving
   │                                     (P1 €34, HACCP Readiness €49, ISO 22000 Kit €99…)
   ▼
RUNG 3 — EVERYTHING KIT (biggest disc.)  pack-of-packs < sum of packs (Compliance Everything €149)
```

- **"Module" = both levels** (Samuel): individual sheets are buyable *and* packs are buyable
  inside a bigger kit; the genuine saving applies at each step up.
- Free DEMO/Lite files already exist for P1, P2 and P13 (Rung 0 is mostly built).

### 7.2 The conversion stack that replaces the "exit timer" (all Lemon-Squeezy-native, all legal)

Samuel's original "stop them as they leave with a 1-minute timer" is **redesigned** — a
resetting/fake countdown is a **banned EU dark pattern** (see §7.4). These deliver the same
"rescue the sale / raise order value" goal, legally and with higher conversion:

1. **Order bump at checkout** — one-click "+€9 add the Training Matrix." Typical take-rate
   10–30%, pure margin, zero extra traffic.
2. **Post-purchase one-time upsell (OTO)** — straight after purchase: *"complete your pack —
   upgrade to the full kit for €X off, this once."* A **genuine** one-time offer (not a
   resetting timer); routinely lifts average order value 10–20%.
3. **Abandoned-cart recovery email** — auto-sent to buyers who leave before paying, carrying
   a **single-use code with a real, fixed deadline** (e.g. 48–72h). The legal stand-in for
   the exit timer.
4. **Email nurture sequence (3–5 emails)** to everyone who took the free quiz — deliver
   value, then soft-pitch the pack. **This is where most revenue actually comes from;** the
   free hook is worthless without the follow-up.

### 7.3 Marketing playbook (what works for a solo EU template seller)

- **Niche positioning beats generic** — "HACCP Readiness for Irish Cafés" out-converts
  "compliance templates." The per-vertical packs already built are the unfair advantage.
- **Price anchoring / decoy** — always show the everything-kit beside the pack with a real
  "save €X vs buying separately"; makes the mid-tier the obvious choice.
- **Social proof / trust** — reviews, "satisfies an EHO inspection / Reg. 852/2004", units
  sold. Compliance buyers buy on *risk reduction* — trust signals are the conversion lever.
- **Etsy = top-of-funnel discovery** (proven buyer intent for "restaurant/spreadsheet
  templates") → redirect to Lemon Squeezy for the ladder (lower fees, cleaner MoR VAT).
- **Interactive lead magnet > static download** — a scored self-assessment roughly doubles
  opt-in vs a file. Hence Rung 0 is a quiz, not just a download.

### 7.4 Legal guardrails (EU Omnibus Directive 2019/2161 — Ireland seller)

- ❌ **No fake or resetting countdown timers** and ❌ **no fake "was/now" prices** — blacklisted
  dark patterns. Amazon was fined **€7.48M** for resetting timers; ~30% of Black-Friday
  sellers were found in breach in EU sweeps.
- ✅ **Order bumps, post-purchase OTOs, and real single-use/real-deadline codes are fine** —
  they are genuine offers, not deception.
- 📐 **Reference-price rule:** if a struck-through "before" price is ever shown, it must be the
  lowest price charged in the **prior 30 days**.
- 🔐 **GDPR:** email capture is personal data → privacy policy + lawful-basis consent on the
  quiz (the no-code tools below provide this).
- 🧾 MoR (Lemon Squeezy) still collects/remits EU VAT on the **discounted** price — discounts
  don't change the seller's zero-filing position.

### 7.5 Lead-magnet format decision (Samuel: no-code quiz now, web app later)

A custom interactive lead-magnet **web app** is the highest-converting format, but for a
starter with no audience it front-loads build + hosting + maintenance + GDPR with payoff that
only scales with traffic — and there is **no front-end in this repo today**. Decision:

- **Now:** launch the identical "Will I pass?" assessment as a **no-code interactive quiz**
  (Tally / Typeform — free tier, GDPR-friendly, native email capture + "email me my result",
  embeds anywhere, live in an afternoon). It delivers the existing **"Lite"** file as the
  result. ~80% of the web-app's conversion lift at ~€0 cost and ~0 maintenance (passive).
- **Later (deferred phase):** graduate to a **dedicated lead-magnet web app + funnel page**
  (interactive scored assessment, exit-intent capture) **only once the quiz proves volume +
  click-through to paid.** Prerequisites to flag at that point: a hosted front-end (none
  exists yet) and a GDPR setup. Documented as future, not built now.

### 7.6 Worked example — compliance line ladder (illustrative; verify at listing)

```
Rung 0  Gap-Analysis "Lite" quiz                              FREE   (email capture)
Rung 1  single module (e.g. CAPA Log / Training Matrix)       €12    (à-la-carte)
Rung 2  HACCP Readiness Pack for Cafés (bundles ~7 modules)   €49    (< sum of modules)
Rung 3  Compliance Everything kit (bundles multiple packs)    €149   (< sum of packs)
        + order bump (+€9 Training Matrix), post-purchase OTO (kit −€20 once),
          abandoned-cart code (48h, single-use)
```
The genuine sum-of-parts saving at Rungs 2–3 is what makes the discount **Omnibus-safe**.

*(See `PRODUCT_ROADMAP.md` for product-by-product mapping; this §7 is the funnel source of truth.)*

---

*End of Monetization Brief — Phase 8 (+ §7 funnel/marketing extension, 30/05/2026). Next:
Phase 12 — build the P13 Gap-Analysis + Mock-Audit flagship (the Rung-0/Rung-1 engine).*
