# Leanta — Development Guide

## Latest Vercel Preview Deployments

After each push to designated branches, Vercel auto-deploys to preview URLs:

### v4 Storytelling Mockup (PR #21)
Branch: `claude/trusting-noether-rxejqv`
**Preview:** https://neuro-hive-git-claude-trusting-noether-rxejqv-ticodebs-projects.vercel.app/v4/
(preloader plays once per session — open a private window to replay it)

**v4.3 — "THE DESCENT" (10/06, Samuel's second verdict — CURRENT):**
- Bright glassmorphism theme `#f2efe8`; dark theme + 3D shapes REMOVED entirely
  (no three.js, no CDN dependencies at all)
- Camera descends through three real environments (nano banana 2 pro backdrops,
  AI-tagged): retail shop → manufacturing floor → hotel lobby; sticky layers,
  backdrop pan + blur-out on exit, floor-indicator elevator on the right
- Each environment: glass card with sector pains, CTA + lead magnet, and a
  companion picker (Lea sprout · Penny fox · Mossy sheep) — the chosen pet
  rides the Lea chat orb; `LEANTA.ommaPetUrl` still overrides with Omma scene
- "THE LOGIC, UNFOLDED" — SVG mind map that unfolds in steps (why-yes logic)
- Pricing section: WITH the grant (€200, credited) vs WITHOUT (quote first)
- Brand: glyph in single emerald accent, thinner handwritten "agency",
  frosted brandpill (always legible on any contrast), typewriter hero line
- Asset slots still auto-activate: `leanta-theme.mp3` (Suno) ·
  `case-{1..3}.mp4` · Omma pet URL — see `v4/assets/MEDIA_BRIEFS.md`

v4.2 — vivid pass + Valentime motion (10/06, superseded same day):
- Palette brightened: neon mint `#00f07a` · signal yellow `#f5c400` · electric
  violet `#8d5cff` accent (preloader + brand glyph)
- Brand: Bebas Neue wordmark + handwritten Caveat "agency" signature; the final
  A of LEANTA replaced by the crossbar-less **ascent glyph** (inline SVG —
  future standalone logo candidate)
- Valentime (noomo) camera pacing: 1100vh runway, per-station dwell easing
  (camera arrives → rests → departs), blur-fade panel choreography, gradient
  hairline + diamond text framing, radial-mask preloader reveal
- New movement: magnetic pull on buttons/chips/glass panels, char-stagger
  chapter titles, breathing hero wordmark
- Lights-up ending: finale + lead-catcher flip to gallery light `#e8e8e6`
  (awwwards screenshot treatment) before handing off to the light store pages
- `v4/assets/img/bg-loop.mp4` slot added — Higgsfield ambient loop auto-fades
  behind the WebGL scene when the file lands (see `v4/assets/MEDIA_BRIEFS.md`)

v4.1 — full noomo architecture (10/06):
- Fixed three.js scene + 760vh scroll runway: cinematic camera flies a spline
  through 5 stations (hero → paper-storm chaos → ordered grid → KPI bars →
  gold portal); glass panels fade/slide along the way; mouse parallax
- Glassmorphism cards, scroll-progress hairline, preloader, custom cursor
- Sound toggle ALWAYS visible — WebAudio ambient pad now, auto-swaps to
  `v4/assets/leanta-theme.mp3` when the Suno track is dropped in
- Lead-catcher form (mailto/WhatsApp/SMS compose — nothing posted by the page)
- LEA pet assistant: animated SVG pet (or Omma/Spline embed via
  `LEANTA.ommaPetUrl` in assets/checkout-config.js) + on-device retrieval chat
  with EU AI Act disclosure; `LEA_UPGRADE` marker = real-model swap point
- Mobile / reduced-motion / no-WebGL / no-JS ⇒ readable flow-mode document

**Status:** ✅ Fully functional mockup — needs Samuel's browser check
**Media pending:** `v4/assets/leanta-theme.mp3` (Suno) · `v4/assets/case-{1..3}.mp4` (Flow/Seedance) · Omma pet URL

---

## File Structure

- `/v4/` — Storytelling landing page (dark theme, noomo-inspired)
  - `v4/index.html` — Main page
  - `v4/v4.css` — Styling (Bebas Neue OFL + Caveat OFL + Plex Mono OFL)
  - `v4/v4.js` — Preloader, cursor, sound toggle, scroll choreography
  - `v4/assets/fonts/` — Self-hosted OFL fonts
  - `v4/assets/img/` — Chapter backdrops (CSS gradients + SVG grain fallback)

- Main site (light cream theme, /assets/leanta.css):
  - `index.html` — Store landing
  - `quiz.html` — Free readiness check
  - `grants.html` — €200 grant pathway
  - `products/` — Product pages
  - `services.html` — Agency arm

---

## Development Notes

### PR #21 (v4 Mockup)
- Branch base: `claude/vigilant-bell-sn55pv` (launch branch)
- Status: Draft PR, ready for design review
- Design system: Dark canvas (#0b0d0c) + emerald (#1db887) + gold (#e7cd72)
- Type scale: 15vw hero, 7.5vw section titles, 13px mono labels
- Motion: GSAP ScrollTrigger + Lenis smooth scroll (pinned chapters on desktop, static on mobile)
- Fallbacks: Full-featured no-JS experience, reduced-motion safe, no CDN dependencies except GSAP/Lenis (pinned versions)

### Deployment Notes
- Vercel deploys to `neuro-hive` (production) and PR preview URLs automatically
- Netlify deploys to `graceful-toffee-4a8918` with matching PR previews
- `.vercelignore` and `netlify.toml` block `/asset-forge` (paid files) and project internals
- Both hosts serve `/v4/` correctly once this PR merges

---

## Next Steps (Post-Launch)

1. Samuel provides Suno-generated track → drop into `v4/assets/leanta-theme.mp3`
2. Samuel renders 3 case-film videos (Flow/Seedance) → drop into `v4/assets/case-{1..3}.mp4`
3. Higgsfield chapter backdrops (optional) → drop into `v4/assets/img/` (CSS gradients work until then)
4. Browser check on desktop + mobile (sandbox cannot render)
5. Decide: merge /v4 as-is, or revisit dark-only vs. hybrid design decision

---

## Links

- Marketing plan: `marketing/GROWTH_INITIATIVES_PLAN.md`
- Sales playbook: `marketing/SALES_PLAYBOOK.md`
- Preliminary client research: `forms/CLIENT_PRELIM_RESEARCH.md`
- Asset-forge state: `asset-forge/handover.md`
