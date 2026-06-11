#!/usr/bin/env python3
"""
ASSET-FORGE — Gemini image generator (nano-banana / gemini-2.5-flash-image).

Reads GEMINI_API_KEY from the environment, or from asset-forge/.env
(git-ignored). NEVER hard-code the key here.

Prompts are the canon ones from marketing/GEMINI_CREATIVE_BRIEF.md, baked in
as named "slots" so output filenames land exactly where v4 expects them.

Usage:
  python3 asset-forge/scripts/gen_gemini.py --list
  python3 asset-forge/scripts/gen_gemini.py pet-sheet
  python3 asset-forge/scripts/gen_gemini.py logo-moodboard og-card
  python3 asset-forge/scripts/gen_gemini.py env-street env-shop      # re-roll stills
  python3 asset-forge/scripts/gen_gemini.py --prompt "..." --out v4/assets/img/foo.png

Notes:
  - Every Gemini image carries an invisible SynthID watermark (EU AI Act friendly).
  - Output is PNG (or whatever the model returns) written to the slot path.
  - Run from the repo root.
"""
import base64
import json
import os
import sys
import urllib.request
import urllib.error

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# Preference order: nano banana 2 pro first (matches the live env stills),
# then flash-image fallbacks if quota/availability bites.
MODELS = [
    os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3-pro-image"),
    "gemini-3.1-flash-image",
    "gemini-2.5-flash-image",
]
ENDPOINT_TPL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent"
)

# ---- baked prompt slots (verbatim from GEMINI_CREATIVE_BRIEF.md) -------------
SLOTS = {
    "env-street": (
        "v4/assets/img/bg-0-street.jpg",
        "16:9",
        "Wide exterior of an Irish small-town street on a bright clear morning, "
        "warm cream-toned shopfronts (#f2efe8 undertone), one emerald #0a8a52 "
        "accent (an awning or sign), people only as anonymous motion blur, "
        "photoreal editorial grade, generous negative space in the upper third "
        "for a glass card overlay, 16:9, no readable text, no faces.",
    ),
    "env-shop": (
        "v4/assets/img/bg-1-retail.jpg",
        "16:9",
        "Wide interior of a bright small Irish retail shop, warm cream walls "
        "#f2efe8 undertone, daylight through the window, one emerald #0a8a52 "
        "accent object, one customer as anonymous motion blur, photoreal "
        "editorial grade, generous negative space upper third for a glass card "
        "overlay, 16:9, no readable text, no faces.",
    ),
    "env-factory": (
        "v4/assets/img/bg-2-factory.jpg",
        "16:9",
        "Wide interior of a small clean Irish food-production floor, bright "
        "daylight, cream undertone #f2efe8, emerald #0a8a52 status LEDs as the "
        "single accent, a hi-vis worker far behind a frosted strip-curtain as "
        "motion blur, photoreal editorial grade, generous negative space upper "
        "third for a glass card overlay, 16:9, no readable text, no faces.",
    ),
    "env-lobby": (
        "v4/assets/img/bg-3-lobby.jpg",
        "16:9",
        "Wide interior of a warm small Irish hotel lobby / reception, bright "
        "natural daylight, cream walls #f2efe8 undertone, one emerald #0a8a52 "
        "accent object, brass fixtures, a guest with a rolling case as motion "
        "blur, photoreal editorial grade, generous negative space upper third "
        "for a glass card overlay, 16:9, no readable text, no faces.",
    ),
    "logo-moodboard": (
        "v4/assets/img/logo-moodboard.png",
        "4:3",
        "Brand sheet on white: monumental Bebas-style 'LEANTA' where the final "
        "A has NO crossbar (an ascent mark), single emerald #0a8a52; beneath it "
        "a thin, casual handwritten word 'agency' in real-ink texture, small. "
        "6 layout variants: glyph alone, wordmark+glyph, frosted-glass pill "
        "lockup, favicon crop, dark-on-cream, cream-on-photo. Flat, no 3D, no "
        "extra words.",
    ),
    "pet-sheet": (
        "v4/assets/img/pet-sheet.png",
        "16:9",
        "Reference sheet, transparent background, soft-3D toy-like mascots "
        "matching a bright glassmorphism site: (1) tiny emerald sprout-blob "
        "'Lea' with a gold leaf antenna (2) copper fox 'Penny' (3) moss-green "
        "sheep 'Mossy' - each in 6 poses: idle, blink, happy, talking, "
        "surprised, sleeping. Single emerald #0a8a52 accent details, warm soft "
        "shadow ellipse, no background scene, no text.",
    ),
    "og-card": (
        "v4/assets/img/og-card.png",
        "16:9",
        "Bright cream gallery banner 1200x630, LEANTA wordmark with an ascent-A "
        "in emerald #0a8a52, a frosted glass strip carrying 'Pass the "
        "inspection. Know your numbers. Keep your evenings.', one real-"
        "environment photo strip along the bottom edge (street/shop/factory/"
        "lobby), subtle grain, no other text.",
    ),
}


def load_key():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    env_file = os.path.join(REPO, "asset-forge", ".env")
    if os.path.exists(env_file):
        for line in open(env_file, encoding="utf-8"):
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def generate(prompt, out_rel, key, aspect="16:9"):
    body = json.dumps(
        {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"],
                "imageConfig": {"aspectRatio": aspect},
            },
        }
    ).encode("utf-8")
    data = None
    for model in MODELS:
        req = urllib.request.Request(
            ENDPOINT_TPL.format(model=model) + "?key=" + key,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")
            print("  … %s -> HTTP %s: %s" % (model, e.code, msg[:160]))
            continue
    if data is None:
        print("  ✗ all models failed")
        return False

    parts = (
        data.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [])
    )
    for part in parts:
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and inline.get("data"):
            raw = base64.b64decode(inline["data"])
            out_abs = os.path.join(REPO, out_rel)
            os.makedirs(os.path.dirname(out_abs), exist_ok=True)
            with open(out_abs, "wb") as f:
                f.write(raw)
            print("  ✓ wrote %s (%d KB)" % (out_rel, len(raw) // 1024))
            return True
    # no image -> surface any text the model returned (refusal / safety)
    txt = next((p.get("text") for p in parts if p.get("text")), None)
    print("  ✗ no image returned" + (": " + txt[:200] if txt else ""))
    return False


def main():
    args = sys.argv[1:]
    if not args or "--list" in args:
        print("Available slots:")
        for name, (path, _a, _p) in SLOTS.items():
            print("  %-16s -> %s" % (name, path))
        print("\nOr: --prompt \"...\" --out <path>")
        return

    key = load_key()
    if not key:
        print(
            "No GEMINI_API_KEY found.\n"
            "  Set it:  bash asset-forge/scripts/set_secret.sh GEMINI_API_KEY\n"
            "  or:      export GEMINI_API_KEY=AIza..."
        )
        sys.exit(1)

    if "--prompt" in args:
        prompt = args[args.index("--prompt") + 1]
        out = args[args.index("--out") + 1]
        print("Generating custom -> %s" % out)
        generate(prompt, out, key, "16:9")
        return

    ok = 0
    for name in args:
        if name not in SLOTS:
            print("Unknown slot: %s (try --list)" % name)
            continue
        path, aspect, prompt = SLOTS[name]
        print("Generating %s -> %s" % (name, path))
        if generate(prompt, path, key, aspect):
            ok += 1
    print("\nDone: %d/%d succeeded." % (ok, len([a for a in args if a in SLOTS])))


if __name__ == "__main__":
    main()
