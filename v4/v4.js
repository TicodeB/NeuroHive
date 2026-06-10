/* LEANTA v4 story — preloader, cursor, sound consent, scroll choreography.
   Progressive enhancement throughout: with no JS, blocked CDNs or
   prefers-reduced-motion the page is a fully readable static document. */

(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced) document.documentElement.classList.add("reduced");

  /* ---------- preloader (skipped on repeat visit / reduced motion) ------ */
  var pre = document.getElementById("pre");
  function killPre() { if (pre) { pre.classList.add("done"); pre.setAttribute("aria-hidden", "true"); } }
  if (!pre || reduced || sessionStorage.getItem("v4seen")) {
    killPre();
  } else {
    sessionStorage.setItem("v4seen", "1");
    var n = 0, bar = pre.querySelector(".bar i"), count = pre.querySelector(".count");
    var t = setInterval(function () {
      n = Math.min(100, n + 2 + Math.random() * 6);
      bar.style.width = n + "%";
      count.textContent = (n < 10 ? "0" : "") + Math.floor(n);
      if (n >= 100) { clearInterval(t); setTimeout(killPre, 250); }
    }, 28);
    setTimeout(killPre, 2600); /* hard cap — never trap the visitor */
  }

  /* ---------- custom cursor (fine pointers only) ------------------------ */
  if (window.matchMedia("(hover: hover) and (pointer: fine)").matches && !reduced) {
    document.body.classList.add("has-cursor");
    var dot = document.querySelector(".cur"), ring = document.querySelector(".cur-ring");
    var mx = innerWidth / 2, my = innerHeight / 2, rx = mx, ry = my;
    addEventListener("pointermove", function (e) { mx = e.clientX; my = e.clientY; }, { passive: true });
    (function loop() {
      rx += (mx - rx) * 0.16; ry += (my - ry) * 0.16;
      dot.style.left = mx + "px"; dot.style.top = my + "px";
      ring.style.left = rx + "px"; ring.style.top = ry + "px";
      requestAnimationFrame(loop);
    })();
    document.querySelectorAll("a, button, [data-hover], label").forEach(function (el) {
      el.addEventListener("pointerenter", function () { ring.classList.add("big"); });
      el.addEventListener("pointerleave", function () { ring.classList.remove("big"); });
    });
  }

  /* ---------- sound consent (OFF by default; hidden if no track) -------- */
  var soundBtn = document.getElementById("sound");
  var AUDIO_SRC = "assets/leanta-theme.mp3"; /* Samuel drops the Suno track here */
  fetch(AUDIO_SRC, { method: "HEAD" }).then(function (r) {
    if (!r.ok) return;
    soundBtn.classList.add("show");
    var audio = null;
    soundBtn.addEventListener("click", function () {
      if (!audio) { audio = new Audio(AUDIO_SRC); audio.loop = true; audio.volume = 0.35; }
      var on = soundBtn.classList.toggle("on");
      soundBtn.setAttribute("aria-pressed", String(on));
      document.getElementById("sound-label").textContent = on ? "Sound on" : "Sound off";
      if (on) { audio.play().catch(function () {}); } else { audio.pause(); }
    });
  }).catch(function () {});

  /* ---------- video case slots (HEAD-check, else keep poster card) ------ */
  document.querySelectorAll(".vid[data-case]").forEach(function (slot) {
    var src = "assets/" + slot.getAttribute("data-case") + ".mp4";
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
  document.addEventListener("DOMContentLoaded", function () {
    var cfg = window.LEANTA || { contactEmail: "hello@leanta.ie" };
    document.querySelectorAll("[data-textus]").forEach(function (slot) {
      var a = document.createElement("a");
      a.className = "btn-x ghost";
      a.setAttribute("data-hover", "");
      if (cfg.contactPhone) {
        a.href = "sms:" + cfg.contactPhone + "?&body=" + encodeURIComponent("Hi Leanta — [your business name]. ");
        a.textContent = "Text us — no call needed";
      } else {
        a.href = "mailto:" + cfg.contactEmail + "?subject=" + encodeURIComponent("Quick question (no call please)");
        a.textContent = "Message us — no call needed";
      }
      slot.appendChild(a);
    });
  });

  /* ---------- hero canvas: drifting emerald constellation --------------- */
  var fx = document.getElementById("fx");
  if (fx && !reduced && fx.getContext) {
    var ctx = fx.getContext("2d");
    var P = [], DPR = Math.min(devicePixelRatio || 1, 2), W, H;
    function size() {
      W = fx.clientWidth; H = fx.clientHeight;
      fx.width = W * DPR; fx.height = H * DPR;
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    }
    size(); addEventListener("resize", size, { passive: true });
    for (var i = 0; i < 42; i++) {
      P.push({ x: Math.random() * 2000, y: Math.random() * 1200,
               vx: (Math.random() - 0.5) * 0.25, vy: (Math.random() - 0.5) * 0.25,
               r: 0.8 + Math.random() * 1.8 });
    }
    var pmx = 0.5, pmy = 0.5;
    addEventListener("pointermove", function (e) {
      pmx = e.clientX / innerWidth; pmy = e.clientY / innerHeight;
    }, { passive: true });
    (function draw() {
      if (!document.hidden) {
        ctx.clearRect(0, 0, W, H);
        var ox = (pmx - 0.5) * 26, oy = (pmy - 0.5) * 18;
        for (var i = 0; i < P.length; i++) {
          var p = P[i];
          p.x += p.vx; p.y += p.vy;
          var x = ((p.x % 2000) + 2000) % 2000 / 2000 * W + ox;
          var y = ((p.y % 1200) + 1200) % 1200 / 1200 * H + oy;
          ctx.beginPath(); ctx.arc(x, y, p.r, 0, 7);
          ctx.fillStyle = i % 6 === 0 ? "rgba(231,205,114,.8)" : "rgba(29,184,135,.65)";
          ctx.fill();
          for (var j = i + 1; j < P.length; j++) {
            var q = P[j];
            var qx = ((q.x % 2000) + 2000) % 2000 / 2000 * W + ox;
            var qy = ((q.y % 1200) + 1200) % 1200 / 1200 * H + oy;
            var d = (x - qx) * (x - qx) + (y - qy) * (y - qy);
            if (d < 16000) {
              ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(qx, qy);
              ctx.strokeStyle = "rgba(0,90,60," + (0.35 - d / 16000 * 0.35) + ")";
              ctx.lineWidth = 0.6; ctx.stroke();
            }
          }
        }
      }
      requestAnimationFrame(draw);
    })();
  }

  /* ---------- scroll choreography (GSAP+Lenis if the CDNs loaded) ------- */
  function initScroll() {
    var hasGsap = typeof window.gsap !== "undefined" && typeof window.ScrollTrigger !== "undefined";
    if (!reduced && typeof window.Lenis === "function") {
      var lenis = new window.Lenis({ lerp: 0.1 });
      function raf(time) { lenis.raf(time); requestAnimationFrame(raf); }
      requestAnimationFrame(raf);
    }
    if (hasGsap && !reduced) {
      gsap.registerPlugin(ScrollTrigger);
      document.querySelectorAll(".rv").forEach(function (el) {
        ScrollTrigger.create({ trigger: el, start: "top 86%",
          onEnter: function () { el.classList.add("in"); }, once: true });
      });
      /* chapter numerals drift slower than the page */
      document.querySelectorAll(".num").forEach(function (el) {
        gsap.to(el, { yPercent: 28, ease: "none",
          scrollTrigger: { trigger: el.parentElement, start: "top bottom", end: "bottom top", scrub: true } });
      });
      /* KPI count-up */
      document.querySelectorAll(".k .val[data-count]").forEach(function (el) {
        var target = parseFloat(el.getAttribute("data-count"));
        var prefix = el.getAttribute("data-prefix") || "";
        var dec = (el.getAttribute("data-count").split(".")[1] || "").length;
        ScrollTrigger.create({ trigger: el, start: "top 85%", once: true,
          onEnter: function () {
            var o = { v: 0 };
            gsap.to(o, { v: target, duration: 1.4, ease: "power2.out", onUpdate: function () {
              el.textContent = prefix + o.v.toLocaleString("en-IE",
                { minimumFractionDigits: dec, maximumFractionDigits: dec }) + (prefix ? "" : "%");
            }});
          }});
      });
    } else {
      /* fallback: IntersectionObserver reveals, instant KPI values */
      document.querySelectorAll(".k .val[data-count]").forEach(function (el) {
        var prefix = el.getAttribute("data-prefix") || "";
        el.textContent = prefix + el.getAttribute("data-count") + (prefix ? "" : "%");
      });
      if ("IntersectionObserver" in window && !reduced) {
        var io = new IntersectionObserver(function (es) {
          es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
        }, { rootMargin: "0px 0px -10% 0px" });
        document.querySelectorAll(".rv").forEach(function (el) { io.observe(el); });
      } else {
        document.querySelectorAll(".rv").forEach(function (el) { el.classList.add("in"); });
      }
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initScroll);
  } else { initScroll(); }
})();
