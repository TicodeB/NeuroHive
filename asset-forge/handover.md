## STATE — 10/06/2026 ~12:30 (SESSION 5 — Samuel's verdicts actioned → v4.3 "THE DESCENT" SHIPPED)
**Branch:** `claude/trusting-noether-rxejqv` (PR #21). HEAD `2318253`, Vercel GREEN.
**Preview:** https://neuro-hive-git-claude-trusting-noether-rxejqv-ticodebs-projects.vercel.app/v4/

### ✅ DONE THIS SESSION
- **v4.2 (superseded same day):** vivid dark palette + Bebas/Caveat brand + ascent-A glyph + Valentime pacing. Samuel's 2nd verdict killed the dark direction.
- **v4.3 "THE DESCENT" (CURRENT):** full rebuild to Samuel's spec — paper-storm + icosahedron + three.js REMOVED. Bright glassmorphism `#f2efe8`. Sticky descent through 3 REAL environments (generated with **nano banana 2 pro** via Gemini API on Samuel's machine, AI-tagged on page): retail shop → manufacturing floor → hotel lobby (`v4/assets/img/bg-{1-retail,2-factory,3-lobby}.jpg`). Per-env: glass card + sector pains + CTA + lead magnet + **companion picker** (Lea sprout/Penny fox/Mossy sheep → rides Lea orb, localStorage; `ommaPetUrl` overrides). **Mind map** "THE LOGIC, UNFOLDED" (SVG steps). **Pricing WITH grant (€200 credited) vs WITHOUT (quote first)** — verbatim-honest. Brand: glyph single emerald, thinner handwritten "agency", frosted brandpill always legible, typewriter hero, floor elevator, magnetic pull, char-stagger (nbsp fix), radial preloader. No CDN deps at all. Verified locally via Playwright screenshots (hero/env/mind/pricing all render).
- **Hermes runbook** `marketing/HERMES_RUNBOOK.md` (plan §15): 9 sector reply templates (quiz chips), guardrails, escalation, universal blocks.
- **3 video scripts** `marketing/video_scripts.md` (plan §3): The Tuesday 60s · The Number 45s · The Offer 30s; FLOW/HEYGEN/SCREEN tags, EU AI Act labels; finished files → `v4/assets/case-{1..3}.mp4` auto-embed.
- **Media briefs** `v4/assets/MEDIA_BRIEFS.md`: Higgsfield bg-loop prompt+spec, Suno track brief, Omma pet steps (36 credits — pet only, ask before more spend).
- **Antigravity dust field (Samuel's upload, 10/06 eve):** the background animation from antigravity.google (zip capture inspected: three.js r180 `landing-main-particles-component`, light theme) cloned dependency-free — Canvas2D ink+12%-emerald dots, upward anti-gravity drift + sway + cursor repulsion, `mix-blend-mode:multiply` into the cream; mounted on hero (`.hero-bg .dust`) + `#why`; still-until-kinetic, IO-paused off-screen, static frame under reduced-motion, 40% count on mobile; verified by Playwright screenshots.
- **§1 research agent** re-launched in background (Ferns+30km prospects + LEO scheme status) → lands as `research/local_ferns_30km.md` next push if completed.

### ⚠️ BLOCKERS / NOTES
- **Claude-in-Chrome extension NOT connecting** (Chrome runs, extension unreachable) → could not drive Higgsfield/Suno/Omma apps. Samuel: check the extension is installed+signed in, then ask Claude to run the three MEDIA_BRIEFS jobs.
- Higgsfield MCP connector still lacks generate_image/generate_video (only outpaint/upscale/motion/bg-removal) — backdrops were made with nano banana instead (Samuel allowed: "nano banana 2 or pro").
- Still pending from Samuel: contactPhone in checkout-config.js · launch gate (merge #20 → repo PRIVATE → LS KYC → checkout URLs) · Suno track · case films · Omma pet URL.

### ⏭ NEXT SESSION
0. **BINDING — sales-asset language rule (Samuel, raised 09/06, dropped between sessions, re-confirmed 10/06):** NO bilingual interiors anywhere. Every sales asset ships in ONE language: EN edition for leanta.ie, SK edition (after native pass) for leanta.sk. The 13a single-language decision was only ever applied to the 24 NEW premium packs — the 8 storefront SKUs (P13/P1/P2/bundle/P3/P4/P5/P12) are still bilingual EN/SK inside AND still v1 styling. Queue (first /goal session after launch gate): rebuild all 8 as EN-only THROUGH `design_system.py` (the gamma-grade backgrounds/covers Samuel asked for — also dropped); SK editions follow the native pass. Builders already support single-language; AGENTS.md "Bilingual EN+SK" rule is hereby superseded for ALL sales assets.
1. Samuel browser-verdict on v4.3 (desktop+phone). Tune only.
2. If Chrome extension works: run MEDIA_BRIEFS jobs (Suno theme → leanta-theme.mp3 · Omma pet remix → ommaPetUrl · optional Higgsfield bg upgrade).
3. Commit research/local_ferns_30km.md when the agent lands; then /v4 promotion decision; then queue per plan.

---

## STATE — 10/06/2026 ~10:00 (SESSION 4 CLOSE — v4.1 cinematic mockup SHIPPED, context full, session ended)
**Branch:** `claude/trusting-noether-rxejqv` (PR #21, base = vigilant-bell → rides PR #20). HEAD `c5211ea`, Vercel deploy GREEN.
**Preview Samuel checks:** https://neuro-hive-git-claude-trusting-noether-rxejqv-ticodebs-projects.vercel.app/v4/ (desktop = cinematic, phone = flow mode; preloader plays once per session — private window to replay). `claude.md` at repo ROOT = always-current preview links (Samuel's standing ask: keep latest Vercel link there after every build).

### ⏭ NEXT SESSION — FIRST ACTIONS
0. ~~v4.2 BUILD QUEUE~~ **SUPERSEDED by v4.3 "THE DESCENT" (see top block + v4/NORTHSTAR.md)** — kept for history; the Gemini brief was rewritten to v4.3 canon:
   - **LEA → single pixel-art mascot** (Codex-terminal-pet style: moves + EXPRESSIONS, transparent bg). Kill the SVG sprout AND the Omma iframe option (`ommaPetUrl` → remove). Build as code-generated pixel SVG: expressions (idle/blink/happy/talk/surprised/think/sleep/hatch), pupils track cursor, **client-switchable skin colours** (cobalt #5468ff default — Samuel liked the codex pic's blue+amber complementaries, "or bolder"; presets: emerald/ember/gold/orchid, localStorage).
   - **LEA rides the scroll**: moves with the journey; on station change she vanishes from the old screen and **hatches** onto the new one (egg-crack animation).
   - **Chat bubble big→small**: open panel shrinks on scroll into a mini pill showing the last short reply (terminal-pet style); click re-expands.
   - **Camera: pure Z-axis dolly** hero→hero (kill the ±5.5 x-swings; near-axis drift only).
   - **Hero declutter**: LEANTA + one line ("Pass the inspection. Know your numbers. Keep your evenings.") + scrollcue ONLY. **Preloader: remove the 00 counter digits** (bar + wordmark stay).
   - **Env video layers**: per-station 5s loop videos + ambient sound (retail murmur, production line etc.), start on mousemove, crossfade per station, gated by sound toggle, HEAD-check slots `v4/assets/env/ch{1..4},finale.{mp4,mp3,jpg}` (renderer goes alpha so 3D floats over video). Samuel generates via Flow/Higgsfield/Gemini using brief §4.1–4.3.
   - **Palette: add ember #ff6b35** (energy/hover accent, story world) + cobalt #5468ff (LEA ONLY); emerald stays anchor, gold stays money-only.
   - **Local-logo carousel** (NOT chips/buttons): typographic wordmarks of real Ferns/Gorey/Enniscorthy businesses (Omni Pro Ferns confirmed by Samuel; rest of list needs his confirm) + permission-gated PNG slots `v4/assets/logos/<slug>.png`, non-endorsement fine print.
   - **Logo: drop any "agency" suffix**. Proposal: handwritten "Leanta" capital-L, hard black/cream — **Caveat Bold woff2 already self-hosted** (`v4/assets/fonts/Caveat-Bold-*.woff2`, OFL, downloaded+verified 10/06); apply to v4 chrome wordmark as proposal; Gemini moodboard prompt in brief §4.5.
1. Read this block + the "v4.1 REBUILD" block below + `claude.md`. v4.1 architecture stands — v4.2 is the feedback pass above, not a rebuild.
2. Awaiting from Samuel (blockers for their items only): mockup verdict desktop+phone · Suno track → `v4/assets/leanta-theme.mp3` (sound btn auto-swaps from WebAudio pad) · case films → `v4/assets/case-{1..3}.mp4` · Omma pet: remix https://omma.build/community/i6ttegp2zyw1 in his account (403 from sandbox), publish, paste scene URL into `ommaPetUrl` in `assets/checkout-config.js` (slot wired, SVG pet fallback live) · `contactPhone` still EMPTY · launch gate (merge #20 → repo PRIVATE → LS KYC → checkout URLs) still open.
3. Claude queue (priority order): post-verdict v4 tweaks → decision: promote /v4/ to index.html? → 9 industry action-plan reply templates + Hermes runbook (plan §15) → re-run §1 local-research agents → 3 video scripts (plan §3) → post-launch: `/api/lea` serverless (real model; `LEA_UPGRADE` marker in v4.js) + Higgsfield backdrops (connector lacked generate_image).

---

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

### ✅ ALSO THIS SESSION (v4 storytelling mockup — noomo direction)
- **Decisions (Samuel via Q&A):** HYBRID — dark cinematic storytelling landing; store/quiz/grants stay light cream. Mockup at **/v4/** (launch pages untouched). Display face **Anton** (OFL; Druk is commercial — NOT used; noomo zip inspected at /tmp only) + **IBM Plex Mono** (OFL, self-hosted). Typefonted LEANTA wordmark direction accepted; favicon swap deferred to post-approval.
- **Built `/v4/`** (index.html + v4.css + v4.js + fonts, ~37KB own code vs noomo's 876KB): preloader counter · custom cursor (fine pointers) · film grain+vignette · emerald constellation hero canvas · marquee · 5 chapters (01 THE FOLDER old-way / 02 THE TUESDAY beats + video slot / 03 THE NUMBERS KPI count-up / 04 THE VISIT €200 offer verbatim-honest / 05 THE PROOF snap gallery) · finale quiz CTA + industry chips · 15.3vw outline footer. GSAP+ScrollTrigger+Lenis via pinned CDNs, full reduced-motion/no-JS/no-CDN fallbacks. Sound: consent pill, OFF by default, auto-hides until `v4/assets/leanta-theme.mp3` exists (Suno, Samuel — check plan covers commercial use). Video slots HEAD-check `v4/assets/case-{1..3}.mp4`; poster fallbacks + EU-AI-Act "AI-assisted" tags baked in.
- **Higgsfield connector limitation:** session exposes only outpaint/upscale/motion-control/bg-removal — NO generate_image. Backdrops deferred; page complete without them. Prompts for Samuel in plan §4 (cream/emerald still-life base, dark variant: "near-black #0b0d0c, emerald glass, gold accent, film grain, editorial").

### ✅ v4.1 REBUILD (10/06 — Samuel: "so many things missing" + noomo source pasted → full noomo architecture)
- **Root-cause of the unstyled screenshots:** Vercel `trailingSlash:false` redirected `/v4/`→`/v4`, breaking every relative URL → all CSS/JS/font paths now ABSOLUTE (`/v4/...`). Fixed first, then rebuilt.
- **Noomo architecture adopted for real** (their HTML/CSS skeleton analysed from Samuel's paste): one fixed three.js scene (`#scene`) + 760vh scroll runway (`#stage`) drives a **cinematic camera on a CatmullRom spline through 5 stations** — hero icosahedron+gold ring → 01 paper-storm CHAOS → 02 papers morph into ORDERED GRID (the story IS the scene) → 03 KPI bars rise → 04 gold portal + road dashes. Fixed glass panels fade/slide per station (mouse parallax on camera + panels). three.js r152 pinned CDN; GSAP/Lenis dropped (not needed). Desktop fine-pointer only; mobile/reduced/no-WebGL/no-JS ⇒ `html.flow` readable document (noomo does the same ≤1024px).
- **Glassmorphism** everywhere content sits (noomo's blur+gradient card recipe, darkened) · **sound toggle now ALWAYS visible** — WebAudio ambient pad (honest placeholder, off by default) auto-swaps to `v4/assets/leanta-theme.mp3` when the Suno file lands · scroll-progress hairline · skip-intro a11y link.
- **Lead catcher** (noomo home-form equivalent, GDPR-honest): name/business/pain + start-point radio pills (€15–69 toolkit · €200 pathway · advice) → composes mailto + WhatsApp/SMS prefills (no data ever posted by the page itself).
- **LEA — pet assistant** (Samuel: "cute pet like omma.build/community/i6ttegp2zyw1, embed intelligent model"): floating orb pet = built-in animated SVG sprout-creature (blinks, pupils track cursor, hover-squish) — auto-replaced by Samuel's **Omma/Spline scene iframe when `LEANTA.ommaPetUrl` is set in assets/checkout-config.js** (key added; omma.build is 403 from sandbox — Samuel remixes the community item in his account, publishes, pastes URL). Chat panel: on-device retrieval over 16 curated site facts (prices/quiz/€200/grants/GDPR/refunds/local-area/…), typing indicator, quick chips, human-handoff links (WA/SMS/mail), **EU-AI-Act disclosure in header + "I'm a bot" answer**. Zero data leaves the browser. `LEA_UPGRADE` marker in v4.js = swap point for real model (Vercel serverless `/api/lea` → Claude Haiku w/ site-KB system prompt; needs API key + GDPR processor note — post-launch).
- All validated: `node --check` ×2, HTML tag balance, CSS brace balance. Samuel must browser-check (sandbox can't render): cinema on desktop Chrome/Safari, flow on phone, Lea chat, lead form mailto.

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
