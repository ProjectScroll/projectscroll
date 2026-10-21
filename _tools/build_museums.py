"""Museums, historic places and research rooms of the valley: a directory by county, with a map and a trip list.
python3 _tools/build_museums.py   (data in _tools/data/museums.json, every entry checked against its own website;
the map's county outlines are in museums/base.json, from the US Census county outlines and the valley model's rivers)"""
import sys, pathlib, json, html, re, urllib.parse
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E = html.escape
D = json.load(open(pathlib.Path(__file__).parent/'data'/'museums.json'))
ORDER = [('Cass','MI'),('Berrien','MI'),('Van Buren','MI'),('St. Joseph','MI'),('Kalamazoo','MI'),('St. Joseph','IN'),('Elkhart','IN'),('LaGrange','IN'),('LaPorte','IN')]
KIND = {'museum':'Museum','historic house':'Historic house','historic site':'Historic site','historical society':'Society','library local history':'Library history room','library':'Library','archive':'Archive'}
# the towns that have an old-map page on this site
OLDMAP = {'Cassopolis':('cassopolis','1860'),'Dowagiac':('dowagiac','1860'),'Niles':('niles','1860'),'Paw Paw':('paw-paw','1860'),'South Bend':('south-bend','1863'),'Elkhart':('elkhart','1861'),'Goshen':('goshen','1861')}
PHOTO = {'Pioneer Log Cabin Museum':('/img/visit/log-cabin-600.webp','The Pioneer Log Cabin Museum: a log building with a porch sign, flower beds and autumn maples')}
SKIP = re.compile(r'(wikipedia|rootsweb|third-party|i could|not seen|see report|blocked|fetch|sbags|directory page|from the page|from a |per a |migenweb|official home page|community directory|not to be confused|county coverage|is in massachusetts)', re.I)
NOADDR = re.compile(r'(p\.o\. box|no street address)', re.I)
def when(n):
    parts = [p.strip() for p in re.split(r'(?<=[.;])\s+', n or '') if p.strip()]
    return ' '.join(p for p in parts if not SKIP.search(p))
def norm_county(d):
    c = d['county'].split(' (')[0]
    return (c if c != 'Regional' else 'Kalamazoo', d['state'])
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
groups = {}
for d in D: groups.setdefault(norm_county(d), []).append(d)
keys = [k for k in ORDER if k in groups] + [k for k in groups if k not in ORDER]
ST = {'MI':'Michigan','IN':'Indiana'}
def cid(k): return re.sub(r'[^a-z]+','-',(k[0]+'-'+k[1]).lower()).strip('-')
used = set()
for d in D:
    s = slug(d['name']);
    if s in used: s = slug(d['name']+' '+d['town'])
    used.add(s); d['_id'] = s
def clean_addr(a): return re.sub(r'\s*\((?:mailing|mail:)[^)]*\)', '', a).strip()
def directions(d):
    a = clean_addr(d['address'])
    if NOADDR.search(a): return ''
    if d.get('ll') and (d.get('approx') or not re.match(r'^\d', a)):
        dest = d['name']+', '+d['town'].split(' (')[0].split(' /')[0]+', '+ST[d['state']]
    else:
        dest = d['name']+', '+clean_addr(a.split(' (')[0])
    return 'https://www.google.com/maps/dir/?api=1&destination='+urllib.parse.quote(dest)
def card(d):
    w = d['hours'] if 'hours' in d else when(d.get('note'))
    url = d.get('url'); di = directions(d)
    acts = []
    acts.append(f'<a class="mu-go" href="{E(url)}" rel="noopener">Their website ›</a>' if url else '<span class="mu-go mu-none">No website: check locally</span>')
    if di: acts.append(f'<a class="mu-dir" href="{E(di)}" rel="noopener" data-dest="{E(di.split("destination=")[1])}">Directions</a>')
    town = d['town'].split(' (')[0].split(' /')[0]
    if town in OLDMAP:
        p, y = OLDMAP[town]; acts.append(f'<a class="mu-old" href="/map/{p}/">{E(town)} on the {y} map</a>')
    chk = '' if d.get('verified') else '<span class="mu-chk" title="We could not confirm this one online. Check before you travel.">check before you go</span>'
    ph = PHOTO.get(d['name'])
    img = f'<img class="mu-ph" src="{ph[0]}" alt="{E(ph[1])}" width="600" height="338" loading="lazy" decoding="async">' if ph else ''
    ll = f' data-ll="{d["ll"][0]},{d["ll"][1]}"' + (' data-approx="1"' if d.get('approx') else '') if d.get('ll') else ''
    research = ' data-r="1"' if d.get('research') else ''
    return f'''<li class="mu" id="{d['_id']}" data-k="{E(d['kind'])}"{ll}{research} data-n="{E(d['name'])}" data-town="{E(d['town'])}" data-t="{E((d['name']+' '+d['town']+' '+d['what']+' '+d.get('research','')+' '+d['county']).lower())}">
        {img}<p class="mu-k">{E(KIND.get(d['kind'], d['kind']))} · {E(d['town'])}<span class="mu-dist"></span>{chk}</p>
        <h3>{E(d['name'])}</h3>
        <p>{E(d['what'])}</p>
        {f'<p class="mu-r"><b>For researchers:</b> {E(d["research"])}</p>' if d.get('research') else ''}
        {f'<p class="mu-w">{E(w)}</p>' if w else ''}
        <p class="mu-a">{E(clean_addr(d['address']))}</p>
        <p class="mu-acts">{' · '.join(acts)}</p>
        <p class="mu-me"><button type="button" class="mu-tb" aria-pressed="false">Add to my trip</button><button type="button" class="mu-bb" aria-pressed="false">Been there</button></p>
      </li>'''
sections = ''.join(f'''    <section class="mu-c" id="{cid(k)}"><h2>{E(k[0])} County, {ST[k[1]]} <span class="mu-n">{len(groups[k])} places</span></h2>
      <ul class="mu-list">{''.join(card(d) for d in sorted(groups[k], key=lambda x:(x['town'], x['name'])))}</ul></section>
''' for k in keys)
chips = ''.join(f'<a class="btn mu-cj" href="#{cid(k)}">{E(k[0])}, {k[1]} <span>{len(groups[k])}</span></a>' for k in keys)
kinds = ''.join(f'<button type="button" class="btn mu-f" data-k="{k}" aria-pressed="false">{v}</button>' for k,v in KIND.items())
n = len(D); nmap = sum(1 for d in D if d.get('ll'))
# search engines: the directory as a list of places
TYPE = {'museum':'Museum','historic house':'LandmarksOrHistoricalBuildings','historic site':'LandmarksOrHistoricalBuildings','library local history':'Library','library':'Library','archive':'ArchiveOrganization','historical society':'Organization'}
items = []
for i, d in enumerate([d for k in keys for d in sorted(groups[k], key=lambda x:(x['town'], x['name']))], 1):
    it = {'@type': TYPE.get(d['kind'], 'Place'), 'name': d['name'], 'description': d['what'],
          'url': 'https://projectscroll.com/museums/#'+d['_id']}
    if d.get('url'): it['sameAs'] = d['url']
    if re.match(r'^\d', clean_addr(d['address'])): it['address'] = {'@type':'PostalAddress','streetAddress':clean_addr(d['address']).split(',')[0],'addressLocality':d['town'].split(' (')[0].split(' /')[0],'addressRegion':d['state'],'addressCountry':'US'}
    if d.get('ll') and not d.get('approx'): it['geo'] = {'@type':'GeoCoordinates','latitude':d['ll'][0],'longitude':d['ll'][1]}
    items.append({'@type':'ListItem','position':i,'item':it})
ld = '<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@type':'ItemList','name':'Museums & historic places of the St. Joseph River valley','numberOfItems':n,'itemListElement':items}, ensure_ascii=False).replace('</','<\\/')+'</script>'

JS = r'''<script>
(function(){ "use strict";
  var $=function(s,r){ return (r||document).querySelector(s); }, $$=function(s,r){ return [].slice.call((r||document).querySelectorAll(s)); };
  var q=$('#muQ'), cnt=$('#muCount'), items=$$('.mu'), fs=$$('.mu-f'), kind='', research=false, near=null, store=true;
  var load=function(k){ try{ return JSON.parse(localStorage.getItem(k)||'[]')||[]; }catch(e){ store=false; return []; } };
  var save=function(k,v){ try{ localStorage.setItem(k,JSON.stringify(v)); }catch(e){} };
  var trip=load('ps-mu-trip'), been=load('ps-mu-been');
  var byId={}; items.forEach(function(li,i){ byId[li.id]=li; li._p=li.parentNode; li._i=i; });
  trip=trip.filter(function(id){ return byId[id]; }); been=been.filter(function(id){ return byId[id]; });
  /* ---- filtering ---- */
  var markers=[], map=null;
  var visible=function(li){ var w=q.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    return (!kind||li.dataset.k===kind) && (!research||li.dataset.r==='1') && w.every(function(x){ return li.dataset.t.indexOf(x)>=0; }); };
  var draw=function(fit){ var n=0;
    items.forEach(function(li){ var ok=visible(li); li.hidden=!ok; if (ok) n++; });
    $$('.mu-c').forEach(function(s){ s.hidden=!s.querySelector('.mu:not([hidden])'); });
    cnt.textContent=n===items.length? n+' places' : n+' of '+items.length+' places';
    if (map) drawMarkers(fit); };
  fs.forEach(function(b){ b.addEventListener('click',function(){ kind=b.dataset.k; fs.forEach(function(x){ x.setAttribute('aria-pressed',String(x===b)); }); draw(true); }); });
  var rb=$('#muR'); rb.addEventListener('click',function(){ research=!research; rb.setAttribute('aria-pressed',String(research)); draw(true); });
  var tm; q.addEventListener('input',function(){ clearTimeout(tm); draw(false); tm=setTimeout(function(){ draw(true); },500); });
  /* ---- near me: one list, nearest first; the position never leaves this device ---- */
  var nb=$('#muNear'), nsec=$('#muNearSec'), nlist=$('#muNearList'), nmsg=$('#muNearMsg');
  var km=function(a,b){ var R=6371, r=Math.PI/180, dl=(b[0]-a[0])*r, dn=(b[1]-a[1])*r, h=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a[0]*r)*Math.cos(b[0]*r)*Math.sin(dn/2)*Math.sin(dn/2); return 2*R*Math.asin(Math.sqrt(h)); };
  var nearOff=function(){ near=null; nsec.hidden=true; nb.setAttribute('aria-pressed','false'); nb.textContent='Sort by distance from me';
    items.forEach(function(li){ li._p.appendChild(li); var s=li.querySelector('.mu-dist'); s.textContent=''; }); draw(false); };
  var nearOn=function(p){ near=p; var withLL=items.filter(function(li){ return li.dataset.ll; });
    withLL.forEach(function(li){ li._d=km(p, li.dataset.ll.split(',').map(Number)); });
    withLL.sort(function(a,b){ return a._d-b._d; });
    withLL.forEach(function(li){ nlist.appendChild(li); var mi=li._d*0.621371; li.querySelector('.mu-dist').textContent=' · about '+(mi<10? mi.toFixed(1) : Math.round(mi))+' mi'+(li.dataset.approx?' (rough)':''); });
    nsec.hidden=false; nb.setAttribute('aria-pressed','true'); nb.textContent='Back to the counties'; draw(false);
    if (map){ if (!map._me) map._me=L.circleMarker(p,{radius:7, className:'mu-me-pt', interactive:false}).addTo(map); else map._me.setLatLng(p); }
    nsec.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth', block:'start'}); };
  nb.addEventListener('click',function(){ if (near){ nearOff(); return; }
    if (!navigator.geolocation){ nmsg.textContent='This browser cannot share a location. Use the county list instead.'; return; }
    nmsg.textContent='Asking your browser where you are…';
    navigator.geolocation.getCurrentPosition(function(pos){ nmsg.textContent='Sorted from where you are now. Your location stays on this device.'; nearOn([pos.coords.latitude,pos.coords.longitude]); },
      function(){ nmsg.textContent='No location shared, so nothing changed. Use the county list instead.'; }, {maximumAge:600000, timeout:15000}); });
  /* ---- my trip and been there ---- */
  var tp=$('#muTrip'), tl=$('#muTripList'), tc=$('#muTripN'), td=$('#muTripDir'), bc=$('#muBeenN');
  var paint=function(){
    items.forEach(function(li){ var t=trip.indexOf(li.id)>=0, b=been.indexOf(li.id)>=0, tb=li.querySelector('.mu-tb'), bb=li.querySelector('.mu-bb');
      tb.setAttribute('aria-pressed',String(t)); tb.textContent=t?'On my trip ✓':'Add to my trip'; bb.setAttribute('aria-pressed',String(b)); bb.textContent=b?'Been there ✓':'Been there';
      li.classList.toggle('on-trip',t); li.classList.toggle('was',b); });
    tc.textContent=trip.length; tp.hidden=!trip.length;
    tl.innerHTML=''; trip.forEach(function(id,i){ var li=byId[id], r=document.createElement('li');
      var a=document.createElement('a'); a.href='#'+id; a.textContent=li.dataset.n; r.appendChild(a);
      var t=document.createElement('span'); t.className='mu-tt'; t.textContent=' · '+li.dataset.town; r.appendChild(t);
      var up=document.createElement('button'); up.type='button'; up.className='mu-up'; up.textContent='↑'; up.setAttribute('aria-label','Move '+li.dataset.n+' earlier'); up.disabled=i===0;
      up.addEventListener('click',function(){ trip.splice(i,1); trip.splice(i-1,0,id); save('ps-mu-trip',trip); paint(); tl.querySelectorAll('.mu-up')[Math.max(0,i-1)].focus(); }); r.appendChild(up);
      var x=document.createElement('button'); x.type='button'; x.className='mu-x'; x.textContent='×'; x.setAttribute('aria-label','Take '+li.dataset.n+' off my trip');
      x.addEventListener('click',function(){ trip.splice(i,1); save('ps-mu-trip',trip); paint(); }); r.appendChild(x);
      tl.appendChild(r); });
    var stops=trip.map(function(id){ var a=byId[id].querySelector('.mu-dir'); return a? a.dataset.dest : null; }).filter(Boolean).slice(0,10);
    if (stops.length){ var dest=stops[stops.length-1], way=stops.slice(0,-1);
      td.href='https://www.google.com/maps/dir/?api=1&destination='+dest+(way.length?'&waypoints='+way.join('%7C'):''); td.hidden=false;
      td.textContent=trip.length>10?'Directions for the first ten stops':'Directions for the whole trip'; } else td.hidden=true;
    bc.textContent=been.length? 'You have been to '+been.length+' of '+items.length+' places.' : '';
    if (map) drawMarkers(false); };
  items.forEach(function(li){
    li.querySelector('.mu-tb').addEventListener('click',function(){ var i=trip.indexOf(li.id); if (i>=0) trip.splice(i,1); else trip.push(li.id); save('ps-mu-trip',trip); paint(); });
    li.querySelector('.mu-bb').addEventListener('click',function(){ var i=been.indexOf(li.id); if (i>=0) been.splice(i,1); else been.push(li.id); save('ps-mu-been',been); paint();
      if (been.length>=3 && window.psEarn) window.psEarn('visitor'); }); });
  $('#muTripClear').addEventListener('click',function(){ trip=[]; save('ps-mu-trip',trip); paint(); q.focus(); });
  $('#muTripPrint').addEventListener('click',function(){ document.documentElement.classList.add('mu-printtrip'); window.print(); });
  window.addEventListener('afterprint',function(){ document.documentElement.classList.remove('mu-printtrip'); });
  if (!store) $('#muMine').hidden=true;
  /* ---- the map: county outlines drawn here, no outside map unless the reader turns it on ---- */
  var box=$('#muMap'), stat=$('#muMapStat');
  var go=function(li){ if (li.hidden){ kind=''; research=false; q.value=''; fs.forEach(function(x){ x.setAttribute('aria-pressed',String(!x.dataset.k)); }); rb.setAttribute('aria-pressed','false'); draw(false); }
    li.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth', block:'center'});
    li.classList.remove('flash'); void li.offsetWidth; li.classList.add('flash'); var h=li.querySelector('h3'); h.tabIndex=-1; h.focus({preventScroll:true}); };
  var drawMarkers=function(fit){ var vis=[];
    markers.forEach(function(m){ var any=m.lis.filter(function(li){ return !li.hidden; });
      if (any.length){ if (!map.hasLayer(m.c)) m.c.addTo(map); vis.push(m.c.getLatLng());
        var t=any.some(function(li){ return li.classList.contains('on-trip'); }), b=any.every(function(li){ return li.classList.contains('was'); });
        var el=m.c.getElement(); if (el){ el.classList.toggle('t',t); el.classList.toggle('b',b); } }
      else if (map.hasLayer(m.c)) map.removeLayer(m.c); });
    if (fit){ if (!kind && !research && !q.value.trim()) map.fitBounds(map._home); else if (vis.length) map.fitBounds(L.latLngBounds(vis).pad(.25),{maxZoom:12}); }
    stat.textContent=vis.length? vis.length+' map pins showing' : 'No pins match';
  };
  var start=function(){ if (map || !window.L) return;
    map=L.map(box,{zoomSnap:.25, minZoom:7, maxZoom:17, scrollWheelZoom:false, attributionControl:true, maxBounds:[[40.9,-87.9],[42.95,-84.3]]});
    map.attributionControl.setPrefix(false);
    map._home=L.latLngBounds([[41.42,-86.95],[42.43,-85.35]]); map.fitBounds(map._home);
    map.on('focus click',function(){ map.scrollWheelZoom.enable(); }); map.on('blur mouseout',function(){ map.scrollWheelZoom.disable(); });
    fetch('/museums/base.json?v=1').then(function(r){ return r.json(); }).then(function(b){
      var pane=map.createPane('base'); pane.style.zIndex=250;
      b.c.forEach(function(c){ c.r.forEach(function(r){ L.polygon(r.map(function(p){ return [p[1],p[0]]; }),{pane:'base', className:c.d?'mu-cty in':'mu-cty', interactive:false}).addTo(map); });
        if (c.d){ var bb=L.polygon(c.r[0].map(function(p){ return [p[1],p[0]]; })).getBounds(); L.marker(bb.getCenter(),{pane:'base', interactive:false, keyboard:false, icon:L.divIcon({className:'mu-cl', html:c.n+'<br>'+c.s, iconSize:[90,26], iconAnchor:[45,13]})}).addTo(map); } });
      L.polygon(b.w.map(function(p){ return [p[1],p[0]]; }),{pane:'base', className:'mu-ws', interactive:false, fill:false}).addTo(map);
      b.v.forEach(function(l){ L.polyline(l.map(function(p){ return [p[1],p[0]]; }),{pane:'base', className:'mu-rv', interactive:false}).addTo(map); });
      map.attributionControl.addAttribution('County lines: US Census Bureau · Rivers: USGS');
    }).catch(function(){});
    var at={};
    items.forEach(function(li){ if (!li.dataset.ll) return; var k=li.dataset.ll; (at[k]=at[k]||[]).push(li); });
    Object.keys(at).forEach(function(k){ var lis=at[k], ll=k.split(',').map(Number), lib=/library|archive|society/.test(lis[0].dataset.k);
      var c=L.circleMarker(ll,{radius:7, className:'mu-pin'+(lib?' lib':''), bubblingMouseEvents:false});
      var div=document.createElement('div'); div.className='mu-pop';
      lis.forEach(function(li){ var p=document.createElement('p'); var s=document.createElement('span'); s.className='mu-pk'; s.textContent=li.querySelector('.mu-k').firstChild.textContent; p.appendChild(s);
        var bt=document.createElement('button'); bt.type='button'; bt.textContent=li.dataset.n+' ›'; bt.addEventListener('click',function(){ map.closePopup(); go(li); }); p.appendChild(bt);
        if (li.dataset.approx){ var a=document.createElement('small'); a.textContent='Pin is near, not exact.'; p.appendChild(a); } div.appendChild(p); });
      c.bindPopup(div,{maxWidth:260}); c.bindTooltip(lis.map(function(li){ return li.dataset.n; }).join(' · '),{direction:'top', offset:[0,-6]});
      markers.push({c:c, lis:lis}); });
    draw(false); paint(); if (near) nearOn(near);
    var osm=null, sb=$('#muOSM');
    sb.hidden=false; sb.addEventListener('click',function(){ var on=sb.getAttribute('aria-pressed')!=='true'; sb.setAttribute('aria-pressed',String(on));
      if (on){ if (!osm) osm=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19, attribution:'Streets: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}); osm.addTo(map); box.classList.add('osm'); }
      else { map.removeLayer(osm); box.classList.remove('osm'); } });
    $('#muHome').hidden=false; $('#muHome').addEventListener('click',function(){ map.fitBounds(map._home); });
  };
  var need=function(){ if (window.L){ start(); return; }
    var l=document.createElement('link'); l.rel='stylesheet'; l.href='/vendor/leaflet-1.9.4/leaflet.css?v=1'; document.head.appendChild(l);
    var s=document.createElement('script'); s.src='/vendor/leaflet-1.9.4/leaflet.js?v=1'; s.onload=start; s.onerror=function(){ stat.textContent='The map could not load. The list below has every place.'; }; document.head.appendChild(s); };
  if ('IntersectionObserver' in window){ var io=new IntersectionObserver(function(e){ if (e.some(function(x){ return x.isIntersecting; })){ io.disconnect(); need(); } },{rootMargin:'300px'}); io.observe(box); } else need();
  paint();
  /* a link to one place (from the map, or shared) lights it up */
  var h=location.hash.slice(1); if (h && byId[h]) setTimeout(function(){ go(byId[h]); },300);
})();
</script>'''

body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Museums &amp; historic places</p>
    <h1>Where the valley keeps its past</h1>
    <p class="lede" style="font-size:1.15rem">{n} museums, historic houses, libraries, research rooms and archives across the St. Joseph River valley and its neighbours, from the log cabin in Cassopolis to the Studebaker collection in South Bend. The hunt starts on this website. It finishes in places like these.</p>
    <div class="mu-bar">
      <label class="nm-q"><span>Find a place</span><input type="search" id="muQ" placeholder="A town, a museum or a subject" autocomplete="off" spellcheck="false"></label>
      <div class="nm-chips" role="group" aria-label="Show one kind of place"><button type="button" class="btn mu-f" data-k="" aria-pressed="true">Everything</button>{kinds}</div>
      <div class="nm-chips mu-opts"><button type="button" class="btn mu-rb" id="muR" aria-pressed="false">Help for researchers</button><button type="button" class="btn mu-nb" id="muNear" aria-pressed="false">Sort by distance from me</button></div>
      <p class="mu-nmsg" id="muNearMsg" aria-live="polite"></p>
      <p class="nm-chips mu-jump"><span class="mu-jl">Jump to a county:</span> {chips}</p>
      <p class="nm-count" id="muCount" aria-live="polite">{n} places</p>
    </div>
    <figure class="mu-mapf">
      <div class="mu-map" id="muMap" role="region" aria-label="Map of the places in this directory. Every place is also in the list below.">
        <p class="mu-mapph">The map of all {nmap} places opens here.</p>
      </div>
      <figcaption><span class="mu-lg"><i class="mu-dot"></i> Museum, house or site</span> <span class="mu-lg"><i class="mu-dot lib"></i> Library, archive or society</span> <span class="mu-lg"><i class="mu-dot t"></i> On my trip</span>
        <button type="button" class="btn mu-osm" id="muOSM" aria-pressed="false" hidden>Show today’s streets</button> <button type="button" class="btn" id="muHome" hidden>Whole valley</button>
        <span class="mu-stat" id="muMapStat" aria-live="polite"></span></figcaption>
    </figure>
    <aside class="mu-trip" id="muTrip" hidden aria-labelledby="muTripH">
      <h2 id="muTripH">My trip <span class="mu-n"><span id="muTripN">0</span> stops</span></h2>
      <ol id="muTripList"></ol>
      <p class="mu-tacts"><a class="btn" id="muTripDir" href="#" rel="noopener" hidden>Directions for the whole trip</a> <button type="button" class="btn" id="muTripPrint">Print my trip</button> <button type="button" class="btn" id="muTripClear">Clear the trip</button></p>
      <p class="note">Your trip list stays in this browser. Directions open Google Maps, starting from wherever you are.</p>
    </aside>
    <p class="mu-mine" id="muMine"><span id="muBeenN"></span></p>
    <section class="mu-c mu-near" id="muNearSec" hidden><h2>Nearest to you</h2><ul class="mu-list" id="muNearList"></ul></section>
{sections}
    <h2>Before you go</h2>
    <ul class="dis">
      <li><b>Check the hours.</b> Many of these places are run by volunteers and open only some days or some seasons. Their own websites have the latest.</li>
      <li><b>Researchers, write ahead.</b> Archives and research rooms often keep their records off the floor. A note a week before lets them have your boxes ready.</li>
      <li><b>Bring what you know.</b> Names, dates, the township, and a copy of anything you found here. Staff can do far more with a good question.</li>
      <li><b>Make a day of it.</b> Add a few places to <i>My trip</i>, then use “Directions for the whole trip”. Mark the ones you have seen with “Been there”: three earns a badge for your <a href="/badges/">field book</a>.</li>
      <li><b>Know of a place we missed?</b> <a href="/#contact">Tell us</a> and we will add it.</li>
    </ul>
    <p class="note">Every place on this page was checked against its own website, or a city, county, library or university page about it, in October 2026. Places marked “check before you go” could not be confirmed online. Hours change: always look at the place’s own site before travelling. Map pins come from each street address; a few pins marked “near, not exact” sit at the town or road. The map draws its own county lines (US Census Bureau) and rivers (USGS). Only if you press “Show today’s streets” does your browser ask OpenStreetMap’s tile server for street maps, under <a href="https://osmfoundation.org/wiki/Privacy_Policy" rel="noopener">its privacy policy</a>. “Sort by distance” asks your browser for your location and uses it only on this page.</p>
{ld}
{JS}
'''
page('museums/index.html', 'Museums & historic places of the valley · Project Scroll',
     f'{n} museums, historic houses, research rooms and archives across the St. Joseph River valley in Michigan and Indiana, with a map, directions and a trip planner, each checked against its own website.',
     body, og='https://projectscroll.com/og/records.jpg')
print('museums built', n, len(keys), 'counties', nmap, 'on the map')
