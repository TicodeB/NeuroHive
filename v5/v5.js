/* ============================================================================
   LEANTA v5 — the journey engine.
   Genuine WebGL camera flying forward through a spatial world. The page never
   scrolls visually: a tall proxy element drives `progress`, the camera eases
   toward it (momentum, reverse, settle), and screen-space copy fades in at
   story beats. Reduced-motion → scene cuts. No-WebGL → readable fallback.

   Config-driven: BEATS defines the whole choreography. A future world is a new
   BEATS array + object factory — the engine doesn't change.
   ========================================================================== */
import * as THREE from "./vendor/three.module.js";

const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const COL = {
  cream: 0xf2efe8, creamWarm: 0xefe6d4, ink: 0x15181a,
  em: 0x0a8a52, pink: 0xe85a8a, orange: 0xe8843a, mint: 0x4fc99a, stone: 0x8a948e,
};

/* ---- JOURNEY CONFIG ------------------------------------------------------ */
/* p: 0..1 progress · cam: where the camera sits · copy: what settles in.
   Camera eases between beats with smoothstep, so it slows at each one. */
/* SEVEN WORLDS (Samuel 11/06): Shops on the Street → Trades → Manufacturing →
   Farmers (land & livestock) → Doctors & Dentists → the €200 Grant world.
   Retail is simply the first fully-dressed one — every world has its beat,
   accent, portal and pain-line; deep scene craft lands world by world. */
const BEATS = [
  { id: "atrium",  p: 0.00, cam: { x: 0,  y: 5, z: 92 },   accent: "em",
    kicker: "", line: "" },
  { id: "approach",p: 0.07, cam: { x: 0,  y: 4, z: 40 },   accent: "em",
    kicker: "", line: "" },
  { id: "portal",  p: 0.13, cam: { x: 0,  y: 3, z: -16 },  accent: "em",
    kicker: "Shops on the street", line: "Step inside the shop." },
  { id: "r-story1",p: 0.21, cam: { x: -6, y: 4, z: -74 },  accent: "stone",
    kicker: "The shop · Saturday", line: "“Have you got…?” — and the answer lives in four places." },
  { id: "r-story2",p: 0.29, cam: { x: 6,  y: 4, z: -132 }, accent: "pink",
    kicker: "The shop · the echo", line: "She asked the same thing four ways. You answered four times." },
  { id: "r-invite",p: 0.36, cam: { x: 0,  y: 5, z: -178 }, accent: "em",
    kicker: "The way out", line: "Records that keep themselves. Messages that answer once.",
    cta: { label: "See what Leanta sets up →", href: "/index.html#products" } },
  { id: "trades",  p: 0.45, cam: { x: -4, y: 4, z: -248 }, accent: "orange",
    kicker: "Trades people", line: "The van knows the job is done. The invoice finds out next month.",
    cta: { label: "Free 2-min readiness check →", href: "/quiz.html" } },
  { id: "mfg",     p: 0.54, cam: { x: 5,  y: 4, z: -318 }, accent: "mint",
    kicker: "Manufacturing", line: "The audit is a formality — or a fright. One folder decides which.",
    cta: { label: "Will you pass? →", href: "/quiz.html" } },
  { id: "farm",    p: 0.63, cam: { x: -5, y: 5, z: -388 }, accent: "orange",
    kicker: "Farmers · land & livestock", line: "Every field remembers. The notebook in the tractor doesn't.",
    cta: { label: "Free readiness check →", href: "/quiz.html" } },
  { id: "school",  p: 0.72, cam: { x: 5,  y: 4, z: -458 }, accent: "mint",
    kicker: "Schools & education", line: "Thirty permission slips went home. The term runs on chasing the one that didn't.",
    cta: { label: "Calmer school admin →", href: "/quiz.html" } },
  { id: "health",  p: 0.81, cam: { x: -4, y: 4, z: -528 }, accent: "pink",
    kicker: "Doctors & dentists", line: "Reception answers the same question forty times a week.",
    cta: { label: "A calmer front desk →", href: "/quiz.html" } },
  { id: "grant",   p: 0.90, cam: { x: 0,  y: 5, z: -598 }, accent: "em",
    kicker: "The €200 grant", line: "€200 mobilises it. The LEO carries its share. We do the paperwork.",
    cta: { label: "The grant pathway →", href: "/grants.html" } },
  { id: "end",     p: 1.00, cam: { x: 0,  y: 6, z: -645 }, accent: "em",
    kicker: "", line: "" },
];
const PORTAL_Z = -30;
/* a roof-A threshold stands before each world */
const WORLD_PORTALS = [
  { z: -218, scale: 1.2 },  /* trades */
  { z: -288, scale: 1.2 },  /* manufacturing */
  { z: -358, scale: 1.2 },  /* farmers */
  { z: -428, scale: 1.2 },  /* schools & education */
  { z: -498, scale: 1.2 },  /* doctors & dentists */
  { z: -568, scale: 1.35 }, /* grant */
];

/* ---- boot / fallback ----------------------------------------------------- */
const canvas = document.getElementById("stage");
let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true,
    powerPreference: "high-performance" });
} catch (e) { renderer = null; }
if (!renderer || !renderer.getContext()) {
  document.getElementById("nowebgl").hidden = false;
  document.getElementById("hero").style.display = "none";
  document.getElementById("compass").style.display = "none";
  canvas.style.display = "none";
  document.body.style.overflow = "auto";
} else {
  start();
}

function start() {
  const DPR = Math.min(window.devicePixelRatio || 1, 1.75);
  renderer.setPixelRatio(DPR);
  renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(COL.cream, 60, 260);

  const camera = new THREE.PerspectiveCamera(55, innerWidth / innerHeight, 0.1, 720);
  camera.position.set(0, 5, 92);

  /* lights */
  scene.add(new THREE.AmbientLight(0xfff6e8, 0.9));
  const key = new THREE.DirectionalLight(0xffffff, 1.1); key.position.set(8, 18, 30); scene.add(key);
  const emGlow = new THREE.PointLight(COL.em, 1.4, 160); emGlow.position.set(0, 4, PORTAL_Z); scene.add(emGlow);

  /* ---- THE LATTICE — ordered mesh of dots holding the whole journey.
     Samuel's spec: "ordered initially like a mesh holding mesh", hover turns
     dots to the accent colour, and the field ACCELERATES into light-speed
     streaks when the camera flies between worlds. ------------------------- */
  const dotTex = (() => {           /* round soft dot — square points look cheap */
    const c = document.createElement("canvas"); c.width = c.height = 64;
    const x = c.getContext("2d");
    const g = x.createRadialGradient(32, 32, 0, 32, 32, 32);
    g.addColorStop(0, "rgba(255,255,255,1)"); g.addColorStop(.6, "rgba(255,255,255,.8)");
    g.addColorStop(1, "rgba(255,255,255,0)");
    x.fillStyle = g; x.fillRect(0, 0, 64, 64);
    return new THREE.CanvasTexture(c);
  })();

  const LAYERS = reduced ? 24 : 54, CW = 18, CH = 10;   /* lattice spans all seven worlds */
  const GAPX = 11, GAPY = 9, GAPZ = 14;
  const COUNT = LAYERS * CW * CH;
  const basePos = new Float32Array(COUNT * 3);
  const colArr = new Float32Array(COUNT * 3);
  const inkC = new THREE.Color(COL.ink);
  {
    let k = 0;
    for (let l = 0; l < LAYERS; l++)
      for (let r = 0; r < CH; r++)
        for (let c = 0; c < CW; c++, k++) {
          basePos[k*3]   = (c - (CW - 1) / 2) * GAPX;
          basePos[k*3+1] = (r - (CH - 1) / 2) * GAPY + 2;
          basePos[k*3+2] = 96 - l * GAPZ;
          colArr[k*3] = inkC.r; colArr[k*3+1] = inkC.g; colArr[k*3+2] = inkC.b;
        }
  }
  const dgeo = new THREE.BufferGeometry();
  dgeo.setAttribute("position", new THREE.BufferAttribute(basePos.slice(), 3));
  dgeo.setAttribute("color", new THREE.BufferAttribute(colArr, 3));
  const dots = new THREE.Points(dgeo, new THREE.PointsMaterial({
    vertexColors: true, size: 0.6, sizeAttenuation: true, map: dotTex,
    transparent: true, opacity: 0.4, depthWrite: false }));
  scene.add(dots);

  /* hover: raycast the lattice, hovered dots glow the world's accent */
  const ray = new THREE.Raycaster(); ray.params.Points.threshold = 2.2;
  const ndc = new THREE.Vector2(2, 2);
  addEventListener("pointermove", e => {
    ndc.x = (e.clientX / innerWidth) * 2 - 1;
    ndc.y = -(e.clientY / innerHeight) * 2 + 1;
  }, { passive: true });

  /* warp streaks: invisible at rest, stretch + brighten with camera speed */
  const SN = reduced ? 0 : 520;
  const sBase = [];
  const sArr = new Float32Array(Math.max(1, SN * 2 * 3));
  for (let i = 0; i < SN; i++) {
    const x = (Math.random() - 0.5) * 170, y = (Math.random() - 0.5) * 110,
          z = 100 - Math.random() * 700;
    sBase.push([x, y, z]);
    sArr.set([x, y, z, x, y, z], i * 6);
  }
  const sgeo = new THREE.BufferGeometry();
  sgeo.setAttribute("position", new THREE.BufferAttribute(sArr, 3));
  const streaks = new THREE.LineSegments(sgeo, new THREE.LineBasicMaterial({
    color: COL.ink, transparent: true, opacity: 0, depthWrite: false }));
  if (SN) scene.add(streaks);

  /* ---- the roof-A portal (extruded, emerald, you fly THROUGH it) -------- */
  function roofAShape() {
    // exact brand glyph, centred + Y-flipped from the SVG path
    const pts = [[0,32],[24,-32],[12,-32],[0,4],[-12,-32],[-24,-32]];
    const s = new THREE.Shape();
    s.moveTo(pts[0][0], pts[0][1]);
    for (let i = 1; i < pts.length; i++) s.lineTo(pts[i][0], pts[i][1]);
    s.closePath();
    return s;
  }
  function makeA(scale, z, emissiveBoost) {
    const geo = new THREE.ExtrudeGeometry(roofAShape(), { depth: 6, bevelEnabled: true,
      bevelThickness: 0.8, bevelSize: 0.8, bevelSegments: 2 });
    geo.center();
    const mat = new THREE.MeshStandardMaterial({ color: COL.cream, emissive: COL.em,
      emissiveIntensity: emissiveBoost, metalness: 0.1, roughness: 0.5 });
    const m = new THREE.Mesh(geo, mat);
    m.scale.setScalar(scale);
    m.position.set(0, -6 * scale, z);
    return m;
  }
  const portal = makeA(1.5, PORTAL_Z, 0.55); scene.add(portal);
  const portals = WORLD_PORTALS.map(w => { const m = makeA(w.scale, w.z, 0.34); scene.add(m); return m; });

  /* light ring behind portal = the next world glimpsed inside the A */
  const halo = new THREE.Mesh(new THREE.CircleGeometry(26, 48),
    new THREE.MeshBasicMaterial({ color: COL.creamWarm, transparent: true, opacity: 0.0 }));
  halo.position.set(0, 2, PORTAL_Z - 4); scene.add(halo);

  /* ---- story objects: FROSTED GLASS panels (gloss, shade, border) -------- */
  function glassTex(tint, border, glossA) {
    const c = document.createElement("canvas"); c.width = 512; c.height = 320;
    const x = c.getContext("2d");
    const m = 42, r = 38, w = 512 - m*2, h = 320 - m*2;
    const rr = (xx, yy, ww, hh, rad) => { x.beginPath(); x.roundRect(xx, yy, ww, hh, rad); };
    /* soft drop shade */
    x.shadowColor = "rgba(21,24,26,.30)"; x.shadowBlur = 26; x.shadowOffsetY = 12;
    rr(m, m, w, h, r); x.fillStyle = tint; x.fill();
    x.shadowColor = "transparent";
    /* frosted border */
    rr(m, m, w, h, r); x.strokeStyle = border; x.lineWidth = 3; x.stroke();
    /* gloss sweep across the top */
    const g = x.createLinearGradient(m, m, m + w*0.7, m + h*0.9);
    g.addColorStop(0, `rgba(255,255,255,${glossA})`); g.addColorStop(.45, "rgba(255,255,255,.06)");
    g.addColorStop(1, "rgba(255,255,255,0)");
    rr(m, m, w, h, r); x.fillStyle = g; x.fill();
    return new THREE.CanvasTexture(c);
  }
  function glassPanel(w, h, tint, border, x, y, z, glossA) {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w * 1.18, h * 1.18),
      new THREE.MeshBasicMaterial({ map: glassTex(tint, border, glossA ?? 0.42),
        transparent: true, depthWrite: false, side: THREE.DoubleSide }));
    m.position.set(x, y, z); return m;
  }
  /* legacy flat panel (still used for the ember) */
  function panel(w, h, color, x, y, z, op) {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h),
      new THREE.MeshBasicMaterial({ color, transparent: true, opacity: op ?? 0.9, side: THREE.DoubleSide }));
    m.position.set(x, y, z); return m;
  }
  // story 1 — "have you got": four frosted sources + one emerald glass search bar
  const cluster1 = new THREE.Group();
  const srcSpots = [[-12,8],[10,10],[-9,-7],[12,-6]];
  srcSpots.forEach(([x,y]) => cluster1.add(
    glassPanel(7, 4.4, "rgba(248,246,240,.55)", "rgba(21,24,26,.20)", x, y, 0)));
  cluster1.add(glassPanel(30, 5, "rgba(10,138,82,.60)", "rgba(255,255,255,.55)", 0, 0, -8, 0.5));
  cluster1.position.set(11, 2, -92); cluster1.rotation.y = -0.38; scene.add(cluster1);

  // story 2 — the echo: pink frosted chips + one merged emerald glass inbox
  const cluster2 = new THREE.Group();
  for (let i = 0; i < 10; i++) {
    const a = (i / 10) * Math.PI * 2;
    cluster2.add(glassPanel(5.4, 3.4, "rgba(232,90,138,.42)", "rgba(255,255,255,.5)",
      Math.cos(a)*13, Math.sin(a)*9, (Math.random()-0.5)*8));
  }
  cluster2.add(glassPanel(26, 7, "rgba(10,138,82,.60)", "rgba(255,255,255,.55)", 0, 0, -10, 0.5));
  cluster2.position.set(-11, 2, -150); cluster2.rotation.y = 0.34; scene.add(cluster2);

  /* a single distant orange ember = the expiring offer, seeding the palette */
  const ember = panel(4, 4, COL.orange, 20, 12, -120, 0.0); scene.add(ember);

  /* ---- Retail World atmosphere — Samuel's "vibing colours" (noomo Spirit):
     iridescent lilac/pink grade + soft bloom suns + a pearlescent script word
     floating in the shop. Brand logic: pink is the customers/communication
     accent, so Retail World wears it; the foundation stays cream/emerald. */
  const gradeEl = document.getElementById("grade");

  function glowTexture(inner, outer) {
    const c = document.createElement("canvas"); c.width = c.height = 256;
    const x = c.getContext("2d");
    const g = x.createRadialGradient(128, 128, 0, 128, 128, 128);
    g.addColorStop(0, inner); g.addColorStop(1, outer);
    x.fillStyle = g; x.fillRect(0, 0, 256, 256);
    return new THREE.CanvasTexture(c);
  }
  const sun = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTexture("rgba(255,255,255,.95)", "rgba(255,255,255,0)"),
    transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending }));
  sun.scale.setScalar(54); sun.position.set(9, 16, -132); scene.add(sun); /* halo behind+above the word */
  const sunPink = new THREE.Sprite(new THREE.SpriteMaterial({
    map: glowTexture("rgba(244,178,220,.75)", "rgba(244,178,220,0)"),
    transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending }));
  sunPink.scale.setScalar(140); sunPink.position.set(-22, 0, -158); scene.add(sunPink);

  /* the script word — Great Vibes (OFL, self-hosted), pearlescent gradient,
     drawn to a canvas texture so it truly floats in the 3D world */
  let wordMesh = null;
  (async () => {
    try {
      const f = new FontFace("GreatVibes", "url(/v5/assets/fonts/GreatVibes-Regular.woff2)");
      await f.load(); document.fonts.add(f);
    } catch (e) { /* falls back to cursive */ }
    const c = document.createElement("canvas"); c.width = 2048; c.height = 640;
    const x = c.getContext("2d");
    x.font = "400 350px GreatVibes, cursive";
    x.textAlign = "center"; x.textBaseline = "middle";
    const g = x.createLinearGradient(280, 0, 1768, 0);
    g.addColorStop(0, "#fdf6ff"); g.addColorStop(.4, "#f3bfe0");
    g.addColorStop(.7, "#c9aef0"); g.addColorStop(1, "#a8ddcb");
    x.shadowColor = "rgba(255,255,255,.95)"; x.shadowBlur = 30;
    x.fillStyle = g; x.fillText("the shop", 1024, 330);
    /* definition so the pearl reads over the bloom */
    x.shadowBlur = 0;
    x.strokeStyle = "rgba(96,62,138,.5)"; x.lineWidth = 5;
    x.strokeText("the shop", 1024, 330);
    const tex = new THREE.CanvasTexture(c); tex.anisotropy = 4;
    wordMesh = new THREE.Mesh(new THREE.PlaneGeometry(36, 11.25),
      new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0, depthWrite: false }));
    wordMesh.position.set(-2, 8.5, -100);
    scene.add(wordMesh);
  })();

  /* ---- scroll proxy (INVERTED: scrolling UP flies you FORWARD) ----------
     Samuel's spec 11/06: the journey is an ascent — wheel/swipe UP moves the
     camera forward on Z. The page loads scrolled to the BOTTOM of the proxy,
     so native momentum/touch/keyboard all work; progress = 1 - y/max. */
  const proxy = document.getElementById("scroll-proxy");
  const JOURNEY = 12;                         // viewport-heights of runway (seven worlds)
  function sizeProxy() { proxy.style.height = (JOURNEY * innerHeight) + "px"; }
  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  sizeProxy();

  function maxScroll() { return document.documentElement.scrollHeight - innerHeight; }
  function scrollProgress() {
    const max = maxScroll();
    return max > 0 ? Math.min(1, Math.max(0, 1 - window.scrollY / max)) : 0;
  }
  function yFor(p) { return (1 - p) * maxScroll(); }
  scrollTo(0, maxScroll());                   // start at the journey's foot

  /* ---- journey sampling (smoothstep between beats → settle at each) ------ */
  const smooth = t => t * t * (3 - 2 * t);
  function sampleAt(p) {
    let i = 0;
    while (i < BEATS.length - 2 && p > BEATS[i + 1].p) i++;
    const a = BEATS[i], b = BEATS[i + 1];
    const raw = (p - a.p) / Math.max(1e-4, b.p - a.p);
    const t = smooth(Math.min(1, Math.max(0, raw)));
    return {
      x: a.cam.x + (b.cam.x - a.cam.x) * t,
      y: a.cam.y + (b.cam.y - a.cam.y) * t,
      z: a.cam.z + (b.cam.z - a.cam.z) * t,
      seg: i, t,
    };
  }

  /* ---- overlay copy ----------------------------------------------------- */
  const beatEl = document.getElementById("beat");
  const kEl = beatEl.querySelector(".beat-kicker");
  const lEl = beatEl.querySelector(".beat-line");
  const ctaEl = beatEl.querySelector(".beat-cta");
  let shownBeat = -1;
  function syncCopy(p, begun) {
    // pick the nearest beat that has copy; show when settled near its centre
    let best = -1, bestD = 1;
    for (let i = 2; i < BEATS.length; i++) {
      if (!BEATS[i].line) continue;
      const d = Math.abs(p - BEATS[i].p);
      if (d < bestD) { bestD = d; best = i; }
    }
    const near = best >= 0 && bestD < 0.085 && begun;
    if (near && best !== shownBeat) {
      const B = BEATS[best];
      kEl.textContent = B.kicker; lEl.textContent = B.line;
      beatEl.style.setProperty("--accent", `var(--${B.accent})`);
      if (B.cta) { ctaEl.textContent = B.cta.label; ctaEl.href = B.cta.href; ctaEl.hidden = false; }
      else ctaEl.hidden = true;
      shownBeat = best;
    }
    beatEl.classList.toggle("show", near);
    if (!near) shownBeat = -1;
  }

  /* ---- camera state (eased toward scroll target) ------------------------ */
  let camP = 0, targetP = 0, begun = false, mx = 0, my = 0;
  let lastP = 0, warp = 0;
  const worldAccent = new THREE.Color(COL.em);
  const mouse = { x: 0, y: 0 };
  addEventListener("pointermove", e => {
    mouse.x = (e.clientX / innerWidth - 0.5);
    mouse.y = (e.clientY / innerHeight - 0.5);
  }, { passive: true });

  addEventListener("scroll", () => { targetP = scrollProgress();
    if (targetP > 0.005 && !begun) setBegun(true); }, { passive: true });

  function applyCamera() {
    const s = sampleAt(camP);
    mx += ((mouse.x * 5) - mx) * 0.05;
    my += ((-mouse.y * 3) - my) * 0.05;
    camera.position.set(s.x + mx, s.y + my, s.z);
    const look = sampleAt(Math.min(1, camP + 0.04));
    camera.lookAt(look.x * 0.5, look.y, s.z - 50);

    // crossing the first portal: warm glow at the threshold, then the world grades
    const clamp01 = x => Math.min(1, Math.max(0, x));
    const warm = clamp01((camP - 0.09) / 0.05) * (1 - clamp01((camP - 0.18) / 0.07));
    /* retail occupies p≈0.14–0.40; its lilac grade fades as trades nears */
    const retail = clamp01((camP - 0.14) / 0.08) * (1 - clamp01((camP - 0.40) / 0.07));
    halo.material.opacity = 0.5 * warm;
    gradeEl.style.opacity = (retail * 0.9).toFixed(3);

    /* every world tints the fog + accent as you near it */
    const TINTS = [
      { p: 0.27, fog: 0xe4d2ee, accent: COL.pink },    /* shops — lilac/pink   */
      { p: 0.45, fog: 0xf3ddc2, accent: COL.orange },  /* trades — amber       */
      { p: 0.54, fog: 0xd9ece2, accent: COL.mint },    /* manufacturing — mint */
      { p: 0.63, fog: 0xe9ecd2, accent: COL.orange },  /* farmers — green-gold */
      { p: 0.72, fog: 0xdcecea, accent: COL.mint },    /* schools — chalk mint */
      { p: 0.81, fog: 0xf6dce6, accent: COL.pink },    /* health — soft pink   */
      { p: 0.90, fog: 0xd9ead9, accent: COL.em },      /* grant — emerald      */
    ];
    const fogC = new THREE.Color(COL.cream).lerp(new THREE.Color(COL.creamWarm), warm * 0.8);
    worldAccent.setHex(COL.em);
    for (const t of TINTS) {
      const inf = Math.max(0, 1 - Math.abs(camP - t.p) / 0.09);
      if (inf > 0) {
        fogC.lerp(new THREE.Color(t.fog), inf * 0.85);
        worldAccent.lerp(new THREE.Color(t.accent), inf * 0.8);
      }
    }
    scene.fog.color.copy(fogC);
    emGlow.color.copy(worldAccent);
    sun.material.opacity = retail * 0.85;
    sunPink.material.opacity = retail * 0.6;
    if (wordMesh) wordMesh.material.opacity = retail * 0.95;
    ember.material.opacity = 0.0; // (kept subtle; activated in offer scene later)

    // progress hairline
    progI.style.width = (camP * 100).toFixed(2) + "%";
  }

  /* ---- animation -------------------------------------------------------- */
  const progI = document.querySelector("#progress i");
  let running = true;
  document.addEventListener("visibilitychange", () => { running = !document.hidden; });

  const clock = new THREE.Clock();
  function frame() {
    requestAnimationFrame(frame);
    if (!running) return;
    const dt = Math.min(0.05, clock.getDelta());
    const time = clock.elapsedTime;

    if (reduced) {
      // scene cuts: snap to nearest beat, no flight
      let nb = 0, nd = 1;
      BEATS.forEach((B, i) => { const d = Math.abs(targetP - B.p); if (d < nd) { nd = d; nb = i; } });
      camP += (BEATS[nb].p - camP) * 0.5;
    } else {
      camP += (targetP - camP) * 0.06;        // momentum + comfort
    }

    portal.rotation.z = Math.sin(time * 0.18) * 0.04;
    portals.forEach((m, i) => { m.rotation.z = Math.sin(time * 0.14 + i) * 0.05; });
    cluster1.children.forEach((c, i) => { c.position.y += Math.sin(time * 0.8 + i) * 0.004; });
    cluster2.rotation.z = time * 0.05;

    /* lattice: gentle wave, hover glow in the world's accent, colour decay */
    const posA = dgeo.getAttribute("position"), colA = dgeo.getAttribute("color");
    for (let i = 0; i < COUNT; i++) {
      posA.array[i*3+1] = basePos[i*3+1] +
        Math.sin(time * 0.7 + basePos[i*3] * 0.16 + basePos[i*3+2] * 0.05) * 0.9;
    }
    posA.needsUpdate = true;
    for (let i = 0; i < COUNT * 3; i += 3) {
      colA.array[i]   += (inkC.r - colA.array[i])   * 0.06;
      colA.array[i+1] += (inkC.g - colA.array[i+1]) * 0.06;
      colA.array[i+2] += (inkC.b - colA.array[i+2]) * 0.06;
    }
    if (ndc.x < 1.5 && !reduced) {
      ray.setFromCamera(ndc, camera);
      const hits = ray.intersectObject(dots);
      for (let h = 0; h < Math.min(hits.length, 48); h++) {
        const i = hits[h].index * 3;
        colA.array[i] = worldAccent.r; colA.array[i+1] = worldAccent.g; colA.array[i+2] = worldAccent.b;
      }
    }
    colA.needsUpdate = true;

    /* warp: camera speed stretches the field into light-speed streaks */
    const v = Math.abs(camP - lastP) / Math.max(dt, 1e-3); lastP = camP;
    warp += (Math.min(1, v * 7) - warp) * 0.14;
    if (SN) {
      const len = warp * warp * 30;
      for (let i = 0; i < SN; i++) {
        sArr[i*6+2] = sBase[i][2] + len / 2;
        sArr[i*6+5] = sBase[i][2] - len / 2;
      }
      sgeo.getAttribute("position").needsUpdate = true;
      streaks.material.opacity = Math.min(0.5, warp * warp * 0.6);
      streaks.material.color.copy(worldAccent).lerp(inkC, 0.45);
      dots.material.opacity = 0.4 - warp * 0.22;   /* mesh yields to the streaks */
    }
    if (wordMesh) {
      wordMesh.position.y = 8.5 + Math.sin(time * 0.45) * 0.5;
      wordMesh.rotation.z = Math.sin(time * 0.3) * 0.012;
    }

    applyCamera();
    syncCopy(camP, begun);
    updateCompass(camP);
    renderer.render(scene, camera);
  }

  function resize() {
    camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight, false);
    sizeProxy();
    scrollTo(0, yFor(targetP));               // keep journey position across resize
  }
  addEventListener("resize", resize); resize();

  /* ---- hero / begin / sound -------------------------------------------- */
  function setBegun(v) {
    begun = v; document.body.classList.toggle("begun", v);
  }
  document.getElementById("begin").addEventListener("click", () => {
    setBegun(true);
    smoothScrollTo(yFor(0.16), 1100);         // a gentle lift into the journey
  });

  function smoothScrollTo(to, dur) {
    const from = window.scrollY, t0 = performance.now();
    (function step(now) {
      const k = Math.min(1, (now - t0) / dur), e = smooth(k);
      scrollTo(0, from + (to - from) * e);
      if (k < 1) requestAnimationFrame(step);
    })(performance.now());
  }

  /* sound — soft ambient pad, OFF by default (EU-polite) */
  const soundBtn = document.getElementById("sound");
  let audio = null, soundOn = false;
  soundBtn.addEventListener("click", () => {
    soundOn = !soundOn;
    soundBtn.setAttribute("aria-pressed", String(soundOn));
    soundBtn.setAttribute("aria-label", soundOn ? "Sound on" : "Sound off");
    if (soundOn) startPad(); else stopPad();
  });
  function startPad() {
    try {
      audio = new (window.AudioContext || window.webkitAudioContext)();
      const g = audio.createGain(); g.gain.value = 0.0; g.connect(audio.destination);
      [110, 164.81, 220].forEach((f, i) => {
        const o = audio.createOscillator(); o.type = "sine"; o.frequency.value = f;
        const og = audio.createGain(); og.gain.value = 0.06 / (i + 1);
        o.connect(og); og.connect(g); o.start();
      });
      g.gain.linearRampToValueAtTime(0.12, audio.currentTime + 1.6);
      audio._master = g;
    } catch (e) {}
  }
  function stopPad() {
    if (!audio) return;
    try { audio._master.gain.linearRampToValueAtTime(0, audio.currentTime + 0.5);
      setTimeout(() => { audio.close(); audio = null; }, 600); } catch (e) {}
  }

  /* ---- compass nav (replaces the floor elevator) ----------------------- */
  const compassToggle = document.getElementById("compass-toggle");
  const compassMenu = document.getElementById("compass-menu");
  const NAV = [
    { label: "Atrium", p: 0.0 },
    { label: "Shops on the street", p: 0.21 },
    { label: "Trades people", p: 0.45 },
    { label: "Manufacturing", p: 0.54 },
    { label: "Farmers", p: 0.63 },
    { label: "Schools & education", p: 0.72 },
    { label: "Doctors & dentists", p: 0.81 },
    { label: "The €200 grant", p: 0.90 },
  ];
  const SEP = "—";
  function buildCompass() {
    NAV.forEach((n, i) => {
      const b = document.createElement("button");
      b.className = "step"; b.setAttribute("role", "menuitem");
      b.dataset.p = n.p; b.dataset.visited = "false";
      b.innerHTML = `<span class="stepdot"></span>${n.label}`;
      b.addEventListener("click", () => {
        setBegun(true);
        smoothScrollTo(yFor(n.p), 1200); closeCompass();
      });
      compassMenu.appendChild(b);
    });
    const sep = document.createElement("div"); sep.className = "compass-sep"; compassMenu.appendChild(sep);
    const shop = document.createElement("a"); shop.href = "/index.html"; shop.setAttribute("role","menuitem");
    shop.textContent = "Store & toolkits"; compassMenu.appendChild(shop);
    const conv = document.createElement("a"); conv.href = "/v4/"; conv.setAttribute("role","menuitem");
    conv.textContent = "Talk to us"; compassMenu.appendChild(conv);
  }
  buildCompass();
  function openCompass() { compassMenu.hidden = false; compassToggle.setAttribute("aria-expanded","true"); }
  function closeCompass() { compassMenu.hidden = true; compassToggle.setAttribute("aria-expanded","false"); }
  compassToggle.addEventListener("click", () =>
    compassMenu.hidden ? openCompass() : closeCompass());
  addEventListener("keydown", e => {
    if (e.key === "Escape") closeCompass();
    if (e.key === "?" ) { compassMenu.hidden ? openCompass() : closeCompass(); }
  });
  function updateCompass(p) {
    const steps = compassMenu.querySelectorAll(".step");
    let cur = 0, cd = 1;
    steps.forEach((s, i) => {
      const sp = parseFloat(s.dataset.p);
      if (p >= sp - 0.02) s.dataset.visited = "true";
      const d = Math.abs(p - sp); if (d < cd) { cd = d; cur = i; }
    });
    steps.forEach((s, i) => s.setAttribute("aria-current", String(i === cur)));
  }

  /* everything is wired — start the render loop */
  frame();
}
