# LEANTA — Go-Live Runbook

**Created:** 09/06/2026 · **Branch:** `claude/vigilant-bell-sn55pv`
**What shipped:** a complete static storefront at the repo root (landing page, free
"Will I pass?" quiz, 4 product pages, legal pages, free demo downloads, config-driven
checkout). It deploys on the Vercel project already attached to this repo.

The site is designed so that **orders can be taken from day one** (email pre-orders)
and **direct checkout switches on by pasting URLs into one file** — no rebuild.

---

## 0. What is already done (this session)

- [x] Storefront built: `index.html`, `quiz.html`, `products/{p13,p1,p2,bundle}.html`,
      `legal/{terms,privacy}.html`, `assets/`, `downloads/` (3 free demo workbooks),
      `vercel.json`, `robots.txt`, `favicon.svg`.
- [x] Pricing per MONETIZATION_BRIEF / §41 resolution: P13 €29 · P1 €34 · P2 €49 ·
      Hospitality Pro Bundle €69 (genuine €14 saving — Omnibus-safe, no fake timers).
- [x] Legal floor: single-business licence, EU 14-day-withdrawal handling, faulty-file
      refund promise, TÜV framing rule honoured, GDPR-clean privacy (no cookies/trackers;
      quiz runs fully client-side).
- [x] EN-only site copy (Slovak listing copy is NOT published — native-editor pass
      pending per handover; the workbooks themselves are bilingual EN/SK inside and the
      site says exactly that).
- [x] Buy buttons fall back to "Reserve by email" (prefilled order mailto) until a
      checkout URL is configured.

## 1. Make the site public (≈10 minutes)

> **Two hosts are already attached to this repo** — both built PR #20 successfully:
> - **Vercel** project `neuro-hive` → production `https://neuro-hive.vercel.app`
> - **Netlify** project `graceful-toffee-4a8918` → public PR preview:
>   `https://deploy-preview-20--graceful-toffee-4a8918.netlify.app`
>   (click it now to see the site before merging)
>
> *Note: Claude's sandbox cannot reach external sites (egress returns 403
> `host_not_allowed` for every domain), so public reachability could not be verified
> from the session — check the URLs in your own browser.*

1. **Preview the site** at the Netlify deploy-preview URL above; then **merge the PR**
   for branch `claude/vigilant-bell-sn55pv` into `main`. Both hosts auto-deploy `main`.
2. **Pick the primary host** (either is fine for a static site):
   - Vercel: if `https://neuro-hive.vercel.app` shows an auth wall / 403 in your
     browser, Settings → Deployment Protection → **Disabled** for Production.
     `vercel.json` (headers, noindex on downloads) only takes effect here.
   - Netlify: `https://graceful-toffee-4a8918.netlify.app` should serve immediately
     after merge with no settings changes. (If you keep Netlify long-term, mirror the
     `vercel.json` headers in a `_headers` file — ask Claude.)
3. Verify the landing page, quiz, one product page and a demo download all work.
3. ⚠️ **Privacy of the repo (do after Vercel is connected & deploying):** this repo is
   currently **PUBLIC** and contains the FULL paid workbooks under
   `asset-forge/products/*.xlsx` (and in git history). Anyone who finds it gets the
   products free. → GitHub → Settings → change visibility to **Private**. Vercel keeps
   deploying private repos via the GitHub integration. (GitHub Pages on the free plan
   stops working for private repos — irrelevant; Vercel is the host.)

## 2. Switch on real checkout (≈20 minutes, one-time KYC)

**Locked strategy (MONETIZATION_BRIEF §1): Lemon Squeezy primary** — it is a Merchant
of Record: collects AND remits EU VAT per buyer country, you never file; effective fee
~6.5% + $0.50. Gumroad = pre-vetted fallback. Etsy = discovery channel only.

1. Create the store at lemonsqueezy.com → connect your Irish bank (SEPA) → verify ID.
2. Create **8 products** and upload the files from `asset-forge/products/`:
   | Product | Price | File(s) |
   |---|---|---|
   | Compliance Readiness Check | €29 | `P13_Compliance_Gap_Analysis_Mock_Audit.xlsx` |
   | Café & Restaurant Compliance Pack | €34 | `P1_Cafe_Restaurant_Compliance_Pack.xlsx` |
   | Hospitality Operations & GP Bundle | €49 | `P2_Hospitality_Operations_GP_Bundle.xlsx` |
   | Hospitality Pro Bundle | €69 | P1 + P2 files together |
   | H&S Safety Statement Builder | €19 | `P3_HS_Safety_Statement_Builder.xlsx` |
   | Cashflow & P&L Tracker | €24 | `P4_Cashflow_PL_Tracker.xlsx` |
   | Fire Safety Register & Checks Log | €15 | `P5_Fire_Safety_Register.xlsx` |
   | Staff Training & Induction Matrix | €15 | `P12_Staff_Training_Matrix.xlsx` |
   Listing copy: `marketing/listings_etsy_gumroad.md` + per-product READMEs.
   Checkout config keys: p13, p1, p2, bundle, p3, p4, p5, p12.
3. In each product enable: **immediate-delivery / 14-day-withdrawal consent checkbox**
   (LS provides), license keys + update delivery.
4. Copy each product's **Buy link** into `assets/checkout-config.js` → `checkoutUrl`.
   Commit + push. Buttons flip from "Reserve by email" to "Buy now" automatically.
5. **Test-purchase** one product as an EU buyer; check the invoice shows LS as seller
   with VAT handled; confirm file delivery works.

**Alternative/parallel fast path — Stripe Payment Links:** the Stripe MCP connector is
wired into the Claude session; completing its OAuth lets Claude create the products and
payment links for you and paste them into the config. ⚠️ Caveat recorded in the
monetization brief: Stripe direct makes YOU the merchant of record (you handle any VAT
duties yourself — viable below thresholds, but confirm with the accountant; LS remains
the locked zero-admin strategy).

**Until either is done:** buttons collect orders by email — reply with a payment link
(Stripe invoice / Revolut / bank transfer) and send the file manually. Slower, but you
can earn from the first visitor.

## 3. Domain & email (mostly DONE — ≈10 minutes left)

- [x] **leanta.ie is owned and verified** (Zoho org "Leanta", verified 27/05/2026).
- [x] **hello@leanta.ie is live on Zoho Workplace** (subscription active 13/05/2026,
      mail sending confirmed). The whole site — contact links, buy-button mailtos,
      legal pages — already uses `hello@leanta.ie` (09/06/2026).
- [x] **leanta.sk is owned too** (Websupport.sk, paid 21/05/2026 — DNS lives in the
      Websupport panel). Mail strategy: **no second mailbox** — `info@leanta.sk` runs
      as a sender alias on the same leanta.ie Zoho mailbox (switch the From address
      in Zoho webmail when writing to Slovak customers).
- [ ] **Point the web side of leanta.ie at the host** — add the domain in the Vercel
      (or Netlify) dashboard and set ONLY the records it asks for:
      apex `A` (or `ALIAS`) + `www` `CNAME`. DNS for leanta.ie is managed at
      **Register 365**.
      ⚠️ **Do NOT touch the existing Zoho records** (`MX`, `SPF/TXT`, `DKIM`) or
      hello@leanta.ie stops receiving mail. Web and mail records coexist fine.
- [ ] **Alias deliverability check (one-time):** sending as `info@leanta.sk` only
      stays out of spam if **leanta.sk's DNS at Websupport carries Zoho's SPF (TXT)
      and DKIM records** for that domain alias. Verify: send a test from
      info@leanta.sk to a Gmail address → open ⋮ → "Show original" → SPF and DKIM
      must both say PASS for the leanta.sk sender. If not, add the records Zoho Mail
      Admin shows under Domains → leanta.sk.
- [ ] **Park leanta.sk usefully:** until the Slovak site ships (gated on the native
      SK copy pass), set a 301 redirect leanta.sk → leanta.ie (Websupport panel or
      add it as a redirect domain on the host) so the domain isn't dead and collects
      any type-in traffic.
- [ ] Update `<title>`/OG tags canonical domain when leanta.ie is live.

## 4. First-week traffic (the funnel, MONETIZATION_BRIEF §7)

- [ ] **Etsy discovery listings** for P1 and P13 (static-file delivery: PDF with the
      demo + link to the site per §1.3) — Etsy's search traffic is the top-of-funnel.
- [ ] Share the **free quiz** link in Irish hospitality owner groups (Facebook groups,
      r/ireland small-biz threads, LinkedIn) — lead with the quiz, not the products.
- [ ] **P13 price experiment** (§41): list €29; test €19 / €29 / €39; hold at the
      conversion-maximising point.
- [ ] Capture every buyer/enquirer email into a list (the list is the moat — §8).

## 5. Quality backlog (before scaling spend)

- [ ] **Slovak native-editor pass** on workbook SK copy + future SK site copy
      (blocker for publishing any SK marketing text — standing rule).
- [ ] **Preview images**: screenshot real sheets in Excel/Google Sheets and replace the
      CSS mockups on product pages.
- [ ] **Accountant sign-off**: MoR sales vs your Irish VAT position (§1.4) — and the
      Stripe-direct caveat if you use Payment Links.
- [ ] Re-verify LS fees + comparables at listing time (figures dated 30/05/2026).
- [ ] Marketing asset pipeline: HeyGen/Higgsfield connectors are available in Claude
      sessions for product explainer videos / hero imagery when ads start.

## 6. Architecture notes (for future sessions)

- Site = plain static HTML/CSS/JS at repo root; no build step; works on Vercel
  (primary) and GitHub Pages (paths are relative).
- `assets/checkout-config.js` is the single switchboard: contact email + per-product
  checkout URLs. Empty URL ⇒ email pre-order flow.
- Quiz scoring mirrors P13's RAG bands (🟢 ≥85 · 🟠 60–84 · 🔴 <60) — keep them in sync
  if the workbook logic changes.
- Demo workbooks in `/downloads/` are copies of `asset-forge/products/*DEMO*` — re-copy
  after any rebuild (`scripts/build_p*.py`).
- Next products to list when ready (roadmap): P14–P18 per-standard kits, P21 à-la-carte
  module €19 as the cheaper top-of-funnel.
