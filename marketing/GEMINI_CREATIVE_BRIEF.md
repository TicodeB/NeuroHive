# LEANTA — Creative-Asset Brief for Gemini (multimodal, Flash 3.5)
10/06/2026 · Owner: Samuel · Repo drop-paths included per asset.
Companion: `GROWTH_INITIATIVES_PLAN.md` §3–4 · `../asset-forge/handover.md` (state).

---

## 1. BRAND DNA (paste this block into every Gemini session first)

> **Leanta** — operations & compliance toolkits + a Lean·AI agency for Irish
> small businesses. Based in Ferns, Co. Wexford; serves the 30 km around it
> (Gorey, Enniscorthy, Bunclody, Camolin, Courtown). From the Irish *lean* —
> to continue, to follow through.
>
> **Voice:** calm, precise, honest, a craftsman not a SaaS. We show, we never
> hype. No invented numbers, no fake urgency, no stock-photo people.
>
> **Two visual worlds, one brand:**
> A) **Story world** (leanta.ie/v4 cinematic landing): near-black `#0b0d0c`,
> cream ink `#f5f1e6`, **emerald `#1db887`** (deep `#005a3c`), gold `#e7cd72`
> (money/premium lines ONLY), film grain, glassmorphism panels, giant
> condensed type (Anton), mono microcopy (IBM Plex Mono).
> B) **Commerce world** (store/quiz/grants): warm cream `#faf6ee`, emerald
> `#0b5d44`, muted gold `#c9a227`, serif display, glass cards, NO dark bg.
>
> **NEW accents (10/06 decision):** complementary energy pair —
> **ember `#ff6b35`** (hover/energy/highlights, story world) and
> **cobalt `#5468ff`** (reserved for LEA the mascot only). Bold is welcome;
> soup is not — emerald stays the brand anchor.
>
> **Logo direction (proposal in progress):** handwritten wordmark "Leanta",
> capital L, hard black on light / cream on dark (self-hosted Caveat Bold is
> the working face), optionally one accent stroke. NO category suffix (no
> "agency", no "storytelling" add-on next to the wordmark).
>
> **Hard rules:** every product screenshot is the REAL workbook — never
> generated. No people's faces. No fake UI. Real local logos only with the
> owner's permission. All AI-generated/assisted media must be EU-AI-Act
> labelled (machine-readable mark + visible "AI-assisted" tag where shown).

## 2. WEBSITE CONTEXT (so Gemini knows where assets land)

The /v4 cinematic page: fixed 3D scene, camera flies forward (z-axis) through
5 stations — HERO (emerald icosahedron) → 01 THE FOLDER (paper-storm chaos,
café kitchen at night) → 02 THE TUESDAY (papers settle into a grid, café
morning) → 03 THE NUMBERS (KPI bars, back-office) → 04 THE VISIT (gold portal,
rural road to the client) — then THE PROOF (case films), finale quiz CTA,
local-businesses carousel, lead form, giant footer. LEA, a pixel-art mascot,
accompanies the scroll and hosts the chat. Sound is opt-in; each environment
gets a 5-second ambient video loop + matching environment sound that activate
on mouse movement.

## 3. WHAT GEMINI FLASH 3.5 IS ASKED TO PRODUCE

| # | Asset group | Output | Drop path in repo |
|---|---|---|---|
| 1 | 5 environment loop videos (5 s, seamless) | 16:9 MP4, 1080p, loopable first↔last frame | `v4/assets/env/ch{1..4}.mp4`, `v4/assets/env/finale.mp4` |
| 2 | Matching ambient audio beds (loopable, -20 LUFS-ish, no melody) | 30–60 s MP3 | `v4/assets/env/ch{1..4}.mp3`, `finale.mp3` |
| 3 | Chapter backdrop stills (fallback posters for #1) | 16:9 PNG/WebP | `v4/assets/env/ch{1..4}.jpg` |
| 4 | Hero + section abstract stills (commerce world) | 3:2 PNG | `assets/img/` |
| 5 | Logo moodboard: handwritten "Leanta" explorations | PNG sheet, 6–9 variants | review only → final is hand-vectored |
| 6 | LEA expression reference sheet (pixel blob mascot) | PNG sprite sheet on transparent | reference only — shipped LEA is code-built SVG |
| 7 | Case-film b-roll beats (with Flow/Seedance via §3 scripts) | 9:16 + 16:9 MP4 | `v4/assets/case-{1..3}.mp4` |

NOT for Gemini: local business logos (real, permission-gated), product
screenshots (real workbooks only), final logo vector, Suno music (separate
brief below).

## 4. THE PROMPTS

### 4.1 Environment video loops (one prompt each; add to all:
*"5-second seamless loop, first and last frame identical, locked-off camera,
shallow depth of field, cinematic, photoreal, no people, no readable text,
no logos, muted near-black grade with emerald and warm amber accents,
film grain"*)

- **ch1 — café kitchen, night (THE FOLDER):** "Empty small-café kitchen at
  23:00, single warm under-shelf light, a worn ring-binder folder and loose
  paper sheets on a stainless counter, kettle steam drifting, slow dust
  motes, oppressive quiet."
- **ch2 — café floor, morning (THE TUESDAY):** "Bright small Irish café at
  07:45 before opening, espresso machine warming with gentle steam, chairs
  coming down off tables suggested by motion blur at frame edge, morning sun
  through window, fridge glow, calm and ready."
- **ch3 — back office / retail till (THE NUMBERS):** "Tiny back-office nook
  of a shop after close: laptop glow on a tidy desk, till drawer open with
  coins catching light, spreadsheet glow reflected on a glass, receipt spool
  gently swaying, emerald screen light vs warm lamp."
- **ch4 — the road out (THE VISIT):** "Rural Co. Wexford road at golden
  hour from a parked van's POV, hedgerows breathing in wind, distant farm
  gate, low sun flare, a feeling of going to help someone."
- **finale — workshop/manufacturing (THE PROOF):** "Small clean workshop /
  light manufacturing floor, one conveyor or pillar drill cycling slowly in
  soft focus, warning-stripe accents desaturated, motes in a shaft of light,
  emerald status LEDs blinking."
- **(retail variant, optional swap for ch3):** "Small-town shop floor mid-
  morning, shelves in soft focus, fridge doors reflecting movement outside
  the window, gentle banner sway over the till."

### 4.2 Ambient audio beds (pair to the loops; generate or source CC0)
- ch1: distant compressor hum, occasional page turn, clock tick, kettle
  ping once — lonely, quiet.
- ch2: espresso machine hiss, cup clinks, soft morning radio murmur (no
  intelligible words), door chime once.
- ch3: receipt printer chatter once, coin slide, keyboard taps, low PC fan.
- ch4: van engine idle then off, wind in hedgerows, distant birds, gravel
  underfoot once.
- finale/manufacturing: rhythmic conveyor cycle, pneumatic hiss every few
  seconds, **human background murmur** (retail-floor style), forklift beep
  far away once.
- Rule: loopable, no melody, no voices with words, sits UNDER the Suno theme
  (theme ducks env beds at 30% when both play).

### 4.3 Chapter backdrop stills — dark variant (poster fallbacks)
Base: *"Minimal premium still-life on near-black #0b0d0c, deep emerald glass
object + small gold accent, soft studio light, generous negative space, film
grain, no text, no people, no fake UI, editorial photography grade, 16:9"*
— one per chapter, swapping the object: ring-binder folder (ch1) · espresso
portafilter (ch2) · brass till coins stack (ch3) · van key on map (ch4) ·
machined gear (finale).

### 4.4 Commerce-world stills (light pages) — from plan §4
Base: *"Minimal premium still-life on warm cream #faf6ee, deep emerald glass
object + small gold accent, soft studio light, generous negative space, no
text, no people, no fake UI, editorial photography grade, 3:2"*. Variants:
hero glass icosahedron · chef's pass · toolbox · shop counter.

### 4.5 Logo moodboard (exploration only)
"Hand-written wordmark 'Leanta', capital L then lowercase, confident single-
stroke handwriting with real ink texture, hard black #141816 on white, 9
variations in a grid: 3 pen weights × 3 energy levels (calm, quick, bold).
Then one row repeated with a single accent: emerald #1db887 tittle, ember
#ff6b35 underline stroke, gold #c9a227 full-stop. Flat, no mockups, no 3D,
no extra words — the wordmark only." (NO 'agency'/'storytelling' suffixes.)

### 4.6 LEA expression reference sheet
"16-bit pixel-art mascot reference sheet, single cute rounded blob creature
with a tiny gold sprout antenna, big square eyes, on TRANSPARENT background,
cobalt blue #5468ff body with darker #2c3fa8 outline-shading, warm amber
ground-shadow ellipse. Grid of 8 poses/expressions: idle · blink · happy
(^-^) · talking (open square mouth) · surprised (O eyes) · thinking (eyes up
+ '…' pixels) · sleeping (-_- + zzz) · hatching from a cracked egg. Crisp
pixels, no anti-aliasing, no background scene." Repeat row 1 in 4 alt skins:
emerald #1db887 · ember #ff6b35 · gold #e7cd72 · orchid #c45ab3.
(Reference only — the production LEA is hand-coded SVG so skins are runtime-
switchable; this sheet locks the LOOK.)

### 4.7 Case-film beats (run §3 scripts through Flow/Seedance; Gemini drafts
shot lists). Format per film: HOOK pain 5 s → OLD WAY 15 s → NEW WAY on real
workbook screen 25 s → OUTCOME + CTA 10 s. Films: café compliance · trades
quote-to-invoice · shop till reconciliation. Every output carries the
machine-readable AI mark + visible "AI-assisted film · real workbook footage".

### 4.8 Suno music brief (NOT Gemini — kept here so all prompts live together)
"Instrumental, 90 s seamless loop, warm organic-electronic, soft felt piano +
analog pad + subtle Irish fiddle texture far in the mix, 70 bpm, no vocals,
no drops, contemplative but forward-moving, ends exactly as it begins."
Check the Suno plan covers commercial use. → `v4/assets/leanta-theme.mp3`.

## 5. LOCAL-LOGO CAROUSEL — rules (humans only, not Gemini)
Real businesses of Ferns/Gorey/Enniscorthy (e.g. Omni Pro in Ferns) appear as
typographic wordmarks until each owner's written permission for their actual
logo exists; then the PNG goes to `v4/assets/logos/<slug>.png` and swaps in
automatically. Carousel copy: "the neighbourhood we serve", never "clients",
with a visible non-endorsement line. Samuel confirms the name list.

## 6. DELIVERY CHECKLIST (every asset)
- [ ] Palette-true (eyedrop check against §1 hexes)
- [ ] Loop seam invisible (videos) / silence-free loop (audio)
- [ ] No people, no readable text, no logos, no fake UI
- [ ] EU AI Act: metadata mark + visible tag where the asset is shown
- [ ] Filed at the exact repo path in §3 (names are wired in code already)
