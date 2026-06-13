# LEANTA v7 — WIREFRAME (low-fidelity blueprint)

Samuel's brief: keep ONLY the camera logic from v5, lose the v5 environment
grade washes, take everything else from v4, and prove the new ideas as a
wireframe before expensive production.

## What v7 proves (cheap, high-impact, built)
- **Unified particle grid, spectrum-coloured graphite → emerald → pink** by
  depth. Hover lifts a dot to the world accent, then it decays back to its
  spectrum colour. This grid is now the ONLY environment — the v5 colour-grade
  washes are dropped; the base is v4 cream.
- **Light-speed ray warp** between worlds: streaks elongate and cycle through
  graphite → emerald → pink during the jump, settling to the next world.
- **Hero = question hook + arc of CTA tiles.** "Would your business still run on
  Tuesday if you didn't show up?" pulls the eye; a bent-semicircle of animated
  world tiles each flies you there. Clear "scroll UP to begin" + "Choose
  companion" prompt.
- **Companion as navigator.** LEA's chips now PILOT the camera ("✈ Fly me to the
  €200 grant") with a witty line, as well as answering from the KB and handing
  off to a human. Voice = browser TTS (toggle in chat).
- **In-world side rail.** Right-edge menu present in every world: jump to any
  microsite, fast-forward / rewind a world, Basket, €200 grant.
- Camera logic, scenes, LEA, sound, lead form, fallbacks all carried from v6.

## Production stubs (labelled in the legend — next phases, not built)
- **[3D flying avatar]** — a rigged GLB companion that flies in the 3D scene
  (currently the cute 2D-SVG pet stands in). Needs GLTFLoader (self-hosted, no
  CDN) + an animation/voice budget call.
- **[changeover video]** — manual→automated case films drop into slots.
- **[water-glass slide]** — liquid-glass refraction transition between worlds
  (shader / displacement); currently a straight fade.

This is a BLUEPRINT for sign-off — fidelity is deliberately low. Once the layout
and interaction model are approved, production raises each piece to finish.
