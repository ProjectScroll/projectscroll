"""Builds Cassopolis, then and now:  python3 tools/build_thennow.py

The 1860 town plan (img/cass1860.jpg) is the Cassopolis inset of the LOC wall map,
pixels 7430,1870 to 8740,3778 of g4113c.la000324, assembled from the Library's image
service. One label on the lake has been painted out (see the page note).
Placement: least-squares fit to 19 street corners that keep their 1860 names
(Broadway, Rowland, O'Keefe, East x York, State, Jefferson, Water, South), read from
OpenStreetMap. Root-mean-square error about 5 m, worst about 9 m.
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
import json
NILES=json.loads((pathlib.Path(__file__).parent/'towns'/'niles_bounds.json').read_text())
TOWNS = [
 dict(slug='cassopolis', name='Cassopolis', inset='Cassopolis, County Seat of Cass Co.', img='/img/cass1860.webp',
      N=41.917772, W=-86.018103, S=41.906100, E=-86.007168, maxb='[41.895,-86.035],[41.930,-85.990]',
      lede='The 1860 wall map has a little plan of Cassopolis, the county seat, with every block, lot and street the engraver knew.',
      look=['<b>State Street and Broadway.</b> The heart of the 1860 town. Find the <b>Court House</b> and the <b>Jail</b> just north of State, then fade to today.',
            '<b>Timber Street</b>, between O’Keefe and East. Look for it on today’s map.',
            'The <b>Union School</b> at the top of the plan, beside the State Road.',
            'The <b>Tannery</b> and the <b>Cemetery</b> on the west side of town, and the State Road running north.',
            'The <b>names on the lots</b>: Tompkins, Martin, Histed, Read, Jones and the rest. Each one is a lead to a deed.'],
      how='The plan was cut from the Library of Congress copy of the wall map. Nineteen street corners that appear on both maps (Broadway, Rowland, O’Keefe and East, where they meet York, State, Jefferson, Water and South) were matched by measurement, and the plan was scaled to fit them. On average the old corners land within about five yards of the new ones.',
      extra='<p class="note">One label has been painted out of this copy so that it does not spoil the hunt. Nothing else has been changed.</p>',
      og='cassopolis', desc='The 1860 town plan of Cassopolis, Michigan, laid over today’s streets. Fade between them or compare side by side.'),
 dict(slug='niles', name='Niles', inset='City of Niles, Berrien Co.', img='/img/towns/niles1860.webp',
      N=NILES['N'], W=NILES['W'], S=NILES['S'], E=NILES['E'], maxb='[41.810,-86.285],[41.855,-86.220]',
      lede='The biggest town plan on the 1860 wall map is the City of Niles, in Berrien County, astride the St. Joseph River.',
      look=['<b>The numbered streets</b>, Front to Twelfth, still in the same order today. Fade to see how closely the blocks match.',
            'The <b>Michigan Central Railroad</b> and its depot on the river, and the <b>mill race</b> beside it.',
            'The <b>bridges</b> across the St. Joseph, and the island in the river.',
            'The <b>additions</b> named for the men who laid them out: Hoffman’s, Beeson’s, Moore’s, Bond’s and the rest. Each name is a lead to a plat in the county’s records.',
            'The <b>Union School</b>, the <b>Fair Ground</b> and the <b>Cemetery</b> on the east side of town.'],
      how='The plan was cut from the Library of Congress copy of the wall map. Forty-three street corners that appear on both maps (Front Street to Ninth Street, where they meet Eagle, Howard, Cass, Ferry, Sycamore and Main) were matched by measurement, and the plan was fitted to them, turning it a fraction of a degree. On average the old corners land within about four yards of the new ones. Where today’s Main Street bends away east of Fifth Street it was left out of the fit, because the 1860 plan carries it straight.',
      og='niles', desc='The 1860 plan of the City of Niles, Michigan, laid over today’s streets. Fade between them or compare side by side.'),
]
def build(t):
    others=' · '.join(f'<a href="/map/{o["slug"]}/">{o["name"]}</a>' for o in TOWNS if o['slug']!=t['slug'])
    looks=''.join(f'<li>{x}</li>' for x in t['look'])
    return f'''    <p class="crumb"><a href="/map/">← The map room</a></p>
    <p class="kicker">Then and now</p>
    <h1>{t["name"]}, 1860 and today</h1>
    <p class="lede" style="font-size:1.15rem">{t["lede"]} Here it is laid over the streets of today. Fade between the two, or drag a line across and see one beside the other.</p>
    <p class="note">Other towns: {others}</p>
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
      <div id="tnMap" class="osd tnmap" role="application" aria-label="The 1860 plan of {t["name"]} laid over a modern street map"></div>
      <div class="tnswipe" id="tnLine" hidden><button type="button" class="tnhandle" id="tnHandle" aria-label="Drag to move the dividing line. Left and right arrow keys also move it."><span aria-hidden="true">◂ ▸</span></button></div>
    </div>
  </div>
    <h2>Things to look for</h2>
    <ul class="dis">{looks}</ul>
    <h2>How this was made</h2>
    <p>{t["how"]}</p>
    {t.get("extra","")}
    <p class="note">1860 plan: <i>Map of the Counties of Cass, Van Buren and Berrien, Michigan</i> (Philadelphia: Geil, Harley &amp; Siverd, 1860), inset “{t["inset"]}” Library of Congress, Geography and Map Division, g4113c.la000324. Public domain. Today’s streets and water: drawn from OpenStreetMap data, © OpenStreetMap contributors, available under the Open Database License.</p>
    <link rel="stylesheet" href="/vendor/leaflet-1.9.4/leaflet.css?v=1">
    <script src="/vendor/leaflet-1.9.4/leaflet.js?v=1"></script>
    <script>
    (function(){{ "use strict";
      const stat=document.getElementById('tnStat');
      if (!window.L){{ stat.textContent='The map could not load. Try refreshing the page.'; return; }}
      const B=L.latLngBounds([{t["S"]},{t["W"]}],[{t["N"]},{t["E"]}]);
      const map=L.map('tnMap',{{zoomSnap:0.25, minZoom:13, maxZoom:19, maxBounds:L.latLngBounds({t["maxb"]}), maxBoundsViscosity:0.8, scrollWheelZoom:true}});
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
      fetch('/map/{t["slug"]}/today.json?v=1').then(r=>r.json()).then(d=>{{
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
      const old=L.imageOverlay('{t["img"]}',B,{{pane:'old', opacity:0.75, alt:'1860 town plan of {t["name"]}', className:'tnold'}}).addTo(map);
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
for t in TOWNS:
    page(f'map/{t["slug"]}/index.html', f'{t["name"]}, 1860 and today · Project Scroll', t['desc'], build(t), og=f'https://projectscroll.com/og/{t["og"]}.jpg')
print('then-and-now built:', ', '.join(t['name'] for t in TOWNS))
