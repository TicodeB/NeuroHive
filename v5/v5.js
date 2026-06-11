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
const BEATS = [
  { id: "atrium",  p: 0.00, cam: { x: 0,   y: 5,  z: 92 }, accent: "em",
    kicker: "", line: "" },
  { id: "approach",p: 0.15, cam: { x: 0,   y: 4,  z: 40 }, accent: "em",
    kicker: "", line: "" },
  { id: "portal",  p: 0.30, cam: { x: 0,   y: 3,  z: -16 }, accent: "em",
    kicker: "Retail world", line: "Step inside the shop." },
  { id: "story1",  p: 0.50, cam: { x: -6,  y: 4,  z: -74 }, accent: "stone",
    kicker: "The shop · Saturday", line: "“Have you got…?” — and the answer lives in four places." },
  { id: "story2",  p: 0.72, cam: { x: 6,   y: 4,  z: -132 }, accent: "pink",
    kicker: "The shop · the echo", line: "She asked the same thing four ways. You answered four times." },
  { id: "invite",  p: 0.92, cam: { x: 0,   y: 5,  z: -190 }, accent: "em",
    kicker: "The way out", line: "Records that keep themselves. Messages that answer once.",
    cta: { label: "See what Leanta sets up →", href: "/index.html#products" } },
  { id: "end",     p: 1.00, cam: { x: 0,   y: 6,  z: -228 }, accent: "em",
    kicker: "", line: "" },
];
const PORTAL_Z = -30, NEXTA_Z = -250;

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

  const camera = new THREE.PerspectiveCamera(55, innerWidth / innerHeight, 0.1, 600);
  camera.position.set(0, 5, 92);

  /* lights */
  scene.add(new THREE.AmbientLight(0xfff6e8, 0.9));
  const key = new THREE.DirectionalLight(0xffffff, 1.1); key.position.set(8, 18, 30); scene.add(key);
  const emGlow = new THREE.PointLight(COL.em, 1.4, 160); emGlow.position.set(0, 4, PORTAL_Z); scene.add(emGlow);

  /* ---- dot field: speed + parallax (the mesh aesthetic, in real 3D) ----- */
  const N = reduced ? 1400 : 4200;
  const dpos = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    dpos[i*3]   = (Math.random() - 0.5) * 150;
    dpos[i*3+1] = (Math.random() - 0.5) * 90;
    dpos[i*3+2] = 100 - Math.random() * 360;
  }
  const dgeo = new THREE.BufferGeometry();
  dgeo.setAttribute("position", new THREE.BufferAttribute(dpos, 3));
  const dots = new THREE.Points(dgeo, new THREE.PointsMaterial({
    color: COL.ink, size: 0.5, sizeAttenuation: true, transparent: true, opacity: 0.34 }));
  scene.add(dots);

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
  const nextA  = makeA(1.0, NEXTA_Z, 0.32);  scene.add(nextA);

  /* light ring behind portal = the next world glimpsed inside the A */
  const halo = new THREE.Mesh(new THREE.CircleGeometry(26, 48),
    new THREE.MeshBasicMaterial({ color: COL.creamWarm, transparent: true, opacity: 0.0 }));
  halo.position.set(0, 2, PORTAL_Z - 4); scene.add(halo);

  /* ---- story objects ---------------------------------------------------- */
  function panel(w, h, color, x, y, z, op) {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h),
      new THREE.MeshBasicMaterial({ color, transparent: true, opacity: op ?? 0.9, side: THREE.DoubleSide }));
    m.position.set(x, y, z); return m;
  }
  // story 1 — "have you got": four scattered sources (stone) + one emerald search bar behind
  const cluster1 = new THREE.Group();
  const srcSpots = [[-12,8],[10,10],[-9,-7],[12,-6]];
  srcSpots.forEach(([x,y]) => cluster1.add(panel(7,4.4, COL.stone, x, y, 0, 0.8)));
  const search = panel(30, 5, COL.em, 0, 0, -8, 0.96); cluster1.add(search);
  cluster1.position.z = -92; scene.add(cluster1);

  // story 2 — the echo: many pink message chips + one merged emerald inbox
  const cluster2 = new THREE.Group();
  for (let i = 0; i < 10; i++) {
    const a = (i / 10) * Math.PI * 2;
    cluster2.add(panel(5.4, 3.4, COL.pink, Math.cos(a)*13, Math.sin(a)*9, (Math.random()-0.5)*8, 0.82));
  }
  const inbox = panel(26, 7, COL.em, 0, 0, -10, 0.95); cluster2.add(inbox);
  cluster2.position.z = -150; scene.add(cluster2);

  /* a single distant orange ember = the expiring offer, seeding the palette */
  const ember = panel(4, 4, COL.orange, 20, 12, -120, 0.0); scene.add(ember);

  /* ---- scroll proxy (INVERTED: scrolling UP flies you FORWARD) ----------
     Samuel's spec 11/06: the journey is an ascent — wheel/swipe UP moves the
     camera forward on Z. The page loads scrolled to the BOTTOM of the proxy,
     so native momentum/touch/keyboard all work; progress = 1 - y/max. */
  const proxy = document.getElementById("scroll-proxy");
  const JOURNEY = 7;                          // viewport-heights of scroll runway
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

    // fog warms as we cross the portal
    const warm = Math.min(1, Math.max(0, (camP - 0.24) / 0.12));
    scene.fog.color.setHex(COL.cream).lerp(new THREE.Color(COL.creamWarm), warm * 0.8);
    halo.material.opacity = 0.5 * warm;
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

    dots.rotation.z = time * 0.006;
    portal.rotation.z = Math.sin(time * 0.18) * 0.04;
    nextA.rotation.z = Math.sin(time * 0.14 + 1) * 0.05;
    cluster1.children.forEach((c, i) => { c.position.y += Math.sin(time * 0.8 + i) * 0.004; });
    cluster2.rotation.z = time * 0.05;

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
    { label: "Retail world", p: 0.42 },
    { label: "The way out", p: 0.92 },
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
