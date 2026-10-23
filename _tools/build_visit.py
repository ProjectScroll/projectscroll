"""Visit & Plan: everything a visitor from somewhere else needs for Cassopolis and the St. Joseph River valley.  python3 _tools/build_visit.py"""
import sys, pathlib, json, re, html, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
P = pathlib.Path(__file__).parent/'data'
E = lambda s: html.escape(s or '', quote=True)
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
S = json.load(open(P/'seasons.json')); F = json.load(open(P/'food.json')); M = json.load(open(P/'museums.json'))
today = datetime.date.today().isoformat()
up = sorted([d for d in S if isinstance(d.get('dates2026'),dict) and (d['dates2026'].get('end') or d['dates2026']['start']) >= today], key=lambda d: d['dates2026']['start'])
def fmt(dt):
    a = datetime.date.fromisoformat(dt['start']); b = datetime.date.fromisoformat(dt.get('end') or dt['start'])
    if a == b: return a.strftime('%a %-d %b %Y')
    return a.strftime('%-d %b') + ('–'+b.strftime('%-d %b %Y') if a.month!=b.month else '–'+b.strftime('%-d %b %Y'))
coming = ''.join(f'<li data-end="{d["dates2026"].get("end") or d["dates2026"]["start"]}"><a href="/seasons/#{slug(d["name"])}"><time datetime="{d["dates2026"]["start"]}">{fmt(d["dates2026"])}</time> <b>{E(d["name"])}</b> <span>{E(d["town"])}</span></a></li>' for d in up[:14])
n_eat = sum(1 for d in F if d.get('type')=='restaurant'); n_stay = sum(1 for d in F if d.get('type')=='lodging')
JS = r'''<script>
document.addEventListener('DOMContentLoaded', function(){ "use strict";
  var $=function(x){ return document.querySelector(x); }, $$=function(x){ return [].slice.call(document.querySelectorAll(x)); };
  var calm=matchMedia('(prefers-reduced-motion: reduce)').matches, glide=calm?'auto':'smooth';
  var t=new Date().toISOString().slice(0,10), n=0;
  $$('#vsComing li').forEach(function(li){ if (li.dataset.end<t || n>=6) li.hidden=true; else n++; });
  if (!n){ var p=$('#vsNone'); if (p) p.hidden=false; }
  $$('.vs-print').forEach(function(b){ b.addEventListener('click', function(){ var d=document.getElementById(b.dataset.day); document.documentElement.classList.add('vs-printing'); d.classList.add('vs-on'); window.print(); }); });
  addEventListener('afterprint', function(){ document.documentElement.classList.remove('vs-printing','vb-printing'); $$('.vs-on').forEach(function(x){ x.classList.remove('vs-on'); }); });

  /* open today: from each museum's posted hours, in its own time zone */
  var DN=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'], DK={Su:0,Mo:1,Tu:2,We:3,Th:4,Fr:5,Sa:6};
  var parse=function(s){ if (s==='always') return {always:true}; var o={d:{}}, m=s.match(/@(\d+)-(\d+)/); if (m) o.season=[+m[1],+m[2]];
    s.replace(/@.*/,'').split(';').forEach(function(seg){ var q=seg.trim().split(' '); if (q.length<2) return; var h=q[1].split('-').map(Number);
      q[0].split(',').forEach(function(r){ var x=r.split('-'); if (x.length===2){ for (var i=DK[x[0]]; ; i=(i+1)%7){ o.d[i]=h; if (i===DK[x[1]]) break; } } else o.d[DK[r]]=h; }); });
    return o; };
  var clock=function(h){ var hh=Math.floor(h), mm=Math.round((h-hh)*60); if (hh===12 && !mm) return 'noon'; return (hh%12||12)+(mm?':'+('0'+mm).slice(-2):'')+(hh<12?' am':' pm'); };
  var nowAt=function(tz){ var q={}; new Intl.DateTimeFormat('en-US',{timeZone:tz==='C'?'America/Chicago':'America/Detroit', weekday:'short', month:'numeric', hour:'numeric', minute:'numeric', hourCycle:'h23'}).formatToParts(new Date()).forEach(function(x){ q[x.type]=x.value; });
    return {dow:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(q.weekday), mon:+q.month, h:(+q.hour%24)+(+q.minute)/60}; };
  var state=function(oh,tz){ var o=parse(oh); if (o.always) return {open:true, txt:'open every day'}; var w=nowAt(tz);
    if (o.season && (w.mon<o.season[0] || w.mon>o.season[1])) return {open:false, txt:'closed for the season'};
    var d=o.d[w.dow];
    if (d && w.h>=d[0] && w.h<d[1]) return {open:true, txt:'open now, until '+clock(d[1])};
    if (d && w.h<d[0]) return {open:true, txt:'open today from '+clock(d[0])};
    for (var k=1;k<=7;k++){ var x=(w.dow+k)%7; if (o.d[x]) return {open:false, txt:(d?'closed for today':'closed today')+' · next open '+(k===1?'tomorrow':DN[x])}; }
    return null; };
  var MN=['January','February','March','April','May','June','July','August','September','October','November','December'];
  var onDate=function(oh,iso){ var o=parse(oh); if (o.always) return {open:true, txt:'open every day'}; var dt=new Date(iso+'T12:00:00'), dow=dt.getDay(), mon=dt.getMonth()+1;
    if (o.season && (mon<o.season[0] || mon>o.season[1])) return {open:false, txt:'closed that time of year'};
    var d=o.d[dow]; return d? {open:true, txt:'open '+clock(d[0])+'–'+clock(d[1])+' that day'} : {open:false, txt:'closed on '+DN[dow]+'s'}; };
  var DKEY='ps-visit-date', pick=''; try{ pick=localStorage.getItem(DKEY)||''; }catch(e){}
  var di=$('#vsDate'), dx=$('#vsDateX'), dm=$('#vsDateMsg'), fl=$('#vsFest'), FEST=JSON.parse($('#vsFestJ').textContent);
  var nice=function(iso){ var d=new Date(iso+'T12:00:00'); return DN[d.getDay()]+' '+d.getDate()+' '+MN[d.getMonth()]; };
  var hours=function(){ var today=new Date().toISOString().slice(0,10); if (pick && pick<today){ pick=''; }
    $$('.vs-days li[data-oh]').forEach(function(li){ try{ var st=pick? onDate(li.dataset.oh,pick) : state(li.dataset.oh, li.dataset.tz), e=li.querySelector('.vs-open'); if (st && e){ e.textContent=' · '+st.txt; e.classList.toggle('on', st.open); e.classList.toggle('off', !st.open); } }catch(err){} });
    $$('.vs-day').forEach(function(day){ var f=day.querySelector('.vs-fit'); if (!pick){ f.hidden=true; return; }
      var shut=[].slice.call(day.querySelectorAll('li[data-oh]')).filter(function(li){ var st=onDate(li.dataset.oh,pick); return !st.open; }).map(function(li){ return li.dataset.n; }).filter(function(v,i,a){ return a.indexOf(v)===i; });
      f.hidden=false; f.className='vs-fit '+(shut.length?'no':'ok'); f.textContent=shut.length? 'On '+nice(pick)+': '+shut.length+(shut.length>1?' museums are':' museum is')+' closed: '+shut.join('; ')+'.' : 'Works on '+nice(pick)+': every museum on this day is open.'; });
    di.value=pick; dx.hidden=!pick; fl.innerHTML=''; fl.hidden=true;
    if (pick){ var on=FEST.filter(function(f){ return f[1]<=pick && pick<=f[2]; }); dm.textContent=on.length? 'Going on in the valley that day:' : 'No festival on our calendar that day. The days below show which museums are open.';
      on.forEach(function(f){ var li=document.createElement('li'), a=document.createElement('a'); a.href='/seasons/#'+f[4]; a.textContent=f[0]; li.appendChild(a); li.appendChild(document.createTextNode(' · '+f[3])); fl.appendChild(li); }); fl.hidden=!on.length; }
    else dm.textContent='';
    if (window.vbPaint) window.vbPaint(); };
  di.min=new Date().toISOString().slice(0,10);
  di.addEventListener('change',function(){ pick=di.value; try{ pick? localStorage.setItem(DKEY,pick) : localStorage.removeItem(DKEY); }catch(e){} hours(); });
  dx.addEventListener('click',function(){ pick=''; try{ localStorage.removeItem(DKEY); }catch(e){} hours(); });
  hours();
  /* stamps: how much of each ready-made day you have stamped, and the Day-tripper badge for all of one */
  var stamps={}; try{ (window.psStamps? window.psStamps() : []).forEach(function(x){ var pre=x.key==='ps-mu-stamp'?'m:':x.key==='ps-food-stamp'?'f:':x.key==='ps-walk-stamp'?'w:walk':x.key==='ps-walk-dowagiac-stamp'?'w:dowagiac':''; if (pre) stamps[pre.length>2?pre:pre+x.id]=1; }); }catch(e){}
  $$('.vs-day').forEach(function(day){ var ids=[].slice.call(day.querySelectorAll('li[data-i]')).map(function(li){ return li.dataset.i; }).filter(function(v,i,a){ return a.indexOf(v)===i; });
    var got=ids.filter(function(i){ return stamps[i]; }); var pg=day.querySelector('.vs-prog'); if (!ids.length || !got.length) return;
    pg.hidden=false; pg.textContent=got.length===ids.length? '✓ Every stop of this day is stamped in your passport.' : 'Your passport: '+got.length+' of '+ids.length+' stops stamped.';
    if (got.length===ids.length && window.psEarn) window.psEarn('daytrip'); });

  /* weather: the National Weather Service forecast for Cassopolis */
  var w=$('#vsWx'); if (w && window.fetch){ var go=function(){ fetch('https://api.weather.gov/points/41.912,-86.010',{headers:{'Accept':'application/geo+json'}}).then(function(r){ return r.json(); }).then(function(j){ return fetch(j.properties.forecast).then(function(r){ return r.json(); }); }).then(function(f){ var p=f.properties.periods; if (!p||!p.length) return; var a=p[0], b=p[1];
      w.innerHTML='<span class="mu-wxk">Weather in the valley</span> <b></b> <span></span>'; w.querySelector('b').textContent=a.name+': '+a.temperature+'°'+a.temperatureUnit+', '+a.shortForecast.toLowerCase();
      if (b) w.querySelector('span:last-child').textContent='· '+b.name+': '+b.temperature+'°'+b.temperatureUnit+', '+b.shortForecast.toLowerCase(); w.hidden=false; }).catch(function(){}); };
    if ('requestIdleCallback' in window) requestIdleCallback(go,{timeout:3000}); else setTimeout(go,1500); }

  /* the map of the days */
  var DAYS=JSON.parse($('#vsDays').textContent), map=null, layers={}, lg=$('#vsLegend');
  DAYS.forEach(function(d){ var b=document.createElement('button'); b.type='button'; b.className='vs-lg'; b.dataset.k=d.k; b.style.setProperty('--dc',d.c); b.innerHTML='<i class="vs-dot"></i>'; b.appendChild(document.createTextNode(d.t)); b.addEventListener('click',function(){ focus(d.k, false); }); lg.appendChild(b); });
  var TOWNS=__TOWNS__;
  var start=function(){ if (map || !window.L) return; $$('#vsMap .mu-mapph').forEach(function(x){ x.remove(); });
    map=L.map('vsMap',{zoomSnap:.25, minZoom:7, maxZoom:16, scrollWheelZoom:false, maxBounds:[[40.9,-87.9],[42.95,-84.3]]}); map.attributionControl.setPrefix(false);
    map.fitBounds([[41.42,-86.75],[42.46,-85.38]]);
    map.on('focus click',function(){ map.scrollWheelZoom.enable(); }); map.on('blur mouseout',function(){ map.scrollWheelZoom.disable(); });
    fetch('/museums/base.json?v=1').then(function(r){ return r.json(); }).then(function(b){ var pane=map.createPane('base'); pane.style.zIndex=250;
      b.c.forEach(function(c){ c.r.forEach(function(r){ L.polygon(r.map(function(q){ return [q[1],q[0]]; }),{pane:'base', className:c.d?'mu-cty in':'mu-cty', interactive:false}).addTo(map); }); });
      b.v.forEach(function(l){ L.polyline(l.map(function(q){ return [q[1],q[0]]; }),{pane:'base', className:'mu-rv', interactive:false}).addTo(map); });
      map.attributionControl.addAttribution('County lines: US Census Bureau · Rivers: USGS'); }).catch(function(){});
    TOWNS.forEach(function(x){ L.marker([x[1],x[2]],{interactive:false, keyboard:false, icon:L.divIcon({className:'vs-town', html:'<span>'+x[0]+'</span>', iconSize:null})}).addTo(map); });
    DAYS.forEach(function(d){ var g=L.featureGroup(); var ll=d.p.map(function(q){ return [q[0],q[1]]; });
      if (ll.length>1) L.polyline(ll,{color:d.c, weight:3, opacity:.85, dashArray:'6 5', interactive:false}).addTo(g);
      d.p.forEach(function(q,i){ L.circleMarker([q[0],q[1]],{radius:7, color:'#fff', weight:1.5, fillColor:d.c, fillOpacity:1, bubblingMouseEvents:false}).bindTooltip((i+1)+'. '+q[2]+' · '+d.t,{direction:'top', offset:[0,-6]}).on('click',function(){ focus(d.k,true); }).addTo(g); });
      g.addTo(map); layers[d.k]=g; }); drawMine(); };
  var mine=null, mineBtn=null;
  var drawMine=function(){ if (!map || !P) return; if (mine){ map.removeLayer(mine); mine=null; }
    var pts=day.map(function(i){ return byI[i]; }).filter(function(x){ return x && x.ll; });
    if (!mineBtn){ mineBtn=document.createElement('button'); mineBtn.type='button'; mineBtn.className='vs-lg vs-mine'; mineBtn.dataset.k='mine'; mineBtn.style.setProperty('--dc','var(--ink)'); mineBtn.innerHTML='<i class="vs-dot"></i>My day'; mineBtn.addEventListener('click',function(){ focus('mine',false); }); lg.appendChild(mineBtn); }
    mineBtn.hidden=!pts.length; if (!pts.length){ delete layers.mine; return; }
    mine=L.featureGroup(); var css=getComputedStyle(document.documentElement).getPropertyValue('--ink').trim()||'#1D2733';
    if (pts.length>1) L.polyline(pts.map(function(x){ return x.ll; }),{color:css, weight:3.5, opacity:.9, interactive:false}).addTo(mine);
    pts.forEach(function(x,i){ L.marker(x.ll,{icon:L.divIcon({className:'vs-num', html:'<span>'+(i+1)+'</span>', iconSize:[22,22]}), keyboard:false}).bindTooltip((i+1)+'. '+x.n+' · My day',{direction:'top', offset:[0,-8]}).addTo(mine); });
    mine.addTo(map); layers.mine=mine; };
  var focus=function(k, toList){ if (!map) return; $$('.vs-lg').forEach(function(b){ b.setAttribute('aria-pressed',String(b.dataset.k===k)); });
    Object.keys(layers).forEach(function(x){ layers[x].eachLayer(function(l){ if (l.setStyle) l.setStyle(x===k?{opacity:1, fillOpacity:1}:{opacity:.25, fillOpacity:.25}); }); });
    var g=layers[k]; if (g && g.getLayers().length) map.fitBounds(g.getBounds().pad(.35),{maxZoom:11, animate:!calm});
    if (toList){ var li=document.getElementById(k==='mine'?'build':'day-'+k); li.scrollIntoView({behavior:glide, block:'start'}); } };
  var need=function(cb){ if (window.L){ start(); if (cb) cb(); return; } if (need.q){ if (cb) need.q.push(cb); return; } need.q=cb?[cb]:[];
    var l=document.createElement('link'); l.rel='stylesheet'; l.href='/vendor/leaflet-1.9.4/leaflet.css?v=1'; document.head.appendChild(l);
    var sc=document.createElement('script'); sc.src='/vendor/leaflet-1.9.4/leaflet.js?v=1'; sc.onload=function(){ start(); need.q.forEach(function(f){ f(); }); }; document.head.appendChild(sc); };
  if ('IntersectionObserver' in window){ var io=new IntersectionObserver(function(e){ if (e.some(function(x){ return x.isIntersecting; })){ io.disconnect(); need(); } },{rootMargin:'300px'}); io.observe($('#vsMap')); } else need();
  $$('.vs-show').forEach(function(b){ b.addEventListener('click',function(){ need(function(){ $('#vsMap').scrollIntoView({behavior:glide, block:'center'}); focus(b.dataset.k,false); }); }); });

  /* build your own day: places from the museums, food and lodging, and the walks */
  var KEY='ps-day', day=[]; try{ day=JSON.parse(localStorage.getItem(KEY)||'[]')||[]; }catch(e){}
  var save=function(){ try{ localStorage.setItem(KEY,JSON.stringify(day)); localStorage.setItem('ps-mu-trip', JSON.stringify(day.filter(function(i){ return i.indexOf('m:')===0; }).map(function(i){ return i.slice(2); }))); }catch(e){} };
  var P=null, byI={}, bq=$('#vbQ'), res=$('#vbRes'), list=$('#vbList'), msg=$('#vbMsg'), gob=$('#vbGo');
  var km=function(a,b){ var R=6371, r=Math.PI/180, dl=(b[0]-a[0])*r, dn=(b[1]-a[1])*r, h=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a[0]*r)*Math.cos(b[0]*r)*Math.sin(dn/2)*Math.sin(dn/2); return 2*R*Math.asin(Math.sqrt(h)); };
  var mi=function(k){ var m=k*0.621371*1.25; return m<10? m.toFixed(1) : String(Math.round(m)); };
  var load=function(cb){ if (P){ cb(); return; } fetch('/visit/places.json?v=1').then(function(r){ return r.json(); }).then(function(j){ P=j; P.forEach(function(x){ byI[x.i]=x; }); day=day.filter(function(i){ return byI[i]; }); cb(); }).catch(function(){ msg.textContent='The list of places could not load. Try again in a moment.'; }); };
  /* rough timing: about 35 mph between stops, and a usual length of stay for each kind of place */
  var stay=function(x){ var k=(x.k||'').toLowerCase(), g=x.g||'';
    if (g==='Places to stay') return 0; if (g==='Walking tours') return 60;
    if (/ice cream|candy|bakery|pastry|soda/.test(k)) return 25; if (/orchard|market|cider/.test(k)) return 45;
    if (g==='Places to eat') return 60; if (/library|archive/.test(k)) return 90; if (/historic site/.test(k)) return 40; if (/museum/.test(k)) return 75; return 60; };
  var hm=function(m){ var h=Math.floor(m/60)%24, mm=m%60; return (h%12||12)+':'+('0'+mm).slice(-2)+(h<12?' am':' pm'); };
  var dur=function(m){ return m<60? m+' min' : Math.floor(m/60)+' h'+(m%60? ' '+m%60+' min':''); };
  var paint=function(){ list.innerHTML=''; $('#vbN').textContent=day.length; $('#vbEmpty').hidden=!!day.length; var clockAt=9*60+30;
    day.forEach(function(i,ix){ var x=byI[i], r=document.createElement('li'), a=document.createElement('a');
      var drive=0, gap=(ix>0 && x.ll && byI[day[ix-1]].ll)? km(byI[day[ix-1]].ll,x.ll) : null; if (gap!==null) drive=gap<0.5? 5 : Math.max(5, Math.round(gap*1.25/56*60/5)*5); clockAt+=drive;
      var tm=document.createElement('span'); tm.className='vb-time'; tm.textContent=(stay(x)===0 && ix>0? 'Evening' : hm(clockAt)); r.appendChild(tm);
      a.href=x.u; a.textContent=x.n; r.appendChild(a);
      var s=document.createElement('span'); s.className='mu-tt'; s.textContent=' · '+x.t+(gap===null? '' : gap<0.5? ' · a short walk from the last stop' : ' · about '+dur(drive)+' drive, '+mi(gap)+' mi')+(stay(x)? ' · stay about '+dur(stay(x)) : ''); r.appendChild(s);
      clockAt+=stay(x);
      if (pick && x.oh){ var st=onDate(x.oh,pick); if (!st.open){ var w2=document.createElement('span'); w2.className='vb-warn'; w2.textContent=' · '+st.txt+' ('+nice(pick)+')'; r.appendChild(w2); } }
      var up=document.createElement('button'); up.type='button'; up.className='mu-up'; up.textContent='↑'; up.disabled=ix===0; up.setAttribute('aria-label','Move '+x.n+' earlier');
      up.addEventListener('click',function(){ day.splice(ix,1); day.splice(ix-1,0,i); save(); paint(); }); r.appendChild(up);
      var xb=document.createElement('button'); xb.type='button'; xb.className='mu-x'; xb.textContent='×'; xb.setAttribute('aria-label','Take '+x.n+' off my day');
      xb.addEventListener('click',function(){ day.splice(ix,1); save(); paint(); find(); }); r.appendChild(xb); list.appendChild(r); });
    var ds=day.map(function(i){ return byI[i].d; }).slice(0,10);
    if (ds.length){ gob.href='https://www.google.com/maps/dir/?api=1&travelmode=driving&destination='+encodeURIComponent(ds[ds.length-1])+(ds.length>1?'&waypoints='+ds.slice(0,-1).map(encodeURIComponent).join('%7C'):''); gob.hidden=false; gob.textContent=day.length>10?'Open the first ten in Google Maps':'Open in Google Maps'; } else gob.hidden=true;
    var mt=[]; try{ mt=JSON.parse(localStorage.getItem('ps-mu-trip')||'[]')||[]; }catch(e){} $('#vbMu').hidden=!mt.filter(function(id){ return day.indexOf('m:'+id)<0; }).length;
    if (day.length) { var nt=document.createElement('li'); nt.className='vb-note'; nt.textContent='Times are rough: they start at 9:30 am and allow about 35 mph between stops.'; list.appendChild(nt); }
    drawMine(); };
  window.vbPaint=function(){ if (P) paint(); };
  var find=function(){ var w=bq.value.trim().toLowerCase().split(/\s+/).filter(Boolean); res.innerHTML=''; if (!w.length || !P) return;
    var hits=P.filter(function(x){ var tx=(x.n+' '+x.t+' '+x.k+' '+x.g).toLowerCase(); return w.every(function(q){ return tx.indexOf(q)>=0; }); }).slice(0,8);
    if (!hits.length){ var e=document.createElement('li'); e.className='vb-none'; e.textContent='Nothing by that name yet.'; res.appendChild(e); return; }
    hits.forEach(function(x){ var r=document.createElement('li'), b=document.createElement('button'); b.type='button'; b.className='btn vb-add'; var on=day.indexOf(x.i)>=0;
      b.textContent=on?'On my day ✓':'Add'; b.disabled=on; b.setAttribute('aria-label',(on?'Already on my day: ':'Add to my day: ')+x.n);
      b.addEventListener('click',function(){ if (day.indexOf(x.i)<0){ day.push(x.i); save(); paint(); msg.textContent=x.n+' added.'; find(); } });
      var s=document.createElement('span'); s.innerHTML='<b></b> <small></small>'; s.querySelector('b').textContent=x.n; s.querySelector('small').textContent=x.t+' · '+x.g; r.appendChild(b); r.appendChild(s); res.appendChild(r); }); };
  bq.addEventListener('focus',function(){ load(find); }); bq.addEventListener('input',function(){ load(find); });
  $('#vbBest').addEventListener('click',function(){ load(function(){ var Q=day.filter(function(i){ return byI[i].ll; }), rest=day.filter(function(i){ return !byI[i].ll; });
    if (Q.length<3){ msg.textContent='Add at least three places to sort them.'; return; }
    var D=function(a,b){ return km(byI[a].ll,byI[b].ll); }, path=[Q[0]], left=Q.slice(1);
    while (left.length){ var last=path[path.length-1]; left.sort(function(a,b){ return D(last,a)-D(last,b); }); path.push(left.shift()); }
    var len=function(r){ var s=0; for (var i=1;i<r.length;i++) s+=D(r[i-1],r[i]); return s; }, better=true;
    while (better){ better=false; for (var i=1;i<path.length-1;i++) for (var j=i+1;j<path.length;j++){ var c=path.slice(0,i).concat(path.slice(i,j+1).reverse(), path.slice(j+1)); if (len(c)<len(path)-1e-9){ path=c; better=true; } } }
    day=path.concat(rest); save(); paint(); msg.textContent='Put in the shortest order by distance, starting at '+byI[day[0]].n+'. About '+mi(len(path))+' mi of driving.'; }); });
  var url=function(){ return location.origin+'/visit/?day='+day.map(encodeURIComponent).join(',')+'#build'; };
  $('#vbShare').addEventListener('click',function(){ if (!day.length){ msg.textContent='Add a place or two first.'; return; } var u=url();
    if (navigator.share){ navigator.share({title:'A day in the St. Joseph River valley', text:day.map(function(i){ return byI[i].n; }).join(' → '), url:u}).catch(function(){}); return; }
    if (navigator.clipboard) navigator.clipboard.writeText(u).then(function(){ msg.textContent='Link copied. Paste it into a message or post.'; }, function(){ msg.textContent='Copy this link: '+u; }); else msg.textContent='Copy this link: '+u; });
  $('#vbPrint').addEventListener('click',function(){ document.documentElement.classList.add('vb-printing'); window.print(); });
  $('#vbClear').addEventListener('click',function(){ day=[]; save(); paint(); find(); msg.textContent=''; });
  $('#vbMu').addEventListener('click',function(){ load(function(){ var mt=[]; try{ mt=JSON.parse(localStorage.getItem('ps-mu-trip')||'[]')||[]; }catch(e){} var k=0;
    mt.forEach(function(id){ var i='m:'+id; if (byI[i] && day.indexOf(i)<0){ day.push(i); k++; } }); save(); paint(); msg.textContent=k? k+' museums brought in from your museums trip.' : 'Those museums are already on your day.'; }); });
  var qs=new URLSearchParams(location.search).get('day');
  if (qs){ load(function(){ var got=qs.split(',').filter(function(i){ return byI[i]; }); if (got.length){ day=got; save(); paint(); msg.textContent='A shared day, saved on this device. Change it as you like.'; } }); }
  else if (day.length) load(paint); else paint();
});
</script>'''
CARDS = [
 ('/food/eat/', 'Eat', f'{n_eat} places to eat with a story: old taverns, soda fountains, a diner beside an auto museum, orchards and farm markets.'),
 ('/food/stay/', 'Stay', f'{n_stay} inns, bed and breakfasts and historic hotels, from Kalamazoo to the lakeshore.'),
 ('/seasons/', 'What’s on', f'{len(S)} fairs, festivals, harvests and holiday walks on a twelve-month calendar you can subscribe to.'),
 ('/museums/', 'Museums & historic places', f'{len(M)} museums, historic houses, libraries and archives on one map, with “open today”, directions and a trip planner.'),
 ('/walk/', 'Walk old Broadway', 'Eleven stops through downtown Cassopolis, with old postcards and the 1860 plan underfoot. Works offline.'),
 ('/walk/dowagiac/', 'Walk Front Street', 'Thirteen stops through downtown Dowagiac: the stove works, the lure makers and the railroad.'),
 ('/passport/', 'Your passport', 'Press “I’m here” at a museum, a stop, a table or a festival to collect stamps and print a certificate.'),
 ('/postcards/', 'Old postcards', 'More than a hundred views of the valley’s towns as they were, to compare with what you see today.'),
]

import visitdata as V
DAYS=[
 ('cass-dow','A day in Cassopolis and Dowagiac','Best on a Tuesday or Friday, when both Dowagiac museums are open; the log cabin keeps summer hours.',[
   ('Morning','Walk old Broadway in Cassopolis, eleven stops with the 1860 plan underfoot.','/walk/',('w','walk')),
   ('Morning','The Local History Branch, in the 1909 Carnegie library: county histories, maps and family files (Mon–Thu).',None,('m','Cass District Library – Local History Branch')),
   ('Morning','The Pioneer Log Cabin Museum on South Broadway, built in 1923 (open through the season; check its website).',None,('m','Pioneer Log Cabin Museum')),
   ('Lunch','Holden Green Tavern, in the old post office storefront on Broadway.',None,('f','Holden Green Tavern')),
   ('Afternoon','Drive about 11 miles to Dowagiac: the Dowagiac Area History Museum, for the Round Oak stove story.',None,('m','Dowagiac Area History Museum')),
   ('Afternoon','Walk Front Street, thirteen stops, with the Heddon Museum’s lures on the way (Tue and Fri; call ahead).','/walk/dowagiac/',('m','Heddon Museum')),
   ('Treat','A soda at Caruso’s, on Front Street since 1922.',None,('f',"Caruso's Candy & Soda Fountain")),
   ('Supper','The Wounded Minnow, in the 1913 Elks Temple, or the Old Tavern Inn at Sumnerville, opened in 1835.',None,('f','Wounded Minnow Saloon'))]),
 ('research','A research day for family historians','Monday to Thursday, when the Local History Branch is open. Bring names, dates and places, a notebook and a pencil.',[
   ('Morning','The Local History Branch, in the 1909 Carnegie library: county histories, old directories, maps and family files. Ask at the desk where to begin.',None,('m','Cass District Library – Local History Branch')),
   ('Late morning','The Cass County Clerk/Register office, upstairs in the old courthouse at 120 N. Broadway, for birth, death and marriage records and the deed books. Call ahead (269-445-4464) to ask what you can see in person.',None,('x','Cass County Clerk/Register office','Cass County Clerk Register Office, 120 N Broadway, Cassopolis, MI 49031',[41.91202,-86.01243])),
   ('Lunch','Holden Green Tavern, two doors down Broadway in the old post office.',None,('f','Holden Green Tavern')),
   ('Afternoon','Prospect Hill Cemetery, the village cemetery on Disbrow Street, with burials going back to the 1830s. Take our guide to reading old gravestones.','/guide/gravestones/',('x','Prospect Hill Cemetery','Prospect Hill Cemetery, Disbrow St, Cassopolis, MI 49031')),
   ('Before you go home','Stuck on a name? Write down what you found and where, and bring us your mystery.','/#services',None)]),
 ('niles','Niles and the river','A half day; the Fort St. Joseph Museum is open Wednesday to Saturday.',[
   ('Morning','The Fort St. Joseph Museum and the Niles History Center.',None,('m','Fort St. Joseph Museum (Niles History Center)')),
   ('Morning','The Four Flags City sites around downtown, mostly seen from outside.',None,('m','Niles Historic Sites (Four Flags City)')),
   ('Lunch','The Old Tavern Inn at Sumnerville, opened in 1835 as a stagecoach stop.',None,('f','Old Tavern Inn')),
   ('Stay','The Morris Estate, a riverside estate kept as a bed and breakfast.',None,('f','The Morris Estate'))]),
 ('free','A day that costs nothing','Wednesday to Friday, when both free museums are open. The two walks are free at any hour.',[
   ('Morning','Walk old Broadway in Cassopolis.','/walk/',('w','walk')),
   ('Late morning','The Dowagiac Area History Museum: admission is free.',None,('m','Dowagiac Area History Museum')),
   ('Afternoon','Walk Front Street in Dowagiac.','/walk/dowagiac/',('w','dowagiac')),
   ('Afternoon','The Fort St. Joseph Museum in Niles, also free.',None,('m','Fort St. Joseph Museum (Niles History Center)')),
   ('Worth the money','If you spend a little, spend it on a soda at Caruso’s.',None,('f',"Caruso's Candy & Soda Fountain"))]),
 ('rainy','A rainy day in South Bend','Any day of the week: the two museums sit side by side on one campus, open Monday to Saturday 10–5 and Sunday 12–5.',[
   ('Morning','The Studebaker National Museum: wagons, carriages and cars from the company that began in a South Bend blacksmith shop.',None,('m','Studebaker National Museum')),
   ('Lunch','Sunny Italy Cafe, South Bend’s oldest Italian restaurant, opened in 1926.',None,('f','Sunny Italy Cafe')),
   ('Afternoon','The History Museum next door, with the Oliver Mansion on its campus.',None,('m','The History Museum')),
   ('Supper','Café Navarre, in a restored bank building at the old center of downtown.',None,('f','Café Navarre')),
   ('Stay','The Oliver Inn, the 1886 house James Oliver built for his daughter.',None,('f','Oliver Inn Bed & Breakfast'))]),
 ('fall','A fall drive to the orchards','Late September to late October; the color is usually best around the middle of October. Best Wednesday to Saturday, when the museums are open.',[
   ('Morning','Start in Niles at the Fort St. Joseph Museum.',None,('m','Fort St. Joseph Museum (Niles History Center)')),
   ('Lunch','Follow the river north to Buchanan: Thistledown & Row, with house-made ciders in the 1884 Redden Building.',None,('f','Thistledown & Row')),
   ('Afternoon','The History Center at Courthouse Square in Berrien Springs (Wed–Sun; closed in winter).',None,('m','History Center at Courthouse Square (Berrien County Historical Association)')),
   ('Afternoon','Jollay Orchards near Coloma, farmed by one family since 1857: cider and doughnuts at the fall market.',None,('f','Jollay Orchards')),
   ('Supper','Blackbird Waterhouse near Coloma, a roadhouse since the late 1920s.',None,('f','Blackbird Waterhouse'))]),
 ('fruit','A weekend in the fruit belt','Blossom time from late April, blueberries in July, apples and cider in the fall.',[
   ('Saturday','Jollay Orchards near Coloma, farmed by the same family since 1857 (fall market).',None,('f','Jollay Orchards')),
   ('Saturday','The Morton House Museum in Benton Harbor (Wed and Sat 11–2). On a weekday, the North Berrien Historical Museum in Coloma instead.',None,('m','Morton House Museum')),
   ('Saturday','The St. Joseph pier lights; inner tours on summer Saturdays, weather permitting.',None,('m','St. Joseph North Pier Lights')),
   ('Supper','Grande Mere Inn at Stevensville.',None,('f','Grande Mere Inn')),
   ('Sunday','The Region of Three Oaks Museum (spring to October, Fri–Sun afternoons).',None,('m','Region of Three Oaks Museum')),
   ('Stay','The Inn at Union Pier or Gordon Beach Inn, near the lake.',None,('f','Gordon Beach Inn'))]),
 ('amish','Elkhart County and the Amish country','Best Tuesday to Saturday, when all three are open; many businesses close on Sundays. Mind the buggies.',[
   ('Morning','Bonneyville Mill near Bristol, the old grist mill (mid-April to mid-November, Tue–Sun).',None,('m','Bonneyville Mill')),
   ('Morning','The Elkhart County Historical Museum in Bristol (Tue–Sat).',None,('m','Elkhart County Historical Museum')),
   ('Lunch','Das Dutchman Essenhaus in Middlebury, or the Blue Gate in Shipshewana.',None,('f','Das Dutchman Essenhaus')),
   ('Afternoon','Menno-Hof in Shipshewana (Mon–Sat 10–5).',None,('m','Menno-Hof')),
   ('Afternoon','Coppes Commons in Nappanee, the old kitchen-cabinet factory.',None,('m','Coppes Commons and Coppes History Museum')),
   ('Stay','Market St. Manor in Nappanee.',None,('f','Market St. Manor'))]),
 ('kzoo','Kalamazoo and the Gilmore','A full day, Monday to Thursday, when the Kellogg Manor House is open; the Gilmore keeps longer hours from April to November.',[
   ('Morning','The Gilmore Car Museum at Hickory Corners.',None,('m','Gilmore Car Museum')),
   ('Lunch','George & Sally’s Blue Moon Diner, a 1941 diner on the Gilmore grounds.',None,('f',"George & Sally's Blue Moon Diner (Gilmore Car Museum)")),
   ('Afternoon','The W.K. Kellogg Manor House (Mon–Thu; call ahead).',None,('m','W.K. Kellogg Manor House')),
   ('Supper','Bell’s Eccentric Café in Kalamazoo.',None,('f',"Bell's Eccentric Café")),
   ('Stay','Henderson Castle or The Kalamazoo House.',None,('f','Henderson Castle'))]),
]
import oldcards as O
PIC={'cass-dow':'ps002','research':'ps005','niles':'ps046','free':'ps011','rainy':'ps071','fall':'ps054','fruit':'ps050','amish':'ps081','kzoo':'ps067'}
def dpic(k):
    d=O.BY[PIC[k]]
    return f'<figure class="vs-pic">{O.pic(d, "(min-width:900px) 11rem, 40vw")}<figcaption>{E(d["title"])} · {E(d["date"])}</figcaption></figure>'
FEST=[[d['name'],d['dates2026']['start'],d['dates2026'].get('end') or d['dates2026']['start'],d['town'],slug(d['name'])] for d in S if isinstance(d.get('dates2026'),dict)]
COL=['#B3362B','#2E7D56','#2F6DB5','#8A5A9E','#C77A12','#0F8B8D','#A23B72','#5B7F1F','#6B4F2A']
DJSON=[]
def stop(a,b,h,r,k,n):
    pl = V.ref(r) if r else None
    href = h or (pl.get('u') if pl else '')
    oh = f' data-oh="{E(pl["oh"])}"' if pl and pl.get('oh') else ''
    tz = ' data-tz="C"' if pl and pl.get('tz')=='C' else ''
    open_ = '<span class="vs-open"></span>' if oh else ''
    link = f'<a href="{E(href)}">{E(b)}</a>' if href else E(b)
    di_ = (f' data-i="{pl["i"]}"' if pl and pl.get('i') else '') + (f' data-n="{E(pl["n"].split(" (")[0])}"' if pl else '')
    return f'<li{oh}{tz}{di_}><span class="vs-t">{E(a)}</span> {link}{open_}</li>', pl
days=''
for di,(k,t,w,st) in enumerate(DAYS):
    lis=[]; pls=[]
    for a,b,h,r in st:
        li,pl=stop(a,b,h,r,k,di); lis.append(li)
        if pl: pls.append(pl)
    gm=V.gmaps([p['d'] for p in pls])
    pts=[]
    for p in pls:
        if p.get('ll') and (not pts or pts[-1][:2]!=list(p['ll'])): pts.append([p['ll'][0],p['ll'][1],p['n']])
    DJSON.append({'k':k,'t':t,'c':COL[di%len(COL)],'p':pts})
    days+=(f'<li class="vs-day" id="day-{k}" data-k="{k}" style="--dc:{COL[di%len(COL)]}">{dpic(k)}<h3><i class="vs-dot" aria-hidden="true"></i>{E(t)}</h3><p class="vs-when">{E(w)}</p><p class="vs-fit" hidden></p><p class="vs-prog" hidden></p><ol>'+''.join(lis)+
      f'</ol><p class="vs-acts">'+(f'<a class="btn vs-gm" href="{E(gm)}" rel="noopener">Open this day in Google Maps</a> ' if gm else '')+
      f'<button type="button" class="btn vs-show" data-k="{k}">Show on the map</button> <button type="button" class="btn vs-print" data-day="day-{k}">Print this day</button></p><p class="vs-spon"><a href="/sponsors/">Sponsor this day ›</a></p></li>')
JS=JS.replace('__TOWNS__', json.dumps([[n,la,lo] for n,la,lo in V.TOWNS]))
FESTJSON=json.dumps(FEST,ensure_ascii=False).replace('</','<\\/')
DAYJSON=json.dumps(DJSON,ensure_ascii=False).replace('</','<\\/')
open(pathlib.Path(__file__).parent.parent/'visit'/'places.json','w').write(json.dumps(V.all_places(),ensure_ascii=False,separators=(',',':')))

cards = ''.join(f'<li><a href="{h}"><b>{E(t)}</b><span>{E(d)}</span></a></li>' for h,t,d in CARDS)
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Visit &amp; Plan</p>
    <h1>Coming to the St. Joseph River valley</h1>
    <p class="lede" style="font-size:1.15rem">Cassopolis and the towns around it, from Kalamazoo to Lake Michigan and down into northern Indiana, are an easy trip from Chicago, Detroit and Indianapolis. Here is what to see, where to eat and stay, what’s on, and how to get here, all in one place.</p>
    <ul class="vs-cards">{cards}</ul>
    <section aria-labelledby="vsDH"><h2 id="vsDH">Ready-made days out</h2>
      <p>Days planned for you, each in an order that saves driving. Open any of them in Google Maps for the route, or print it. Museum hours below are worked out from each place’s posted hours; they don’t know about holidays, so check before you go. Every place’s posted hours were last checked in October 2026.</p>
      <p class="mu-wx" id="vsWx" hidden></p>
      <div class="vs-date"><label><span>Coming on a particular day?</span> <input type="date" id="vsDate"></label> <button type="button" class="linkbtn" id="vsDateX" hidden>Back to today</button>
        <p id="vsDateMsg" aria-live="polite"></p><ul class="vs-fest" id="vsFest" hidden></ul></div>
      <figure class="mu-mapf vs-mapf">
        <div class="mu-map vs-map" id="vsMap" role="region" aria-label="Map of the ready-made days. Every stop is also listed below."><p class="mu-mapph">The map of the days opens here.</p></div>
        <figcaption class="vs-legend" id="vsLegend"></figcaption>
      </figure>
      <ol class="vs-days">{days}</ol>
      <p><a class="btn" href="/visit/project-scroll-pocket-guide.pdf" download>Download the pocket guide (PDF, to print and fold)</a></p></section>
    <section aria-labelledby="vsBH" id="build"><h2 id="vsBH">Build your own day</h2>
      <p>Pick museums, places to eat and stay, and the walks. We’ll put them in a sensible driving order, and you can open the route in Google Maps, print it, or send it to someone. Your day is kept on this device only, and it is the same list as “My trip” on the museums page.</p>
      <div class="vs-build">
        <label class="nm-q"><span>Find a place to add</span><input type="search" id="vbQ" placeholder="A town, a museum, a restaurant, an inn" autocomplete="off" spellcheck="false"></label>
        <ul class="vb-res" id="vbRes" aria-live="polite"></ul>
        <div class="vb-day" id="vbDay">
          <h3>My day <span class="mu-n"><span id="vbN">0</span> stops</span></h3>
          <ol id="vbList"></ol>
          <p class="vb-empty" id="vbEmpty">Nothing yet. Search above, or press “Add to my day” on the <a href="/food/">food and lodging</a> page.</p>
          <p class="mu-tacts"><button type="button" class="btn" id="vbBest">Best order</button> <a class="btn" id="vbGo" href="#" rel="noopener" hidden>Open in Google Maps</a> <button type="button" class="btn" id="vbShare">Share this day</button> <button type="button" class="btn" id="vbPrint">Print</button> <button type="button" class="btn" id="vbMu" hidden>Bring in my museums trip</button> <button type="button" class="linkbtn" id="vbClear">Start over</button></p>
          <p class="mu-tmsg" id="vbMsg" aria-live="polite"></p>
        </div>
      </div></section>
    <section aria-labelledby="vsCH"><h2 id="vsCH">Coming up</h2>
      <ol class="vs-coming" id="vsComing">{coming}</ol>
      <p class="note" id="vsNone" hidden>Nothing on the calendar for the next few weeks. See the <a href="/seasons/">full year</a>.</p>
      <p><a class="btn" href="/seasons/">The whole year</a> <a class="btn" href="/seasons/valley.ics">Add the calendar to your phone</a></p></section>
    <section aria-labelledby="vsGH"><h2 id="vsGH">Getting here</h2>
      <ul class="dis">
        <li><b>By car.</b> Cassopolis is about 2 hours from Chicago, 3 from Detroit, 3 from Indianapolis, an hour and three-quarters from Grand Rapids, an hour from Kalamazoo and half an hour from South Bend. Times are approximate and vary with traffic.</li>
        <li><b>By air.</b> South Bend International Airport is the nearest, about half an hour from Cassopolis. Kalamazoo/Battle Creek International is about an hour; the Chicago airports about two and a half.</li>
        <li><b>By train.</b> Amtrak’s Michigan trains between Chicago and Detroit or Port Huron stop at Niles and Dowagiac, and at Kalamazoo. Amtrak’s long-distance trains stop at South Bend and Elkhart, and the South Shore Line runs from downtown Chicago to the South Bend airport. Check current schedules before you plan.</li>
        <li><b>Mind the clock.</b> The Michigan towns and South Bend, Elkhart and Goshen keep Eastern time, but La Porte County, Indiana, including La Porte and Michigan City, keeps Central time: an hour earlier.</li>
      </ul></section>
    <section aria-labelledby="vsWH"><h2 id="vsWH">When to come</h2>
      <ul class="dis">
        <li><b>Spring.</b> Maple syrup festivals in March, then the orchards in bloom from late April, with Blossomtime in St. Joseph and Benton Harbor.</li>
        <li><b>Summer.</b> The county fairs, the National Blueberry Festival in South Haven, u-pick berries and the lake towns. Most small museums keep summer hours, roughly Memorial Day to Labor Day.</li>
        <li><b>Fall.</b> Apples and cider in the fruit belt, the straw-bale art trail around Shipshewana, and the fall colour along the St. Joseph River.</li>
        <li><b>Winter.</b> Candlelight parades and lights in December, and ice festivals in St. Joseph, South Haven, Dowagiac and Shipshewana.</li>
      </ul></section>
    <section aria-labelledby="vsTH"><h2 id="vsTH">Good to know</h2>
      <ul class="dis">
        <li><b>Check before you go.</b> Many museums are run by volunteers and open only a few days a week, some only in summer. Each card on the <a href="/museums/">museums page</a> links to the place’s own site; ring ahead if you are travelling far.</li>
        <li><b>Amish country.</b> In and around Shipshewana and Middlebury, many businesses close on Sundays, and you will share the roads with horse-drawn buggies: slow down and pass wide.</li>
        <li><b>Save the walks.</b> The Broadway and Front Street walks keep working without a signal once you have opened them; phone coverage can be thin between towns.</li>
        <li><b>Be a good guest.</b> Many old buildings on the walks are homes and businesses: look from the sidewalk, and never go onto private property without leave.</li>
        <li><b>Plan a day.</b> Take one of the days above, or <a href="#build">build your own</a> from the museums, the places to eat and stay, and the walks.</li>
      </ul></section>
    <section aria-labelledby="vsIH"><h2 id="vsIH">Visitor information</h2>
      <ul class="dis">
        <li><a href="https://www.swmichigan.org/" rel="noopener">Southwestern Michigan Tourist Council</a>: Berrien, Cass and Van Buren counties.</li>
        <li><a href="https://www.discoverkalamazoo.com/" rel="noopener">Discover Kalamazoo</a>.</li>
        <li><a href="https://www.visitsouthbend.com/" rel="noopener">Visit South Bend Mishawaka</a>.</li>
        <li><a href="https://www.visitelkhartcounty.com/" rel="noopener">Visit Elkhart County</a>: Elkhart, Goshen, Middlebury, Nappanee and Bristol.</li>
        <li><a href="https://www.michigan.org/" rel="noopener">Pure Michigan</a>, the state’s travel site.</li>
      </ul>
      <p class="note">Project Scroll is independent and not affiliated with any of these. Spotted something out of date? <a href="/story/">Tell us</a>.</p></section>
''' + f'<script type="application/json" id="vsDays">{DAYJSON}</script><script type="application/json" id="vsFestJ">{FESTJSON}</script>\n' + JS + '\n'
page('visit/index.html', 'Visit & Plan: coming to Cassopolis and the St. Joseph River valley · Project Scroll',
     'Planning a trip to Cassopolis and the St. Joseph River valley: places to eat and stay with a story, festivals and fairs, museums, walking tours, getting here by car, air or train, and when to come.', body, og='https://projectscroll.com/og/cassopolis.jpg')
print('visit built', len(up))
