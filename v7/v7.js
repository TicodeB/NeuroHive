/* ============================================================================
   LEANTA v6 — "THE JOURNEY"  (engine)
   v5's scroll-to-fly WebGL camera carrying v4's real microsite content.
   The canvas is fixed; a tall proxy drives the camera (scroll UP = forward).
   v4's glass scenes ride on top as crisp HTML, revealed as the camera settles
   at each beat. LEA, companions, sound and the lead form are ported from v4.
   Config-driven: BEATS + the .scene[data-p] markup are the whole choreography.
   ========================================================================== */
import * as THREE from "./vendor/three.module.js";

var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
var cfg = window.LEANTA || {};
var COL = { cream:0xf2efe8, creamWarm:0xefe6d4, ink:0x15181a,
  em:0x0a8a52, pink:0xe85a8a, orange:0xe8843a, mint:0x4fc99a, stone:0x8a948e };
var ACCENT_HEX = { em:COL.em, pink:COL.pink, orange:COL.orange, mint:COL.mint, stone:COL.stone };
/* unified grid spectrum (Samuel): graphite → emerald → pink */
var GRAPHITE = new THREE.Color(0x2a2e30), EMER = new THREE.Color(COL.em), PINKC = new THREE.Color(COL.pink);
function rampColor(t, out){ out = out || new THREE.Color();
  if (t < 0.5) out.copy(GRAPHITE).lerp(EMER, t/0.5); else out.copy(EMER).lerp(PINKC, (t-0.5)/0.5); return out; }

/* beats aligned to the .scene[data-p] markers; cam = where the camera sits */
var BEATS = [
  { id:"atrium",  p:0.00, cam:{x:0,  y:5, z:92}  },
  { id:"approach",p:0.06, cam:{x:0,  y:4, z:44}  },
  { id:"shops",   p:0.14, cam:{x:-6, y:4, z:-8}  },
  { id:"trades",  p:0.26, cam:{x:6,  y:4, z:-78} },
  { id:"mfg",     p:0.37, cam:{x:-6, y:4, z:-142}},
  { id:"farm",    p:0.48, cam:{x:6,  y:5, z:-206}},
  { id:"school",  p:0.58, cam:{x:-6, y:4, z:-264}},
  { id:"health",  p:0.68, cam:{x:6,  y:4, z:-322}},
  { id:"grant",   p:0.78, cam:{x:0,  y:5, z:-386}},
  { id:"logic",   p:0.88, cam:{x:0,  y:5, z:-448}},
  { id:"finale",  p:0.96, cam:{x:0,  y:6, z:-500}},
  { id:"end",     p:1.00, cam:{x:0,  y:6, z:-528}},
];
var PORTAL_Z = -30;                                   /* hero → shops portal */
var WORLD_PORTALS = [-43,-110,-174,-235,-293,-354];   /* roof-A between worlds */

/* ---- content systems run with OR without WebGL --------------------------- */
initLea();
initSound();
initLead();

/* ---- engine boot / fallback ---------------------------------------------- */
var canvas = document.getElementById("stage");
var renderer = null;
try { renderer = new THREE.WebGLRenderer({ canvas:canvas, antialias:true, alpha:true, powerPreference:"high-performance" }); }
catch (e) { renderer = null; }
if (!renderer || !renderer.getContext()) {
  document.documentElement.classList.add("static-doc");   /* scenes → readable stacked doc */
  var b0 = document.getElementById("begin");
  if (b0) b0.addEventListener("click", function () { var s = document.getElementById("scenes"); if (s) s.scrollIntoView({ behavior:"smooth" }); });
} else {
  startEngine();
}

/* ========================================================================== */
function startEngine() {
  var DPR = Math.min(window.devicePixelRatio || 1, 1.75);
  renderer.setPixelRatio(DPR);
  renderer.setClearColor(0x000000, 0);

  var scene = new THREE.Scene();
  scene.fog = new THREE.Fog(COL.cream, 60, 300);
  var camera = new THREE.PerspectiveCamera(55, innerWidth/innerHeight, 0.1, 760);
  camera.position.set(0, 5, 92);

  scene.add(new THREE.AmbientLight(0xfff6e8, 0.9));
  var key = new THREE.DirectionalLight(0xffffff, 1.1); key.position.set(8,18,30); scene.add(key);
  var emGlow = new THREE.PointLight(COL.em, 1.4, 170); emGlow.position.set(0,4,PORTAL_Z); scene.add(emGlow);

  /* ---- lattice — ordered mesh holding the whole journey ----------------- */
  var dotTex = (function () {
    var c = document.createElement("canvas"); c.width = c.height = 64; var x = c.getContext("2d");
    var g = x.createRadialGradient(32,32,0,32,32,32);
    g.addColorStop(0,"rgba(255,255,255,1)"); g.addColorStop(.6,"rgba(255,255,255,.8)"); g.addColorStop(1,"rgba(255,255,255,0)");
    x.fillStyle = g; x.fillRect(0,0,64,64); return new THREE.CanvasTexture(c);
  })();
  var LAYERS = reduced ? 28 : 58, CW = 18, CH = 10, GAPX = 11, GAPY = 9, GAPZ = 14;
  var COUNT = LAYERS*CW*CH;
  var basePos = new Float32Array(COUNT*3), colArr = new Float32Array(COUNT*3), baseCol = new Float32Array(COUNT*3);
  var inkC = new THREE.Color(COL.ink), tmpC = new THREE.Color();
  (function () { var k = 0;
    for (var l=0;l<LAYERS;l++) for (var r=0;r<CH;r++) for (var c=0;c<CW;c++,k++) {
      basePos[k*3] = (c-(CW-1)/2)*GAPX; basePos[k*3+1] = (r-(CH-1)/2)*GAPY+2; basePos[k*3+2] = 96-l*GAPZ;
      rampColor(l/(LAYERS-1), tmpC);   /* depth-graded: graphite (near) → emerald → pink (deep) */
      colArr[k*3]=tmpC.r; colArr[k*3+1]=tmpC.g; colArr[k*3+2]=tmpC.b;
      baseCol[k*3]=tmpC.r; baseCol[k*3+1]=tmpC.g; baseCol[k*3+2]=tmpC.b;
    }
  })();
  var dgeo = new THREE.BufferGeometry();
  dgeo.setAttribute("position", new THREE.BufferAttribute(basePos.slice(),3));
  dgeo.setAttribute("color", new THREE.BufferAttribute(colArr,3));
  var dots = new THREE.Points(dgeo, new THREE.PointsMaterial({ vertexColors:true, size:0.6, sizeAttenuation:true,
    map:dotTex, transparent:true, opacity:0.4, depthWrite:false }));
  scene.add(dots);

  var ray = new THREE.Raycaster(); ray.params.Points.threshold = 2.2;
  var ndc = new THREE.Vector2(2,2);
  addEventListener("pointermove", function (e) { ndc.x = (e.clientX/innerWidth)*2-1; ndc.y = -(e.clientY/innerHeight)*2+1; }, { passive:true });

  /* ---- warp streaks ----------------------------------------------------- */
  var SN = reduced ? 0 : 540;
  var sBase = [], sArr = new Float32Array(Math.max(1,SN*2*3));
  for (var i=0;i<SN;i++){ var x=(Math.random()-0.5)*180, y=(Math.random()-0.5)*120, z=100-Math.random()*720;
    sBase.push([x,y,z]); sArr.set([x,y,z,x,y,z], i*6); }
  var sgeo = new THREE.BufferGeometry(); sgeo.setAttribute("position", new THREE.BufferAttribute(sArr,3));
  var streaks = new THREE.LineSegments(sgeo, new THREE.LineBasicMaterial({ color:COL.ink, transparent:true, opacity:0, depthWrite:false }));
  if (SN) scene.add(streaks);

  /* ---- roof-A portals --------------------------------------------------- */
  function roofAShape(){ var pts=[[0,32],[24,-32],[12,-32],[0,4],[-12,-32],[-24,-32]];
    var s=new THREE.Shape(); s.moveTo(pts[0][0],pts[0][1]); for(var i=1;i<pts.length;i++) s.lineTo(pts[i][0],pts[i][1]); s.closePath(); return s; }
  function makeA(scale,z,emissive){ var geo=new THREE.ExtrudeGeometry(roofAShape(),{depth:6,bevelEnabled:true,bevelThickness:.8,bevelSize:.8,bevelSegments:2});
    geo.center(); var m=new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color:COL.cream, emissive:COL.em, emissiveIntensity:emissive, metalness:.1, roughness:.5 }));
    m.scale.setScalar(scale); m.position.set(0,-6*scale,z); return m; }
  var portal = makeA(1.5, PORTAL_Z, 0.55); scene.add(portal);
  var portals = WORLD_PORTALS.map(function (z) { var m = makeA(1.15, z, 0.3); scene.add(m); return m; });
  var halo = new THREE.Mesh(new THREE.CircleGeometry(26,48), new THREE.MeshBasicMaterial({ color:COL.creamWarm, transparent:true, opacity:0 }));
  halo.position.set(0,2,PORTAL_Z-4); scene.add(halo);

  /* ---- scroll proxy (inverted: UP = forward) ---------------------------- */
  var proxy = document.getElementById("scroll-proxy"), JOURNEY = 13;
  function sizeProxy(){ proxy.style.height = (JOURNEY*innerHeight)+"px"; }
  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  sizeProxy();
  function maxScroll(){ return document.documentElement.scrollHeight - innerHeight; }
  function scrollProgress(){ var m=maxScroll(); return m>0 ? Math.min(1,Math.max(0,1-window.scrollY/m)) : 0; }
  function yFor(p){ return (1-p)*maxScroll(); }
  scrollTo(0, maxScroll());

  /* ---- journey sampling ------------------------------------------------- */
  var smooth = function (t){ return t*t*(3-2*t); };
  function sampleAt(p){ var i=0; while (i<BEATS.length-2 && p>BEATS[i+1].p) i++;
    var a=BEATS[i], b=BEATS[i+1], raw=(p-a.p)/Math.max(1e-4,b.p-a.p), t=smooth(Math.min(1,Math.max(0,raw)));
    return { x:a.cam.x+(b.cam.x-a.cam.x)*t, y:a.cam.y+(b.cam.y-a.cam.y)*t, z:a.cam.z+(b.cam.z-a.cam.z)*t }; }

  /* ---- scene reveal sync ------------------------------------------------- */
  var scenes = [].slice.call(document.querySelectorAll(".scene")).map(function (el) {
    return { el:el, p:parseFloat(el.dataset.p), accent:el.dataset.accent || "em", lit:false }; });
  var mind = document.getElementById("mind"), mindRun = false;
  function syncScenes(camP){
    var best=-1, bestD=1;
    for (var i=0;i<scenes.length;i++){ var d=Math.abs(camP-scenes[i].p); if (d<bestD){ bestD=d; best=i; } }
    for (var j=0;j<scenes.length;j++){
      var on = (j===best && bestD<0.05);
      if (on !== scenes[j].lit){ scenes[j].lit = on; scenes[j].el.classList.toggle("active", on);
        if (on && scenes[j].el.id==="sc-logic") runMind();
        if (on) setMoodSafe("happy", 1400);
      }
    }
  }
  function runMind(){ if (mindRun || !mind) return; mindRun = true;
    setTimeout(function(){ mind.classList.add("s0"); },120);
    setTimeout(function(){ mind.classList.add("s1"); },700);
    setTimeout(function(){ mind.classList.add("s2"); },1400); }

  /* ---- camera state ----------------------------------------------------- */
  var camP=0, targetP=0, begun=false, mx=0, my=0, lastP=0, warp=0;
  var mouse={x:0,y:0}, worldAccent=new THREE.Color(COL.em);
  var gradeEl = document.getElementById("grade"), progI = document.querySelector("#progress i");
  addEventListener("pointermove", function (e){ mouse.x=e.clientX/innerWidth-0.5; mouse.y=e.clientY/innerHeight-0.5; }, { passive:true });
  addEventListener("scroll", function (){ targetP=scrollProgress(); if (targetP>0.005 && !begun) setBegun(true); }, { passive:true });

  function clamp01(x){ return Math.min(1,Math.max(0,x)); }
  function nearestScene(camP){ var best=scenes[0], bestD=1;
    for (var i=0;i<scenes.length;i++){ var d=Math.abs(camP-scenes[i].p); if (d<bestD){ bestD=d; best=scenes[i]; } }
    return { s:best, d:bestD }; }

  function applyCamera(){
    var s = sampleAt(camP);
    mx += ((mouse.x*5)-mx)*0.05; my += ((-mouse.y*3)-my)*0.05;
    camera.position.set(s.x+mx, s.y+my, s.z);
    var look = sampleAt(Math.min(1,camP+0.04));
    camera.lookAt(look.x*0.5, look.y, s.z-50);

    /* portal-cross warm glow, then per-world accent wash */
    var warm = clamp01((camP-0.09)/0.05) * (1-clamp01((camP-0.17)/0.06));
    halo.material.opacity = 0.5*warm;

    var near = nearestScene(camP), inf = Math.max(0, 1-near.d/0.09);
    var isWorld = ["pink","orange","mint"].indexOf(near.s.accent)>=0 || near.s.el.id==="sc-shops";
    var aHex = ACCENT_HEX[near.s.accent] || COL.em;
    worldAccent.setHex(COL.em).lerp(new THREE.Color(aHex), inf*0.85);
    emGlow.color.copy(worldAccent);
    var fogC = new THREE.Color(COL.cream).lerp(new THREE.Color(COL.creamWarm), warm*0.7).lerp(new THREE.Color(aHex), inf*0.10);
    scene.fog.color.copy(fogC);
    /* v7: previous environment grade washes dropped — base stays v4 cream,
       the recoloured grid IS the only environment (Samuel's call). */
    if (gradeEl) gradeEl.style.opacity = "0";
    if (progI) progI.style.width = (camP*100).toFixed(2)+"%";
  }

  var clock = new THREE.Clock(), running = true;
  document.addEventListener("visibilitychange", function (){ running = !document.hidden; });
  function frame(){
    requestAnimationFrame(frame);
    if (!running) return;
    var dt = Math.min(0.05, clock.getDelta()), time = clock.elapsedTime;
    if (reduced){ var nb=0,nd=1; for (var i=0;i<BEATS.length;i++){ var d=Math.abs(targetP-BEATS[i].p); if (d<nd){nd=d;nb=i;} } camP += (BEATS[nb].p-camP)*Math.min(1,dt*8); }
    else camP += (targetP-camP)*Math.min(1, dt*4.2);   /* time-based: same feel at 60fps, converges on low-fps too */

    portal.rotation.z = Math.sin(time*0.18)*0.04;
    portals.forEach(function (m,k){ m.rotation.z = Math.sin(time*0.14+k)*0.05; });

    /* lattice wave + hover accent + colour decay */
    var posA = dgeo.getAttribute("position"), colA = dgeo.getAttribute("color");
    for (var p2=0;p2<COUNT;p2++) posA.array[p2*3+1] = basePos[p2*3+1] + Math.sin(time*0.7 + basePos[p2*3]*0.16 + basePos[p2*3+2]*0.05)*0.9;
    posA.needsUpdate = true;
    for (var ci=0;ci<COUNT*3;ci+=3){ colA.array[ci]+=(baseCol[ci]-colA.array[ci])*0.06; colA.array[ci+1]+=(baseCol[ci+1]-colA.array[ci+1])*0.06; colA.array[ci+2]+=(baseCol[ci+2]-colA.array[ci+2])*0.06; }
    if (ndc.x<1.5 && !reduced){ ray.setFromCamera(ndc,camera); var hits=ray.intersectObject(dots);
      for (var h=0;h<Math.min(hits.length,48);h++){ var idx=hits[h].index*3; colA.array[idx]=worldAccent.r; colA.array[idx+1]=worldAccent.g; colA.array[idx+2]=worldAccent.b; } }
    colA.needsUpdate = true;

    /* warp on camera speed */
    var v = Math.abs(camP-lastP)/Math.max(dt,1e-3); lastP = camP;
    warp += (Math.min(1, v*7)-warp)*0.14;
    if (SN){ var len = warp*warp*58;                       /* light-speed rays */
      for (var w=0;w<SN;w++){ sArr[w*6+2]=sBase[w][2]+len/2; sArr[w*6+5]=sBase[w][2]-len/2; }
      sgeo.getAttribute("position").needsUpdate = true;
      streaks.material.opacity = Math.min(0.62, warp*warp*0.7);
      /* the rays cycle graphite → emerald → pink during the jump, settling to the world */
      var phase = ((time*0.25 + camP*5) % 1 + 1) % 1;
      rampColor(phase, tmpC); streaks.material.color.copy(tmpC).lerp(worldAccent, 0.4);
      dots.material.opacity = 0.4 - warp*0.28;
    }

    applyCamera();
    syncScenes(camP);
    updateCompass(camP);
    updateRail(camP);
    renderer.render(scene, camera);
  }
  function resize(){ camera.aspect=innerWidth/innerHeight; camera.updateProjectionMatrix();
    renderer.setSize(innerWidth,innerHeight,false); sizeProxy(); scrollTo(0,yFor(targetP)); }
  addEventListener("resize", resize); resize();

  /* ---- begin / hero ----------------------------------------------------- */
  function setBegun(v){ begun=v; document.body.classList.toggle("begun", v); }
  var beginBtn = document.getElementById("begin");
  if (beginBtn) beginBtn.addEventListener("click", function (){ setBegun(true); smoothScrollTo(yFor(0.15),1100); });
  function smoothScrollTo(to,dur){ var from=window.scrollY, t0=performance.now();
    (function step(now){ var k=Math.min(1,(now-t0)/dur); scrollTo(0, from+(to-from)*smooth(k)); if (k<1) requestAnimationFrame(step); })(performance.now()); }
  /* the companion + side-rail pilot the camera through this */
  window.__flyTo = function (p){ setBegun(true); smoothScrollTo(yFor(p), 1300); };
  /* hero arc tiles + anything with [data-fly] flies the camera to that beat */
  document.querySelectorAll("[data-fly]").forEach(function (el){
    el.addEventListener("click", function (){ window.__flyTo(parseFloat(el.dataset.fly)); }); });

  /* ---- compass ---------------------------------------------------------- */
  var compassToggle = document.getElementById("compass-toggle"), compassMenu = document.getElementById("compass-menu");
  var NAV = [
    { label:"Atrium", p:0.0 }, { label:"Shops on the street", p:0.14 }, { label:"Trades people", p:0.26 },
    { label:"Manufacturing", p:0.37 }, { label:"Farmers", p:0.48 }, { label:"Schools & education", p:0.58 },
    { label:"Doctors & dentists", p:0.68 }, { label:"The €200 grant", p:0.78 }, { label:"Would you pass?", p:0.96 },
  ];
  NAV.forEach(function (n){ var b=document.createElement("button"); b.className="step"; b.setAttribute("role","menuitem");
    b.dataset.p=n.p; b.dataset.visited="false"; b.innerHTML='<span class="stepdot"></span>'+n.label;
    b.addEventListener("click", function (){ setBegun(true); smoothScrollTo(yFor(n.p),1200); closeCompass(); });
    compassMenu.appendChild(b); });
  var sep=document.createElement("div"); sep.className="compass-sep"; compassMenu.appendChild(sep);
  [["Store & toolkits","/index.html"],["Free readiness check","/quiz.html"],["The €200 grant","/grants.html"]].forEach(function (l){
    var a=document.createElement("a"); a.href=l[1]; a.setAttribute("role","menuitem"); a.textContent=l[0]; compassMenu.appendChild(a); });
  function openCompass(){ compassMenu.hidden=false; compassToggle.setAttribute("aria-expanded","true"); }
  function closeCompass(){ compassMenu.hidden=true; compassToggle.setAttribute("aria-expanded","false"); }
  compassToggle.addEventListener("click", function (){ compassMenu.hidden ? openCompass() : closeCompass(); });
  addEventListener("keydown", function (e){ if (e.key==="Escape") closeCompass(); });
  function updateCompass(p){ var steps=compassMenu.querySelectorAll(".step"), cur=0, cd=1;
    steps.forEach(function (s,i){ var sp=parseFloat(s.dataset.p); if (p>=sp-0.02) s.dataset.visited="true"; var d=Math.abs(p-sp); if (d<cd){cd=d;cur=i;} });
    steps.forEach(function (s,i){ s.setAttribute("aria-current", String(i===cur)); }); }

  /* ---- side rail — the in-world menu: jump to any world, basket, grant,
     fast-forward / rewind. Present once the journey has begun. -------------- */
  var rail = document.getElementById("rail");
  function stepWorld(dir){ var ps = NAV.map(function (n){ return n.p; }).sort(function (a,b){ return a-b; });
    var target=null, i;
    if (dir>0){ for (i=0;i<ps.length;i++){ if (ps[i]>camP+0.01){ target=ps[i]; break; } } if (target==null) target=ps[ps.length-1]; }
    else { for (i=ps.length-1;i>=0;i--){ if (ps[i]<camP-0.01){ target=ps[i]; break; } } if (target==null) target=ps[0]; }
    window.__flyTo(target); }
  if (rail){
    var fwd=document.createElement("button"); fwd.className="rail-arrow"; fwd.title="Fly forward a world"; fwd.setAttribute("aria-label","Forward a world"); fwd.textContent="▲";
    var list=document.createElement("div"); list.className="rail-list";
    NAV.forEach(function (n){ var b=document.createElement("button"); b.className="rail-step"; b.dataset.p=n.p; b.dataset.visited="false";
      b.title=n.label; b.setAttribute("aria-label",n.label); b.innerHTML='<span class="rdot"></span><span class="rlbl">'+n.label+'</span>';
      b.addEventListener("click", function (){ window.__flyTo(n.p); }); list.appendChild(b); });
    var rew=document.createElement("button"); rew.className="rail-arrow"; rew.title="Rewind a world"; rew.setAttribute("aria-label","Rewind a world"); rew.textContent="▼";
    var extra=document.createElement("div"); extra.className="rail-extra";
    var basket=document.createElement("a"); basket.className="rail-link"; basket.href="/index.html#products"; basket.setAttribute("data-hover",""); basket.innerHTML="🛒 Basket";
    var grant=document.createElement("button"); grant.className="rail-link"; grant.setAttribute("data-hover",""); grant.innerHTML="★ €200 grant";
    grant.addEventListener("click", function (){ window.__flyTo(0.78); });
    extra.appendChild(basket); extra.appendChild(grant);
    rail.appendChild(fwd); rail.appendChild(list); rail.appendChild(rew); rail.appendChild(extra);
    fwd.addEventListener("click", function (){ stepWorld(1); });
    rew.addEventListener("click", function (){ stepWorld(-1); });
  }
  function updateRail(p){ if (!rail) return; var steps=rail.querySelectorAll(".rail-step"), cur=0, cd=1;
    steps.forEach(function (s,i){ var sp=parseFloat(s.dataset.p); if (p>=sp-0.02) s.dataset.visited="true"; var d=Math.abs(p-sp); if (d<cd){cd=d;cur=i;} });
    steps.forEach(function (s,i){ s.setAttribute("aria-current", String(i===cur)); }); }

  frame();
}

/* ==========================================================================
   LEA — companion pets + on-device chat (ported & adapted from v4)
   ========================================================================== */
function setMoodSafe(m, hold){ if (window.__leaSetMood) window.__leaSetMood(m, hold); }

function initLea(){
  function petFace(){ return (
    '<ellipse class="cheek" cx="35" cy="63" rx="6" ry="3.6" fill="#ff7a66"/><ellipse class="cheek" cx="65" cy="63" rx="6" ry="3.6" fill="#ff7a66"/>'+
    '<g class="eye eL"><ellipse class="ball" cx="40" cy="53" rx="7.8" ry="9.2" fill="#fff"/><circle class="pup" cx="40" cy="55" r="4.1" fill="#15181a"/>'+
    '<circle class="cl" cx="37.6" cy="50.6" r="1.8" fill="#fff"/><path class="lid" d="M32 54 Q40 48 48 54" stroke="#15181a" stroke-width="2.6" fill="none" stroke-linecap="round"/></g>'+
    '<g class="eye eR"><ellipse class="ball" cx="60" cy="53" rx="7.8" ry="9.2" fill="#fff"/><circle class="pup" cx="60" cy="55" r="4.1" fill="#15181a"/>'+
    '<circle class="cl" cx="57.6" cy="50.6" r="1.8" fill="#fff"/><path class="lid" d="M52 54 Q60 48 68 54" stroke="#15181a" stroke-width="2.6" fill="none" stroke-linecap="round"/></g>'+
    '<path class="mouth m-idle" d="M44 69 Q50 74 56 69" stroke="#15181a" stroke-width="2.6" fill="none" stroke-linecap="round"/>'+
    '<path class="mouth m-happy" d="M41 67 Q50 81 59 67 Q50 72 41 67 Z" fill="#15181a"/>'+
    '<ellipse class="mouth m-talk" cx="50" cy="70" rx="4.6" ry="3.2" fill="#15181a"/><circle class="mouth m-surp" cx="50" cy="71" r="3.5" fill="#15181a"/>'+
    '<path class="mouth m-sleep" d="M46 71 Q50 73.5 54 71" stroke="#15181a" stroke-width="2.2" fill="none" stroke-linecap="round"/>'+
    '<g class="zzz"><text x="68" y="33" class="z1">z</text><text x="77" y="25" class="z2">z</text></g>'); }
  function petSVG(body1, body2, accent, kind){
    var gid="pg"+kind+body1.replace(/[^a-z0-9]/gi,"")+body2.replace(/[^a-z0-9]/gi,""), fill='url(#'+gid+')';
    var open='<svg viewBox="0 0 100 100" data-mood="idle" aria-hidden="true"><defs><radialGradient id="'+gid+'" cx="38%" cy="28%" r="82%">'+
      '<stop offset="0%" stop-color="'+body1+'"/><stop offset="100%" stop-color="'+body2+'"/></radialGradient></defs>'+
      '<ellipse class="shadow" cx="50" cy="93" rx="25" ry="4.4" fill="#15181a" opacity=".12"/><g class="pet">';
    var close='</g></svg>', gloss='<ellipse class="gloss" cx="39" cy="46" rx="11" ry="7.5" fill="#fff" opacity=".26"/>';
    if (kind==="sprout") return open+
      '<path d="M50 15 C50 6 57 3 63 4 C61 11 56 15 50 16 Z" fill="'+accent+'"/>'+
      '<line x1="50" y1="22" x2="50" y2="12" stroke="'+accent+'" stroke-width="2.6" stroke-linecap="round"/>'+
      '<ellipse cx="50" cy="58" rx="31" ry="28" fill="'+fill+'"/>'+gloss+
      '<ellipse cx="38" cy="86" rx="6.2" ry="3.3" fill="'+body2+'"/><ellipse cx="62" cy="86" rx="6.2" ry="3.3" fill="'+body2+'"/>'+petFace()+close;
    if (kind==="fox") return open+
      '<path d="M27 35 L21 14 L43 27 Z" fill="'+fill+'"/><path d="M73 35 L79 14 L57 27 Z" fill="'+fill+'"/>'+
      '<path d="M28 33 L25 20 L38 28 Z" fill="'+accent+'" opacity=".55"/><path d="M72 33 L75 20 L62 28 Z" fill="'+accent+'" opacity=".55"/>'+
      '<ellipse cx="50" cy="58" rx="31" ry="28" fill="'+fill+'"/>'+gloss+
      '<ellipse cx="50" cy="68" rx="17" ry="13" fill="#fff" opacity=".9"/>'+petFace()+'<ellipse cx="50" cy="63.5" rx="3.6" ry="2.7" fill="'+body2+'"/>'+close;
    return open+
      '<circle cx="32" cy="42" r="11" fill="#fbfaf7"/><circle cx="46" cy="35" r="12.5" fill="#fbfaf7"/><circle cx="62" cy="37" r="11.5" fill="#fbfaf7"/>'+
      '<circle cx="70" cy="48" r="10" fill="#fbfaf7"/><circle cx="28" cy="55" r="10" fill="#fbfaf7"/><circle cx="72" cy="58" r="9.5" fill="#fbfaf7"/>'+
      '<ellipse cx="50" cy="60" rx="29" ry="26" fill="#fbfaf7"/><ellipse cx="50" cy="61" rx="21" ry="19" fill="'+fill+'"/>'+gloss+
      '<path d="M27 50 C19 48 17 41 22 37 C28 39 30 45 27 50 Z" fill="'+body2+'"/><path d="M73 50 C81 48 83 41 78 37 C72 39 70 45 73 50 Z" fill="'+body2+'"/>'+petFace()+close;
  }
  var PETS = [
    { id:"sprout", name:"Lea", title:"Lea the sprout", svg:petSVG("#3ddca8","#0a8a52","#d7a900","sprout") },
    { id:"fox",    name:"Penny", title:"Penny the fox", svg:petSVG("#ff9d5c","#c45f1e","#15181a","fox") },
    { id:"sheep",  name:"Mossy", title:"Mossy the sheep", svg:petSVG("#bcb6a8","#7d7669","#15181a","sheep") }
  ];
  var petChoice = "sprout";
  try { petChoice = localStorage.getItem("v6pet") || petChoice; } catch (e) {}

  var orb = document.getElementById("lea-orb");
  var orbCore = orb ? orb.querySelector(".core") : null;
  var orbLbl = orb ? orb.querySelector(".lbl") : null;
  function currentPet(){ for (var i=0;i<PETS.length;i++) if (PETS[i].id===petChoice) return PETS[i]; return PETS[0]; }
  function renderOrbPet(){ if (!orbCore) return; var pet=currentPet(); orbCore.innerHTML=pet.svg;
    if (orbLbl) orbLbl.textContent="Ask "+pet.name;
    if (!reduced){ var pups=orbCore.querySelectorAll(".pup"), eyes=orbCore.querySelectorAll(".eye");
      (function blink(){ if (!orbCore.isConnected) return;
        eyes.forEach(function (ey){ ey.style.transform="scaleY(.08)"; });
        setTimeout(function (){ eyes.forEach(function (ey){ ey.style.transform=""; }); },140);
        setTimeout(blink, 2600+Math.random()*3200); })();
      addEventListener("pointermove", function (e){ var r=orb.getBoundingClientRect();
        var dx=e.clientX-(r.left+r.width/2), dy=e.clientY-(r.top+r.height/2), len=Math.max(40,Math.hypot(dx,dy));
        pups.forEach(function (pp){ pp.style.transform="translate("+(dx/len)*2.4+"px,"+(dy/len)*2.4+"px)"; }); }, { passive:true }); }
  }
  renderOrbPet();

  function petEl(){ return orbCore ? orbCore.querySelector("svg[data-mood]") : null; }
  var moodHold=null, sleepTmr=null;
  function setMood(m, holdMs){ var s=petEl(); if (!s) return; s.dataset.mood=m;
    if (moodHold){ clearTimeout(moodHold); moodHold=null; }
    if (holdMs) moodHold=setTimeout(function (){ var e=petEl(); if (e && e.dataset.mood===m) e.dataset.mood="idle"; }, holdMs); }
  window.__leaSetMood = setMood;
  function wakePet(){ var s=petEl(); if (s && s.dataset.mood==="sleeping") s.dataset.mood="idle";
    if (sleepTmr) clearTimeout(sleepTmr);
    if (!reduced) sleepTmr=setTimeout(function (){ var e=petEl();
      if (e && !moodHold && e.dataset.mood==="idle" && (!panelLea || panelLea.hidden)) e.dataset.mood="sleeping"; },24000); }
  if (!reduced){ addEventListener("pointermove", wakePet, { passive:true }); addEventListener("scroll", wakePet, { passive:true }); wakePet(); }

  /* companion picker (in the chat header) */
  var petsBox = document.getElementById("lea-pets");
  if (petsBox) PETS.forEach(function (pet){ var b=document.createElement("button");
    b.type="button"; b.setAttribute("role","radio"); b.setAttribute("aria-checked", String(pet.id===petChoice));
    b.title=pet.title; b.setAttribute("data-hover",""); b.innerHTML=pet.svg;
    b.addEventListener("click", function (){ petChoice=pet.id; try { localStorage.setItem("v6pet", petChoice); } catch (e) {}
      petsBox.querySelectorAll("button").forEach(function (bb){ bb.setAttribute("aria-checked", String(bb.title===pet.title)); });
      renderOrbPet(); setMood("happy",1700); });
    petsBox.appendChild(b); });

  /* ---- chat brain ------------------------------------------------------- */
  var panelLea=document.getElementById("lea"), msgs=document.getElementById("lea-msgs"),
      chipsBox=document.getElementById("lea-chips"), leaForm=document.getElementById("lea-form"), leaInput=document.getElementById("lea-input");
  var KB = [
    { k:["price","cost","much","toolkit","toolkits","pack","packs","buy"], a:"Toolkits are one-time purchases, no subscription: Readiness Check €29 · Compliance Pack €34 · Operations & GP €49 · Pro Bundle €69 (a genuine €14 saving) · single tools from €15. Free demo workbooks are on every product page.", l:[["Browse the toolkits","/index.html#products"]] },
    { k:["inside","contain","include","workbook","excel","spreadsheet"], a:"Each toolkit is a finished Excel/Sheets workbook: compliance records (HACCP, allergens, temps, fire, training), operations sheets (GP%, labour, cashflow) and a dashboard where every tile prescribes the next action. Every screenshot on the site is the real workbook.", l:[["See the store","/index.html#products"]] },
    { k:["quiz","readiness","check","pass","inspection","inspector","test"], a:"The free readiness check takes 2 minutes: pick your trade, answer 10 questions, get a traffic-light verdict on screen immediately. It runs entirely in your browser — nothing is sent anywhere unless you choose to message us the result.", l:[["Take the readiness check","/quiz.html"]] },
    { k:["200","grant","pathway","leo","funding","voucher","digital","without"], a:"With the grant: €200 mobilises the on-site audit plus a complete, application-ready LEO grant pack; approved → the scheme carries its share and your €200 is credited. Without the grant: you keep the audit + pack your €200 already bought, see a fixed quote, and decide freely. Approval is always the LEO's call — never ours.", l:[["The grant pathway","/grants.html"]] },
    { k:["agency","service","automation","visit","audit","onsite"], a:"The agency side: we drive out, map one painful process where it happens, and rebuild it in front of you — old way, new way, measured. Lean method with modern tooling, GDPR-first, in your own accounts.", l:[["Agency services","/services.html"]] },
    { k:["contact","phone","call","reach","talk","speak","human","person","samuel"], a:"We're message-first: hit any \"message us\" button and a human replies, usually within a working day. No phone calls unless you ask for one. Want me to hand you over now?", l:[] },
    { k:["refund","return","guarantee","terms","licence","license","withdrawal"], a:"Terms, licence and refunds (including your EU withdrawal rights) are written in plain language on the terms page — EU consumer law applies.", l:[["Terms & refunds","/legal/terms.html"]] },
    { k:["privacy","gdpr","data","tracking","cookies"], a:"The site runs without tracking, the quiz runs entirely in your browser, and this chat never leaves your device either. You message us first — that's your consent for a reply; we delete threads on request.", l:[["Privacy","/legal/privacy.html"]] },
    { k:["bot","robot","ai","model","lea","who"], a:"Honest answer (EU AI Act and all): I'm an automated assistant — a scripted helper answering from this site's own content, nothing more. Not a human, never pretending to be one. Ask for a human any time and I'll hand you straight over.", l:[] },
    { k:["pet","companion","fox","sheep","sprout","avatar","cute"], a:"Pick your travel companion in my header — Lea the sprout, Penny the fox or Mossy the sheep. Whoever you pick rides this bubble with you. (They're all me with different hats, between us.)", l:[] },
    { k:["update","free","forever","subscription","monthly"], a:"Toolkits are one-time purchases with free regulatory updates — when a rule changes, the fix comes to you at no charge. No subscription trap.", l:[] },
    { k:["where","based","ferns","wexford","ireland","local","gorey","enniscorthy"], a:"Leanta is based in Ferns, Co. Wexford and works the surrounding 30 km — Enniscorthy, Bunclody, Gorey, Camolin, Courtown and around. Close enough to actually drive out.", l:[] },
    { k:["trade","trades","shop","farm","farmer","school","doctor","dentist","clinic","manufacturing","factory"], a:"Every world on this journey is a real trade we work with — shops, trades, manufacturing, farms, schools and clinics. Tell me yours and I'll point you to the right pack or the readiness check.", l:[["Take the readiness check","/quiz.html"]] },
    { k:["haccp","allergen","allergens","temperature","fire","safety","training","traceability"], a:"Covered: HACCP plans, 14-allergen matrices, temperature logs, fire registers, safety statements, training matrices and supplier traceability — the records inspectors actually ask for, designed so they take seconds to keep.", l:[["Which pack fits? Take the check","/quiz.html"]] },
    { k:["music","sound","audio","song","suno"], a:"The sound control plays the ambient theme — off until you turn it on. There's an ADHD-focus track too. Headphones recommended.", l:[] },
    { k:["hello","hi","hey","morning","evening"], a:"Hello! Ask me about the toolkits, the free readiness check, or the €200 grant pathway — or say \"human\" and I'll hand you over to a real person.", l:[] }
  ];
  function mailHref(qRaw){ /* assembled at runtime so the address isn't a scrapeable literal in source */
    var addr = cfg.contactEmail || (["hello","leanta.ie"].join("@"));
    return "mailto:"+addr+"?subject="+encodeURIComponent("Question from the journey")+"&body="+encodeURIComponent('Hi Leanta — I asked: "'+qRaw+'" — could a human pick this up?'); }
  function answer(qRaw){ var q=qRaw.toLowerCase().replace(/[^\wÀ-ž€ ]/g," "), words=q.split(/\s+/).filter(Boolean), best=null, bestScore=0;
    KB.forEach(function (entry){ var s=0; entry.k.forEach(function (kw){ if (words.indexOf(kw)!==-1) s+=2; else if (q.indexOf(kw)!==-1) s+=1; }); if (s>bestScore){ bestScore=s; best=entry; } });
    if (best && bestScore>=2) return { text:best.a, links:best.l };
    var handoff=[["Message a human", mailHref(qRaw)]];
    if (cfg.contactPhone) handoff.unshift(["WhatsApp a human","https://wa.me/"+cfg.contactPhone.replace(/[^0-9]/g,"")+"?text="+encodeURIComponent('Hi Leanta — I asked: "'+qRaw+'"')]);
    return { text:"That one's beyond my script — I only know what's on this site. A human will know though: message us and we reply within a working day (no call unless you ask).", links:handoff }; }
  function addMsg(text, who, links){ var d=document.createElement("div"); d.className="msg "+who; d.textContent=text;
    if (links && links.length) links.forEach(function (ln){ d.appendChild(document.createElement("br")); var a=document.createElement("a");
      a.href=ln[1]; a.textContent="→ "+ln[0]; if (ln[1].indexOf("http")===0) a.rel="noopener"; d.appendChild(a); });
    msgs.appendChild(d); msgs.scrollTop=msgs.scrollHeight; }
  function botReply(q){ var typing=document.createElement("div"); typing.className="msg bot typing"; typing.innerHTML="<i></i><i></i><i></i>";
    msgs.appendChild(typing); msgs.scrollTop=msgs.scrollHeight; setMood("talking");
    var res=answer(q); /* LEA_UPGRADE: swap for fetch("/api/lea") when a server endpoint exists */
    setTimeout(function (){ typing.remove(); addMsg(res.text,"bot",res.links); setMood("happy",1500); speakIfOn(res.text); }, 480+Math.min(900,q.length*14)); }

  var voiceBtn=document.getElementById("lea-voice"), voiceOn=false;
  function speakIfOn(text){ if (!voiceOn || !("speechSynthesis" in window) || !text) return;
    try { speechSynthesis.cancel(); var u=new SpeechSynthesisUtterance(text); u.rate=1.04; u.pitch=1.18; u.volume=0.9;
      var vs=speechSynthesis.getVoices(); var pick=vs.find(function (v){ return /en-IE|Irish/i.test(v.lang+" "+v.name); })||vs.find(function (v){ return /en-GB/i.test(v.lang); })||vs.find(function (v){ return v.lang&&v.lang.indexOf("en")===0; });
      if (pick) u.voice=pick; speechSynthesis.speak(u); } catch (e) {} }
  if (voiceBtn) voiceBtn.addEventListener("click", function (){ voiceOn=!voiceOn; voiceBtn.setAttribute("aria-pressed", String(voiceOn));
    voiceBtn.textContent=voiceOn?"🔈":"🔊"; if (!voiceOn){ try { speechSynthesis.cancel(); } catch (e) {} } else speakIfOn("Hi — I'm "+currentPet().name+". I'll read my answers aloud now."); });

  if (orb && panelLea){
    /* companion-as-navigator: some chips fly the camera (with a witty line),
       others answer from the KB. This is how the pet "takes you" places. */
    var CHIPS = [
      { label:"✈ Fly me to the €200 grant", to:0.78, say:"Hop on — grant bay coming up. €200 in, the LEO carries the rest. 🚀" },
      { label:"✈ Take me to 'Would you pass?'", to:0.96, say:"Buckle up — the question that started all this is at the end of the flight." },
      { label:"Which pack fits my trade?" },
      { label:"Will I pass next week's inspection?" },
      { label:"Talk to a human" }
    ];
    CHIPS.forEach(function (c){ var b=document.createElement("button"); b.type="button"; b.textContent=c.label;
      b.addEventListener("click", function (){ addMsg(c.label,"user");
        if (c.to!=null && window.__flyTo){ if (c.say) addMsg(c.say,"bot"); setMood("happy",1500); speakIfOn(c.say||""); window.__flyTo(c.to); }
        else botReply(c.label); });
      chipsBox.appendChild(b); });
    var greeted=false;
    function toggleLea(open){ panelLea.hidden=!open; orb.setAttribute("aria-expanded", String(open));
      if (open){ setMood("surprised",1000); if (!greeted){ greeted=true; var g="Hi — I'm "+currentPet().name+", Leanta's automated helper (not a human, happy to fetch one). What's eating your week?"; addMsg(g,"bot"); speakIfOn(g); } leaInput.focus(); } }
    window.__leaOpen = function (){ toggleLea(true); };
    orb.addEventListener("click", function (){ toggleLea(panelLea.hidden); });
    document.getElementById("lea-close").addEventListener("click", function (){ toggleLea(false); });
    addEventListener("keydown", function (e){ if (e.key==="Escape" && !panelLea.hidden) toggleLea(false); });
    leaForm.addEventListener("submit", function (e){ e.preventDefault(); var q=leaInput.value.trim(); if (!q) return; leaInput.value=""; addMsg(q,"user"); botReply(q); });
  }
  var sayHello = document.getElementById("say-hello");
  if (sayHello) sayHello.addEventListener("click", function (){ if (window.__leaOpen) window.__leaOpen(); });
  var pickPet = document.getElementById("pick-pet");
  if (pickPet) pickPet.addEventListener("click", function (){ if (window.__leaOpen) window.__leaOpen(); });
}

/* ==========================================================================
   SOUND — ambient/focus tracks (mp3) with WebAudio pad fallback; OFF default
   ========================================================================== */
function initSound(){
  var btn=document.getElementById("sound"), modeBtn=document.getElementById("soundmode"), modeLabel=document.getElementById("soundmode-label");
  var SRC={ ambient:"/v4/assets/leanta-theme.mp3", focus:"/v4/assets/leanta-focus.mp3" };
  var engines={}, mode="ambient", playing=false;
  function mp3Engine(src){ var a=new Audio(src); a.loop=true; a.volume=0.55; return { start:function (){ a.play().catch(function (){}); }, stop:function (){ a.pause(); } }; }
  function padEngine(){ var ctx, nodes=[]; function build(){ ctx=new (window.AudioContext||window.webkitAudioContext)(); var g=ctx.createGain(); g.gain.value=0; g.connect(ctx.destination);
      [[110,"sine",1],[165.1,"triangle",0.5],[220.6,"sine",0.22]].forEach(function (cf){ var o=ctx.createOscillator(); o.type=cf[1]; o.frequency.value=cf[0]; var og=ctx.createGain(); og.gain.value=0.05*cf[2]; o.connect(og); og.connect(g); o.start(); nodes.push(o); });
      g.gain.linearRampToValueAtTime(0.12, ctx.currentTime+1.6); ctx._g=g; }
    return { start:function (){ if (!ctx) build(); if (ctx.state==="suspended") ctx.resume(); }, stop:function (){ if (ctx){ ctx._g.gain.linearRampToValueAtTime(0,ctx.currentTime+0.4); } } }; }
  function engineFor(m, cb){ if (engines[m]) return cb(engines[m]);
    fetch(SRC[m], { method:"HEAD" }).then(function (r){ engines[m]=r.ok?mp3Engine(SRC[m]):padEngine(); cb(engines[m]); }).catch(function (){ engines[m]=padEngine(); cb(engines[m]); }); }
  function play(){ engineFor(mode, function (eng){ eng.start(); }); playing=true; btn.classList.add("on"); btn.setAttribute("aria-pressed","true"); btn.setAttribute("aria-label","Sound on"); if (modeBtn) modeBtn.hidden=false; }
  function stop(){ Object.keys(engines).forEach(function (m){ engines[m].stop(); }); playing=false; btn.classList.remove("on"); btn.setAttribute("aria-pressed","false"); btn.setAttribute("aria-label","Sound off"); }
  if (btn) btn.addEventListener("click", function (){ playing?stop():play(); });
  if (modeBtn) modeBtn.addEventListener("click", function (){ var was=playing; if (playing) stop(); mode=(mode==="ambient")?"focus":"ambient";
    if (modeLabel) modeLabel.textContent=(mode==="ambient")?"Ambient":"Focus"; modeBtn.setAttribute("aria-pressed", String(mode==="focus")); if (was) play(); });
}

/* ==========================================================================
   LEAD — composes a message in the visitor's own mail app; never posts data
   ========================================================================== */
function initLead(){
  var form=document.getElementById("lead"); if (!form) return;
  document.querySelectorAll(".fld input").forEach(function (inp){ inp.addEventListener("input", function (){ inp.parentElement.classList.toggle("filled", inp.value.trim().length>1); }); });
  form.addEventListener("submit", function (e){ e.preventDefault();
    var name=(document.getElementById("f-name")||{}).value||"", biz=(document.getElementById("f-biz")||{}).value||"", pain=(document.getElementById("f-pain")||{}).value||"";
    var addr=(window.LEANTA&&window.LEANTA.contactEmail)||(["hello","leanta.ie"].join("@"));
    var body="Hi Leanta,\n\n"+(name?("I'm "+name+". "):"")+(biz?("We're "+biz+". "):"")+"\n\nWhat eats our week: "+(pain||"(tell us)")+"\n\nCould you point us in the right direction?\n";
    window.location.href="mailto:"+addr+"?subject="+encodeURIComponent("A hello from the journey")+"&body="+encodeURIComponent(body);
    var done=document.getElementById("lead-done"); if (done) done.hidden=false;
  });
}
