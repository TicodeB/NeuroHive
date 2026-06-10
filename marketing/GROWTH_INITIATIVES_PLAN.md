# Leanta — Growth Initiatives Plan (10/06/2026)

Captures every initiative Samuel raised on 09–10/06 so nothing is lost between
sessions. Each item: what it is → status → next smallest action. Companion docs:
`SALES_PLAYBOOK.md` (launch week) · `FLYWHEEL_MOAT_STRATEGY.md` (the flywheel —
**it lives here in `marketing/`**) · `../asset-forge/handover.md` (state).

---

## 1. Local-first: NACE-classified businesses, Ferns + 30km

**The strategy.** Before chasing the whole Irish market, own the radius we can
drive: Ferns → Enniscorthy (~12km), Bunclody (~17km), Gorey (~20km), Camolin,
Ballycanew, Oulart, Courtown (~22km), Carnew (Co. Wicklow), northern edge of
Wexford town (~30km). Pipeline: **registered businesses → cluster by NACE →
shared processes first (every business does finance/HR/scheduling/compliance) →
enrich per industry → pain points → use cases → demonstration assets that
convert** (see §2).

**Status:** two research agents were dispatched 09/06 but died on a session
limit before doing any work — the systematic landscape pass is still OPEN.
Direct search confirmed the data sources: CSO Business Demography (county-level
active enterprises by NACE), CRO registers, Wexford County Development Plan
2022–2028 monitoring reports, LEO Wexford, commercial directories.

**What we already have:** `asset-forge/intelligence.db` maps 4 verticals of
processes/assets/pain points, and `v_universal_core` lists the cross-industry
MUST-haves — top of list: H&S Risk Assessment & Safety Statement (21 business
types), Fire Safety Register (17), HACCP system (10), Cleaning schedule (10),
Supplier traceability (10), Allergen matrix (8), Temperature log (8). These ARE
the "same for all" processes — the local cluster map plugs into them.

**Next smallest action:** re-run the two research agents (prompts preserved in
session log), output `asset-forge/research/local_ferns_30km.md` + a
`local_targets` DB table (name, town, NACE, cluster, source).

## 2. Demonstration selling — "old way / new way / outcome"

The conversion mechanism: don't claim, **show**. We validate our skill by
rebuilding a real process in front of the buyer; they feel the pain leave.

- **Shipped 10/06:** "The old way vs. the Leanta way" section on the homepage;
  dashboard showcase ("insight, not decoration" + prescribed actions on every
  tile); comms section (text us, we reply AND action); grant pathway page.
- **Per-cluster demo videos (60–90s, vertical):** old way (paper, retyping,
  panic) → new way (workbook/automation) → outcome stated honestly (time per
  task, not invented revenue claims). One per local cluster, café first.
- **Sales ideas (ranked):**
  1. **Process Makeover demo** — film ONE real local process redone; the video
     is both proof and ad. CTA: free process audit / €15–69 pack tripwire.
  2. **Named-neighbour case studies** (with permission) — in a 30km radius,
     recognition converts better than any ad.
  3. **Walk-in + phone demo + A4 poster QR** (already in SALES_PLAYBOOK §1/§4).
  4. **"We run on our own tools"** — show Leanta's own dashboard publicly.
  5. **Seasonal hooks** — inspection cycles, Christmas menus → allergen matrix,
     year-end → cashflow pack.

## 3. Explainer videos — production pipeline

Samuel will render in **Google Flow / AI Studio 2.0** (+ Higgsfield Seedance for
b-roll, ElevenLabs voiceover, HeyGen avatar where useful). Claude's job:
scripts + shot lists + prompts. **First three scripts to write next session:**
café compliance (P1), trades quote/invoice, retail till reconciliation.
Format per video: HOOK (the pain, 5s) → OLD WAY (15s) → NEW WAY on screen
(25s) → OUTCOME + CTA (10s). Voiceover EN (SK variant after native pass).
**EU AI Act note:** synthetic/AI-generated video and avatar content must be
machine-readable-marked and, where realistic humans appear, disclosed —
build the "Made with AI assistance" tag into the template, verify current
obligations at publish time.

## 4. Image/asset generation prompts (Seedance 2.0 · Nano Banana 2 · Wan/Qwen)

Brand prompt base (no AI slop rule): *"Minimal premium still-life on warm cream
(#faf6ee), deep emerald glass object + small gold accent, soft studio light,
generous negative space, no text, no people, no fake UI, editorial photography
grade, 3:2"*. Variants: hero abstract (glass icosahedron), per-vertical icons
(chef's pass, toolbox, shop counter — same palette), poster background.
**Rule: generated imagery is decoration only — every screenshot of a product
must be REAL (the actual workbook), never generated.** That's the no-slop line.

## 5. Website v3 (SHIPPED 10/06) + external design pass

Shipped: three.js 3D hero (emerald glass icosahedron + gold torus knot +
satellites; mouse parallax, scroll parallax, card tilt; reduced-motion safe,
CSS-orb fallback, DPR-capped) · reworked logo (rising-check mark, applied
site-wide via CSS) · old/new section · dashboard showcase · comms strip ·
grants.html funnel · payment trust footer on all 12 pages · LSS method section.

**External design-tool prompt** (paste into v0.dev / Lovable / Figma Make /
"omma.ai" if that's the service — Samuel to confirm the name):

> Redesign leanta.ie, a premium one-person Irish consultancy + digital-products
> studio. Aesthetic: Gamma-deck editorial perfection — warm cream (#faf6ee)
> background, deep emerald (#0b5d44) + muted gold (#c9a227) accents, large
> serif display headings, generous whitespace, glassmorphism cards with 1px
> emerald borders, soft layered shadows, subtle 3D glass objects in the hero,
> NO dark backgrounds, NO stock photos, NO generic AI imagery. Tone: calm,
> precise, trustworthy — a craftsman's site, not a SaaS template. Sections:
> hero with one sentence of value + 2 CTAs; "old way vs new way" comparison;
> product cards (€15–69 one-time workbooks); a realistic spreadsheet dashboard
> render with traffic-light KPIs that each prescribe an action; grant-funded
> agency pathway (€200 start); async-contact section (text/email, no calls);
> honest fine print. Typography: Georgia/serif display + system sans body.
> Accessibility AA, reduced-motion variants, mobile-first.

## 6. "Once-off → repeatable": the monthly drop

Convert one-time buyers into recurring relationships **without breaking the
"one-time purchase, free updates" promise already published**:
- **Leanta Club (subscription, ~€9–12/mo or ~€79/yr):** a NEW spreadsheet/tool
  drops every month (the P3–P21 build queue = 12+ months of drops), plus the
  **researched-intelligence layer**: refreshed LEO/EU grant watchlist, standards
  updates (BRCGS Issue 10, ISO 9001:2026), local opportunity notes. Existing
  buyers keep their free regulatory updates — the Club adds NEW tools + intel.
- Mechanics: Lemon Squeezy subscriptions; drop = email + download. Start
  manual, automate later. **Decision needed: price point + name.**

## 7. Excel/Sheets add-in with embedded agent

Google Sheets version EXISTS (`asset-forge/apps_script/`, PR #16): menu,
morning briefing with deltas, append-only journal, grounded Gemini sidebar.
Excel route: **Office.js add-in** (free to build, distributable as sideload
file first, AppSource later) — same pattern: habit nudges, log updates,
document upload → cells. Roadmap after launch revenue, not before.
**Compatibility test matrix (manual, pre-listing):** every SKU opened in
Excel desktop (Win/Mac), Excel online, Google Sheets import, LibreOffice —
log result per sheet (formulas, CF, dropdowns, protection). Sandbox cannot do
this (no renderer); it's a Samuel-with-laptop job, checklist in §12 form pack.

## 8. Pack design v2 — "gamma-grade" (reference: Samuel's gamma.app deck link)

Target look: editorial cover sheet, palette-locked section headers, KPI cards,
generous spacing — `scripts/design_system.py` (premium-pack track) already
encodes most of this; apply it to P1/P2/P13 retroactively as v2.0 releases.
**Honest feasibility:** openpyxl writes native charts/CF fine; true pivot
tables + slicers and Power Query are unreliable to author programmatically —
the BI-flavoured SKU should be a **Power BI template (.pbit) + matching
spreadsheet** rather than faked pivots. "Action scripts/metas" = the Apps
Script add-on (exists) + documented macros. Embed the intelligence layer
(grants watchlist, standards calendar) as a maintained "00 Intel" sheet —
updated via the Club drops (§6).

## 9. Affiliate / hardware-margin arm (later phase — do not build yet)

Samuel's model: be the trusted local integrator; **affiliate/reseller** for
robotics, vision systems & sensors, technical/cleaning/scientific supplies,
food-grade chemicals & greases, machinery, geo tags, edu materials, ADHD/focus
aids. Sourcing via Accio/Alibaba where appropriate. Install ourselves only on
big projects; otherwise subcontract + commission.
**Guardrails before launch:** (a) recommend-first credibility — only products
we'd specify in an audit anyway; (b) disclose affiliate relationships on the
site (consumer law + trust); (c) food-grade chemicals/greases carry regulatory
duties (SDS, labelling) — affiliate-link only, never re-label or stock; (d)
start with 3–5 programmes max, tracked in the DB (`affiliates` table, later).

## 10. x402 / machine payments + token-bucket billing

Roadmap (footer already says "on the roadmap"): x402-style HTTP-payment
endpoint so agents/clients can pay per use from a prepaid token bucket when we
run AI work on their behalf. Practical sequencing: (1) launch revenue first,
(2) simple prepaid "automation hours/tokens" product on Lemon Squeezy, (3)
true x402 endpoint when there's actual machine-to-machine demand. NOT a
launch-week item; keep credit-card trust badges (done) — never raw card fields
(PCI scope stays with the MoR).

## 11. AI glasses for premises inspections

Use case: hands-free capture during audits (photos, voice notes, checklist
overlay) → faster preliminary research docs. **Honesty rule: we don't show
hardware we don't own.** Next action: pick + buy the actual unit (candidates:
Ray-Ban Meta class for capture vs RealWear class for industrial), THEN film a
real inspection segment and add a "How we inspect" section with OUR footage.
GDPR on-site: announce recording, no covert capture, client owns the footage.

## 12. Engagement paperwork (forms pack)

`forms/CLIENT_PRELIM_RESEARCH.md` created 10/06 — the mandatory pre-engagement
research doc: company snapshot, NACE, stakeholder map, process inventory, pain
hypotheses, estimated available cash, **grant-funding route (majority of
funding should come from schemes)**, data-safety note. Still to draft: on-site
audit checklist, engagement agreement skeleton (solicitor review), NDA,
compatibility test checklist (§7), fulfilment log.

## 13. Ideal persona — and why they should NOT buy

**Persona "Máire, 44"** — owner-operator, café/B&B/trade within 30km; 6 staff;
70-hour weeks; phone-first, hates calls mid-service; inspection anxiety is
episodic but sharp; €15–69 is impulse-band IF trust exists; will not learn new
software; trusts neighbours' word over ads.
**Why she buys:** removes a named dread tonight; one-time price; no
subscription trap; local person answers; text-first service; grant pathway
makes the bigger job feel free-ish.
**Why she rightly does NOT buy (and what we do):** "I have a folder" (→ €29
gap check, not argument) · "no time to even open Excel" (→ agency does it
with her on-site) · "free templates exist" (→ freshness/logic/bilingual/one-
system, said plainly) · "AI did this, it'll be generic slop" (→ real workbook
screenshots, named local references, human on the doorstep) · genuinely too
small/cash-tight (→ we SAY so — the refusal builds the referral).

## 14. Competitors

Samuel to paste his list (asked 10/06). Baseline scan queued with the §1
research agents: Irish HACCP/H&S consultancies selling templates, Etsy/
Template.net sellers, job-management SaaS (the complaints are our brief).

---

### Sequencing (recommendation)
**This week (launch):** playbook §1 unchanged — merge, private, KYC, listings,
posts. The new site v3 + grants funnel support it.
**Next 2 sessions:** §1 local research agents → local_targets list → §3 first
three video scripts → §13/§2 outreach begins on the 30km list.
**After first revenue:** §6 Club, §8 pack design v2, §7 add-in, then §9–§11.
