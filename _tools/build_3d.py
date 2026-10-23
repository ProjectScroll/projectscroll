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
_W = json.load(open(R / '_tools/data/walk.json'))['stops']
PINS = [dict(n=s['name'], la=s['lat'], lo=s['lon'], b=s['built'], t=(s['then'].split('. ')[0].rstrip('.') + '.'), u='/walk/#' + s['id'], l='Read this stop on the walking tour') for s in _W if s['id'] != 'log-cabin']
PINS.append(dict(n='Forest Hall and the island', la=41.9039, lo=-85.9769, b='summers of the 1890s on', t='Grand Island and its resort hotel drew summer people to Diamond Lake for generations.', u='/news/summer-on-diamond-lake/', l='Read the story'))
SPOTS = [('The Cass County Courthouse', 41.91202, -86.01243, 26), ('Stone Lake', 41.9042, -86.0175, 12), ('Diamond Lake', 41.8980, -85.9890, 12), ('Grand Island', 41.9039, -85.9769, 18)]

body = f'''    <p class="crumb"><a href="/map/">← The map room</a></p>
    <p class="kicker">Cassopolis in LiDAR</p>
    <h1>The county seat, laser by laser</h1>
    <p class="lede" style="font-size:1.15rem">In 2015 an aircraft flew over Cass County firing laser pulses at the ground, hundreds of thousands a second, and timing each echo. Every dot below is one of those echoes: {M['n']:,} of them in the blocks around the courthouse, every one the survey kept, and {M['wn']:,} more across the country around. Around them lies the land the same survey measured, from Stone Lake to Diamond Lake, about six kilometres across. Turn it, tilt it, and lay the 1860 town plan over the real ground.</p>
    <figure class="l3d" id="l3d" aria-label="A three-dimensional model of Cassopolis, Stone Lake and Diamond Lake built from laser survey data">
      <canvas id="l3dC" aria-hidden="true"></canvas>
      <div class="l3d-ui" role="toolbar" aria-label="Model controls">
        <button type="button" class="l3d-b" id="l3dPlan" aria-pressed="false">1860 plan</button>
        <button type="button" class="l3d-b" id="l3dBld" aria-pressed="true">Buildings</button>
        <button type="button" class="l3d-b" id="l3dTrees" aria-pressed="true">Trees</button>
        <button type="button" class="l3d-b" id="l3dMore" hidden>Whole area</button>
        <button type="button" class="l3d-b" id="l3dTall" aria-pressed="false">Height ×3</button>
        <button type="button" class="l3d-b" id="l3dSpin" aria-pressed="false">Fly around</button>
        <button type="button" class="l3d-b" id="l3dPins" aria-pressed="true">Story pins</button>
        <button type="button" class="l3d-b" id="l3dTour" aria-pressed="false">Guided tour</button>
        <label class="l3d-b l3d-r">Sun <input type="range" id="l3dSun" min="0" max="100" step="1" value="30" aria-label="Time of day for the sun and shadows"><output id="l3dSunO">off</output></label>
        <button type="button" class="l3d-b" id="l3dReset">Reset view</button>
        <button type="button" class="l3d-b" id="l3dFull">Full screen</button>
      </div>
      <div class="l3d-tags" id="l3dTags" aria-hidden="true"></div>
      <div class="l3d-pins" id="l3dPinBox"></div>
      <div class="l3d-card" id="l3dCard" role="status" hidden></div>
      <p class="l3d-load" id="l3dLoad" role="status">Loading the survey…</p>
      <p class="l3d-help">Drag to turn · scroll or pinch to zoom · right-drag or two fingers to move · tap the ground for a reading</p>
      <noscript><img src="/img/l3d-cassopolis.webp" width="1058" height="898" alt="Central Cassopolis from above, built from laser survey points: buildings in gold, trees in green, on the bare ground."></noscript>
    </figure>
    <ul class="l3d-key" aria-label="What the colours mean">
      <li><i style="background:#e8b84a"></i>Buildings, {M['nb']+M['wnb']:,} points</li>
      <li><i style="background:#3fb38a"></i>Trees, {M['nv']+M['wnv']:,} points</li>
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
      <li><b>Story pins.</b> The gold pins are the stops of our <a href="/walk/">walking tour of Cassopolis</a>, from the site of the first courthouse to the bank corner, and the island in Diamond Lake. Press one for a line of its history.</li>
      <li><b>Guided tour.</b> Press <i>Guided tour</i> and the view flies itself from Stone Lake to the courthouse square and out to Diamond Lake. Touch the model to stop it.</li>
      <li><b>Sun and shadows.</b> Move the <i>Sun</i> slider through a midsummer day, from six in the morning to eight at night, and every roof and tree in the town blocks casts its shadow on the ground. The shadows are worked out from the laser points themselves.</li>
      <li><b>Tap for a reading.</b> Tap or click the bare ground anywhere, and the model tells you how high it stands above sea level and how far it is from the courthouse.</li>
      <li><b>Buildings and Trees.</b> Each button hides or shows its points, so you can see the bare land under the town, or the trees alone.</li>
      <li><b>Height ×3.</b> The town is fairly level, so tripling the heights makes the rise of the land easier to see. The buildings stretch too.</li>
    </ul>
    <aside class="l3d-svc" aria-label="A service we offer"><p><b>Your own place in 3D.</b> Project Scroll makes LiDAR models like this one for other places: a farm, a lake, a town, an old mill site, a family’s home ground, from the same public surveys, with fly-throughs and still pictures to keep. <a href="/services/#studio">See the studio</a>, or write to research@projectscroll.com.</p></aside>
    <p class="note">Source: U.S. Geological Survey, 3D Elevation Program, Michigan Cass County LiDAR, 2015 (public domain), read from the survey’s public point-cloud archive. In the town blocks every building and tree point is shown. Across the wider country the page shows the survey’s lighter sampling, about one point in ten, so that it stays quick to load (on a phone, press <i>Whole area</i> to load it); press <i>Buildings</i> or <i>Trees</i> to hide either. The points cover the blocks north and east of the courthouse; the ground around them is the survey’s bare-earth elevation from the 3D Elevation Program, shaped every six metres or so and shaded from a grid about one and a half metres apart. Town plan: <i>Map of the Counties of Cass, Van Buren and Berrien, Michigan</i> (Geil, Harley &amp; Siverd, 1860), Library of Congress. 3D drawing by three.js.</p>
    <script type="importmap">{{"imports":{{"three":"/vendor/three-{V}/three.module.min.js"}}}}</script>
    <script type="module">
    import * as THREE from 'three';
    import {{ OrbitControls }} from '/vendor/three-{V}/OrbitControls.min.js';
    (async()=>{{
    const M={json.dumps(M)}, PLAN={json.dumps(PLAN)}, SPOTS={json.dumps(SPOTS)}, PINS={json.dumps(PINS)};
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
    const gu={{uPlan:{{value:0}}, uTex:{{value:planTex}}, uBox:{{value:new THREE.Vector4(M.west,M.east,M.south,M.north)}}, uPB:{{value:new THREE.Vector4(PLAN.W,PLAN.E,PLAN.S,PLAN.N)}}, uSize:{{value:new THREE.Vector2(M.w,M.h)}}, uHD:{{value:hdTex}}, uWB:{{value:new THREE.Vector4(M.wwest,M.weast,M.wsouth,M.wnorth)}}, uSunOn:{{value:0}}, uSun:{{value:new THREE.Vector3(-.5,1,.35).normalize()}}, uShadow:{{value:null}}, uSM:{{value:new THREE.Matrix4()}}}};
    const gmat=new THREE.ShaderMaterial({{uniforms:gu, vertexShader:`varying vec3 vN; varying vec3 vP; varying vec3 vW; void main(){{ vN=normal; vP=position; vW=(modelMatrix*vec4(position,1.)).xyz; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }}`,
      fragmentShader:`uniform float uPlan, uSunOn; uniform sampler2D uTex, uHD, uShadow; uniform vec4 uBox, uPB, uWB; uniform vec2 uSize; uniform vec3 uSun; uniform mat4 uSM; varying vec3 vN; varying vec3 vP; varying vec3 vW;
      void main(){{ float sh=clamp(dot(normalize(vN),normalize(vec3(-.5,1.,.35))),0.,1.); vec3 c=mix(vec3(.003,.01,.02),vec3(.025,.075,.12),sh);
        float h=vP.y*.5; float fw=max(fwidth(h),1e-4); float l=(1.-smoothstep(0.,1.,abs(fract(h-.5)-.5)/fw))*(1.-smoothstep(.15,.45,fw)); c=mix(c,vec3(.08,.42,.48),l*.35);
        float lon=uBox.x+(vP.x/uSize.x+.5)*(uBox.y-uBox.x), lat=uBox.z+(-vP.z/uSize.y+.5)*(uBox.w-uBox.z);
        vec2 uv=vec2((lon-uPB.x)/(uPB.y-uPB.x),(lat-uPB.z)/(uPB.w-uPB.z));
        vec2 hw=vec2((lon-uWB.x)/(uWB.y-uWB.x),(lat-uWB.z)/(uWB.w-uWB.z)); if (hw.x>=0. && hw.x<=1. && hw.y>=0. && hw.y<=1.) c=texture2D(uHD,hw).rgb*(.88+.24*sh);
        if (uPlan>0. && uv.x>=0. && uv.x<=1. && uv.y>=0. && uv.y<=1.){{ vec3 pc=texture2D(uTex,uv).rgb; c=mix(c,pc*mix(.75,1.05,sh),uPlan*.92); }}
        if (uSunOn>0.){{ float ls=clamp(dot(normalize(vN),uSun),0.,1.); float lit=.55+.6*ls*smoothstep(0.,.25,uSun.y); vec4 sc=uSM*vec4(vW,1.); vec3 q=sc.xyz/sc.w*.5+.5;
          if (q.x>0. && q.x<1. && q.y>0. && q.y<1. && q.z<1.){{ float dd=texture2D(uShadow,q.xy).r; if (q.z-.0008>dd) lit*=.5; }}
          c*=mix(1.,lit,uSunOn); }}
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
    const pu={{uTrees:{{value:1}}, uBld:{{value:1}}, uPx:{{value:gl.getPixelRatio()}}, uTime:{{value:0}}, uLight:{{value:1}}}};
    const pmat=new THREE.ShaderMaterial({{uniforms:pu, transparent:true, depthWrite:true,
      vertexShader:`attribute float kind; attribute vec3 color; uniform float uTrees, uBld, uPx, uTime; varying vec3 vC; varying float vK;
        void main(){{ vC=color; vK=kind; vec4 mv=modelViewMatrix*vec4(position,1.); gl_Position=projectionMatrix*mv;
          float s=(kind<1.5?1.9:1.6)*uPx*260./-mv.z; gl_PointSize=clamp(s,1.,7.); if ((kind>1.5 && uTrees<.5) || (kind<1.5 && uBld<.5)){{ gl_PointSize=0.; gl_Position=vec4(2.,2.,2.,1.); }} }}`,
      fragmentShader:`uniform float uLight; varying vec3 vC; varying float vK; void main(){{ vec2 d=gl_PointCoord-.5; float r=dot(d,d); if (r>.25) discard; float glow=vK<1.5?1.15:1.; gl_FragColor=vec4(vC*glow*uLight*(1.-r*1.2),1.);
#include <colorspace_fragment>
}}`}});
    world.add(new THREE.Points(pg,pmat));
    /* the shadow pass: the same points, seen from the sun, write only their depth */
    const shScene=new THREE.Scene(), shSize=innerWidth<700?1024:2048, shR=900;
    const shRT=new THREE.WebGLRenderTarget(shSize,shSize); shRT.depthTexture=new THREE.DepthTexture(shSize,shSize); gu.uShadow.value=shRT.depthTexture;
    const sunCam=new THREE.OrthographicCamera(-shR,shR,shR,-shR,10,9000);
    const dmat=new THREE.ShaderMaterial({{uniforms:{{uTrees:pu.uTrees, uBld:pu.uBld, uPs:{{value:2.4*shSize/(2*shR)}}}},
      vertexShader:`attribute float kind; uniform float uTrees, uBld, uPs; void main(){{ gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); gl_PointSize=max(2.,uPs); if ((kind>1.5 && uTrees<.5) || (kind<1.5 && uBld<.5)){{ gl_PointSize=0.; gl_Position=vec4(2.,2.,2.,1.); }} }}`,
      fragmentShader:`void main(){{ gl_FragColor=vec4(1.); }}`}});
    const shWorld=new THREE.Group(); shScene.add(shWorld); shWorld.add(new THREE.Points(pg,dmat));
    /* a soft gold ring marks the courthouse */
    const spots=SPOTS.map(([name,la,lo,hy])=>{{ const [x,z]=ll2xz(la,lo); const el=document.createElement('span'); el.className='l3d-tag'; el.textContent=name; tags.appendChild(el); return {{v:new THREE.Vector3(x,hy,z), el}}; }});
    const size=()=>{{ const w=cv.clientWidth, h=cv.clientHeight; gl.setSize(w,h,false); cam.aspect=w/h; cam.updateProjectionMatrix(); }};
    new ResizeObserver(size).observe(cv); size(); home();
    let tall=1, tallTo=1, plan=0, planTo=0;
    const B=(id,f)=>{{ const b=document.getElementById(id); b.addEventListener('click',()=>f(b)); return b; }};
    const press=(b,on)=>b.setAttribute('aria-pressed',String(on));
    B('l3dPlan',b=>{{ planTo=planTo?0:1; press(b,!!planTo); }});
    B('l3dTrees',b=>{{ pu.uTrees.value=pu.uTrees.value?0:1; press(b,!!pu.uTrees.value); }});
    B('l3dBld',b=>{{ pu.uBld.value=pu.uBld.value?0:1; press(b,!!pu.uBld.value); }});
    B('l3dTall',b=>{{ tallTo=tallTo===1?3:1; press(b,tallTo===3); }});
    const spin=B('l3dSpin',b=>{{ ctl.autoRotate=!ctl.autoRotate; press(b,ctl.autoRotate); }});
    B('l3dReset',()=>home());
    B('l3dFull',()=>{{ if (document.fullscreenElement) document.exitFullscreen(); else if (fig.requestFullscreen) fig.requestFullscreen().catch(()=>{{}}); }});
    if (!still){{ ctl.autoRotate=true; press(spin,true); ctl.addEventListener('start',()=>{{ ctl.autoRotate=false; press(spin,false); }}, {{once:true}}); }}
    /* the card */
    const card=document.getElementById('l3dCard');
    const show=(h,parts)=>{{ card.innerHTML=''; const b=document.createElement('b'); b.textContent=h; card.append(b); parts.forEach(p=>card.append(p)); const x=document.createElement('button'); x.type='button'; x.className='l3d-x'; x.setAttribute('aria-label','Close'); x.textContent='×'; x.addEventListener('click',()=>{{ card.hidden=true; }}); card.append(x); card.hidden=false; }};
    const span=s=>{{ const e=document.createElement('span'); e.textContent=s; return e; }};
    /* story pins: buttons that ride on the model */
    const pinBox=document.getElementById('l3dPinBox'); let pinsOn=true;
    const pins=PINS.map(q=>{{ const [x,z]=ll2xz(q.la,q.lo); const e=document.createElement('button'); e.type='button'; e.className='l3d-pin'; e.setAttribute('aria-label',q.n); e.title=q.n;
      e.addEventListener('click',()=>{{ const a=document.createElement('a'); a.href=q.u; a.textContent=q.l+' ›'; show(q.n,[span(' '+q.b+'. '+q.t+' '),a]); }}); pinBox.append(e); return {{v:new THREE.Vector3(x,0,z), e, q}}; }});
    const gH=(x,z)=>{{ ray.set(new THREE.Vector3(x,600,z),new THREE.Vector3(0,-1,0)); const inTown=Math.abs(x)<M.w/2&&Math.abs(z)<M.h/2; const hit=ray.intersectObjects(inTown?[ground]:grounds,false)[0]; return hit?hit.point.y/world.scale.y:0; }};
    const ray=new THREE.Raycaster(), grounds=world.children.filter(o=>o.isMesh);
    pins.forEach(p=>{{ p.v.y=gH(p.v.x,p.v.z)+6; }});
    B('l3dPins',b=>{{ pinsOn=!pinsOn; press(b,pinsOn); pinBox.hidden=!pinsOn; }});
    /* tap the ground for a reading */
    const ptr=new THREE.Vector2(); let downAt=null; const ch=ll2xz(SPOTS[0][1],SPOTS[0][2]);
    cv.addEventListener('pointerdown',e=>{{ downAt=[e.clientX,e.clientY]; }});
    cv.addEventListener('pointerup',e=>{{ if (!downAt || Math.hypot(e.clientX-downAt[0],e.clientY-downAt[1])>6) return; const r=cv.getBoundingClientRect(); ptr.set((e.clientX-r.left)/r.width*2-1, -(e.clientY-r.top)/r.height*2+1); ray.setFromCamera(ptr,cam);
      const hit=ray.intersectObjects(grounds,false)[0]; if (!hit) return; const y=hit.point.y/world.scale.y, el=y+M.z0, dx=hit.point.x-ch[0], dz=hit.point.z-ch[1], d=Math.hypot(dx,dz);
      const dirs=['north','north-east','east','south-east','south','south-west','west','north-west'], dir=dirs[Math.round(((Math.atan2(dx,-dz)*180/Math.PI)+360)%360/45)%8];
      show('The ground here',[span(' '+el.toFixed(1)+' metres ('+Math.round(el*3.2808).toLocaleString('en-US')+' feet) above sea level. '+(d<40?'You are at the courthouse.':(d<1000?Math.round(d)+' metres':(d/1000).toFixed(2)+' km')+' '+dir+' of the courthouse.'))]); }});
    /* the sun: a midsummer day at Cassopolis, six in the morning to eight at night */
    const sunI=document.getElementById('l3dSun'), sunO=document.getElementById('l3dSunO'); let shDirty=false, sunOn=false;
    const setSun=()=>{{ const f=+sunI.value/100, hr=6+f*14, h=(hr-13.6)*Math.PI/12; const lat=41.91*Math.PI/180, dec=23.4*Math.PI/180;
      const el=Math.asin(Math.sin(lat)*Math.sin(dec)+Math.cos(lat)*Math.cos(dec)*Math.cos(h)), az=Math.atan2(Math.sin(h),Math.cos(h)*Math.sin(lat)-Math.tan(dec)*Math.cos(lat))+Math.PI;
      const s=new THREE.Vector3(Math.sin(az)*Math.cos(el), Math.sin(el), -Math.cos(az)*Math.cos(el)).normalize(); gu.uSun.value.copy(s); gu.uSunOn.value=1; sunOn=true;
      pu.uLight.value=.45+.55*Math.max(0,Math.min(1,s.y*2.5)); const hh=Math.floor(hr), mm=Math.round((hr-hh)*60/15)*15%60; sunO.textContent=((hh+11)%12+1)+':'+String(mm).padStart(2,'0')+(hh<12?' am':' pm'); shDirty=true; }};
    sunI.addEventListener('input',setSun);
    const shadowPass=()=>{{ const s=gu.uSun.value; if (s.y<.03){{ gl.setRenderTarget(shRT); gl.clear(); gl.setRenderTarget(null); }} else {{
      shWorld.scale.y=world.scale.y; sunCam.position.set(s.x*4000, s.y*4000, s.z*4000); sunCam.up.set(0,0,-1); sunCam.lookAt(0,0,0); sunCam.updateMatrixWorld(); sunCam.updateProjectionMatrix();
      gl.setRenderTarget(shRT); gl.clear(); gl.render(shScene,sunCam); gl.setRenderTarget(null); }}
      gu.uSM.value.multiplyMatrices(sunCam.projectionMatrix,sunCam.matrixWorldInverse); shDirty=false; }};
    /* the guided tour */
    const tourB=document.getElementById('l3dTour'); let tour=null;
    const at=(la,lo)=>{{ const [x,z]=ll2xz(la,lo); return new THREE.Vector3(x,0,z); }};
    const STOPS=[
      [at(41.9005,-85.998), [-2400,1900,2300], 'The county seat between two lakes: Stone Lake to the west, Diamond Lake to the east, and the town on the higher ground between.'],
      [at(41.9048,-86.0175), [-520,360,620], 'Stone Lake, at the foot of the town, a few minutes’ walk west of the courthouse.'],
      [at(41.91165,-86.01255), [-170,150,230], 'The public square of the 1831 plat, where Broadway crosses State Street. The stone courthouse, finished in 1900, stands on it.'],
      [at(41.9135,-86.0110), [260,220,330], 'The town blocks: every gold dot is a laser echo from a roof, every green one an echo from a tree.'],
      [at(41.9015,-85.9800), [-900,700,1000], 'Diamond Lake, a little over a mile east of the courthouse, with Grand Island in the middle.'],
    ];
    const ease=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;
    const stopTour=()=>{{ if (!tour) return; tour=null; press(tourB,false); }};
    const goStop=i=>{{ if (i>=STOPS.length){{ stopTour(); home(); return; }} const [tg,off,cap]=STOPS[i]; const k=Math.max(1,1.2/Math.max(.3,cam.aspect));
      tour={{i, t0:performance.now(), dur:still?1:5200, fp:cam.position.clone(), ft:ctl.target.clone(), tp:new THREE.Vector3(tg.x+off[0]*k,off[1]*k,tg.z+off[2]*k), tt:tg.clone()}}; show('Guided tour, '+(i+1)+' of '+STOPS.length,[span(' '+cap)]); }};
    tourB.addEventListener('click',()=>{{ if (tour){{ stopTour(); return; }} ctl.autoRotate=false; press(spin,false); press(tourB,true); goStop(0); }});
    cv.addEventListener('pointerdown',stopTour); cv.addEventListener('wheel',stopTour,{{passive:true}});
    load.hidden=true; fig.classList.add('ready');
    /* the wider country: x and z in decimetres from the north-west corner, height in decimetres, then the class and a height shade */
    const more=document.getElementById('l3dMore'); let wideOn=false;
    const loadWide=()=>{{ if (wideOn) return; wideOn=true; more.hidden=true; fetch('wide-pts.bin').then(r=>r.ok?r.arrayBuffer():null).then(w=>{{ if (!w) return; const dw=new DataView(w), m=w.byteLength/8|0, [x0,z0]=ll2xz(M.wnorth,M.wwest);
      const Q=new Float32Array(m*3), QC=new Float32Array(m*3), QK=new Float32Array(m);
      for (let i=0;i<m;i++){{ const o=i*8, k=dw.getUint8(o+6), s=dw.getUint8(o+7)/255, a=k===1?gold:leaf, t=Math.min(1,s*1.6); Q[i*3]=x0+dw.getUint16(o,true)/10; Q[i*3+1]=dw.getInt16(o+4,true)/10; Q[i*3+2]=z0+dw.getUint16(o+2,true)/10; QK[i]=k;
        QC[i*3]=a[0].r+(a[1].r-a[0].r)*t; QC[i*3+1]=a[0].g+(a[1].g-a[0].g)*t; QC[i*3+2]=a[0].b+(a[1].b-a[0].b)*t; }}
      const qg=new THREE.BufferGeometry(); qg.setAttribute('position',new THREE.BufferAttribute(Q,3)); qg.setAttribute('color',new THREE.BufferAttribute(QC,3)); qg.setAttribute('kind',new THREE.BufferAttribute(QK,1)); world.add(new THREE.Points(qg,pmat)); shWorld.add(new THREE.Points(qg,dmat)); shDirty=true; }}).catch(()=>{{}}); }};
    /* on a big screen the whole area loads at once; on a phone, when asked */
    more.addEventListener('click',loadWide); if (innerWidth>=700 && (navigator.deviceMemory||8)>=4) loadWide(); else more.hidden=false;
    let vis=true; new IntersectionObserver(es=>{{ vis=es[0].isIntersecting; }}).observe(fig);
    const tmp=new THREE.Vector3();
    gl.setAnimationLoop(()=>{{ if (!vis) return;
      const t0=tall; tall+=(tallTo-tall)*(still?1:.12); plan+=(planTo-plan)*(still?1:.15); world.scale.y=tall; gu.uPlan.value=plan; if (Math.abs(t0-tall)>1e-4) shDirty=true;
      if (tour){{ const f=Math.min(1,(performance.now()-tour.t0)/tour.dur), e=ease(f); cam.position.lerpVectors(tour.fp,tour.tp,e); ctl.target.lerpVectors(tour.ft,tour.tt,e); if (f>=1 && performance.now()-tour.t0>tour.dur+(still?6000:3500)) goStop(tour.i+1); }}
      if (sunOn && shDirty) shadowPass();
      ctl.update(); gl.render(scene,cam);
      const w=cv.clientWidth, h=cv.clientHeight, dcam=cam.position.distanceTo(ctl.target);
      if (pinsOn) pins.forEach(p=>{{ tmp.copy(p.v); tmp.y*=tall; tmp.project(cam); const on=tmp.z<1&&Math.abs(tmp.x)<1.02&&Math.abs(tmp.y)<1.02&&dcam<2600; p.e.style.visibility=on?'visible':'hidden'; p.e.style.transform=`translate(${{(tmp.x*.5+.5)*w}}px,${{(-tmp.y*.5+.5)*h}}px)`; }});
      spots.forEach(s=>{{ tmp.copy(s.v); tmp.y*=tall; tmp.project(cam); const on=tmp.z<1; s.el.style.opacity=on&&Math.abs(tmp.x)<1.05&&Math.abs(tmp.y)<1.05?1:0; s.el.style.transform=`translate(${{(tmp.x*.5+.5)*w}}px,${{(-tmp.y*.5+.5)*h}}px)`; }});
    }});
    }})();
    </script>
'''
page('map/3d/cassopolis/index.html', 'Cassopolis in LiDAR · Project Scroll',
     f'Cassopolis, Stone Lake and Diamond Lake in 3D, from the 2015 Cass County LiDAR flight: {M["n"]+M["wn"]:,} laser points, buildings in gold, trees in green, each switchable, and the 1860 town plan laid on the ground.',
     body, og='https://projectscroll.com/og/records.jpg')
print('3d cassopolis built', M['n'])

# ---------------- the St. Joseph River Valley in 3D ----------------
VJ = json.load(open(R / 'map/3d/valley/valley.json'))
VM = VJ['meta']
GOLD = [  # three lost towns, from the lost towns page; finding all three earns a badge
  dict(id='adamsport', name='Adamsport and Christiana', line='Two mill plats faced each other across Christiana Creek, and grew together as Adamsville.', lat=41.7853, lon=-85.9939),
  dict(id='wakelee', name='Wakelee', line='A lumber station on the new railroad, laid out in 1871. When the timber was cut, the reason for it went too.', lat=41.98389, lon=-85.87889),
  dict(id='waterford', name='Waterford', line='A mill town on the Elkhart River. In 1868 the dam came down and the mill moved to Goshen.', lat=41.54306, lon=-85.83056),
  dict(id='williamsville', name='Williamsville', line='Laid out by Josiah Williams in 1848, in Porter Township. A post office and a few houses, then the trade went elsewhere.', lat=41.8667, lon=-85.8642),
  dict(id='kessington', name='Kessington', line='Nineteen lots on the old Chicago road, platted in 1872: a store, a blacksmith, a church and a school.', lat=41.7767, lon=-85.8969),
  dict(id='venice', name='Venice (about here)', line='A paper town of 1836: 538 lots, two squares, and not one house built. Dowagiac grew over the ground; the exact plat is not known.', lat=41.991, lon=-86.098),
  dict(id='new-coloma', name='New Coloma (about here)', line='Lots laid out by the new railroad station in 1869. The stores closed for want of trade; the ground is inside Coloma today.', lat=42.1889, lon=-86.3111),
  dict(id='dennison', name='Denniston, then Lowell (about here)', line='Laid out in 1837 on the east bank opposite South Bend, for its water power. Vacated, then Lowell, then a ward of the city.', lat=41.680, lon=-86.244),
  dict(id='mount-pleasant', name='Mount Pleasant (about here)', line='Platted on Portage Prairie and vacated by the legislature in 1850. A church and a school marked the spot long after.', lat=41.703, lon=-86.332),
  dict(id='st-joseph', name='St. Joseph, Indiana (about here)', line='The first seat of St. Joseph County, laid out in 1830 at the portage. The seat moved to South Bend the next spring.', lat=41.717, lon=-86.277),
]
NG = len(GOLD)
_ND = json.load(open(R / '_tools/data/news.json'))
_N = {s['slug']: s for s in (_ND['stories'] + [_ND.get('lead') or {}]) if isinstance(s, dict) and s.get('slug')}
def _town(n):
    for tn, x, z in VJ['towns']:
        if tn == n: return round(VM['lat0'] - z / VM['kz'], 5), round(VM['lon0'] + x / VM['kx'], 5)
    raise KeyError(n)
_PIN = [  # stories pinned where they happened: (place, lat/lon or town, [slugs])
  ('Cassopolis', _town('Cassopolis'), ['how-cassopolis-got-its-name', 'e-clampus-vitus-in-cassopolis-1846', 'the-hotel-that-walked', 'the-courthouse-that-became-the-colonial', 'dr-goodwins-hotel', 'race-day-at-the-cassopolis-fair', 'who-was-in-town-in-1860', 'cassopolis-in-lidar']),
  ('Dewey Lake', (42.0554, -86.1853), ['the-week-dewey-lake-went-wild']),
  ('Dowagiac', _town('Dowagiac'), ['how-dowagiac-got-its-name', 'the-roosevelt-special-at-dowagiac', 'company-d-sixth-michigan']),
  ('Vandalia', (41.9181, -85.9161), ['the-kentucky-raid-of-1847', 'how-vandalia-got-its-name']),
  ('Diamond Lake', (41.9015, -85.9800), ['summer-on-diamond-lake']),
  ('Niles', _town('Niles'), ['how-niles-got-its-name']),
  ('Edwardsburg', _town('Edwardsburg'), ['how-edwardsburg-got-its-name', 'edwardsburg-in-1910', 'band-night-at-eagle-lake']),
  ('Paw Paw', _town('Paw Paw'), ['how-paw-paw-got-its-name']),
  ('Kalamazoo', (42.2917, -85.5872), ['how-kalamazoo-got-its-name']),
  ('South Bend', _town('South Bend'), ['the-oliver-hotel-south-bend']),
  ('Mishawaka', _town('Mishawaka'), ['mishawaka-city-hall-and-mayor-herzog', 'springbrook-park-the-trolley-park']),
]
PINV = []
for name, (la, lo), slugs in _PIN:
    st = [[_N[s]['headline'], '/news/' + s + '/'] for s in slugs if s in _N]
    if st: PINV.append(dict(n=name, x=round((lo - VM['lon0']) * VM['kx'], 3), z=round(-(la - VM['lat0']) * VM['kz'], 3), s=st))
GEO = [  # what the ice left, placed from Michigan State University's Geography of Michigan and Wikipedia
  ('Kalamazoo moraine', 41.965, -85.985), ('Sturgis moraine', 41.80, -85.42), ('Valparaiso moraine', 42.02, -86.44),
  ('Kankakee outwash plain', 41.625, -86.33), ('Outwash plain', 41.70, -86.02)]
GEO = [dict(n=n, x=round((lo - VM['lon0']) * VM['kx'], 3), z=round(-(la - VM['lat0']) * VM['kz'], 3)) for n, la, lo in GEO]
CASS = [dict(x=x, z=z) for n, x, z in VJ['towns'] if n == 'Cassopolis'][0]
# the river's fall, from source to lake, drawn as a profile under the model
PR = json.load(open(R / 'map/3d/valley/profile.json'))
def _profile():
    W, H, L, T, B = 760, 320, 54, 46, 46
    d, h = PR['d'], PR['h']; D = d[-1]; lo, hi = 170, 340
    X = lambda v: L + (W - L - 40) * v / D; Y = lambda v: T + (H - T - B) * (hi - v) / (hi - lo); RX = W - 30
    pts = ' '.join(f'{X(a):.1f},{Y(b):.1f}' for a, b in zip(d, h))
    area = f'M{X(0):.1f},{Y(lo):.1f} L' + pts.replace(' ', ' L') + f' L{X(D):.1f},{Y(lo):.1f} Z'
    g = ''.join(f'<line x1="{L}" x2="{W-14}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" class="rp-g"/><text x="{L-6}" y="{Y(v)+4:.1f}" text-anchor="end" class="rp-t">{v} m</text>' for v in range(180, 341, 40))
    km = ''.join(f'<text x="{X(v):.1f}" y="{H-B+16}" text-anchor="middle" class="rp-t">{v} km</text>' for v in range(0, int(D) + 1, 50))
    tw = ''
    show = ['Hillsdale', 'Union City', 'Colon', 'Three Rivers', 'Constantine', 'Elkhart', 'South Bend', 'Niles', 'Berrien Springs', 'St. Joseph']
    for i, n in enumerate(show):
        if n not in PR['towns']: continue
        dd, hh, _ = PR['towns'][n]; lift = {'Hillsdale':14,'Union City':28,'Colon':14,'Three Rivers':14,'Constantine':42,'Elkhart':28,'South Bend':14,'Niles':42,'Berrien Springs':28,'St. Joseph':14}[n]; anc = 'start' if i == 0 else ('end' if n == 'St. Joseph' else 'middle')
        tw += f'<g class="rp-town"><circle cx="{X(dd):.1f}" cy="{Y(hh):.1f}" r="3.2"/><line x1="{X(dd):.1f}" x2="{X(dd):.1f}" y1="{Y(hh)-4:.1f}" y2="{Y(hh)-lift:.1f}"/><text x="{X(dd):.1f}" y="{Y(hh)-lift-4:.1f}" text-anchor="{anc}">{n}</text></g>'
    # the dams on the main stem today (OpenStreetMap), placed along the profile between the towns they stand by
    DAMS = [('Sturgis', 121.7), ('Three Rivers', 132.6), ('Constantine', 146.6), ('Mottville', 157.7), ('Elkhart', 186.9), ('Twin Branch', 205.6), ('French Paper, Niles', 236.0), ('Buchanan', 247.8), ('Berrien Springs', 265.7)]
    def _h(x):
        for (a0, b0), (a1, b1) in zip(zip(d, h), zip(d[1:], h[1:])):
            if a0 <= x <= a1: return b0 + (b1 - b0) * (x - a0) / ((a1 - a0) or 1)
        return h[-1]
    tw += ''.join(f'<g class="rp-dam"><title>{n} dam</title><rect x="{X(x)-2:.1f}" y="{Y(_h(x))-11:.1f}" width="4" height="15" rx="1"/></g>' for n, x in DAMS)
    fall = round(h[0] - h[-1])
    return (f'<figure class="rprof"><svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="rpT rpD"><title id="rpT">The fall of the St. Joseph River</title>'
            f'<desc id="rpD">The river’s surface falls about {fall} metres from near Hillsdale, about {round(h[0])} metres above sea level, to Lake Michigan at St. Joseph, about {round(h[-1])} metres, over roughly {round(D)} kilometres of our simplified line.</desc>'
            f'{g}<path d="{area}" class="rp-a"/><polyline points="{pts}" class="rp-l"/>{tw}{km}</svg>'
            f'<figcaption>The St. Joseph River falls about {fall} metres ({round(fall*3.2808)} feet) on its way to Lake Michigan, most steeply in its first fifty kilometres below Hillsdale. The small blue bars are the dams on the main river today, from the Sturgis Dam near Centreville down to Berrien Springs. Heights are read from the same elevation model, along a simplified line of the river; the river’s own course, with every bend, is longer.</figcaption></figure>')
PROFILE = _profile()
for g in GOLD:
    g['x'] = round((g['lon']-VM['lon0'])*VM['kx'], 3); g['z'] = round(-(g['lat']-VM['lat0'])*VM['kz'], 3)
body = f'''    <p class="crumb"><a href="/map/">← The map room</a></p>
    <p class="kicker">The valley in 3D</p>
    <h1>The St. Joseph River Valley</h1>
    <p class="lede" style="font-size:1.15rem">All {VM['area_km2']:,.0f} square kilometres that drain to the St. Joseph River, from the hills past Hillsdale to Lake Michigan, built from the U.S. Geological Survey’s laser-made elevation of the ground. The river and its branches are drawn in gold. {NG} lost towns are hidden in the hills: find all {NG}.</p>
    <figure class="l3d l3d-v" id="l3d" aria-label="A three-dimensional model of the St. Joseph River watershed">
      <canvas id="l3dC" aria-hidden="true"></canvas>
      <div class="l3d-ui" role="toolbar" aria-label="Model controls">
        <button type="button" class="l3d-b" id="l3dRiv" aria-pressed="true">Rivers</button>
        <button type="button" class="l3d-b" id="l3dTown" aria-pressed="true">Towns</button>
        <label class="l3d-b l3d-r">Height <input type="range" id="l3dEx" min="5" max="40" step="1" value="15" aria-label="Height exaggeration"><output id="l3dExO">×15</output></label>
        <button type="button" class="l3d-b" id="l3dPins" aria-pressed="true">Story pins</button>
        <button type="button" class="l3d-b" id="l3dGeo" aria-pressed="false">What the ice left</button>
        <button type="button" class="l3d-b" id="l3dSpin" aria-pressed="false">Fly around</button>
        <button type="button" class="l3d-b" id="l3dCass">Fly to Cassopolis</button>
        <button type="button" class="l3d-b" id="l3dReset">Reset view</button>
        <button type="button" class="l3d-b" id="l3dFull">Full screen</button>
      </div>
      <div class="l3d-tags" id="l3dTags" aria-hidden="true"></div>
      <div class="l3d-pins" id="l3dPinBox"></div>
      <div class="l3d-card" id="l3dCard" role="status" hidden></div>
      <p class="l3d-found" id="l3dFound" aria-live="polite"></p>
      <p class="l3d-load" id="l3dLoad" role="status">Loading the valley…</p>
      <p class="l3d-help">Drag to turn · scroll or pinch to zoom · tap a gold light or a pin</p>
      <noscript><img src="/map/3d/valley/relief.webp" width="4096" height="2212" alt="The St. Joseph River watershed seen from above, shaded by the shape of the land."></noscript>
    </figure>
    <h2>What you are looking at</h2>
    <ul class="dis">
      <li><b>The whole watershed.</b> The bright land is every acre whose rain ends in the St. Joseph River: parts of fifteen counties in Michigan and Indiana. The darker land around it drains elsewhere: to the Kalamazoo, the Maumee, the Kankakee, or straight to Lake Michigan.</li>
      <li><b>The shape of the ground.</b> The heights come from the U.S. Geological Survey’s 3D Elevation Program, which in this country is made mostly from laser surveys flown county by county. Here the shape of the land is drawn every 200 metres or so, and its light and shade from a grid about 50 metres apart, sharp enough to show the river’s own bluffs and old channels. The heights are raised (×15 to start) because the valley falls only about 200 metres from its eastern hills to the lake. Use the slider to flatten it or raise it further.</li>
      <li><b>What the ice left.</b> The long ridges and knobby hills are moraines, left where the glaciers stood and melted, about 15,000 years ago. The flat, open plains between them are outwash, sand and gravel spread by the meltwater. The river wanders through them both.</li>
      <li><b>Story pins.</b> The gold pins mark where our stories happened, from the Dewey Lake week of 1964 to how Kalamazoo got its name. Press one for the stories told there.</li>
      <li><b>What the ice left.</b> Press it to name the big landforms: the Kalamazoo moraine, which runs through Cassopolis on its way to Kalamazoo and Hastings; the Sturgis moraine, Michigan’s oldest; the Valparaiso moraine along the lake shore; and the flat outwash plains spread by the meltwater. The labels are placed by eye from published maps, near the ground they name, not on a surveyed line.</li>
      <li><b>Fly to Cassopolis.</b> The button flies you down into the county seat and opens <a href="/map/3d/cassopolis/">Cassopolis in LiDAR</a>, where every laser point is shown.</li>
      <li><b>The gold lights.</b> Each is the site of a lost town from the county histories. Tap each one. Where only the township or the neighbourhood is known, the light stands near it and its card says “about here.” Find all {NG} and the valley is yours: there is a badge for it.</li>
    </ul>
    <aside class="l3d-svc" aria-label="A service we offer"><p><b>Your own place in 3D.</b> Project Scroll makes LiDAR models like this one for other places: a farm, a lake, a town, an old mill site, a family’s home ground, from the same public surveys, with fly-throughs and still pictures to keep. <a href="/services/#studio">See the studio</a>, or write to research@projectscroll.com.</p></aside>
    <h2>The river’s fall</h2>
    {PROFILE}
    <p class="note">Sources: U.S. Geological Survey, 3D Elevation Program, bare-earth elevation (public domain); watershed boundary from the USGS Watershed Boundary Dataset (HUC 04050001, St. Joseph); rivers and towns from OpenStreetMap, © OpenStreetMap contributors. Landforms: Michigan State University, <i>Geography of Michigan</i>, “Moraines”; Wikipedia, “Valparaiso Moraine” and “Kankakee Outwash Plain.” Lost-town sites: USGS place names (Williamsville, Kessington), and the land descriptions in Rogers’s <i>History of Cass County</i> (1875), Ellis’s <i>History of Berrien and Van Buren Counties</i> (1880) and Howard’s <i>History of St. Joseph County, Indiana</i> (1907), placed on the federal land-survey grid. 3D drawing by three.js. See also <a href="/map/3d/cassopolis/">Cassopolis in LiDAR</a>, where every laser point is shown.</p>
    <script type="importmap">{{"imports":{{"three":"/vendor/three-{V}/three.module.min.js"}}}}</script>
    <script type="module">
    import * as THREE from 'three';
    import {{ OrbitControls }} from '/vendor/three-{V}/OrbitControls.min.js';
    import {{ Line2 }} from '/vendor/three-{V}/Line2.min.js';
    import {{ LineMaterial }} from '/vendor/three-{V}/LineMaterial.min.js';
    import {{ LineGeometry }} from '/vendor/three-{V}/LineGeometry.min.js';
    (async()=>{{
    const GOLD={json.dumps(GOLD)}, PINV={json.dumps(PINV)}, GEO={json.dumps(GEO)}, CASS={json.dumps(CASS)};
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
    const tally=()=>{{ const n=GOLD.filter(g=>found[g.id]).length, N=GOLD.length; foundEl.textContent=n? n+' of '+N+' lost towns found'+(n===N?'. The valley is yours.':'') : ''; if (n===N && window.psEarn) window.psEarn('valley'); }};
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
    /* story pins and the ice's landforms */
    const span=s=>{{ const e=document.createElement('span'); e.textContent=s; return e; }};
    const pinBox=document.getElementById('l3dPinBox'); let pinsOn=true, geoOn=false;
    const vpins=PINV.map(q=>{{ const e=document.createElement('button'); e.type='button'; e.className='l3d-pin'; e.setAttribute('aria-label','Stories at '+q.n); e.title=q.n;
      e.addEventListener('click',()=>{{ card.innerHTML=''; const h=document.createElement('b'); h.textContent=q.n; card.append(h); const ul=document.createElement('ul'); ul.className='l3d-list'; q.s.forEach(([hd,u])=>{{ const li=document.createElement('li'); const a=document.createElement('a'); a.href=u; a.textContent=hd; li.append(a); ul.append(li); }}); card.append(ul); card.hidden=false; }});
      pinBox.append(e); return {{q,e}}; }});
    const geos=GEO.map(g=>({{g, el:tagFor(g.n,'l3d-tag l3d-geo')}}));
    B('l3dPins',b=>{{ pinsOn=!pinsOn; press(b,pinsOn); pinBox.hidden=!pinsOn; }});
    B('l3dGeo',b=>{{ geoOn=!geoOn; press(b,geoOn); }});
    /* down into Cassopolis */
    let fly=null;
    B('l3dCass',()=>{{ ctl.autoRotate=false; press(spin,false); fly={{t0:performance.now(), fp:cam.position.clone(), ft:ctl.target.clone(), tt:new THREE.Vector3(CASS.x, Y(hAt(CASS.x,CASS.z)), CASS.z)}}; fly.tp=fly.tt.clone().add(new THREE.Vector3(-1.2,2.2,2.4)); if (still) location.href='/map/3d/cassopolis/'; }});
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
    gl.setAnimationLoop(t=>{{ if (!vis) return;
      if (fly){{ const f=Math.min(1,(performance.now()-fly.t0)/3200), e=f<.5?2*f*f:1-Math.pow(-2*f+2,2)/2; cam.position.lerpVectors(fly.fp,fly.tp,e); ctl.target.lerpVectors(fly.ft,fly.tt,e); if (f>=1){{ fly=null; location.href='/map/3d/cassopolis/'; }} }}
      ctl.update();
      const pulse=still?1:1+.18*Math.sin(t/420); gold.forEach((s,i)=>{{ const k=found[s.userData.id]?.75:1; s.scale.setScalar(3.2*k*pulse); s.material.opacity=found[s.userData.id]?.55:1; }});
      gl.render(scene,cam);
      const w=cv.clientWidth, h=cv.clientHeight, dist=cam.position.length();
      if (pinsOn) vpins.forEach(o=>{{ tmp.set(o.q.x, Y(hAt(o.q.x,o.q.z))+.9, o.q.z); tmp.project(cam); const on=tmp.z<1&&Math.abs(tmp.x)<1.02&&Math.abs(tmp.y)<1.02; o.e.style.visibility=on?'visible':'hidden'; o.e.style.transform=`translate(${{(tmp.x*.5+.5)*w}}px,${{(-tmp.y*.5+.5)*h}}px)`; }});
      geos.forEach(o=>{{ tmp.set(o.g.x, Y(hAt(o.g.x,o.g.z))+1.2, o.g.z); tmp.project(cam); const on=geoOn&&tmp.z<1&&Math.abs(tmp.x)<1.05&&Math.abs(tmp.y)<1.05; o.el.style.opacity=on?1:0; o.el.style.transform=`translate(${{(tmp.x*.5+.5)*w}}px,${{(-tmp.y*.5+.5)*h}}px)`; }});
      towns.forEach(o=>{{ tmp.set(o.x, Y(hAt(o.x,o.z))+.6, o.z); tmp.project(cam); const on=showTowns && tmp.z<1 && Math.abs(tmp.x)<1.05 && Math.abs(tmp.y)<1.05; o.el.style.opacity=on?1:0; o.el.style.transform=`translate(${{(tmp.x*.5+.5)*w}}px,${{(-tmp.y*.5+.5)*h}}px)`; }});
    }});
    }})();
    </script>
'''
page('map/3d/valley/index.html', 'The St. Joseph River Valley in 3D · Project Scroll',
     'The whole St. Joseph River watershed in 3D, from Hillsdale to Lake Michigan, built from U.S. Geological Survey elevation data, with the river and its branches in gold and three lost towns to find.',
     body, og='https://projectscroll.com/og/records.jpg')
print('3d valley built')
