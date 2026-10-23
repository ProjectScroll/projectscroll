"""The 3D pages: Cassopolis in LiDAR (the real 2015 survey points) and, later, the river valley.
python3 _tools/build_3d.py   (the data files in map/3d/cassopolis/ are made once from the survey; see the note at the foot of the page)"""
import sys, pathlib, json, html
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
R = pathlib.Path(__file__).resolve().parents[1]
E = html.escape
M = json.load(open(R / 'map/3d/cassopolis/meta.json'))
V = '0.169.0'
# the 1860 town plan (the same picture and placing as the then-and-now page)
PLAN = dict(src='/img/cass1860.webp', N=41.917772, W=-86.018103, S=41.906100, E=-86.007168)
SPOTS = [('The Cass County Courthouse', 41.91167, -86.01278, 22), ('Stone Lake', 41.9042, -86.0175, 12), ('Diamond Lake', 41.8980, -85.9890, 12), ('Grand Island', 41.9039, -85.9769, 18)]

body = f'''    <p class="crumb"><a href="/map/">← The map room</a></p>
    <p class="kicker">Cassopolis in LiDAR</p>
    <h1>The county seat, laser by laser</h1>
    <p class="lede" style="font-size:1.15rem">In 2015 an aircraft flew over Cass County firing laser pulses at the ground, hundreds of thousands a second, and timing each echo. Every dot below is one of those echoes: {M['n']:,} of them, from the blocks around the courthouse. Around them lies the land the same survey measured, from Stone Lake to Diamond Lake, about six kilometres across. Turn it, tilt it, and lay the 1860 town plan over the real ground.</p>
    <figure class="l3d" id="l3d" aria-label="A three-dimensional model of Cassopolis, Stone Lake and Diamond Lake built from laser survey data">
      <canvas id="l3dC" aria-hidden="true"></canvas>
      <div class="l3d-ui" role="toolbar" aria-label="Model controls">
        <button type="button" class="l3d-b" id="l3dPlan" aria-pressed="false">1860 plan</button>
        <button type="button" class="l3d-b" id="l3dTrees" aria-pressed="true">Trees</button>
        <button type="button" class="l3d-b" id="l3dTall" aria-pressed="false">Height ×3</button>
        <button type="button" class="l3d-b" id="l3dSpin" aria-pressed="false">Fly around</button>
        <button type="button" class="l3d-b" id="l3dReset">Reset view</button>
        <button type="button" class="l3d-b" id="l3dFull">Full screen</button>
      </div>
      <div class="l3d-tags" id="l3dTags" aria-hidden="true"></div>
      <p class="l3d-load" id="l3dLoad" role="status">Loading the survey…</p>
      <p class="l3d-help">Drag to turn · scroll or pinch to zoom · right-drag or two fingers to move</p>
      <noscript><img src="/img/l3d-cassopolis.webp" width="1058" height="898" alt="Central Cassopolis from above, built from laser survey points: buildings in gold, trees in green, on the bare ground."></noscript>
    </figure>
    <ul class="l3d-key" aria-label="What the colours mean">
      <li><i style="background:#e8b84a"></i>Buildings, {M['nb']:,} points</li>
      <li><i style="background:#3fb38a"></i>Trees, {M['nv']:,} points</li>
      <li><i style="background:#2c5f7a"></i>The bare ground, with a contour every two metres</li>
      <li><i style="background:#1c56a0"></i>Stone Lake and Diamond Lake</li>
    </ul>
    <h2>What you are looking at</h2>
    <ul class="dis">
      <li><b>Real survey points, not a drawing.</b> Each dot is a laser return recorded by the U.S. Geological Survey’s 2015 flight over Cass County, placed to within a few centimetres. Roof shapes, chimneys and the crowns of single trees are all there because the laser hit them.</li>
      <li><b>The ground.</b> The survey marks which returns struck bare earth. Those make the surface underneath, a model of the land with the buildings and trees taken off. It rises about {M['ground_range'][1]-M['ground_range'][0]:.0f} metres across these blocks.</li>
      <li><b>Buildings and trees.</b> The survey does not say which of the other points are roofs and which are leaves, so we sorted them: a laser pulse that hits a roof comes back once; one that hits a tree comes back several times, from leaves, branches and the ground below. Flat, single echoes in a patch the size of a building are coloured gold. A few porches and dense evergreens may be the wrong colour.</li>
      <li><b>The lakes and the land around.</b> Stone Lake lies just west of the courthouse, and Diamond Lake, with Grand Island in it, a short way east. The wider ground comes from the same 2015 flight, as the survey’s bare-earth elevation: the shape of the land every six metres or so, and its light and shade from a grid one and a half metres apart, sharp enough to show field edges, ditches and old roadbeds. The lakes are drawn flat at their surface, because the survey does not see through water. Buildings and trees are shown only in the town blocks, where every point is kept.</li>
      <li><b>The 1860 plan.</b> Press <i>1860 plan</i> to lay the town plan from the 1860 county wall map on the ground. Its west part reaches into these blocks. Compare it with the <a href="/map/cassopolis/">flat then-and-now page</a>.</li>
      <li><b>Height ×3.</b> The town is fairly level, so tripling the heights makes the rise of the land easier to see. The buildings stretch too.</li>
    </ul>
    <p class="note">Source: U.S. Geological Survey, 3D Elevation Program, Michigan Cass County LiDAR, 2015 (public domain), read from the survey’s public point-cloud archive. About one in two tree points is shown, to keep the page light; every building point is kept. The points cover the blocks north and east of the courthouse; the ground around them is the survey’s bare-earth elevation from the 3D Elevation Program, shaped every six metres or so and shaded from a grid about one and a half metres apart. Town plan: <i>Map of the Counties of Cass, Van Buren and Berrien, Michigan</i> (Geil, Harley &amp; Siverd, 1860), Library of Congress. 3D drawing by three.js.</p>
    <script type="importmap">{{"imports":{{"three":"/vendor/three-{V}/three.module.min.js"}}}}</script>
    <script type="module">
    import * as THREE from 'three';
    import {{ OrbitControls }} from '/vendor/three-{V}/OrbitControls.min.js';
    (async()=>{{
    const M={json.dumps(M)}, PLAN={json.dumps(PLAN)}, SPOTS={json.dumps(SPOTS)};
    const fig=document.getElementById('l3d'), cv=document.getElementById('l3dC'), load=document.getElementById('l3dLoad'), tags=document.getElementById('l3dTags');
    const still=matchMedia('(prefers-reduced-motion: reduce)').matches;
    let gl; try{{ gl=new THREE.WebGLRenderer({{canvas:cv, antialias:true, powerPreference:'high-performance'}}); }}catch(e){{ load.textContent='This browser cannot draw 3D. Here is the model from above.'; fig.classList.add('no3d'); return; }}
    gl.setPixelRatio(Math.min(devicePixelRatio,2)); gl.setClearColor(0x0b1622,1);
    const scene=new THREE.Scene(); scene.fog=new THREE.Fog(0x0b1622,2600,9000);
    const cam=new THREE.PerspectiveCamera(45,1,1,20000);
    const ctl=new OrbitControls(cam,cv); ctl.enableDamping=true; ctl.dampingFactor=.08; ctl.maxPolarAngle=Math.PI*.47; ctl.minDistance=40; ctl.maxDistance=7000; ctl.autoRotateSpeed=.6;
    const home=()=>{{ const k=Math.max(1,1.35/Math.max(.3,cam.aspect)); ctl.target.set(950,0,800); cam.position.set(950-2450*k,1700*k,800+1900*k); ctl.update(); }}; home();
    const world=new THREE.Group(); scene.add(world);
    const ll2xz=(lat,lon)=>[ (lon-M.west)/(M.east-M.west)*M.w-M.w/2, -((lat-M.south)/(M.north-M.south)*M.h-M.h/2) ];
    const [g,p]=await Promise.all([fetch('ground.bin').then(r=>r.arrayBuffer()), fetch('points.bin').then(r=>{{ if(!r.ok) throw 0; return r.arrayBuffer(); }})]).catch(()=>[null,null]);
    /* the wider ground's heights come packed in a picture: red is the high byte, green the low, in centimetres above 250 m */
    const wb=await fetch('wide.png').then(r=>r.ok?r.blob():null).then(b=>b&&createImageBitmap(b,{{colorSpaceConversion:'none',premultiplyAlpha:'none'}})).then(bm=>{{ if(!bm) return null; const c=document.createElement('canvas'); c.width=bm.width; c.height=bm.height; const x=c.getContext('2d',{{willReadFrequently:true}}); x.drawImage(bm,0,0); const d=x.getImageData(0,0,c.width,c.height).data, o=new Uint16Array(c.width*c.height); for(let k=0;k<o.length;k++) o[k]=(d[k*4]<<8)|d[k*4+1]; return o; }}).catch(()=>null);
    if (!g){{ load.textContent='The survey could not be loaded. Try again when you are online.'; return; }}
    /* the bare ground: a 2 m grid, shaded by slope, with a faint contour every metre and the old plan laid on when asked */
    const hgt=new Uint16Array(g), gx=M.gx, gy=M.gy;
    const geo=new THREE.PlaneGeometry((gx-1)*M.step,(gy-1)*M.step,gx-1,gy-1); geo.rotateX(-Math.PI/2);
    const pos=geo.attributes.position; for (let j=0;j<gy;j++) for (let i=0;i<gx;i++){{ const v=j*gx+i, srcRow=gy-1-j; pos.setY(v, hgt[srcRow*gx+i]/100); }}
    geo.translate(-M.w/2+((gx-1)*M.step)/2,0,M.h/2-((gy-1)*M.step)/2); geo.computeVertexNormals();
    const hdTex=new THREE.TextureLoader().load('ground-hd.webp'); hdTex.colorSpace=THREE.SRGBColorSpace; hdTex.anisotropy=8;
    const planTex=new THREE.TextureLoader().load(PLAN.src); planTex.colorSpace=THREE.SRGBColorSpace; planTex.anisotropy=8;
    const gu={{uPlan:{{value:0}}, uTex:{{value:planTex}}, uBox:{{value:new THREE.Vector4(M.west,M.east,M.south,M.north)}}, uPB:{{value:new THREE.Vector4(PLAN.W,PLAN.E,PLAN.S,PLAN.N)}}, uSize:{{value:new THREE.Vector2(M.w,M.h)}}, uHD:{{value:hdTex}}, uWB:{{value:new THREE.Vector4(M.wwest,M.weast,M.wsouth,M.wnorth)}}}};
    const gmat=new THREE.ShaderMaterial({{uniforms:gu, vertexShader:`varying vec3 vN; varying vec3 vP; void main(){{ vN=normal; vP=position; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }}`,
      fragmentShader:`uniform float uPlan; uniform sampler2D uTex, uHD; uniform vec4 uBox, uPB, uWB; uniform vec2 uSize; varying vec3 vN; varying vec3 vP;
      void main(){{ float sh=clamp(dot(normalize(vN),normalize(vec3(-.5,1.,.35))),0.,1.); vec3 c=mix(vec3(.003,.01,.02),vec3(.025,.075,.12),sh);
        float h=vP.y*.5; float fw=max(fwidth(h),1e-4); float l=(1.-smoothstep(0.,1.,abs(fract(h-.5)-.5)/fw))*(1.-smoothstep(.15,.45,fw)); c=mix(c,vec3(.08,.42,.48),l*.35);
        float lon=uBox.x+(vP.x/uSize.x+.5)*(uBox.y-uBox.x), lat=uBox.z+(-vP.z/uSize.y+.5)*(uBox.w-uBox.z);
        vec2 uv=vec2((lon-uPB.x)/(uPB.y-uPB.x),(lat-uPB.z)/(uPB.w-uPB.z));
        vec2 hw=vec2((lon-uWB.x)/(uWB.y-uWB.x),(lat-uWB.z)/(uWB.w-uWB.z)); if (hw.x>=0. && hw.x<=1. && hw.y>=0. && hw.y<=1.) c=texture2D(uHD,hw).rgb*(.88+.24*sh);
        if (uPlan>0. && uv.x>=0. && uv.x<=1. && uv.y>=0. && uv.y<=1.){{ vec3 pc=texture2D(uTex,uv).rgb; c=mix(c,pc*mix(.75,1.05,sh),uPlan*.92); }}
        gl_FragColor=vec4(c,1.);
#include <colorspace_fragment>
      }}` }});
    const ground=new THREE.Mesh(geo,gmat); world.add(ground);
    /* the land around: the survey's bare-earth grid from Stone Lake to Diamond Lake, set a little lower under the town so the detailed ground lies on top; both share the sharp shaded picture */
    if (wb){{ const W=wb, wx=M.wgx, wy=M.wgy;
      const [x0,z0]=ll2xz(M.wnorth,M.wwest), [x1,z1]=ll2xz(M.wsouth,M.weast);
      const wg=new THREE.PlaneGeometry(x1-x0,z1-z0,wx-1,wy-1); wg.rotateX(-Math.PI/2); wg.translate((x0+x1)/2,0,(z0+z1)/2);
      const wp=wg.attributes.position, tx0=-M.w/2+3, tx1=M.w/2-3, tz0=-M.h/2+3, tz1=M.h/2-3;
      for (let k=0;k<wx*wy;k++){{ let y=W[k]/100+M.wbase-M.z0; const x=wp.getX(k), z=wp.getZ(k); if (x>tx0&&x<tx1&&z>tz0&&z<tz1) y-=1.2; wp.setY(k,y); }}
      wg.computeVertexNormals();
      const wide=new THREE.Mesh(wg,gmat); wide.renderOrder=-1; world.add(wide); }}
    /* the survey points: x, y, z in decimetres, a class (1 building, 2 tree) and a height shade */
    const n=M.n, dv=new DataView(p), P=new Float32Array(n*3), C=new Float32Array(n*3), K=new Float32Array(n);
    const gold=[new THREE.Color(0x9c6a1c),new THREE.Color(0xf6d27a)], leaf=[new THREE.Color(0x1d6b55),new THREE.Color(0x67d6a6)];
    for (let i=0;i<n;i++){{ const o=i*8, x=dv.getInt16(o,true)/10, y=dv.getInt16(o+2,true)/10, z=dv.getInt16(o+4,true)/10, k=dv.getUint8(o+6), s=dv.getUint8(o+7)/255;
      P[i*3]=x; P[i*3+1]=z; P[i*3+2]=-y; K[i]=k; const a=k===1?gold:leaf, t=Math.min(1,s*1.6); C[i*3]=a[0].r+(a[1].r-a[0].r)*t; C[i*3+1]=a[0].g+(a[1].g-a[0].g)*t; C[i*3+2]=a[0].b+(a[1].b-a[0].b)*t; }}
    const pg=new THREE.BufferGeometry(); pg.setAttribute('position',new THREE.BufferAttribute(P,3)); pg.setAttribute('color',new THREE.BufferAttribute(C,3)); pg.setAttribute('kind',new THREE.BufferAttribute(K,1));
    const pu={{uTrees:{{value:1}}, uPx:{{value:gl.getPixelRatio()}}, uTime:{{value:0}}}};
    const pmat=new THREE.ShaderMaterial({{uniforms:pu, transparent:true, depthWrite:true,
      vertexShader:`attribute float kind; attribute vec3 color; uniform float uTrees, uPx, uTime; varying vec3 vC; varying float vK;
        void main(){{ vC=color; vK=kind; vec4 mv=modelViewMatrix*vec4(position,1.); gl_Position=projectionMatrix*mv;
          float s=(kind<1.5?1.9:1.6)*uPx*260./-mv.z; if (kind>1.5 && uTrees<.5) s=0.; gl_PointSize=clamp(s,1.,7.); }}`,
      fragmentShader:`varying vec3 vC; varying float vK; void main(){{ vec2 d=gl_PointCoord-.5; float r=dot(d,d); if (r>.25) discard; float glow=vK<1.5?1.15:1.; gl_FragColor=vec4(vC*glow*(1.-r*1.2),1.);
#include <colorspace_fragment>
}}`}});
    world.add(new THREE.Points(pg,pmat));
    /* a soft gold ring marks the courthouse */
    const spots=SPOTS.map(([name,la,lo,hy])=>{{ const [x,z]=ll2xz(la,lo); const el=document.createElement('span'); el.className='l3d-tag'; el.textContent=name; tags.appendChild(el); return {{v:new THREE.Vector3(x,hy,z), el}}; }});
    const size=()=>{{ const w=cv.clientWidth, h=cv.clientHeight; gl.setSize(w,h,false); cam.aspect=w/h; cam.updateProjectionMatrix(); }};
    new ResizeObserver(size).observe(cv); size(); home();
    let tall=1, tallTo=1, plan=0, planTo=0;
    const B=(id,f)=>{{ const b=document.getElementById(id); b.addEventListener('click',()=>f(b)); return b; }};
    const press=(b,on)=>b.setAttribute('aria-pressed',String(on));
    B('l3dPlan',b=>{{ planTo=planTo?0:1; press(b,!!planTo); }});
    B('l3dTrees',b=>{{ pu.uTrees.value=pu.uTrees.value?0:1; press(b,!!pu.uTrees.value); }});
    B('l3dTall',b=>{{ tallTo=tallTo===1?3:1; press(b,tallTo===3); }});
    const spin=B('l3dSpin',b=>{{ ctl.autoRotate=!ctl.autoRotate; press(b,ctl.autoRotate); }});
    B('l3dReset',()=>home());
    B('l3dFull',()=>{{ if (document.fullscreenElement) document.exitFullscreen(); else if (fig.requestFullscreen) fig.requestFullscreen().catch(()=>{{}}); }});
    if (!still){{ ctl.autoRotate=true; press(spin,true); ctl.addEventListener('start',()=>{{ ctl.autoRotate=false; press(spin,false); }}, {{once:true}}); }}
    load.hidden=true; fig.classList.add('ready');
    let vis=true; new IntersectionObserver(es=>{{ vis=es[0].isIntersecting; }}).observe(fig);
    const tmp=new THREE.Vector3();
    gl.setAnimationLoop(()=>{{ if (!vis) return;
      tall+=(tallTo-tall)*(still?1:.12); plan+=(planTo-plan)*(still?1:.15); world.scale.y=tall; gu.uPlan.value=plan;
      ctl.update(); gl.render(scene,cam);
      const w=cv.clientWidth, h=cv.clientHeight; spots.forEach(s=>{{ tmp.copy(s.v); tmp.y*=tall; tmp.project(cam); const on=tmp.z<1; s.el.style.opacity=on&&Math.abs(tmp.x)<1.05&&Math.abs(tmp.y)<1.05?1:0; s.el.style.transform=`translate(${{(tmp.x*.5+.5)*w}}px,${{(-tmp.y*.5+.5)*h}}px)`; }});
    }});
    }})();
    </script>
'''
page('map/3d/cassopolis/index.html', 'Cassopolis in LiDAR · Project Scroll',
     f'Cassopolis, Stone Lake and Diamond Lake in 3D, from the 2015 Cass County LiDAR flight: {M["n"]:,} laser points in the town blocks, buildings in gold, trees in green, the 1860 town plan laid on the ground.',
     body, og='https://projectscroll.com/og/records.jpg')
print('3d cassopolis built', M['n'])

# ---------------- the St. Joseph River Valley in 3D ----------------
VJ = json.load(open(R / 'map/3d/valley/valley.json'))
VM = VJ['meta']
GOLD = [  # three lost towns, from the lost towns page; finding all three earns a badge
  dict(id='adamsport', name='Adamsport and Christiana', line='Two mill plats faced each other across Christiana Creek, and grew together as Adamsville.', lat=41.7853, lon=-85.9939),
  dict(id='wakelee', name='Wakelee', line='A lumber station on the new railroad, laid out in 1871. When the timber was cut, the reason for it went too.', lat=41.98389, lon=-85.87889),
  dict(id='waterford', name='Waterford', line='A mill town on the Elkhart River. In 1868 the dam came down and the mill moved to Goshen.', lat=41.54306, lon=-85.83056),
]
for g in GOLD:
    g['x'] = round((g['lon']-VM['lon0'])*VM['kx'], 3); g['z'] = round(-(g['lat']-VM['lat0'])*VM['kz'], 3)
body = f'''    <p class="crumb"><a href="/map/">← The map room</a></p>
    <p class="kicker">The valley in 3D</p>
    <h1>The St. Joseph River Valley</h1>
    <p class="lede" style="font-size:1.15rem">All {VM['area_km2']:,.0f} square kilometres that drain to the St. Joseph River, from the hills past Hillsdale to Lake Michigan, built from the U.S. Geological Survey’s laser-made elevation of the ground. The river and its branches are drawn in gold. Three lost towns are hidden in the hills: find all three.</p>
    <figure class="l3d l3d-v" id="l3d" aria-label="A three-dimensional model of the St. Joseph River watershed">
      <canvas id="l3dC" aria-hidden="true"></canvas>
      <div class="l3d-ui" role="toolbar" aria-label="Model controls">
        <button type="button" class="l3d-b" id="l3dRiv" aria-pressed="true">Rivers</button>
        <button type="button" class="l3d-b" id="l3dTown" aria-pressed="true">Towns</button>
        <label class="l3d-b l3d-r">Height <input type="range" id="l3dEx" min="5" max="40" step="1" value="15" aria-label="Height exaggeration"><output id="l3dExO">×15</output></label>
        <button type="button" class="l3d-b" id="l3dSpin" aria-pressed="false">Fly around</button>
        <button type="button" class="l3d-b" id="l3dReset">Reset view</button>
        <button type="button" class="l3d-b" id="l3dFull">Full screen</button>
      </div>
      <div class="l3d-tags" id="l3dTags" aria-hidden="true"></div>
      <div class="l3d-card" id="l3dCard" role="status" hidden></div>
      <p class="l3d-found" id="l3dFound" aria-live="polite"></p>
      <p class="l3d-load" id="l3dLoad" role="status">Loading the valley…</p>
      <p class="l3d-help">Drag to turn · scroll or pinch to zoom · tap a gold light</p>
      <noscript><img src="/map/3d/valley/relief.webp" width="4096" height="2212" alt="The St. Joseph River watershed seen from above, shaded by the shape of the land."></noscript>
    </figure>
    <h2>What you are looking at</h2>
    <ul class="dis">
      <li><b>The whole watershed.</b> The bright land is every acre whose rain ends in the St. Joseph River: parts of fifteen counties in Michigan and Indiana. The darker land around it drains elsewhere: to the Kalamazoo, the Maumee, the Kankakee, or straight to Lake Michigan.</li>
      <li><b>The shape of the ground.</b> The heights come from the U.S. Geological Survey’s 3D Elevation Program, which in this country is made mostly from laser surveys flown county by county. Here the shape of the land is drawn every 200 metres or so, and its light and shade from a grid about 50 metres apart, sharp enough to show the river’s own bluffs and old channels. The heights are raised (×15 to start) because the valley falls only about 200 metres from its eastern hills to the lake. Use the slider to flatten it or raise it further.</li>
      <li><b>What the ice left.</b> The long ridges and knobby hills are moraines, left where the glaciers stood and melted, about 15,000 years ago. The flat, open plains between them are outwash, sand and gravel spread by the meltwater. The river wanders through them both.</li>
      <li><b>The gold lights.</b> Three are the sites of lost towns from the county histories. Tap each one. Find all three and the valley is yours: there is a badge for it.</li>
    </ul>
    <p class="note">Sources: U.S. Geological Survey, 3D Elevation Program, bare-earth elevation (public domain); watershed boundary from the USGS Watershed Boundary Dataset (HUC 04050001, St. Joseph); rivers and towns from OpenStreetMap, © OpenStreetMap contributors. 3D drawing by three.js. See also <a href="/map/3d/cassopolis/">Cassopolis in LiDAR</a>, where every laser point is shown.</p>
    <script type="importmap">{{"imports":{{"three":"/vendor/three-{V}/three.module.min.js"}}}}</script>
    <script type="module">
    import * as THREE from 'three';
    import {{ OrbitControls }} from '/vendor/three-{V}/OrbitControls.min.js';
    import {{ Line2 }} from '/vendor/three-{V}/Line2.min.js';
    import {{ LineMaterial }} from '/vendor/three-{V}/LineMaterial.min.js';
    import {{ LineGeometry }} from '/vendor/three-{V}/LineGeometry.min.js';
    (async()=>{{
    const GOLD={json.dumps(GOLD)};
    const fig=document.getElementById('l3d'), cv=document.getElementById('l3dC'), load=document.getElementById('l3dLoad'), tags=document.getElementById('l3dTags'), card=document.getElementById('l3dCard'), foundEl=document.getElementById('l3dFound');
    const still=matchMedia('(prefers-reduced-motion: reduce)').matches;
    let gl; try{{ gl=new THREE.WebGLRenderer({{canvas:cv, antialias:true}}); }}catch(e){{ load.textContent='This browser cannot draw 3D.'; fig.classList.add('no3d'); return; }}
    gl.setPixelRatio(Math.min(devicePixelRatio,2)); gl.setClearColor(0x08121c,1);
    const [J,G]=await Promise.all([fetch('valley.json').then(r=>r.json()), fetch('ground.bin').then(r=>r.arrayBuffer())]).catch(()=>[null,null]);
    if (!J){{ load.textContent='The valley could not be loaded. Try again when you are online.'; return; }}
    const M=J.meta, gw=M.gw, gh=M.gh, hgt=new Uint16Array(G);
    const scene=new THREE.Scene(); scene.fog=new THREE.Fog(0x08121c,180,420);
    const cam=new THREE.PerspectiveCamera(42,1,.1,2000);
    const ctl=new OrbitControls(cam,cv); ctl.enableDamping=true; ctl.dampingFactor=.08; ctl.maxPolarAngle=Math.PI*.46; ctl.minDistance=8; ctl.maxDistance=330; ctl.autoRotateSpeed=.35;
    const home=()=>{{ cam.position.set(-40,95,120); ctl.target.set(0,0,0); ctl.update(); }}; home();
    let ex=15; const Y=(m)=>(m-150)/1000*ex;   /* metres above the lake plain, raised */
    /* height at a point, from the 1-in-4 grid */
    const hAt=(x,z)=>{{ const u=(x/M.w+.5)*(gw-1), v=(z/M.h+.5)*(gh-1); const i=Math.max(0,Math.min(gw-2,Math.floor(u))), j=Math.max(0,Math.min(gh-2,Math.floor(v))), fu=u-i, fv=v-j;
      const a=hgt[j*gw+i], b=hgt[j*gw+i+1], c=hgt[(j+1)*gw+i], d=hgt[(j+1)*gw+i+1]; return (a*(1-fu)*(1-fv)+b*fu*(1-fv)+c*(1-fu)*fv+d*fu*fv)/10+M.zmin; }};
    const geo=new THREE.PlaneGeometry(M.w,M.h,gw-1,gh-1); geo.rotateX(-Math.PI/2);
    const base=new Float32Array(gw*gh); for (let k=0;k<gw*gh;k++) base[k]=hgt[k]/10+M.zmin;
    const pos=geo.attributes.position; const setH=()=>{{ for (let k=0;k<gw*gh;k++) pos.setY(k,Y(base[k])); pos.needsUpdate=true; geo.computeVertexNormals(); }}; setH();
    const tex=new THREE.TextureLoader().load('relief.webp'); tex.colorSpace=THREE.SRGBColorSpace; tex.anisotropy=8;
    const land=new THREE.Mesh(geo,new THREE.MeshBasicMaterial({{map:tex}})); scene.add(land);
    /* the watershed edge and the rivers, in gold */
    const lines=[], lineMats=[];
    const mkLine=(pts,w,c,o)=>{{ const g=new LineGeometry(); const a=[]; pts.forEach(p=>a.push(p[0],0,p[1])); g.setPositions(a); const m=new LineMaterial({{color:c, linewidth:w, transparent:true, opacity:o, depthTest:true}}); lineMats.push(m); const l=new Line2(g,m); l.userData.pts=pts; lines.push(l); scene.add(l); return l; }};
    const lift=()=>{{ lines.forEach(l=>{{ const a=[]; l.userData.pts.forEach(p=>a.push(p[0],Y(hAt(p[0],p[1]))+.12,p[1])); l.geometry.setPositions(a); }}); }};
    mkLine(J.ring.concat([J.ring[0]]),1.6,0xe8b84a,.75);
    const rivers=[]; Object.entries(J.riv).forEach(([n,segs])=>segs.forEach(s=>rivers.push(mkLine(s,n==='St. Joseph River'?3.2:1.8,n==='St. Joseph River'?0xffd77a:0xd9a84a,.95))));
    lift();
    /* towns */
    const tagFor=(name,cls)=>{{ const el=document.createElement('span'); el.className=cls; el.textContent=name; tags.appendChild(el); return el; }};
    const towns=J.towns.map(([n,x,z])=>({{n,x,z,el:tagFor(n,'l3d-tag l3d-town')}}));
    /* the three gold lights */
    let found={{}}; try{{ found=JSON.parse(localStorage.getItem('ps-valley')||'{{}}')||{{}}; }}catch(e){{}}
    const glow=(()=>{{ const c=document.createElement('canvas'); c.width=c.height=64; const x=c.getContext('2d'); const g=x.createRadialGradient(32,32,0,32,32,32); g.addColorStop(0,'rgba(255,240,190,1)'); g.addColorStop(.25,'rgba(246,210,122,.9)'); g.addColorStop(1,'rgba(232,184,74,0)'); x.fillStyle=g; x.fillRect(0,0,64,64); const t=new THREE.CanvasTexture(c); return t; }})();
    const gold=GOLD.map(g=>{{ const s=new THREE.Sprite(new THREE.SpriteMaterial({{map:glow, transparent:true, depthWrite:false, blending:THREE.AdditiveBlending}})); s.scale.set(3.2,3.2,1); s.userData=g; scene.add(s); return s; }});
    const placeGold=()=>gold.forEach(s=>s.position.set(s.userData.x, Y(hAt(s.userData.x,s.userData.z))+1.4, s.userData.z));
    placeGold();
    const tally=()=>{{ const n=GOLD.filter(g=>found[g.id]).length; foundEl.textContent=n? n+' of 3 lost towns found'+(n===3?'. The valley is yours.':'') : ''; if (n===3 && window.psEarn) window.psEarn('valley'); }};
    tally();
    const ray=new THREE.Raycaster(), ptr=new THREE.Vector2(); let downAt=null;
    cv.addEventListener('pointerdown',e=>{{ downAt=[e.clientX,e.clientY]; }});
    cv.addEventListener('pointerup',e=>{{ if (!downAt || Math.hypot(e.clientX-downAt[0],e.clientY-downAt[1])>6) return; const r=cv.getBoundingClientRect(); ptr.set((e.clientX-r.left)/r.width*2-1, -(e.clientY-r.top)/r.height*2+1); ray.setFromCamera(ptr,cam);
      let best=null, bd=1e9; gold.forEach(s=>{{ const p=s.position.clone().project(cam); const d=Math.hypot(p.x-ptr.x,p.y-ptr.y); if (d<bd){{ bd=d; best=s; }} }});
      if (best && bd<.06){{ const g=best.userData; found[g.id]=1; try{{ localStorage.setItem('ps-valley',JSON.stringify(found)); }}catch(e){{}}
        card.innerHTML=''; const h=document.createElement('b'); h.textContent=g.name; const p=document.createElement('span'); p.textContent=' '+g.line+' '; const a=document.createElement('a'); a.href='/lost-towns/#'+g.id; a.textContent='Read about it →'; card.append(h,p,a); card.hidden=false; tally(); }}
      else card.hidden=true; }});
    const size=()=>{{ const w=cv.clientWidth, h=cv.clientHeight; gl.setSize(w,h,false); cam.aspect=w/h; cam.updateProjectionMatrix(); lineMats.forEach(m=>m.resolution.set(w,h)); }};
    new ResizeObserver(size).observe(cv); size();
    const B=(id,f)=>{{ const b=document.getElementById(id); b.addEventListener('click',()=>f(b)); return b; }};
    const press=(b,on)=>b.setAttribute('aria-pressed',String(on));
    let showTowns=true;
    B('l3dRiv',b=>{{ const on=!rivers[0].visible; rivers.forEach(l=>l.visible=on); press(b,on); }});
    B('l3dTown',b=>{{ showTowns=!showTowns; press(b,showTowns); }});
    const exI=document.getElementById('l3dEx'), exO=document.getElementById('l3dExO');
    exI.addEventListener('input',()=>{{ ex=+exI.value; exO.textContent='×'+ex; setH(); lift(); placeGold(); }});
    const spin=B('l3dSpin',b=>{{ ctl.autoRotate=!ctl.autoRotate; press(b,ctl.autoRotate); }});
    B('l3dReset',()=>home());
    B('l3dFull',()=>{{ if (document.fullscreenElement) document.exitFullscreen(); else if (fig.requestFullscreen) fig.requestFullscreen().catch(()=>{{}}); }});
    if (!still){{ ctl.autoRotate=true; press(spin,true); ctl.addEventListener('start',()=>{{ ctl.autoRotate=false; press(spin,false); }}, {{once:true}}); }}
    load.hidden=true; fig.classList.add('ready');
    let vis=true; new IntersectionObserver(es=>{{ vis=es[0].isIntersecting; }}).observe(fig);
    const tmp=new THREE.Vector3(); let t0=performance.now();
    gl.setAnimationLoop(t=>{{ if (!vis) return; ctl.update();
      const pulse=still?1:1+.18*Math.sin(t/420); gold.forEach((s,i)=>{{ const k=found[s.userData.id]?.75:1; s.scale.setScalar(3.2*k*pulse); s.material.opacity=found[s.userData.id]?.55:1; }});
      gl.render(scene,cam);
      const w=cv.clientWidth, h=cv.clientHeight, dist=cam.position.length();
      towns.forEach(o=>{{ tmp.set(o.x, Y(hAt(o.x,o.z))+.6, o.z); tmp.project(cam); const on=showTowns && tmp.z<1 && Math.abs(tmp.x)<1.05 && Math.abs(tmp.y)<1.05; o.el.style.opacity=on?1:0; o.el.style.transform=`translate(${{(tmp.x*.5+.5)*w}}px,${{(-tmp.y*.5+.5)*h}}px)`; }});
    }});
    }})();
    </script>
'''
page('map/3d/valley/index.html', 'The St. Joseph River Valley in 3D · Project Scroll',
     'The whole St. Joseph River watershed in 3D, from Hillsdale to Lake Michigan, built from U.S. Geological Survey elevation data, with the river and its branches in gold and three lost towns to find.',
     body, og='https://projectscroll.com/og/records.jpg')
print('3d valley built')
