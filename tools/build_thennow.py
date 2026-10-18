"""Builds Cassopolis, then and now:  python3 tools/build_thennow.py

The 1860 town plan (img/cass1860.jpg) is the Cassopolis inset of the LOC wall map,
pixels 7430,1870 to 8740,3778 of g4113c.la000324, assembled from the Library's image
service. One label on the lake has been painted out (see the page note).
Placement: least-squares fit to 19 street corners that keep their 1860 names
(Broadway, Rowland, O'Keefe, East x York, State, Jefferson, Water, South), read from
OpenStreetMap. Root-mean-square error about 5 m, worst about 9 m.
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
N, W, S, E = 41.917772, -86.018103, 41.906100, -86.007168
body = f'''    <p class="crumb"><a href="/map/">← The map room</a></p>
    <p class="kicker">Then and now</p>
    <h1>Cassopolis, 1860 and today</h1>
    <p class="lede" style="font-size:1.15rem">The 1860 wall map has a little plan of Cassopolis, the county seat, with every block, lot and street the engraver knew. Here it is laid over the streets of today. Fade between the two, or drag a line across and see one beside the other.</p>
    <p class="note">Drag to move, scroll or pinch to zoom. The old plan was lined up by hand on street corners that still carry their 1860 names, so it is close but not exact: expect it to be out by a few yards in places.</p>
  <div class="maproom">
    <div class="mapbar tnbar">
      <span class="seg" role="group" aria-label="How to compare">
        <button type="button" class="btn" id="tnFade" aria-pressed="true">Fade</button><button type="button" class="btn" id="tnSwipe" aria-pressed="false">Side by side</button>
      </span>
      <label class="tnrange" id="tnFadeBox"><span>Today</span><input type="range" id="tnOp" min="0" max="100" value="75" aria-label="How much of the 1860 plan to show"><span>1860</span></label>
      <button type="button" class="btn" id="tnHome">Back to town</button>
      <span class="mapstat" id="tnStat" aria-live="polite">Loading…</span>
    </div>
    <div class="tnwrap">
      <div id="tnMap" class="osd tnmap" role="application" aria-label="The 1860 plan of Cassopolis laid over a modern street map"></div>
      <div class="tnswipe" id="tnLine" hidden><button type="button" class="tnhandle" id="tnHandle" aria-label="Drag to move the dividing line. Left and right arrow keys also move it."><span aria-hidden="true">◂ ▸</span></button></div>
    </div>
  </div>
    <h2>Things to look for</h2>
    <ul class="dis">
      <li><b>State Street and Broadway.</b> The heart of the 1860 town. Find the <b>Court House</b> and the <b>Jail</b> just north of State, then fade to today.</li>
      <li><b>Timber Street</b>, between O’Keefe and East. Look for it on today’s map.</li>
      <li>The <b>Union School</b> at the top of the plan, beside the State Road.</li>
      <li>The <b>Tannery</b> and the <b>Cemetery</b> on the west side of town, and the State Road running north.</li>
      <li>The <b>names on the lots</b>: Tompkins, Martin, Histed, Read, Jones and the rest. Each one is a lead to a deed.</li>
    </ul>
    <h2>How this was made</h2>
    <p>The plan was cut from the Library of Congress copy of the wall map. Nineteen street corners that appear on both maps (Broadway, Rowland, O’Keefe and East, where they meet York, State, Jefferson, Water and South) were matched by measurement, and the plan was scaled to fit them. On average the old corners land within about five yards of the new ones.</p>
    <p class="note">One label has been painted out of this copy so that it does not spoil the hunt. Nothing else has been changed.</p>
    <p class="note">1860 plan: <i>Map of the Counties of Cass, Van Buren and Berrien, Michigan</i> (Philadelphia: Geil, Harley &amp; Siverd, 1860), inset “Cassopolis, County Seat of Cass Co.” Library of Congress, Geography and Map Division, g4113c.la000324. Public domain. Today’s streets and water: drawn from OpenStreetMap data, © OpenStreetMap contributors, available under the Open Database License.</p>
    <link rel="stylesheet" href="/vendor/leaflet-1.9.4/leaflet.css?v=1">
    <script src="/vendor/leaflet-1.9.4/leaflet.js?v=1"></script>
    <script>
    (function(){{ "use strict";
      const stat=document.getElementById('tnStat');
      if (!window.L){{ stat.textContent='The map could not load. Try refreshing the page.'; return; }}
      const B=L.latLngBounds([{S},{W}],[{N},{E}]);
      const map=L.map('tnMap',{{zoomSnap:0.25, minZoom:13, maxZoom:19, maxBounds:L.latLngBounds([41.895,-86.035],[41.930,-85.990]), maxBoundsViscosity:0.8, scrollWheelZoom:true}});
      const home=()=>map.fitBounds(B.pad(0.02));
      home();
      // today's streets and water, drawn from OpenStreetMap data (no labels, by design)
      const dec=a=>{{ const o=[]; let la=0, lo=0; for(let i=0;i<a.length;i+=2){{ la+=a[i]; lo+=a[i+1]; o.push([la/1e5, lo/1e5]); }} return o; }};
      const isDark=()=>{{ const t=document.documentElement.dataset.theme; return t ? t==='dark' : matchMedia('(prefers-color-scheme: dark)').matches; }};
      const pal=()=>isDark() ? {{land:'#1d2329', water:'#2c4656', minor:'#7d8994', major:'#c9d1d8', rail:'#8a7f72'}} : {{land:'#f1efe8', water:'#b9d0dc', minor:'#a6a39a', major:'#5d5a54', rail:'#8a7560'}};
      const cv=L.canvas({{padding:0.5}});
      const groups={{w:[], r:[], m:[], x:[]}};
      const style={{
        w:c=>({{renderer:cv, stroke:false, fillColor:c.water, fillOpacity:1, interactive:false}}),
        r:c=>({{renderer:cv, color:c.minor, weight:2, interactive:false}}),
        m:c=>({{renderer:cv, color:c.major, weight:3.5, interactive:false}}),
        x:c=>({{renderer:cv, color:c.rail, weight:2, dashArray:'6 5', interactive:false}})
      }};
      const paint=()=>{{ const c=pal(); map.getContainer().style.background=c.land; for(const k in groups) for(const l of groups[k]) l.setStyle(style[k](c)); }};
      fetch('/map/cassopolis/today.json?v=1').then(r=>r.json()).then(d=>{{
        const c=pal();
        for(const p of d.w) groups.w.push(L.polygon(p.map(dec), style.w(c)).addTo(map));
        for(const k of ['r','x','m']) for(const a of d[k]) groups[k].push(L.polyline(dec(a), style[k](c)).addTo(map));
      }}).catch(()=>{{ stat.textContent='Today’s streets did not load. Try refreshing the page.'; }});
      new MutationObserver(paint).observe(document.documentElement,{{attributes:true, attributeFilter:['data-theme']}});
      matchMedia('(prefers-color-scheme: dark)').addEventListener('change',paint);
      map.attributionControl.setPrefix(false);
      map.attributionControl.addAttribution('Today: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors');
      map.getContainer().style.background=pal().land;
      map.createPane('old').style.zIndex=450;
      const old=L.imageOverlay('/img/cass1860.webp',B,{{pane:'old', opacity:0.75, alt:'1860 town plan of Cassopolis', className:'tnold'}}).addTo(map);
      old.on('load',()=>{{ stat.textContent='1860 plan placed over today’s streets.'; clip(); }});
      old.on('error',()=>{{ stat.textContent='The 1860 plan did not load. Try refreshing the page.'; }});
      const op=document.getElementById('tnOp');
      op.addEventListener('input',()=>old.setOpacity(op.value/100));
      document.getElementById('tnHome').onclick=home;
      // side by side
      const wrap=document.querySelector('.tnwrap'), line=document.getElementById('tnLine'), handle=document.getElementById('tnHandle');
      const bFade=document.getElementById('tnFade'), bSwipe=document.getElementById('tnSwipe'), fadeBox=document.getElementById('tnFadeBox');
      let swipe=false, frac=0.5;
      function clip(){{
        const img=old.getElement(); if(!img) return;
        if(!swipe){{ img.style.clipPath=''; return; }}
        const w=wrap.getBoundingClientRect(), r=img.getBoundingClientRect();
        const x=w.left+w.width*frac;
        const cut=Math.min(100,Math.max(0,r.right-x)/(r.width||1)*100);
        img.style.clipPath='inset(0 '+cut.toFixed(3)+'% 0 0)';
        line.style.left=(frac*100)+'%';
      }}
      function mode(s){{
        swipe=s; bFade.setAttribute('aria-pressed',String(!s)); bSwipe.setAttribute('aria-pressed',String(s));
        line.hidden=!s; fadeBox.hidden=s; old.setOpacity(s?1:op.value/100); clip();
      }}
      bFade.onclick=()=>mode(false); bSwipe.onclick=()=>mode(true);
      map.on('move zoom zoomend resize viewreset',clip);
      map.on('zoomanim',()=>requestAnimationFrame(function f(t0){{ clip(); if(map._animatingZoom) requestAnimationFrame(f); }}));
      let drag=false;
      const at=e=>{{ const w=wrap.getBoundingClientRect(); frac=Math.min(0.98,Math.max(0.02,(e.clientX-w.left)/w.width)); clip(); }};
      handle.addEventListener('pointerdown',e=>{{ drag=true; handle.setPointerCapture(e.pointerId); map.dragging.disable(); e.preventDefault(); }});
      handle.addEventListener('pointermove',e=>{{ if(drag) at(e); }});
      const up=()=>{{ if(!drag) return; drag=false; map.dragging.enable(); }};
      handle.addEventListener('pointerup',up); handle.addEventListener('pointercancel',up);
      handle.addEventListener('keydown',e=>{{ if(e.key==='ArrowLeft'||e.key==='ArrowRight'){{ frac=Math.min(0.98,Math.max(0.02,frac+(e.key==='ArrowLeft'?-0.04:0.04))); clip(); e.preventDefault(); }} }});
      L.DomEvent.disableClickPropagation(line);
    }})();
    </script>
'''
page('map/cassopolis/index.html', 'Cassopolis, 1860 and today · Project Scroll',
     'The 1860 town plan of Cassopolis, Michigan, laid over today’s streets. Fade between them or compare side by side.', body)
print('then-and-now built')
