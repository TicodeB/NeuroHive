## STATE — 10/06/2026 (LAUNCH-WEEK SESSION 3 — site v3 + growth initiatives capture)
**Branch:** `claude/trusting-noether-rxejqv` (PR #21, base = vigilant-bell → rides PR #20).

### ✅ DONE THIS SESSION
- **Site v3 shipped:** three.js 3D hero (mouse+scroll parallax, card tilt, reduced-motion/CDN-fail safe → CSS orbs fallback) · logo reworked (rising-check `favicon.svg`, applied site-wide via `.brand-mark` CSS) · homepage "old way vs Leanta way" demo-selling section · dashboard showcase ("insight, not decoration", every KPI prescribes an action; labelled illustrative/sample data) · comms section ("text us, we reply AND action"; `data-textus` renderer + `LEANTA.contactPhone` config — **EMPTY: Samuel must fill the business mobile**) · **`grants.html`** — €200-out-of-pocket grant pathway (honest mechanics: mobilisation fee buys audit+application pack; LEO decides; not-approved ⇒ client chooses) · LSS DMAIC method section on services · payment trust badges + x402-roadmap line in all 12 page footers (NO raw card fields — PCI stays with MoR).
- **`marketing/GROWTH_INITIATIVES_PLAN.md`** — captures ALL of Samuel's 10/06 asks: local NACE Ferns+30km plan (research agents died on session limit 09/06 — re-run queued), demo-selling angle + ranked sales ideas, video pipeline (Google Flow/Seedance/ElevenLabs/HeyGen + EU AI Act labelling note), image-gen prompt base (no-slop rule: product screenshots always real), external design-tool prompt (v0/Lovable/"omma.ai" — name unconfirmed), monthly-drop "Leanta Club" subscription design, Excel Office.js agent add-in roadmap (Sheets version exists, PR #16), gamma-grade pack design v2 (pivot-table honesty → .pbit SKU), affiliate/hardware arm guardrails, x402 token-bucket sequencing, AI-glasses rule (don't show hardware we don't own), persona "Máire" + why-NOT-buy, competitor list awaited from Samuel.
- **`forms/CLIENT_PRELIM_RESEARCH.md`** — mandatory pre-engagement research template (stakeholders, process inventory, est. available cash, grant route majority-funded, GDPR/data-safety note; client files NEVER in a public repo).

### ✅ ALSO THIS SESSION (later)
- **Quiz v2:** industry picker (9 sectors) → 4 industry + 6 universal questions → verdict on screen → **message-first CTAs** (visitor-initiated prefilled WhatsApp/SMS/email with score+industry; activates fully when `contactPhone` set). GDPR: customer-initiated contact, no gating of the verdict.
- **Plan §15:** channel rails decision (WhatsApp Business app NOW · sms: links NOW · WhatsApp API via Twilio/360dialog at volume, prices to verify · Telegram = Hermes ops only · iMessage skip) + **Hermes operator role & guardrails** (replies only in customer-initiated threads, approved templates, honest bot disclosure, escalation rules). Next build: 9 industry action-plan reply templates + Hermes runbook in repo.
- **omma.build identified** = Spline's NL builder for interactive 3D sites — use to prototype hero scene/design concepts; watch runtime weight on rural mobile.

### ▶️ NEXT
- Samuel: Tue/Wed gate steps (merge #20 → repo PRIVATE → LS KYC → checkout URLs) + fill `contactPhone` in `assets/checkout-config.js` + paste competitor list + confirm "omma.ai" service name + browser-check the 3D hero (sandbox can't render).
- Claude: re-run §1 local-landscape + §AI-media research agents → `research/local_ferns_30km.md`; write first 3 video scripts (plan §3); Etsy listing support Thu.

---

## STATE — 09/06/2026 ~20:30 (LAUNCH-WEEK SESSION 2 — Tuesday gate check + sales machinery execution)
**Branch:** `claude/trusting-noether-rxejqv` (= vigilant-bell 6420d2d + this session; PR based on vigilant-bell so it rides PR #20 into main).

### ✅ DONE THIS SESSION
- **PR #20 flipped draft → READY FOR REVIEW** — Samuel's merge is now one click (github.com/TicodeB/NeuroHive/pull/20).
- **Gate status verified (Tue checklist, playbook §1):** repo **STILL PUBLIC** (paid files + history exposed — flip to PRIVATE remains the #1 manual step, Settings → General → Danger Zone, AFTER merging #20); `assets/checkout-config.js` all 8 SKUs in email pre-order mode = correct day-one state; Vercel bot on #20 says deploy **Ready** and Netlify preview **ready** → the 403s curl gets from this sandbox are egress, NOT a broken site — Samuel must browser-check neuro-hive.vercel.app + the Netlify URL.
- **Gmail recon:** NO pre-orders at hello@leanta.ie yet (forwards visible in Gmail). ⚠️ **Stripe emailed "[Action required] Provide information about Leanta" twice (28/05 + 04/06)** — Stripe account restricted pending info; only matters if the Stripe-fallback path is wanted (VAT caveat: Stripe ≠ MoR → conflicts with locked stay-non-registered/MoR decision; LS primary stands).
- **6 Gmail drafts created in samuel.vyhnanek@gmail.com** (addressed to self; swap recipient + [bracketed] fields, delete marker line): §A nurture e-mails 1–5 + §B pre-order reply. Real URLs filled (leanta.ie/products/{p1,p13,bundle,tools}.html); unsubscribe = reply-based (no ESP yet — swap in link when ESP chosen); §B LS-URL placeholder kept.

### ▶️ NEXT (launch week — playbook §1 is the source of truth)
- **Samuel TONIGHT (Tue):** merge #20 → repo PRIVATE → browser-check both hosts (paid paths blocked, demos download) → quiz end-to-end on phone → join 3 FB groups. If DNS not yet pointed, share vercel.app links, not leanta.ie.
- **Samuel WED:** LS KYC → upload 8 products → paste checkout URLs into `assets/checkout-config.js` (on main post-merge) → real test purchase. Answer Stripe's action-required only if fallback wanted.
- **Claude next session:** verify merge + checkout URLs live; Etsy listing support (Thu) from `marketing/listings_etsy_gumroad.md`; Friday posts staged from `launch_posts.md`; poster QR (replace placeholder with real QR → leanta.ie/quiz.html) printable on request. Deferred queue unchanged (SK backfill ids 21–54, P6–P11/P14–P21, ESP, Skool, deploy purge).

---

## STATE — 09/06/2026 (LAUNCH SESSION — post-project)
**LAUNCH:** Leanta storefront built at repo ROOT (outside `asset-forge/`) on branch
`claude/vigilant-bell-sn55pv` — landing + free "Will I pass?" quiz + product pages
(P13 €29 · P1 €34 · P2 €49 · Hospitality Pro Bundle €69) + legal pages + demo
downloads + config-driven checkout (`assets/checkout-config.js`: empty URL ⇒ email
pre-order; paste LS/Stripe URL ⇒ Buy now). Deploys via the Vercel project already
attached to this repo (`neuro-hive.vercel.app`, currently 403 = deployment protection).
**Manual go-live steps (Samuel) live in `/LAUNCH_RUNBOOK.md`** — merge PR → disable
Vercel deployment protection → make repo PRIVATE (full paid xlsx are public!) → LS
KYC → paste checkout URLs. Site copy EN-only (SK gated on native pass, per rule).

**SAME-DAY EXTENSION (CEO sprint, Fri 12/06 deadline):** (1) **4 new à-la-carte
products built** — P3 €19 / P4 €24 / P5 €15 / P12 €15 via `scripts/build_alacarte_tools.py`
(composes the validated P1/P2 sheet builders; full+DEMO; zip/XML+tab+merge validated;
demos in site `/downloads/`; see `products/TOOLS_README.md`). Catalogue now **8 SKUs**.
(2) **Design v2 "Emerald Mesh"** — light cream/gloss/glassmorphism (NO dark bg per
Samuel), 3D orbs, button sheen, scroll-reveal (reduced-motion safe). (3) **Security:**
`.vercelignore` + `netlify.toml` block `asset-forge/` (paid files) from both hosts;
repo-private still pending Samuel. (4) **Agency arm added** — `services.html` (Lean
Six Sigma + AI, on-site, 8 verticals) + `insights.html` whitepaper + grant funnel
(LEO Digital for Business fully-funded; Grow Digital Voucher €5k/50%; Lean for Micro
— verified live 09/06/2026, re-verify at use). (5) **`marketing/`** — sales playbook,
flywheel/moat strategy (incl. NotebookLM sourcebook + Skool + A4 poster), listings,
posts, nurture emails. (6) hello@leanta.ie wired site-wide; leanta.ie @ Register 365;
leanta.sk @ Websupport (alias info@leanta.sk). Target: €2,000 revenue month 1 (10×
tool spend); pricing experiments per §41.

### ▶️ NEXT SESSION (run on branch **`claude/vigilant-bell-sn55pv`** until PR #20 merges; after merge → `main`)
1. **Samuel's physical steps first** (LAUNCH_RUNBOOK.md): merge PR #20 → check
   site public on both hosts → **repo PRIVATE** → LS KYC → paste 8 checkout URLs
   into `assets/checkout-config.js` → test-purchase. Stripe alternative: re-run
   the Stripe MCP OAuth in the new session (old URL expires) and Claude wires
   Payment Links.
2. **Then Claude executes SALES_PLAYBOOK.md** (marketing/): Etsy listings from
   `listings_etsy_gumroad.md`, posts from `launch_posts.md`, nurture from
   `email_nurture.md` (Gmail drafts), poster print (marketing/poster_a4.html →
   browser print → A4), NotebookLM: upload `LEANTA_STORY_SOURCEBOOK.md`.
3. **Deferred build queue:** P6–P11 + P14–P21 packs (needs SK backfill ids 21–54
   first — bilingual rule); SK storefront on leanta.sk (needs native SK pass);
   preview screenshots for listings; Skool community setup (FLYWHEEL_MOAT_STRATEGY §d);
   ESP for nurture sequence; Vercel/Netlify old-deploy purge (leak hygiene).
4. **Sources of truth:** LAUNCH_RUNBOOK.md (go-live) · marketing/SALES_PLAYBOOK.md
   (week-1 selling) · marketing/FLYWHEEL_MOAT_STRATEGY.md (moat/flywheel/edu) ·
   MONETIZATION_BRIEF.md §7–8 (funnel/moat doctrine) · this handover (state).

---

## STATE — 30/05/2026 21:30
Project: ASSET-FORGE
Phase last completed: 12 — 🎁 Build a flagship compliance pack (BONUS) ✅ COMPLETE — **PROJECT COMPLETE (13/13 sessions)**
Checkpoint score: 1 flagship compliance pack built (P13 Gap-Analysis + Mock-Audit, full + DEMO) | **100% complete (13 of 13 sessions)**. All Phase 9 + Phase 12 flagships shipped (P1, P2, P13). ▶️ NEXT = optional pre-launch hardening (Slovak native edit · preview images · live fee re-verify) — see §below.

### ✅ DONE THIS SESSION (Phase 12 — code tier)
- **Built P13 — Compliance Gap-Analysis & Mock-Audit (Lite)**, the bonus-track flagship, via `scripts/build_p13_gap_analysis_pack.py` (re-runnable; full + watermarked DEMO, P1/P2 builder pattern). Bundles `CA:1` (Gap-Analysis) + `CA:2` (Mock-Audit).
- **5 sheets, bilingual EN/SK:** 00 Start Here · 01 Gap Analysis (26 clauses × 8 sections, generic Annex SL + food spine) · 02 Mock Audit (20 "could you show…?" questions) · 03 Readiness dashboard · 04 Next Steps (upsell routing to P14–P18).
- **Real logic (not blank tables):** Status dropdown → auto Conf.% (Conform 100 / Partial 50 / Not in place 0 / N/A excluded) + auto Priority (HIGH/MEDIUM); `AVERAGEIFS` per-section roll-up; overall conformance + mock readiness averaged into an **overall readiness % with RAG "will I pass?" verdict** (🟢 ≥85 · 🟠 60–84 · 🔴 <60); live `COUNTIF` HIGH/MEDIUM gap counters. RAG conditional formatting throughout. Scoring design emulated & verified.
- **Outputs:** `products/P13_Compliance_Gap_Analysis_Mock_Audit.xlsx` (full, free, editable) + `products/P13_DEMO_…xlsx` (sheet-protected, "enter email to download" watermark) + `products/P13_README.md` (product sheet + EN/SK listing copy + launch-checklist + funnel/bundle path).
- **EU conventions:** DD/MM/YYYY, percentages, metric framing, 852/2004 · 1169/2011 · Amd 1:2024 refs. **Framing rule honoured:** "audit-ready for a TÜV-style certifier" — never "TÜV template". → upsells to P14–P18.
- **⚠️ v1.1 BUGFIX (Samuel hit Excel "we found a problem with content"):** two real defects fixed — (1) a 32-char tab name ("02 · Mock Audit · Skúšobný audit") exceeded Excel's 31-char limit → corruption; shortened to "…· Skúška" + builder now asserts ≤31; (2) DEMO used `insert_rows()`, which corrupts merged-cell/CF ranges → replaced with a non-destructive "DEMO Preview · Ukážka" notice sheet + sheet protection. **Same `insert_rows` pattern existed in build_p1 & build_p2 demos → FIXED both the same way + rebuilt.** All 6 product files re-validated (XML well-formed · tabs ≤31 · zero merged-range overlaps). **NOTE: LibreOffice/soffice is BROKEN in this sandbox** (can't open even a trivial xlsx) → validate xlsx via openpyxl reload + zip/XML parse + merged-overlap check, NOT soffice.
- **PRICING (§41 RESOLVED):** P13 is **PAID €29** (launch test), not free — Samuel: "sell as much as you can, see what market can take." DB re-seeded (P13 → 29.0/`pack`); `seed_compliance.py` AUDIT_PRODUCTS + AUDIT_LADDER updated; validate.py green; 24 products, **0 free-tier**.

### ✅ DONE THIS SESSION (Phase 11 productisation + Funnel/Monetization extension)

**Sales funnel & conversion architecture (Samuel-requested, planning tier):**
- Samuel's frame: *"only starting up; digital products to the right audience = passive income."* → automation-first, free-tier-only, niche-targeted.
- Added **MONETIZATION_BRIEF.md §7** — the value-ladder (Rung 0 free teaser → Rung 1 à-la-carte module → Rung 2 pack → Rung 3 everything-kit), the conversion stack that **legally replaces Samuel's "exit timer" idea** (order bump · post-purchase one-time upsell · abandoned-cart recovery code · 3–5 email nurture), the marketing playbook, EU **Omnibus** legal guardrails (no fake/resetting timers — Amazon fined €7.48M; real sum-of-parts savings only; GDPR consent), and the lead-magnet decision.
- **Lead-magnet decision (Samuel): no-code interactive quiz NOW (Tally/Typeform, free, GDPR-ready) delivering the existing "Lite" file; dedicated web app DEFERRED** until traffic/conversion is proven (needs a hosted front-end — none in repo — + GDPR setup). "Module" = both levels (sheets buyable AND packs buyable inside kits).
- **DB:** added `products.pricing_tier` (free/module/pack/kit) + `products.parent_product` (rolls-up-into). Backfilled all base + audit rows; added **4 representative à-la-carte compliance modules** (Rung 1) to prove the structure — rest of catalogue is a documented roll-out, not hand-authored. **Now 24 products** (1 free · 8 module · 13 pack · 2 kit). Verified: no NULL tiers, no dup names, no dangling CA refs, **every child priced below its parent (Omnibus-safe)**, base enrichment intact.
- **Deferred (documented, NOT built):** custom lead-magnet web app + funnel page (interactive assessment, exit-intent, on-page timer) — future phase, gated on proven volume + GDPR + hosting.

### ✅ DONE THIS SESSION (Phase 11 — planning tier)
- Extended `deliverables/PRODUCT_ROADMAP.md` with **PART B — Audit & Compliance Productisation** (§4–§8): the tiered offer, per-standard bundle definitions from `v_audit_packs`, 8 one-page build specs, bundle architecture, and the Phase-12 handoff.
- Added **8 new product rows (P13–P20)** to the `products` table via `scripts/seed_products.py` (now **20 products total**). Each carries `audience` (operator/auditor/consultant) + `standard_ids` (→ `standards` table). Re-seeded & verified.
- **Tier ladder (brief §15.5):** ① FREE gap-analysis-lite lead magnet (P13, €0) → ② operator standard kits €49–99 (P14 HACCP Café/Restaurant €49 · P15 ISO 22000/FSSC 22000 €99 · P16 BRCGS/IFS Doc-Control €89 · P17 ISO 9001 €79 · P18 FSSC 22000 V7 Transition €49) → ③ pro audit suite €149+ (P19 Auditor Edition €149 · P20 Consultant Multi-Client Console €149).
- **Two-sided demand captured:** same audit premise sells an operator readiness pack AND an auditor protocol — `compliance_assets.buyer_role` already carries both → incremental revenue, zero new research.
- **No new builds invented:** every compliance product bundles existing `compliance_assets` by ID. Their `bundled_asset_ids` carry a **`CA:` prefix** to disambiguate from `digital_assets` IDs (Phase-7 rows).
- **Pricing grounded live (Tavily, 30/05/2026):** single templates €10–60 (Etsy/Gumroad) vs consultant ISO toolkits €300–800+ (Advisera) → our €49–99 kits + €149+ auditor editions sit in the defensible middle. Prices INDICATIVE — re-verify at listing.
- **Framing rule honoured (brief §15):** packs positioned "audit-ready for a TÜV-style certifier auditing you to ISO/BRCGS/IFS", NEVER "TÜV templates."

### ▶️ NEXT SMALLEST ACTION
- **BRANCH:** all Phase-12 work is on **`claude/cool-planck-rYR4I`** (this branch carries Phases 0–12). A PR will be opened for it. Run any follow-up `/goal` on this branch.
- **PROJECT COMPLETE — all 13 sessions done.** Every brief §1 deliverable exists: `intelligence.db`, MASTER_INTELLIGENCE_REPORT, asset_catalogue.xlsx, PRODUCT_ROADMAP, MONETIZATION_BRIEF, and 3 built flagships (P1, P2 hospitality + P13 compliance). No further phase to run.
- **Optional pre-launch hardening (NOT a phase — do before publishing any listing):** (1) Slovak native-editor pass on all listing copy + the 34 food/non-food/trades assets (ids 21–54) + 19 compliance_assets still needing SK microcopy; (2) export preview-image screenshots from Excel/Google Sheets (no headless renderer in this env); (3) re-verify Lemon Squeezy fees + EU VAT/MoR + marketplace comparables live at listing time; (4) wire the P13 email-capture funnel + GDPR consent; (5) confirm standard-version triggers (BRCGS Issue 10, ISO 9001:2026) for transition-pack upsells when they publish.

### ➕ STANDING ADD-ONS (carry forward)
- **openpyxl required** for any .xlsx build/inspection — not vendored; `pip install openpyxl` in each fresh session (3.1.5 used). P1/P2 builders + `export_catalogue.py` need it. **Phase 12 P13 builder will need it.**
- **Bilingual EN+SK** binding rule (AGENTS.md). **34 food/non-food/trades assets (ids 21–54) still need SK names/microcopy**; compliance_assets (19) also need an SK pass — backfill before listing P6–P20. Slovak in all listing copy needs a **native-editor pass before public launch** (`/slovak` skill NOT installed here).
- **Platform LOCKED (Phase 8):** Lemon Squeezy primary / Gumroad fallback / Etsy discovery. Don't quote LS "5%" — effective ~6.5%+$0.50. All 20 `products.platform` = "Lemon Squeezy".
- **Prices LOCKED/INDICATIVE:** P1 €34, P2 €49 (locked). P13–P20 indicative (see roadmap §4) — re-verify live at listing.
- **DB now has:** `standards` (21), `compliance_assets` (19), view `v_audit_packs` (115 rows), `products` (**24 rows** — 12 base + 8 audit P13–P20 + 4 à-la-carte compliance modules; columns `audience`, `standard_ids`, `pricing_tier`, `parent_product` populated). **Re-seed ORDER MATTERS:** `python3 scripts/seed_products.py` (12 base — wipes `products`, adds pricing_tier/parent_product cols + base ladder) **THEN** `python3 scripts/seed_compliance.py` (re-enriches base + adds 8 audit rows + 4 module rows = 24). Audit products live in `seed_compliance.py` (`AUDIT_PRODUCTS`/`AUDIT_MODULES`/`AUDIT_LADDER`), base ladder in `seed_products.py` (`LADDER`).
- **Value-ladder columns:** `pricing_tier` ∈ {free,module,pack,kit}; `parent_product` = name of the pack/kit a module/pack rolls into (NULL for top-level). Invariant to keep (Omnibus-safe): every child price < its parent price. MONETIZATION_BRIEF §7 is the funnel source of truth.
- **CA-prefix convention:** audit/compliance products store `bundled_asset_ids` as `CA:<ids>` referencing `compliance_assets`; Phase-7 products store plain ids referencing `digital_assets`. Phase-12 build + any export must respect this split.
- **Research tooling:** Tavily MCP, Semantic Scholar, Consensus.
- **Script set:** init_db, classify, validate, export_catalogue, seed_* (hospitality/food/nonfood/trades/products/existing_solutions/compliance), build_p1_compliance_pack, build_p2_operations_bundle, **build_p13_gap_analysis_pack** (Phase 12), set_secret.
- No `sqlite3` CLI — use Python `sqlite3` module for DB inspection.

### ❓ OPEN QUESTIONS / DECISIONS NEEDED FROM SAMUEL
- ✅ RESOLVED (Samuel, 30/05/2026): **P13 is PAID, not free.** "Sell as much as you can, see what market can take." → DB P13 = **€29 launch test**, tier `pack`. Run the price experiment €19 → €29 → €39 and hold at the conversion-maximising ceiling. Free-tier products now 0; top-of-funnel discovery falls to module P21 (€19) or a future cut-down teaser.
- ✅ RESOLVED (Samuel, 30/05/2026): VAT — stay non-registered + rely on MoR (Lemon Squeezy is legal seller, handles per-sale EU VAT). Confirm specifics with accountant before launch.
- ✅ RESOLVED (Samuel, 30/05/2026): Excise/duty (alcohol) — KEEP FOLDED into Cashflow/P&L (P2/P4). No dedicated excise tracker.
- Confirm `asset-forge/` living inside the `NeuroHive` repo is intended. (Unchanged.)

### ⚠️ RISKS / WATCHOUTS
- **Slovak copy not yet native-edited** — do NOT publish any listing SK text before a native pass.
- **Compliance prices indicative** — re-verify marketplace comparables + LS fees live at listing time (figures dated 30/05/2026).
- **Standard versions move** — BRCGS Issue 10 (in development) and ISO 9001:2026 (at FDIS) will trigger "transition pack" upsells (mirror P18) and listing-copy updates when they publish.
- **Preview images not generated** (no headless spreadsheet renderer in this env) — capture screenshots at listing time from Excel/Google Sheets.
- **Lemon Squeezy post-Stripe-acquisition uncertainty** — Gumroad fallback pre-vetted; both host the same files, migration = re-upload not rebuild.
- **EU digital-goods withdrawal right** — listings must include the immediate-delivery / 14-day-waiver checkbox (LS provides). Free P13 still needs correct licence/terms.
- One phase per session; if a phase looks like >~15 tool calls, propose splitting.
- Legal-mandatory (Legal=3) auto-promotes to MUST — held since Phase 5 (115/115). Phases 7–11 did not alter tiers.
