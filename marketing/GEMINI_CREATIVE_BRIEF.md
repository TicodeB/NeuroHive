# LEANTA — Creative-Asset Brief for Gemini (Flash 3.5 multimodal)
10/06/2026 (rewritten same day for **v4.3 "THE DESCENT"** — the dark v4.1/4.2
prompts are obsolete). Canon: `v4/NORTHSTAR.md` · state: `../asset-forge/handover.md`.
Owner: Samuel. Paste §1 into EVERY Gemini session first, then the task prompt.

---

## 1. BRAND DNA (the paste-block)

> **Leanta** — operations & compliance toolkits + a Lean·AI agency for Irish
> small businesses. Ferns, Co. Wexford + 30 km (Gorey, Enniscorthy, Bunclody,
> Camolin, Courtown). From the Irish *lean* — to continue, to follow through.
>
> **Voice:** calm, precise, honest; a craftsman, not a SaaS. Show, never hype.
> No invented numbers, no fake urgency, no stock-photo clichés.
>
> **Look (v4.3 "THE DESCENT", current):** bright gallery cream `#f2efe8`
> (secondary `#e9e5dc`), ink `#15181a`, **ONE accent: emerald `#0a8a52`** —
> nothing else carries colour. Frosted glassmorphism on everything that
> carries content. Barely-there paper grain. Awwwards-gallery calm:
> Valentime / jasminadenner / Google Stitch energy.
> **Type:** Bebas Neue (monumental display) · Caveat handwritten (thin,
> casual, small — the "agency" signature) · IBM Plex Mono (microcopy labels).
> **Brand mark:** the ascent-A glyph — LEANTA's final A with the crossbar
> removed, single emerald. Logo lives in a frosted pill, legible on anything.
>
> **The page story:** visitor lands on a bright Irish street (hero), then the
> camera DESCENDS floor-to-floor through three real rooms where boring work
> lives — retail shop → production floor → hotel lobby. Real premium
> generated environments (never procedural shapes), still until the mouse
> moves, then alive (parallax, drift, sweep). Every room sells: CTA + lead
> magnet + companion pet + honest pricing (with grant €200 / without).
>
> **Hard rules:** product screenshots = the REAL workbook, never generated ·
> real local logos only with the owner's written permission · every
> AI-generated/assisted asset is EU-AI-Act labelled (machine-readable mark +
> visible "AI-assisted" tag where shown) · people only as anonymous motion
> blur / backs, never recognisable faces · no readable invented text, no
> fake UI inside imagery.

## 2. WHAT GEMINI FLASH 3.5 DOES FOR US (the job summary)

1. **Image generation & editing (native):** environment stills (new sectors,
   seasonal variants), social/OG cards, Etsy–Gumroad listing graphics, A4
   poster art, logo-direction moodboards, companion-pet reference sheets —
   all palette-locked to §1.
2. **Motion-prompt drafting:** for each still it generates the matching
   **5-second loop prompt pack** (camera, motion layers, audio bed) that
   Samuel pastes into Google Flow / Veo / Higgsfield — Gemini doesn't render
   video here, it engineers the prompts and QCs the result frames.
3. **Asset QC (vision):** check delivered media against §6 (palette eyedrop,
   loop seam, faces, text artefacts, AI-tag presence) and return a pass/fail
   note per file.
4. **Derivatives:** crops (16:9 → 9:16 / 1:1), alt-text lines, compressed
   web variants ≤ 350 KB, poster frames from videos.
5. **Shot-list expansion:** turn `marketing/video_scripts.md` beats into
   per-shot Flow prompts (style block §4.4 appended to each).

## 3. CURRENT SLOT REGISTRY (don't re-make what's live)

| Asset | Status |
|---|---|
| `v4/assets/img/bg-0-street.jpg` hero + `bg-{1,2,3}` shop/factory/lobby | ✅ live (nano banana 2 pro) |
| `v4/assets/leanta-theme.mp3` + `leanta-focus.mp3` (Suno) | ✅ live, both modes |
| Nova companion (`v4/assets/omma/nova.glb`) + sprout/fox/sheep picker | ✅ live |
| `v4/assets/case-{1..3}.mp4` case films | ⏳ scripts ready (`video_scripts.md`) |
| Environment **loop videos** (animate the 4 live stills) + ambient audio | ⏳ THE priority |
| Local logos `v4/assets/logos/<slug>.png` | ⏳ permission-gated, never generated |

## 4. THE PROMPTS

### 4.1 Environment loop videos — animate the four LIVE stills
(Feed Gemini the existing jpg + this; it returns the Flow/Veo/Higgsfield
prompt tuned to that exact frame. Append to all: *"animate this exact image;
5-second seamless loop, first and last frame identical; locked-off camera;
subtle motion only; photoreal; keep the bright warm grade with emerald
accents; people only as soft anonymous motion blur; no readable text"*)

- **bg-0 street (hero):** "Irish small-town street, morning: awning edge
  breathing in wind, one cyclist crossing as motion blur, cloud light
  shifting slowly across shopfronts, a dog's tail at frame edge."
- **bg-1 retail shop:** "Shelf banner sway, fridge-door reflection of a
  passer-by, price tag fluttering once, dust motes in the window light,
  one customer drifting through background blur."
- **bg-2 production floor:** "Conveyor cycling slowly, pneumatic arm settling
  every 2 s, emerald status LEDs blinking, steam wisp from a kettle vat,
  hi-vis worker passing far behind frosted strip-curtain."
- **bg-3 hotel lobby:** "Key fob light blinking at reception, lift doors
  opening once to warm light, plant leaves stirring under aircon, guest
  with rolling case as blur, brass fixtures catching moving daylight."

### 4.2 Ambient audio beds (pair per loop; loopable 30–60 s, −20 LUFS, no
melody, no intelligible words — they sit UNDER the Suno theme, which ducks
them to 30% when both play)
- street: light wind, distant traffic swell, gull cry once, footsteps pass.
- shop: **human background murmur**, fridge hum, barcode beep twice, bag rustle.
- factory: rhythmic conveyor cycle, pneumatic hiss, forklift beep far away,
  low ventilation bed.
- lobby: soft murmur + cutlery clinks from a far room, lift chime once,
  page turn at reception.

### 4.3 New environment stills (only when a new sector page is needed)
Base: "Wide interior of {a small Irish café / trades workshop / B&B breakfast
room / pharmacy / butcher counter}, bright natural daylight, warm cream walls
`#f2efe8` undertone, one emerald `#0a8a52` accent object in frame, people only
as anonymous motion blur, photoreal editorial grade, generous negative space
upper third for glass card overlay, 16:9, no readable text, no faces."

### 4.4 Case-film style block (append to every Flow shot from video_scripts.md)
"Photoreal cinematic, warm bright Irish daylight grade with emerald `#0a8a52`
accent, shallow depth of field, no recognisable faces, no readable invented
text; on-screen tag 'AI-assisted production' in the first 3 seconds."
(Shots/beats + VO live in `marketing/video_scripts.md`; workbook close-ups are
REAL screen captures — never generated.)

### 4.5 Logo / brand moodboard (exploration only — mark is near-settled)
"Brand sheet on white: monumental Bebas-style 'LEANTA' where the final A has
NO crossbar (an ascent mark), single emerald `#0a8a52`; beneath it a thin,
casual handwritten word 'agency' in real-ink texture, small. 6 layout
variants: glyph alone · wordmark+glyph · frosted-glass pill lockup · favicon
crop · dark-on-cream · cream-on-photo. Flat, no 3D, no extra words."

### 4.6 Companion-pet reference sheet (look-lock for the picker pets)
"Reference sheet, transparent background, soft-3D toy-like mascots matching a
bright glassmorphism site: ① tiny emerald sprout-blob 'Lea', gold leaf
antenna ② copper fox 'Penny' ③ moss-green sheep 'Mossy' — each in 6 poses:
idle, blink, happy, talking, surprised, sleeping. Single emerald `#0a8a52`
accent details, warm soft shadow ellipse, no background scene, no text."
(Nova the Omma space-fox is live and stays as-is.)

### 4.7 Social / listing graphics
- **OG card 1200×630:** "Bright cream gallery banner, LEANTA wordmark with
  ascent-A in emerald, frosted glass strip with 'Pass the inspection. Know
  your numbers. Keep your evenings.', one real-environment photo strip along
  the bottom edge (street/shop/factory/lobby), grain, no other text."
- **Etsy/Gumroad listing hero 2000×1600:** "Cream studio tabletop, a laptop
  showing a SPACE LEFT BLANK screen (real workbook screenshot composited
  later — never generate UI), emerald glass paperweight, gold-free, soft
  daylight, generous margin for price badge."
- **A4 poster art:** existing layout `marketing/poster_a4.html` — Gemini
  supplies only the background wash: "very subtle cream paper texture with
  one emerald ink swash, 5% opacity, A4 portrait."

### 4.8 Suno (✅ DONE — kept for re-rolls only)
Ambient: "ambient cinematic instrumental, warm analog synth pads, 65 BPM,
subtle Irish folk inflection — distant low whistle and soft fiddle drone,
gentle felt piano, soft tape hiss, hopeful and calm, minimal percussion,
seamless loop, no vocals." · Focus: "focus-enforcing instrumental loop,
steady hypnotic 90 BPM eighth-note pulse, warm sub bass drone, repeating
pentatonic synth arpeggio, no melody changes, no drops, narrow frequency
band, lo-fi study meets minimal techno, deeply repetitive, seamless loop,
no vocals." Licence: confirm commercial use on the Suno plan pre-launch.

### 4.9 Omma (pet platform — 36 credits, spend ONLY on Samuel's OK)
Remix flow in `v4/assets/MEDIA_BRIEFS.md` §3; current default companion Nova
already self-hosted as GLB (iframe was blocked by frame-ancestors).

## 5. LOCAL-LOGO CAROUSEL — humans only
Real Ferns/Gorey/Enniscorthy businesses (e.g. Omni Pro, Ferns) appear as
typographic wordmarks until each owner's written permission exists; then
`v4/assets/logos/<slug>.png` swaps in. Copy says "the neighbourhood we
serve" + a visible non-endorsement line. Gemini never generates these.

## 6. DELIVERY CHECKLIST (Gemini runs this as QC on every file)
- [ ] Palette-true: bg reads `#f2efe8`-warm, accent is `#0a8a52` and ONLY that
- [ ] Loop seam invisible / audio loops without click
- [ ] No recognisable faces, no readable invented text, no fake UI, no logos
- [ ] EU AI Act: metadata mark + visible "AI-assisted" tag where shown
- [ ] Web weight: stills ≤ 350 KB, loops ≤ 8 MB (rural mobile)
- [ ] Filed at the exact path in §3 (slots auto-activate on file presence)
