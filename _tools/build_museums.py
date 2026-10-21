"""Museums, historic places and research rooms of the valley: a directory by county, with a map and a trip list.
python3 _tools/build_museums.py   (data in _tools/data/museums.json, every entry checked against its own website;
the map's county outlines are in museums/base.json, from the US Census county outlines and the valley model's rivers)"""
import sys, pathlib, json, html, re, urllib.parse
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E = html.escape
D = json.load(open(pathlib.Path(__file__).parent/'data'/'museums.json'))
ORDER = [('Cass','MI'),('Berrien','MI'),('Van Buren','MI'),('St. Joseph','MI'),('Kalamazoo','MI'),('Barry','MI'),('St. Joseph','IN'),('Elkhart','IN'),('LaGrange','IN'),('LaPorte','IN')]
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
    if d.get('ll'): acts.append('<button type="button" class="mu-sm">Show on the map</button>')
    chk = '' if d.get('verified') else '<span class="mu-chk" title="We could not confirm this one online. Check before you travel.">check before you go</span>'
    ph = PHOTO.get(d['name'])
    img = f'<img class="mu-ph" src="{ph[0]}" alt="{E(ph[1])}" width="600" height="338" loading="lazy" decoding="async">' if ph else ''
    ll = f' data-ll="{d["ll"][0]},{d["ll"][1]}"' + (' data-approx="1"' if d.get('approx') else '') if d.get('ll') else ''
    research = ' data-r="1"' if d.get('research') else ''
    research += (f' data-oh="{E(d["oh"])}"' if d.get('oh') else '') + (' data-tz="C"' if d.get('tz') == 'C' else '')
    return f'''<li class="mu" id="{d['_id']}" data-k="{E(d['kind'])}"{ll}{research} data-n="{E(d['name'])}" data-town="{E(d['town'])}" data-t="{E((d['name']+' '+d['town']+' '+d['what']+' '+d.get('research','')+' '+d['county']).lower())}">
        {img}<p class="mu-k">{E(KIND.get(d['kind'], d['kind']))} · {E(d['town'])}<span class="mu-dist"></span>{chk}</p>
        <h3>{E(d['name'])}</h3>
        <p>{E(d['what'])}</p>
        {f'<p class="mu-r"><b>For researchers:</b> {E(d["research"])}</p>' if d.get('research') else ''}
        {f'<p class="mu-w">{E(w)}</p>' if w else ''}{'<p class="mu-open" aria-live="off"></p>' if d.get('oh') else ''}
        <p class="mu-a">{E(clean_addr(d['address']))}</p>
        <p class="mu-acts">{' · '.join(acts)}</p>
        <p class="mu-me"><button type="button" class="mu-tb" aria-pressed="false">Add to my trip</button><button type="button" class="mu-bb" aria-pressed="false">Been there</button>{'<button type="button" class="mu-sb" hidden>I’m here: stamp it</button>' if d.get('ll') else ''}</p>
        <p class="mu-msg" aria-live="polite"></p>
      </li>'''
sections = ''.join(f'''    <section class="mu-c" id="{cid(k)}"><h2>{E(k[0])} County, {ST[k[1]]} <span class="mu-n">{len(groups[k])} places</span></h2>
      <ul class="mu-list">{''.join(card(d) for d in sorted(groups[k], key=lambda x:(x['town'], x['name'])))}</ul></section>
''' for k in keys)
chips = ''.join(f'<a class="btn mu-cj" href="#{cid(k)}">{E(k[0])}, {k[1]} <span>{len(groups[k])}</span></a>' for k in keys)
kinds = ''.join(f'<button type="button" class="btn mu-f" data-k="{k}" aria-pressed="false">{v}</button>' for k,v in KIND.items())
n = len(D); nmap = sum(1 for d in D if d.get('ll'))
TRIPS = [
  ('Studebaker and South Bend', 'Wagons, cars and the families who built them, all within a few blocks of the river.', [31, 29, 30, 39, 83]),
  ('A Cass County loop', 'The county seat and the towns around it: a cabin, a stove town, a fishing-lure maker and an old filling station.', [3, 55, 6, 2, 53, 0, 7]),
  ('Niles and the river', 'Fort St. Joseph, the four flags and the mills and courthouse down the St. Joseph.', [8, 9, 10, 15, 12]),
  ('Lighthouses and the lake shore', 'From Michigan City up the shore to South Haven: lights, railroads and the people of the big lake.', [70, 69, 76, 78, 21]),
  ('Amish country', 'Shipshewana, Middlebury, Bristol and Nappanee: the plain people, a mill and a kitchen-cabinet town.', [73, 74, 92, 50, 91]),
  ('A Kalamazoo day', 'The valley’s big neighbour: its museum, its park, its old cemetery and an air museum to finish.', [56, 65, 64, 58, 57]),
]
dts = ''.join(f'''<li class="mu-dt"><h3>{E(t)}</h3><p>{E(b)}</p><ol>{''.join(f'<li><a href="#{D[i]["_id"]}">{E(D[i]["name"])}</a></li>' for i in ix)}</ol>
        <p><button type="button" class="btn mu-dtb" data-ids="{'.'.join(D[i]['_id'] for i in ix)}">Load this day trip</button></p></li>''' for t, b, ix in TRIPS)
DAYS = ['Sundays','Mondays','Tuesdays','Wednesdays','Thursdays','Fridays','Saturdays']
opts = ''.join(f'<option value="{i}">open on {d}</option>' for i, d in enumerate(DAYS))
# search engines: the directory as a list of places
TYPE = {'museum':'Museum','historic house':'LandmarksOrHistoricalBuildings','historic site':'LandmarksOrHistoricalBuildings','library local history':'Library','library':'Library','archive':'ArchiveOrganization','historical society':'Organization'}
items = []
for i, d in enumerate([d for k in keys for d in sorted(groups[k], key=lambda x:(x['town'], x['name']))], 1):
    it = {'@type': TYPE.get(d['kind'], 'Place'), 'name': d['name'], 'description': d['what'],
          'url': 'https://projectscroll.com/museums/#'+d['_id']}
    if d.get('url'): it['sameAs'] = d['url']
    if re.match(r'^\d', clean_addr(d['address'])): it['address'] = {'@type':'PostalAddress','streetAddress':clean_addr(d['address']).split(',')[0],'addressLocality':d['town'].split(' (')[0].split(' /')[0],'addressRegion':d['state'],'addressCountry':'US'}
    if d.get('oh') and d['oh'] != 'always' and '@' not in d['oh']:
        hm = lambda x: f'{int(float(x)):02d}:{int(round((float(x)%1)*60)):02d}'
        it['openingHours'] = [seg.split()[0]+' '+'-'.join(hm(t) for t in seg.split()[1].split('-')) for seg in d['oh'].split('; ')]
    if d.get('ll') and not d.get('approx'): it['geo'] = {'@type':'GeoCoordinates','latitude':d['ll'][0],'longitude':d['ll'][1]}
    items.append({'@type':'ListItem','position':i,'item':it})
ld = '<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@type':'ItemList','name':'Museums & historic places of the St. Joseph River valley','numberOfItems':n,'itemListElement':items}, ensure_ascii=False).replace('</','<\\/')+'</script>'

JS = r'''<script>
(function(){ "use strict";
  var $=function(s,r){ return (r||document).querySelector(s); }, $$=function(s,r){ return [].slice.call((r||document).querySelectorAll(s)); };
  var calm=matchMedia('(prefers-reduced-motion: reduce)').matches, glide=calm?'auto':'smooth';
  var q=$('#muQ'), cnt=$('#muCount'), items=$$('.mu'), fs=$$('.mu-f'), sel=$('#muOpen'), kind='', research=false, openF='', near=null, store=true;
  var load=function(k,d){ try{ var v=JSON.parse(localStorage.getItem(k)||'null'); return v==null? d : v; }catch(e){ store=false; return d; } };
  var save=function(k,v){ try{ localStorage.setItem(k,JSON.stringify(v)); }catch(e){} };
  var trip=load('ps-mu-trip',[]), been=load('ps-mu-been',[]), stamp=load('ps-mu-stamp',{});
  var byId={}; items.forEach(function(li,i){ byId[li.id]=li; li._p=li.parentNode; li._i=i; });
  trip=trip.filter(function(id){ return byId[id]; }); been=been.filter(function(id){ return byId[id]; });
  var LL=function(li){ return li.dataset.ll? li.dataset.ll.split(',').map(Number) : null; };
  var km=function(a,b){ var R=6371, r=Math.PI/180, dl=(b[0]-a[0])*r, dn=(b[1]-a[1])*r, h=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a[0]*r)*Math.cos(b[0]*r)*Math.sin(dn/2)*Math.sin(dn/2); return 2*R*Math.asin(Math.sqrt(h)); };
  var miles=function(k){ var m=k*0.621371; return m<10? m.toFixed(1) : String(Math.round(m)); };

  /* ---- opening hours: read from each place's posted hours, in the place's own time zone ---- */
  var DN=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'], DK={Su:0,Mo:1,Tu:2,We:3,Th:4,Fr:5,Sa:6}, MN=['','January','February','March','April','May','June','July','August','September','October','November','December'];
  var parse=function(s){ if (s==='always') return {always:true}; var o={d:{}}, m=s.match(/@(\d+)-(\d+)/); if (m) o.season=[+m[1],+m[2]];
    s.replace(/@.*/,'').split(';').forEach(function(seg){ var p=seg.trim().split(' '); if (p.length<2) return; var h=p[1].split('-').map(Number);
      p[0].split(',').forEach(function(r){ var x=r.split('-'); if (x.length===2){ for (var i=DK[x[0]]; ; i=(i+1)%7){ o.d[i]=h; if (i===DK[x[1]]) break; } } else o.d[DK[r]]=h; }); });
    return o; };
  var clock=function(h){ var hh=Math.floor(h), mm=Math.round((h-hh)*60); if (hh===12 && !mm) return 'noon'; return (hh%12||12)+(mm?':'+('0'+mm).slice(-2):'')+(hh<12?' am':' pm'); };
  var nowAt=function(tz){ var p={}; new Intl.DateTimeFormat('en-US',{timeZone:tz==='C'?'America/Chicago':'America/Detroit', weekday:'short', month:'numeric', hour:'numeric', minute:'numeric', hourCycle:'h23'}).formatToParts(new Date()).forEach(function(x){ p[x.type]=x.value; });
    return {dow:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(p.weekday), mon:+p.month, h:(+p.hour%24)+(+p.minute)/60}; };
  var inSeason=function(o,mon){ return !o.season || (mon>=o.season[0] && mon<=o.season[1]); };
  items.forEach(function(li){ if (li.dataset.oh) li._oh=parse(li.dataset.oh); });
  var state=function(li){ var o=li._oh; if (!o) return null; if (o.always) return {open:true, today:true, txt:'Open grounds, every day'};
    var n=nowAt(li.dataset.tz), tz=li.dataset.tz==='C'?' Central':'';
    if (!inSeason(o,n.mon)) return {open:false, today:false, txt:'Closed for the season (open '+MN[o.season[0]]+' to '+MN[o.season[1]]+')'};
    var t=o.d[n.dow];
    if (t && n.h>=t[0] && n.h<t[1]) return {open:true, today:true, txt:'Open now, until '+clock(t[1])+tz};
    if (t && n.h<t[0]) return {open:false, today:true, txt:'Opens today at '+clock(t[0])+tz};
    for (var k=1;k<=7;k++){ var d=(n.dow+k)%7; if (o.d[d]) return {open:false, today:!!t, txt:(t?'Closed for today':'Closed today')+' · next open '+(k===1?'tomorrow':DN[d])+' at '+clock(o.d[d][0])+tz}; }
    return null; };
  var hours=function(){ items.forEach(function(li){ var e=li.querySelector('.mu-open'); if (!e) return; var s=state(li); e.textContent=s? s.txt : ''; e.classList.toggle('on', !!(s && s.open)); }); };

  /* ---- filtering ---- */
  var markers=[], map=null, group=null;
  var openOK=function(li){ if (!openF) return true; var o=li._oh; if (!o) return false; if (o.always) return true;
    if (openF==='now'){ var s=state(li); return !!(s && s.open); }
    if (openF==='today'){ var n=nowAt(li.dataset.tz); return inSeason(o,n.mon) && !!o.d[n.dow]; }
    return !!o.d[+openF]; };
  var visible=function(li){ var w=q.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    return (!kind||li.dataset.k===kind) && (!research||li.dataset.r==='1') && openOK(li) && w.every(function(x){ return li.dataset.t.indexOf(x)>=0; }); };
  var filtered=function(){ return !!(kind || research || openF || q.value.trim()); };
  var draw=function(fit){ var n=0;
    items.forEach(function(li){ var ok=visible(li); li.hidden=!ok; if (ok) n++; });
    $$('.mu-c').forEach(function(s){ s.hidden=!s.querySelector('.mu:not([hidden])'); });
    cnt.textContent=n===items.length? n+' places' : n+' of '+items.length+' places';
    if (map) drawMarkers(fit); };
  fs.forEach(function(b){ b.addEventListener('click',function(){ kind=b.dataset.k; fs.forEach(function(x){ x.setAttribute('aria-pressed',String(x===b)); }); draw(true); }); });
  var rb=$('#muR'); rb.addEventListener('click',function(){ research=!research; rb.setAttribute('aria-pressed',String(research)); draw(true); });
  sel.addEventListener('change',function(){ openF=sel.value; draw(true); });
  var tm; q.addEventListener('input',function(){ clearTimeout(tm); draw(false); tm=setTimeout(function(){ draw(true); },500); });

  /* ---- near me: one list, nearest first; the position never leaves this device ---- */
  var nb=$('#muNear'), nsec=$('#muNearSec'), nlist=$('#muNearList'), nmsg=$('#muNearMsg');
  var nearOff=function(){ near=null; nsec.hidden=true; nb.setAttribute('aria-pressed','false'); nb.textContent='Sort by distance from me';
    items.forEach(function(li){ li._p.appendChild(li); li.querySelector('.mu-dist').textContent=''; }); draw(false); };
  var nearOn=function(p){ near=p; var withLL=items.filter(function(li){ return li.dataset.ll; });
    withLL.forEach(function(li){ li._d=km(p, LL(li)); });
    withLL.sort(function(a,b){ return a._d-b._d; });
    withLL.forEach(function(li){ nlist.appendChild(li); li.querySelector('.mu-dist').textContent=' · about '+miles(li._d)+' mi'+(li.dataset.approx?' (rough)':''); });
    nsec.hidden=false; nb.setAttribute('aria-pressed','true'); nb.textContent='Back to the counties'; draw(false);
    if (map){ if (!map._me) map._me=L.circleMarker(p,{radius:7, className:'mu-me-pt', interactive:false}).addTo(map); else map._me.setLatLng(p); }
    nsec.scrollIntoView({behavior:glide, block:'start'}); };
  var where=function(ok,bad,hi){ if (!navigator.geolocation){ bad('This browser cannot share a location.'); return; }
    navigator.geolocation.getCurrentPosition(function(pos){ ok([pos.coords.latitude,pos.coords.longitude], pos.coords.accuracy||0); }, function(){ bad('No location shared, so nothing changed.'); }, {maximumAge:hi?0:600000, timeout:20000, enableHighAccuracy:!!hi}); };
  nb.addEventListener('click',function(){ if (near){ nearOff(); return; }
    nmsg.textContent='Asking your browser where you are…';
    where(function(p){ nmsg.textContent='Sorted from where you are now. Your location stays on this device.'; nearOn(p); }, function(m){ nmsg.textContent=m+' Use the county list instead.'; }); });

  /* ---- my trip, been there and the passport ---- */
  var tp=$('#muTrip'), tl=$('#muTripList'), tc=$('#muTripN'), td=$('#muTripDir'), bc=$('#muBeenN'), tmsg=$('#muTripMsg'), pass=$('#muPass'), pl=$('#muStamps');
  var tripURL=function(){ return location.origin+'/museums/?trip='+trip.join('.'); };
  var paint=function(){
    items.forEach(function(li){ var t=trip.indexOf(li.id)>=0, b=been.indexOf(li.id)>=0, tb=li.querySelector('.mu-tb'), bb=li.querySelector('.mu-bb'), st=stamp[li.id];
      tb.setAttribute('aria-pressed',String(t)); tb.textContent=t?'On my trip ✓':'Add to my trip'; bb.setAttribute('aria-pressed',String(b)); bb.textContent=b?'Been there ✓':'Been there';
      li.classList.toggle('on-trip',t); li.classList.toggle('was',b); li.classList.toggle('stamped',!!st); if (st) li.dataset.stamp=st; else delete li.dataset.stamp;
      var sb=li.querySelector('.mu-sb'); if (sb){ sb.hidden=!navigator.geolocation; sb.textContent=st?'Stamped ✓':'I’m here: stamp it'; sb.disabled=!!st; } });
    tc.textContent=trip.length; tp.hidden=!trip.length;
    tl.innerHTML=''; trip.forEach(function(id,i){ var li=byId[id], r=document.createElement('li');
      var a=document.createElement('a'); a.href='#'+id; a.textContent=li.dataset.n; r.appendChild(a);
      var t=document.createElement('span'); t.className='mu-tt'; t.textContent=' · '+li.dataset.town; r.appendChild(t);
      if (i>0){ var a0=LL(byId[trip[i-1]]), a1=LL(li); if (a0 && a1){ var g=document.createElement('span'); g.className='mu-leg'; g.textContent=' · '+miles(km(a0,a1)*1.25)+' mi'; g.title='Rough road distance from the stop before'; r.appendChild(g); } }
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
    var ks=Object.keys(stamp).filter(function(id){ return byId[id]; }).sort(function(a,b){ return stamp[a]<stamp[b]?-1:1; });
    pass.hidden=!ks.length; pl.innerHTML='';
    ks.forEach(function(id){ var li=byId[id], r=document.createElement('li'), a=document.createElement('a'); a.href='#'+id; a.className='mu-stamp';
      var b=document.createElement('b'); b.textContent=li.dataset.n; var t=document.createElement('span'); t.textContent=li.dataset.town; var d=document.createElement('time'); d.textContent=stamp[id];
      a.appendChild(t); a.appendChild(b); a.appendChild(d); r.appendChild(a); pl.appendChild(r); });
    $('#muPassN').textContent=ks.length;
    if (map) drawMarkers(false); };
  var setTrip=function(ids, msg){ trip=ids.filter(function(id){ return byId[id]; }); save('ps-mu-trip',trip); paint(); tmsg.textContent=msg||''; tp.scrollIntoView({behavior:glide, block:'start'}); };
  items.forEach(function(li){
    li.querySelector('.mu-tb').addEventListener('click',function(){ var i=trip.indexOf(li.id); if (i>=0) trip.splice(i,1); else trip.push(li.id); save('ps-mu-trip',trip); tmsg.textContent=''; paint(); });
    li.querySelector('.mu-bb').addEventListener('click',function(){ var i=been.indexOf(li.id); if (i>=0) been.splice(i,1); else been.push(li.id); save('ps-mu-been',been); paint();
      if (been.length>=3 && window.psEarn) window.psEarn('visitor'); });
    var sb=li.querySelector('.mu-sb'), msg=li.querySelector('.mu-msg');
    if (sb) sb.addEventListener('click',function(){ msg.textContent='Checking where you are…';
      where(function(p,acc){ var d=km(p,LL(li)), reach=(li.dataset.approx?2.5:0.35)+Math.min(acc,500)/1000;
        if (d<=reach){ stamp[li.id]=new Date().toISOString().slice(0,10); save('ps-mu-stamp',stamp); if (been.indexOf(li.id)<0){ been.push(li.id); save('ps-mu-been',been); }
          paint(); msg.textContent='Stamped. It is in your passport, kept on this device only.'; if (window.psEarn){ window.psEarn('stamp'); if (been.length>=3) window.psEarn('visitor'); } }
        else msg.textContent='You look to be about '+miles(d)+' mi away. The stamp works at the door.'; },
        function(m){ msg.textContent=m; }, true); }); });
  $('#muTripClear').addEventListener('click',function(){ trip=[]; save('ps-mu-trip',trip); tmsg.textContent=''; paint(); q.focus(); });
  $('#muTripPrint').addEventListener('click',function(){ document.documentElement.classList.add('mu-printtrip'); window.print(); });
  window.addEventListener('afterprint',function(){ document.documentElement.classList.remove('mu-printtrip','mu-printqr'); });
  if (!store) $('#muMine').hidden=true;

  /* best order: the shortest path by distance (nearest neighbour, then untangled), from where you are if you sorted by distance, else from the first stop */
  $('#muTripBest').addEventListener('click',function(){
    var P=trip.filter(function(id){ return LL(byId[id]); }), rest=trip.filter(function(id){ return !LL(byId[id]); });
    if (P.length<3){ tmsg.textContent='Add at least three stops with map pins to sort them.'; return; }
    var pt=function(id){ return LL(byId[id]); }, D=function(a,b){ return km(pt(a),pt(b)); };
    var first=P[0]; if (near){ first=P.slice().sort(function(a,b){ return km(near,pt(a))-km(near,pt(b)); })[0]; }
    var path=[first], left=P.filter(function(id){ return id!==first; });
    while (left.length){ var last=path[path.length-1]; left.sort(function(a,b){ return D(last,a)-D(last,b); }); path.push(left.shift()); }
    var len=function(r){ var s=0; for (var i=1;i<r.length;i++) s+=D(r[i-1],r[i]); return s; }, before=len(P), better=true;
    while (better){ better=false; for (var i=1;i<path.length-1;i++) for (var j=i+1;j<path.length;j++){ var c=path.slice(0,i).concat(path.slice(i,j+1).reverse(), path.slice(j+1)); if (len(c)<len(path)-1e-9){ path=c; better=true; } } }
    var after=len(path); trip=path.concat(rest); save('ps-mu-trip',trip); paint();
    tmsg.textContent='Put in the shortest order by distance, starting at '+byId[path[0]].dataset.n+(near?' (the stop nearest you)':'')+'. About '+miles(after*1.25)+' mi of driving'+(before-after>0.5?', '+miles((before-after)*1.25)+' mi less than before':'')+'.'; });

  /* sharing: a link that carries the stops; the phone's own share menu where there is one, the clipboard otherwise */
  $('#muTripShare').addEventListener('click',function(){ var url=tripURL(), names=trip.map(function(id){ return byId[id].dataset.n; });
    if (navigator.share){ navigator.share({title:'A day among the valley’s museums', text:names.join(' → '), url:url}).catch(function(){}); return; }
    var done=function(){ tmsg.textContent='Link copied. Paste it into a message or post.'; };
    var showIt=function(){ tmsg.textContent='Copy this link: '; var i=document.createElement('input'); i.type='text'; i.readOnly=true; i.value=url; i.className='mu-link'; i.setAttribute('aria-label','Link to this trip'); tmsg.appendChild(i); i.focus(); i.select(); };
    if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, showIt); else showIt(); });
  var qd=$('#muQR');
  $('#muTripQR').addEventListener('click',function(){ var show=function(){ var c=qrcode(0,'M'); c.addData(tripURL()); c.make(); $('#muQRc').innerHTML=c.createSvgTag({cellSize:6, margin:3, scalable:true, alt:'QR code for this trip'});
      $('#muQRl').textContent=trip.map(function(id){ return byId[id].dataset.n; }).join(' → '); if (qd.showModal) qd.showModal(); else qd.setAttribute('open',''); };
    if (window.qrcode) show(); else { var s=document.createElement('script'); s.src='/vendor/qrcode-generator-1.4.4/qrcode.min.js?v=1'; s.onload=show; s.onerror=function(){ tmsg.textContent='The QR maker could not load. The share link still works.'; }; document.head.appendChild(s); } });
  $('#muQRx').addEventListener('click',function(){ qd.close ? qd.close() : qd.removeAttribute('open'); });
  $('#muQRp').addEventListener('click',function(){ document.documentElement.classList.add('mu-printqr'); window.print(); });
  qd.addEventListener('click',function(e){ if (e.target===qd) qd.close(); });

  /* day trips */
  $$('.mu-dtb').forEach(function(b){ b.addEventListener('click',function(){ var ids=b.dataset.ids.split('.'); var mine=trip.length && trip.join('.')!==ids.join('.');
    setTrip(ids,'Loaded “'+b.closest('.mu-dt').querySelector('h3').textContent+'”.'+(mine?' It replaced the trip you had.':'')+' Check each place’s hours before you set out.'); }); });

  /* a trip shared by link */
  var sp=new URLSearchParams(location.search), shared=(sp.get('trip')||'').split('.').filter(function(id){ return byId[id]; });
  if (shared.length){ if (!trip.length || trip.join('.')===shared.join('.')) setTrip(shared,'A trip someone shared with you: '+shared.length+' stops.');
    else { var bn=$('#muShared'); bn.hidden=false; $('#muSharedN').textContent=shared.length;
      $('#muSharedUse').addEventListener('click',function(){ bn.hidden=true; setTrip(shared,'Now showing the shared trip. Your old one was replaced.'); });
      $('#muSharedNo').addEventListener('click',function(){ bn.hidden=true; }); }
    history.replaceState(null,'',location.pathname+location.hash); }

  /* save for no-signal use: the page, its map and the town outlines go into this device's saved copy */
  var ob=$('#muOff'), om=$('#muOffMsg');
  if ('caches' in window && navigator.serviceWorker && navigator.serviceWorker.controller){ ob.hidden=false;
    ob.addEventListener('click',function(){ om.textContent='Saving…';
      var urls=['/museums/','/museums/base.json?v=1','/vendor/leaflet-1.9.4/leaflet.js?v=1','/vendor/leaflet-1.9.4/leaflet.css?v=1','/vendor/qrcode-generator-1.4.4/qrcode.min.js?v=1'].concat($$('img.mu-ph').map(function(i){ return i.getAttribute('src'); }), $$('link[rel=stylesheet][href*="?v="],script[src*="?v="]').map(function(e){ return e.getAttribute('href')||e.getAttribute('src'); }));
      caches.keys().then(function(k){ var name=k.filter(function(x){ return /^ps-[0-9a-f]{6,}$/.test(x); })[0]||'ps-files'; return caches.open(name); })
        .then(function(c){ return Promise.all(urls.map(function(u){ return c.add(new Request(u,{cache:'reload'})).catch(function(){}); })); })
        .then(function(){ return navigator.storage && navigator.storage.persist ? navigator.storage.persist() : false; })
        .then(function(){ om.textContent='Saved. This page, its map, your trip and your passport now open on this device without signal. Directions still need a connection.'; ob.textContent='Saved for no-signal use ✓'; })
        .catch(function(){ om.textContent='This browser would not save the page. It will still work wherever you have signal.'; }); }); }

  /* ---- the map: county outlines drawn here, no outside map unless the reader turns it on ---- */
  var box=$('#muMap'), stat=$('#muMapStat');
  var go=function(li){ if (li.hidden){ kind=''; research=false; openF=''; sel.value=''; q.value=''; fs.forEach(function(x){ x.setAttribute('aria-pressed',String(!x.dataset.k)); }); rb.setAttribute('aria-pressed','false'); draw(false); }
    li.scrollIntoView({behavior:glide, block:'center'});
    li.classList.remove('flash'); void li.offsetWidth; li.classList.add('flash'); var h=li.querySelector('h3'); h.tabIndex=-1; h.focus({preventScroll:true}); };
  var drawMarkers=function(fit){ var vis=[];
    markers.forEach(function(m){ var any=m.lis.filter(function(li){ return !li.hidden; }); m.on=any.length>0;
      m.t=any.some(function(li){ return li.classList.contains('on-trip'); }); m.b=m.on && any.every(function(li){ return li.classList.contains('was'); });
      if (m.on) vis.push(m.c.getLatLng()); });
    if (fit){ if (!filtered()) map.fitBounds(map._home); else if (vis.length) map.fitBounds(L.latLngBounds(vis).pad(.25),{maxZoom:12}); }
    cluster();
    stat.textContent=vis.length? vis.length+' map pins showing' : 'No pins match'; };
  /* pins close together on screen gather into one numbered circle; zoom in and they part */
  var cluster=function(){ if (!map) return; group.clearLayers(); var z=map.getZoom(), cl=[];
    markers.forEach(function(m){ m.cl=null; if (!m.on){ if (map.hasLayer(m.c)) map.removeLayer(m.c); return; }
      var p=map.latLngToLayerPoint(m.c.getLatLng()), hit=null;
      if (z<13) for (var i=0;i<cl.length;i++){ if (cl[i].p.distanceTo(p)<26){ hit=cl[i]; break; } }
      if (hit) hit.ms.push(m); else cl.push({p:p, ms:[m]}); });
    cl.forEach(function(c){
      if (c.ms.length===1){ var m=c.ms[0]; if (!map.hasLayer(m.c)) m.c.addTo(map); var el=m.c.getElement(); if (el){ el.classList.toggle('t',m.t); el.classList.toggle('b',m.b); } return; }
      var n=0, la=0, lo=0, t=false; c.ms.forEach(function(m){ if (map.hasLayer(m.c)) map.removeLayer(m.c); n+=m.lis.filter(function(li){ return !li.hidden; }).length; var g=m.c.getLatLng(); la+=g.lat; lo+=g.lng; t=t||m.t; });
      var names=[]; c.ms.forEach(function(m){ m.lis.forEach(function(li){ if (!li.hidden) names.push(li.dataset.n); }); });
      var mk=L.marker([la/c.ms.length, lo/c.ms.length],{title:n+' places here; press to zoom in', alt:n+' places', riseOnHover:true,
        icon:L.divIcon({className:'mu-clu'+(t?' t':''), html:'<span>'+n+'</span>', iconSize:[n>9?36:30, n>9?36:30]})});
      mk.on('click keypress',function(e){ if (e.type==='keypress' && e.originalEvent.key!=='Enter') return; map.fitBounds(L.latLngBounds(c.ms.map(function(m){ return m.c.getLatLng(); })).pad(.6),{maxZoom:14}); });
      mk.bindTooltip(names.slice(0,6).join(' · ')+(names.length>6?' · and '+(names.length-6)+' more':''),{direction:'top', offset:[0,-14]});
      group.addLayer(mk); c.ms.forEach(function(m){ m.cl=mk; }); }); };
  /* a card and its pin light up together */
  var lit=null, light=function(li,on){ var m=li._m; if (!map || !m) return; var el=m.cl? (m.cl.getElement&&m.cl.getElement()) : m.c.getElement(); if (lit && lit!==el) lit.classList.remove('hl'); if (el){ el.classList.toggle('hl',on); lit=on?el:null; } };
  items.forEach(function(li){ li.addEventListener('mouseenter',function(){ light(li,true); }); li.addEventListener('mouseleave',function(){ light(li,false); });
    li.addEventListener('focusin',function(){ light(li,true); }); li.addEventListener('focusout',function(e){ if (!li.contains(e.relatedTarget)) light(li,false); });
    var b=li.querySelector('.mu-sm'); if (b) b.addEventListener('click',function(){ var ll=LL(li);
      var fly=function(){ box.scrollIntoView({behavior:glide, block:'center'}); map.once('moveend',function(){ cluster(); li._m.c.openPopup(); }); map.setView(ll, 15, {animate:!calm}); };
      if (map) fly(); else { need(); var w=setInterval(function(){ if (map && markers.length){ clearInterval(w); fly(); } },120); setTimeout(function(){ clearInterval(w); },8000); } }); });
  var start=function(){ if (map || !window.L) return;
    map=L.map(box,{zoomSnap:.25, minZoom:7, maxZoom:17, scrollWheelZoom:false, attributionControl:true, maxBounds:[[40.9,-87.9],[42.95,-84.3]]});
    map.attributionControl.setPrefix(false); group=L.layerGroup().addTo(map);
    map._home=L.latLngBounds([[41.42,-86.95],[42.43,-85.35]]); map.fitBounds(map._home);
    map.on('focus click',function(){ map.scrollWheelZoom.enable(); }); map.on('blur mouseout',function(){ map.scrollWheelZoom.disable(); });
    map.on('zoomend',cluster);
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
        var oh=li.querySelector('.mu-open'); if (oh && oh.textContent){ var o=document.createElement('small'); o.textContent=oh.textContent; p.appendChild(o); }
        if (li.dataset.approx){ var a=document.createElement('small'); a.textContent='Pin is near, not exact.'; p.appendChild(a); } div.appendChild(p); });
      c.bindPopup(div,{maxWidth:260}); c.bindTooltip(lis.map(function(li){ return li.dataset.n; }).join(' · '),{direction:'top', offset:[0,-6]});
      var m={c:c, lis:lis}; lis.forEach(function(li){ li._m=m; }); markers.push(m); });
    draw(false); paint(); if (near) nearOn(near);
    var osm=null, sb=$('#muOSM');
    sb.hidden=false; sb.addEventListener('click',function(){ var on=sb.getAttribute('aria-pressed')!=='true'; sb.setAttribute('aria-pressed',String(on));
      if (on){ if (!osm) osm=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19, attribution:'Streets: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}); osm.addTo(map); box.classList.add('osm'); }
      else { map.removeLayer(osm); box.classList.remove('osm'); } });
    $('#muHome').hidden=false; $('#muHome').addEventListener('click',function(){ map.fitBounds(map._home); });
  };
  var need=function(){ if (window.L){ start(); return; } if (need.on) return; need.on=1;
    var l=document.createElement('link'); l.rel='stylesheet'; l.href='/vendor/leaflet-1.9.4/leaflet.css?v=1'; document.head.appendChild(l);
    var s=document.createElement('script'); s.src='/vendor/leaflet-1.9.4/leaflet.js?v=1'; s.onload=start; s.onerror=function(){ stat.textContent='The map could not load. The list below has every place.'; }; document.head.appendChild(s); };
  if ('IntersectionObserver' in window){ var io=new IntersectionObserver(function(e){ if (e.some(function(x){ return x.isIntersecting; })){ io.disconnect(); need(); } },{rootMargin:'300px'}); io.observe(box); } else need();
  hours(); setInterval(function(){ hours(); if (openF==='now') draw(false); },60000);
  paint();
  /* a link to one place (from the map, or shared) lights it up */
  var h=location.hash.slice(1); if (h && byId[h]) setTimeout(function(){ go(byId[h]); },300);
})();
</script>'''

body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Museums &amp; historic places</p>
    <h1>Where the valley keeps its past</h1>
    <p class="lede" style="font-size:1.15rem">Here are {n} museums, historic houses, libraries, research rooms and archives across the St. Joseph River valley and its neighbours, from the log cabin in Cassopolis to the Studebaker collection in South Bend. The hunt starts on this website. It finishes in places like these.</p>
    <div class="mu-bar">
      <label class="nm-q"><span>Find a place</span><input type="search" id="muQ" placeholder="A town, a museum or a subject" autocomplete="off" spellcheck="false"></label>
      <div class="nm-chips" role="group" aria-label="Show one kind of place"><button type="button" class="btn mu-f" data-k="" aria-pressed="true">Everything</button>{kinds}</div>
      <div class="nm-chips mu-opts"><button type="button" class="btn mu-rb" id="muR" aria-pressed="false">Help for researchers</button><label class="mu-ol"><span class="vh">Opening days</span><select id="muOpen"><option value="">Open any day</option><option value="now">Open right now</option><option value="today">Open today</option>{opts}</select></label><button type="button" class="btn mu-nb" id="muNear" aria-pressed="false">Sort by distance from me</button><button type="button" class="btn mu-off" id="muOff" hidden>Save for no-signal use</button></div>
      <p class="mu-nmsg" id="muNearMsg" aria-live="polite"></p><p class="mu-nmsg" id="muOffMsg" aria-live="polite"></p>
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
    <p class="mu-shared" id="muShared" hidden role="status">Someone shared a trip of <b id="muSharedN"></b> stops with you. <button type="button" class="btn" id="muSharedUse">Use the shared trip</button> <button type="button" class="btn" id="muSharedNo">Keep my own</button></p>
    <aside class="mu-trip" id="muTrip" hidden aria-labelledby="muTripH">
      <h2 id="muTripH">My trip <span class="mu-n"><span id="muTripN">0</span> stops</span></h2>
      <ol id="muTripList"></ol>
      <p class="mu-tacts"><a class="btn" id="muTripDir" href="#" rel="noopener" hidden>Directions for the whole trip</a> <button type="button" class="btn" id="muTripBest">Best order</button> <button type="button" class="btn" id="muTripShare">Share this trip</button> <button type="button" class="btn" id="muTripQR">QR code</button> <button type="button" class="btn" id="muTripPrint">Print my trip</button> <button type="button" class="btn" id="muTripClear">Clear the trip</button></p>
      <p class="mu-tmsg" id="muTripMsg" aria-live="polite"></p>
      <p class="note">Your trip list stays in this browser. Distances between stops are rough road miles. Directions open Google Maps, starting from wherever you are. A shared link or QR code carries only the list of stops.</p>
    </aside>
    <dialog class="mu-qr" id="muQR" aria-labelledby="muQRh"><h2 id="muQRh">Scan for this trip</h2><div id="muQRc"></div><p class="mu-qrl" id="muQRl"></p><p class="mu-tacts"><button type="button" class="btn" id="muQRp">Print the code</button> <button type="button" class="btn" id="muQRx">Close</button></p></dialog>
    <p class="mu-mine" id="muMine"><span id="muBeenN"></span></p>
    <section class="mu-pass" id="muPass" hidden aria-labelledby="muPassH"><h2 id="muPassH">My passport <span class="mu-n"><span id="muPassN">0</span> stamps</span></h2><ol class="mu-stamps" id="muStamps"></ol>
      <p class="note">A stamp is earned by pressing “I’m here” at the place itself. Your browser checks your location once; it stays on this device.</p></section>
    <section class="mu-dts" aria-labelledby="muDtH"><h2 id="muDtH">Day trips</h2><p>Six ready-made days out. Load one, press “Best order”, and check each place’s hours before you go.</p><ul class="mu-dtl">{dts}</ul></section>
    <section class="mu-c mu-near" id="muNearSec" hidden><h2>Nearest to you</h2><ul class="mu-list" id="muNearList"></ul></section>
{sections}
    <h2>Before you go</h2>
    <ul class="dis">
      <li><b>Check the hours.</b> Many of these places are run by volunteers and open only some days or some seasons. Their own websites have the latest.</li>
      <li><b>Researchers, write ahead.</b> Archives and research rooms often keep their records off the floor. A note a week before lets them have your boxes ready.</li>
      <li><b>Bring what you know.</b> Names, dates, the township, and a copy of anything you found here. Staff can do far more with a good question.</li>
      <li><b>Make a day of it.</b> Load a day trip or add a few places to <i>My trip</i>, press “Best order”, then use “Directions for the whole trip”. Share it with a link or a QR code. Mark the ones you have seen with “Been there”: three earns a badge for your <a href="/badges/">field book</a>, and pressing “I’m here” at the door stamps your passport.</li>
      <li><b>No signal out there?</b> Press “Save for no-signal use” before you leave, and this page, its map and your trip will open on your phone without a connection.</li>
      <li><b>Know of a place we missed?</b> <a href="/#contact">Tell us</a> and we will add it.</li>
    </ul>
    <p class="note">Every place on this page was checked against its own website, or a city, county, library or university page about it, in October 2026. Places marked “check before you go” could not be confirmed online. The “open now” and “open today” lines are worked out from each place’s posted hours and seasons, in its own time zone; they do not know about holidays, events or a volunteer’s day off. Hours change: always look at the place’s own site before travelling. Map pins come from each street address; a few pins marked “near, not exact” sit at the town or road. The map draws its own county lines (US Census Bureau) and rivers (USGS). Only if you press “Show today’s streets” does your browser ask OpenStreetMap’s tile server for street maps, under <a href="https://osmfoundation.org/wiki/Privacy_Policy" rel="noopener">its privacy policy</a>. “Sort by distance” asks your browser for your location and uses it only on this page.</p>
{ld}
{JS}
'''
page('museums/index.html', 'Museums & historic places of the valley · Project Scroll',
     f'{n} museums, historic houses, research rooms and archives across the St. Joseph River valley in Michigan and Indiana, with a map, directions and a trip planner, each checked against its own website.',
     body, og='https://projectscroll.com/og/records.jpg')
print('museums built', n, len(keys), 'counties', nmap, 'on the map')
