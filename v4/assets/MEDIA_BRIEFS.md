# v4 Media Production Briefs — Higgsfield · Suno · Omma
File slots are wired; each asset auto-activates the moment the file lands. No code changes needed.

## 1 · Higgsfield — animated background loop
**Drop at:** `v4/assets/img/bg-loop.mp4` (the page HEAD-checks and fades it in behind the WebGL scene at 28% opacity; WebGL clear goes translucent automatically)
**Spec:** 1920×1080 · 10–20 s seamless loop · H.264 · keep under ~8 MB (rural mobile)
**Prompt:**
> Slow drifting abstract background, near-black green-tinted void (#0b0d0c), luminous neon-mint (#00f07a) light ribbons and soft volumetric glow, scattered signal-yellow (#f5c400) dust particles floating upward, subtle violet (#8d5cff) edge light, film grain, very slow camera drift, seamless loop, cinematic, no text, no people

## 2 · Suno — site theme
**Drop at:** `v4/assets/leanta-theme.mp3` (sound toggle auto-swaps from the WebAudio pad)
**Spec:** ~2 min, loopable (matching first/last bars), no vocals
**Prompt:**
> Ambient cinematic instrumental, warm analog synth pads, 65 BPM, subtle Irish folk inflection (distant low whistle or fiddle drone), soft tape hiss, hopeful and calm, minimal percussion, loopable, no vocals
**Licence check:** confirm the Suno plan covers commercial use before launch.

## 3 · Omma — Lea pet (36 credits on the account — spend sparingly)
1. Open https://omma.build/community/i6ttegp2zyw1 in the logged-in account → Remix
2. Tint suggestion (keep cheap — one remix pass): body toward emerald #00f07a, accent #f5c400
3. Publish → copy the public scene URL
4. Paste into `assets/checkout-config.js` → `LEANTA.ommaPetUrl = "…"`
The floating orb swaps the built-in SVG pet for the Omma scene automatically.
**Budget guardrail:** pet first; nothing else until Samuel OKs further spend.
