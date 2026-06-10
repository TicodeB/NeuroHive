/* LEANTA v4.1 story engine.
   Architecture (borrowed from noomo, rebuilt honestly):
   - One fixed WebGL scene (#scene) + a 760vh scroll runway (#stage); scroll
     position drives a cinematic camera along a spline through 5 "stations".
   - Content lives in fixed glass panels that fade/slide as the camera passes.
   - Mobile / reduced-motion / no-WebGL / no-JS => html.flow: everything
     renders as a normal readable document. Progressive enhancement throughout.
   - Sound: ALWAYS-visible toggle. Plays /v4/assets/leanta-theme.mp3 when the
     Suno track exists; until then a WebAudio ambient pad (honest placeholder).
   - Lea: pet companion + chat. Brain is on-device retrieval over site facts
     (no data leaves the browser). Swap-in point for a real model is marked
     LEA_UPGRADE below. Omma/Spline pet embeds via LEANTA.ommaPetUrl.        */

(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced) document.documentElement.classList.add("reduced");

  var wantCinema = !reduced &&
    window.matchMedia("(min-width: 1024px) and (pointer: fine)").matches &&
    typeof window.THREE !== "undefined";

  /* ---------- preloader ------------------------------------------------- */
  var pre = document.getElementById("pre");
  function killPre() { if (pre) { pre.classList.add("done"); pre.setAttribute("aria-hidden", "true"); } }
  if (!pre || reduced || sessionStorage.getItem("v4seen")) {
    killPre();
  } else {
    sessionStorage.setItem("v4seen", "1");
    var pn = 0, pbar = pre.querySelector(".bar i"), pcount = pre.querySelector(".count");
    var pt = setInterval(function () {
      pn = Math.min(100, pn + 2 + Math.random() * 6);
      pbar.style.width = pn + "%";
      pcount.textContent = (pn < 10 ? "0" : "") + Math.floor(pn);
      if (pn >= 100) { clearInterval(pt); setTimeout(killPre, 300); }
    }, 28);
    setTimeout(killPre, 2800); /* hard cap — never trap the visitor */
  }

  /* ---------- custom cursor (fine pointers only) ------------------------ */
  if (window.matchMedia("(hover: hover) and (pointer: fine)").matches && !reduced) {
    document.body.classList.add("has-cursor");
    var dot = document.querySelector(".cur"), ring = document.querySelector(".cur-ring");
    var cmx = innerWidth / 2, cmy = innerHeight / 2, crx = cmx, cry = cmy;
    addEventListener("pointermove", function (e) { cmx = e.clientX; cmy = e.clientY; }, { passive: true });
    (function curLoop() {
      crx += (cmx - crx) * 0.16; cry += (cmy - cry) * 0.16;
      dot.style.left = cmx + "px"; dot.style.top = cmy + "px";
      ring.style.left = crx + "px"; ring.style.top = cry + "px";
      requestAnimationFrame(curLoop);
    })();
    document.addEventListener("pointerover", function (e) {
      if (e.target.closest("a, button, [data-hover], label, input")) ring.classList.add("big");
      else ring.classList.remove("big");
    }, { passive: true });

    /* magnetic pull — interactive elements lean toward the cursor */
    document.addEventListener("pointermove", function (e) {
      var t = e.target.closest(".btn-x, .chip, .sound, .glass");
      if (!t) return;
      if (!t.classList.contains("magnet")) t.classList.add("magnet");
      var r = t.getBoundingClientRect();
      var strength = t.classList.contains("glass") ? 6 : 4;
      var dx = ((e.clientX - r.left) / r.width - 0.5) * 2 * strength;
      var dy = ((e.clientY - r.top) / r.height - 0.5) * 2 * strength;
      t.style.transform = "translate(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px)";
    }, { passive: true });
    document.addEventListener("pointerout", function (e) {
      var t = e.target.closest(".btn-x, .chip, .sound, .glass");
      if (t && !t.contains(e.relatedTarget)) t.style.transform = "";
    }, { passive: true });
  }

  /* ---------- sound: always-visible toggle ------------------------------ */
  /* mp3 if Samuel has dropped the Suno track in; otherwise an honest
     WebAudio ambient pad so the button works TODAY. Off by default (EU-polite). */
  var soundBtn = document.getElementById("sound");
  var soundLabel = document.getElementById("sound-label");
  var AUDIO_SRC = "/v4/assets/leanta-theme.mp3";
  var engine = null; /* {start,stop} */

  function mp3Engine() {
    var a = new Audio(AUDIO_SRC); a.loop = true; a.volume = 0.35;
    return { start: function () { a.play().catch(function () {}); }, stop: function () { a.pause(); } };
  }
  function padEngine() {
    var ctx = null, master = null, pluckTimer = null;
    function build() {
      ctx = new (window.AudioContext || window.webkitAudioContext)();
      master = ctx.createGain(); master.gain.value = 0.0001; master.connect(ctx.destination);
      var filter = ctx.createBiquadFilter(); filter.type = "lowpass";
      filter.frequency.value = 460; filter.Q.value = 0.7; filter.connect(master);
      [[110, "sine", 1], [165.1, "triangle", 0.5], [220.6, "sine", 0.22]].forEach(function (cfgO) {
        var o = ctx.createOscillator(), g = ctx.createGain();
        o.type = cfgO[1]; o.frequency.value = cfgO[0]; g.gain.value = cfgO[2];
        o.connect(g); g.connect(filter); o.start();
      });
      var lfo = ctx.createOscillator(), lg = ctx.createGain();
      lfo.frequency.value = 0.06; lg.gain.value = 95; lfo.connect(lg); lg.connect(filter.frequency); lfo.start();
      function pluck() {
        if (!ctx) return;
        var f = [392, 523.25, 659.25, 587.33][Math.floor(Math.random() * 4)];
        var o = ctx.createOscillator(), g = ctx.createGain();
        o.type = "sine"; o.frequency.value = f;
        g.gain.setValueAtTime(0.028, ctx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 1.3);
        o.connect(g); g.connect(master); o.start(); o.stop(ctx.currentTime + 1.4);
        pluckTimer = setTimeout(pluck, 6000 + Math.random() * 5000);
      }
      pluckTimer = setTimeout(pluck, 4000);
    }
    return {
      start: function () {
        if (!ctx) build();
        if (ctx.state === "suspended") ctx.resume();
        master.gain.cancelScheduledValues(ctx.currentTime);
        master.gain.exponentialRampToValueAtTime(0.055, ctx.currentTime + 1.2);
      },
      stop: function () {
        if (!ctx) return;
        master.gain.cancelScheduledValues(ctx.currentTime);
        master.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.5);
        clearTimeout(pluckTimer);
      }
    };
  }
  fetch(AUDIO_SRC, { method: "HEAD" }).then(function (r) {
    engine = r.ok ? mp3Engine() : padEngine();
    if (r.ok) soundBtn.title = "Theme by Suno — off until you ask.";
  }).catch(function () { engine = padEngine(); });

  soundBtn.addEventListener("click", function () {
    if (!engine) engine = padEngine();
    var on = soundBtn.classList.toggle("on");
    soundBtn.setAttribute("aria-pressed", String(on));
    soundLabel.textContent = on ? "Sound on" : "Sound off";
    if (on) engine.start(); else engine.stop();
  });
  addEventListener("pagehide", function () { if (engine) engine.stop(); });

  /* ---------- video case slots (HEAD-check, else keep poster card) ------ */
  document.querySelectorAll(".vid[data-case]").forEach(function (slot) {
    var src = "/v4/assets/" + slot.getAttribute("data-case") + ".mp4";
    fetch(src, { method: "HEAD" }).then(function (r) {
      if (!r.ok) return;
      var v = document.createElement("video");
      v.src = src; v.controls = true; v.playsInline = true; v.preload = "metadata";
      slot.insertBefore(v, slot.firstChild);
      var fb = slot.querySelector(".fallback");
      if (fb) fb.remove();
    }).catch(function () {});
  });

  /* ---------- "Text us" buttons (same contract as the main site) -------- */
  var cfg = window.LEANTA || { contactEmail: "hello@leanta.ie" };
  document.querySelectorAll("[data-textus]").forEach(function (slot) {
    var a = document.createElement("a");
    a.className = "btn-x ghost"; a.setAttribute("data-hover", "");
    if (cfg.contactPhone) {
      a.href = "sms:" + cfg.contactPhone + "?&body=" + encodeURIComponent("Hi Leanta — [your business name]. ");
      a.textContent = "Text us — no call needed";
    } else {
      a.href = "mailto:" + (cfg.contactEmail || "hello@leanta.ie") +
        "?subject=" + encodeURIComponent("Quick question (no call please)");
      a.textContent = "Message us — no call needed";
    }
    slot.appendChild(a);
  });

  /* ---------- KPI count-up ---------------------------------------------- */
  var counted = false;
  function countUp(scope) {
    if (counted) return; counted = true;
    (scope || document).querySelectorAll(".val[data-count]").forEach(function (el) {
      var target = parseFloat(el.getAttribute("data-count"));
      var prefix = el.getAttribute("data-prefix") || "";
      var dec = (String(el.getAttribute("data-count")).split(".")[1] || "").length;
      var t0 = performance.now();
      (function tick(now) {
        var k = Math.min(1, (now - t0) / 1300); k = 1 - Math.pow(1 - k, 3);
        el.textContent = prefix + (target * k).toFixed(dec);
        if (k < 1) requestAnimationFrame(tick);
      })(t0);
    });
  }

  /* ---------- reveals for normal-flow content (#post + flow panels) ----- */
  if ("IntersectionObserver" in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("in");
          if (en.target.querySelector && en.target.querySelector(".val[data-count]")) countUp(en.target);
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.18 });
    document.querySelectorAll(".rv").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".rv").forEach(function (el) { el.classList.add("in"); });
    countUp(document);
  }

  /* ====================================================================== */
  /*  THE CINEMA — fixed three.js scene, scroll-driven camera               */
  /* ====================================================================== */
  var progressBar = document.querySelector("#progress i");
  addEventListener("scroll", function () {
    var h = document.documentElement;
    var pTot = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight);
    if (progressBar) progressBar.style.width = (pTot * 100).toFixed(2) + "%";
  }, { passive: true });

  function enterFlow() {
    document.documentElement.classList.add("flow");
    countUpWhenVisible();
  }
  function countUpWhenVisible() {
    var kg = document.querySelector(".kgrid");
    if (!kg) return;
    if ("IntersectionObserver" in window && !reduced) {
      var io2 = new IntersectionObserver(function (es) {
        es.forEach(function (en) { if (en.isIntersecting) { countUp(document); io2.disconnect(); } });
      }, { threshold: 0.3 });
      io2.observe(kg);
    } else { countUp(document); }
  }

  if (!wantCinema) { enterFlow(); }
  else {
    try { initCinema(); } catch (err) { enterFlow(); }
  }

  function initCinema() {
    var T = window.THREE;
    var canvas = document.getElementById("scene");
    var stage = document.getElementById("stage");
    var cine = document.getElementById("cine");
    var renderer = new T.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setClearColor(0x0b0d0c, 1);
    renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));

    /* Higgsfield ambient loop behind the scene — activates only if the
       asset exists; clear-alpha drops so the video glows through the fog */
    var bgloop = document.getElementById("bgloop");
    if (bgloop) {
      fetch("/v4/assets/img/bg-loop.mp4", { method: "HEAD" }).then(function (r) {
        if (!r.ok) return;
        bgloop.src = "/v4/assets/img/bg-loop.mp4";
        bgloop.classList.add("live");
        bgloop.play().catch(function () {});
        renderer.setClearColor(0x0b0d0c, 0.55);
      }).catch(function () {});
    }

    var scene = new T.Scene();
    scene.fog = new T.FogExp2(0x0b0d0c, 0.0145);
    var camera = new T.PerspectiveCamera(52, innerWidth / innerHeight, 0.1, 240);

    scene.add(new T.HemisphereLight(0x2c3531, 0x0b0d0c, 0.85));
    [[0, 2, -2, 0x00f07a, 1.1], [0, 1, -42, 0xf5f1e6, 0.8], [0, 2, -84, 0x00f07a, 0.9],
     [0, 3, -126, 0xf5c400, 0.9], [0, 1, -162, 0xf5c400, 1.3]].forEach(function (L) {
      var pl = new T.PointLight(L[3], L[4], 60);
      pl.position.set(L[0], L[1], L[2]); scene.add(pl);
    });

    /* particles — the drifting emerald constellation, full journey length */
    var pGeo = new T.BufferGeometry(), pCount = 1400, pPos = new Float32Array(pCount * 3);
    for (var i = 0; i < pCount; i++) {
      pPos[i * 3] = (Math.random() - 0.5) * 56;
      pPos[i * 3 + 1] = (Math.random() - 0.5) * 30;
      pPos[i * 3 + 2] = 12 - Math.random() * 192;
    }
    pGeo.setAttribute("position", new T.BufferAttribute(pPos, 3));
    var points = new T.Points(pGeo, new T.PointsMaterial({
      color: 0x86ffc9, size: 0.13, transparent: true, opacity: 0.55, depthWrite: false
    }));
    scene.add(points);

    /* station 0 — hero: emerald icosahedron + gold ring */
    var hero = new T.Group();
    var icoWire = new T.Mesh(new T.IcosahedronGeometry(2.2, 1),
      new T.MeshBasicMaterial({ color: 0x00f07a, wireframe: true, transparent: true, opacity: 0.75 }));
    var icoCore = new T.Mesh(new T.IcosahedronGeometry(2.08, 1),
      new T.MeshStandardMaterial({ color: 0x0e1411, roughness: 0.35, metalness: 0.15,
        emissive: 0x0c6b46, emissiveIntensity: 0.6 }));
    var ringG = new T.Mesh(new T.TorusGeometry(3.4, 0.025, 12, 90),
      new T.MeshBasicMaterial({ color: 0xf5c400, transparent: true, opacity: 0.85 }));
    ringG.rotation.x = 1.15;
    hero.add(icoWire); hero.add(icoCore); hero.add(ringG);
    hero.position.set(0, 0.2, -2);
    scene.add(hero);

    /* stations 1→2 — the PAPER STORM that settles into an ordered grid     */
    var papers = [], paperGeo = new T.PlaneGeometry(0.92, 1.3);
    var COLS = 12, ROWS = 7;
    for (var pi = 0; pi < COLS * ROWS; pi++) {
      var shade = 0.86 + Math.random() * 0.14;
      var m = new T.Mesh(paperGeo, new T.MeshStandardMaterial({
        color: new T.Color(shade * 0.96, shade * 0.945, shade * 0.9),
        roughness: 0.9, metalness: 0, side: T.DoubleSide
      }));
      var c = pi % COLS, r = Math.floor(pi / COLS);
      m.userData = {
        rad: 3.5 + Math.random() * 7.5,
        th0: Math.random() * Math.PI * 2,
        y0: (Math.random() - 0.5) * 9,
        ph: Math.random() * Math.PI * 2,
        spin: 0.25 + Math.random() * 0.85,
        rx: Math.random() * Math.PI * 2, ry: Math.random() * Math.PI * 2,
        rz: Math.random() * Math.PI * 2,
        sr1: (Math.random() - 0.5) * 2.4, sr2: (Math.random() - 0.5) * 2.4,
        ox: (c - (COLS - 1) / 2) * 1.18,
        oy: (r - (ROWS - 1) / 2) * 1.12,
        oz: -84.5 + (Math.random() - 0.5) * 0.3
      };
      papers.push(m); scene.add(m);
    }

    /* station 3 — KPI bars rising */
    var bars = [], barCols = [0x00f07a, 0x00f07a, 0xe0a44e, 0x00f07a, 0xe06a5e,
                              0x00f07a, 0x00f07a, 0xe0a44e, 0x00f07a];
    var barGeo = new T.BoxGeometry(0.8, 1, 0.8); barGeo.translate(0, 0.5, 0);
    for (var bi = 0; bi < 9; bi++) {
      var bm = new T.Mesh(barGeo, new T.MeshStandardMaterial({
        color: 0x10221c, roughness: 0.4, metalness: 0.1,
        emissive: barCols[bi], emissiveIntensity: 0.75
      }));
      bm.position.set((bi - 4) * 1.35, -2.4, -126);
      bm.scale.y = 0.001;
      bm.userData.h = 1 + ((bi * 37) % 40) / 10;
      bars.push(bm); scene.add(bm);
    }

    /* station 4 — the gold portal (the visit / walking through the door)  */
    var portal = new T.Mesh(new T.TorusGeometry(3.2, 0.06, 14, 100),
      new T.MeshStandardMaterial({ color: 0x7a6200, roughness: 0.3, metalness: 0.6,
        emissive: 0xf5c400, emissiveIntensity: 1.1 }));
    portal.position.set(0, 0.5, -162);
    scene.add(portal);
    var dashes = [];
    for (var di = 0; di < 12; di++) {
      var dm = new T.Mesh(new T.BoxGeometry(0.12, 0.02, 1.3),
        new T.MeshBasicMaterial({ color: 0x00f07a, transparent: true, opacity: 0 }));
      dm.position.set(0, -2, -134 - di * 2.3);
      dashes.push(dm); scene.add(dm);
    }

    /* camera + look-target splines */
    var v3 = function (x, y, z) { return new T.Vector3(x, y, z); };
    var camCurve = new T.CatmullRomCurve3([
      v3(0, 0.4, 7), v3(5.5, 1.2, -28), v3(-5.5, 0.6, -70),
      v3(4.5, 2.2, -110), v3(0, 0.6, -146), v3(0, 0.8, -159)
    ]);
    var lookCurve = new T.CatmullRomCurve3([
      v3(0, 0.2, -2), v3(0, 0, -42), v3(0, 0, -84.5),
      v3(0, 0.6, -126), v3(0, 0.5, -162), v3(0, 0.5, -172)
    ]);

    var panels = Array.prototype.slice.call(document.querySelectorAll(".panel"));
    var STN = panels.length - 1; /* 4 → pN runs 0..4 */

    function smooth01(x, a, b) { var t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); }

    /* Valentime pacing: the camera ARRIVES, RESTS, DEPARTS. Each station
       segment keeps a dwell plateau at both ends; travel between is eased. */
    function dwell(p) {
      var x = Math.min(1, Math.max(0, p)) * STN;
      var i = Math.floor(x);
      if (i >= STN) return STN;
      return i + smooth01(x - i, 0.14, 0.86);
    }

    /* split panel titles into chars for the staggered reveal */
    panels.forEach(function (pl) {
      var t = pl.querySelector(".title");
      if (!t || t.children.length) return;
      var txt = t.textContent;
      t.textContent = "";
      t.setAttribute("aria-label", txt);
      for (var ci = 0; ci < txt.length; ci++) {
        var sp = document.createElement("span");
        sp.className = "chx";
        sp.setAttribute("aria-hidden", "true");
        sp.textContent = txt[ci] === " " ? " " : txt[ci];
        sp.style.transitionDelay = (ci * 30) + "ms";
        t.appendChild(sp);
      }
    });

    var pCur = 0, mx = 0, my = 0, px = 0, py = 0, inView = true;
    addEventListener("pointermove", function (e) {
      mx = (e.clientX / innerWidth - 0.5) * 2;
      my = (e.clientY / innerHeight - 0.5) * 2;
    }, { passive: true });

    function size() {
      renderer.setSize(innerWidth, innerHeight, false);
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
    }
    size(); addEventListener("resize", size);

    var camPos = new T.Vector3(), lookPos = new T.Vector3();
    var t0 = performance.now();
    canvas.classList.add("live");

    function frame(now) {
      requestAnimationFrame(frame);
      var rect = stage.getBoundingClientRect();
      if (rect.bottom < -20) { /* journey done — hide the cinema, save GPU */
        if (inView) { cine.classList.add("off"); inView = false; }
        return;
      }
      if (!inView) { cine.classList.remove("off"); inView = true; }

      var time = (now - t0) / 1000;
      var pTgt = Math.min(1, Math.max(0, -rect.top / (rect.height - innerHeight)));
      pCur += (pTgt - pCur) * 0.075;
      px += (mx - px) * 0.05; py += (my - py) * 0.05;

      /* camera along the spline + mouse parallax — eased station pacing */
      var pN = dwell(pCur);
      var pSpline = pN / STN;
      camCurve.getPoint(pSpline, camPos);
      lookCurve.getPoint(pSpline, lookPos);
      camera.position.set(camPos.x + px * 1.7, camPos.y + py * -0.9, camPos.z);
      camera.lookAt(lookPos.x + px * 0.7, lookPos.y + py * -0.4, lookPos.z);

      /* hero cluster idle */
      hero.rotation.y += 0.0022; icoWire.rotation.x += 0.0009;
      ringG.rotation.z += 0.0014;
      hero.position.y = 0.2 + Math.sin(time * 0.8) * 0.25;

      /* papers: chaos → order between stations 1 and 2 */
      var tOrder = smooth01(pN, 1.05, 1.95);
      for (var k = 0; k < papers.length; k++) {
        var u = papers[k].userData, P = papers[k];
        var th = u.th0 + time * u.spin * (1 - tOrder);
        var cxp = Math.cos(th) * u.rad, czp = Math.sin(th) * u.rad * 0.7;
        var cyp = u.y0 + Math.sin(time * 1.3 + u.ph) * 0.5;
        P.position.set(
          cxp + (u.ox - cxp) * tOrder,
          cyp + (u.oy - cyp) * tOrder,
          (-42 + czp) + (u.oz - (-42 + czp)) * tOrder
        );
        var f = 1 - tOrder;
        P.rotation.set((u.rx + time * u.sr1) * f, (u.ry + time * u.sr2) * f, u.rz * f);
      }

      /* bars rise through station 3 */
      var tBars = smooth01(pN, 2.45, 3.15);
      for (var b = 0; b < bars.length; b++) {
        var grow = Math.min(1, Math.max(0, (tBars - b * 0.045) / 0.7));
        bars[b].scale.y = Math.max(0.001, bars[b].userData.h * grow);
      }

      /* portal breathes; road dashes light up on approach */
      portal.rotation.z = time * 0.25;
      portal.material.emissiveIntensity = 1.0 + Math.sin(time * 2) * 0.25;
      var tRoad = smooth01(pN, 3.35, 3.9);
      for (var d = 0; d < dashes.length; d++) {
        dashes[d].material.opacity = tRoad * 0.85;
      }

      points.rotation.y = time * 0.008;

      /* panel choreography — opacity + Valentime blur-fade */
      for (var s = 0; s < panels.length; s++) {
        var dd = pN - s;
        var o = 1 - Math.min(1, Math.abs(dd) / 0.55);
        var el = panels[s];
        el.style.opacity = (o * o).toFixed(3);
        el.style.visibility = o > 0.01 ? "visible" : "hidden";
        el.style.transform = "translateY(" + (dd * -70).toFixed(1) + "px)";
        el.style.filter = o > 0.01 ? "blur(" + ((1 - o) * 12).toFixed(1) + "px)" : "";
        var on = Math.abs(dd) < 0.42;
        el.classList.toggle("on", on);
        if (on && s === 3) countUp(el);
      }

      renderer.render(scene, camera);
    }
    requestAnimationFrame(frame);
  }

  /* ====================================================================== */
  /*  LEAD CATCHER — static-site honest version                             */
  /* ====================================================================== */
  var lead = document.getElementById("lead");
  if (lead) {
    lead.addEventListener("submit", function (e) {
      e.preventDefault();
      var gv = function (id) { return (document.getElementById(id).value || "").trim(); };
      var name = gv("f-name"), biz = gv("f-biz"), pain = gv("f-pain");
      var budget = (lead.querySelector('input[name="budget"]:checked') || {}).value || "Not sure yet";
      var subject = "My Tuesday — " + (biz || name || "new enquiry");
      var body = "Hi Leanta,\n\nName: " + (name || "—") +
        "\nBusiness + town: " + (biz || "—") +
        "\nWhat eats my week: " + (pain || "—") +
        "\nWhere I'd start: " + budget +
        "\n\n(Sent from the story page — please reply by message, no call.)";
      var alt = document.getElementById("lead-alt");
      alt.innerHTML = "";
      if (cfg.contactPhone) {
        var wa = document.createElement("a");
        wa.className = "btn-x ghost"; wa.setAttribute("data-hover", "");
        wa.href = "https://wa.me/" + cfg.contactPhone.replace(/[^0-9]/g, "") + "?text=" + encodeURIComponent(body);
        wa.textContent = "WhatsApp it instead"; wa.rel = "noopener";
        var sm = document.createElement("a");
        sm.className = "btn-x ghost"; sm.setAttribute("data-hover", "");
        sm.href = "sms:" + cfg.contactPhone + "?&body=" + encodeURIComponent(body);
        sm.textContent = "Text it";
        alt.appendChild(wa); alt.appendChild(sm);
      }
      document.getElementById("lead-done").hidden = false;
      location.href = "mailto:" + (cfg.contactEmail || "hello@leanta.ie") +
        "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    });
  }

  /* ====================================================================== */
  /*  LEA — pet companion + assistant                                       */
  /*  Avatar: LEANTA.ommaPetUrl (Omma/Spline scene embed) when set;         */
  /*  otherwise the built-in SVG sprout-pet below.                          */
  /*  Brain: on-device retrieval over site facts. LEA_UPGRADE: replace      */
  /*  the body of botReply() with fetch("/api/lea") → serverless → model,   */
  /*  keeping the same {text, links} contract and the disclosure header.    */
  /* ====================================================================== */
  var orb = document.getElementById("lea-orb");
  var panelLea = document.getElementById("lea");
  var msgs = document.getElementById("lea-msgs");
  var chipsBox = document.getElementById("lea-chips");
  var leaForm = document.getElementById("lea-form");
  var leaInput = document.getElementById("lea-input");

  /* --- avatar --- */
  var PET_SVG =
    '<svg viewBox="0 0 100 100" aria-hidden="true">' +
    '<defs><radialGradient id="lg" cx="38%" cy="30%" r="80%">' +
    '<stop offset="0%" stop-color="#3ddca8"/><stop offset="55%" stop-color="#1db887"/>' +
    '<stop offset="100%" stop-color="#005a3c"/></radialGradient></defs>' +
    '<g class="pet">' +
    '<path class="sprout" d="M50 16 C50 8 56 5 61 6 C60 12 56 15 50 16 Z" fill="#e7cd72"/>' +
    '<line x1="50" y1="22" x2="50" y2="13" stroke="#e7cd72" stroke-width="2.4" stroke-linecap="round"/>' +
    '<ellipse class="body" cx="50" cy="58" rx="30" ry="27" fill="url(#lg)"/>' +
    '<ellipse cx="38" cy="66" rx="5" ry="3" fill="#e06a5e" opacity=".22"/>' +
    '<ellipse cx="62" cy="66" rx="5" ry="3" fill="#e06a5e" opacity=".22"/>' +
    '<g class="eye eL"><ellipse cx="40" cy="54" rx="7.2" ry="8.4" fill="#f7f4ea"/>' +
    '<circle class="pup" cx="40" cy="55" r="3.4" fill="#10231c"/></g>' +
    '<g class="eye eR"><ellipse cx="60" cy="54" rx="7.2" ry="8.4" fill="#f7f4ea"/>' +
    '<circle class="pup" cx="60" cy="55" r="3.4" fill="#10231c"/></g>' +
    '<path class="mouth" d="M44 69 Q50 74 56 69" stroke="#0b2d22" stroke-width="2.4" fill="none" stroke-linecap="round"/>' +
    '<ellipse cx="38" cy="84" rx="6" ry="3.2" fill="#005a3c"/>' +
    '<ellipse cx="62" cy="84" rx="6" ry="3.2" fill="#005a3c"/>' +
    '</g></svg>';

  if (orb) {
    var core = orb.querySelector(".core");
    if (cfg.ommaPetUrl) {
      /* Samuel's remixed Omma/Spline pet — drops straight in */
      var fr = document.createElement("iframe");
      fr.src = cfg.ommaPetUrl; fr.title = "Lea — Leanta's pet assistant";
      fr.loading = "lazy"; fr.setAttribute("frameborder", "0");
      fr.style.cssText = "position:absolute;inset:0;width:100%;height:100%;border-radius:50%;pointer-events:none;";
      core.style.background = "transparent"; core.style.boxShadow = "none";
      core.appendChild(fr);
    } else {
      core.innerHTML = PET_SVG;
      /* blink + look-at-cursor for the built-in pet */
      var pups = core.querySelectorAll(".pup"), eyes = core.querySelectorAll(".eye");
      if (!reduced) {
        addEventListener("pointermove", function (e) {
          var r = orb.getBoundingClientRect();
          var dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
          var len = Math.max(40, Math.hypot(dx, dy));
          var ox = (dx / len) * 2.4, oy = (dy / len) * 2.4;
          pups.forEach(function (pp) { pp.style.transform = "translate(" + ox + "px," + oy + "px)"; });
        }, { passive: true });
        (function blink() {
          eyes.forEach(function (ey) { ey.style.transform = "scaleY(.08)"; });
          setTimeout(function () {
            eyes.forEach(function (ey) { ey.style.transform = ""; });
          }, 140);
          setTimeout(blink, 2600 + Math.random() * 3200);
        })();
      }
    }
  }

  /* --- brain: curated site facts (everything verifiable on this site) --- */
  var KB = [
    { k: ["price", "cost", "much", "toolkit", "toolkits", "pack", "packs", "buy"],
      a: "Toolkits are one-time purchases, no subscription: Readiness Check €29 · Compliance Pack €34 · Operations & GP €49 · Pro Bundle €69 (a genuine €14 saving) · single tools from €15. Free demo workbooks are on every product page.",
      l: [["Browse the toolkits", "/index.html#products"]] },
    { k: ["inside", "contain", "include", "workbook", "excel", "spreadsheet"],
      a: "Each toolkit is a finished Excel/Sheets workbook: compliance records (HACCP, allergens, temps, fire, training), operations sheets (GP%, labour, cashflow) and a dashboard where every tile prescribes the next action. Every screenshot on the site is the real workbook — nothing mocked up.",
      l: [["See a product page", "/products/p13.html"]] },
    { k: ["quiz", "readiness", "check", "pass", "inspection", "inspector", "test"],
      a: "The free readiness check takes 2 minutes: pick your industry, answer 10 questions, get a traffic-light verdict on screen immediately. It runs entirely in your browser — nothing is sent anywhere unless you choose to message us the result.",
      l: [["Take the readiness check", "/quiz.html"]] },
    { k: ["200", "grant", "pathway", "leo", "funding", "voucher", "digital"],
      a: "The €200 pathway: €200 mobilises the on-site process audit plus a complete, application-ready grant pack for your Local Enterprise Office (Digital for Business · Grow Digital Voucher up to €5,000 at 50% · Lean for Micro). Approved → the scheme carries its share and your €200 is credited. Not approved → you keep all the work and decide freely. We never promise approval — that's the LEO's call.",
      l: [["The grant pathway", "/grants.html"]] },
    { k: ["agency", "service", "automation", "visit", "audit", "onsite"],
      a: "The agency side: we drive out, map one painful process where it happens, and rebuild it in front of you — old way, new way, measured. Lean Six Sigma method with modern AI tooling, GDPR-first, in your own accounts.",
      l: [["Agency services", "/services.html"]] },
    { k: ["contact", "phone", "call", "reach", "talk", "speak", "human", "person", "samuel"],
      a: "We're message-first: email hello@leanta.ie or any \"message us\" button — a human replies, usually within a working day. No phone calls unless you ask for one. Want me to hand you over now?",
      l: [["Email us", "mailto:hello@leanta.ie"]] },
    { k: ["refund", "return", "guarantee", "terms", "licence", "license", "withdrawal"],
      a: "Terms, licence and refunds (including your EU withdrawal rights) are written in plain language on the terms page — no tricks, EU consumer law applies.",
      l: [["Terms & refunds", "/legal/terms.html"]] },
    { k: ["privacy", "gdpr", "data", "tracking", "cookies"],
      a: "The site runs without tracking, the quiz runs entirely in your browser, and this chat never leaves your device either. You message us first — that's your consent for a reply; we delete threads on request.",
      l: [["Privacy", "/legal/privacy.html"]] },
    { k: ["bot", "robot", "ai", "model", "lea", "who"],
      a: "Honest answer (EU AI Act and all): I'm Lea, an automated assistant — a scripted helper answering from this site's own content, nothing more. Not a human, never pretending to be one. Ask for a human any time and I'll hand you straight over.",
      l: [] },
    { k: ["update", "free", "forever", "subscription", "monthly"],
      a: "Toolkits are one-time purchases with free regulatory updates — when a rule changes, the fix comes to you at no charge. No subscription trap.",
      l: [] },
    { k: ["sheets", "google", "libreoffice", "compatible", "version", "mac"],
      a: "Workbooks are built for Excel and import cleanly to Google Sheets; LibreOffice opens them too — formulas and formatting are kept deliberately portable.",
      l: [] },
    { k: ["where", "based", "ferns", "wexford", "ireland", "local", "gorey", "enniscorthy"],
      a: "Leanta is based in Ferns, Co. Wexford and works the surrounding 30 km — Enniscorthy, Bunclody, Gorey, Camolin, Courtown and around. Close enough to actually drive out.",
      l: [] },
    { k: ["video", "film", "case", "proof", "demo"],
      a: "The case films show one real process rebuilt on camera — old way, new way, outcome in minutes. They're AI-assisted productions and labelled as such; the workbook footage inside is always the real thing.",
      l: [] },
    { k: ["music", "sound", "audio", "song", "suno"],
      a: "The sound toggle (bottom-left) plays the ambient theme — off until you turn it on. The full Suno-made track is on its way; headphones recommended.",
      l: [] },
    { k: ["haccp", "allergen", "allergens", "temperature", "fire", "safety", "training", "traceability"],
      a: "Covered: HACCP plans, 14-allergen matrices, temperature logs, fire registers, safety statements, training matrices and supplier traceability — the records inspectors actually ask for, designed so they take seconds to keep.",
      l: [["Which pack fits? Take the check", "/quiz.html"]] },
    { k: ["hello", "hi", "hey", "morning", "evening"],
      a: "Hello! Ask me about the toolkits, the free readiness check, or the €200 grant pathway — or say \"human\" and I'll hand you over to a real person.",
      l: [] }
  ];

  function answer(qRaw) {
    var q = qRaw.toLowerCase().replace(/[^\wÀ-ž€ ]/g, " ");
    var words = q.split(/\s+/).filter(Boolean);
    var best = null, bestScore = 0;
    KB.forEach(function (entry) {
      var s = 0;
      entry.k.forEach(function (kw) {
        if (words.indexOf(kw) !== -1) s += 2;
        else if (q.indexOf(kw) !== -1) s += 1;
      });
      if (s > bestScore) { bestScore = s; best = entry; }
    });
    if (best && bestScore >= 2) return { text: best.a, links: best.l };
    var handoff = [["Email a human", "mailto:" + (cfg.contactEmail || "hello@leanta.ie") +
      "?subject=" + encodeURIComponent("Question from the story page") +
      "&body=" + encodeURIComponent("Hi Leanta — I asked Lea: \"" + qRaw + "\" — could a human pick this up?")]];
    if (cfg.contactPhone) {
      handoff.unshift(["WhatsApp a human", "https://wa.me/" + cfg.contactPhone.replace(/[^0-9]/g, "") +
        "?text=" + encodeURIComponent("Hi Leanta — I asked Lea: \"" + qRaw + "\"")]);
    }
    return {
      text: "That one's beyond my script — I only know what's on this site. A human will know though: message us and Samuel replies within a working day (no call unless you ask).",
      links: handoff
    };
  }

  function addMsg(text, who, links) {
    var d = document.createElement("div");
    d.className = "msg " + who;
    d.textContent = text;
    if (links && links.length) {
      links.forEach(function (ln) {
        d.appendChild(document.createElement("br"));
        var a = document.createElement("a");
        a.href = ln[1]; a.textContent = "→ " + ln[0]; a.setAttribute("data-hover", "");
        if (ln[1].indexOf("http") === 0) a.rel = "noopener";
        d.appendChild(a);
      });
    }
    msgs.appendChild(d);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function botReply(q) {
    var typing = document.createElement("div");
    typing.className = "msg bot typing";
    typing.innerHTML = "<i></i><i></i><i></i>";
    msgs.appendChild(typing); msgs.scrollTop = msgs.scrollHeight;
    var res = answer(q); /* LEA_UPGRADE: replace with fetch("/api/lea") */
    setTimeout(function () {
      typing.remove();
      addMsg(res.text, "bot", res.links);
    }, 480 + Math.min(900, q.length * 14));
  }

  if (orb && panelLea) {
    var CHIPS = ["What do toolkits cost?", "How does the €200 pathway work?", "Will I pass an inspection?", "Talk to a human"];
    CHIPS.forEach(function (cq) {
      var b = document.createElement("button");
      b.type = "button"; b.textContent = cq; b.setAttribute("data-hover", "");
      b.addEventListener("click", function () { addMsg(cq, "user"); botReply(cq); });
      chipsBox.appendChild(b);
    });

    var greeted = false;
    var toggleLea = function (open) {
      panelLea.hidden = !open;
      orb.setAttribute("aria-expanded", String(open));
      if (open) {
        if (!greeted) {
          greeted = true;
          addMsg("Hi — I'm Lea, Leanta's automated helper (not a human, happy to fetch one). What's eating your week?", "bot");
        }
        leaInput.focus();
      }
    };
    orb.addEventListener("click", function () { toggleLea(panelLea.hidden); });
    document.getElementById("lea-close").addEventListener("click", function () { toggleLea(false); });
    addEventListener("keydown", function (e) { if (e.key === "Escape" && !panelLea.hidden) toggleLea(false); });

    leaForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var q = leaInput.value.trim();
      if (!q) return;
      leaInput.value = "";
      addMsg(q, "user");
      botReply(q);
    });
  }
})();
