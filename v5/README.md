# LEANTA v5 — the journey (scroll-to-fly WebGL)

Genuine 3D camera that flies forward through a spatial world as you scroll.
The page never moves vertically: a tall `#scroll-proxy` drives `progress`, and
the camera eases toward it (momentum, reverse, settle) via the BEATS config in
`v5.js`. Self-hosted three.js (r169, MIT, `vendor/`). No CDN.

## Architecture (config-driven, per the v5 brief)
- **BEATS** array in `v5.js` = the entire choreography. Each beat: `{ id, p,
  cam:{x,y,z}, accent, kicker, line, cta? }`. Camera smoothsteps between beats,
  so it slows/settles at each. A future world = a new BEATS array + object
  factory; the engine is untouched.
- **Roof-A portal**: extruded brand glyph (`makeA`) the camera flies THROUGH;
  fog warms + halo glows as you cross. A second distant A marks the next world.
- **Story objects**: accent-coloured groups (stone "four places", pink "echo
  messages", emerald "merged inbox") — placeholders to be replaced with real
  scene craft in the next phase.
- **Colour tokens** (`v5.css :root`): cream/ink/emerald foundation + pink
  (customers), orange (offers/urgency), mint (guidance), stone (neutral).
- **Compass** nav (bottom-left pip → journey map) replaces the floor elevator.
- **Fallbacks**: no-WebGL → readable `#nowebgl` doc; reduced-motion → scene
  cuts (snap to nearest beat, no flight); no-JS → `<noscript>`.

## Status
✅ Milestone 1: scroll-to-fly camera + roof-A portal flythrough proven
   (Playwright/headless, swiftshader). Hero, beats, compass, fallbacks wired.
⏭ Next: real Retail-World scene craft (replace placeholder panels), companion
   guides, offer (orange) scene, mobile tuning, contact endpoint, services room.
