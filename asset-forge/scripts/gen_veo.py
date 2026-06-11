#!/usr/bin/env python3
"""
ASSET-FORGE — Gemini Veo image-to-video generator for v4 backdrop loops.

Reads GEMINI_API_KEY from env or asset-forge/.env (git-ignored).
Animates an existing still into a short looping clip, writes to the slot path.
The v4.js mountLoop() auto-replaces the still with `<basename>-loop.mp4` the
moment that file exists — so dropping the MP4 in is the whole wire-up.

Usage:
  python3 asset-forge/scripts/gen_veo.py --list
  python3 asset-forge/scripts/gen_veo.py bg-street bg-retail bg-factory bg-lobby
  python3 asset-forge/scripts/gen_veo.py --all
"""
import base64, json, os, sys, time, urllib.request, urllib.error

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODEL = os.environ.get("VEO_MODEL", "veo-3.0-fast-generate-001")
DURATION = 8  # seconds — Veo 3 fast requires 4-8s; 8s gives a longer loop
ASPECT = "16:9"
BASE = "https://generativelanguage.googleapis.com/v1beta"

# Brief §4.1 — each entry: still path → output loop path → motion prompt.
SLOTS = {
    "bg-street": (
        "v4/assets/img/bg-0-street.jpg",
        "v4/assets/img/bg-0-street-loop.mp4",
        ("Irish small-town street, bright morning: awning edge breathing in "
         "wind, one cyclist crossing as motion blur, cloud light shifting "
         "slowly across the cream shopfronts, a dog's tail flicking at the "
         "frame edge. Locked-off camera, subtle micro-motion only, photoreal, "
         "warm bright grade, emerald accents preserved, no readable text."),
    ),
    "bg-retail": (
        "v4/assets/img/bg-1-retail.jpg",
        "v4/assets/img/bg-1-retail-loop.mp4",
        ("Bright Irish retail shop interior: shelf banner swaying gently, the "
         "fridge door reflecting a passer-by once, a price tag fluttering, "
         "dust motes drifting in the window light, one customer drifting "
         "through the background as motion blur. Locked-off camera, subtle "
         "motion only, photoreal warm bright grade, emerald accents preserved, "
         "no readable text."),
    ),
    "bg-factory": (
        "v4/assets/img/bg-2-factory.jpg",
        "v4/assets/img/bg-2-factory-loop.mp4",
        ("Small clean Irish food-production floor: a conveyor cycling slowly, "
         "a pneumatic arm settling every two seconds, emerald status LEDs "
         "blinking, a wisp of steam from a kettle vat, a hi-vis worker "
         "passing far behind a frosted strip-curtain. Locked-off camera, "
         "subtle motion only, photoreal warm bright grade, emerald accents "
         "preserved, no readable text, no faces."),
    ),
    "bg-lobby": (
        "v4/assets/img/bg-3-lobby.jpg",
        "v4/assets/img/bg-3-lobby-loop.mp4",
        ("Warm small Irish hotel lobby: a key-fob light blinking at "
         "reception, lift doors opening once to warm light, plant leaves "
         "stirring softly under air-conditioning, a guest with a rolling "
         "case passing through as motion blur, brass fixtures catching "
         "moving daylight. Locked-off camera, subtle motion only, photoreal "
         "warm bright grade, emerald accents preserved, no readable text."),
    ),
}


def load_key():
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if k:
        return k
    p = os.path.join(REPO, "asset-forge", ".env")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def http(url, data=None, method=None, timeout=60):
    req = urllib.request.Request(
        url,
        data=(json.dumps(data).encode() if data is not None else None),
        headers={"Content-Type": "application/json"} if data is not None else {},
        method=method or ("POST" if data is not None else "GET"),
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def submit(still_abs, prompt, key):
    img_b64 = base64.b64encode(open(still_abs, "rb").read()).decode()
    body = {
        "instances": [{
            "prompt": prompt,
            "image": {"bytesBase64Encoded": img_b64, "mimeType": "image/jpeg"},
        }],
        "parameters": {
            "aspectRatio": ASPECT,
            "durationSeconds": DURATION,
            "personGeneration": "allow_adult",
        },
    }
    url = "%s/models/%s:predictLongRunning?key=%s" % (BASE, MODEL, key)
    res = http(url, body, timeout=60)
    return res.get("name")


def poll(op_name, key, max_wait=600):
    """Returns the finished operation payload, or None on timeout."""
    deadline = time.time() + max_wait
    every = 8
    url = "%s/%s?key=%s" % (BASE, op_name, key)
    while time.time() < deadline:
        try:
            r = http(url, timeout=30)
        except urllib.error.HTTPError as e:
            print("    poll error:", e.code, e.read()[:120].decode("replace"))
            time.sleep(every); continue
        if r.get("done"):
            return r
        time.sleep(every)
    return None


def download_video(op_payload, out_abs, key):
    # Veo returns the video in operation.response.generateVideoResponse.generatedSamples[].video.uri
    # OR (older format) operation.response.predictions[].videoUri/bytes — handle both.
    resp = op_payload.get("response") or {}
    # Try nested structures first
    candidates = []
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("uri", "videoUri") and isinstance(v, str) and v.startswith("http"):
                    candidates.append(("uri", v))
                if k in ("bytesBase64Encoded", "videoBytesBase64Encoded") and isinstance(v, str):
                    candidates.append(("b64", v))
                walk(v)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(resp)
    if not candidates:
        return False, "no video in response: " + json.dumps(resp)[:200]
    kind, val = candidates[0]
    os.makedirs(os.path.dirname(out_abs), exist_ok=True)
    if kind == "b64":
        open(out_abs, "wb").write(base64.b64decode(val))
    else:
        # signed URL — append key if it's a Google API URL
        url = val + ("&" if "?" in val else "?") + "key=" + key
        with urllib.request.urlopen(url, timeout=180) as r:
            open(out_abs, "wb").write(r.read())
    return True, os.path.getsize(out_abs)


def main():
    args = sys.argv[1:]
    if not args or "--list" in args:
        print("Available slots (Veo image-to-video, %ds %s):" % (DURATION, ASPECT))
        for name, (still, out, _) in SLOTS.items():
            print("  %-12s  %s  ->  %s" % (name, still, out))
        return
    if "--all" in args:
        args = list(SLOTS.keys())
    key = load_key()
    if not key:
        print("No GEMINI_API_KEY found."); sys.exit(1)

    # phase 1: submit all in parallel (Veo runs them long-running)
    jobs = []
    for name in args:
        if name not in SLOTS:
            print("Unknown slot:", name); continue
        still, out, prompt = SLOTS[name]
        still_abs = os.path.join(REPO, still)
        if not os.path.exists(still_abs):
            print("  ✗ %s: still missing %s" % (name, still)); continue
        try:
            op = submit(still_abs, prompt, key)
        except urllib.error.HTTPError as e:
            print("  ✗ %s submit HTTP %s: %s" % (name, e.code, e.read()[:300].decode("utf-8", "replace"))); continue
        print("  ↑ %s submitted -> %s" % (name, op))
        jobs.append((name, op, out))

    # phase 2: poll each to completion
    for name, op, out in jobs:
        print("  … polling %s" % name)
        r = poll(op, key)
        if not r:
            print("  ✗ %s timed out" % name); continue
        if r.get("error"):
            print("  ✗ %s error:" % name, r["error"]); continue
        ok, info = download_video(r, os.path.join(REPO, out), key)
        if ok:
            print("  ✓ %s wrote %s (%d KB)" % (name, out, info // 1024))
        else:
            print("  ✗ %s: %s" % (name, info))


if __name__ == "__main__":
    main()
