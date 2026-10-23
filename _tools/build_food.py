"""Food, Recipes & Lodging: places to eat and stay with a story, the valley kitchen (recipes from the old cookbooks and papers),
and where the food came from. python3 _tools/build_food.py   (data in _tools/data/food.json and _tools/data/recipes.json)"""
import sys, pathlib, json, html, re, urllib.parse
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E = html.escape
P = pathlib.Path(__file__).parent/'data'
F = [d for d in json.load(open(P/'food.json')) if d.get('keep', True)]
R = [d for d in json.load(open(P/'recipes.json')) if d.get('keep', True)]
ST = {'MI':'Michigan','IN':'Indiana'}
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
used=set()
for d in F:
    s=slug(d['name']+' '+d['town']) if slug(d['name']) in used else slug(d['name']); used.add(s); d['_id']=s
def directions(d):
    if not d.get('address'): return ''
    return 'https://www.google.com/maps/dir/?api=1&destination='+urllib.parse.quote(d['name']+', '+d['address'])
import math
_MU = [m for m in json.load(open(P/'museums.json')) if m.get('ll')]
def _km(a,b):
    r=math.pi/180; dl=(b[0]-a[0])*r; dn=(b[1]-a[1])*r; h=math.sin(dl/2)**2+math.cos(a[0]*r)*math.cos(b[0]*r)*math.sin(dn/2)**2; return 12742*math.asin(math.sqrt(h))
def _mslug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
_MID={}; _u=set()
for m in json.load(open(P/'museums.json')):
    k=_mslug(m['name']); k=_mslug(m['name']+' '+m['town']) if k in _u else k; _u.add(k); _MID[m['name']]=k
def near(d):
    if not d.get('ll'): return ''
    best=min(_MU, key=lambda m:_km(d['ll'],m['ll'])); k=_km(d['ll'],best['ll'])
    if k>8: return ''
    mi=k*0.621371; t='next door' if mi<0.15 else (f'{mi:.1f} mi away' if mi<10 else f'{round(mi)} mi away')
    return f'<p class="fd-near">Nearby: <a href="/museums/#{_MID[best["name"]]}">{E(best["name"])}</a>, {t}</p>'
def kclass(d):
    k=(d.get('kind','')+' '+d['name']).lower()
    if d['type']=='lodging': return 'inn' if re.search(r'inn|hotel|castle|estate', k) and 'b&b' not in k else 'bnb'
    if re.search(r'orchard|market|cider|distill', k): return 'orchard'
    if re.search(r'ice cream|candy|bakery|pastry|soda', k): return 'sweet'
    if re.search(r'tavern|pub|saloon|brew|supper club', k): return 'tavern'
    return 'dine'
def card(d):
    di = directions(d)
    acts = [f'<a class="mu-go" href="{E(d["url"])}" rel="noopener">Their website ›</a>' if d.get('url') else '<span class="mu-none">No website: call ahead</span>']
    if di: acts.append(f'<a href="{E(di)}" rel="noopener">Directions</a>')
    if d.get('ll'): acts.append('<button type="button" class="mu-sm">Show on the map</button>')
    if d.get('ll'): acts.append(f'<button type="button" class="mu-tb fd-add" data-i="f:{d["_id"]}" aria-pressed="false">Add to my day</button>')
    chk = '' if d.get('verified') else '<span class="mu-chk" title="We could not confirm every detail online. Check before you go.">check before you go</span>'
    ll = f' data-ll="{d["ll"][0]},{d["ll"][1]}"' if d.get('ll') else ''
    return f'''<li class="mu fd" id="{d['_id']}" data-ty="{d['type']}" data-kc="{kclass(d)}" data-c="{E(d['county'])}"{ll} data-n="{E(d['name'])}" data-t="{E((d['name']+' '+d['town']+' '+d['county']+' '+d.get('kind','')+' '+d.get('story','')+' '+d.get('what','')).lower())}">
        <p class="mu-k">{E(d.get('kind',''))} · {E(d['town'])}{chk}</p>
        <h3>{E(d['name'])}</h3>
        <p class="fd-story">{E(d.get('story',''))}</p>
        {f'<p>{E(d["what"])}</p>' if d.get('what') else ''}
        {f'<p class="mu-a">{E(d["address"])}</p>' if d.get('address') else ''}
        {near(d)}<p class="mu-acts">{' · '.join(acts)}</p>
        {'<p class="mu-me"><button type="button" class="mu-sb fd-sb" hidden>I’m here: stamp it</button></p><p class="mu-msg" aria-live="polite"></p>' if d.get('ll') else ''}
      </li>'''
def group(ty):
    out=''
    xs=[d for d in F if d['type']==ty]
    for st in ('MI','IN'):
        ys=sorted([d for d in xs if d['state']==st], key=lambda d:(d['county'], d['town'], d['name']))
        if ys: out+=f'<h3 class="fd-st">{ST[st]}</h3><ul class="mu-list">{"".join(card(d) for d in ys)}</ul>'
    return out, len(xs)
eat, ne = group('restaurant'); stay, ns = group('lodging')
RLINK={'Celery Soup':('Kalamazoo grew celery for a century','/made-in-the-valley/#kalamazoo-celery'),
 'Apple Fritters':('Apples and cider today: the fall orchards','/visit/#day-fall'),
 'Apple Butter With Cider':('Apples and cider today: the fall orchards','/visit/#day-fall'),
 'Cream Peach Pie':('The fruit belt and its great market','/made-in-the-valley/#benton-harbor-fruit-market'),
 'Pickle Peaches':('The fruit belt and its great market','/made-in-the-valley/#benton-harbor-fruit-market'),
 'Boiled Huckleberry Pudding':('Blueberry season on the calendar','/seasons/#blueberry-u-pick-season'),
 'Maple Creams':('Maple sugar festivals on the calendar','/seasons/#kalamazoo-nature-center-maple-sugar-festival')}
COURSE = [('bread','Breads'),('soup','Soups'),('main','Main dishes'),('vegetable','Vegetables'),('pie-cake','Pies & cakes'),('dessert','Puddings & desserts'),('preserve','Preserves & pickles'),('drink','Drinks'),('candy','Candy'),('hint','Household hints')]
CNAME = dict(COURSE)
from PIL import Image as _Img
ROOT = pathlib.Path(__file__).parent.parent
def _wh(src):
    try:
        with _Img.open(ROOT/src.lstrip('/')) as im: return im.size
    except Exception: return None
def rplace(d): return (d.get('source_place') or '').split(',')[0].strip()
def rec(d):
    who = f' · {E(d["contributor"])}' if d.get('contributor') else ''
    src = f'<a href="{E(d["url"])}" rel="noopener">{E(d["source_title"])}</a>' if d.get('url') else E(d['source_title'])
    course = d.get('course') or ('hint' if d['kind']=='hint' else 'main')
    if d.get('img'):
        wh = _wh(d['img']); whs = f' width="{wh[0]}" height="{wh[1]}"' if wh else ''
        pic = (f'<figure class="rc-pic"><a class="nw-pz" href="{E(d["img"])}"><img src="{E(d["img"])}"{whs} alt="{E(d["title"])}, as printed in {E(d["source_title"])}" loading="lazy" decoding="async"></a>'
               f'<figcaption>As printed{(", "+E(str(d["year"]))) if d.get("year") else ""}. Tap to enlarge.</figcaption></figure>')
    else:
        pic = f'<div class="rc-card" aria-hidden="true"><b>{E(d["source_title"].split(" (")[0])}</b><span>{E(rplace(d))}</span><i>{E(str(d.get("year") or ""))}</i></div>'
    return f'''<li class="rc" id="{slug(d['title'])}" data-kind="{d['kind']}" data-co="{course}" data-pl="{E(rplace(d))}" data-t="{E((d['title']+' '+d['text']+' '+(d.get('source_place') or '')+' '+d['source_title']+' '+(d.get('contributor') or '')).lower())}">
        {pic}
        <p class="mu-k">{E(CNAME.get(course,'Recipe'))} · {E(d.get('source_place') or '')}{(', '+E(str(d['year']))) if d.get('year') else ''}</p>
        <h3>{E(d['title'])}</h3>
        <blockquote class="rc-t">{E(d['text'])}</blockquote>
        <p class="rc-src">From {src}{who}</p>
        {f'<p class="fd-near">Its story today: <a href="{RLINK[d["title"]][1]}">{E(RLINK[d["title"]][0])}</a></p>' if d['title'] in RLINK else ''}
        {f'<details class="rc-m"><summary>Making it today</summary><p>{E(d["modern"])}</p></details>' if d.get('modern') else ''}
      </li>'''
_ORDER = {c:i for i,(c,_) in enumerate(COURSE)}
_RS = sorted(R, key=lambda d:(_ORDER.get(d.get('course') or ('hint' if d['kind']=='hint' else 'main'), 99), d['title']))
recipes = ''.join(rec(d) for d in _RS)
_cos = [c for c,_ in COURSE if any((d.get('course') or ('hint' if d['kind']=='hint' else 'main'))==c for d in R)]
rchips = '<button type="button" class="btn rc-c" data-co="" aria-pressed="true">All</button>' + ''.join(f'<button type="button" class="btn rc-c" data-co="{c}" aria-pressed="false">{E(CNAME[c])}</button>' for c in _cos)
_pls = sorted({rplace(d) for d in R if rplace(d)})
rpl = ''.join(f'<option value="{E(x)}">{E(x)}</option>' for x in _pls)
CB = json.load(open(P/'cookbooks.json')) if (P/'cookbooks.json').exists() else []
def cbk(b):
    n = sum(1 for d in R if d['source_title']==b['match'] or d['source_title'].startswith(b['match']))
    wh = _wh(b['img']) if b.get('img') else None; whs = f' width="{wh[0]}" height="{wh[1]}"' if wh else ''
    im = f'<a class="nw-pz" href="{E(b["img"])}"><img src="{E(b["img"])}"{whs} alt="The cover of {E(b["title"])}" loading="lazy" decoding="async"></a>' if b.get('img') else f'<div class="rc-card"><b>{E(b["title"])}</b><span>{E(b["place"])}</span><i>{E(b["year"])}</i></div>'
    link = f'<a href="{E(b["url"])}" rel="noopener">{"Read the paper" if b.get("paper") else "Read the whole book"} ›</a>' if b.get('url') else ''
    return f'<li class="cb"><figure class="rc-pic cb-pic">{im}</figure><div><p class="mu-k">{E(b["place"])} · {E(b["year"])}</p><h3>{E(b["title"])}</h3><p>{E(b["about"])}</p><p class="rc-src">{n} {"item" if n==1 else "items"} on this page{" · "+link if link else ""}</p></div></li>'
shelf = ''.join(cbk(b) for b in CB)
GLOSS = [
 ('Saleratus', 'An early baking soda (bicarbonate of potash or soda). Use baking soda.'),
 ('Butter the size of an egg', 'About 1/4 cup (4 tablespoons). “The size of a walnut” is about 2 tablespoons.'),
 ('A gill', 'Half a cup (4 fluid ounces).'),
 ('A coffeecup, a teacup', 'A coffeecup is about 1 cup; a teacup a little less, about 3/4 cup.'),
 ('A salt spoon', 'About 1/4 teaspoon.'),
 ('Rich paste', 'Pie pastry made with plenty of butter or lard.'),
 ('A soft ball', 'Sugar syrup cooked until a drop forms a soft ball in cold water: 235–240°F on a candy thermometer.'),
 ('A quick, moderate or slow oven', 'Before oven dials: quick or hot is about 400–450°F, moderate about 350–375°F, slow about 300–325°F.'),
 ('Cassia buds', 'The dried flower buds of the cassia (Chinese cinnamon) tree. Whole cloves or a cinnamon stick will do.'),
 ('Paraffine paper', 'Waxed paper.'),
 ('Dripping pan', 'A shallow roasting or baking pan.'),
 ('Maître d’hôtel sauce', 'Melted butter with chopped parsley, lemon juice, salt and pepper.'),
 ('Sweet milk, sour milk', 'Sweet milk is fresh milk. Sour milk was soured naturally; buttermilk is the nearest today.'),
 ('A peck, a bushel', 'A peck is about 8 quarts (around 12 lb of apples or peaches); a bushel is four pecks.'),
]
gloss = ''.join(f'<dt>{E(a)}</dt><dd>{E(b)}</dd>' for a,b in GLOSS)
counties = sorted({d['county']+'|'+d['state'] for d in F}, key=lambda x:(x.split('|')[1]!='MI', x))
copts = ''.join(f'<option value="{E(c.split("|")[0])}">{E(c.split("|")[0])} County, {ST[c.split("|")[1]]}</option>' for c in counties)
items=[]
for d in F:
    it={'@type':'Restaurant' if d['type']=='restaurant' else 'LodgingBusiness','name':d['name'],'description':d.get('story',''),'url':'https://projectscroll.com/food/#'+d['_id']}
    if d.get('url'): it['sameAs']=d['url']
    if d.get('address'): it['address']={'@type':'PostalAddress','streetAddress':d['address'].split(',')[0],'addressLocality':d['town'],'addressRegion':d['state'],'addressCountry':'US'}
    items.append(it)
ld='<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@type':'ItemList','name':'Places to eat and stay with a story in the St. Joseph River valley','itemListElement':[{'@type':'ListItem','position':i+1,'item':x} for i,x in enumerate(items)]},ensure_ascii=False).replace('</','<\\/')+'</script>'
JS = r'''<script>
(function(){ "use strict";
  var $=function(s){ return document.querySelector(s); }, $$=function(s){ return [].slice.call(document.querySelectorAll(s)); };
  var calm=matchMedia('(prefers-reduced-motion: reduce)').matches, glide=calm?'auto':'smooth';
  var items=$$('.fd'), q=$('#fdQ'), cs=$('#fdC'), tys=$$('.fd-f'), kcs=$$('.fd-k'), kc='', cnt=$('#fdCount'), ty='', map=null, marks=[], showMu=false, mu=[];
  var draw=function(){ var w=q.value.trim().toLowerCase().split(/\s+/).filter(Boolean), c=cs.value, n=0;
    items.forEach(function(li){ var ok=(!ty||li.dataset.ty===ty) && (!kc||li.dataset.kc===kc) && (!c||li.dataset.c===c) && w.every(function(x){ return li.dataset.t.indexOf(x)>=0; }); li.hidden=!ok; if (ok) n++; });
    $$('.fd-sec').forEach(function(s){ s.hidden=!s.querySelector('.fd:not([hidden])'); });
    $$('.fd-sec h3.fd-st').forEach(function(h){ var ul=h.nextElementSibling; h.hidden=h.classList.contains('gone') || !ul.querySelector('.fd:not([hidden])'); });
    cnt.textContent=n===items.length? n+' places' : n+' of '+items.length+' places';
    if (map) pins(); };
  tys.forEach(function(b){ b.addEventListener('click',function(){ ty=b.dataset.ty; tys.forEach(function(x){ x.setAttribute('aria-pressed',String(x===b)); }); draw(); }); });
  kcs.forEach(function(b){ b.addEventListener('click',function(){ kc=b.dataset.kc; kcs.forEach(function(x){ x.setAttribute('aria-pressed',String(x===b)); }); draw(); }); });
  q.addEventListener('input',draw); cs.addEventListener('change',draw);
  /* in season now: what the valley is picking, pressing or boiling down this month */
  var SEA=__SEASON__, sa=$('#fdSeason'), mo=new Date().getMonth(), z=SEA[mo];
  if (sa && z){ sa.innerHTML='<p class="fd-sk">In season in '+z[0]+'</p><p></p><p class="fd-sl"></p>'; sa.children[1].textContent=z[1];
    z[2].forEach(function(l,i){ var a=document.createElement('a'); a.href=l[1]; a.textContent=l[0]; if (i) sa.children[2].appendChild(document.createTextNode(' · ')); sa.children[2].appendChild(a); }); sa.hidden=false; }
  var go=function(li){ li.scrollIntoView({behavior:glide, block:'center'}); li.classList.remove('flash'); void li.offsetWidth; li.classList.add('flash'); };
  var pins=function(){ marks.forEach(function(m){ var on=!m.li.hidden; if (on && !map.hasLayer(m.c)) m.c.addTo(map); if (!on && map.hasLayer(m.c)) map.removeLayer(m.c); }); };
  var start=function(){ if (map || !window.L) return;
    [].forEach.call(document.querySelectorAll('.mu-mapph'),function(x){ x.remove(); });
    map=L.map('fdMap',{zoomSnap:.25, minZoom:7, maxZoom:17, scrollWheelZoom:false, maxBounds:[[40.9,-87.9],[42.95,-84.3]]}); map.attributionControl.setPrefix(false);
    map.fitBounds([[41.42,-86.95],[42.43,-85.35]]);
    map.on('focus click',function(){ map.scrollWheelZoom.enable(); }); map.on('blur mouseout',function(){ map.scrollWheelZoom.disable(); });
    fetch('/museums/base.json?v=1').then(function(r){ return r.json(); }).then(function(b){ var pane=map.createPane('base'); pane.style.zIndex=250;
      b.c.forEach(function(c){ c.r.forEach(function(r){ L.polygon(r.map(function(p){ return [p[1],p[0]]; }),{pane:'base', className:c.d?'mu-cty in':'mu-cty', interactive:false}).addTo(map); }); });
      b.v.forEach(function(l){ L.polyline(l.map(function(p){ return [p[1],p[0]]; }),{pane:'base', className:'mu-rv', interactive:false}).addTo(map); });
      map.attributionControl.addAttribution('County lines: US Census Bureau · Rivers: USGS'); }).catch(function(){});
    __TOWNS__.forEach(function(x){ L.marker([x[1],x[2]],{interactive:false, keyboard:false, icon:L.divIcon({className:'vs-town', html:'<span>'+x[0]+'</span>', iconSize:null})}).addTo(map); });
    items.forEach(function(li){ if (!li.dataset.ll) return; var ll=li.dataset.ll.split(',').map(Number);
      var c=L.circleMarker(ll,{radius:7, className:'mu-pin '+(li.dataset.ty==='lodging'?'stay':'eat'), bubblingMouseEvents:false});
      var b=document.createElement('button'); b.type='button'; b.className='fd-popb'; b.textContent=li.dataset.n+' ›'; b.addEventListener('click',function(){ map.closePopup(); go(li); });
      c.bindPopup(b); c.bindTooltip(li.dataset.n,{direction:'top', offset:[0,-6]}); marks.push({c:c, li:li}); li._c=c; c.addTo(map); });
    var sm=$('#fdMu'); sm.hidden=false; sm.addEventListener('click',function(){ showMu=!showMu; sm.setAttribute('aria-pressed',String(showMu));
      if (showMu && !mu.length) fetch('/museums/places.json?v=1').then(function(r){ return r.json(); }).then(function(ps){ ps.forEach(function(p){ var c=L.circleMarker([p[1],p[2]],{radius:5, className:'mu-pin fd-mu', bubblingMouseEvents:false}); c.bindTooltip(p[0],{direction:'top'}); var a=document.createElement('a'); a.href='/museums/#'+p[3]; a.textContent=p[0]+' ›'; c.bindPopup(a); mu.push(c); c.addTo(map); }); });
      else mu.forEach(function(c){ showMu? c.addTo(map) : map.removeLayer(c); }); });
    pins(); };
  var need=function(){ if (window.L){ start(); return; } if (need.on) return; need.on=1;
    var l=document.createElement('link'); l.rel='stylesheet'; l.href='/vendor/leaflet-1.9.4/leaflet.css?v=1'; document.head.appendChild(l);
    var s=document.createElement('script'); s.src='/vendor/leaflet-1.9.4/leaflet.js?v=1'; s.onload=start; document.head.appendChild(s); };
  if ('IntersectionObserver' in window){ var io=new IntersectionObserver(function(e){ if (e.some(function(x){ return x.isIntersecting; })){ io.disconnect(); need(); } },{rootMargin:'300px'}); io.observe($('#fdMap')); } else need();
  items.forEach(function(li){ var b=li.querySelector('.mu-sm'); if (!b) return; b.addEventListener('click',function(){ var ll=li.dataset.ll.split(',').map(Number);
    var fly=function(){ $('#fdMap').scrollIntoView({behavior:glide, block:'center'}); map.setView(ll,15,{animate:!calm}); if (li._c) li._c.openPopup(); };
    if (map) fly(); else { need(); var t=setInterval(function(){ if (map && marks.length){ clearInterval(t); fly(); } },120); setTimeout(function(){ clearInterval(t); },8000); } }); });
  /* nearest to me: each list sorted by distance from where you are; the position stays on this device */
  items.forEach(function(li,i){ li._p=li.parentNode; li._i=i; });
  var nb=$('#fdNear'), nm=$('#fdNearMsg'), near=false;
  var km=function(a,b){ var R=6371, r=Math.PI/180, dl=(b[0]-a[0])*r, dn=(b[1]-a[1])*r, h=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a[0]*r)*Math.cos(b[0]*r)*Math.sin(dn/2)*Math.sin(dn/2); return 2*R*Math.asin(Math.sqrt(h)); };
  nb.addEventListener('click',function(){
    if (near){ near=false; nb.setAttribute('aria-pressed','false'); nb.textContent='Nearest to me'; nm.textContent='';
      items.forEach(function(li){ li._p.appendChild(li); var k=li.querySelector('.fd-dist'); if (k) k.remove(); }); $$('.fd-st').forEach(function(h){ h.classList.remove('gone'); }); draw(); return; }
    if (!navigator.geolocation){ nm.textContent='This browser cannot share a location.'; return; }
    nm.textContent='Asking your browser where you are…';
    navigator.geolocation.getCurrentPosition(function(pos){ var me=[pos.coords.latitude,pos.coords.longitude]; near=true; nb.setAttribute('aria-pressed','true'); nb.textContent='Back to the lists';
      ['eat','stay'].forEach(function(sec){ var S=document.getElementById(sec), first=S.querySelector('.mu-list'); var lis=items.filter(function(li){ return S.contains(li); });
        lis.forEach(function(li){ li._d=li.dataset.ll? km(me, li.dataset.ll.split(',').map(Number)) : 1e9; });
        lis.sort(function(a,b){ return a._d-b._d; }).forEach(function(li){ first.appendChild(li); if (li._d<1e9){ var k=document.createElement('span'); k.className='fd-dist'; k.textContent=' · about '+((li._d*.621371)<10?(li._d*.621371).toFixed(1):Math.round(li._d*.621371))+' mi'; li.querySelector('.mu-k').appendChild(k); } });
        S.querySelectorAll('.fd-st').forEach(function(h){ h.classList.add('gone'); }); });
      nm.textContent='Sorted from where you are now. Your location stays on this device.'; draw(); },
      function(){ nm.textContent='No location shared, so nothing changed.'; }, {maximumAge:600000, timeout:15000}); });
  /* a stamp for the table: pressing "I'm here" at the place itself; the location is checked once and stays on this device */
  var fst={}; try{ fst=JSON.parse(localStorage.getItem('ps-food-stamp')||'{}')||{}; }catch(e){}
  var fpaint=function(){ items.forEach(function(li){ var b=li.querySelector('.fd-sb'); if (!b) return; b.hidden=!navigator.geolocation; b.disabled=!!fst[li.id]; b.textContent=fst[li.id]? 'Stamped ✓ '+fst[li.id] : 'I’m here: stamp it'; }); };
  items.forEach(function(li){ var b=li.querySelector('.fd-sb'), m=li.querySelector('.mu-msg'); if (!b) return;
    b.addEventListener('click',function(){ m.textContent='Checking where you are…';
      navigator.geolocation.getCurrentPosition(function(p){ var d=km([p.coords.latitude,p.coords.longitude], li.dataset.ll.split(',').map(Number)), reach=.35+Math.min(p.coords.accuracy||0,400)/1000;
        if (d<=reach){ fst[li.id]=new Date().toISOString().slice(0,10); try{ localStorage.setItem('ps-food-stamp',JSON.stringify(fst)); }catch(e){} fpaint(); m.innerHTML='Stamped. It is in your <a href="/passport/">passport</a>, on this device only.'; if (window.psEarn) window.psEarn('stamp'); if (window.psStampCheck) window.psStampCheck(); }
        else m.textContent='You look to be about '+((d*.621371)<10?(d*.621371).toFixed(1):Math.round(d*.621371))+' mi away. The stamp works at the door.'; },
        function(){ m.textContent='No location shared, so nothing changed.'; }, {enableHighAccuracy:true, timeout:20000, maximumAge:0}); }); });
  fpaint();
  /* the recipe box: ticks for the ones you have cooked, kept on this device */
  var made={}; try{ made=JSON.parse(localStorage.getItem('ps-cooked')||'{}')||{}; }catch(e){}
  $$('.rc').forEach(function(li){ var b=document.createElement('button'); b.type='button'; b.className='mu-bb rc-b';
    var set=function(){ var on=!!made[li.id]; b.setAttribute('aria-pressed',String(on)); b.textContent=on?'I made this ✓':'I made this'; }; set();
    b.addEventListener('click',function(){ if (made[li.id]) delete made[li.id]; else made[li.id]=new Date().toISOString().slice(0,10); try{ localStorage.setItem('ps-cooked',JSON.stringify(made)); }catch(e){} set();
      if (Object.keys(made).length>=1 && window.psEarn) window.psEarn('cook'); });
    var p=document.createElement('p'); p.className='mu-me'; p.appendChild(b);
    var pr=document.createElement('button'); pr.type='button'; pr.className='mu-tb'; pr.textContent='Print this recipe'; pr.addEventListener('click',function(){ li.classList.add('rc-print'); document.documentElement.classList.add('rc-printing'); window.print(); });
    p.appendChild(pr); li.appendChild(p); });
  addEventListener('afterprint',function(){ document.documentElement.classList.remove('rc-printing'); $$('.rc-print').forEach(function(x){ x.classList.remove('rc-print'); }); });
  /* add to my day: the same list the Visit & Plan day builder uses, kept on this device */
  var day=[]; try{ day=JSON.parse(localStorage.getItem('ps-day')||'[]')||[]; }catch(e){}
  var dpaint=function(){ $$('.fd-add').forEach(function(b){ var on=day.indexOf(b.dataset.i)>=0; b.setAttribute('aria-pressed',String(on)); b.textContent=on?'On my day ✓':'Add to my day'; }); var n=$('#fdDayN'); if (n){ n.textContent=day.length; n.parentNode.hidden=!day.length; } };
  $$('.fd-add').forEach(function(b){ b.addEventListener('click',function(){ var i=day.indexOf(b.dataset.i); if (i>=0) day.splice(i,1); else day.push(b.dataset.i); try{ localStorage.setItem('ps-day',JSON.stringify(day)); }catch(e){} dpaint(); }); });
  dpaint();
  /* the recipe box: find by word, kind of dish or town */
  var rq=$('#rcQ'), rp=$('#rcP'), rcs=$$('.rc-c'), rco='', rli=$$('.rc'), rcn=$('#rcCount');
  var rdraw=function(){ var w=rq.value.trim().toLowerCase().split(/\s+/).filter(Boolean), pl=rp.value, n=0;
    rli.forEach(function(li){ var ok=(!rco||li.dataset.co===rco) && (!pl||li.dataset.pl===pl) && w.every(function(x){ return li.dataset.t.indexOf(x)>=0; }); li.hidden=!ok; if (ok) n++; });
    rcn.textContent=n===rli.length? n+' recipes and hints' : n+' of '+rli.length; $('#rcNone').hidden=n>0; };
  if (rq){ rq.addEventListener('input',rdraw); rp.addEventListener('change',rdraw);
    rcs.forEach(function(b){ b.addEventListener('click',function(){ rco=b.dataset.co; rcs.forEach(function(x){ x.setAttribute('aria-pressed',String(x===b)); }); rdraw(); }); }); }
  var pa=$('#rcAll'); if (pa) pa.addEventListener('click',function(){ $$('.rc').forEach(function(li){ li.classList.add('rc-print'); }); document.documentElement.classList.add('rc-printing'); window.print(); });
  draw();
  var h=location.hash.slice(1), t=h && document.getElementById(h); if (t && (t.classList.contains('fd') || t.classList.contains('rc'))) setTimeout(function(){ go(t); },300);
})();
</script>'''
SEASON=[
 ['January','Winter. The orchards are resting; the ice festivals are on the calendar.',[['The year’s calendar','/seasons/']]],
 ['February','Still winter. Maple sugaring usually begins as the days start to warm.',[['Maple festivals on the calendar','/seasons/#kalamazoo-nature-center-maple-sugar-festival']]],
 ['March','Maple syrup time. The Kalamazoo Nature Center’s Maple Sugar Festival comes early in the month.',[['Maple Sugar Festival','/seasons/#kalamazoo-nature-center-maple-sugar-festival'],['Maple creams from the valley kitchen','#maple-creams']]],
 ['April','Sugaring ends with the Wakarusa Maple Syrup Festival late in the month, and the fruit belt starts to bloom.',[['Wakarusa Maple Syrup Festival','/seasons/#wakarusa-maple-syrup-festival']]],
 ['May','Blossom time in the fruit belt, with Blossomtime in St. Joseph and Benton Harbor.',[['Blossomtime Festival','/seasons/#blossomtime-festival'],['A weekend in the fruit belt','/visit/#day-fruit']]],
 ['June','Early summer: the orchards are setting fruit and the u-pick season is coming.',[['A weekend in the fruit belt','/visit/#day-fruit']]],
 ['July','Blueberry u-pick season opens, and the Coloma Glad-Peach Festival comes at the end of the month.',[['Blueberry season','/seasons/#blueberry-u-pick-season'],['Coloma Glad-Peach Festival','/seasons/#coloma-glad-peach-festival']]],
 ['August','Blueberries and peaches, the National Blueberry Festival in South Haven, and apple picking from the middle of the month.',[['National Blueberry Festival','/seasons/#national-blueberry-festival'],['Cream peach pie from the valley kitchen','#cream-peach-pie']]],
 ['September','Apple-picking season, the Nappanee Apple Festival, and cider again at the orchards.',[['Nappanee Apple Festival','/seasons/#nappanee-apple-festival'],['Jollay Orchards','#jollay-orchards'],['Kercher’s Sunrise Orchards','#kercher-s-sunrise-orchards']]],
 ['October','Apples, cider and doughnuts at the orchards, through the end of the month.',[['A fall drive to the orchards','/visit/#day-fall'],['Jollay Orchards','#jollay-orchards'],['Apple fritters from the valley kitchen','#apple-fritters']]],
 ['November','The orchard season closes. Time for apple butter with cider from the valley kitchen.',[['Apple butter with cider','#apple-butter-with-cider']]],
 ['December','Holiday candy from the valley kitchen: maple creams and popcorn candy.',[['Maple creams','#maple-creams'],['Popcorn candy','#popcorn-candy']]],
]
JS = JS.replace('__SEASON__', json.dumps(SEASON, ensure_ascii=False))
import visitdata as _V
JS = JS.replace('__TOWNS__', json.dumps([[n,la,lo] for n,la,lo in _V.TOWNS]))
FIELDS = [
  ('The fruit belt', 'Along the Lake Michigan shore the big lake keeps spring frosts back and autumn warm, and for well over a century the counties near it have grown apples, peaches, cherries, grapes and blueberries. Many of the valley’s festivals are harvest festivals.', '/seasons/#summer', 'Harvest festivals by season'),
  ('Mills on every stream', 'Before the railroads, every town needed a grist mill to grind its wheat and corn, and most of the valley’s early towns grew up beside one. A few still stand, and one or two still grind.', '/roads-and-rails/', 'Roads, rails and mills'),
  ('Celery and the muck lands', 'Kalamazoo’s low, black “muck” soil made it famous for celery from the late 1800s. The Celery Flats Historical Area in Portage keeps the story.', '/museums/#celery-flats-historical-area', 'Celery Flats in the museums directory'),
  ('The stove in the kitchen', 'Dowagiac’s Round Oak stoves heated and cooked for farm kitchens across the country. The Dowagiac Area History Museum tells the story.', '/museums/#dowagiac-area-history-museum', 'Dowagiac Area History Museum'),
]
_OC = {c['id']:c for c in json.load(open(P/'oldcards.json'))}
FPIC = {'The fruit belt':'ps050','Mills on every stream':'ps111','The stove in the kitchen':'ps107'}
def fpic(t):
    k=FPIC.get(t)
    if not k: return ''
    c=_OC[k]; h=round(700*c['h']/c['w'])
    cred = '' if (c.get('credit') or '').startswith('none') else ' · '+E(c['credit'])
    return (f'<figure class="fd-pic"><a href="/postcards/#oc-{k}"><picture><source type="image/avif" srcset="/img/oldcards/{k}-700.avif"><img src="/img/oldcards/{k}-700.webp" width="700" height="{h}" alt="{E(c["title"])}, on an old postcard" loading="lazy" decoding="async"></picture></a>'
            f'<figcaption>{E(c["title"])}, {E(str(c.get("date") or ""))}{cred}</figcaption></figure>')
fields = ''.join(f'<li class="fd-fi">{fpic(t)}<h3>{E(t)}</h3><p>{E(d)}</p><p><a href="{u}">{E(l)} ›</a></p></li>' for t,d,u,l in FIELDS)
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Food, recipes &amp; lodging</p>
    <figure class="pg-art"><picture><source type="image/avif" srcset="/img/card-food-art-270.avif 270w, /img/card-food-art.avif 540w" sizes="8rem"><img class="vt-food" src="/img/card-food-art-270.webp" srcset="/img/card-food-art-270.webp 270w, /img/card-food-art.webp 540w" sizes="8rem" width="540" height="960" alt="" decoding="async"></picture></figure>
    <h1>A table and a bed in the valley</h1>
    <p class="lede" style="font-size:1.15rem">Where to eat and where to stay, chosen for their stories: dining rooms in old banks and depots, family tables that have fed a town for generations, inns in houses built before the railroad came. And from the old cookbooks and weekly papers, what the valley cooked.</p>
    <p class="nm-chips fd-jump"><a class="btn" href="#eat">Places to eat</a><a class="btn" href="#stay">Places to stay</a><a class="btn" href="#recipes">The valley kitchen</a><a class="btn" href="#cookbooks">The cookbooks</a><a class="btn" href="#words">Old kitchen words</a><a class="btn" href="#fields">Where the food came from</a></p>
    <aside class="fd-season" id="fdSeason" hidden aria-label="In season now"></aside>
    <div class="mu-bar">
      <label class="nm-q"><span>Find a place</span><input type="search" id="fdQ" placeholder="A town, a kind of place, a building" autocomplete="off" spellcheck="false"></label>
      <div class="nm-chips" role="group" aria-label="Show one kind"><button type="button" class="btn fd-f" data-ty="" aria-pressed="true">Everything</button><button type="button" class="btn fd-f" data-ty="restaurant" aria-pressed="false">Places to eat</button><button type="button" class="btn fd-f" data-ty="lodging" aria-pressed="false">Places to stay</button><button type="button" class="btn" id="fdNear" aria-pressed="false">Nearest to me</button><label class="mu-ol"><span class="vh">County</span><select id="fdC"><option value="">Every county</option>{copts}</select></label></div>
      <div class="nm-chips" role="group" aria-label="Show one sort of place"><button type="button" class="btn fd-k" data-kc="" aria-pressed="true">Any sort</button><button type="button" class="btn fd-k" data-kc="tavern" aria-pressed="false">Taverns &amp; pubs</button><button type="button" class="btn fd-k" data-kc="dine" aria-pressed="false">Restaurants &amp; diners</button><button type="button" class="btn fd-k" data-kc="sweet" aria-pressed="false">Sweets &amp; soda fountains</button><button type="button" class="btn fd-k" data-kc="orchard" aria-pressed="false">Orchards, markets &amp; cider</button><button type="button" class="btn fd-k" data-kc="inn" aria-pressed="false">Historic inns &amp; hotels</button><button type="button" class="btn fd-k" data-kc="bnb" aria-pressed="false">Bed &amp; breakfasts</button></div>
      <p class="mu-nmsg" id="fdNearMsg" aria-live="polite"></p>
      <p class="nm-count" id="fdCount" aria-live="polite">{len(F)} places</p>
    </div>
    <figure class="mu-mapf">
      <div class="mu-map" id="fdMap" role="region" aria-label="Map of the places to eat and stay. Every place is also in the list below."><p class="mu-mapph">The map opens here.</p></div>
      <figcaption><span class="mu-lg"><i class="mu-dot fd-eat"></i> Places to eat</span> <span class="mu-lg"><i class="mu-dot fd-stay"></i> Places to stay</span> <button type="button" class="btn" id="fdMu" aria-pressed="false" hidden>Show the museums too</button></figcaption>
    </figure>
    <section class="fd-sec" id="eat"><h2>Places to eat with a story <span class="mu-n">{ne} places</span></h2>{eat}</section>
    <section class="fd-sec" id="stay"><h2>Places to stay <span class="mu-n">{ns} places</span></h2>{stay}</section>
    <section id="recipes"><h2>The valley kitchen</h2>
      <p><button type="button" class="btn" id="rcAll">Print the whole recipe box</button> <a class="btn" href="/food/valley-kitchen-recipes.pdf" download>Download the recipe booklet (PDF)</a></p>
      <p>Recipes and household hints as they were printed in the valley’s own cookbooks and newspapers, word for word, with a note on how to make each one today. Tick the ones you have cooked: one earns a badge for your <a href="/badges/">field book</a>.</p>
      <div class="mu-bar rc-bar">
        <label class="nm-q"><span>Find a recipe</span><input type="search" id="rcQ" placeholder="An ingredient, a town, a cook" autocomplete="off" spellcheck="false"></label>
        <div class="nm-chips" role="group" aria-label="Show one kind of dish">{rchips}</div>
        <label class="rc-pl"><span>From</span><select id="rcP"><option value="">Every town</option>{rpl}</select></label>
        <p class="nm-count" id="rcCount" aria-live="polite">{len(R)} recipes and hints</p>
      </div>
      <ul class="rc-list">{recipes}</ul>
      <p class="rc-none" id="rcNone" hidden>No recipe matches. Try another word or town.</p></section>
    <section id="cookbooks"><h2>The cookbooks on the shelf</h2>
      <p>Every recipe above comes from one of these books and papers, made by the church societies, clubs and newspapers of the valley. Each one is free to read online.</p>
      <ul class="cb-list">{shelf}</ul></section>
    <section id="words"><h2>Old kitchen words</h2>
      <p>The old cooks wrote for readers who already knew how. Here is what their words mean in a kitchen today.</p>
      <dl class="rc-gloss">{gloss}</dl></section>
    <section id="fields"><h2>Where the food came from</h2><ul class="fd-fields">{fields}</ul></section>
    <h2>Before you go</h2>
    <ul class="dis">
      <li><b>Call or check first.</b> Hours change with the seasons, and small places close for holidays and family days.</li>
      <li><b>Make a day of it.</b> Pair a meal with the <a href="/museums/">museums nearby</a>, the <a href="/walk/">Broadway walk</a> or a <a href="/seasons/">festival</a>.</li>
      <li><b>Know a place with a story?</b> <a href="/#contact">Tell us</a>, with what you know of its history.</li>
      <li><b>Own one of these places?</b> Project Scroll is free to play and depends on sponsors. <a href="/sponsors/">See how to keep the lanterns lit</a>.</li>
    </ul>
    <p class="vs-plan"><a class="btn" href="/visit/">Plan your visit: ready-made days out, food, lodging and festivals</a> <span hidden><a class="btn" href="/visit/#build">See my day (<span id="fdDayN">0</span>)</a></span></p>
    <p class="note">Every place here was chosen for its history and checked against its own website, or a city, county or tourism page, in October 2026. No place paid to be listed; any sponsor will always be marked as one. Places marked “check before you go” could not be fully confirmed online. The recipes are from cookbooks and newspapers published before 1929, now in the public domain, quoted as printed; the notes on making them today are ours.</p>
{ld}
{JS}
'''
page('food/index.html', 'Food, recipes & lodging · Project Scroll',
     f'Where to eat and stay in the St. Joseph River valley, chosen for their history: {ne} places to eat and {ns} places to stay, with a map, plus recipes from the valley’s old cookbooks and newspapers.',
     body, og='https://projectscroll.com/og/records.jpg')
# the museums as a small shared list for other maps
M = json.load(open(P/'museums.json'))
def mslug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
pl=[]; seen=set()
for d in M:
    s=mslug(d['name']); s = mslug(d['name']+' '+d['town']) if s in seen else s; seen.add(s)
    if d.get('ll'): pl.append([d['name'], d['ll'][0], d['ll'][1], s])
open(pathlib.Path(__file__).parent.parent/'museums'/'places.json','w').write(json.dumps(pl, ensure_ascii=False, separators=(',',':')))
print('food built', ne, ns, len(R))
