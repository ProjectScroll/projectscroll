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
GOAFF=json.loads((_TD/'goshen_affine.json').read_text())
ELAFF=json.loads((_TD/'elkhart_affine.json').read_text())
UWM='https://cdm17272.contentdm.oclc.org/iiif/2/agdm:21064'
ELKCREDIT='1861 plan: <i>Map of Elkhart Co. Indiana</i> (Philadelphia: Samuel Geil, 1861), published by Geil &amp; Harley, inset “{inset}.” American Geographical Society Library, University of Wisconsin–Milwaukee Libraries. Public domain, shown live from the Library’s image service.'
TOWNS = [
 dict(slug='cassopolis', hunt={'h': [1370218351], 't': 'The street that changed its name', 'q': 'Timber Street ran between O’Keefe and East in 1860. It is still there today under another name. Fade the plan away and find it.', 'lab': 'What it is called today'}, name='Cassopolis', inset='Cassopolis, County Seat of Cass Co.', img='/img/cass1860.webp',
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
 dict(slug='niles', hunt={'h': [172395083, 5859367], 't': 'Two streets that changed their names', 'q': 'North Street, on the west bank below Main, and the street marked only “Avenue” on the east side of town are both still on the ground under other names. Fade the plan away and find them.', 'lab': 'What one of them is called today'}, name='Niles', inset='City of Niles, Berrien Co.', img='/img/towns/niles1860.webp',
      N=NILES['N'], W=NILES['W'], S=NILES['S'], E=NILES['E'], maxb='[41.810,-86.285],[41.855,-86.220]',
      lede='The biggest town plan on the 1860 wall map is the City of Niles, in Berrien County, astride the St. Joseph River.',
      look=['<b>The numbered streets</b>, Front to Twelfth, still in the same order today. Fade to see how closely the blocks match.',
            'The <b>Michigan Central Railroad</b> and its depot on the river, and the <b>mill race</b> beside it.',
            'The <b>bridges</b> across the St. Joseph, and the island in the river.',
            'The <b>additions</b> named for the men who laid them out: Hoffman’s, Beeson’s, Moore’s, Bond’s and the rest. Each name is a lead to a plat in the county’s records.',
            'The <b>Union School</b>, the <b>Fair Ground</b> and the <b>Cemetery</b> on the east side of town.'],
      how='The plan was cut from the Library of Congress copy of the wall map. Forty-three street corners that appear on both maps (Front Street to Ninth Street, where they meet Eagle, Howard, Cass, Ferry, Sycamore and Main) were matched by measurement, and the plan was fitted to them, turning it a fraction of a degree. On average the old corners land within about four yards of the new ones. Where today’s Main Street bends away east of Fifth Street it was left out of the fit, because the 1860 plan carries it straight.',
      og='niles', desc='The 1860 plan of the City of Niles, Michigan, laid over today’s streets. Fade between them or compare side by side.'),
 dict(slug='dowagiac', hunt={'h': [1791197882, 176602452, 2767408012], 't': 'Three streets in Spalding’s Addition', 'q': 'East of the railroad, in Spalding’s Addition, the 1860 plan names Spalding, Wayne and Center Streets. Today one is spelled another way, one has a new name, and one has become part of a longer street. Fade the plan away and find all three.', 'lab': 'What one of them is called today'}, name='Dowagiac', inset='Dowagiac, Cass Co.', img='/img/towns/dowagiac1860.webp',
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
 dict(slug='paw-paw', hunt={'h': [3220699467], 't': 'The street that changed its name', 'q': 'Main Street ran through the middle of Paw Paw in 1860, between Oak and Paw Paw Streets. Through the heart of town it carries another name today. Fade the plan away and find it.', 'lab': 'What it is called today'}, name='Paw Paw', inset='Paw Paw, County Seat of Van Buren Co.', img='/img/towns/pawpaw1860.webp',
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
 dict(slug='south-bend', hunt={'h': [4239982495, 1544337818], 't': 'Two streets that changed their names', 'q': 'Water Street and Market Street are both still on the ground in South Bend, under the names they carry today. Fade the plan away and find them.', 'lab': 'What one of them is called today'}, name='South Bend', year='1863', img=None,
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
      og='south-bend', desc='The 1863 plan of South Bend, Indiana, laid over today’s streets. Fade between them or compare side by side.'),
 dict(slug='goshen', hunt={'h': [3923262336, 2088074974], 't': 'Two streets that changed their names', 'q': 'Market Street, on the south side of the Court House square, has a new name today, and Pearl Street at the south end of town is spelled another way. Fade the plan away and find both.', 'lab': 'What one of them is called today'}, name='Goshen', year='1861', img=None, iiif=UWM, region=[7340,2250,1790,2550], px=1790,
      aff=dict(GOAFF), N=41.5955, W=-85.8412, S=41.5779, E=-85.8238, maxb='[41.565,-85.860],[41.608,-85.805]',
      lede='Goshen, the county seat of Elkhart County, Indiana, has a plan in the corner of the 1861 county map, coloured by its additions.',
      look=['The <b>Court House square</b>, between Third and Main. Fade to today: the courthouse still stands on it.',
            '<b>Market Street</b>, along the south side of the square. It is still there under another name. Fade to today and find what it is called now.',
            '<b>Pearl Street</b> at the south end of town. Today’s map spells it differently.',
            'The <b>railroad</b> crossing the north-east of town on its long diagonal, with the <b>Depot Grounds</b> and the passenger and freight depots.',
            'The <b>race</b> and <b>Rock Run</b>, the machine shop and the tannery beside them, and the <b>Elkhart River</b> on the west.',
            'The <b>additions</b> named for the men who laid them out: Barnes’s, Albright’s, Mayfield’s, Chamberlain’s and the rest. Each name is a lead to a plat in the county’s records.'],
      how='The plan is shown live from the University of Wisconsin–Milwaukee Libraries’ image service, at full detail. Forty street corners that appear on both maps (Second, Third, Main, Fifth, Sixth and Seventh, where they meet Wilkinson, Pike, Clinton, Market, Washington, Jefferson, Madison, Monroe and Pearl) were matched by measurement, and the plan was fitted to them, turning it a little over half a degree. On average the old corners land within about four yards of the new ones. Monroe Street jogs at Main on both maps, and each side was measured on its own. Where today’s Main Street bends away south of Monroe it was left out of the fit.',
      extra='<p class="note">The business directory printed beside the plan has been left off this copy, though a few of its letters show at the left edge. The whole directory is on the full county map in the <a href="/map/#town-goshen">map room</a>.</p>',
      credit=ELKCREDIT.format(inset='Goshen'), inset='Goshen',
      og='goshen', desc='The 1861 plan of Goshen, Indiana, laid over today’s streets. Fade between them or compare side by side.'),
 dict(slug='elkhart', hunt={'h': [4228470081], 't': 'The street that changed its name', 'q': 'Pigeon Street ran between Jackson and High in 1861. It is still there today under another name. Fade the plan away and find it.', 'lab': 'What it is called today'}, name='Elkhart', year='1861', img=None, iiif=UWM, region=[1700,2370,1890,2430], px=1890, notch=[59.4,54.6],
      aff=dict(ELAFF), N=41.6935, W=-85.9819, S=41.6766, E=-85.9644, maxb='[41.665,-86.000],[41.705,-85.945]',
      lede='Elkhart, Indiana, grew up on the point where the Elkhart River runs into the St. Joseph. The 1861 county map has its plan in the corner.',
      look=['<b>Main and Second Streets</b>, running down from the point between the rivers. Washington, Jefferson, Jackson, High and Franklin still cross them under their 1861 names.',
            '<b>Pigeon Street</b>, between Jackson and High. It is still there under another name. Fade to today and find what it is called now.',
            '<b>Vistula Street</b>, cutting across the west side on the slant. It is still on today’s map.',
            'The <b>Grist Mill</b> and the <b>Paper Mill</b> at the top of the plan, by the dam on the St. Joseph.',
            'The <b>Michigan Southern &amp; Northern Indiana Railroad</b> and its Goshen branch, and Chapman &amp; Kimball’s addition beside it, with Division and Rail Road Streets.',
            '<b>Water and Sycamore Streets</b> on the point between the two rivers.'],
      how='The plan is shown live from the University of Wisconsin–Milwaukee Libraries’ image service, at full detail. Twenty-four street corners that appear on both maps (Main, Second, Third, Fourth and Fifth, where they meet Sycamore, Washington, Jefferson, Jackson, Pigeon, High and Franklin) were matched by measurement, and the plan was fitted to them. Elkhart’s streets run on a slant to the compass, about twenty degrees, and the 1861 engraver drew them the same way, so the plan hardly turns at all. On average the old corners land within about three yards of the new ones.',
      extra='<p class="note">The title of the county map is printed in the corner of this inset, over open ground; that corner has been cut away so it does not hide today’s streets. The oval stamp at the foot of the plan is the library’s mark on the original.</p>',
      credit=ELKCREDIT.format(inset='Elkhart'), inset='Elkhart',
      og='elkhart', desc='The 1861 plan of Elkhart, Indiana, laid over today’s streets. Fade between them or compare side by side.'),
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
          el.onload=()=>{{ this._place(); this.fire('load'); }}; el.onerror=()=>{{ el.style.display='none'; this.fire('error'); }}; el.src='{url}'; m.getPane('old').appendChild(el); m.on('viewreset zoomend resize',this._place,this); }},
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
def hunt(t,Y):
    v=t.get('hunt')
    if not v: return ''
    n=len(v['h']); slug=t['slug']
    done=('Both found.' if n==2 else 'All three found.')+' The old names are still on the '+Y+' plan, and now you know where they went.' if n>1 else 'Found it. The old name is still on the '+Y+' plan, and now you know where it went.'
    return f"""    <aside class="namehunt" aria-labelledby="nhT" data-k="ps-tn-{slug}" data-word="street" data-words="streets" data-h="{','.join(map(str,v['h']))}" data-yes="{{n}}: that’s the one." data-done="{done}" data-no="Not that one. Fade to today’s streets and look where the old one ran.">
      <p class="nh-k">A challenge · {t['name']}</p>
      <h3 id="nhT">{v['t']}</h3>
      <p>{v['q']}</p>
      <form class="nh-form" autocomplete="off"><label for="nhIn">{v['lab']}</label><input id="nhIn" type="text" maxlength="40" spellcheck="false"><button class="btn" type="submit">Check</button></form>
      <p class="nh-out" aria-live="polite"></p>
      <ol class="nh-found" aria-label="Streets you have found"></ol>
    </aside>
"""
def build(t):
    others=' · '.join(f'<a href="/map/{o["slug"]}/">{o["name"]}</a>' for o in TOWNS if o['slug']!=t['slug'])
    Y=t.get('year','1860')
    nx=TOWNS[(TOWNS.index(t)+1)%len(TOWNS)]
    looks=''.join(f'<li>{x}</li>' for x in t['look'])
    return f'''    <p class="crumb"><a href="/map/">← The map room</a></p>
    <p class="kicker">Then and now</p>
    <h1>{t["name"]}, {Y} and today</h1>
    <p class="lede" style="font-size:1.15rem">{t["lede"]} Here it is laid over the streets of today. Fade between the two, or drag a line across and see one beside the other.</p>
    <p class="note">Other towns: {others} · <a href="/map/then-and-now/">all seven</a></p>
    <p class="note">Drag to move. Scroll, pinch or use the buttons to zoom. The old plan was lined up by hand on street corners that still carry their {Y} names, so it is close but not exact: expect it to be out by a few yards in places.</p>
  <div class="maproom">
    <div class="mapbar tnbar">
      <span class="seg" role="group" aria-label="How to compare">
        <button type="button" class="btn" id="tnFade" aria-pressed="true">Fade</button><button type="button" class="btn" id="tnSwipe" aria-pressed="false">Side by side</button>
      </span>
      <label class="tnrange" id="tnFadeBox"><span>Today</span><input type="range" id="tnOp" min="0" max="100" value="75" aria-label="How much of the {Y} plan to show"><span>{Y}</span></label>
      <button type="button" class="btn" id="tnHome">Back to town</button>
      <button type="button" class="btn" id="tnFull">Full screen</button><button type="button" class="btn" id="tnShare">Share this view</button><button type="button" class="btn" id="tnPrint">Print</button><button type="button" class="btn" id="tnNames" aria-pressed="false" disabled title="Solve this town’s renamed-street challenge to unlock">Today’s names 🔒</button>
      <span class="mapstat" id="tnStat" aria-live="polite">Loading…</span>
    </div>
    <div class="tnwrap">
      <div id="tnMap" class="osd tnmap" role="application" aria-label="The {Y} plan of {t["name"]} laid over a modern street map"></div>
      <div class="tnswipe" id="tnLine" data-year="{Y}" hidden><button type="button" class="tnhandle" id="tnHandle" aria-label="Drag to move the dividing line. Left and right arrow keys also move it."><span aria-hidden="true">◂ ▸</span></button></div>
    </div>
  </div>
    <h2>Things to look for</h2>
    <ul class="dis">{looks}</ul>
{hunt(t,Y)}    <h2>How this was made</h2>
    <p>{t["how"]}</p>
    {t.get("extra","")}
    <p class="note tncredit">{t.get("credit") or CREDIT.format(inset=t["inset"])} Today’s streets and water: drawn from OpenStreetMap data, © OpenStreetMap contributors, available under the Open Database License.</p>
    {('<p class="note">The business directory printed beside this plan is in the roll of names: <a href="/names/?town='+t['slug']+'">who was in '+t['name']+' in '+Y+' →</a></p>') if t['slug'] in ('cassopolis','niles','dowagiac','paw-paw','goshen') else ''}
    <p class="tnnext"><a href="/map/{nx['slug']}/">Next town: {nx['name']}, {nx.get('year','1860')} →</a> <span aria-hidden="true">·</span> <a href="/map/then-and-now/">All seven towns</a></p>
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
        const N={json.dumps(t.get('notch'))};
        const poly=c=>'polygon(0 0,'+N[0]+'% 0,'+N[0]+'% '+N[1]+'%,'+c+'% '+N[1]+'%,'+c+'% 100%,0 100%)';
        if(!swipe){{ img.style.clipPath=N?poly(100):''; return; }}
        const w=wrap.getBoundingClientRect(), r=img.getBoundingClientRect();
        const x=w.left+w.width*frac;
        const cut=Math.min(100,Math.max(0,r.right-x)/(r.width||1)*100);
        const keep=100-cut;
        img.style.clipPath=(N&&keep>N[0])?poly(keep.toFixed(3)):'inset(0 '+cut.toFixed(3)+'% 0 0)';
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
      // full screen: the whole map tool, with the map resized to fit
      const room=document.querySelector('.maproom'), bFull=document.getElementById('tnFull');
      if (!room.requestFullscreen) bFull.hidden=true;
      bFull.onclick=()=>{{ if (document.fullscreenElement) document.exitFullscreen(); else room.requestFullscreen().catch(()=>{{}}); }};
      document.addEventListener('fullscreenchange',()=>{{ const on=!!document.fullscreenElement; room.classList.toggle('isfull',on); bFull.textContent=on?'Leave full screen':'Full screen'; setTimeout(()=>{{ map.invalidateSize(); clip(); }},120); }});
      // share this view: the link carries the zoom and the centre
      const hv=()=>{{ const c=map.getCenter(); return '#'+map.getZoom().toFixed(2)+'/'+c.lat.toFixed(5)+'/'+c.lng.toFixed(5); }};
      document.getElementById('tnShare').onclick=()=>{{ const url=location.origin+location.pathname+hv(); history.replaceState(null,'',hv());
        if (navigator.share && matchMedia('(pointer:coarse)').matches) navigator.share({{title:document.title,url}}).catch(()=>{{}});
        else if (navigator.clipboard) navigator.clipboard.writeText(url).then(()=>{{ stat.textContent='Link to this view copied. It opens the map just here.'; }},()=>prompt('Copy this link:',url)); else prompt('Copy this link:',url); }};
      const fromHash=()=>{{ const m=/^#(\\d+(?:\\.\\d+)?)\\/(-?\\d+\\.\\d+)\\/(-?\\d+\\.\\d+)$/.exec(location.hash); if (m) map.setView([+m[2],+m[3]],+m[1]); }};
      fromHash(); addEventListener('hashchange',fromHash);
      // print: the map as it stands, with its credit line
      document.getElementById('tnPrint').onclick=()=>{{ document.documentElement.classList.add('printmap'); setTimeout(()=>window.print(),150); }};
      addEventListener('afterprint',()=>document.documentElement.classList.remove('printmap'));
      // today's names, the prize for solving the town's challenge: OpenStreetMap's own map, with its street names, under the old plan
      const bNames=document.getElementById('tnNames'), need={len(t.get('hunt',{}).get('h',[]))};
      let osm=null, namesOn=false;
      const solved=()=>{{ try{{ return need>0 && JSON.parse(localStorage.getItem('ps-tn-{t["slug"]}')||'[]').length>=need; }}catch(e){{ return false; }} }};
      const unlock=()=>{{ if (solved()){{ bNames.disabled=false; bNames.title='Show today’s street names under the old plan'; bNames.textContent='Today’s names'; }} }};
      unlock(); document.addEventListener('ps-badge',unlock); document.addEventListener('submit',()=>setTimeout(unlock,50),true);
      bNames.onclick=()=>{{ if (bNames.disabled) return; namesOn=!namesOn; bNames.setAttribute('aria-pressed',String(namesOn));
        if (namesOn){{ if (!osm) osm=L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:19, attribution:'Street names: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}}); osm.addTo(map); osm.bringToBack(); stat.textContent='Today’s names on, from OpenStreetMap. Fade the old plan to read them.'; }}
        else {{ if (osm) map.removeLayer(osm); stat.textContent='Today’s names off.'; }} }};
    }})();
    </script>
'''
FIT={'cassopolis':(19,5),'niles':(43,4),'dowagiac':(33,3),'paw-paw':(30,4),'south-bend':(18,9),'goshen':(40,4),'elkhart':(24,3)}
def hubpage():
    cards=[]; total=0
    for t in TOWNS:
        Y=t.get('year','1860'); n=len(t.get('hunt',{}).get('h',[])); total+=n; c,yd=FIT[t['slug']]
        cards.append(f"""      <li class="tncard"><a href="/map/{t['slug']}/"><img src="/img/thennow/{t['slug']}.webp" width="480" height="320" alt="Part of the {Y} plan of {t['name']}" loading="lazy" decoding="async"><span class="tnc-y">{Y}</span><b>{t['name']}</b></a>
        <span class="tnc-f">Lined up on {c} street corners, within about {yd} yards</span>
        <span class="tnc-s" data-k="ps-tn-{t['slug']}" data-n="{n}">{n} renamed street{'s' if n!=1 else ''} to find</span></li>""")
    body=f"""    <p class="crumb"><a href="/map/">← The map room</a></p>
    <p class="kicker">Then and now</p>
    <h1>Seven towns, then and now</h1>
    <p class="lede" style="font-size:1.15rem">The old town plans of the St. Joseph River Valley, each laid over the streets of today. Fade from one to the other, or drag a line across and see them side by side. In every town, at least one street has changed its name since the plan was engraved. Find them all.</p>
    <p class="tntally" id="tnTally" aria-live="polite">{total} renamed streets in all.</p>
    <p class="note">Find your first and you earn the <a href="/badges/">Street sleuth</a> badge. Find all {total} and you are the hunt’s Town surveyor.</p>
    <ul class="tngrid">
{chr(10).join(cards)}
    </ul>
    <h2>How they were made</h2>
    <p>Each plan was matched to today’s map by measurement, on street corners that appear on both: the corners that still carry their old names, plus the few whose new names we were sure of. The plan was then stretched and turned, as little as it would go, to fit them. Where a street has bent, jogged or been widened since, it was left out of the fit, and each town’s page says which.</p>
    <p class="note">Michigan plans: <i>Map of the Counties of Cass, Van Buren and Berrien, Michigan</i> (1860), Library of Congress. South Bend: M. W. Stokes, <i>Map of St. Joseph Co., Indiana</i> (1863), Library of Congress. Goshen and Elkhart: <i>Map of Elkhart Co. Indiana</i> (1861), American Geographical Society Library, University of Wisconsin–Milwaukee Libraries. All public domain. Today’s streets: © OpenStreetMap contributors.</p>
    <script>
    (function(){{ var sum=0, tot=0; [].forEach.call(document.querySelectorAll('.tnc-s'), function(s){{ var n=+s.dataset.n, got=0; try{{ got=JSON.parse(localStorage.getItem(s.dataset.k)||'[]').length; }}catch(e){{}} tot+=n; sum+=Math.min(got,n); if (got){{ s.textContent=(got>=n?'Solved: ':'')+Math.min(got,n)+' of '+n+' renamed street'+(n!==1?'s':'')+' found'; if (got>=n) s.classList.add('done'); }} }});
      var t=document.getElementById('tnTally'); if (t && sum) t.textContent='You have found '+sum+' of '+tot+' renamed streets.'+(sum>=tot?' Every one. Well done.':''); }})();
    </script>
"""
    page('map/then-and-now/index.html','Seven towns, then and now · Project Scroll','Seven old town plans of the St. Joseph River Valley, from Cassopolis to South Bend, Goshen and Elkhart, laid over today’s streets, each with a renamed street to find.',body,og='https://projectscroll.com/og/then-and-now.jpg')

for t in TOWNS:
    page(f'map/{t["slug"]}/index.html', f'{t["name"]}, {t.get("year","1860")} and today · Project Scroll', t['desc'], build(t), og=f'https://projectscroll.com/og/{t["og"]}.jpg')
hubpage()
print('then-and-now built:', ', '.join(t['name'] for t in TOWNS))
