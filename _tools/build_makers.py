"""Made in the Valley: the factories and farms that made the valley's name, each with what it made, its story,
how it ended, and where to see it today.  Data: data/makers.json.  python3 _tools/build_makers.py"""
import sys, json, re, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
import oldcards as O
E = lambda s: html.escape(str(s), quote=True)
H = pathlib.Path(__file__).parent/'data'
M = json.load(open(H/'makers.json'))
MU = {m['name']: m for m in json.load(open(H/'museums.json'))}
def smart(s):
    s = re.sub(r"(^|[\s(])'", r'\1“', s); s = re.sub(r"'(?=[\s.,;:)!?]|$)", '”', s); return s.replace("'", '’')
REG = [('Cass County, Michigan', ['round-oak-stove','dowagiac-drill','heddon']),
       ('Berrien and St. Joseph counties, Michigan', ['benton-harbor-fruit-market','whirlpool','kawneer','clark-equipment','sheffield-car']),
       ('Kalamazoo', ['kalamazoo-celery','gibson','upjohn','kalamazoo-stove','shakespeare','checker-motors']),
       ('South Bend and Mishawaka, Indiana', ['studebaker','oliver-chilled-plow','singer-south-bend','ball-band','bendix']),
       ('Elkhart, Nappanee and La Porte, Indiana', ['conn','miles-laboratories','coppes','rumely'])]
PC = {'round-oak-stove':['ps022','ps107'], 'dowagiac-drill':['ps013'], 'sheffield-car':['ps062'], 'benton-harbor-fruit-market':['ps051','ps050']}
SEE = {'round-oak-stove':['Dowagiac Area History Museum'], 'dowagiac-drill':['Dowagiac Area History Museum'], 'heddon':['Heddon Museum'],
       'studebaker':['Studebaker National Museum','Studebaker-Bendix Heritage Trail'], 'oliver-chilled-plow':['The History Museum'], 'bendix':['Studebaker-Bendix Heritage Trail'],
       'gibson':['Kalamazoo Valley Museum'], 'kalamazoo-stove':['Kalamazoo Valley Museum'], 'checker-motors':['Gilmore Car Museum','Kalamazoo Valley Museum'],
       'rumely':['La Porte County History Museum (La Porte County Historical Society)'], 'coppes':['Coppes Commons and Coppes History Museum']}
BY = {m['id']: m for m in M}
# the years each maker worked in the valley, as its entry gives them: None = ongoing, '?' = end not established
SPAN = {'round-oak-stove':(1871,1947),'dowagiac-drill':(1881,'?'),'heddon':(1902,1984),'kawneer':(1907,'?'),'clark-equipment':(1904,'?'),
 'sheffield-car':(1879,1918),'studebaker':(1852,1963),'oliver-chilled-plow':(1855,1985),'singer-south-bend':(1868,1955),'bendix':(1924,'?'),
 'ball-band':(1867,1997),'conn':(1875,1972),'miles-laboratories':(1885,'?'),'gibson':(1902,1984),'kalamazoo-celery':(1856,2000),'upjohn':(1886,1995),
 'checker-motors':(1923,1982),'shakespeare':(1897,1970),'kalamazoo-stove':(1902,1952),'whirlpool':(1911,None),'benton-harbor-fruit-market':(1860,None),
 'rumely':(1853,1983),'coppes':(1876,None)}
assert sorted(SPAN)==sorted(BY)
import visitdata as V
TLL = {n:(la,lo) for n,la,lo in V.TOWNS}
def town_ll(m):
    t=m['town'].split(' / ')[0]
    return TLL.get(t) or TLL.get({'St. Joseph':'St. Joseph'}.get(t,t))
Y0, Y1 = 1850, 2026
def bar(k):
    a,b = SPAN[k]; m=BY[k]
    end = Y1 if b in (None,'?') else b
    left=(a-Y0)/(Y1-Y0)*100; wid=(end-a)/(Y1-Y0)*100
    lab = f'{a}–{"today" if b is None else ("?" if b=="?" else b)}'
    cls = ' open' if b is None else (' unk' if b=='?' else '')
    return f'<li><a href="#{k}"><span class="tl-n">{E(m["name"].split(" (")[0])}</span><span class="tl-t"><i class="tl-b{cls}" style="left:{left:.1f}%;width:{wid:.1f}%"></i></span><span class="tl-y">{lab}</span></a></li>'
TIMELINE = ''.join(bar(k) for k in sorted(SPAN, key=lambda k: SPAN[k][0]))
PINS = json.dumps([[m['id'], m['name'].split(' (')[0], m['town'], *town_ll(m)] for m in M if town_ll(m)], ensure_ascii=False)
assert sorted(BY) == sorted(i for _, L in REG for i in L)
def card(m):
    k = m['id']; facts = []
    if m.get('founded'): facts.append(('Begun', m['founded']))
    if m.get('founder'): facts.append(('By', m['founder']))
    if m.get('made'): facts.append(('Made', m['made']))
    if m.get('peak'): facts.append(('At its height', m['peak']))
    if m.get('end'): facts.append(('How it ended', m['end']))
    if m.get('today'): facts.append(('Today', m['today']))
    dl = ''.join(f'<dt>{E(a)}</dt><dd>{E(smart(b))}</dd>' for a, b in facts)
    pcs = ''.join(f'<figure class="mk-pc">{O.pic(O.BY[i], "(min-width:900px) 16rem, 46vw")}<figcaption><a href="/postcards/#oc-{i}">{E(O.BY[i]["title"])}</a> · {E(O.BY[i]["date"])}</figcaption></figure>' for i in PC.get(k, []))
    see = [f'<a href="/museums/#{O.slug(n)}">{E(n.split(" (")[0])}</a>' for n in SEE.get(k, []) if n in MU]
    see += [f'<a href="{E(s["url"])}" rel="noopener">{E(s["place"].split(" (")[0])}</a>' for s in m.get('see_it', []) if not any(s['place'].startswith(n.split(' (')[0]) for n in SEE.get(k, []))]
    src = ' '.join(f'<a href="{E(u)}" rel="noopener">source {i}</a>' for i, u in enumerate(m['sources'], 1))
    return f'''<li class="mk" id="{k}"><p class="mu-k">{E(m['town'])}, {E(m['state'])}</p><h3>{E(m['name'])}</h3>
        {f'<div class="mk-pcs">{pcs}</div>' if pcs else ''}<p>{E(smart(m['story']))}</p><dl class="mk-dl">{dl}</dl>
        {f'<p class="mk-see"><b>See it:</b> {" · ".join(see)}</p>' if see else ''}<p class="mk-near">Have something {E(m['name'].split(' (')[0].split(' / ')[0])} made? <a href="/heirlooms/">Add it to the heirloom cabinet ›</a></p><p class="wk-src">{src}</p></li>'''
secs = ''.join(f'<section aria-labelledby="mk-{O.slug(t)}"><h2 id="mk-{O.slug(t)}">{E(t)}</h2><ol class="mk-list">{"".join(card(BY[i]) for i in L)}</ol></section>' for t, L in REG)
nav = ' '.join(f'<a href="#mk-{O.slug(t)}">{E(t.split(",")[0])}</a>' for t, _ in REG)
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Made in the Valley</p>
    <h1>What the valley made</h1>
    <p class="lede" style="font-size:1.15rem">Stoves and seed drills, fishing lures and band horns, wagons, plows, guitars, rubber boots, washing machines, celery and peaches. For a century the towns of the St. Joseph River valley made things the whole country knew by name. Here are {len(M)} of the makers: who started them, what they made, how they ended, and where you can still see their work.</p>
    <p class="nm-chips mu-jump"><span class="mu-jl">Jump to:</span> {nav} <a href="#mkmap">The map</a> <a href="#mktime">The timeline</a></p>
    <section aria-labelledby="mkmapH" id="mkmap"><h2 id="mkmapH">The makers on the map</h2>
      <figure class="mu-mapf"><div class="mu-map mk-map" id="mkMap" role="region" aria-label="Map of the makers' towns. Every maker is also listed below."><p class="mu-mapph">The map opens here.</p></div>
      <figcaption class="note">Pins mark each maker’s town, not the exact site of the works. Press a pin to jump to its story.</figcaption></figure></section>
    <section aria-labelledby="mktimeH" id="mktime"><h2 id="mktimeH">A century and a half of making</h2>
      <p>When each maker worked in the valley, from the dates on its entry below. A bar running to the right edge is still going; a fading bar is one whose end we have not pinned down.</p>
      <div class="tl-axis" aria-hidden="true"><span></span><span class="tl-ax"><b style="left:0.0%">1850</b><b style="left:28.4%">1900</b><b style="left:56.8%">1950</b><b style="left:85.2%">2000</b></span><span></span></div>
      <ol class="mk-tl">{TIMELINE}</ol></section>
{secs}
    <p class="vs-plan"><a class="btn" href="/heirlooms/">Have something one of them made? Add it to the heirloom cabinet</a></p>
    <p class="note">Each maker was checked against the sources linked under it in October 2026: museum and library pages, state historical markers, local newspapers and company histories. Where sources disagree on a date, we say so or give the range. The big claims (“largest in the world”) are the makers’ own boasts, as printed at the time. Corrections are welcome at <a href="mailto:research@projectscroll.com">research@projectscroll.com</a>.</p>
'''
body += '''<script>
(function(){ "use strict"; var el=document.getElementById('mkMap'); if (!el) return; var PINS=__PINS__, map=null;
  var start=function(){ if (map || !window.L) return; el.innerHTML='';
    map=L.map(el,{zoomSnap:.25, minZoom:7, maxZoom:14, scrollWheelZoom:false, maxBounds:[[40.9,-87.9],[42.95,-84.3]]}); map.attributionControl.setPrefix(false); map.fitBounds([[41.38,-86.9],[42.4,-85.45]]);
    map.on('focus click',function(){ map.scrollWheelZoom.enable(); }); map.on('blur mouseout',function(){ map.scrollWheelZoom.disable(); });
    fetch('/museums/base.json?v=1').then(function(r){ return r.json(); }).then(function(b){ var pane=map.createPane('base'); pane.style.zIndex=250;
      b.c.forEach(function(c){ c.r.forEach(function(r){ L.polygon(r.map(function(q){ return [q[1],q[0]]; }),{pane:'base', className:c.d?'mu-cty in':'mu-cty', interactive:false}).addTo(map); }); });
      b.v.forEach(function(l){ L.polyline(l.map(function(q){ return [q[1],q[0]]; }),{pane:'base', className:'mu-rv', interactive:false}).addTo(map); });
      map.attributionControl.addAttribution('County lines: US Census Bureau · Rivers: USGS'); }).catch(function(){});
    __TOWNS__.forEach(function(x){ L.marker([x[1],x[2]],{interactive:false, keyboard:false, icon:L.divIcon({className:'vs-town', html:'<span>'+x[0]+'</span>', iconSize:null})}).addTo(map); });
    var seen={}; PINS.forEach(function(p){ var k=p[3]+','+p[4], n=seen[k]=(seen[k]||0)+1, ang=n*2.1, r=n>1?0.018*Math.sqrt(n):0, ll=[p[3]+r*Math.sin(ang), p[4]+r*1.35*Math.cos(ang)];
      var c=L.circleMarker(ll,{radius:7, className:'mu-pin mk-pin', bubblingMouseEvents:false}); c.bindTooltip(p[1]+' · '+p[2],{direction:'top', offset:[0,-6]});
      c.on('click',function(){ var t=document.getElementById(p[0]); if (t) t.scrollIntoView({behavior:'smooth', block:'start'}); }); c.addTo(map); }); };
  var need=function(){ if (window.L){ start(); return; } var l=document.createElement('link'); l.rel='stylesheet'; l.href='/vendor/leaflet-1.9.4/leaflet.css?v=1'; document.head.appendChild(l);
    var sc=document.createElement('script'); sc.src='/vendor/leaflet-1.9.4/leaflet.js?v=1'; sc.onload=start; document.head.appendChild(sc); };
  if ('IntersectionObserver' in window){ var io=new IntersectionObserver(function(e){ if (e.some(function(x){ return x.isIntersecting; })){ io.disconnect(); need(); } },{rootMargin:'300px'}); io.observe(el); } else need();
})();
</script>'''.replace('__PINS__', PINS).replace('__TOWNS__', json.dumps([[n,la,lo] for n,la,lo in V.TOWNS]))
page('made-in-the-valley/index.html', 'Made in the Valley · Project Scroll', f'The makers of the St. Joseph River valley: Round Oak stoves, Heddon lures, Studebaker wagons, Oliver plows, Conn horns, Gibson guitars, Kalamazoo celery and more. {len(M)} makers, their stories and where to see their work today.', body, og='https://projectscroll.com/og/legends.jpg')
print('makers built', len(M))
