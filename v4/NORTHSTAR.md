# NORTHSTAR — what Samuel actually wants (read this BEFORE touching /v4)

## The storyline, in one paragraph

Samuel is building a launch site that has to feel like an **awwwards
Site-of-the-Day from a real agency** — noomo's Valentime, jasminadenner,
Google Stitch. A visitor arrives on a bright, gallery-calm page, the LEANTA
wordmark monumental and the handwritten "agency" beneath it, and then the
page takes them on a **journey through real places** — an Irish street, a
shop, a production floor, a hotel lobby — because those are the rooms where
Leanta's boring-work problem actually lives. Everything they see is **real
premium generated media** (Higgsfield image-2, nano banana 2 pro, Omma 3D,
Suno audio) — never procedural shapes, never coded approximations, never
empty placeholder slots. The page is **alive but disciplined**: assets sit
still until the mouse moves, then parallax and drift; text types itself;
the mind map draws itself; glass everywhere. And every room sells:
CTA + lead magnet + companion pet + honest pricing (with grant / without).
The visitor should leave thinking *"if their website works this hard,
imagine what they'd do for my Tuesday."*

## The ten commandments

1. **Premium media or nothing.** Samuel PAYS for Higgsfield (image-2), Suno,
   Omma, Gemini (nano banana 2/pro), GPT. When an asset is needed — generate
   it NOW with those. A placeholder is a failure; a brief is not a deliverable.
2. **No procedural decoration.** No particle storms, no wireframe solids,
   no generic three.js. Real environments with real people in motion blur.
3. **Bright + glassmorphism.** Cream gallery base, frosted glass on
   everything that carries content. Logo always legible (frosted pill).
4. **One accent colour.** Emerald. The ascent-A glyph is the brand mark.
   Handwritten "agency" — thin, casual, small.
5. **Camera flies FORWARD** into environments (dolly-in), descends floor to
   floor. Movement everywhere, but motivated movement.
6. **Still → alive on mouse.** Assets are calm photographs until the visitor
   moves; then they breathe (parallax, drift, sweep).
7. **Smart little animations.** Typewriter CTAs, self-drawing mind maps,
   bento hover lifts, green form ticks. Intelligence the visitor can feel —
   "appeal to the client's smartness."
8. **Every section sells, honestly.** CTA + lead magnet + pet picker per
   environment; pricing always shown with-grant AND without-grant; wishlist
   carousel labelled "not affiliations". Verbatim-honest, always.
9. **Capture is real.** Twilio SMS capture (api/capture.js), live beautiful
   forms, message-first. No lead ever lost (mailto fallback).
10. **When a tool is unreachable, say exactly which button Samuel must
    press** (connector name, where, what to click) — then keep building
    with what IS reachable. Never quietly downgrade to placeholders.

## Current asset registry (all auto-activate on file presence)

| Slot | Source | Status |
|---|---|---|
| `assets/img/bg-0-street.jpg` | nano banana 2 pro | ✅ live (hero) |
| `assets/img/bg-{1,2,3}-*.jpg` | nano banana 2 pro | ✅ live (descent) |
| `assets/leanta-theme.mp3` | Suno "Whistle Over Moss" 3:18 | ✅ live |
| `assets/leanta-focus.mp3` | Suno "Study Loop Drift" 3:28 | ✅ live |
| `assets/case-{1..3}.mp4` | Flow/HeyGen per video_scripts.md | ⏳ |
| `LEANTA.ommaPetUrl` | Omma remix of pink space-fox | ⏳ Samuel (36 credits) |
| Backdrop video loops | Higgsfield image-2 → video | ⏳ blocked: connector lacks generate tools — Samuel must reconnect the Higgsfield connector (Settings → Connectors → Higgsfield → reconnect/update) |
