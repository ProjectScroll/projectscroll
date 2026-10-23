"""Outdoors & water (beaches, parks, trails, paddling, u-pick, the wine trail, fall and winter) and Getting here.
python3 _tools/build_outdoors.py   (data: _tools/data/outdoors.json)"""
import sys, pathlib, json, re, html, urllib.parse
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
import pages as _pg
E = html.escape
D = json.load(open(pathlib.Path(__file__).parent/'data'/'outdoors.json'))
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def link(u, t): return f'<a href="{E(u)}" rel="noopener">{t}</a>' if u else ''
def dirs(name, addr, ll):
    if ll and ll[0]: q = f'{ll[0]},{ll[1]}'
    elif addr and re.match(r'^\d', addr): q = name+', '+addr
    else: return ''
    return '<a href="https://www.google.com/maps/dir/?api=1&destination='+urllib.parse.quote(q)+'" rel="noopener">Directions</a>'
def clean_addr(a):
    return re.sub(r'\s*\((?:no street|county’s|county\'s|address from|from PickYourOwn)[^)]*\)', '', a or '').strip()

GROUPS = [('beach', 'Beaches and lake access', 'Lake Michigan’s sand and the inland lakes’ swimming beaches. Michigan state parks need a Recreation Passport on the car; Indiana state parks charge at the gate.',
           lambda c: c.startswith('Beach') or 'swimming beach' in c or 'lake access' in c or 'Public lake' in c),
          ('parks', 'Parks, forests and nature centers', 'Old-growth woods, dunes, a dark-sky park, botanical gardens and nature centers with trails for every season.',
           lambda c: c.startswith(('State park','County park','Nature','Botanical','City park'))),
          ('trails', 'Trails to walk and ride', 'Rail-trails on old railroad beds and riverwalks along the St. Joseph and Elkhart rivers.',
           lambda c: c.startswith('Trail')),
          ('water', 'Paddling and the rivers', 'Water trails on the St. Joseph, Dowagiac, Paw Paw and Galien rivers, and the liveries and launches that put you on them.',
           lambda c: c.startswith(('Paddling','Public river')))]
used = set()
def card(x):
    s = slug(x['name']); s = s if s not in used else slug(x['name']+' '+x.get('town','')); used.add(s)
    ll = (x.get('lat'), x.get('lon')) if x.get('lat') else None
    llat = f' data-ll="{x["lat"]},{x["lon"]}"' if ll else ''
    closed = 'CLOSED' in (x.get('season') or '')
    rows = ''.join(f'<p class="od-r"><b>{k}</b> {E(v)}</p>' for k, v in [('When:', x.get('season')), ('Cost:', x.get('fee')), ('Dogs:', x.get('dogs')), ('Access:', x.get('access'))] if v and v not in ('—', 'Not stated.'))
    hist = f'<p class="od-h"><b>The story:</b> {E(x["history"])}{(" "+link(x.get("history_source"), "Source")) if x.get("history_source") else ""}</p>' if x.get('history') else ''
    acts = ' · '.join(a for a in [link(x.get('url'), 'Official page'), dirs(x['name'], clean_addr(x.get('address')), ll)] if a)
    return (f'<li class="mu od{" od-closed" if closed else ""}" id="{s}"{llat} data-n="{E(x["name"])}">'
            f'<p class="mu-k">{E(x.get("category",""))} · {E(x.get("town",""))}{", "+E(x["state"]) if x.get("state") else ""}{" · <b class=od-x>Closed this season</b>" if closed else ""}</p>'
            f'<h3>{E(x["name"])}</h3><p>{E(x.get("do",""))}</p>{rows}{hist}'
            f'<p class="od-a">{E(clean_addr(x.get("address")))}</p><p class="mu-acts">{acts}</p></li>')
secs = ''
for k, t, sub, f in GROUPS:
    xs = [x for x in D['places'] if f(x.get('category',''))]
    if not xs: continue
    secs += f'    <section class="od-s" id="{k}" aria-labelledby="h-{k}"><h2 id="h-{k}">{t} <span class="mu-n">{len(xs)}</span></h2><p class="se-sub">{sub}</p><ul class="mu-list od-list">{"".join(card(x) for x in xs)}</ul></section>\n'

def upcard(x):
    s = slug(x['name']); used.add(s)
    unv = 'PickYourOwn' in (x.get('source') or '') or 'UNVERIFIED' in (x.get('notes') or '')
    ll = (x.get('lat'), x.get('lon')) if x.get('lat') else None
    acts = ' · '.join(a for a in [link(x.get('url'), 'Farm’s page'), dirs(x['name'], clean_addr(x.get('address')), ll)] if a)
    return (f'<li class="mu od" id="{s}"{(" data-ll=\"%s,%s\"" % ll) if ll else ""} data-n="{E(x["name"])}"><p class="mu-k">U-pick · {E(x.get("town",""))}{" · <b class=od-x>Check before you go</b>" if unv else ""}</p>'
            f'<h3>{E(x["name"])}</h3><p><b>What to pick:</b> {E(x.get("fruit",""))}</p><p class="od-r"><b>When:</b> {E(x.get("months",""))}</p>'
            f'<p class="od-a">{E(clean_addr(x.get("address")))}</p><p class="mu-acts">{acts}</p></li>')
W = D['wine']
wine = ''.join(f'<li><b>{E(r["name"])}</b>, {E(clean_addr(r.get("address")))}{(" · "+link(r.get("url"),"Website")) if r.get("url") else ""}</li>' for r in W.get('rooms', []))
FW = D.get('fall_and_winter', {})
fall = ''.join(f'<li><b>{E(r["name"])}.</b> {E(r["route"])}</li>' for r in FW.get('drives', []))
wn = FW.get('winter', {})
ski = ''.join(f'<li>{E(s)}</li>' for s in wn.get('cross_country_ski', []))
sled = ''.join(f'<li>{E(s)}</li>' for s in wn.get('sledding_tubing', []))
meta = D.get('meta', {})

body = f'''    <p class="crumb"><a href="/visit/">← Visit &amp; Plan</a></p>
    <p class="kicker">Outdoors &amp; water</p>
    <h1>Beaches, rivers, trails and orchards</h1>
    <p class="lede">The valley is made of water: Lake Michigan on one side, the St. Joseph River through the middle, and lakes in every township. Here are the public beaches, parks, rail-trails and water trails, the u-pick orchards and the wine trail, with when to go, what it costs and whether the dog can come.</p>
    <nav class="cm-nav" aria-label="On this page"><a href="#beach">Beaches</a> · <a href="#parks">Parks &amp; nature</a> · <a href="#trails">Trails</a> · <a href="#water">Paddling</a> · <a href="#upick">U-pick</a> · <a href="#wine">Wine trail</a> · <a href="#seasons">Fall &amp; winter</a> · <a href="/valley-map/">On the valley map</a></nav>
{secs}    <section class="od-s" id="upick" aria-labelledby="h-up"><h2 id="h-up">U-pick orchards and berry farms <span class="mu-n">{len(D["upick"])}</span></h2>
      <p class="se-sub">The fruit belt in season: strawberries in June, cherries and blueberries in July, peaches in August, apples and pumpkins in the fall. Picking days depend on the weather, so call or check the farm’s page the morning you go.</p>
      <ul class="mu-list od-list">{"".join(upcard(x) for x in D["upick"])}</ul>
      <p class="note">More farm markets, cider mills and orchards with a story are on <a href="/food/eat/">Places to eat</a> (choose “Orchards, markets &amp; cider”).</p></section>
    <section class="od-s" id="wine" aria-labelledby="h-w"><h2 id="h-w">The Lake Michigan Shore Wine Trail</h2>
      <p>{E(W.get("summary",""))} The trail’s own page lists every member: {link(W.get("trail_url"), "Lake Michigan Shore Wine Trail")}. A few tasting rooms:</p>
      <ul class="dis">{wine}</ul>
      <p class="note">Please choose a driver. Tasting-room hours change with the season.</p></section>
    <section class="od-s" id="seasons" aria-labelledby="h-fw"><h2 id="h-fw">Fall color and winter</h2>
      <h3>Fall color drives</h3><ul class="dis">{fall}</ul>
      <p class="note">Color usually peaks around the middle of October. Routes from Visit Southwest Michigan’s Fall Color Guide and the County Road Association of Michigan.</p>
      <h3>Cross-country skiing and snowshoeing</h3><ul class="dis">{ski}</ul>
      <h3>Sledding and tubing</h3><ul class="dis">{sled}</ul>
      <p>{E(wn.get("night_skies",""))}</p></section>
    <h2>Before you go</h2>
    <ul class="dis">
      <li><b>Passes.</b> {E(meta.get("recreation_passport",""))}</li>
      <li><b>Indiana state parks.</b> {E(meta.get("indiana_state_parks",""))}</li>
      <li><b>Public land only.</b> Every place here is open to the public. Please keep to paths and posted hours, and leave private shores and farm fields alone.</li>
      <li><b>Lake Michigan.</b> Watch the beach flags and the forecast: rip currents along the piers are real. Never walk the piers in high waves.</li>
    </ul>
    <p class="note">Gathered and checked against each park’s, farm’s or agency’s own page in October 2026. Fees, hours and dog rules change; a farm marked “check before you go” was confirmed only from a listing site. Map pins come from each street address.</p>
    <p class="ctas"><a class="btn primary" href="/valley-map/">See them on the valley map</a> <a class="btn" href="/getting-here/">Getting here</a> <a class="btn" href="/visit/">Plan a day out</a></p>
'''
items = [{"@type": "TouristAttraction", "name": x['name'], "url": "https://projectscroll.com/outdoors/", "description": x.get('do','')} for x in D['places']]
_pg.EXTRA['outdoors/index.html'] = {"mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [{"@type": "ListItem", "position": i+1, "item": it} for i, it in enumerate(items)]}}
page('outdoors/index.html', 'Outdoors & water: beaches, trails, paddling and u-pick · Project Scroll',
     f'{len(D["places"])} public beaches, parks, nature centers, rail-trails and water trails in the St. Joseph River valley, plus u-pick orchards, the Lake Michigan Shore Wine Trail, fall color drives and winter sledding.',
     body, og='https://projectscroll.com/og/food.jpg?v=1')

# ---------- getting here ----------
G = D['getting_here']
def tr(rows): return ''.join(rows)
air = ''.join(f'<li><b>{E(a["name"])} ({E(a["code"])})</b>, about {a["to_cassopolis"]["miles"]} miles, {E(a["to_cassopolis"]["time"])} by car to Cassopolis. {E(a.get("notes",""))} {link(a.get("url"), "Airport site")}</li>' for a in G.get('air', []))
rail = ''.join(f'<li><b>{E(r["name"])}</b>{(" ("+E(r["code"])+")") if r.get("code") else ""}: {E(r.get("routes",""))}. {E(r.get("notes","")) if "verify" not in (r.get("notes") or "") else ""} {link(r.get("url"), "Station page")}</li>' for r in G.get('rail', []) if 'verify' not in (r.get('notes') or ''))
bus = ''.join(f'<li><b>{E(b["name"])}</b>, {E(b["address"])}. {E(b.get("notes",""))}</li>' for b in G.get('bus', []))
drive = ''.join(f'<tr><td>{E(d["from"])}</td><td>{d["miles"]}</td><td>{E(d["time"])}</td></tr>' for d in G.get('drive', []))
gbody = f'''    <p class="crumb"><a href="/visit/">← Visit &amp; Plan</a></p>
    <p class="kicker">Planes, trains and the open road</p>
    <h1>Getting here</h1>
    <p class="lede">Cassopolis sits in the middle of the St. Joseph River valley, an easy drive from Chicago, Detroit, Indianapolis and Grand Rapids, with an airport at South Bend and Amtrak stations at Dowagiac and Niles, two of the valley’s handsomest old depots.</p>
    <h2>By car</h2>
    <div class="tblwrap"><table class="cm-tbl"><caption>To Cassopolis, without traffic</caption><thead><tr><th scope="col">From</th><th scope="col">Miles</th><th scope="col">Time</th></tr></thead><tbody>{drive}</tbody></table></div>
    <p class="note">Times are estimates without traffic, worked out from road routes between town centers. Allow extra time around Chicago, where the clock is also an hour behind.</p>
    <h2>By air</h2><ul class="dis">{air}</ul>
    <h2>By train</h2><ul class="dis">{rail}</ul>
    <h2>By bus</h2><ul class="dis">{bus}</ul>
    <h2>Clocks</h2>
    <p>{E(G.get("time_zones",""))}</p>
    <p class="ctas"><a class="btn primary" href="/visit/">Plan a day out</a> <a class="btn" href="/food/stay/">Places to stay</a> <a class="btn" href="/valley-map/">The valley map</a></p>
'''
page('getting-here/index.html', 'Getting here: by car, air, train and bus · Project Scroll',
     'How to reach Cassopolis and the St. Joseph River valley: drive times from Chicago, Detroit and Indianapolis, South Bend and Kalamazoo airports, Amtrak at Dowagiac and Niles, the South Shore Line and buses.',
     gbody, og='https://projectscroll.com/og/food-stay.jpg?v=1')
print('outdoors and getting here built', len(D['places']), len(D['upick']))
