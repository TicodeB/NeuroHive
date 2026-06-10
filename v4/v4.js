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
    var ty = env.querySelector(".ty");
    if (!ty || reduced) return;
    if (ty.getAttribute("data-done") === "1") return;
    ty.setAttribute("data-done", "1");
    typewrite(ty, ty.getAttribute("data-type"), 26);
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

  /* ---------- THE DESCENT — scroll engine -------------------------------- */
  var envs = Array.prototype.slice.call(document.querySelectorAll(".env"));
  var floors = document.querySelectorAll("#floors span");
  var progressBar = document.querySelector("#progress i");
  var desktop = window.matchMedia("(min-width: 1024px)").matches;

  envs.forEach(function (env) {           /* lazy-set the backdrop images */
    var bg = env.querySelector(".bg");
    if (bg) bg.style.backgroundImage = "url('" + bg.getAttribute("data-img") + "')";
  });

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
          /* descend THROUGH the room: pan the backdrop up, blur it out at exit */
          var t = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - innerHeight)));
          var bg = env.querySelector(".bg");
          if (bg && r.bottom > 0 && r.top < innerHeight) {
            bg.style.transform = "translateY(" + ((t - 0.5) * -9) + "%) scale(" + (1.04 + t * 0.05) + ")";
            var exit = Math.max(0, (t - 0.8) / 0.2);    /* last 20% — sink below */
            bg.style.filter = exit > 0 ? "blur(" + (exit * 10).toFixed(1) + "px) brightness(" + (1 - exit * 0.12).toFixed(2) + ")" : "";
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
  if (mind && "IntersectionObserver" in window && !reduced) {
    var step = -1;
    var mio = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        if (step < 0) { step = 0; mind.classList.add("s0");
          setTimeout(function () { mind.classList.add("s1"); }, 700);
          setTimeout(function () { mind.classList.add("s2"); }, 1700);
          mio.disconnect();
        }
      });
    }, { threshold: 0.35 });
    mio.observe(mind);
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
  var AUDIO_SRC = "/v4/assets/leanta-theme.mp3";
  var engine = null;

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

  /* ---------- lead catcher ----------------------------------------------- */
  var cfg = window.LEANTA || { contactEmail: "hello@leanta.ie" };
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
  /*  COMPANIONS — three cute pets; the pick rides the Lea orb.             */
  /*  Samuel's Omma scene (LEANTA.ommaPetUrl) overrides everything.         */
  /* ====================================================================== */
  function petSVG(body1, body2, accent, kind) {
    var head =
      '<svg viewBox="0 0 100 100" aria-hidden="true">' +
      '<defs><radialGradient id="pg' + kind + '" cx="38%" cy="30%" r="80%">' +
      '<stop offset="0%" stop-color="' + body1 + '"/><stop offset="100%" stop-color="' + body2 + '"/>' +
      '</radialGradient></defs><g class="pet">';
    var tail = '</g></svg>';
    var eyes =
      '<g class="eye eL"><ellipse cx="40" cy="54" rx="7.2" ry="8.4" fill="#fff"/>' +
      '<circle class="pup" cx="40" cy="55" r="3.4" fill="#15181a"/></g>' +
      '<g class="eye eR"><ellipse cx="60" cy="54" rx="7.2" ry="8.4" fill="#fff"/>' +
      '<circle class="pup" cx="60" cy="55" r="3.4" fill="#15181a"/></g>' +
      '<path d="M44 69 Q50 74 56 69" stroke="#15181a" stroke-width="2.4" fill="none" stroke-linecap="round"/>';
    if (kind === "sprout") return head +
      '<path d="M50 16 C50 8 56 5 61 6 C60 12 56 15 50 16 Z" fill="' + accent + '"/>' +
      '<line x1="50" y1="22" x2="50" y2="13" stroke="' + accent + '" stroke-width="2.4" stroke-linecap="round"/>' +
      '<ellipse cx="50" cy="58" rx="30" ry="27" fill="url(#pg' + kind + ')"/>' +
      '<ellipse cx="38" cy="66" rx="5" ry="3" fill="#e06a5e" opacity=".25"/>' +
      '<ellipse cx="62" cy="66" rx="5" ry="3" fill="#e06a5e" opacity=".25"/>' + eyes +
      '<ellipse cx="38" cy="84" rx="6" ry="3.2" fill="' + body2 + '"/>' +
      '<ellipse cx="62" cy="84" rx="6" ry="3.2" fill="' + body2 + '"/>' + tail;
    if (kind === "fox") return head +
      '<path d="M28 36 L22 16 L42 28 Z" fill="url(#pg' + kind + ')"/>' +
      '<path d="M72 36 L78 16 L58 28 Z" fill="url(#pg' + kind + ')"/>' +
      '<path d="M28 36 L25 22 L38 30 Z" fill="#fff" opacity=".7"/>' +
      '<path d="M72 36 L75 22 L62 30 Z" fill="#fff" opacity=".7"/>' +
      '<ellipse cx="50" cy="58" rx="30" ry="27" fill="url(#pg' + kind + ')"/>' +
      '<ellipse cx="50" cy="68" rx="16" ry="12" fill="#fff" opacity=".85"/>' + eyes +
      '<ellipse cx="50" cy="63" rx="4" ry="3" fill="' + accent + '"/>' + tail;
    /* sheep */
    return head +
      '<circle cx="32" cy="42" r="11" fill="#fff"/><circle cx="46" cy="36" r="12" fill="#fff"/>' +
      '<circle cx="62" cy="38" r="11" fill="#fff"/><circle cx="70" cy="48" r="10" fill="#fff"/>' +
      '<circle cx="28" cy="54" r="10" fill="#fff"/>' +
      '<ellipse cx="50" cy="60" rx="28" ry="25" fill="#fff"/>' +
      '<ellipse cx="50" cy="62" rx="20" ry="18" fill="url(#pg' + kind + ')"/>' +
      '<path d="M27 50 C20 48 18 42 22 38 C27 40 29 45 27 50 Z" fill="' + body2 + '"/>' +
      '<path d="M73 50 C80 48 82 42 78 38 C73 40 71 45 73 50 Z" fill="' + body2 + '"/>' + eyes + tail;
  }
  var PETS = [
    { id: "sprout", name: "Lea", title: "Lea the sprout", svg: petSVG("#3ddca8", "#0a8a52", "#d7a900", "sprout") },
    { id: "fox",    name: "Penny", title: "Penny the fox", svg: petSVG("#ff9d5c", "#c45f1e", "#15181a", "fox") },
    { id: "sheep",  name: "Mossy", title: "Mossy the sheep", svg: petSVG("#bcb6a8", "#7d7669", "#15181a", "sheep") }
  ];
  var petChoice = "sprout";
  try { petChoice = localStorage.getItem("v4pet") || "sprout"; } catch (err) {}

  var orb = document.getElementById("lea-orb");
  var orbCore = orb ? orb.querySelector(".core") : null;
  var orbLbl = orb ? orb.querySelector(".lbl") : null;

  function currentPet() {
    for (var i = 0; i < PETS.length; i++) if (PETS[i].id === petChoice) return PETS[i];
    return PETS[0];
  }
  function renderOrbPet() {
    if (!orbCore) return;
    if (cfg.ommaPetUrl) {
      var fr = document.createElement("iframe");
      fr.src = cfg.ommaPetUrl; fr.title = "Lea — Leanta's pet assistant";
      fr.loading = "lazy"; fr.setAttribute("frameborder", "0");
      fr.style.pointerEvents = "none";
      orbCore.innerHTML = ""; orbCore.appendChild(fr);
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
    var res = answer(q); /* LEA_UPGRADE: replace with fetch("/api/lea") */
    setTimeout(function () {
      typing.remove();
      addMsg(res.text, "bot", res.links);
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
