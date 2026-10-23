"""The Valley map: every place on the site with a pin, on one map, in layers you can switch on and off.
python3 _tools/build_valleymap.py   (reads museums, food, seasons, walks, lost towns, town plans, and drives/outdoors when present)"""
import sys, pathlib, json, re, html
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E = html.escape
P = pathlib.Path(__file__).parent/'data'
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def load(n, d=None):
    f = P/n
    return json.load(open(f)) if f.exists() else d

pts = []   # [layer, name, kind, town, lat, lon, href, extra]
def add(layer, name, kind, town, ll, href, extra=''):
    if not ll: return
    pts.append([layer, name, kind, town, round(float(ll[0]),5), round(float(ll[1]),5), href, extra])

# museums & historic places (ids as build_museums.py makes them)
KIND = {'museum':'Museum','historic site':'Historic site','historic house':'Historic house','historical society':'Historical society','archive':'Archive','library local history':'Library local-history room','library':'Library'}
used = set()
for d in load('museums.json', []):
    s = slug(d['name'])
    if s in used: s = slug(d['name']+' '+d['town'])
    used.add(s)
    add('museum', d['name'], KIND.get(d['kind'], d['kind']), d['town'], d.get('ll'), f'/museums/#{s}', d.get('what','')[:140])

# places to eat and stay (ids as build_food.py makes them)
used = set()
for d in [x for x in load('food.json', []) if x.get('keep', True)]:
    s = slug(d['name']+' '+d['town']) if slug(d['name']) in used else slug(d['name']); used.add(s)
    ty = 'eat' if d['type']=='restaurant' else 'stay'
    add(ty, d['name'], (d.get('kind') or '').capitalize(), d['town'], d.get('ll'), f'/food/{ty}/#{s}', (d.get('what') or '')[:140])

# festivals and seasons
MON = ['','January','February','March','April','May','June','July','August','September','October','November','December']
for d in load('seasons.json', []):
    add('fest', d['name'], d.get('when') or MON[d.get('month') or 0], d['town'], d.get('ll'), f'/seasons/#{slug(d["name"])}', str(d.get('month') or ''))
    if d.get('dates2026') and d.get('ll'): pts[-1] += [d['dates2026']['start'], d['dates2026'].get('end') or d['dates2026']['start']]

# the two virtual walks
w = load('walk.json', {})
for s in w.get('stops', []): add('walk', s['name'], 'Broadway walk stop', 'Cassopolis', (s['lat'], s['lon']), f'/walk/#{s["id"]}')
w = load('walk-dowagiac.json', {})
for s in w.get('stops', []): add('walk', s['name'], 'Front Street walk stop', 'Dowagiac', (s['lat'], s['lon']), f'/walk/dowagiac/#{s["id"]}')

# lost towns (read from build_lost.py so the two never drift)
src = (pathlib.Path(__file__).parent/'build_lost.py').read_text(encoding='utf-8')
for m in re.finditer(r"dict\(n='([^']*)',(.*?)ll=\(([-\d.]+),\s*([-\d.]+)\)", src, re.S):
    n = m.group(1); sid = re.sub(r'[^a-z]+','-', n.lower().split(',')[0].split(' and ')[0]).strip('-')
    add('lost', n, 'Lost town', '', (m.group(3), m.group(4)), f'/lost-towns/#{sid}')

# the old town plans, laid over today's streets
PLANS = [('cassopolis','Cassopolis, 1860',41.9117,-86.0097),('niles','Niles, 1860',41.8298,-86.2541),('dowagiac','Dowagiac, 1860',41.9842,-86.1086),
         ('paw-paw','Paw Paw, 1860',42.2178,-85.8911),('south-bend','South Bend, 1863',41.6764,-86.2520),('goshen','Goshen, 1861',41.5823,-85.8345),('elkhart','Elkhart, 1861',41.6820,-85.9767)]
for k, n, la, lo in PLANS: add('plan', n, 'Old town plan over today’s streets', n.split(',')[0], (la, lo), f'/map/{k}/')

# outdoors and drives, when their data exists
o = load('outdoors.json', {})
for d in (o.get('places') or []):
    add('out', d['name'], d.get('category',''), d.get('town',''), (d.get('lat'), d.get('lon')) if d.get('lat') else None, '/outdoors/#'+slug(d['name']), (d.get('do') or '')[:140])
for d in (o.get('upick') or []):
    add('out', d['name'], 'U-pick: '+(d.get('fruit') or ''), d.get('town',''), (d.get('lat'), d.get('lon')) if d.get('lat') else None, '/outdoors/#'+slug(d['name']), d.get('months',''))
for dr in (load('drives.json', []) or []):
    for i, s in enumerate(dr.get('stops', [])):
        add('drive', s['name'], f'{dr["title"]}, stop {i+1}', '', (s.get('lat'), s.get('lon')) if s.get('lat') else None, f'/drives/{dr["slug"]}/#stop-{i+1}')

LAYERS = [('museum','Museums &amp; historic places','#B8892A'),('eat','Places to eat','#B3362B'),('stay','Places to stay','#7A4E9C'),
          ('fest','Festivals &amp; seasons','#3F7F4A'),('walk','Walk stops','#2F6FA0'),('lost','Lost towns','#6F6A60'),('plan','Old town plans','#8A5A2B'),
          ('out','Outdoors &amp; u-pick','#1F8A8A'),('drive','Drive stops','#C06A1A')]
cnt = {k: sum(1 for p in pts if p[0]==k) for k, _, _ in LAYERS}
LAY = [l for l in LAYERS if cnt[l[0]]]
chips = ''.join(f'<button type="button" class="vm-chip" data-l="{k}" aria-pressed="true"><i style="background:{c}"></i>{t} <span>{cnt[k]}</span></button>' for k, t, c in LAY)
DATA = json.dumps(pts, ensure_ascii=False, separators=(',',':'))
COL = json.dumps({k: c for k, _, c in LAY})
N = len(pts)

body = f'''    <p class="crumb"><a href="/visit/">← Visit &amp; Plan</a></p>
    <p class="kicker">The whole valley, on one map</p>
    <h1>The valley map</h1>
    <p class="lede">Every place on Project Scroll that has a pin: {cnt.get('museum',0)} museums and historic places, {cnt.get('eat',0)+cnt.get('stay',0)} places to eat and stay, {cnt.get('fest',0)} festivals, the walk stops, the lost towns and the old town plans. Switch the layers on and off, find what is near you, and open any pin for its story.</p>
    <div class="vm-bar" role="group" aria-label="Map layers">{chips}</div>
    <div class="vm-tools">
      <label class="vm-q"><span class="sr">Find a place</span><input type="search" id="vmQ" placeholder="Find a place or town" autocomplete="off"></label>
      <button type="button" class="btn" id="vmMonth" aria-pressed="false">Festivals this month only</button>
      <button type="button" class="btn" id="vmNear">Near me</button>
      <button type="button" class="btn" id="vmOSM" aria-pressed="false" hidden>Show today’s streets</button>
      <button type="button" class="btn" id="vmHome" hidden>Whole valley</button>
      <span class="vm-stat" id="vmStat" aria-live="polite"></span>
    </div>
    <figure class="mu-mapf">
      <div class="mu-map vm-map" id="vmMap" role="region" aria-label="Map of every place on the site. Every place is also in the list below.">
        <p class="mu-mapph">The map opens here, with {N} pins.</p>
      </div>
      <figcaption class="vm-key">Pins sit at each place’s street address; a few sit at the town. Press a pin for its story and a link.</figcaption>
    </figure>
    <h2 id="vmListH">The places <span class="mu-n" id="vmN"></span></h2>
    <ol class="vm-list" id="vmList"></ol>
    <p class="note">Map pins come from each street address. County lines: US Census Bureau; rivers: USGS. Only if you press “Show today’s streets” does your browser ask OpenStreetMap’s tile server for street maps, under <a href="https://osmfoundation.org/wiki/Privacy_Policy" rel="noopener">its privacy policy</a>. “Near me” asks your browser for your location and uses it only on this page. Hours and dates change: check each place before you go.</p>
    <p class="ctas"><a class="btn primary" href="/visit/">Plan a day out</a> <a class="btn" href="/museums/">Museums</a> <a class="btn" href="/food/">Food &amp; lodging</a> <a class="btn" href="/seasons/">Festivals</a></p>
<script>
(function(){{
  var P={DATA}, COL={COL}, $=function(s){{ return document.querySelector(s); }};
  var box=$('#vmMap'), stat=$('#vmStat'), list=$('#vmList'), q=$('#vmQ'), on={{}}, month=false, near=null, map=null, marks=[];
  var calm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  [].forEach.call(document.querySelectorAll('.vm-chip'),function(b){{ on[b.dataset.l]=true;
    b.addEventListener('click',function(){{ on[b.dataset.l]=!on[b.dataset.l]; b.setAttribute('aria-pressed',String(on[b.dataset.l])); draw(); }}); }});
  var thisMonth=new Date().getMonth()+1, today=null;
  var iso=function(d){{ return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2); }};
  if (location.hash==='#today'){{ var t0=new Date(), wd=t0.getDay(), t1=new Date(t0); t1.setDate(t0.getDate()+(wd>=5||wd===0? (7-wd)%7 : 6-wd+1));
    var a=iso(t0), z=iso(t1), hits=P.filter(function(p){{ return p[0]==='fest' && p[8] && p[8]<=z && p[9]>=a; }});
    if (hits.length){{ today=hits; Object.keys(on).forEach(function(k){{ on[k]=(k==='fest'); }}); [].forEach.call(document.querySelectorAll('.vm-chip'),function(b){{ b.setAttribute('aria-pressed',String(on[b.dataset.l])); }});
      var m=document.createElement('p'); m.className='vm-today'; m.textContent='On now and coming up through '+t1.toLocaleDateString('en-US',{{weekday:'long',month:'long',day:'numeric'}})+': '+hits.length+(hits.length===1?' event':' events')+'. Turn the other layers on to see what is near them.'; $('.vm-bar').before(m); }} }}
  $('#vmMonth').addEventListener('click',function(){{ month=!month; this.setAttribute('aria-pressed',String(month)); draw(); }});
  q.addEventListener('input',function(){{ draw(); }});
  var km=function(a,b){{ var r=Math.PI/180, dl=(b[0]-a[0])*r, dn=(b[1]-a[1])*r, h=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a[0]*r)*Math.cos(b[0]*r)*Math.sin(dn/2)*Math.sin(dn/2); return 12742*Math.asin(Math.sqrt(h)); }};
  var vis=function(p){{ if (!on[p[0]]) return false; if (today && p[0]==='fest' && today.indexOf(p)<0) return false; if (month && p[0]==='fest' && String(p[7])!==String(thisMonth)) return false;
    var t=q.value.trim().toLowerCase(); if (t && (p[1]+' '+p[3]+' '+p[2]).toLowerCase().indexOf(t)<0) return false; return true; }};
  var esc=function(s){{ var d=document.createElement('div'); d.textContent=s; return d.innerHTML; }};
  var draw=function(){{ var v=P.filter(vis);
    if (near) v.forEach(function(p){{ p.d=km(near,[p[4],p[5]]); }}), v.sort(function(a,b){{ return a.d-b.d; }});
    else v.sort(function(a,b){{ return (a[3]||'~').localeCompare(b[3]||'~') || a[1].localeCompare(b[1]); }});
    $('#vmN').textContent=v.length+(v.length===1?' place':' places');
    list.innerHTML=v.slice(0,400).map(function(p){{ var d=near? '<span class="vm-d">'+(p.d*0.621371<10?(p.d*0.621371).toFixed(1):Math.round(p.d*0.621371))+' mi</span>':'';
      return '<li><i style="background:'+COL[p[0]]+'"></i><a href="'+p[6]+'">'+esc(p[1])+'</a> <span class="vm-k">'+esc(p[2])+(p[3]?' · '+esc(p[3]):'')+'</span>'+d+'</li>'; }}).join('');
    if (map) {{ marks.forEach(function(m){{ var s=vis(m.p); if (s && !map.hasLayer(m.c)) m.c.addTo(map); if (!s && map.hasLayer(m.c)) map.removeLayer(m.c); }}); }}
    stat.textContent=v.length+' showing'; }};
  $('#vmNear').addEventListener('click',function(){{ var b=this; if (!navigator.geolocation){{ stat.textContent='This browser cannot share a location.'; return; }}
    stat.textContent='Finding you…'; navigator.geolocation.getCurrentPosition(function(g){{ near=[g.coords.latitude,g.coords.longitude]; b.setAttribute('aria-pressed','true'); draw();
      if (map){{ if (window._me) map.removeLayer(window._me); window._me=L.circleMarker(near,{{radius:8,className:'vm-me'}}).addTo(map).bindTooltip('You are here'); map.setView(near,11,{{animate:!calm}}); }}
      $('#vmListH').scrollIntoView({{behavior:calm?'auto':'smooth'}}); }}, function(){{ stat.textContent='No location shared. The list is sorted by town.'; }}, {{timeout:10000}}); }});
  var start=function(){{ if (map || !window.L) return;
    [].forEach.call(document.querySelectorAll('.mu-mapph'),function(x){{ x.remove(); }});
    map=L.map(box,{{zoomSnap:.25, minZoom:7, maxZoom:17, scrollWheelZoom:false, maxBounds:[[40.9,-87.9],[42.95,-84.3]]}});
    map.attributionControl.setPrefix(false); map._home=L.latLngBounds([[41.42,-86.95],[42.43,-85.35]]); map.fitBounds(map._home);
    map.on('focus click',function(){{ map.scrollWheelZoom.enable(); }}); map.on('blur mouseout',function(){{ map.scrollWheelZoom.disable(); }});
    fetch('/museums/base.json?v=1').then(function(r){{ return r.json(); }}).then(function(b){{ var pane=map.createPane('base'); pane.style.zIndex=250;
      b.c.forEach(function(c){{ c.r.forEach(function(r){{ L.polygon(r.map(function(p){{ return [p[1],p[0]]; }}),{{pane:'base', className:c.d?'mu-cty in':'mu-cty', interactive:false}}).addTo(map); }}); }});
      b.v.forEach(function(l){{ L.polyline(l.map(function(p){{ return [p[1],p[0]]; }}),{{pane:'base', className:'mu-rv', interactive:false}}).addTo(map); }});
      map.attributionControl.addAttribution('County lines: US Census Bureau · Rivers: USGS'); }}).catch(function(){{}});
    P.forEach(function(p){{ var c=L.circleMarker([p[4],p[5]],{{radius:6, color:'#1d2733', weight:1.2, fillColor:COL[p[0]], fillOpacity:.92, bubblingMouseEvents:false}});
      var div=document.createElement('div'); div.className='mu-pop';
      div.innerHTML='<p><b>'+esc(p[1])+'</b><br><small>'+esc(p[2])+(p[3]?' · '+esc(p[3]):'')+'</small></p>'+(p[0]!=='fest'&&p[7]?'<p><small>'+esc(p[7])+'</small></p>':'')+'<p><a href="'+p[6]+'">Read more ›</a></p>';
      c.bindPopup(div,{{maxWidth:260}}); c.bindTooltip(p[1],{{direction:'top', offset:[0,-6]}}); marks.push({{p:p, c:c}}); }});
    draw();
    var osm=null, sb=$('#vmOSM'); sb.hidden=false; sb.addEventListener('click',function(){{ var o=sb.getAttribute('aria-pressed')!=='true'; sb.setAttribute('aria-pressed',String(o));
      if (o){{ if (!osm) osm=L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:19, attribution:'Streets: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}}); osm.addTo(map); box.classList.add('osm'); }}
      else {{ map.removeLayer(osm); box.classList.remove('osm'); }} }});
    $('#vmHome').hidden=false; $('#vmHome').addEventListener('click',function(){{ map.fitBounds(map._home); }}); }};
  var need=function(){{ if (window.L){{ start(); return; }} if (need.on) return; need.on=1;
    var l=document.createElement('link'); l.rel='stylesheet'; l.href='/vendor/leaflet-1.9.4/leaflet.css?v=1'; document.head.appendChild(l);
    var s=document.createElement('script'); s.src='/vendor/leaflet-1.9.4/leaflet.js?v=1'; s.onload=start; s.onerror=function(){{ stat.textContent='The map could not load. The list below has every place.'; }}; document.head.appendChild(s); }};
  if ('IntersectionObserver' in window){{ var io=new IntersectionObserver(function(e){{ if (e.some(function(x){{ return x.isIntersecting; }})){{ io.disconnect(); need(); }} }},{{rootMargin:'300px'}}); io.observe(box); }} else need();
  draw();
}})();
</script>
'''
page('valley-map/index.html', 'The valley map · every place on one map · Project Scroll',
     f'One map of the St. Joseph River valley with {N} places: museums and historic places, places to eat and stay, festivals, walk stops, lost towns and old town plans. Switch layers on and off and find what is near you.',
     body, og='https://projectscroll.com/og/valley-map.jpg?v=1')
print('valley map built', N, cnt)

# ---------- the home-page tile's live data: the dated festivals, placed on the tile picture ----------
import math as _m
_W, _H, _lat0, _lat1, _lon0, _lon1 = 960, 540, 41.45, 42.42, -86.95, -85.35
_k = _m.cos(_m.radians(41.95)); _sc = min(_W/((_lon1-_lon0)*_k), _H/(_lat1-_lat0)); _cx = (_lon0+_lon1)/2; _cy = (_lat0+_lat1)/2
def _xy(la, lo): return (round((_W/2+(lo-_cx)*_k*_sc)/_W*100, 2), round((_H/2-(la-_cy)*_sc)/_H*100, 2))
_ev = []
for d in load('seasons.json', []):
    dt = d.get('dates2026')
    if not dt: continue
    x, y = _xy(*d['ll']) if d.get('ll') else (None, None)
    _ev.append([d['name'], d['town'], dt['start'], dt.get('end') or dt['start'], x if x is not None and 0 <= x <= 100 else None, y if y is not None and 0 <= y <= 100 else None, slug(d['name'])])
_mu = [[d['oh'], d.get('tz') or 'E'] for d in load('museums.json', []) if d.get('oh')]
open(pathlib.Path(__file__).parent.parent/'valley-map'/'today.json', 'w').write(json.dumps({'n': N, 'ev': _ev, 'mu': _mu}, ensure_ascii=False, separators=(',',':')))
print('valley map tile data', len(_ev))
