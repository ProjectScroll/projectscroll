"""Builds Cassopolis, then and now:  python3 _tools/build_thennow.py

The 1860 town plan (img/cass1860.jpg) is the Cassopolis inset of the LOC wall map,
pixels 7430,1870 to 8740,3778 of g4113c.la000324, assembled from the Library's image
service. One label on the lake has been painted out (see the page note).
Placement: least-squares fit to 19 street corners that keep their 1860 names
(Broadway, Rowland, O'Keefe, East x York, State, Jefferson, Water, South), read from
OpenStreetMap. Root-mean-square error about 5 m, worst about 9 m.
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
import json
_TD=pathlib.Path(__file__).parent/'towns'
NILES=json.loads((_TD/'niles_bounds.json').read_text())
DOWAGIAC=json.loads((_TD/'dowagiac_bounds.json').read_text())
PAWPAW=json.loads((_TD/'pawpaw_bounds.json').read_text())
SBAFF=json.loads((_TD/'southbend_affine.json').read_text())
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
 dict(slug='dowagiac', name='Dowagiac', inset='Dowagiac, Cass Co.', img='/img/towns/dowagiac1860.webp',
      N=DOWAGIAC['N'], W=DOWAGIAC['W'], S=DOWAGIAC['S'], E=DOWAGIAC['E'], maxb='[41.965,-86.135],[42.000,-86.085]',
      lede='Dowagiac, in Cass County, grew up along the Michigan Central Railroad, which cuts across its 1860 plan on a long diagonal.',
      look=['<b>The railroad</b>, its depot and freight house, and how the streets beside it were laid out on the slant.',
            'The <b>Union School</b> on Parsonage Street, and the <b>Cemetery</b> at the west edge of town.',
            'The <b>additions</b> named for the men who laid them out: Hamilton’s, McOmber’s, Spalding’s and the rest. Each name is a lead to a plat.',
            '<b>Dowagiac Creek</b> and <b>Herndon Mills</b> at the south edge of the plan.',
            'The <b>names on the lots</b>, such as P. Hamilton and G. C. Jones, and the business directory printed beside the plan.'],
      how='The plan was cut from the Library of Congress copy of the wall map. Thirty-three street corners that appear on both maps (Parsonage, Green, Cross, Center, Hamilton, Orchard, Front and McOmber, where they meet Wayne, North, Telegraph, West, Spruce, Courtland and Division) were matched by measurement, and the plan was fitted to them. On average the old corners land within about three yards of the new ones.',
      extra='<p class="note">The little village of Brownsville, printed in the corner of the same inset, has been left out of this copy.</p>',
      og='dowagiac', desc='The 1860 plan of Dowagiac, Michigan, laid over today’s streets. Fade between them or compare side by side.'),
 dict(slug='paw-paw', name='Paw Paw', inset='Paw Paw, County Seat of Van Buren Co.', img='/img/towns/pawpaw1860.webp',
      N=PAWPAW['N'], W=PAWPAW['W'], S=PAWPAW['S'], E=PAWPAW['E'], maxb='[42.200,-85.915],[42.235,-85.865]',
      lede='Paw Paw, the county seat of Van Buren County, sits on the Paw Paw River.',
      look=['<b>Kalamazoo, Niles, LaGrave, Brown, Van Buren and Gremps Streets</b>, all still carrying their 1860 names.',
            'The <b>Paw Paw River</b> winding through the west side of town, and the mills and tannery beside it.',
            'The <b>Cemetery</b> and the <b>Road to Allegan</b> at the north edge.',
            'The <b>additions</b>: Willard’s, Dyckman’s and Woodman’s. Each name is a lead to a plat.',
            'The <b>business directory</b> printed beside the plan: lawyers, county officers, merchants and mechanics of 1860.'],
      how='The plan was cut from the Library of Congress copy of the wall map. Thirty street corners that appear on both maps (Gremps, Kalamazoo, Niles, LaGrave, Brown and Van Buren, where they meet Cedar, Pine, Elm, Oak and Paw Paw Street) were matched by measurement, and the plan was fitted to them. On average the old corners land within about four yards of the new ones.',
      extra='<p class="note">The wall map was printed in sheets, and the join between two of them runs across the south end of this plan. The strip below the join has been left off.</p>',
      og='pawpaw', desc='The 1860 plan of Paw Paw, Michigan, laid over today’s streets. Fade between them or compare side by side.'),
 dict(slug='south-bend', name='South Bend', year='1863', img=None,
      iiif='https://tile.loc.gov/image-services/iiif/service:gmd:gmd409:g4093:g4093s:la000168', region=[230,5800,3360,3200], px=2400,
      aff=dict(SBAFF), N=41.691177, W=-86.274251, S=41.663669, E=-86.233984, maxb='[41.645,-86.300],[41.710,-86.205]',
      lede='The 1863 map of St. Joseph County, Indiana, has a plan of South Bend in its corner, with the village of Lowell across the river.',
      look=['<b>Michigan, Main and Lafayette Streets</b>, and the <b>Court House square</b> on Main. Fade to today and the square is still there.',
            '<b>Water Street</b> and <b>Market Street</b>. Both are still on the ground, under other names. Fade to today and find what they are called now.',
            '<b>Lowell</b>, across the river: a separate town in 1863, part of South Bend today.',
            'The great bend of the <b>St. Joseph River</b>, and the bridges across it.',
            'The <b>Agricultural Fair Ground</b>, and the <b>Cemetery</b> beside the La Porte road at the west edge of town.',
            'The <b>additions</b> named for the men who laid them out, such as Hendricks &amp; Grant’s. Each name is a lead to a plat in the county’s records.'],
      how='The plan is shown live from the Library of Congress’s image service, at full detail. Eighteen street corners that appear on both maps (Marion, Madison, Washington, Jefferson and Wayne, where they meet William, Lafayette, Main and Michigan) were matched by measurement, and the plan was fitted to them, turning it a fraction of a degree. On average the old corners land within about nine yards of the new ones. The worst is near William Street, which jogs on today’s ground and runs straight on the 1863 plan.',
      extra='<p class="note">The pale band across the plan is a fold in the paper of the original. Nothing has been painted out.</p>',
      credit='1863 plan: <i>Map of St. Joseph Co., Indiana</i>, compiled and published by M. W. Stokes (South Bend, 1863), inset “South Bend” and “Lowell.” Library of Congress, Geography and Map Division, g4093s.la000168 (item 2013593163). Public domain, shown live from the Library’s image service.',
      og='map', desc='The 1863 plan of South Bend, Indiana, laid over today’s streets. Fade between them or compare side by side.'),
]
CREDIT='1860 plan: <i>Map of the Counties of Cass, Van Buren and Berrien, Michigan</i> (Philadelphia: Geil, Harley &amp; Siverd, 1860), inset “{inset}” Library of Congress, Geography and Map Division, g4113c.la000324. Public domain.'
def overlay(t,Y):
    alt=f"{Y} town plan of {t['name']}"
    if not t.get('aff'):
        return f"      const old=L.imageOverlay('{t['img']}',B,{{pane:'old', opacity:0.75, alt:'{alt}', className:'tnold'}}).addTo(map);\n"
    x0,y0,w,h=t['region']; A=t['aff']['clat']; C=t['aff']['clon']; k=w/t['px']
    url=f"{t['iiif']}/{x0},{y0},{w},{h}/{t['px']},/0/default.jpg"
    # an image placed by an affine transform: image pixel (u,v) -> full-map pixel -> lat/lon (least-squares fit)
    return f"""      const ll=(u,v)=>{{ const x={x0}+u*{k:.6f}, y={y0}+v*{k:.6f}; return L.latLng({A[0]!r}*x+{A[1]!r}*y+{A[2]!r}, {C[0]!r}*x+{C[1]!r}*y+{C[2]!r}); }};
      const Aff=L.Layer.extend({{
        onAdd(m){{ const el=this._el=L.DomUtil.create('img','tnold leaflet-image-layer'); el.alt='{alt}'; el.style.transformOrigin='0 0'; el.style.opacity=this._op;
          el.onload=()=>{{ this._place(); this.fire('load'); }}; el.onerror=()=>this.fire('error'); el.src='{url}'; m.getPane('old').appendChild(el); m.on('viewreset zoomend resize',this._place,this); }},
        onRemove(m){{ this._el.remove(); m.off('viewreset zoomend resize',this._place,this); }},
        _place(){{ const el=this._el, W=el.naturalWidth, H=el.naturalHeight; if(!W) return; const m=this._map;
          const p0=m.latLngToLayerPoint(ll(0,0)), px=m.latLngToLayerPoint(ll(W,0)), py=m.latLngToLayerPoint(ll(0,H));
          el.style.width=W+'px'; el.style.height=H+'px';
          el.style.transform='matrix('+[(px.x-p0.x)/W,(px.y-p0.y)/W,(py.x-p0.x)/H,(py.y-p0.y)/H,p0.x,p0.y].map(n=>n.toFixed(6)).join(',')+')'; }},
        setOpacity(o){{ this._op=o; if(this._el) this._el.style.opacity=o; return this; }},
        getElement(){{ return this._el; }}
      }});
      const old=new Aff().setOpacity(0.75).addTo(map);
"""
def build(t):
    others=' · '.join(f'<a href="/map/{o["slug"]}/">{o["name"]}</a>' for o in TOWNS if o['slug']!=t['slug'])
    Y=t.get('year','1860')
    looks=''.join(f'<li>{x}</li>' for x in t['look'])
    return f'''    <p class="crumb"><a href="/map/">← The map room</a></p>
    <p class="kicker">Then and now</p>
    <h1>{t["name"]}, {Y} and today</h1>
    <p class="lede" style="font-size:1.15rem">{t["lede"]} Here it is laid over the streets of today. Fade between the two, or drag a line across and see one beside the other.</p>
    <p class="note">Other towns: {others}</p>
    <p class="note">Drag to move. Scroll, pinch or use the buttons to zoom. The old plan was lined up by hand on street corners that still carry their {Y} names, so it is close but not exact: expect it to be out by a few yards in places.</p>
  <div class="maproom">
    <div class="mapbar tnbar">
      <span class="seg" role="group" aria-label="How to compare">
        <button type="button" class="btn" id="tnFade" aria-pressed="true">Fade</button><button type="button" class="btn" id="tnSwipe" aria-pressed="false">Side by side</button>
      </span>
      <label class="tnrange" id="tnFadeBox"><span>Today</span><input type="range" id="tnOp" min="0" max="100" value="75" aria-label="How much of the {Y} plan to show"><span>{Y}</span></label>
      <button type="button" class="btn" id="tnHome">Back to town</button>
      <span class="mapstat" id="tnStat" aria-live="polite">Loading…</span>
    </div>
    <div class="tnwrap">
      <div id="tnMap" class="osd tnmap" role="application" aria-label="The {Y} plan of {t["name"]} laid over a modern street map"></div>
      <div class="tnswipe" id="tnLine" data-year="{Y}" hidden><button type="button" class="tnhandle" id="tnHandle" aria-label="Drag to move the dividing line. Left and right arrow keys also move it."><span aria-hidden="true">◂ ▸</span></button></div>
    </div>
  </div>
    <h2>Things to look for</h2>
    <ul class="dis">{looks}</ul>
    <h2>How this was made</h2>
    <p>{t["how"]}</p>
    {t.get("extra","")}
    <p class="note">{t.get("credit") or CREDIT.format(inset=t["inset"])} Today’s streets and water: drawn from OpenStreetMap data, © OpenStreetMap contributors, available under the Open Database License.</p>
    <link rel="stylesheet" href="/vendor/leaflet-1.9.4/leaflet.css?v=1">
    <script src="/vendor/leaflet-1.9.4/leaflet.js?v=1"></script>
    <script>
    (function(){{ "use strict";
      const stat=document.getElementById('tnStat');
      if (!window.L){{ stat.textContent='The map could not load. Try refreshing the page.'; return; }}
      const B=L.latLngBounds([{t["S"]},{t["W"]}],[{t["N"]},{t["E"]}]);
      const map=L.map('tnMap',{{{'zoomAnimation:false, ' if t.get('aff') else ''}zoomSnap:0.25, minZoom:13, maxZoom:19, maxBounds:L.latLngBounds({t["maxb"]}), maxBoundsViscosity:0.8, scrollWheelZoom:true}});
      const home=()=>map.fitBounds(B.pad(0.02));
      home();
      // today's streets and water, drawn from OpenStreetMap data (no labels, by design)
      const dec=a=>{{ const o=[]; let la=0, lo=0; for(let i=0;i<a.length;i+=2){{ la+=a[i]; lo+=a[i+1]; o.push([la/1e5, lo/1e5]); }} return o; }};
      const isDark=()=>{{ const t=document.documentElement.dataset.theme; return t ? t==='dark' : matchMedia('(prefers-color-scheme: dark)').matches; }};
      const pal=()=>isDark() ? {{land:'#1d2329', water:'#2c4656', minor:'#7d8994', major:'#c9d1d8', rail:'#8a7f72'}} : {{land:'#f1efe8', water:'#b9d0dc', minor:'#a6a39a', major:'#5d5a54', rail:'#8a7560'}};
      const cv=L.canvas({{padding:0.5}});
      const groups={{w:[], s:[], r:[], m:[], x:[]}}; let sw=4;
      const style={{
        w:c=>({{renderer:cv, stroke:false, fillColor:c.water, fillOpacity:1, interactive:false}}),
        s:c=>({{renderer:cv, color:c.water, weight:sw, interactive:false}}),
        r:c=>({{renderer:cv, color:c.minor, weight:2, interactive:false}}),
        m:c=>({{renderer:cv, color:c.major, weight:3.5, interactive:false}}),
        x:c=>({{renderer:cv, color:c.rail, weight:2, dashArray:'6 5', interactive:false}})
      }};
      const paint=()=>{{ const c=pal(); map.getContainer().style.background=c.land; for(const k in groups) for(const l of groups[k]) l.setStyle(style[k](c)); }};
      fetch('/map/{t["slug"]}/today.json?v=1').then(r=>r.json()).then(d=>{{
        const c=pal(); if(!d.w.length) sw=12; // a river given only as its centre line is drawn wide
        for(const p of d.w) groups.w.push(L.polygon(p.map(dec), style.w(c)).addTo(map));
        for(const k of ['s','r','x','m']) for(const a of (d[k]||[])) groups[k].push(L.polyline(dec(a), style[k](c)).addTo(map));
      }}).catch(()=>{{ stat.textContent='Today’s streets did not load. Try refreshing the page.'; }});
      new MutationObserver(paint).observe(document.documentElement,{{attributes:true, attributeFilter:['data-theme']}});
      matchMedia('(prefers-color-scheme: dark)').addEventListener('change',paint);
      map.attributionControl.setPrefix(false);
      map.attributionControl.addAttribution('Today: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors');
      map.getContainer().style.background=pal().land;
      map.createPane('old').style.zIndex=450;
{overlay(t,Y)}      old.on('load',()=>{{ stat.textContent='{Y} plan placed over today’s streets.'; clip(); }});
      old.on('error',()=>{{ stat.textContent='The {Y} plan did not load. Try refreshing the page.'; }});
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
    page(f'map/{t["slug"]}/index.html', f'{t["name"]}, {t.get("year","1860")} and today · Project Scroll', t['desc'], build(t), og=f'https://projectscroll.com/og/{t["og"]}.jpg')
print('then-and-now built:', ', '.join(t['name'] for t in TOWNS))
