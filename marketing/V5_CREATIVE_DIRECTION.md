# LEANTA v5 — Creative Direction & Implementation Plan
*11/06/2026 — answer to Samuel's "world-class creative director" brief.*

Read this before any code lands. Direction is decisive but the brief
explicitly says **"do not immediately replace the existing concept with
a generic redesign — build on the strongest ideas."** This memo says
what we keep, what we kill, and the sequence to rebuild in.

---

## 0. ONE THING TO RESOLVE BEFORE CODE

The brief says **"Reusable React components."** Leanta v4 is **vanilla
HTML/CSS/JS** — no React, no Vue, no bundler. Switching frameworks is a
2–3 day full rewrite that we don't need for this experience. **My
recommendation:** keep vanilla but honour the *spirit* of the brief with
**config-driven world modules + a small reusable system in plain ESM**:

- `worlds/<slug>/world.json` — config (title, scenes, palette, beats)
- `worlds/<slug>/scenes/*.html` — scene fragments
- `lib/journey.js` — camera, scroll progression, portal transitions
- `lib/voice.js`, `lib/sound.js`, `lib/guide.js` — orthogonal systems

A future business-specific Ferns experience replaces ONE JSON +
fragments. Same architectural goal, none of the framework cost.

I will assume vanilla unless Samuel overrules.

---

## 1. AUDIT — what's there now

### Strong, keep:
- **Cream `#f2efe8` + ink `#15181a` + single emerald `#0a8a52`** palette — restrained, locally warm, distinctive.
- **The ascent-A glyph** (crossbar-less roof-A) — already a recurring inline SVG; primed to become the spatial device the brief asks for.
- **The bg-loop videos just landed** (street/retail/factory/lobby — Veo) — environments now breathe.
- **LEA chat assistant** — on-device retrieval, EU-AI-Act disclosure, just gained a browser-voice button.
- **Companion pets** — Lea sprout / Penny fox / Mossy sheep (animated SVG with five expressions, chat-wired).
- **Mesh-dot field** with cursor swarm + Z-dolly (Canvas2D, lightweight) — alive without WebGL cost.
- **The understated copy voice** — "two-line wastage count," "Sunday evenings off the laptop."
- **The €200 grant pathway** — the most distinctive offer in our category.
- **The "stakes" line** I just added per env — keeps it.

### Wrong or generic, kill:
- **Hero overcrowding** — typewriter line + brand block + scroll-cue + dust-canvas + ascent-A glyph + sound toggle + brandpill all fighting in one frame. Brief: one invitation only.
- **Right-side `00 01 02 03` floor elevator** — exactly the "numbered list of sections" the brief rejects.
- **The handwritten "agency" under LEANTA** — brief: remove. Logo becomes wordmark alone.
- **Sticky-stack camera** — each env has a tiny per-pin Z-dolly, but **between rooms it's a card hand-off, not a continuous fly-through**. noomo uses 167 calls to THREE.js for a real spline-driven camera. Ours doesn't.
- **2D SVG pets** — I called them "soft-3D"; that was a stretch. They're stylised flat SVG.
- **Plain-text `hello@leanta.ie`** — appears in the HTML/JS as a scrapable `mailto:`. Samuel: "Don't reveal company email address, so it's not scraped." Fix: JS-rendered with anti-scrape splitting + a contact form posting to a serverless function.
- **No services pricelist on /v4** — brief now demands hard prices + value props.

---

## 2. CREATIVE DIRECTION — one sentence

> **A connected world of Irish small-business interiors, joined by the LEANTA roof-A as a portal — visitors travel forward, recognise themselves in short funny scenes, and find a calmer alternative on the other side of each threshold.**

Not a portfolio site. Not a brochure. A **spatial tour** of the boring
work — and the door out of it.

---

## 3. JOURNEY STORYBOARD — 7 beats

| # | Beat | Camera | What the visitor sees | What they feel |
|---|---|---|---|---|
| 0 | **Arrival** | Held wide, deep negative space | Cream void, a single distant ascent-A breathing emerald, mesh-dots drifting. Three controls: **Begin Journey · Choose Guide · Sound**. One line: *"Let the journey begin."* | Calm, curious. Confident this is something. |
| 1 | **First scroll = forward** | Slow dolly toward the A | A grows; mesh-dots part to let you through; sound of distant doors. | *"I'm moving INTO the screen, not down it."* |
| 2 | **The A becomes the door** | Pass through | The A's interior is a peek of the next world (Retail). Light-bleed transition; mesh thins to a single line. | Wonder. The A is a portal, not a logo. |
| 3 | **Retail World — Recognition** | Settles inside the shop | First scene fires: *"Have you got that thing my husband bought?"* — owner cycling through WhatsApp, Notes, a paper book. | Recognition. *"This is literally me on Saturday."* |
| 4 | **Retail World — Humor → Possibility** | Slow pan, 3 more scenes | Each: pain shown visually, one wry line of copy, then the calmer alternative (a clean dashboard tile, a record that kept itself). | Laughter, then *"…we could do that?"* |
| 5 | **Retail World — Invitation** | Pull back, A re-forms in distance | The €450 site inspection card surfaces; one CTA: *"Bring this calm to my shop."* The A reframes the scene like a doorway you walked through. | Ready. *"I want them to do this for me."* |
| 6 | **Forward** | Soft dolly to next A | Hospitality / Trades / Services / Manufacturing previewed as distant doorways. The visitor chooses which to enter, or returns to the Atelier (services + pricelist). | Sovereignty. Their tour, not ours. |

**Reversibility:** every beat reverses on scroll-up. Camera is not glued
to scroll position — it tweens toward a target the scroll updates,
inertia-smoothed (≈12 frames). Reduced-motion users get hard cuts and
fade-stills with no camera move.

---

## 4. THE ROOF-A AS SPATIAL DEVICE

Five usages, one symbol:

1. **Logo** — wordmark only, no "agency", larger, transparent, with a *subtle premium animation*: a single emerald light traces up the left side, across the apex, down the right (3.6 s loop). Pauses when idle, accelerates on hover.
2. **Hero glyph** — held alone in the void, big, breathing.
3. **Portal between worlds** — camera flies through the inside of the A; on the other side is the next interior.
4. **Distance marker** — far-away A glyphs hint at the next world before you reach it.
5. **Scene framing** — when a key story line lands, an A subtly frames the scene like a doorway.

It must read against cream, against photographic backgrounds, and at every
camera distance. The animation is restrained — never a stamp loop.

---

## 5. NAVIGATION — replaces the floor elevator

Right-side `00 01 02 03` strip → **dies**.

Replacement: a single discreet **"compass" pip** bottom-left that, when
hovered or focused, expands into a small radial menu of the worlds you've
visited + the Atelier + Conversation + voice/sound/motion preferences.
Visited worlds glow emerald; unvisited are ghost-outlined.

Keyboard: `?` opens the radial; arrows traverse; `Esc` closes. No
exposition. The pip is the only chrome at rest.

---

## 6. RETAIL WORLD — first deep world, 4 scenes

Each scene = single visual gag + single line + one prop change. NO paragraphs.

| Scene | Visual | Line | Calmer alternative shown |
|---|---|---|---|
| **A. "Have you got…"** | Customer at counter. Owner opens phone: 9 unread WhatsApps; Notes app; a paper book; the till. | "Saturday's busiest question is 'have you got…?' and the answer lives in four places." | A single search bar lights up. Stock + variants + last-sold-time appear. |
| **B. The ghost shop** | Google Maps with the shop's pin half-faded; a competing chain's pin glowing nearby. | "Twenty-three years on the street. Page two of Google." | A clean listing appears: hours, photos, 'open now', message button. |
| **C. The echo customer** | Same question typed into WhatsApp, Instagram DM, email, then asked on the phone. | "She asked you the same thing four ways. You answered four times." | One inbox merges the four; a draft reply autocompletes from the answer to the first one. |
| **D. The expired offer** | Owner finally posts the discount poster at 6pm. Discount ended at 5. | "If the offer's gone, the post is just an apology in disguise." | A scheduler appears: posts queue across channels with the discount's own clock attached. |

Each closes with the same beat: ascent-A reforms in the distance + a
single subtle line: *"This is one of the things Leanta sets up for you."*
The full pitch only lands at the end of the world.

Architecture: each scene = `worlds/retail/scenes/{a,b,c,d}.html` + a
camera waypoint. Adding scene E = drop a file in.

---

## 7. THE BIG 5 SERVICE PACKAGES — Atelier

Locked names + hard prices + itemised inclusions + outcome promise.
**Local-Ferns advantage** is the spine of every package: we drive out;
we sit at the counter; the same person who walked the floor stays the
contact; no offshore inbox.

### Entry — **Site Inspection & Automation Audit — €450**
*The decision-quality first visit. Required before any package.*
- 90-minute on-site walkthrough (Ferns + 30km, included; further on quote)
- Connected-assets inventory (every app, sheet, paper, channel)
- Top-3 leak map (what's costing time/money this month, in numbers)
- Specific automation recommendations, plain English, ranked by ROI
- Written report inside 5 working days
- **If you buy a package within 30 days, the €450 credits in full.**

---

### 1. **Pass-the-Audit Package — €890**
*Walk into the next inspection already ready. First-time-pass guarantee.*
- The Compliance Pack toolkit (HACCP, allergens, temps, fire, training)
- Records configured to your sector + your premises
- One mock inspection with the actual inspector's checklist
- A "fridge-door card" your team can follow in 30 seconds a shift
- Sector-specific add-on (food/care/hospitality/retail/manufacturing)
- 12-month regulatory updates, free
- **Outcome:** pass first time, no corrective-action letter — or we work free until you do.

### 2. **Money Plumber Package — €1,290**
*Find the leaks. Seal the leaks. Show the leaks on a tile.*
- Margin audit: till variance, wastage, GP%, labour %, supplier price drift
- Money-leak dashboard (every tile prescribes Monday's action)
- Two weeks of weekly leak reports + corrective sit-downs
- Two automated reorder triggers
- **Outcome:** identifiable monthly leak number sealed + 8–12 hours of admin saved per person per week — measured, not estimated.

### 3. **Customer Switchboard Package — €1,490**
*Every message answered within an hour, 6 days a week. From one inbox.*
- Unified inbox: WhatsApp + Instagram DM + email + form + missed calls
- AI-drafted reply suggestions on the top 20 questions for your sector
- Booking inbox + auto-confirmation + reminder
- After-hours auto-acknowledge with promise of next-morning reply
- Hand-off SOP (who answers what, when)
- **Outcome:** zero unanswered messages by 11am; measured weekly.

### 4. **Marketing Auto-Engine Package — €1,290**
*Three posts a week, automatic reviews, found by 'near me' search.*
- Local SEO setup (Google Business, citations, sector schema)
- Offer engine: discount → poster → schedule → post-everywhere → expire on its own
- Review collector (text after visit, one-tap rate, route to Google)
- Three scheduled posts per week from a quarterly content calendar
- Monthly visibility report (impressions, calls, route-clicks)
- **Outcome:** found on "near me," ≥10 new reviews/quarter, 3 posts/week with no owner thought.

### 5. **Admin Auto-Pilot Package — €1,090**
*The boring tasks run themselves. The owner just approves.*
- Invoice automation (raise, send, chase, mark paid)
- Roster + payroll prep
- Supplier-order templates with auto-fill from stock
- Booking → calendar → reminder → no-show recovery
- Approve-in-one-tap inbox
- **Outcome:** 6+ hours per week back, every week, from week two.

---

### **Add-ons (singles, no package required):**
- **Money Pulse** dashboard add-on — €390/quarter
- **Compliance refresh** — €290/year
- **Local content pack** (12 weeks of posts) — €490
- **GDPR + privacy hardening** — €390
- **VAT + accountant handoff workflow** — €290

### **Excel toolkit shop** (pre-existing, kept):
- Readiness Check €29 · Compliance Pack €34 · Operations & GP €49 · Pro Bundle €69 · single tools from €15
- These are the **DIY** tier. Packages above are **done-with-you**.

**Why these 5, not 8:**
*Legal / Financial Services packages get folded into Admin Auto-Pilot
add-ons — they don't have enough independent visible value to justify
their own door in the experience. The Big 5 each map to a recognisable
business pain the visitor will have lived this week.*

---

## 8. EMAIL ANTI-SCRAPE

Currently `hello@leanta.ie` is in `v4/v4.js` KB strings and `<a href="mailto:…">` — easy to scrape.

Fix:
- All visible "message us" buttons render via JS: `'hello' + String.fromCharCode(64) + 'leanta.ie'`.
- The chat KB stores the parts in a config, joins at runtime.
- The **lead catcher form** posts to `/api/lead` (serverless function) instead of opening `mailto:` — message goes to a private inbox we control.
- A WhatsApp Business number stays as the primary visible route (Samuel to provide).

---

## 9. IMPLEMENTATION SEQUENCE (auditable)

1. **This memo lands** — Samuel reviews, redirects, approves direction.
2. **Atrium + portal-A** — rebuild hero per beat 0 + 1 + 2 above. Kill scroll-cue, brandpill clutter, "agency" subscript, floor elevator.
3. **Logo system** — transparent SVG wordmark, no "agency", subtle traced-light A animation. Re-used as portal + scene framing.
4. **Camera & scroll engine** — inertial Z-dolly that tweens toward scroll-target; story beats as waypoints (settle, reveal, release). Reduced-motion fallback.
5. **Compass pip** navigation — replaces floor elevator.
6. **Retail World — 4 scenes** as described. Scene-config JSON + reusable scene component.
7. **Atelier (services + pricelist)** — the Big 5 page-as-room, hard prices, "what / outcome / why local Ferns" three-column for each.
8. **Online shop** — keep the existing `/index.html#products` for now; future merge into the journey as a "Shop World".
9. **Email anti-scrape** + serverless lead form.
10. **Accessibility + reduced-motion + mobile fallback + WebGL/audio graceful fallback**.
11. **Verify on desktop + mobile** + Playwright happy-path.

After each phase: coherence + perf check. If a phase introduces jank or
breaks the story arc, fix before next.

---

## 10. WHAT I NEED FROM SAMUEL BEFORE CODE

These are the only blockers; nothing else stops the rebuild:

- **OK on vanilla stack** (no React rewrite) — yes / no.
- **OK on the Big 5 + their prices** — or which to swap.
- **A WhatsApp number** for the visible-contact route (the email goes underground).
- **Permission to remove "agency" from the wordmark on the existing site too** (not just /v4), or scope it to /v4 only for now.
- **OK that the next push will look smaller on screen but be the foundation** — the Atrium rebuild + portal-A may briefly *reduce* visual content while the new architecture goes in, before Retail World fills it back up.

Everything else I'll just make the call on and ship.
