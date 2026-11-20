/* Aoi's 3D scenes: toon-shaded (cel-shaded) like a bright adventure game, and you can drag to
   turn them on every axis, pinch or scroll to zoom, and tap things to name them.
   Loaded only when a 3D step is shown. three.js is MIT-licensed (THREE-LICENSE.txt). */
import * as THREE from './three.module.min.js';
import { OrbitControls } from './OrbitControls.js';

const PAL = { sky: 0x8fd6ff, skyLow: 0xd8f3ff, grass: 0x8cc84b, sun: 0xffd166, coral: 0xff6b6b, teal: 0x2ec4b6,
  cream: 0xfff3d6, ink: 0x2b2d42, night: 0x0b1440, blue: 0x4f8dff, red: 0xff5d73, pink: 0xffa3b5 };

function toonGradient(){
  const data = new Uint8Array([90, 170, 255]); /* three flat bands of light: the cel look */
  const tex = new THREE.DataTexture(data, 3, 1, THREE.RedFormat);
  tex.minFilter = tex.magFilter = THREE.NearestFilter; tex.needsUpdate = true;
  return tex;
}
const GRAD = toonGradient();
const toon = (color, extra) => new THREE.MeshToonMaterial(Object.assign({ color, gradientMap: GRAD }, extra || {}));
/* A thin dark outline behind each shape, for the drawn-cartoon edge. */
function outlined(mesh, scale){
  const o = new THREE.Mesh(mesh.geometry, new THREE.MeshBasicMaterial({ color: PAL.ink, side: THREE.BackSide }));
  o.scale.setScalar(scale || 1.04); mesh.add(o); return mesh;
}
function labelSprite(text, color){
  const c = document.createElement('canvas'), g = c.getContext('2d'), f = 44;
  g.font = `800 ${f}px "M PLUS Rounded 1c", sans-serif`;
  const w = Math.ceil(g.measureText(text).width) + 28; c.width = w; c.height = f + 24;
  g.font = `800 ${f}px "M PLUS Rounded 1c", sans-serif`;
  g.fillStyle = 'rgba(255,255,255,.88)'; g.strokeStyle = '#2b2d42'; g.lineWidth = 5;
  const r = 18; g.beginPath(); g.roundRect ? g.roundRect(3, 3, w - 6, f + 18, r) : g.rect(3, 3, w - 6, f + 18); g.fill(); g.stroke();
  g.fillStyle = color || '#2b2d42'; g.textBaseline = 'middle'; g.fillText(text, 14, (f + 24) / 2 + 2);
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), depthTest: false }));
  s.scale.set(w / 90, (f + 24) / 90, 1); s.renderOrder = 10;
  return s;
}

/* --- scenes --- */
const PLANETS = [ /* name, Japanese, toon colour, radius (not to scale), orbit radius (not to scale) */
  ['Mercury', '水星', 0xb8b1a6, 0.35, 4], ['Venus', '金星', 0xf3c969, 0.55, 5.6], ['Earth', '地球', 0x4f9dff, 0.6, 7.4],
  ['Mars', '火星', 0xff7b4f, 0.45, 9], ['Jupiter', '木星', 0xe7b98b, 1.5, 12.5], ['Saturn', '土星', 0xf2dc9b, 1.25, 16.5],
  ['Uranus', '天王星', 0x9fe6f0, 0.9, 20], ['Neptune', '海王星', 0x4f6fff, 0.88, 23]];
function solar(scene, cam, pick){
  scene.background = new THREE.Color(PAL.night);
  cam.position.set(0, 18, 30);
  const sun = new THREE.Mesh(new THREE.SphereGeometry(2.4, 40, 24), new THREE.MeshBasicMaterial({ color: PAL.sun }));
  sun.userData.name = 'The Sun · 太陽'; scene.add(outlined(sun, 1.03)); pick.push(sun);
  scene.add(new THREE.PointLight(0xffffff, 300, 0, 1.6)); scene.add(new THREE.AmbientLight(0xffffff, 0.35));
  const movers = [];
  PLANETS.forEach(([en, jp, col, r, orbit], i) => {
    const ring = new THREE.Mesh(new THREE.RingGeometry(orbit - 0.03, orbit + 0.03, 96), new THREE.MeshBasicMaterial({ color: 0x9fb4ff, side: THREE.DoubleSide, transparent: true, opacity: 0.35 }));
    ring.rotation.x = Math.PI / 2; scene.add(ring);
    const p = outlined(new THREE.Mesh(new THREE.SphereGeometry(r, 32, 20), toon(col)));
    p.userData.name = `${en} · ${jp}`;
    if (en === 'Saturn'){ const rr = new THREE.Mesh(new THREE.RingGeometry(r * 1.4, r * 2.2, 48), toon(0xd9c38a, { side: THREE.DoubleSide })); rr.rotation.x = Math.PI / 2.4; p.add(rr); }
    if (en === 'Earth'){ const land = new THREE.Mesh(new THREE.SphereGeometry(r * 1.01, 24, 12, 0, 1.6, 0.6, 1.2), toon(PAL.grass)); p.add(land); }
    if (en === 'Jupiter'){ [-0.3, 0.25].forEach(y => { const b = new THREE.Mesh(new THREE.TorusGeometry(r * Math.cos(y) * 1.0, 0.07, 6, 48), toon(0xc58a5a)); b.rotation.x = Math.PI / 2; b.position.y = r * Math.sin(y); p.add(b); }); }
    const a = i * 0.9; p.position.set(Math.cos(a) * orbit, 0, Math.sin(a) * orbit);
    scene.add(p); pick.push(p); movers.push({ p, orbit, a, speed: 0.6 / Math.pow(orbit, 1.5) });
  });
  return t => movers.forEach(m => { const a = m.a + t * m.speed; m.p.position.set(Math.cos(a) * m.orbit, 0, Math.sin(a) * m.orbit); m.p.rotation.y = t * 0.5; });
}
/* Real star directions: RA (hours) and Dec (degrees), J2000, placed on a big sphere around you. */
function skyDome(scene, cam, pick, opts){
  scene.background = new THREE.Color(0x0a1238);
  cam.position.set(0, 0, 0.01);
  const R = 60, pos = (ra, dec) => { const a = ra / 24 * Math.PI * 2, d = dec * Math.PI / 180; return new THREE.Vector3(-Math.cos(d) * Math.cos(a) * R, Math.sin(d) * R, Math.cos(d) * Math.sin(a) * R); };
  const stars = opts.stars, mats = {};
  Object.keys(stars).forEach(id => {
    const s = stars[id], size = Math.max(0.35, 1.3 - s[4] * 0.28), col = id === 'betelgeuse' ? 0xffb08a : id === 'rigel' ? 0xcfe0ff : 0xffffff;
    const m = new THREE.Mesh(new THREE.SphereGeometry(size, 12, 8), new THREE.MeshBasicMaterial({ color: col }));
    m.position.copy(pos(s[2], s[3])); m.userData.name = s[1] ? `${s[0]} · ${s[1]}` : s[0]; scene.add(m); pick.push(m);
    if (s[4] < 1.9 || s[1]){ const l = labelSprite(s[1] ? `${s[0]} ${s[1]}` : s[0], '#2b2d42'); l.position.copy(pos(s[2], s[3] - 3)); l.scale.multiplyScalar(4.2); scene.add(l); }
  });
  const lineMat = new THREE.LineBasicMaterial({ color: 0x7ec8e3 });
  (opts.lines || []).forEach(([a, b]) => { const g = new THREE.BufferGeometry().setFromPoints([pos(stars[a][2], stars[a][3]), pos(stars[b][2], stars[b][3])]); scene.add(new THREE.Line(g, lineMat)); });
  /* a few hundred faint background stars, randomly placed, just for atmosphere */
  const bg = new THREE.BufferGeometry(), pts = [];
  for (let i = 0; i < 600; i++){ const v = new THREE.Vector3().randomDirection().multiplyScalar(R * 1.4); pts.push(v.x, v.y, v.z); }
  bg.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
  scene.add(new THREE.Points(bg, new THREE.PointsMaterial({ color: 0x9fb4ff, size: 0.25 })));
  /* look first towards the chosen star */
  const look = opts.look ? pos(stars[opts.look][2], stars[opts.look][3]) : new THREE.Vector3(0, 0, -1);
  cam.position.copy(look.clone().normalize().multiplyScalar(-0.01));
  return null;
}
/* A simplified cartoon heart: the four chambers and the big vessels in the right places,
   blue for the right side (oxygen-poor blood) and red for the left (oxygen-rich). */
function heart(scene, cam, pick, opts){
  scene.background = new THREE.Color(PAL.skyLow);
  cam.position.set(0, 0.6, 9);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x9fd6ff, 1.1)); const d = new THREE.DirectionalLight(0xffffff, 1.6); d.position.set(4, 6, 8); scene.add(d);
  const g = new THREE.Group(); g.rotation.z = -0.35; /* tipped to the left, as in the chest */ scene.add(g);
  const blob = (x, y, z, sx, sy, sz, col, name) => { const m = outlined(new THREE.Mesh(new THREE.SphereGeometry(1, 32, 20), toon(col))); m.position.set(x, y, z); m.scale.set(sx, sy, sz); m.userData.name = name; g.add(m); pick.push(m); return m; };
  /* the person's right is on the viewer's left, as in anatomy pictures */
  blob(-1.05, 0.95, 0.2, 0.95, 0.85, 0.85, PAL.blue, 'Right atrium · 右心房');
  blob(-0.45, -0.55, 0.6, 1.25, 1.45, 1.0, 0x6fa8ff, 'Right ventricle · 右心室');
  blob(0.95, 0.9, -0.4, 0.95, 0.8, 0.85, PAL.red, 'Left atrium · 左心房');
  blob(0.75, -0.75, 0.0, 1.2, 1.6, 1.05, 0xff7a8c, 'Left ventricle · 左心室');
  const tube = (pts, r, col, name) => { const c = new THREE.CatmullRomCurve3(pts.map(p => new THREE.Vector3(...p))); const m = outlined(new THREE.Mesh(new THREE.TubeGeometry(c, 40, r, 14), toon(col)), 1.06); m.userData.name = name; g.add(m); pick.push(m); };
  tube([[0.2, 0.9, 0.2], [0.0, 2.2, 0.1], [0.9, 2.8, -0.2], [1.6, 2.1, -0.4], [1.7, 0.6, -0.8]], 0.36, 0xff3f5e, 'Aorta · 大動脈 (to the body)');
  tube([[-0.25, 0.7, 0.9], [-0.3, 2.0, 0.8], [0.6, 2.5, 0.5]], 0.3, 0x3f73e6, 'Pulmonary artery · 肺動脈 (to the lungs)');
  tube([[-1.4, 1.4, 0.1], [-1.45, 3.0, 0.0]], 0.27, 0x2f5fd0, 'Superior vena cava · 上大静脈 (from the body)');
  if (opts.face){ /* a friendly face for the very first look */
    [[-0.2, -0.2], [0.5, -0.2]].forEach(([x, y]) => { const e = new THREE.Mesh(new THREE.SphereGeometry(0.13, 16, 10), new THREE.MeshBasicMaterial({ color: PAL.ink })); e.position.set(x, y, 1.62); g.add(e); });
    const sm = new THREE.Mesh(new THREE.TorusGeometry(0.25, 0.05, 8, 24, Math.PI), new THREE.MeshBasicMaterial({ color: PAL.ink })); sm.position.set(0.15, -0.55, 1.6); sm.rotation.z = Math.PI; g.add(sm);
  }
  return t => { const beat = 1 + Math.max(0, Math.sin(t * 7.5)) * 0.04; g.scale.setScalar(beat); };
}
const SCENES = { solar, sky: skyDome, heart };

export function mount(el, name, opts){
  opts = opts || {};
  const w = el.clientWidth || 340, h = el.clientHeight || 300;
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1)); renderer.setSize(w, h);
  el.appendChild(renderer.domElement);
  const scene = new THREE.Scene(), cam = new THREE.PerspectiveCamera(name === 'sky' ? 70 : 45, w / h, 0.005, 500), pick = [];
  const tick = SCENES[name](scene, cam, pick, opts);
  const ctl = new OrbitControls(cam, renderer.domElement);
  ctl.enableDamping = true; ctl.enablePan = false;
  if (name === 'sky'){ ctl.target.set(0, 0, 0); ctl.rotateSpeed = -0.35; ctl.enableZoom = false; ctl.minPolarAngle = 0; ctl.maxPolarAngle = Math.PI; }
  else { ctl.autoRotate = !!opts.spin; ctl.autoRotateSpeed = 1.2; }
  const tip = document.createElement('div'); tip.className = 'three-tip'; el.appendChild(tip);
  const ray = new THREE.Raycaster(), v2 = new THREE.Vector2();
  let downAt = null;
  renderer.domElement.addEventListener('pointerdown', e => { downAt = [e.clientX, e.clientY]; });
  renderer.domElement.addEventListener('pointerup', e => {
    if (!downAt || Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) > 6) return; /* a drag, not a tap */
    const r = renderer.domElement.getBoundingClientRect();
    v2.set((e.clientX - r.left) / r.width * 2 - 1, -(e.clientY - r.top) / r.height * 2 + 1);
    ray.setFromCamera(v2, cam);
    const hit = ray.intersectObjects(pick, false)[0];
    let o = hit && hit.object; while (o && !o.userData.name) o = o.parent;
    if (o){ tip.textContent = o.userData.name; tip.classList.add('on'); if (opts.onPick) opts.onPick(o.userData.name); }
  });
  let alive = true; const t0 = performance.now();
  (function loop(){ if (!alive) return; const t = (performance.now() - t0) / 1000; if (tick) tick(t); ctl.update(); renderer.render(scene, cam); requestAnimationFrame(loop); })();
  return () => { alive = false; ctl.dispose(); renderer.dispose(); scene.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) [].concat(o.material).forEach(m => { if (m.map) m.map.dispose(); m.dispose(); }); }); el.innerHTML = ''; };
}
