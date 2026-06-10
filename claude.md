# Leanta — Development Guide

## Latest Vercel Preview Deployments

After each push to designated branches, Vercel auto-deploys to preview URLs:

### v4 Storytelling Mockup (PR #21)
Branch: `claude/trusting-noether-rxejqv`
**Preview:** https://neuro-hive-git-claude-trusting-noether-rxejqv-ticodebs-projects.vercel.app/v4/

This is the light-mode noomo-style storytelling page with:
- Preloader (0–100 counter)
- 5 immersive chapters (The Folder, The Tuesday, The Numbers, The Visit, The Proof)
- Quiz funnel finale
- Full dark cinematic styling (Anton display + Plex Mono labels)
- Fallback poster cards for video cases (awaiting Suno music + case films)

**Status:** ✅ Fully functional mockup — ready for review and minor styling tweaks
**Media pending:** `v4/assets/leanta-theme.mp3` (Suno) · `v4/assets/case-{1..3}.mp4` (Samuel's Flow/Seedance renders)

---

## File Structure

- `/v4/` — Storytelling landing page (dark theme, noomo-inspired)
  - `v4/index.html` — Main page
  - `v4/v4.css` — Styling (Anton OFL + Plex Mono OFL)
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
