"""Broadway Virtual Walk: downtown Cassopolis stop by stop, on the 1860 plan, with the old postcards and what is there now.
python3 _tools/build_walk.py   (stops in _tools/data/walk.json)"""
import sys, pathlib, json, html, re
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
import basemap
E = html.escape
CFG = [
  dict(data='walk.json', out='walk/index.html', url='/walk/', key='ps-walk', badge='walker', slug='cassopolis', town='Cassopolis', street='Broadway',
       title='Broadway Virtual Walk · Cassopolis, Michigan · Project Scroll', kicker='Broadway Virtual Walk', h1='Walk old Broadway',
       lede='Cassopolis, Michigan, from the 1860 plan to today: {n} stops down the main street, each with what stood there, who ran it, and what is there now. Walk it from your chair, stop by stop on the old plan, or bring this page to Broadway and stamp each stop on the spot.',
       plan=('/img/cass1860.webp', [[41.9061,-86.018103],[41.917772,-86.007168]], '1860 plan: Geil, Harley &amp; Siverd, Library of Congress'),
       bounds=[[41.9,-86.03],[41.925,-85.995]], extra='<a class="btn" href="/map/3d/cassopolis/">Fly over it in 3D</a> <a class="btn" href="/map/cassopolis/">The full 1860 plan</a> <a class="btn" href="/walk/dowagiac/">Next: Front Street, Dowagiac ›</a>',
       start='Start at the north end and walk south with the stops in order; the whole walk is under a mile.',
       note='The stops come from the county histories of 1875, 1882 and 1906, the Sanborn sheets, and the village and county records, each linked under its stop. The plan is the 1860 county wall map’s inset of Cassopolis. Where a date or name could not be confirmed, the stop says so. Corrections are welcome at research@projectscroll.com.',
       desc='Walk Broadway in Cassopolis, Michigan, stop by stop on the 1860 plan: {n} buildings and sites with their history, the old postcards and what is there now. Walk it online, or on foot with a passport stamp at each stop.', og='cassopolis'),
  dict(data='walk-dowagiac.json', out='walk/dowagiac/index.html', url='/walk/dowagiac/', key='ps-walk-dowagiac', badge='walker2', slug='dowagiac', town='Dowagiac', street='Front Street',
       title='Front Street Virtual Walk · Dowagiac, Michigan · Project Scroll', kicker='Front Street Virtual Walk', h1='Walk old Front Street',
       lede='Dowagiac, Michigan, the stove town: {n} stops through the downtown that the Round Oak works, the lure makers and the railroad built, each with what stood there and what is there now. Walk it from your chair, or bring this page to Front Street and stamp each stop on the spot.',
       plan=None, bounds=[[41.97,-86.125],[41.995,-86.095]], extra='<a class="btn" href="/map/dowagiac/">Dowagiac’s 1860 plan over today’s streets</a> <a class="btn" href="/walk/">Also: Broadway, Cassopolis ›</a>',
       start='Start at the history museum on Division Street and follow the stops in order; the whole walk is about a mile.',
       note='The stops come from the Dowagiac Area History Museum’s walking tour, the museum and city websites, the National Register file for the depot and the county histories, each linked under its stop. The base map and aerial photographs are from the USGS National Map, a public-domain service of the US Geological Survey; “Plain” shows only today’s streets drawn on this page from OpenStreetMap data. Where a date or name could not be confirmed, the stop says so. Corrections are welcome at research@projectscroll.com.',
       desc='Walk Front Street in Dowagiac, Michigan, stop by stop: {n} buildings and sites from the Round Oak stove works and the Heddon lure makers to the 1903 depot, with their history and what is there now.', og='dowagiac'),
]
for C in CFG:
  W = json.load(open(pathlib.Path(__file__).parent/'data'/C['data']))
  S = [s for s in W['stops'] if s.get('keep', True)]
  for i, s in enumerate(S, 1): s['n'] = i; s['id'] = s.get('id') or re.sub(r'[^a-z0-9]+','-',s['name'].lower()).strip('-')
  def pc(s):
      if not s.get('card'): return ''
      k, cap = s['card']
      if k.startswith('oc:'):
          import oldcards as O; d = O.BY[k[3:]]
          return f'<figure class="wk-pc wk-oc">{O.pic(d, "(min-width:900px) 30rem, 92vw")}<figcaption>{E(cap)} <span class="credit">{E(O.credit(d))} · <a href="{E(d["url"])}" rel="noopener">source</a></span></figcaption></figure>'
      return f'<figure class="wk-pc"><picture><source type="image/avif" srcset="/img/strip/{k}-800.avif 800w, /img/strip/{k}.avif 1600w" sizes="(min-width:900px) 30rem, 92vw"><img src="/img/strip/{k}-800.webp" srcset="/img/strip/{k}-800.webp 800w, /img/strip/{k}.webp 1600w" sizes="(min-width:900px) 30rem, 92vw" width="1600" height="400" alt="{E(cap)}" loading="lazy" decoding="async"></picture><figcaption>{E(cap)}</figcaption></figure>'
  def photo(s):
      if not s.get('card'): return ''
      import urllib.parse as _u
      mt='mailto:research@projectscroll.com?subject='+_u.quote('Then and now: '+s['name'])+'&body='+_u.quote('My photo of '+s['name']+', taken from where the old postcard was made. (Attach the photo.)\n\nMay Project Scroll show it beside the postcard, with my name? Yes / No\nMy name, as I would like it shown:')
      return f'<p class="wk-photo">📷 <b>Photo spot.</b> Stand where the photographer stood: line up the rooflines and corners with the postcard, take the same picture, and <a href="{mt}">send it to us</a>. The best go up beside the old view, with your name.</p>'
  def src(s):
      u = s.get('sources') or []
      return ' '.join(f'<a href="{E(x)}" rel="noopener">source {i}</a>' for i, x in enumerate(u, 1))
  SQ={'first-courthouse','historic-courthouse','the-fort','public-square','bank-corner','gem-theatre-site'}
  def sb(s):
      if C['data']=='walk.json':
          if s['id'] in SQ: return '<a class="wk-sbn" href="/map/#sanborn-cassopolis/001-2/1900,1700,1980,1730">The square on the 1884 Sanborn sheet</a>'
          return '<a class="wk-sbn" href="/map/#sanborn-cassopolis/001-2">Open the 1884 Sanborn sheet</a>'
      return '<a class="wk-sbn" href="/map/#sanborn-dowagiac">Open the Sanborn sheets of Dowagiac</a>'
  def blt(b): return ('built '+b) if re.match(r'^(\d|about|c\.)', b) else b[0].lower()+b[1:]
  stops = ''.join(f'''<li class="wk" id="{s['id']}" data-ll="{s['lat']},{s['lon']}" data-n="{E(s['name'])}">
          <p class="mu-k">Stop {s['n']} of {len(S)}{(' · '+E(blt(str(s['built'])))) if s.get('built') else ''}<span class="wk-st"></span></p>
          <h3>{E(s['name'])}</h3>
          {pc(s)}{photo(s)}
          <p class="wk-then"><b>Then.</b> {E(s['then'])}</p>
          <p class="wk-now"><b>Now.</b> {E(s['now'])}</p>
          {f'<p class="mu-a">{E(s["address"])}</p>' if s.get('address') else ''}
          <p class="wk-src">{src(s)} · {sb(s)}</p>
          <p class="mu-me"><button type="button" class="mu-sb wk-sb" hidden>I’m here: stamp it</button></p><p class="mu-msg" aria-live="polite"></p>
        </li>''' for s in S)
  sanborn = ''.join(f'<li><a href="{E(x["url"])}" rel="noopener">{E(str(x["year"]))}</a>{(" · "+E(x["note"])) if x.get("note") else ""}</li>' for x in W.get('sanborn', []))
  markers = ''.join(f'<li><a href="{E(x["url"])}" rel="noopener">{E(x["title"])}</a>{(" · "+E(x["location"])) if x.get("location") else ""}</li>' for x in W.get('markers', []))
  route = json.dumps([[s['lat'], s['lon']] for s in S])
  JS = '<script>'+basemap.BASE_JS+'</script>'+r'''<script>
  (function(){ "use strict";
    var $=function(s){ return document.querySelector(s); }, $$=function(s){ return [].slice.call(document.querySelectorAll(s)); };
    var calm=matchMedia('(prefers-reduced-motion: reduce)').matches;
    var stops=$$('.wk'), N=stops.length, cur=0, map=null, pins=[], plan=null, osm=null, line=null;
    var seen={}, stamp={}; try{ seen=JSON.parse(localStorage.getItem('__KEY__')||'{}')||{}; stamp=JSON.parse(localStorage.getItem('__KEY__-stamp')||'{}')||{}; }catch(e){}
    var save=function(){ try{ localStorage.setItem('__KEY__',JSON.stringify(seen)); localStorage.setItem('__KEY__-stamp',JSON.stringify(stamp)); }catch(e){} };
    var LL=function(li){ return li.dataset.ll.split(',').map(Number); };
    var km=function(a,b){ var R=6371, r=Math.PI/180, dl=(b[0]-a[0])*r, dn=(b[1]-a[1])*r, h=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a[0]*r)*Math.cos(b[0]*r)*Math.sin(dn/2)*Math.sin(dn/2); return 2*R*Math.asin(Math.sqrt(h)); };
    var stage=$('#wkStage'), num=$('#wkNum'), prev=$('#wkPrev'), next=$('#wkNext'), prog=$('#wkProg');
    var paint=function(){ var n=Object.keys(seen).length; prog.textContent=n? 'You have walked '+n+' of '+N+' stops'+(Object.keys(stamp).length? ', and stamped '+Object.keys(stamp).length+' in person' : '')+'.' : '';
      stops.forEach(function(li,i){ var s=li.querySelector('.wk-st'); s.textContent=stamp[li.id]? ' · stamped '+stamp[li.id] : (seen[li.id]? ' · walked' : '');
        var b=li.querySelector('.wk-sb'); if (b){ b.hidden=!navigator.geolocation; b.disabled=!!stamp[li.id]; b.textContent=stamp[li.id]? 'Stamped ✓' : 'I’m here: stamp it'; }
        if (pins[i]){ var el=pins[i].getElement(); if (el){ el.classList.toggle('seen',!!seen[li.id]); el.classList.toggle('cur',i===cur); } } }); };
    var show=function(i, fly){ cur=(i+N)%N; var li=stops[cur]; seen[li.id]=1; save();
      stage.innerHTML=''; var c=document.createElement('div'); c.className='wk wk-card'; c.innerHTML=li.innerHTML; c.querySelectorAll('[id]').forEach(function(x){ x.removeAttribute('id'); }); c.querySelectorAll('.mu-me,.mu-msg,.cshare-w').forEach(function(x){ x.remove(); });
      var h3=c.querySelector('h3'); if (h3){ var h2=document.createElement('h2'); h2.className='wk-h'; h2.textContent=h3.textContent; h3.replaceWith(h2); }
      stage.appendChild(c); num.textContent='Stop '+(cur+1)+' of '+N; prev.disabled=false; next.disabled=false;
      if (map && fly!==false){ map.flyTo(LL(li), 18, {duration:calm?0:.8}); }
      if (Object.keys(seen).length===N && window.psEarn) window.psEarn('__BADGE__');
      paint(); };
    prev.addEventListener('click',function(){ show(cur-1); }); next.addEventListener('click',function(){ show(cur+1); });
    $('#wkBox').addEventListener('keydown',function(e){ if (e.target.closest('input,select,textarea')) return; if (e.key==='ArrowRight'){ show(cur+1); e.preventDefault(); } if (e.key==='ArrowLeft'){ show(cur-1); e.preventDefault(); } });
    stops.forEach(function(li,i){ var b=li.querySelector('.wk-sb'), m=li.querySelector('.mu-msg'); if (!b) return;
      b.addEventListener('click',function(){ if (!navigator.geolocation) return; m.textContent='Checking where you are…';
        navigator.geolocation.getCurrentPosition(function(p){ var d=km([p.coords.latitude,p.coords.longitude], LL(li)), reach=.12+Math.min(p.coords.accuracy||0,300)/1000;
          if (d<=reach){ stamp[li.id]=new Date().toISOString().slice(0,10); seen[li.id]=1; save(); paint(); m.textContent='Stamped. It is in your passport, on this device only.'; if (window.psEarn) window.psEarn('stamp'); if (window.psStampCheck) window.psStampCheck(); }
          else m.textContent='You look to be about '+(d*0.621371<10?(d*0.621371).toFixed(1):Math.round(d*0.621371))+' mi away. The stamp works on the spot.'; },
          function(){ m.textContent='No location shared, so nothing changed.'; }, {enableHighAccuracy:true, timeout:20000, maximumAge:0}); }); });
    /* the map: the 1860 plan of the village with the stops on it; today's streets only if asked for */
    var start=function(){ if (map || !window.L) return;
      [].forEach.call(document.querySelectorAll('.mu-mapph'),function(x){ x.remove(); });
    map=L.map('wkMap',{zoomSnap:.25, minZoom:15, maxZoom:19, scrollWheelZoom:false, maxBounds:__BOUNDS__}); map.attributionControl.setPrefix(false);
      /* today's streets, drawn here from OpenStreetMap data saved with the site */
      var dec=function(a){ var o=[], la=0, lo=0; for (var i=0;i<a.length;i+=2){ la+=a[i]; lo+=a[i+1]; o.push([la/1e5, lo/1e5]); } return o; };
      map.createPane('today').style.zIndex=300;
      fetch('/map/__SLUG__/today.json?v=1').then(function(r){ return r.json(); }).then(function(d){
        (d.w||[]).forEach(function(p){ L.polygon(p.map(dec),{pane:'today', className:'wk-w', interactive:false}).addTo(map); });
        [['s','wk-w2'],['r','wk-r'],['m','wk-m'],['x','wk-x']].forEach(function(k){ (d[k[0]]||[]).forEach(function(a){ L.polyline(dec(a),{pane:'today', className:k[1], interactive:false}).addTo(map); }); });
        map.attributionControl.addAttribution('Today’s streets: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'); }).catch(function(){});
      var PL=__PLAN__; map.createPane('plan').style.zIndex=350;
      if (PL){ plan=L.imageOverlay(PL[0],PL[1],{pane:'plan', opacity:.85, className:'wk-plan'}).addTo(map); map.attributionControl.addAttribution(PL[2]); }
      line=L.polyline(__ROUTE__,{className:'wk-route', interactive:false}).addTo(map);
      stops.forEach(function(li,i){ var m=L.marker(LL(li),{icon:L.divIcon({className:'wk-pin', html:'<span>'+(i+1)+'</span>', iconSize:[26,26]}), title:'Stop '+(i+1)+': '+li.dataset.n, alt:'Stop '+(i+1)}).addTo(map);
        m.on('click',function(){ show(i,false); map.panTo(LL(li)); }); pins.push(m); });
      map.fitBounds(line.getBounds().pad(.25));
      map.on('focus click',function(){ map.scrollWheelZoom.enable(); }); map.on('blur mouseout',function(){ map.scrollWheelZoom.disable(); });
      var op=$('#wkOp'); if (plan){ op.hidden=false; } op.querySelector('input').addEventListener('input',function(e){ plan.setOpacity(+e.target.value/100); });
      map.on('psbase',function(e){ map.getPane('today').style.opacity= e.base==='plain'? '' : (e.base==='topo'? '0' : '.55'); });
      window.psBase(map, map.getContainer(), $('#wkBase'), 'topo');
      paint(); };
    var need=function(){ if (window.L){ start(); return; } if (need.on) return; need.on=1;
      var l=document.createElement('link'); l.rel='stylesheet'; l.href='/vendor/leaflet-1.9.4/leaflet.css?v=1'; document.head.appendChild(l);
      var s=document.createElement('script'); s.src='/vendor/leaflet-1.9.4/leaflet.js?v=1'; s.onload=start; document.head.appendChild(s); };
    if ('IntersectionObserver' in window){ var io=new IntersectionObserver(function(e){ if (e.some(function(x){ return x.isIntersecting; })){ io.disconnect(); need(); } },{rootMargin:'300px'}); io.observe($('#wkMap')); } else need();
    /* play the tour aloud: the browser's own voice reads each stop, then moves on */
    var pb=$('#wkPlay'), playing=false, sy=window.speechSynthesis;
    var say=function(){ if (!playing) return; var li=stops[cur], t=li.dataset.n+'. '+[].slice.call(li.querySelectorAll('.wk-then,.wk-now')).map(function(p){ return p.textContent; }).join(' ');
      var u=new SpeechSynthesisUtterance(t); u.lang='en-US'; u.rate=.98;
      u.onend=function(){ if (!playing) return; if (cur<N-1) setTimeout(function(){ if (playing){ show(cur+1); say(); } },1200); else { playing=false; pb.setAttribute('aria-pressed','false'); pb.textContent='Play the tour aloud'; } };
      sy.cancel(); sy.speak(u); };
    if (sy && window.SpeechSynthesisUtterance){ pb.hidden=false; pb.addEventListener('click',function(){ playing=!playing; pb.setAttribute('aria-pressed',String(playing)); pb.textContent=playing?'Stop reading':'Play the tour aloud'; if (playing) say(); else sy.cancel(); });
      prev.addEventListener('click',function(){ if (playing) say(); }); next.addEventListener('click',function(){ if (playing) say(); }); addEventListener('pagehide',function(){ sy.cancel(); }); }
    /* follow me on foot: your position on the plan, and each stop opens as you reach it; nothing leaves this device */
    var fb=$('#wkFollow'), watch=null, me=null, fmsg=$('#wkProg');
    if (navigator.geolocation){ fb.hidden=false; fb.addEventListener('click',function(){
      if (watch!==null){ navigator.geolocation.clearWatch(watch); watch=null; fb.setAttribute('aria-pressed','false'); fb.textContent='Follow me on foot'; if (me && map) map.removeLayer(me); me=null; return; }
      need(); fb.setAttribute('aria-pressed','true'); fb.textContent='Stop following';
      watch=navigator.geolocation.watchPosition(function(p){ var here=[p.coords.latitude,p.coords.longitude];
        if (map){ if (!me) me=L.circleMarker(here,{radius:8, className:'mu-me-pt', interactive:false}).addTo(map); else me.setLatLng(here); }
        var best=-1, bd=1e9; stops.forEach(function(li,i){ var d=km(here,LL(li))*1000; if (d<bd){ bd=d; best=i; } });
        if (bd>2000){ fmsg.textContent='You look to be away from __STREET__. Following starts working when you are in downtown __TOWN__.'; return; }
        if (bd<=40+Math.min(p.coords.accuracy||0,40) && best!==cur){ show(best); if (navigator.vibrate) navigator.vibrate(90); fmsg.textContent='You are at stop '+(best+1)+': '+stops[best].dataset.n+'.'; if (playing) say(); }
      }, function(){ fmsg.textContent='No location shared, so following is off.'; fb.click(); }, {enableHighAccuracy:true, maximumAge:5000, timeout:30000}); }); }
    /* save the walk for the street: the page, the plan, the map code and the postcards go into this device's saved copy */
    var ob=$('#wkOff'), PLANURL=__PLANURL__;
    if ('caches' in window && navigator.serviceWorker && navigator.serviceWorker.controller){ ob.hidden=false; ob.addEventListener('click',function(){ ob.textContent='Saving…';
      var urls=['__URL__','/map/__SLUG__/today.json?v=1'].concat(PLANURL? [PLANURL] : []).concat(['/vendor/leaflet-1.9.4/leaflet.js?v=1','/vendor/leaflet-1.9.4/leaflet.css?v=1']).concat($$('.wk-list img').map(function(i){ return i.currentSrc||i.src; }), $$('link[rel=stylesheet][href*="?v="],script[src*="?v="]').map(function(e){ return e.getAttribute('href')||e.getAttribute('src'); }));
      caches.keys().then(function(k){ return caches.open(k.filter(function(x){ return /^ps-[0-9a-f]{6,}$/.test(x); })[0]||'ps-files'); })
        .then(function(c){ return Promise.all(urls.map(function(u){ return c.add(new Request(u,{cache:'reload'})).catch(function(){}); })); })
        .then(function(){ return navigator.storage && navigator.storage.persist ? navigator.storage.persist() : false; })
        .then(function(){ ob.textContent='Saved for no-signal use ✓'; fmsg.textContent='Saved. The walk, its map and its pictures now open on this device without signal.'; })
        .catch(function(){ ob.textContent='Could not save'; }); }); }
    var h=location.hash.slice(1), at=stops.findIndex(function(li){ return li.id===h; });
    show(at>=0? at : 0, false); if (at>=0) $('#wkBox').scrollIntoView();
  })();
  </script>'''.replace('__ROUTE__', route).replace('__KEY__', C['key']).replace('__BADGE__', C['badge']).replace('__BOUNDS__', json.dumps(C['bounds'])).replace('__SLUG__', C['slug']).replace('__STREET__', C['street']).replace('__TOWN__', C['town']).replace('__URL__', C['url']).replace('__PLAN__', json.dumps(list(C['plan']) if C['plan'] else None)).replace('__PLANURL__', json.dumps(C['plan'][0] if C['plan'] else None))
  body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
      <p class="kicker">{C['kicker']}</p>
      <figure class="pg-art"><picture><source type="image/avif" srcset="/img/card-walk-art-270.avif 270w, /img/card-walk-art.avif 540w" sizes="8rem"><img class="vt-walk" src="/img/card-walk-art-270.webp" srcset="/img/card-walk-art-270.webp 270w, /img/card-walk-art.webp 540w" sizes="8rem" width="540" height="960" alt="" decoding="async"></picture></figure>
      <h1>{C['h1']}</h1>
      <p class="lede" style="font-size:1.15rem">{C['lede'].format(n=len(S))}</p>
      <div class="wk-box" id="wkBox">
        <div class="wk-map" id="wkMap" role="region" aria-label="A map of downtown {C['town']} with the stops of the walk. Every stop is also in the list below."><p class="mu-mapph">The map opens here.</p></div>
        <div class="wk-side">
          <p class="wk-nav"><button type="button" class="btn" id="wkPrev">‹ Back</button> <span id="wkNum" aria-live="polite"></span> <button type="button" class="btn primary" id="wkNext">Next stop ›</button></p>
          <div class="wk-stage" id="wkStage" aria-live="polite"></div>
        </div>
        <p class="wk-tools"><label class="wk-op" id="wkOp" hidden>1860 plan <input type="range" min="0" max="100" value="90" aria-label="How strongly the 1860 plan shows"></label> {basemap.buttons("topo","wkBase")} <button type="button" class="btn" id="wkPlay" aria-pressed="false" hidden>Play the tour aloud</button> <button type="button" class="btn" id="wkFollow" aria-pressed="false" hidden>Follow me on foot</button> {C['extra']} <button type="button" class="btn" id="wkOff" hidden>Save for no-signal use</button></p>
        <p class="mu-mine" id="wkProg" aria-live="polite"></p>
      </div>
      <h2>Every stop</h2>
      <ol class="wk-list">{stops}</ol>
      {f'<h2>The fire-insurance sheets</h2><p>The Sanborn Map Company drew {C['town']} building by building for fire insurers. Each sheet shows what every building was made of and what it was used for. Open one beside this walk:</p><ul class="dis">{sanborn}</ul>' if sanborn else ''}
      {f'<h2>Historical markers in town</h2><ul class="dis">{markers}</ul>' if markers else ''}
      <h2>Walking it for real</h2>
      <ul class="dis">
        <li><b>{C['start'].split('; ')[0]}</b>; {C['start'].split('; ')[1]}</li>
        <li><b>Let the page follow you.</b> “Follow me on foot” opens each stop as you reach it, and “Play the tour aloud” reads it to you, so you can keep your eyes on the street.</li>
        <li><b>Stamp as you go.</b> “I’m here” checks your location once, on your phone, and stamps that stop. Nothing leaves your device.</li>
        <li><b>Stay on the sidewalk</b> and on public ground, and be kind to the businesses: many of these buildings are still working shops and offices.</li>
        <li><b>Take the same picture.</b> Where a stop has an old postcard, stand where the photographer stood and <a href="/postcards/">send us your photo</a>.</li>
      </ul>
      <p class="vs-plan"><a class="btn" href="/visit/">Plan your visit: ready-made days out, food, lodging and festivals</a></p>
      <p class="note">{C['note']}</p>
  {JS}
  '''
  import pages as _pg
  _base = 'https://projectscroll.com/' + C['out'].replace('index.html','')
  _pg.EXTRA[C['out']] = {"mainEntity": {"@type":"TouristTrip","name":C['title'].split(' · ')[0],"touristType":"History walkers",
      "itinerary":{"@type":"ItemList","numberOfItems":len(S),"itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"TouristAttraction","name":s['name'],"url":_base+'#'+s['id'],
      "geo":{"@type":"GeoCoordinates","latitude":s['lat'],"longitude":s['lon']}}} for i,s in enumerate(S)]}}}
  page(C['out'], C['title'], C['desc'].format(n=len(S)), body, og=f"https://projectscroll.com/og/{C['og']}.jpg")
  print('walk built', C['out'], len(S))
