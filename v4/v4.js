/* LEANTA v4.3 — "THE DESCENT" engine.
   Bright glassmorphism story. No three.js, no GSAP — sticky environment
   layers + a light scroll handler. Sections:
   - preloader (radial reveal) · custom cursor · magnetic pull
   - typewriter lines · env descent (bg pan/blur, card reveal, floors)
   - mind-map unfold (IntersectionObserver steps)
   - sound toggle (mp3 swap-in or WebAudio pad) · case video slots
   - lead catcher (mailto/WA/SMS compose — nothing posted by the page)
   - LEA chat + companion pets (Sprout/Penny/Mossy; ommaPetUrl overrides)
   LEA_UPGRADE marks the real-model swap point.                          */

(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced) document.documentElement.classList.add("reduced");
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  /* backgrounds stay STILL until the visitor moves the mouse — then alive */
  var gmx = 0, gmy = 0;                       /* normalized -1..1 */
  addEventListener("pointermove", function (e) {
    if (!document.body.classList.contains("kinetic")) document.body.classList.add("kinetic");
    gmx = (e.clientX / innerWidth - 0.5) * 2;
    gmy = (e.clientY / innerHeight - 0.5) * 2;
  }, { passive: true });

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

  /* ---------- custom cursor + magnetic pull ----------------------------- */
  if (fine && !reduced) {
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

    document.addEventListener("pointermove", function (e) {
      var t = e.target.closest(".btn-x, .chip, .sound, .brandpill, .pcard");
      if (!t) return;
      if (!t.classList.contains("magnet")) t.classList.add("magnet");
      var r = t.getBoundingClientRect();
      var s = t.classList.contains("pcard") ? 6 : 4;
      var dx = ((e.clientX - r.left) / r.width - 0.5) * 2 * s;
      var dy = ((e.clientY - r.top) / r.height - 0.5) * 2 * s;
      t.style.transform = "translate(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px)";
    }, { passive: true });
    document.addEventListener("pointerout", function (e) {
      var t = e.target.closest(".btn-x, .chip, .sound, .brandpill, .pcard");
      if (t && !t.contains(e.relatedTarget)) t.style.transform = "";
    }, { passive: true });
  }

  /* ---------- typewriter ------------------------------------------------- */
  function typewrite(el, txt, speed, done) {
    el.textContent = "";
    var i = 0;
    (function tick() {
      if (i <= txt.length) {
        el.textContent = txt.slice(0, i); i++;
        setTimeout(tick, speed + Math.random() * 28);
      } else if (done) { done(); }
    })();
  }
  var typeline = document.getElementById("typeline");
  if (typeline && !reduced) {
    setTimeout(function () { typewrite(typeline, typeline.getAttribute("data-type"), 34); },
      sessionStorage.getItem("v4seen") === "1" && pre && !pre.classList.contains("done") ? 2400 : 600);
  } else if (typeline) {
    typeline.textContent = typeline.getAttribute("data-type");
  }

  /* env eyebrows retype each time their environment goes live */
  function typeEyebrow(env) {
    if (reduced) return;
    var ty = env.querySelector(".ty");
    if (ty && ty.getAttribute("data-done") !== "1") {
      ty.setAttribute("data-done", "1");
      typewrite(ty, ty.getAttribute("data-type"), 26);
    }
    var tcl = env.querySelector(".tcl");
    if (tcl && tcl.getAttribute("data-done") !== "1") {
      tcl.setAttribute("data-done", "1");
      setTimeout(function () {
        typewrite(tcl, tcl.getAttribute("data-type"), 30, function () { tcl.classList.add("done"); });
      }, 700);
    }
  }

  /* ---------- char-stagger titles ---------------------------------------- */
  document.querySelectorAll(".env .title").forEach(function (t) {
    if (reduced) return;
    var frag = document.createDocumentFragment(), n = 0;
    Array.prototype.slice.call(t.childNodes).forEach(function (node) {
      if (node.nodeType === 3) {
        var txt = node.textContent;
        for (var ci = 0; ci < txt.length; ci++) {
          var sp = document.createElement("span");
          sp.className = "chx";
          sp.textContent = txt[ci] === " " ? " " : txt[ci];
          sp.style.transitionDelay = (n * 26) + "ms"; n++;
          frag.appendChild(sp);
        }
      } else { frag.appendChild(node.cloneNode(true)); }
    });
    t.setAttribute("aria-label", t.textContent);
    t.textContent = ""; t.appendChild(frag);
  });

  /* ---------- hero background: image + mouse parallax -------------------- */
  var hbImg = document.querySelector(".hb-img");
  if (hbImg) hbImg.style.backgroundImage = "url('" + hbImg.getAttribute("data-img") + "')";
  if (hbImg && fine && !reduced) {
    var hpx = 0, hpy = 0;
    (function heroPar() {
      hpx += (gmx - hpx) * 0.04; hpy += (gmy - hpy) * 0.04;
      hbImg.style.transform = "translate(" + (hpx * -18) + "px," + (hpy * -12) + "px) scale(1.04)";
      requestAnimationFrame(heroPar);
    })();
  }

  /* ---------- the mesh field --------------------------------------------- */
  /* Samuel's spec (10/06 eve): a SYMMETRICAL mesh of dots (Stitch-wave DNA)
     with real depth — a 3D dot lattice projected in perspective, undulating
     in layered sine waves; the camera DOLLIES ALONG Z as you scroll (and
     drifts forward on its own once kinetic); dots near the cursor SWARM
     (tangential shimmer) and change colour ink → emerald. Dependency-free
     Canvas2D with manual perspective projection. House rules kept: still
     until body.kinetic, IO-paused off-screen, static frame under
     prefers-reduced-motion, reduced lattice on mobile.                      */
  function initDust(canvas, opts) {
    var ctxD = canvas.getContext && canvas.getContext("2d");
    if (!ctxD) return;
    opts = opts || {};
    var DPR = Math.min(devicePixelRatio || 1, 1.75);
    var mob = window.matchMedia("(max-width: 1023px)").matches;
    var COLS = Math.round((opts.cols || 76) * (mob ? 0.55 : 1));
    var ROWS = Math.round((opts.rows || 44) * (mob ? 0.55 : 1));
    var GAP = (opts.gap || 30) * DPR;
    var FOV = 460 * DPR, NEAR = 50 * DPR, CAMH = 150 * DPR;
    var DEPTH = ROWS * GAP;
    var W = 0, H = 0, cx = 0, hor = 0, inView = true, ramp = 0, drawnStill = false;
    var mxp = -1e4, myp = -1e4, R = 120 * DPR, R2 = R * R;
    var camZ = 0, scrollZ = 0;

    function seed() {
      var host = canvas.parentElement;
      W = Math.max(1, host.clientWidth); H = Math.max(1, host.clientHeight);
      canvas.width = W * DPR; canvas.height = H * DPR;
      cx = canvas.width / 2; hor = canvas.height * 0.40;
      drawnStill = false;
    }
    function draw(time, animate) {
      ctxD.clearRect(0, 0, canvas.width, canvas.height);
      var t = time * 0.001;
      var dolly = camZ + scrollZ;
      for (var r = 0; r < ROWS; r++) {
        var zw = ((r * GAP - dolly) % DEPTH + DEPTH) % DEPTH;
        var s = FOV / (FOV + zw + NEAR);
        if (s < 0.12) continue;
        var rowAlpha = Math.min(0.55, Math.max(0, s * 1.35 - 0.12));
        var size = Math.max(0.6, 2.3 * DPR * s);
        for (var c = 0; c < COLS; c++) {
          var x = (c - (COLS - 1) / 2) * GAP;
          var y = (Math.sin(c * 0.55 + t * 1.1) * 9 +
                   Math.sin(r * 0.50 - t * 0.8) * 7 +
                   Math.sin((c + r) * 0.32 + t * 0.6) * 5) * DPR;
          var sx = cx + x * s;
          var sy = hor + (y + CAMH) * s;
          if (sx < -8 || sx > canvas.width + 8 || sy < -8 || sy > canvas.height + 8) continue;
          var f = 0;
          if (animate && mxp > -1e3) {
            var dx = sx - mxp, dy = sy - myp, d2 = dx * dx + dy * dy;
            if (d2 < R2) {
              f = 1 - Math.sqrt(d2) / R;
              /* swarm: tangential shimmer around the cursor */
              var ang = Math.atan2(dy, dx) + 1.25;
              var disp = f * 20 * DPR * (0.6 + 0.4 * Math.sin(t * 3.1 + c * 1.3 + r * 0.7));
              sx += Math.cos(ang) * disp;
              sy += Math.sin(ang) * disp;
            }
          }
          /* hover colour: ink → emerald */
          ctxD.fillStyle = f > 0.01
            ? "rgba(" + Math.round(21 - 11 * f) + "," + Math.round(24 + 114 * f) + "," +
              Math.round(26 + 56 * f) + "," + Math.min(0.9, rowAlpha + 0.35 * f).toFixed(3) + ")"
            : "rgba(21,24,26," + rowAlpha.toFixed(3) + ")";
          ctxD.beginPath();
          ctxD.arc(sx, sy, f > 0.01 ? size * (1 + f * 0.8) : size, 0, 6.2832);
          ctxD.fill();
        }
      }
    }
    seed();
    addEventListener("resize", seed);
    if (reduced) { draw(0, false); return; }   /* calm static lattice       */
    addEventListener("pointermove", function (e) {
      var rct = canvas.getBoundingClientRect();
      mxp = (e.clientX - rct.left) * DPR; myp = (e.clientY - rct.top) * DPR;
    }, { passive: true });
    addEventListener("scroll", function () {   /* Z-axis camera move        */
      scrollZ = (window.scrollY || 0) * 0.45 * DPR;
    }, { passive: true });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (en) { inView = en.isIntersecting; });
      }, { rootMargin: "80px" }).observe(canvas);
    }
    (function loop(t) {
      requestAnimationFrame(loop);
      if (!inView || document.hidden) return;
      var target = document.body.classList.contains("kinetic") ? 1 : 0;
      ramp += (target - ramp) * 0.02;
      if (ramp > 0.004) {
        camZ += 0.4 * DPR * ramp;              /* gentle self-dolly forward */
        draw(t, true);
      } else if (!drawnStill) { draw(0, false); drawnStill = true; }
    })(0);
  }
  document.querySelectorAll("canvas.dust").forEach(function (c) {
    initDust(c, c.getAttribute("data-dust") === "hero"
      ? { cols: 76, rows: 44, gap: 30 }
      : { cols: 60, rows: 26, gap: 34 });
  });

  /* ---------- THE DESCENT — scroll engine -------------------------------- */
  var envs = Array.prototype.slice.call(document.querySelectorAll(".env"));
  var floors = document.querySelectorAll("#floors span");
  var progressBar = document.querySelector("#progress i");
  var desktop = window.matchMedia("(min-width: 1024px)").matches;

  envs.forEach(function (env) {           /* lazy-set the backdrop images */
    var bg = env.querySelector(".bg");
    if (bg) bg.style.backgroundImage = "url('" + bg.getAttribute("data-img") + "')";
  });

  /* ---------- environment loop videos (still → motion on mouse) ----------- */
  /* Each backdrop is a calm photo until a matching `<name>-loop.mp4` lands
     beside it; then it becomes a silent 5-s loop that starts on the first
     mouse move (Samuel's spec + the house "still until kinetic" rule).
     A `<name>-amb.mp3` ambient bed is a documented follow-up (gated by the
     sound toggle). Reduced-motion keeps the still. Files auto-mount — no
     code change needed when they appear. */
  var bgLoops = [];
  function mountLoop(host, stillPath) {
    if (!host || !stillPath || reduced) return;
    var loop = stillPath.replace(/\.jpg$/i, "-loop.mp4");
    fetch(loop, { method: "HEAD" }).then(function (r) {
      if (!r.ok) return;
      var v = document.createElement("video");
      v.src = loop; v.muted = true; v.loop = true; v.playsInline = true;
      v.setAttribute("playsinline", ""); v.preload = "auto"; v.className = "bgloop";
      host.appendChild(v);
      bgLoops.push(v);
      if (document.body.classList.contains("kinetic")) v.play().catch(function () {});
    }).catch(function () {});
  }
  envs.forEach(function (env) {
    var bg = env.querySelector(".bg");
    if (bg) mountLoop(bg, bg.getAttribute("data-img"));
  });
  if (hbImg) mountLoop(hbImg, hbImg.getAttribute("data-img"));
  addEventListener("pointermove", function playLoops() {
    removeEventListener("pointermove", playLoops);
    bgLoops.forEach(function (v) { v.play().catch(function () {}); });
  }, { passive: true });

  function setFloor(fl) {
    floors.forEach(function (s) { s.classList.toggle("on", s.getAttribute("data-fl") === String(fl)); });
  }
  setFloor(0);

  var ticking = false;
  function onScroll() {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      var h = document.documentElement;
      var pTot = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight);
      if (progressBar) progressBar.style.width = (pTot * 100).toFixed(2) + "%";

      var current = 0;
      envs.forEach(function (env, i) {
        var r = env.getBoundingClientRect();
        var inside = r.top < innerHeight * 0.5 && r.bottom > innerHeight * 0.5;
        var live = r.top < innerHeight * 0.7 && r.bottom > innerHeight * 0.45;
        if (live && !env.classList.contains("live")) { env.classList.add("live"); typeEyebrow(env); }
        if (inside) current = i + 1;
        if (desktop && !reduced) {
          /* TRUE Z-axis dolly (Valentime architecture, CSS perspective):
             the room starts deep in Z and flies PAST the camera as you
             scroll — real depth, not a zoom. Pin has perspective:1100px. */
          var t = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - innerHeight)));
          var bg = env.querySelector(".bg");
          if (bg && r.bottom > 0 && r.top < innerHeight) {
            var z = -150 + t * 520;                     /* far → through us */
            bg.style.transform = "translate3d(" + (gmx * -14) + "px," +
              ((gmy * -8) + (t - 0.5) * -26) + "px," + z.toFixed(1) + "px)";
            var exit = Math.max(0, (t - 0.82) / 0.18);  /* through the far wall */
            bg.style.filter = exit > 0 ? "blur(" + (exit * 12).toFixed(1) + "px) brightness(" + (1 + exit * 0.1).toFixed(2) + ")" : "";
          }
        }
      });
      setFloor(current);
    });
  }
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- mind map unfold -------------------------------------------- */
  var mind = document.getElementById("mind");
  if (mind && !reduced) {
    /* the map DEVELOPS as you scroll through it: root → branches → leaves */
    addEventListener("scroll", function () {
      var r = mind.getBoundingClientRect();
      var vis = Math.min(1, Math.max(0, (innerHeight * 0.85 - r.top) / (r.height * 0.9)));
      mind.classList.toggle("s0", vis > 0.1);
      mind.classList.toggle("s1", vis > 0.42);
      mind.classList.toggle("s2", vis > 0.72);
    }, { passive: true });
    /* 3D float: the board tilts toward the cursor (perspective on .mindwrap) */
    if (fine) {
      var mtx = 0, mty = 0;
      (function mindTilt() {
        requestAnimationFrame(mindTilt);
        if (!document.body.classList.contains("kinetic")) return;
        mtx += (gmx - mtx) * 0.06; mty += (gmy - mty) * 0.06;
        mind.style.transform = "rotateX(" + (7 - mty * 6).toFixed(2) +
          "deg) rotateY(" + (mtx * 9).toFixed(2) + "deg)";
      })();
    }
  } else if (mind) {
    mind.classList.add("s0", "s1", "s2");
  }

  /* ---------- reveals ----------------------------------------------------- */
  if ("IntersectionObserver" in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.18 });
    document.querySelectorAll(".rv").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".rv").forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- sound: always-visible toggle ------------------------------ */
  var soundBtn = document.getElementById("sound");
  var soundLabel = document.getElementById("sound-label");
  var modeBtn = document.getElementById("soundmode");
  var modeLabel = document.getElementById("soundmode-label");
  var SRC = { ambient: "/v4/assets/leanta-theme.mp3", focus: "/v4/assets/leanta-focus.mp3" };
  var mode = "ambient";          /* ambient | focus (ADHD focus-enforcing) */
  var engines = {};              /* per-mode engine cache */
  var engine = null;
  var playing = false;

  function mp3Engine(src) {
    var a = new Audio(src); a.loop = true; a.volume = 0.35;
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
  /* ADHD focus pad — steady 8th-note pulse, narrow band, no surprises */
  function focusPadEngine() {
    var ctx = null, master = null, seqTimer = null, stepN = 0;
    function build() {
      ctx = new (window.AudioContext || window.webkitAudioContext)();
      master = ctx.createGain(); master.gain.value = 0.0001; master.connect(ctx.destination);
      var filter = ctx.createBiquadFilter(); filter.type = "lowpass";
      filter.frequency.value = 900; filter.Q.value = 0.5; filter.connect(master);
      var drone = ctx.createOscillator(), dg = ctx.createGain();
      drone.type = "sine"; drone.frequency.value = 98; dg.gain.value = 0.5;
      drone.connect(dg); dg.connect(filter); drone.start();
      var NOTES = [196, 246.9, 293.7, 246.9, 196, 293.7, 392, 293.7]; /* G pentatonic-ish loop */
      function step() {
        if (!ctx) return;
        var o = ctx.createOscillator(), g = ctx.createGain();
        o.type = "triangle"; o.frequency.value = NOTES[stepN % NOTES.length]; stepN++;
        g.gain.setValueAtTime(0.05, ctx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.32);
        o.connect(g); g.connect(filter); o.start(); o.stop(ctx.currentTime + 0.35);
        seqTimer = setTimeout(step, 333); /* 90 BPM eighths — steady, hypnotic */
      }
      step();
    }
    return {
      start: function () {
        if (!ctx) build();
        if (ctx.state === "suspended") ctx.resume();
        master.gain.cancelScheduledValues(ctx.currentTime);
        master.gain.exponentialRampToValueAtTime(0.06, ctx.currentTime + 0.8);
      },
      stop: function () {
        if (!ctx) return;
        master.gain.cancelScheduledValues(ctx.currentTime);
        master.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.4);
        clearTimeout(seqTimer);
      }
    };
  }

  function engineFor(m, cb) {
    if (engines[m]) { cb(engines[m]); return; }
    fetch(SRC[m], { method: "HEAD" }).then(function (r) {
      engines[m] = r.ok ? mp3Engine(SRC[m]) : (m === "focus" ? focusPadEngine() : padEngine());
      if (r.ok) soundBtn.title = "Studio track by Suno — off until you ask.";
      cb(engines[m]);
    }).catch(function () {
      engines[m] = (m === "focus" ? focusPadEngine() : padEngine());
      cb(engines[m]);
    });
  }

  soundBtn.addEventListener("click", function () {
    playing = soundBtn.classList.toggle("on");
    soundBtn.setAttribute("aria-pressed", String(playing));
    soundLabel.textContent = playing ? "Music on" : "Music off";
    if (playing) engineFor(mode, function (en) { engine = en; en.start(); });
    else if (engine) engine.stop();
  });
  if (modeBtn) modeBtn.addEventListener("click", function () {
    mode = mode === "ambient" ? "focus" : "ambient";
    modeBtn.classList.toggle("focus", mode === "focus");
    modeBtn.setAttribute("aria-pressed", String(mode === "focus"));
    modeLabel.textContent = mode === "focus" ? "Focus" : "Ambient";
    if (playing) {
      if (engine) engine.stop();
      engineFor(mode, function (en) { engine = en; en.start(); });
    }
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

  /* ---------- lead catcher ----------------------------------------------- */
  var cfg = window.LEANTA || { contactEmail: "hello@leanta.ie" };
  var lead = document.getElementById("lead");
  if (lead) {
    lead.addEventListener("submit", function (e) {
      e.preventDefault();
      var gv = function (id) { return (document.getElementById(id).value || "").trim(); };
      var name = gv("f-name"), biz = gv("f-biz"), pain = gv("f-pain"), phone = gv("f-phone");
      var budget = (lead.querySelector('input[name="budget"]:checked') || {}).value || "Not sure yet";
      var subject = "My Tuesday — " + (biz || name || "new enquiry");
      var body = "Hi Leanta,\n\nName: " + (name || "—") +
        "\nBusiness + town: " + (biz || "—") +
        "\nWhat eats my week: " + (pain || "—") +
        (phone ? "\nMobile for SMS plan: " + phone : "") +
        "\nWhere I'd start: " + budget +
        "\n\n(Sent from the story page — please reply by message, no call.)";

      /* Twilio capture — serverless first; mailto is the always-works fallback */
      fetch("/api/capture", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, biz: biz, pain: pain, phone: phone, budget: budget })
      }).then(function (r) {
        if (r.ok) {
          var done = document.getElementById("lead-done");
          done.hidden = false;
          done.textContent = phone
            ? "Got it — your action plan lands by SMS within a working day. (A copy is drafting in your mail app too.)"
            : "Got it — we reply within a working day. (A copy is drafting in your mail app too.)";
        }
      }).catch(function () {});
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

  /* live form polish — green tick the moment a field is filled */
  document.querySelectorAll(".fld input").forEach(function (inp) {
    inp.addEventListener("input", function () {
      inp.parentElement.classList.toggle("filled", inp.value.trim().length > 1);
    });
  });

  /* ====================================================================== */
  /*  COMPANIONS — three cute pets; the pick rides the Lea orb.             */
  /*  Samuel's Omma scene (LEANTA.ommaPetUrl) overrides everything.         */
  /* ====================================================================== */
  /* the shared face — eyes (with catch-light), rosy cheeks, and one mouth per
     mood; CSS shows the active mouth/lid from the svg's data-mood. */
  function petFace() {
    return (
      '<ellipse class="cheek" cx="35" cy="63" rx="6" ry="3.6" fill="#ff7a66"/>' +
      '<ellipse class="cheek" cx="65" cy="63" rx="6" ry="3.6" fill="#ff7a66"/>' +
      '<g class="eye eL">' +
        '<ellipse class="ball" cx="40" cy="53" rx="7.8" ry="9.2" fill="#fff"/>' +
        '<circle class="pup" cx="40" cy="55" r="4.1" fill="#15181a"/>' +
        '<circle class="cl" cx="37.6" cy="50.6" r="1.8" fill="#fff"/>' +
        '<path class="lid" d="M32 54 Q40 48 48 54" stroke="#15181a" stroke-width="2.6" fill="none" stroke-linecap="round"/>' +
      '</g>' +
      '<g class="eye eR">' +
        '<ellipse class="ball" cx="60" cy="53" rx="7.8" ry="9.2" fill="#fff"/>' +
        '<circle class="pup" cx="60" cy="55" r="4.1" fill="#15181a"/>' +
        '<circle class="cl" cx="57.6" cy="50.6" r="1.8" fill="#fff"/>' +
        '<path class="lid" d="M52 54 Q60 48 68 54" stroke="#15181a" stroke-width="2.6" fill="none" stroke-linecap="round"/>' +
      '</g>' +
      '<path class="mouth m-idle" d="M44 69 Q50 74 56 69" stroke="#15181a" stroke-width="2.6" fill="none" stroke-linecap="round"/>' +
      '<path class="mouth m-happy" d="M41 67 Q50 81 59 67 Q50 72 41 67 Z" fill="#15181a"/>' +
      '<ellipse class="mouth m-talk" cx="50" cy="70" rx="4.6" ry="3.2" fill="#15181a"/>' +
      '<circle class="mouth m-surp" cx="50" cy="71" r="3.5" fill="#15181a"/>' +
      '<path class="mouth m-sleep" d="M46 71 Q50 73.5 54 71" stroke="#15181a" stroke-width="2.2" fill="none" stroke-linecap="round"/>' +
      '<g class="zzz"><text x="68" y="33" class="z1">z</text><text x="77" y="25" class="z2">z</text></g>'
    );
  }
  function petSVG(body1, body2, accent, kind) {
    /* gradient id must be unique per palette, not per kind — Nova and Penny
       are both "fox", so a shared "pgfox" id makes one steal the other's
       colour wherever both svgs live in the DOM (pickers + orb). */
    var gid = "pg" + kind + body1.replace(/[^a-z0-9]/gi, "") + body2.replace(/[^a-z0-9]/gi, "");
    var fill = 'url(#' + gid + ')';
    var open =
      '<svg viewBox="0 0 100 100" data-mood="idle" aria-hidden="true">' +
      '<defs><radialGradient id="' + gid + '" cx="38%" cy="28%" r="82%">' +
      '<stop offset="0%" stop-color="' + body1 + '"/><stop offset="100%" stop-color="' + body2 + '"/>' +
      '</radialGradient></defs>' +
      '<ellipse class="shadow" cx="50" cy="93" rx="25" ry="4.4" fill="#15181a" opacity=".12"/>' +
      '<g class="pet">';
    var close = '</g></svg>';
    var gloss = '<ellipse class="gloss" cx="39" cy="46" rx="11" ry="7.5" fill="#fff" opacity=".26"/>';
    if (kind === "sprout") return open +
      '<path d="M50 15 C50 6 57 3 63 4 C61 11 56 15 50 16 Z" fill="' + accent + '"/>' +
      '<line x1="50" y1="22" x2="50" y2="12" stroke="' + accent + '" stroke-width="2.6" stroke-linecap="round"/>' +
      '<ellipse cx="50" cy="58" rx="31" ry="28" fill="' + fill + '"/>' + gloss +
      '<ellipse cx="38" cy="86" rx="6.2" ry="3.3" fill="' + body2 + '"/>' +
      '<ellipse cx="62" cy="86" rx="6.2" ry="3.3" fill="' + body2 + '"/>' + petFace() + close;
    if (kind === "fox") return open +
      '<path d="M27 35 L21 14 L43 27 Z" fill="' + fill + '"/>' +
      '<path d="M73 35 L79 14 L57 27 Z" fill="' + fill + '"/>' +
      '<path d="M28 33 L25 20 L38 28 Z" fill="' + accent + '" opacity=".55"/>' +
      '<path d="M72 33 L75 20 L62 28 Z" fill="' + accent + '" opacity=".55"/>' +
      '<ellipse cx="50" cy="58" rx="31" ry="28" fill="' + fill + '"/>' + gloss +
      '<ellipse cx="50" cy="68" rx="17" ry="13" fill="#fff" opacity=".9"/>' + petFace() +
      '<ellipse cx="50" cy="63.5" rx="3.6" ry="2.7" fill="' + body2 + '"/>' + close;
    /* sheep */
    return open +
      '<circle cx="32" cy="42" r="11" fill="#fbfaf7"/><circle cx="46" cy="35" r="12.5" fill="#fbfaf7"/>' +
      '<circle cx="62" cy="37" r="11.5" fill="#fbfaf7"/><circle cx="70" cy="48" r="10" fill="#fbfaf7"/>' +
      '<circle cx="28" cy="55" r="10" fill="#fbfaf7"/><circle cx="72" cy="58" r="9.5" fill="#fbfaf7"/>' +
      '<ellipse cx="50" cy="60" rx="29" ry="26" fill="#fbfaf7"/>' +
      '<ellipse cx="50" cy="61" rx="21" ry="19" fill="' + fill + '"/>' + gloss +
      '<path d="M27 50 C19 48 17 41 22 37 C28 39 30 45 27 50 Z" fill="' + body2 + '"/>' +
      '<path d="M73 50 C81 48 83 41 78 37 C72 39 70 45 73 50 Z" fill="' + body2 + '"/>' + petFace() + close;
  }
  var PETS = [
    { id: "sprout", name: "Lea", title: "Lea the sprout", svg: petSVG("#3ddca8", "#0a8a52", "#d7a900", "sprout") },
    { id: "fox",    name: "Penny", title: "Penny the fox", svg: petSVG("#ff9d5c", "#c45f1e", "#15181a", "fox") },
    { id: "sheep",  name: "Mossy", title: "Mossy the sheep", svg: petSVG("#bcb6a8", "#7d7669", "#15181a", "sheep") }
  ];
  /* Nova — Samuel's Omma pink space-fox, self-hosted GLB from the published
     scene (omma.build/p/vary-blink-voice-react-b1rqnk). Rendered with
     model-viewer (lazy-loaded, pinned). LEANTA.ommaPetUrl iframe still wins
     if Omma ever allows embedding. */
  var NOVA_GLB = "/v4/assets/omma/nova.glb";
  PETS.unshift({ id: "omma", name: "Nova", title: "Nova — the Omma companion",
    omma: true, svg: petSVG("#ff4fa3", "#b3186e", "#fff", "fox") });
  var petChoice = "omma";
  try { petChoice = localStorage.getItem("v4pet") || petChoice; } catch (err) {}

  var mvLoaded = false;
  function ensureModelViewer(cb) {
    if (mvLoaded || window.customElements && customElements.get("model-viewer")) { cb(); return; }
    var sc = document.createElement("script");
    sc.type = "module";
    sc.src = "https://unpkg.com/@google/model-viewer@3.5.0/dist/model-viewer.min.js";
    sc.onload = function () { mvLoaded = true; cb(); };
    document.head.appendChild(sc);
  }

  var orb = document.getElementById("lea-orb");
  var orbCore = orb ? orb.querySelector(".core") : null;
  var orbLbl = orb ? orb.querySelector(".lbl") : null;

  function currentPet() {
    for (var i = 0; i < PETS.length; i++) if (PETS[i].id === petChoice) return PETS[i];
    return PETS[0];
  }
  function renderOrbPet() {
    if (!orbCore) return;
    if (petChoice === "omma") {
      if (cfg.ommaPetUrl) {              /* live Omma scene, if embeddable */
        var fr = document.createElement("iframe");
        fr.src = cfg.ommaPetUrl; fr.title = "Nova — Leanta's pet assistant";
        fr.loading = "lazy"; fr.setAttribute("frameborder", "0");
        fr.style.pointerEvents = "none";
        orbCore.innerHTML = ""; orbCore.appendChild(fr);
      } else {                           /* self-hosted GLB from the scene */
        ensureModelViewer(function () {
          orbCore.innerHTML = "";
          var mv = document.createElement("model-viewer");
          mv.src = NOVA_GLB; mv.setAttribute("auto-rotate", "");
          mv.setAttribute("rotation-per-second", "24deg");
          mv.setAttribute("disable-zoom", ""); mv.setAttribute("interaction-prompt", "none");
          mv.setAttribute("shadow-intensity", "0");
          mv.setAttribute("camera-orbit", "0deg 82deg 110%");
          mv.style.cssText = "position:absolute;inset:-6%;width:112%;height:112%;background:transparent;pointer-events:none;";
          orbCore.appendChild(mv);
        });
      }
      if (orbLbl) orbLbl.textContent = "Ask Nova";
      return;
    }
    var pet = currentPet();
    orbCore.innerHTML = pet.svg;
    if (orbLbl) orbLbl.textContent = "Ask " + pet.name;
    if (!reduced) {
      var pups = orbCore.querySelectorAll(".pup"), eyes = orbCore.querySelectorAll(".eye");
      (function blink() {
        if (!orbCore.isConnected) return;
        eyes.forEach(function (ey) { ey.style.transform = "scaleY(.08)"; });
        setTimeout(function () { eyes.forEach(function (ey) { ey.style.transform = ""; }); }, 140);
        setTimeout(blink, 2600 + Math.random() * 3200);
      })();
      addEventListener("pointermove", function (e) {
        var r = orb.getBoundingClientRect();
        var dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
        var len = Math.max(40, Math.hypot(dx, dy));
        pups.forEach(function (pp) { pp.style.transform = "translate(" + (dx / len) * 2.4 + "px," + (dy / len) * 2.4 + "px)"; });
      }, { passive: true });
    }
  }
  renderOrbPet();

  /* ----- expressions: idle · happy · talking · surprised · sleeping ------ */
  /*  Moods drive the SVG via data-mood (CSS does the rest). Nova (the 3D     */
  /*  model) has no svg[data-mood], so every call is a safe no-op for her.    */
  function petEl() { return orbCore ? orbCore.querySelector("svg[data-mood]") : null; }
  var moodHold = null, sleepTmr = null;
  function setMood(m, holdMs) {
    var s = petEl(); if (!s) return;
    s.dataset.mood = m;
    if (moodHold) { clearTimeout(moodHold); moodHold = null; }
    if (holdMs) moodHold = setTimeout(function () {
      var e = petEl(); if (e && e.dataset.mood === m) e.dataset.mood = "idle";
    }, holdMs);
  }
  function wakePet() {
    var s = petEl();
    if (s && s.dataset.mood === "sleeping") s.dataset.mood = "idle";
    if (sleepTmr) clearTimeout(sleepTmr);
    if (!reduced) sleepTmr = setTimeout(function () {
      var e = petEl();
      if (e && !moodHold && e.dataset.mood === "idle" && (!panelLea || panelLea.hidden))
        e.dataset.mood = "sleeping";
    }, 24000);
  }
  if (!reduced) {
    addEventListener("pointermove", wakePet, { passive: true });
    addEventListener("scroll", wakePet, { passive: true });
    wakePet();
  }

  /* pet pickers inside each environment card */
  document.querySelectorAll(".petpick").forEach(function (box) {
    PETS.forEach(function (pet) {
      var b = document.createElement("button");
      b.type = "button"; b.setAttribute("role", "radio");
      b.setAttribute("aria-checked", String(pet.id === petChoice));
      b.title = pet.title; b.setAttribute("data-hover", "");
      b.innerHTML = pet.svg;
      b.addEventListener("click", function () {
        petChoice = pet.id;
        try { localStorage.setItem("v4pet", petChoice); } catch (err) {}
        document.querySelectorAll('.petpick button').forEach(function (bb) {
          bb.setAttribute("aria-checked", String(bb.title === pet.title));
        });
        renderOrbPet();
        setMood("happy", 1700);
      });
      box.appendChild(b);
    });
  });

  /* ====================================================================== */
  /*  LEA — chat brain: on-device retrieval over site facts                 */
  /* ====================================================================== */
  var panelLea = document.getElementById("lea");
  var msgs = document.getElementById("lea-msgs");
  var chipsBox = document.getElementById("lea-chips");
  var leaForm = document.getElementById("lea-form");
  var leaInput = document.getElementById("lea-input");

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
    { k: ["200", "grant", "pathway", "leo", "funding", "voucher", "digital", "without"],
      a: "With the grant: €200 mobilises the on-site audit plus a complete, application-ready LEO grant pack; approved → the scheme carries its share and your €200 is credited. Without the grant: you keep the audit + pack your €200 already bought, see a fixed quote, and decide freely. Approval is always the LEO's call — never ours.",
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
      a: "Honest answer (EU AI Act and all): I'm an automated assistant — a scripted helper answering from this site's own content, nothing more. Not a human, never pretending to be one. Ask for a human any time and I'll hand you straight over.",
      l: [] },
    { k: ["pet", "companion", "fox", "sheep", "sprout", "avatar", "cute"],
      a: "You can pick your travel companion in any of the three rooms — Lea the sprout, Penny the fox or Mossy the sheep. Whoever you pick rides this bubble with you. (They're all me with different hats, between us.)",
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
    { k: ["video", "film", "case", "proof", "demo", "backdrop", "image", "photo"],
      a: "The case films show one real process rebuilt on camera — AI-assisted productions, labelled as such; the workbook footage inside is always real. The room backdrops on this page are AI-generated environments and are marked too.",
      l: [] },
    { k: ["music", "sound", "audio", "song", "suno"],
      a: "The sound toggle (bottom-left) plays the ambient theme — off until you turn it on. The full studio track is on its way; headphones recommended.",
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
      "&body=" + encodeURIComponent("Hi Leanta — I asked: \"" + qRaw + "\" — could a human pick this up?")]];
    if (cfg.contactPhone) {
      handoff.unshift(["WhatsApp a human", "https://wa.me/" + cfg.contactPhone.replace(/[^0-9]/g, "") +
        "?text=" + encodeURIComponent("Hi Leanta — I asked: \"" + qRaw + "\"")]);
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
    setMood("talking");
    var res = answer(q); /* LEA_UPGRADE: replace with fetch("/api/lea") */
    setTimeout(function () {
      typing.remove();
      addMsg(res.text, "bot", res.links);
      setMood("happy", 1500);
    }, 480 + Math.min(900, q.length * 14));
  }

  if (orb && panelLea) {
    var CHIPS = ["What do toolkits cost?", "With vs without the grant?", "Will I pass an inspection?", "Talk to a human"];
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
        setMood("surprised", 1000);
        if (!greeted) {
          greeted = true;
          addMsg("Hi — I'm " + currentPet().name + ", Leanta's automated helper (not a human, happy to fetch one). What's eating your week?", "bot");
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
