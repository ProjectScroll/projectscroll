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
def card(d):
    di = directions(d)
    acts = [f'<a class="mu-go" href="{E(d["url"])}" rel="noopener">Their website ›</a>' if d.get('url') else '<span class="mu-none">No website: call ahead</span>']
    if di: acts.append(f'<a href="{E(di)}" rel="noopener">Directions</a>')
    if d.get('ll'): acts.append('<button type="button" class="mu-sm">Show on the map</button>')
    chk = '' if d.get('verified') else '<span class="mu-chk" title="We could not confirm every detail online. Check before you go.">check before you go</span>'
    ll = f' data-ll="{d["ll"][0]},{d["ll"][1]}"' if d.get('ll') else ''
    return f'''<li class="mu fd" id="{d['_id']}" data-ty="{d['type']}" data-c="{E(d['county'])}"{ll} data-n="{E(d['name'])}" data-t="{E((d['name']+' '+d['town']+' '+d['county']+' '+d.get('kind','')+' '+d.get('story','')+' '+d.get('what','')).lower())}">
        <p class="mu-k">{E(d.get('kind',''))} · {E(d['town'])}{chk}</p>
        <h3>{E(d['name'])}</h3>
        <p class="fd-story">{E(d.get('story',''))}</p>
        {f'<p>{E(d["what"])}</p>' if d.get('what') else ''}
        {f'<p class="mu-a">{E(d["address"])}</p>' if d.get('address') else ''}
        <p class="mu-acts">{' · '.join(acts)}</p>
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
def rec(d):
    who = f' · {E(d["contributor"])}' if d.get('contributor') else ''
    src = f'<a href="{E(d["url"])}" rel="noopener">{E(d["source_title"])}</a>' if d.get('url') else E(d['source_title'])
    return f'''<li class="rc" id="{slug(d['title'])}" data-kind="{d['kind']}">
        <p class="mu-k">{'Household hint' if d['kind']=='hint' else 'Recipe'} · {E(d.get('source_place') or '')}{(', '+E(str(d['year']))) if d.get('year') else ''}</p>
        <h3>{E(d['title'])}</h3>
        <blockquote class="rc-t">{E(d['text'])}</blockquote>
        <p class="rc-src">From {src}{who}</p>
        {f'<details class="rc-m"><summary>Making it today</summary><p>{E(d["modern"])}</p></details>' if d.get('modern') else ''}
      </li>'''
recipes = ''.join(rec(d) for d in R if d['kind']=='recipe') + ''.join(rec(d) for d in R if d['kind']=='hint')
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
  var items=$$('.fd'), q=$('#fdQ'), cs=$('#fdC'), tys=$$('.fd-f'), cnt=$('#fdCount'), ty='', map=null, marks=[], showMu=false, mu=[];
  var draw=function(){ var w=q.value.trim().toLowerCase().split(/\s+/).filter(Boolean), c=cs.value, n=0;
    items.forEach(function(li){ var ok=(!ty||li.dataset.ty===ty) && (!c||li.dataset.c===c) && w.every(function(x){ return li.dataset.t.indexOf(x)>=0; }); li.hidden=!ok; if (ok) n++; });
    $$('.fd-sec').forEach(function(s){ s.hidden=!s.querySelector('.fd:not([hidden])'); });
    $$('.fd-sec h3.fd-st').forEach(function(h){ var ul=h.nextElementSibling; h.hidden=h.classList.contains('gone') || !ul.querySelector('.fd:not([hidden])'); });
    cnt.textContent=n===items.length? n+' places' : n+' of '+items.length+' places';
    if (map) pins(); };
  tys.forEach(function(b){ b.addEventListener('click',function(){ ty=b.dataset.ty; tys.forEach(function(x){ x.setAttribute('aria-pressed',String(x===b)); }); draw(); }); });
  q.addEventListener('input',draw); cs.addEventListener('change',draw);
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
  draw();
  var h=location.hash.slice(1), t=h && document.getElementById(h); if (t && t.classList.contains('fd')) setTimeout(function(){ go(t); },300);
})();
</script>'''
FIELDS = [
  ('The fruit belt', 'Along the Lake Michigan shore the big lake keeps spring frosts back and autumn warm, and for well over a century the counties near it have grown apples, peaches, cherries, grapes and blueberries. Many of the valley’s festivals are harvest festivals.', '/seasons/#summer', 'Harvest festivals by season'),
  ('Mills on every stream', 'Before the railroads, every town needed a grist mill to grind its wheat and corn, and most of the valley’s early towns grew up beside one. A few still stand, and one or two still grind.', '/roads-and-rails/', 'Roads, rails and mills'),
  ('Celery and the muck lands', 'Kalamazoo’s low, black “muck” soil made it famous for celery from the late 1800s. The Celery Flats Historical Area in Portage keeps the story.', '/museums/#celery-flats-historical-area', 'Celery Flats in the museums directory'),
  ('The stove in the kitchen', 'Dowagiac’s Round Oak stoves heated and cooked for farm kitchens across the country. The Dowagiac Area History Museum tells the story.', '/museums/#dowagiac-area-history-museum', 'Dowagiac Area History Museum'),
]
fields = ''.join(f'<li class="fd-fi"><h3>{E(t)}</h3><p>{E(d)}</p><p><a href="{u}">{E(l)} ›</a></p></li>' for t,d,u,l in FIELDS)
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Food, recipes &amp; lodging</p>
    <figure class="pg-art"><picture><source type="image/avif" srcset="/img/card-food-art-270.avif 270w, /img/card-food-art.avif 540w" sizes="8rem"><img class="vt-food" src="/img/card-food-art-270.webp" srcset="/img/card-food-art-270.webp 270w, /img/card-food-art.webp 540w" sizes="8rem" width="540" height="960" alt="" decoding="async"></picture></figure>
    <h1>A table and a bed in the valley</h1>
    <p class="lede" style="font-size:1.15rem">Where to eat and where to stay, chosen for their stories: dining rooms in old banks and depots, family tables that have fed a town for generations, inns in houses built before the railroad came. And from the old cookbooks and weekly papers, what the valley cooked.</p>
    <p class="nm-chips fd-jump"><a class="btn" href="#eat">Places to eat</a><a class="btn" href="#stay">Places to stay</a><a class="btn" href="#recipes">The valley kitchen</a><a class="btn" href="#fields">Where the food came from</a></p>
    <div class="mu-bar">
      <label class="nm-q"><span>Find a place</span><input type="search" id="fdQ" placeholder="A town, a kind of place, a building" autocomplete="off" spellcheck="false"></label>
      <div class="nm-chips" role="group" aria-label="Show one kind"><button type="button" class="btn fd-f" data-ty="" aria-pressed="true">Everything</button><button type="button" class="btn fd-f" data-ty="restaurant" aria-pressed="false">Places to eat</button><button type="button" class="btn fd-f" data-ty="lodging" aria-pressed="false">Places to stay</button><button type="button" class="btn" id="fdNear" aria-pressed="false">Nearest to me</button><label class="mu-ol"><span class="vh">County</span><select id="fdC"><option value="">Every county</option>{copts}</select></label></div>
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
      <p>Recipes and household hints as they were printed in the valley’s own cookbooks and newspapers, word for word, with a note on how to make each one today. Tick the ones you have cooked: one earns a badge for your <a href="/badges/">field book</a>.</p>
      <ul class="rc-list">{recipes}</ul></section>
    <section id="fields"><h2>Where the food came from</h2><ul class="fd-fields">{fields}</ul></section>
    <h2>Before you go</h2>
    <ul class="dis">
      <li><b>Call or check first.</b> Hours change with the seasons, and small places close for holidays and family days.</li>
      <li><b>Make a day of it.</b> Pair a meal with the <a href="/museums/">museums nearby</a>, the <a href="/walk/">Broadway walk</a> or a <a href="/seasons/">festival</a>.</li>
      <li><b>Know a place with a story?</b> <a href="/#contact">Tell us</a>, with what you know of its history.</li>
      <li><b>Own one of these places?</b> Project Scroll is free to play and depends on sponsors. <a href="/sponsors/">See how to keep the lanterns lit</a>.</li>
    </ul>
    <p class="vs-plan"><a class="btn" href="/visit/">Plan your visit: ready-made days out, food, lodging and festivals</a></p>
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
