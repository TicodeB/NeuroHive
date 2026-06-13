/* Leanta hero 3D — three.js floating emerald-glass objects with mouse + scroll
   parallax. Progressive enhancement only:
   - skipped entirely on prefers-reduced-motion, missing WebGL, or load failure
     (the CSS orbs remain as the fallback visual);
   - pointer-events: none — never blocks reading or clicks;
   - DPR capped at 2, paused when the tab is hidden. No tracking, no cookies. */

(function () {
  "use strict";

  var mount = document.getElementById("hero3d");
  if (!mount) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var canWebGL = (function () {
    try {
      var c = document.createElement("canvas");
      return !!(window.WebGLRenderingContext &&
        (c.getContext("webgl2") || c.getContext("webgl")));
    } catch (e) { return false; }
  })();
  if (!canWebGL) return;

  import("https://cdn.jsdelivr.net/npm/three@0.165.0/build/three.module.js")
    .then(start)
    .catch(function () { /* CDN blocked or offline — CSS orbs stay */ });

  function start(THREE) {
    var hero = mount.closest(".hero");
    var renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    mount.appendChild(renderer.domElement);
    if (hero) hero.classList.add("has-3d");

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(38, 1, 0.1, 60);
    camera.position.set(0, 0, 11);

    /* Lighting: warm key + cool fill, matching the cream/emerald/gold palette */
    scene.add(new THREE.AmbientLight(0xfaf6ee, 0.85));
    var key = new THREE.DirectionalLight(0xffffff, 1.25);
    key.position.set(4, 6, 8);
    scene.add(key);
    var gold = new THREE.PointLight(0xe7cd72, 18, 30);
    gold.position.set(-5, 3, 5);
    scene.add(gold);

    var group = new THREE.Group();
    scene.add(group);

    var matEmerald = new THREE.MeshPhysicalMaterial({
      color: 0x0e6b4e, roughness: 0.18, metalness: 0.05,
      clearcoat: 1, clearcoatRoughness: 0.15
    });
    var matGold = new THREE.MeshPhysicalMaterial({
      color: 0xc9a227, roughness: 0.25, metalness: 0.65,
      clearcoat: 0.8, clearcoatRoughness: 0.2
    });
    var matMint = new THREE.MeshPhysicalMaterial({
      color: 0x1da97c, roughness: 0.3, metalness: 0.1,
      clearcoat: 0.6, clearcoatRoughness: 0.3
    });

    var ico = new THREE.Mesh(new THREE.IcosahedronGeometry(1.85, 0), matEmerald);
    ico.position.set(4.4, 1.1, 0);
    group.add(ico);

    var wire = new THREE.Mesh(
      new THREE.IcosahedronGeometry(2.18, 1),
      new THREE.MeshBasicMaterial({ color: 0x0b5d44, wireframe: true, transparent: true, opacity: 0.16 })
    );
    wire.position.copy(ico.position);
    group.add(wire);

    var knot = new THREE.Mesh(new THREE.TorusKnotGeometry(0.62, 0.2, 110, 14), matGold);
    knot.position.set(1.6, -1.7, -1.5);
    group.add(knot);

    var sats = [];
    for (var i = 0; i < 9; i++) {
      var r = 0.1 + Math.random() * 0.2;
      var s = new THREE.Mesh(new THREE.SphereGeometry(r, 20, 20), i % 3 ? matMint : matGold);
      s.position.set(-1 + Math.random() * 8.5, -2.6 + Math.random() * 5.2, -2.5 + Math.random() * 2);
      s.userData = { y0: s.position.y, sp: 0.4 + Math.random() * 0.8, ph: Math.random() * Math.PI * 2 };
      sats.push(s);
      group.add(s);
    }

    /* Pointer + scroll parallax (lerped, subtle) */
    var px = 0, py = 0, tx = 0, ty = 0, scroll = 0;
    window.addEventListener("pointermove", function (e) {
      tx = (e.clientX / window.innerWidth - 0.5) * 2;
      ty = (e.clientY / window.innerHeight - 0.5) * 2;
    }, { passive: true });
    window.addEventListener("scroll", function () {
      scroll = window.scrollY || 0;
    }, { passive: true });

    function resize() {
      var w = mount.clientWidth, h = mount.clientHeight;
      renderer.setSize(w, h, false);
      camera.aspect = w / Math.max(h, 1);
      camera.updateProjectionMatrix();
    }
    resize();
    window.addEventListener("resize", resize, { passive: true });

    var clock = new THREE.Clock();
    renderer.setAnimationLoop(function () {
      if (document.hidden) return;
      var t = clock.getElapsedTime();
      px += (tx - px) * 0.045;
      py += (ty - py) * 0.045;

      ico.rotation.x = t * 0.12; ico.rotation.y = t * 0.17;
      wire.rotation.x = -t * 0.07; wire.rotation.y = -t * 0.1;
      knot.rotation.x = t * 0.25; knot.rotation.z = t * 0.18;
      sats.forEach(function (s) {
        s.position.y = s.userData.y0 + Math.sin(t * s.userData.sp + s.userData.ph) * 0.28;
        s.rotation.y = t * 0.5;
      });

      group.rotation.y = px * 0.14;
      group.rotation.x = py * 0.08;
      group.position.x = px * 0.45;
      group.position.y = -py * 0.3 - Math.min(scroll / 600, 1) * 1.2;

      renderer.render(scene, camera);
    });
  }

  /* Gentle mouse-follow tilt on cards flagged with data-tilt (no library) */
  if (window.matchMedia("(hover: hover)").matches) {
    document.addEventListener("DOMContentLoaded", function () {
      document.querySelectorAll("[data-tilt]").forEach(function (card) {
        card.addEventListener("pointermove", function (e) {
          var b = card.getBoundingClientRect();
          var rx = ((e.clientY - b.top) / b.height - 0.5) * -5;
          var ry = ((e.clientX - b.left) / b.width - 0.5) * 6;
          card.style.transform = "perspective(700px) rotateX(" + rx + "deg) rotateY(" + ry + "deg) translateY(-3px)";
        });
        card.addEventListener("pointerleave", function () {
          card.style.transform = "";
        });
      });
    });
  }
})();
