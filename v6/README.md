# LEANTA v6 — "THE JOURNEY"

v5's scroll-to-fly WebGL camera carrying v4's real microsite content.

## The fusion model
- **Engine (from v5):** a fixed WebGL canvas — ordered dot lattice, roof-A
  portals you fly through, light-speed warp streaks on acceleration, per-world
  atmospheric grade. Scroll UP = fly forward (the journey is an ascent); a tall
  `#scroll-proxy` drives an eased, frame-rate-independent camera (momentum,
  reverse, settle at each beat).
- **Content (from v4):** the real glass-card microsites ride on top as crisp
  screen-space `.scene` panels, revealed as the camera settles at each beat —
  real fonts (Bebas/Caveat/Plex), copy, links, the mind map, pricing, the LEA
  chat and companions, the lead form. No blurry canvas text.
- **Worlds:** Atrium → Shops → Trades → Manufacturing → Farmers → Schools →
  Doctors & Dentists → the €200 Grant → THE LOGIC UNFOLDED → Would you pass?
  Each has its accent (pink/orange/mint/em), portal, pain-line and CTA.

## Ported v4 systems
- **LEA** — on-device KB chat, EU-AI-Act disclosure, browser voice (off by
  default), companion pets (Lea sprout · Penny fox · Mossy sheep) with moods.
- **Sound** — ambient + ADHD-focus mp3 tracks with a WebAudio pad fallback,
  OFF by default.
- **Lead form** — composes a message in the visitor's own mail app; never posts
  data anywhere. The email address is assembled at runtime, not a scrapeable
  literal in the source (a real server endpoint is the proper fix — see below).

## Fallbacks
- **No-WebGL** → `static-doc`: the same scenes become a readable stacked page.
- **No-JS** → identical readable stacked page (progressive enhancement).
- **Reduced-motion** → scene cuts instead of camera flight.

## Config-driven
The whole choreography is the `BEATS` array in `v6.js` + the `.scene[data-p]`
markers in the HTML. A new world = a new beat + a new `.scene` — the engine is
untouched. This is the seam a future Ferns-business personalisation hooks into.

## TODO (next)
- Server-side `/api/lead` + `/api/lea` (real anti-scrape + live model). The
  `LEA_UPGRADE` marker in v6.js is the swap point.
- Avatar voice upgrade (browser TTS now; premium voice needs a key).
- Per-world scene craft / Ferns photography personalisation layer.
- Twilio text-us + scheduler in the Grant world (needs Samuel's creds).
