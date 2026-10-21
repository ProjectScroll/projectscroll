"""Broadway Virtual Walk: downtown Cassopolis stop by stop, on the 1860 plan, with the old postcards and what is there now.
python3 _tools/build_walk.py   (stops in _tools/data/walk.json)"""
import sys, pathlib, json, html, re
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E = html.escape
W = json.load(open(pathlib.Path(__file__).parent/'data'/'walk.json'))
S = [s for s in W['stops'] if s.get('keep', True)]
for i, s in enumerate(S, 1): s['n'] = i; s['id'] = s.get('id') or re.sub(r'[^a-z0-9]+','-',s['name'].lower()).strip('-')
def pc(s):
    if not s.get('card'): return ''
    k, cap = s['card']
    return f'<figure class="wk-pc"><picture><source type="image/avif" srcset="/img/strip/{k}-800.avif 800w, /img/strip/{k}.avif 1600w" sizes="(min-width:900px) 30rem, 92vw"><img src="/img/strip/{k}-800.webp" srcset="/img/strip/{k}-800.webp 800w, /img/strip/{k}.webp 1600w" sizes="(min-width:900px) 30rem, 92vw" width="1600" height="400" alt="{E(cap)}" loading="lazy" decoding="async"></picture><figcaption>{E(cap)}</figcaption></figure>'
def src(s):
    u = s.get('sources') or []
    return ' '.join(f'<a href="{E(x)}" rel="noopener">source {i}</a>' for i, x in enumerate(u, 1))
def blt(b): return ('built '+b) if re.match(r'^(\d|about|c\.)', b) else b[0].lower()+b[1:]
stops = ''.join(f'''<li class="wk" id="{s['id']}" data-ll="{s['lat']},{s['lon']}" data-n="{E(s['name'])}">
        <p class="mu-k">Stop {s['n']} of {len(S)}{(' · '+E(blt(str(s['built'])))) if s.get('built') else ''}<span class="wk-st"></span></p>
        <h3>{E(s['name'])}</h3>
        {pc(s)}
        <p class="wk-then"><b>Then.</b> {E(s['then'])}</p>
        <p class="wk-now"><b>Now.</b> {E(s['now'])}</p>
        {f'<p class="mu-a">{E(s["address"])}</p>' if s.get('address') else ''}
        <p class="wk-src">{src(s)}</p>
        <p class="mu-me"><button type="button" class="mu-sb wk-sb" hidden>I’m here: stamp it</button></p><p class="mu-msg" aria-live="polite"></p>
      </li>''' for s in S)
sanborn = ''.join(f'<li><a href="{E(x["url"])}" rel="noopener">{E(str(x["year"]))}</a>{(" · "+E(x["note"])) if x.get("note") else ""}</li>' for x in W.get('sanborn', []))
markers = ''.join(f'<li><a href="{E(x["url"])}" rel="noopener">{E(x["title"])}</a>{(" · "+E(x["location"])) if x.get("location") else ""}</li>' for x in W.get('markers', []))
route = json.dumps([[s['lat'], s['lon']] for s in S])
JS = r'''<script>
(function(){ "use strict";
  var $=function(s){ return document.querySelector(s); }, $$=function(s){ return [].slice.call(document.querySelectorAll(s)); };
  var calm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var stops=$$('.wk'), N=stops.length, cur=0, map=null, pins=[], plan=null, osm=null, line=null;
  var seen={}, stamp={}; try{ seen=JSON.parse(localStorage.getItem('ps-walk')||'{}')||{}; stamp=JSON.parse(localStorage.getItem('ps-walk-stamp')||'{}')||{}; }catch(e){}
  var save=function(){ try{ localStorage.setItem('ps-walk',JSON.stringify(seen)); localStorage.setItem('ps-walk-stamp',JSON.stringify(stamp)); }catch(e){} };
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
    if (Object.keys(seen).length===N && window.psEarn) window.psEarn('walker');
    paint(); };
  prev.addEventListener('click',function(){ show(cur-1); }); next.addEventListener('click',function(){ show(cur+1); });
  $('#wkBox').addEventListener('keydown',function(e){ if (e.target.closest('input,select,textarea')) return; if (e.key==='ArrowRight'){ show(cur+1); e.preventDefault(); } if (e.key==='ArrowLeft'){ show(cur-1); e.preventDefault(); } });
  stops.forEach(function(li,i){ var b=li.querySelector('.wk-sb'), m=li.querySelector('.mu-msg'); if (!b) return;
    b.addEventListener('click',function(){ if (!navigator.geolocation) return; m.textContent='Checking where you are…';
      navigator.geolocation.getCurrentPosition(function(p){ var d=km([p.coords.latitude,p.coords.longitude], LL(li)), reach=.12+Math.min(p.coords.accuracy||0,300)/1000;
        if (d<=reach){ stamp[li.id]=new Date().toISOString().slice(0,10); seen[li.id]=1; save(); paint(); m.textContent='Stamped. It stays on this device.'; if (window.psEarn) window.psEarn('stamp'); }
        else m.textContent='You look to be about '+(d*0.621371<10?(d*0.621371).toFixed(1):Math.round(d*0.621371))+' mi away. The stamp works on the spot.'; },
        function(){ m.textContent='No location shared, so nothing changed.'; }, {enableHighAccuracy:true, timeout:20000, maximumAge:0}); }); });
  /* the map: the 1860 plan of the village with the stops on it; today's streets only if asked for */
  var start=function(){ if (map || !window.L) return;
    map=L.map('wkMap',{zoomSnap:.25, minZoom:15, maxZoom:19, scrollWheelZoom:false, maxBounds:[[41.9,-86.03],[41.925,-85.995]]}); map.attributionControl.setPrefix(false);
    plan=L.imageOverlay('/img/cass1860.webp',[[41.9061,-86.018103],[41.917772,-86.007168]],{opacity:.9, className:'wk-plan'}).addTo(map);
    map.attributionControl.addAttribution('1860 plan: Geil, Harley &amp; Siverd, Library of Congress');
    line=L.polyline(__ROUTE__,{className:'wk-route', interactive:false}).addTo(map);
    stops.forEach(function(li,i){ var m=L.marker(LL(li),{icon:L.divIcon({className:'wk-pin', html:'<span>'+(i+1)+'</span>', iconSize:[26,26]}), title:'Stop '+(i+1)+': '+li.dataset.n, alt:'Stop '+(i+1)}).addTo(map);
      m.on('click',function(){ show(i,false); map.panTo(LL(li)); }); pins.push(m); });
    map.fitBounds(line.getBounds().pad(.25));
    map.on('focus click',function(){ map.scrollWheelZoom.enable(); }); map.on('blur mouseout',function(){ map.scrollWheelZoom.disable(); });
    var op=$('#wkOp'); op.hidden=false; op.querySelector('input').addEventListener('input',function(e){ plan.setOpacity(+e.target.value/100); });
    var sb=$('#wkOSM'); sb.hidden=false; sb.addEventListener('click',function(){ var on=sb.getAttribute('aria-pressed')!=='true'; sb.setAttribute('aria-pressed',String(on));
      if (on){ if (!osm) osm=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19, attribution:'Streets: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}); osm.addTo(map); osm.bringToBack(); }
      else map.removeLayer(osm); });
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
      if (bd>2000){ fmsg.textContent='You look to be away from Broadway. Following starts working when you are in downtown Cassopolis.'; return; }
      if (bd<=40+Math.min(p.coords.accuracy||0,40) && best!==cur){ show(best); if (navigator.vibrate) navigator.vibrate(90); fmsg.textContent='You are at stop '+(best+1)+': '+stops[best].dataset.n+'.'; if (playing) say(); }
    }, function(){ fmsg.textContent='No location shared, so following is off.'; fb.click(); }, {enableHighAccuracy:true, maximumAge:5000, timeout:30000}); }); }
  /* save the walk for the street: the page, the plan, the map code and the postcards go into this device's saved copy */
  var ob=$('#wkOff');
  if ('caches' in window && navigator.serviceWorker && navigator.serviceWorker.controller){ ob.hidden=false; ob.addEventListener('click',function(){ ob.textContent='Saving…';
    var urls=['/walk/','/img/cass1860.webp','/vendor/leaflet-1.9.4/leaflet.js?v=1','/vendor/leaflet-1.9.4/leaflet.css?v=1'].concat($$('.wk-list img').map(function(i){ return i.currentSrc||i.src; }), $$('link[rel=stylesheet][href*="?v="],script[src*="?v="]').map(function(e){ return e.getAttribute('href')||e.getAttribute('src'); }));
    caches.keys().then(function(k){ return caches.open(k.filter(function(x){ return /^ps-[0-9a-f]{6,}$/.test(x); })[0]||'ps-files'); })
      .then(function(c){ return Promise.all(urls.map(function(u){ return c.add(new Request(u,{cache:'reload'})).catch(function(){}); })); })
      .then(function(){ return navigator.storage && navigator.storage.persist ? navigator.storage.persist() : false; })
      .then(function(){ ob.textContent='Saved for no-signal use ✓'; fmsg.textContent='Saved. The walk, the 1860 plan and the postcards now open on this device without signal.'; })
      .catch(function(){ ob.textContent='Could not save'; }); }); }
  var h=location.hash.slice(1), at=stops.findIndex(function(li){ return li.id===h; });
  show(at>=0? at : 0, false); if (at>=0) $('#wkBox').scrollIntoView();
})();
</script>'''.replace('__ROUTE__', route)
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Broadway Virtual Walk</p>
    <figure class="pg-art"><picture><source type="image/avif" srcset="/img/card-walk-art-270.avif 270w, /img/card-walk-art.avif 540w" sizes="8rem"><img class="vt-walk" src="/img/card-walk-art-270.webp" srcset="/img/card-walk-art-270.webp 270w, /img/card-walk-art.webp 540w" sizes="8rem" width="540" height="960" alt="" decoding="async"></picture></figure>
    <h1>Walk old Broadway</h1>
    <p class="lede" style="font-size:1.15rem">Cassopolis, Michigan, from the 1860 plan to today: {len(S)} stops down the main street, each with what stood there, who ran it, and what is there now. Walk it from your chair, stop by stop on the old plan, or bring this page to Broadway and stamp each stop on the spot.</p>
    <div class="wk-box" id="wkBox">
      <div class="wk-map" id="wkMap" role="region" aria-label="The 1860 plan of Cassopolis with the stops of the walk. Every stop is also in the list below."><p class="mu-mapph">The 1860 plan opens here.</p></div>
      <div class="wk-side">
        <p class="wk-nav"><button type="button" class="btn" id="wkPrev">‹ Back</button> <span id="wkNum" aria-live="polite"></span> <button type="button" class="btn primary" id="wkNext">Next stop ›</button></p>
        <div class="wk-stage" id="wkStage" aria-live="polite"></div>
      </div>
      <p class="wk-tools"><label class="wk-op" id="wkOp" hidden>1860 plan <input type="range" min="0" max="100" value="90" aria-label="How strongly the 1860 plan shows"></label> <button type="button" class="btn mu-osm" id="wkOSM" aria-pressed="false" hidden>Show today’s streets</button> <button type="button" class="btn" id="wkPlay" aria-pressed="false" hidden>Play the tour aloud</button> <button type="button" class="btn" id="wkFollow" aria-pressed="false" hidden>Follow me on foot</button> <a class="btn" href="/map/3d/cassopolis/">Fly over it in 3D</a> <a class="btn" href="/map/cassopolis/">The full 1860 plan</a> <button type="button" class="btn" id="wkOff" hidden>Save for no-signal use</button></p>
      <p class="mu-mine" id="wkProg" aria-live="polite"></p>
    </div>
    <h2>Every stop</h2>
    <ol class="wk-list">{stops}</ol>
    {f'<h2>The fire-insurance sheets</h2><p>The Sanborn Map Company drew Cassopolis building by building for fire insurers. Each sheet shows what every building was made of and what it was used for. Open one beside this walk:</p><ul class="dis">{sanborn}</ul>' if sanborn else ''}
    {f'<h2>Historical markers in town</h2><ul class="dis">{markers}</ul>' if markers else ''}
    <h2>Walking it for real</h2>
    <ul class="dis">
      <li><b>Start at the north end</b> and walk south with the stops in order; the whole walk is under a mile.</li>
      <li><b>Let the page follow you.</b> “Follow me on foot” opens each stop as you reach it, and “Play the tour aloud” reads it to you, so you can keep your eyes on the street.</li>
      <li><b>Stamp as you go.</b> “I’m here” checks your location once, on your phone, and stamps that stop. Nothing leaves your device.</li>
      <li><b>Stay on the sidewalk</b> and on public ground, and be kind to the businesses: many of these buildings are still working shops and offices.</li>
      <li><b>Take the same picture.</b> Where a stop has an old postcard, stand where the photographer stood and <a href="/postcards/">send us your photo</a>.</li>
    </ul>
    <p class="note">The stops come from the county histories of 1875, 1882 and 1906, the Sanborn sheets, and the village and county records, each linked under its stop. The plan is the 1860 county wall map’s inset of Cassopolis. Where a date or name could not be confirmed, the stop says so. Corrections are welcome at research@projectscroll.com.</p>
{JS}
'''
page('walk/index.html', 'Broadway Virtual Walk · Cassopolis, Michigan · Project Scroll',
     f'Walk Broadway in Cassopolis, Michigan, stop by stop on the 1860 plan: {len(S)} buildings and sites with their history, the old postcards and what is there now. Walk it online, or on foot with a passport stamp at each stop.',
     body, og='https://projectscroll.com/og/cassopolis.jpg')
print('walk built', len(S))
