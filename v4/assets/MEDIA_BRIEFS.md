# v4 Media Production Briefs — Higgsfield · Suno · Omma
File slots are wired; each asset auto-activates the moment the file lands. No code changes needed.

## 1 · Environment loop videos (Higgsfield image-2 → video, or Flow/Veo)
⚠️ v4.3 update — the old dark abstract `bg-loop.mp4` brief is OBSOLETE (v4.2
dark theme). The job now: **animate the four LIVE nano-banana stills** so each
floor breathes on mouse-move, with matching ambient audio per environment.
**Drop at:** `v4/assets/img/bg-{0-street,1-retail,2-factory,3-lobby}-loop.mp4`
(+ optional `-amb.mp3` each). Wire-in note: next code session adds the
HEAD-check still→loop swap; files may land first.
**Spec:** 1920×1080 · 5 s seamless loop (first frame = last) · H.264 · ≤8 MB each.
**Prompts:** feed the existing jpg + the per-environment motion prompt in
`marketing/GEMINI_CREATIVE_BRIEF.md` §4.1 (street: awning breath + cyclist
blur · shop: banner sway + fridge reflection · factory: conveyor cycle +
emerald LEDs · lobby: lift doors + key-fob blink), all carrying: *"animate
this exact image, locked-off camera, subtle motion only, bright warm grade,
emerald #0a8a52 accents, people as soft anonymous blur, no readable text."*
**Ambient beds:** brief §4.2 — street wind · shop human murmur + barcode
beep · conveyor rhythm + pneumatic hiss · lobby murmur + lift chime. Loopable,
no melody; the Suno theme ducks them to 30% when both play.

## 2 · Suno (model v5.5) — TWO tracks, mode toggle is live on the page
The Music pill has an AMBIENT/FOCUS switch. Each file auto-swaps in when dropped:

**Track A — AMBIENT → `v4/assets/leanta-theme.mp3`** (~2 min, loopable, instrumental)
> Style: ambient cinematic instrumental, warm analog synth pads, 65 BPM, subtle Irish folk inflection — distant low whistle and soft fiddle drone, gentle felt piano notes, soft tape hiss, hopeful and calm, minimal percussion, seamless loop, no vocals

**Track B — ADHD FOCUS → `v4/assets/leanta-focus.mp3`** (~3 min, loopable, instrumental)
> Style: focus-enforcing instrumental loop, steady hypnotic 90 BPM eighth-note pulse, warm sub bass drone, repeating pentatonic synth arpeggio, no melody changes, no drops, no surprises, narrow frequency band, lo-fi study music meets minimal techno, deeply repetitive, seamless loop, no vocals

**Licence check:** confirm the Suno plan covers commercial use before launch.

## 3 · Omma — Lea pet (36 credits on the account — spend sparingly)
1. Open https://omma.build/community/i6ttegp2zyw1 in the logged-in account → Remix
2. Tint suggestion (keep cheap — one remix pass): body toward emerald #00f07a, accent #f5c400
3. Publish → copy the public scene URL
4. Paste into `assets/checkout-config.js` → `LEANTA.ommaPetUrl = "…"`
The floating orb swaps the built-in SVG pet for the Omma scene automatically.
**Budget guardrail:** pet first; nothing else until Samuel OKs further spend.
