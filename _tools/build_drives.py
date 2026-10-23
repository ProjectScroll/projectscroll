"""History drives: /drives/ and one page per drive, stop by stop, with a map and directions.
python3 _tools/build_drives.py   (data: _tools/data/drives.json)"""
import sys, pathlib, json, html, re, urllib.parse
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
import basemap
E = html.escape
P = pathlib.Path(__file__).parent/'data'
D = json.load(open(P/'drives.json'))
def hrs(m):
    h, mm = divmod(int(m), 60)
    return (f'{h} hr ' if h else '') + (f'{mm} min' if mm else '').strip()
def gm(stops):
    pts = [f'{s["lat"]},{s["lon"]}' for s in stops if s.get('lat')]
    if not pts: return ''
    q = 'https://www.google.com/maps/dir/?api=1&travelmode=driving&destination=' + urllib.parse.quote(pts[-1])
    if len(pts) > 1: q += '&waypoints=' + '%7C'.join(urllib.parse.quote(x) for x in pts[:-1][:9])
    return q
def link(s):
    return f' <a href="{E(s["link"])}">More on Project Scroll ›</a>' if s.get('link') else ''
def srcs(d):
    xs = d.get('sources') or []
    return ''.join(f'<li>{E(x["cite"])} <a href="{E(x["url"])}" rel="noopener">link</a></li>' if x.get('url') else f'<li>{E(x["cite"])}</li>' for x in xs)

MAPJS = basemap.BASE_JS + r'''
(function(){
  var box=document.getElementById('drMap'); if (!box) return; var S=JSON.parse(box.dataset.s);
  var start=function(){ if (box._m || !window.L) return; box.innerHTML='';
    var map=L.map(box,{scrollWheelZoom:false}); box._m=map; map.attributionControl.setPrefix(false);
    window.psBase(map, box, document.getElementById('drBase'), 'topo');
    var line=L.polyline(S.map(function(s){ return [s[1],s[2]]; }),{color:'#C06A1A', weight:4, opacity:.85, dashArray:'8 6'}).addTo(map);
    S.forEach(function(s,i){ L.marker([s[1],s[2]],{icon:L.divIcon({className:'wk-pin', html:'<span>'+(i+1)+'</span>', iconSize:[26,26]}), title:'Stop '+(i+1)+': '+s[0]}).addTo(map)
      .on('click',function(){ var el=document.getElementById('stop-'+(i+1)); if (el) el.scrollIntoView({behavior:'smooth'}); }); });
    map.fitBounds(line.getBounds().pad(.12));
    map.on('focus click',function(){ map.scrollWheelZoom.enable(); }); };
  var need=function(){ if (window.L){ start(); return; } var l=document.createElement('link'); l.rel='stylesheet'; l.href='/vendor/leaflet-1.9.4/leaflet.css?v=1'; document.head.appendChild(l);
    var s=document.createElement('script'); s.src='/vendor/leaflet-1.9.4/leaflet.js?v=1'; s.onload=start; document.head.appendChild(s); };
  if ('IntersectionObserver' in window){ var io=new IntersectionObserver(function(e){ if (e.some(function(x){ return x.isIntersecting; })){ io.disconnect(); need(); } },{rootMargin:'300px'}); io.observe(box); } else need();
})();'''

cards = []
for i, d in enumerate(D):
    st = [s for s in d['stops'] if s.get('lat')]
    S = json.dumps([[s['name'], s['lat'], s['lon']] for s in st], ensure_ascii=False)
    stops = ''.join(f'''      <li class="dr-stop" id="stop-{k+1}"><h3><span class="dr-n">{k+1}</span> {E(s["name"])}</h3>
        <p class="dr-ad">{E(s.get("address",""))}</p>
        <p>{E(s.get("see",""))}</p>
        <p class="dr-open"><b>Open:</b> {E(s.get("open","") or "Check before you go.")}</p>
        <p class="dr-acts"><a href="https://www.google.com/maps/dir/?api=1&amp;destination={s["lat"]},{s["lon"]}" rel="noopener">Directions to this stop</a>{link(s)}</p>
        {f'<p class="note">Source: {E(s["source"])}</p>' if s.get("source") and not str(s["source"]).startswith("http") else (f'<p class="note"><a href="{E(s["source"])}" rel="noopener">Source</a></p>' if s.get("source") else "")}</li>
''' for k, s in enumerate(d['stops']) if s.get('lat') or True)
    body = f'''    <p class="crumb"><a href="/drives/">← History drives</a></p>
    <p class="kicker">A history drive · about {d["miles"]} miles · about {hrs(d["minutes"])} of driving</p>
    <h1>{E(d["title"])}</h1>
    <p class="lede">{E(d["intro"])}</p>
    <p class="ctas"><a class="btn primary" href="{gm(st)}" rel="noopener">Open the whole drive in Google Maps</a> <a class="btn" href="#stop-1">Start at stop 1</a></p>
    <figure class="mu-mapf"><div class="mu-map dr-map" id="drMap" data-s="{E(S)}" role="region" aria-label="Map of the drive. Every stop is also listed below."><p class="mu-mapph">The map opens here.</p></div>
      <figcaption class="vm-key">{basemap.buttons("topo","drBase")} The numbers follow the stops below. The dashed line joins the stops in order; it is not the road route.</figcaption></figure>
    <p class="note">{E(d.get("route_note",""))}</p>
    <h2>The stops</h2>
    <ol class="dr-stops">
{stops}    </ol>
    <h2>Food and rest stops</h2>
    <p>{E(d.get("food",""))}</p>
    <h2>Before you go</h2>
    <ul class="dis"><li>Hours change and some stops are by appointment: check each place before you set out.</li><li>Stops marked “view from the road” are on private or working property: please stay on the road.</li><li>Distances and times are road distances, rounded, without time spent at the stops.</li></ul>
    <h2>Sources</h2>
    <ul class="nw-src">{srcs(d)}</ul>
    <p class="ctas"><a class="btn" href="/drives/">All the drives</a> <a class="btn" href="/valley-map/">The valley map</a> <a class="btn" href="/visit/">Plan a day out</a></p>
<script>{MAPJS}</script>
'''
    page(f'drives/{d["slug"]}/index.html', f'{d["title"]} · a history drive · Project Scroll', (d['intro'][:150].rsplit(' ', 1)[0] + '…'), body)
    cards.append(f'<li class="dr-card"><a href="/drives/{d["slug"]}/"><b>{E(d["title"])}</b><span class="dr-meta">{len(d["stops"])} stops · about {d["miles"]} miles · about {hrs(d["minutes"])}</span><span>{E(d["intro"][:180].rsplit(" ",1)[0])}…</span></a></li>')

hub = f'''    <p class="crumb"><a href="/visit/">← Visit &amp; Plan</a></p>
    <p class="kicker">Get in the car</p>
    <h1>History drives</h1>
    <p class="lede">Four self-guided drives through the St. Joseph River valley, stop by stop, with what to see at each one, when it is open, and directions. Every stop is a public place: a museum, a park, a marker, a courthouse, or a building you can see from the road.</p>
    <ul class="dr-cards">{''.join(cards)}</ul>
    <p class="ctas"><a class="btn" href="/valley-map/">See the drives on the valley map</a> <a class="btn" href="/visit/">Plan a day out</a></p>
'''
page('drives/index.html', 'History drives · Project Scroll', 'Four self-guided history drives through the St. Joseph River valley: the Underground Railroad road, the fruit belt, the county seats and the makers’ road.', hub)
print('drives built', len(D))
