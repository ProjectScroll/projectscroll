"""The Valley map: every place on the site with a pin, on one map, in layers you can switch on and off.
python3 _tools/build_valleymap.py   (reads museums, food, seasons, walks, stories, postcards, lost towns, town plans,
and outdoors / drives / cemeteries / towns when present)

Each pin is a small dict (short keys, to keep the page light):
  l layer · n name · k kind · t town · a lat · o lon · h link · x one line · i "my day" id · p picture
  f free · oh hours · tz time zone · s,e first and last day (dated events) · sk passport stamp key · d directions"""
import sys, pathlib, json, re, html, math
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
import visitdata as V
import basemap
E = html.escape
ROOT = pathlib.Path(__file__).parent.parent
P = pathlib.Path(__file__).parent/'data'
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def load(n, d=None):
    f = P/n
    return json.load(open(f)) if f.exists() else d
def img(base):
    """the smallest picture we keep for a base path like /img/news/slug"""
    for suf in ('-600.webp', '-700.webp', '.webp'):
        if (ROOT/(base.lstrip('/')+suf)).exists(): return base+suf
    return ''

pts = []
def add(layer, name, kind, town, ll, href, extra='', **kw):
    if not ll or ll[0] in (None, '') : return None
    d = {'l': layer, 'n': name, 'k': kind, 't': town, 'a': round(float(ll[0]), 5), 'o': round(float(ll[1]), 5), 'h': href}
    if extra: d['x'] = extra
    d.update({k: v for k, v in kw.items() if v not in (None, '', 0, False)})
    pts.append(d); return d

FREE = re.compile(r'\b(free|no (?:park entry |trail-use )?fee|donations)\b', re.I)
def free_hours(s): return bool(s and re.search(r'(^|[.;,]\s*)(admission )?free\b|free admission|admission is free|no admission', s, re.I))

# ---- museums & historic places ----
KIND = {'museum':'Museum','historic site':'Historic site','historic house':'Historic house','historical society':'Historical society','archive':'Archive','library local history':'Library local-history room','library':'Library'}
for d in V.M:
    pl = V.mplace(d); mid = V.MID[d['name']]
    add('museum', d['name'], KIND.get(d['kind'], d['kind']), d['town'], d.get('ll'), f'/museums/#{mid}', (d.get('what') or '')[:150],
        i=pl['i'], d=pl['d'], oh=d.get('oh'), tz=d.get('tz'), f=free_hours(d.get('hours') or ''), sk='mu|'+mid, hr=(d.get('hours') or '')[:90])

# ---- places to eat and stay ----
for d in V.F:
    pl = V.fplace(d)
    if not pl['ll']: continue
    ty = 'stay' if d['type'] == 'lodging' else 'eat'
    add(ty, d['name'], (d.get('kind') or '').capitalize(), d['town'], pl['ll'], pl['u'], (d.get('what') or '')[:150],
        i=pl['i'], d=pl['d'], sk='fd|'+V.FID[d['name']])

# ---- festivals and seasons ----
MON = ['','January','February','March','April','May','June','July','August','September','October','November','December']
nfree = 0
for d in load('seasons.json', []):
    dt = d.get('dates2026') or {}
    fr = bool(re.search(r'free admission|admission is free|admission free|\bfree to (attend|the public)|free and open', d.get('what') or '', re.I)); nfree += fr
    add('fest', d['name'], d.get('when') or MON[d.get('month') or 0], d['town'], d.get('ll'), f'/seasons/#{slug(d["name"])}', (d.get('what') or '')[:150],
        i='s:'+slug(d['name']), d=d['name']+', '+d['town']+', '+V.ST.get(d['state'], d['state']), f=fr, mo=d.get('month'),
        s=dt.get('start'), e=dt.get('end') or dt.get('start'), sk='fe|'+slug(d['name']))

# ---- the two virtual walks ----
for key, f, town, label, href in (('w1', 'walk.json', 'Cassopolis', 'Broadway walk stop', '/walk/'), ('w2', 'walk-dowagiac.json', 'Dowagiac', 'Front Street walk stop', '/walk/dowagiac/')):
    for s in (load(f, {}) or {}).get('stops', []):
        add('walk', s['name'], label, town, (s['lat'], s['lon']), f'{href}#{s["id"]}', (s.get('then') or '')[:150],
            d=s['name']+', '+(s.get('address') or town), sk=key+'|'+s['id'])

# ---- stories with a place ----
TC = {n: (la, lo) for n, la, lo in V.TOWNS}
for st in load('news.json', {}).get('stories', []):
    if not st.get('ll'): continue
    ll = st['ll']
    if st['slug'].startswith('stone-lake'): ll = TC['Cassopolis']          # the story is pinned to the village, not the water
    pic = img(st['pic'][0]) if st.get('pic') else ''
    add('story', st['headline'], (st.get('kicker') or 'Story'), st.get('town',''), ll, f'/news/{st["slug"]}/', (st.get('short') or st.get('dek') or '')[:150],
        p=pic, pa=(st['pic'][1] if pic else ''))
have = {p['h'] for p in pts if p['l'] == 'story'}
sm = load('storymap.json', {}) or {}
for town, items in (sm.get('groups') or {}).items():
    if town not in TC: continue
    for k, (sl, title) in enumerate(items):
        if f'/news/{sl}/' in have: continue
        st = next((s for s in load('news.json', {}).get('stories', []) if s['slug'] == sl), {})
        # stories without their own spot sit in a small ring round the town centre, so none hides another
        la, lo = TC[town]; r = 0.0028; a = k*2.4
        pic = img(st['pic'][0]) if st.get('pic') else ''
        add('story', title, st.get('kicker') or 'Story', town, (la+r*math.cos(a), lo+r*1.35*math.sin(a)), f'/news/{sl}/', (st.get('short') or st.get('dek') or '')[:150],
            p=pic, pa=(st['pic'][1] if pic else ''))

# ---- old postcards, one pin per town ----
PCT = {'Benton Harbor / St. Joseph': ('Benton Harbor', 'benton-harbor-and-st-joseph'), 'Benton Harbor': ('Benton Harbor', 'benton-harbor-and-st-joseph'),
       'St. Joseph': ('St. Joseph', 'benton-harbor-and-st-joseph'), 'Coloma (Paw Paw Lake)': ('Coloma', 'coloma'), 'South Bend / Mishawaka': ('South Bend', 'south-bend-and-mishawaka'),
       'South Bend': ('South Bend', 'south-bend-and-mishawaka'), 'Mishawaka': ('Mishawaka', 'south-bend-and-mishawaka')}
cards = {}
for c in load('oldcards.json', []):
    town, anc = PCT.get(c['place'], (c['place'], slug(c['place'])))
    if town not in TC: continue
    cards.setdefault(town, [anc, []])[1].append(c)
for town, (anc, cs) in cards.items():
    la, lo = TC[town]
    c0 = cs[0]
    add('card', f'Old postcards of {town}', f'{len(cs)} card' + ('' if len(cs) == 1 else 's'), town, (la-0.004, lo-0.006), f'/postcards/#{anc}',
        f'{c0["title"]}, {c0.get("date","")}'.strip(', '), p=img(f'/img/oldcards/{c0["id"]}'), pa=c0['title'])

# ---- towns with a page of their own (and the name stories for the rest) ----
TOWNP = {'Cassopolis': '/cassopolis/', 'Dowagiac': '/dowagiac/', 'Niles': '/niles/', 'Paw Paw': '/paw-paw/'}
for t in load('towns.json', []) or []:                    # new town pages, when built
    if (ROOT/t['slug']/'index.html').exists(): TOWNP[t['name']] = f'/{t["slug"]}/'
for n, la, lo in V.TOWNS:
    href = TOWNP.get(n) or (f'/news/how-{slug(n)}-got-its-name/' if (ROOT/'news'/f'how-{slug(n)}-got-its-name').exists() else '')
    if href: add('town', n, 'Town page' if n in TOWNP else 'How it got its name', n, (la+0.004, lo+0.006), href)

# ---- lost towns (read from build_lost.py so the two never drift) ----
src = (pathlib.Path(__file__).parent/'build_lost.py').read_text(encoding='utf-8')
for m in re.finditer(r"dict\(n='([^']*)',(.*?)ll=\(([-\d.]+),\s*([-\d.]+)\)", src, re.S):
    n = m.group(1); sid = re.sub(r'[^a-z]+','-', n.lower().split(',')[0].split(' and ')[0]).strip('-')
    add('lost', n, 'Lost town', '', (m.group(3), m.group(4)), f'/lost-towns/#{sid}')

# ---- the old town plans, laid over today's streets ----
PLANS = [('cassopolis','Cassopolis, 1860',41.9117,-86.0097),('niles','Niles, 1860',41.8298,-86.2541),('dowagiac','Dowagiac, 1860',41.9842,-86.1086),
         ('paw-paw','Paw Paw, 1860',42.2178,-85.8911),('south-bend','South Bend, 1863',41.6764,-86.2520),('goshen','Goshen, 1861',41.5823,-85.8345),('elkhart','Elkhart, 1861',41.6820,-85.9767)]
OVL = {'cassopolis': ['/img/cass1860.webp', [[41.9061,-86.018103],[41.917772,-86.007168]]],
       'niles': ['/img/towns/niles1860.webp', [[41.821922,-86.265238],[41.841467,-86.238526]]],
       'dowagiac': ['/img/towns/dowagiac1860.webp', [[41.9772,-86.122047],[41.991542,-86.098734]]],
       'paw-paw': ['/img/towns/pawpaw1860.webp', [[42.215018,-85.903344],[42.224283,-85.877588]]]}
for k, n, la, lo in PLANS: add('plan', n, 'Old town plan over today’s streets', n.split(',')[0], (la, lo), f'/map/{k}/', ov=k if k in OVL else '')

# ---- outdoors, u-pick, drives and cemeteries, when their data exists ----
o = load('outdoors.json', {}) or {}
for d in (o.get('places') or []):
    fee = d.get('fee') or ''
    add('out', d['name'], d.get('category',''), d.get('town',''), (d.get('lat'), d.get('lon')), '/outdoors/#'+slug(d['name']), (d.get('do') or '')[:150],
        d=d['name']+', '+(d.get('address') or d.get('town','')), f=bool(re.match(r'(free|no (park entry |trail-use )?fee|donations|walk-ins free)', fee, re.I)))
for d in (o.get('upick') or []):
    add('out', d['name'], 'U-pick: '+(d.get('fruit') or '')[:60], d.get('town',''), (d.get('lat'), d.get('lon')), '/outdoors/#'+slug(d['name']), d.get('months',''),
        d=d['name']+', '+(d.get('address') or d.get('town','')))
DRIVES = []
for dr in (load('drives.json', []) or []):
    line = []
    for i, s in enumerate(dr.get('stops', [])):
        if add('drive', s['name'], f'{dr["title"]}, stop {i+1}', '', (s.get('lat'), s.get('lon')), f'/drives/{dr["slug"]}/#stop-{i+1}', (s.get('see') or '')[:150],
               d=s['name']+', '+(s.get('address') or '')): line.append([s['lat'], s['lon']])
    if len(line) > 1: DRIVES.append({'n': dr['title'], 'h': f'/drives/{dr["slug"]}/', 'p': line})
for g in (load('cemeteries.json', []) or []):
    for w in g.get('walk', []):
        if w.get('lat'): add('cem', w['name'], 'Historic cemetery', g.get('county','')+' County', (w['lat'], w['lon']), '/cemeteries/#'+slug(g['county']+' '+g['state']), (w.get('why') or '')[:150], d=w['name']+', '+(w.get('address') or ''))

LAYERS = [('museum','Museums &amp; historic places','#B8892A','M'),('story','Stories','#9C2F5C','N'),('fest','Festivals &amp; events','#3F7F4A','F'),
          ('eat','Places to eat','#B3362B','E'),('stay','Places to stay','#7A4E9C','S'),('out','Outdoors &amp; u-pick','#1F8A8A','O'),
          ('walk','Walk stops','#2F6FA0','W'),('card','Old postcards','#4C6A2E','C'),('town','Towns','#1D2733','T'),('lost','Lost towns','#6F6A60','L'),
          ('plan','Old town plans','#8A5A2B','P'),('drive','Drives','#C06A1A','D'),('cem','Historic cemeteries','#5A5F73','G')]
cnt = {k: sum(1 for p in pts if p['l'] == k) for k, *_ in LAYERS}
LAY = [l for l in LAYERS if cnt[l[0]]]
chips = ''.join(f'<button type="button" class="vm-chip" data-l="{k}" aria-pressed="true"><i style="background:{c}"></i>{t} <span>{cnt[k]}</span></button>' for k, t, c, _ in LAY)
N = len(pts)
nf = sum(1 for p in pts if p.get('f'))
print('free places', nf, 'free festivals', nfree)

JS = r'''
(function(){
  var P=__DATA__, NOPIN=__NOPIN__, COL=__COL__, CODE=__CODE__, OVL=__OVL__, DRV=__DRV__, $=function(s){ return document.querySelector(s); }, $$=function(s){ return [].slice.call(document.querySelectorAll(s)); };
  var box=$('#vmMap'), stat=$('#vmStat'), list=$('#vmList'), q=$('#vmQ'), sum=$('#vmSum'), on={}, map=null, lay=null, near=null, openNow=false, freeOnly=false, day='', month=false;
  var calm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ls=function(k,d){ try{ var v=JSON.parse(localStorage.getItem(k)||'null'); return v==null? d : v; }catch(e){ return d; } };
  var esc=function(s){ var d=document.createElement('div'); d.textContent=s==null?'':String(s); return d.innerHTML; };
  var iso=function(d){ return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2); };
  var nice=function(s){ return new Date(s+'T12:00:00').toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric'}); };
  var T0=new Date(), TODAY=iso(T0), T1=new Date(T0); T1.setDate(T0.getDate()+1); var TOM=iso(T1);

  /* ---- posted hours (the same reading the museums page uses) ---- */
  var DN=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'], DK={Su:0,Mo:1,Tu:2,We:3,Th:4,Fr:5,Sa:6};
  var parse=function(s){ if (s==='always') return {always:true}; var o={d:{}}, m=s.match(/@(\d+)-(\d+)/); if (m) o.season=[+m[1],+m[2]];
    s.replace(/@.*/,'').split(';').forEach(function(seg){ var p=seg.trim().split(' '); if (p.length<2) return; var h=p[1].split('-').map(Number);
      p[0].split(',').forEach(function(r){ var x=r.split('-'); if (x.length===2){ for (var i=DK[x[0]]; ; i=(i+1)%7){ o.d[i]=h; if (i===DK[x[1]]) break; } } else o.d[DK[r]]=h; }); });
    return o; };
  var clock=function(h){ var hh=Math.floor(h), mm=Math.round((h-hh)*60); if (hh===12 && !mm) return 'noon'; return (hh%12||12)+(mm?':'+('0'+mm).slice(-2):'')+(hh<12?' am':' pm'); };
  var nowAt=function(tz){ var p={}; new Intl.DateTimeFormat('en-US',{timeZone:tz==='C'?'America/Chicago':'America/Detroit', weekday:'short', month:'numeric', hour:'numeric', minute:'numeric', hourCycle:'h23'}).formatToParts(new Date()).forEach(function(x){ p[x.type]=x.value; });
    return {dow:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(p.weekday), mon:+p.month, h:(+p.hour%24)+(+p.minute)/60}; };
  P.forEach(function(p){ if (p.oh) try{ p._o=parse(p.oh); }catch(e){} });
  var openState=function(p){ var o=p._o; if (!o) return null; if (o.always) return {open:true, txt:'Open grounds, every day'}; var n=nowAt(p.tz), tz=p.tz==='C'?' Central':'';
    if (o.season && (n.mon<o.season[0] || n.mon>o.season[1])) return {open:false, txt:'Closed for the season'};
    var t=o.d[n.dow]; if (t && n.h>=t[0] && n.h<t[1]) return {open:true, txt:'Open now, until '+clock(t[1])+tz};
    if (t && n.h<t[0]) return {open:false, txt:'Opens today at '+clock(t[0])+tz};
    for (var k=1;k<=7;k++){ var d=(n.dow+k)%7; if (o.d[d] && (!o.season || true)) return {open:false, txt:'Closed now · next open '+(k===1?'tomorrow':DN[d])+' at '+clock(o.d[d][0])+tz}; }
    return null; };
  var openOn=function(p,s){ var o=p._o; if (!o) return null; if (o.always) return {open:true, txt:'Open grounds, every day'}; var dt=new Date(s+'T12:00:00'), w=dt.getDay(), mon=dt.getMonth()+1;
    if (o.season && (mon<o.season[0] || mon>o.season[1])) return {open:false, txt:'Closed for the season'};
    var t=o.d[w]; return t? {open:true, txt:'Open '+DN[w]+' '+clock(t[0])+' to '+clock(t[1])+(p.tz==='C'?' Central':'')} : {open:false, txt:'Closed on '+DN[w]+'s'}; };
  var runs=function(p,s){ return p.s && p.s<=s && p.e>=s; };

  /* ---- passport stamps and the "my day" list, both kept on this device only ---- */
  var ST={mu:ls('ps-mu-stamp',{}), fd:ls('ps-food-stamp',{}), fe:ls('ps-fest-stamp',{}), w1:ls('ps-walk-stamp',{}), w2:ls('ps-walk-dowagiac-stamp',{})}, BEEN=ls('ps-mu-been',[]);
  var stamped=function(p){ if (!p.sk) return ''; var a=p.sk.split('|'), t=ST[a[0]]||{};
    if (a[0]==='fe'){ for (var k in t) if (k.indexOf(a[1]+'-')===0) return t[k]; return ''; }
    if (t[a[1]]) return t[a[1]]; if (a[0]==='mu' && BEEN.indexOf(a[1])>=0) return 'visited'; return ''; };
  var DAY=ls('ps-day',[]); if (!Array.isArray(DAY)) DAY=[];
  var saveDay=function(){ try{ localStorage.setItem('ps-day',JSON.stringify(DAY)); localStorage.setItem('ps-mu-trip',JSON.stringify(DAY.filter(function(i){ return i.indexOf('m:')===0; }).map(function(i){ return i.slice(2); }))); }catch(e){}
    var c=$('#vmDayN'); if (c) c.textContent=DAY.length? ' ('+DAY.length+')' : ''; };
  saveDay();

  /* ---- what shows ---- */
  $$('.vm-chip').forEach(function(b){ on[b.dataset.l]=true; b.addEventListener('click',function(){ on[b.dataset.l]=!on[b.dataset.l]; b.setAttribute('aria-pressed',String(on[b.dataset.l])); draw(true); }); });
  var paintChips=function(){ $$('.vm-chip').forEach(function(b){ b.setAttribute('aria-pressed',String(!!on[b.dataset.l])); }); };
  var vis=function(p){ if (!on[p.l]) return false;
    if (freeOnly && !p.f) return false;
    if (month && p.l==='fest' && String(p.mo)!==String(T0.getMonth()+1)) return false;
    if (openNow){ if (p.l==='museum'){ var s=openState(p); if (!s || !s.open) return false; } if (p.l==='fest' && !runs(p,TODAY)) return false; }
    if (day){ if (p.l==='museum'){ var s2=openOn(p,day); if (!s2 || !s2.open) return false; } if (p.l==='fest' && !runs(p,day)) return false; }
    var t=q.value.trim().toLowerCase(); if (t && (p.n+' '+p.t+' '+p.k).toLowerCase().indexOf(t)<0) return false; return true; };
  var km=function(a,b){ var r=Math.PI/180, dl=(b[0]-a[0])*r, dn=(b[1]-a[1])*r, h=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a[0]*r)*Math.cos(b[0]*r)*Math.sin(dn/2)*Math.sin(dn/2); return 12742*Math.asin(Math.sqrt(h)); };
  var mi=function(k){ var m=k*0.621371; return m<10? m.toFixed(1) : String(Math.round(m)); };

  /* ---- the popup: picture, hours, passport, add to my day, directions ---- */
  var dirURL=function(p){ return 'https://www.google.com/maps/dir/?api=1&destination='+encodeURIComponent(p.d || (p.a+','+p.o)); };
  var pop=function(p){ var div=document.createElement('div'); div.className='mu-pop vm-pop';
    var h='';
    if (p.p) h+='<img src="'+p.p+'" alt="'+esc(p.pa||'')+'" width="240" height="160" loading="lazy" decoding="async">';
    h+='<p><b>'+esc(p.n)+'</b><br><small>'+esc(p.k)+(p.t?' · '+esc(p.t):'')+'</small></p>';
    if (p.l==='fest' && p.s) h+='<p class="vm-when"><small>'+(p.s===p.e? nice(p.s) : nice(p.s)+' to '+nice(p.e))+'</small></p>';
    if (p._o){ var s=day? openOn(p,day) : openState(p); if (s) h+='<p class="vm-open'+(s.open?' on':'')+'"><small>'+esc(s.txt)+(day?' ('+nice(day)+')':'')+'</small></p>'; }
    else if (p.hr) h+='<p><small>'+esc(p.hr)+'</small></p>';
    if (p.x && p.l!=='fest') h+='<p><small>'+esc(p.x)+'</small></p>';
    if (p.f) h+='<p class="vm-free"><small>Free</small></p>';
    var sd=stamped(p); if (sd) h+='<p class="vm-been"><small>✓ In your passport'+(sd!=='visited'?', '+esc(sd):'')+'</small></p>';
    h+='<p class="vm-acts">';
    if (p.ov) h+='<button type="button" class="vm-ovb">Lay the plan over today’s streets</button> ';
    if (p.i) h+='<button type="button" class="vm-add" aria-pressed="'+(DAY.indexOf(p.i)>=0)+'">'+(DAY.indexOf(p.i)>=0?'In my day ✓':'Add to my day')+'</button> ';
    if (p.d) h+='<a href="'+dirURL(p)+'" rel="noopener">Directions</a> · ';
    h+='<a href="'+p.h+'">'+(p.l==='story'?'Read the story':p.l==='card'?'See the cards':'Read more')+' ›</a></p>';
    div.innerHTML=h;
    var b=div.querySelector('.vm-add'); if (b) b.addEventListener('click',function(){ var k=DAY.indexOf(p.i); if (k>=0) DAY.splice(k,1); else DAY.push(p.i); saveDay();
      b.setAttribute('aria-pressed',String(k<0)); b.textContent=k<0?'In my day ✓':'Add to my day'; draw(); });
    var ob=div.querySelector('.vm-ovb'); if (ob) ob.addEventListener('click',function(){ var o=OVL[p.ov]; if (!o || !map) return; streets(true); map.fitBounds(o[1],{animate:!calm}); });
    return div; };

  /* ---- the list under the map ---- */
  var listDraw=function(v){ $('#vmN').textContent=v.length+(v.length===1?' place':' places');
    list.innerHTML=v.slice(0,500).map(function(p){ var d=near? '<span class="vm-d">'+mi(p._d)+' mi</span>':'', sd=stamped(p), extra='';
      if (p._o){ var s=day? openOn(p,day) : openState(p); if (s) extra=' <span class="vm-o'+(s.open?' on':'')+'">'+esc(s.txt)+'</span>'; }
      if (p.l==='fest' && p.s) extra=' <span class="vm-o">'+(p.s===p.e? nice(p.s) : nice(p.s)+' to '+nice(p.e))+'</span>';
      return '<li><i style="background:'+COL[p.l]+'"></i><a href="'+p.h+'">'+esc(p.n)+'</a>'+(sd?' <span class="vm-ck" title="In your passport">✓</span>':'')+(p.i&&DAY.indexOf(p.i)>=0?' <span class="vm-ck" title="In my day">★</span>':'')+
        ' <span class="vm-k">'+esc(p.k)+(p.t?' · '+esc(p.t):'')+extra+'</span>'+d+'</li>'; }).join(''); };

  /* ---- a quiet line saying what the chosen day holds ---- */
  var sumDraw=function(){ var d=day || (openNow? TODAY : ''); if (!d){ sum.hidden=true; return; }
    var mu=P.filter(function(p){ return p.l==='museum' && (openNow? (openState(p)||{}).open : (openOn(p,d)||{}).open); }).length, ev=P.filter(function(p){ return p.l==='fest' && runs(p,d); }).concat(NOPIN.filter(function(p){ return runs(p,d); }));
    sum.hidden=false; sum.textContent=(openNow? 'Open right now: ' : nice(d)+': ')+mu+(mu===1?' museum or historic place':' museums and historic places')+(openNow?' open this hour':' open')+(ev.length? ', and '+ev.length+(ev.length===1?' event: ':' events: ')+ev.map(function(e){ return e.n; }).join('; ') : ', and no fair or festival on the calendar')+'.'; };

  /* ---- clustering: nearby pins fold into one numbered circle until you zoom in ---- */
  var marks=null, overlays={}, lines=[];
  var cl=function(v){ if (!map) return; lay.clearLayers(); var z=map.getZoom();
    if (z>=12){ v.forEach(function(p){ lay.addLayer(p._m); }); }
    else { var cell=z<9?44:34, g={};
      v.forEach(function(p){ var pt=map.project([p.a,p.o],z), k=Math.floor(pt.x/cell)+':'+Math.floor(pt.y/cell); (g[k]=g[k]||[]).push(p); });
      Object.keys(g).forEach(function(k){ var ps=g[k]; if (ps.length<3){ ps.forEach(function(p){ lay.addLayer(p._m); }); return; }
        var la=0, lo=0, c={}; ps.forEach(function(p){ la+=p.a; lo+=p.o; c[p.l]=(c[p.l]||0)+1; }); la/=ps.length; lo/=ps.length;
        var top=Object.keys(c).sort(function(a,b){ return c[b]-c[a]; })[0], n=ps.length, sz=n<10?30:n<50?36:42;
        var m=L.marker([la,lo],{icon:L.divIcon({className:'vm-cl', html:'<span style="--c:'+COL[top]+';width:'+sz+'px;height:'+sz+'px">'+n+'</span>', iconSize:[sz,sz]}), keyboard:true, title:n+' places here: press to zoom in'});
        m.on('click',function(){ var b=L.latLngBounds(ps.map(function(p){ return [p.a,p.o]; })); if (b.getNorthEast().distanceTo(b.getSouthWest())<60) map.setView(b.getCenter(), Math.max(map.getZoom()+3,14)); else map.fitBounds(b.pad(.25),{animate:!calm, maxZoom:15}); });
        lay.addLayer(m); }); }
    // the 1860 plans appear over their towns when you are close enough to read them
    Object.keys(OVL).forEach(function(k){ var o=OVL[k], show=on.plan && z>=13; if (show && !overlays[k]) overlays[k]=L.imageOverlay(o[0],o[1],{opacity:.72, className:'vm-ovl', alt:'Plan of '+k+', about 1860'}); if (overlays[k]){ if (show && !map.hasLayer(overlays[k])) overlays[k].addTo(map); if (!show && map.hasLayer(overlays[k])) map.removeLayer(overlays[k]); } });
    lines.forEach(function(l){ if (on.drive && !map.hasLayer(l)) l.addTo(map); if (!on.drive && map.hasLayer(l)) map.removeLayer(l); }); };

  var cur=[];
  var draw=function(){ var v=P.filter(vis);
    if (near){ v.forEach(function(p){ p._d=km(near,[p.a,p.o]); }); v.sort(function(a,b){ return a._d-b._d; }); }
    else v.sort(function(a,b){ return (a.t||'~').localeCompare(b.t||'~') || a.n.localeCompare(b.n); });
    cur=v; listDraw(v); sumDraw(); cl(v); stat.textContent=v.length+' showing'; };

  /* ---- the tools ---- */
  q.addEventListener('input',function(){ draw(); });
  var tog=function(id,fn){ var b=$(id); b.addEventListener('click',function(){ var v=b.getAttribute('aria-pressed')!=='true'; b.setAttribute('aria-pressed',String(v)); fn(v); draw(); }); };
  tog('#vmOpen',function(v){ openNow=v; if (v){ day=''; $('#vmDay').value=''; $('#vmDate').hidden=true; } });
  tog('#vmFree',function(v){ freeOnly=v; });
  tog('#vmMonth',function(v){ month=v; });
  $('#vmDay').addEventListener('change',function(){ var v=this.value, di=$('#vmDate'); di.hidden=v!=='pick';
    day= v==='today'? TODAY : v==='tom'? TOM : v==='pick'? (di.value||'') : '';
    if (v==='pick' && !di.value){ di.value=TOM; day=TOM; di.focus(); }
    if (day){ openNow=false; $('#vmOpen').setAttribute('aria-pressed','false'); } draw(); });
  $('#vmDate').addEventListener('change',function(){ day=this.value||''; draw(); });
  $('#vmNear').addEventListener('click',function(){ var b=this; if (!navigator.geolocation){ stat.textContent='This browser cannot share a location.'; return; }
    stat.textContent='Finding you…'; navigator.geolocation.getCurrentPosition(function(g){ near=[g.coords.latitude,g.coords.longitude]; b.setAttribute('aria-pressed','true'); draw();
      if (map){ if (window._me) map.removeLayer(window._me); window._me=L.circleMarker(near,{radius:8,className:'vm-me'}).addTo(map).bindTooltip('You are here'); map.setView(near,11,{animate:!calm}); }
      $('#vmListH').scrollIntoView({behavior:calm?'auto':'smooth'}); }, function(){ stat.textContent='No location shared. The list is sorted by town.'; }, {timeout:10000}); });

  /* ---- share this view: the place, the zoom, the layers and the day, in the address ---- */
  var code=function(){ return Object.keys(CODE).filter(function(k){ return on[k]; }).map(function(k){ return CODE[k]; }).join(''); };
  $('#vmShare').addEventListener('click',function(){ var c=map? map.getCenter() : {lat:41.93,lng:-86.15}, z=map? map.getZoom() : 9;
    var h='#v-'+c.lat.toFixed(4)+'_'+c.lng.toFixed(4)+'_'+(Math.round(z*4)/4)+'_'+code()+'_'+(day||'')+'_'+(openNow?'o':'')+(freeOnly?'f':'')+(month?'m':'');
    var url=location.origin+location.pathname+h; try{ history.replaceState(null,'',h); }catch(e){}
    var done=function(){ stat.textContent='Link to this view copied.'; };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done,function(){ stat.textContent=url; }); else stat.textContent=url; });
  var want=null;
  var hs=location.hash;
  if (/^#v-/.test(hs)){ var a=hs.slice(3).split('_'); if (a.length>=4){ want=[+a[0],+a[1],+a[2]];
      Object.keys(CODE).forEach(function(k){ on[k]=a[3].indexOf(CODE[k])>=0; }); paintChips();
      if (a[4] && /^\d{4}-\d\d-\d\d$/.test(a[4])){ day=a[4]; $('#vmDay').value='pick'; $('#vmDate').hidden=false; $('#vmDate').value=day; }
      var fl=a[5]||''; if (fl.indexOf('o')>=0){ openNow=true; $('#vmOpen').setAttribute('aria-pressed','true'); } if (fl.indexOf('f')>=0){ freeOnly=true; $('#vmFree').setAttribute('aria-pressed','true'); } if (fl.indexOf('m')>=0){ month=true; $('#vmMonth').setAttribute('aria-pressed','true'); } } }
  else if (hs==='#today' || hs==='#tomorrow'){ day= hs==='#today'? TODAY : TOM; $('#vmDay').value= hs==='#today'?'today':'tom';
    Object.keys(on).forEach(function(k){ on[k]=(k==='museum'||k==='fest'); }); paintChips(); }

  /* ---- the map itself, loaded only when it comes into view ---- */
  var base=null, streets=function(){ if (base && base.get()==='plain') base.set('topo'); };
  var start=function(){ if (map || !window.L) return;
    $$('.mu-mapph').forEach(function(x){ x.remove(); });
    map=L.map(box,{zoomSnap:.25, minZoom:7, maxZoom:18, scrollWheelZoom:false, maxBounds:[[40.9,-87.9],[42.95,-84.3]], preferCanvas:true});
    map.attributionControl.setPrefix(false); map._home=L.latLngBounds([[41.42,-86.95],[42.43,-85.35]]);
    if (want) map.setView([want[0],want[1]], want[2]); else map.fitBounds(map._home);
    map.on('focus click',function(){ map.scrollWheelZoom.enable(); }); map.on('blur mouseout',function(){ map.scrollWheelZoom.disable(); });
    fetch('/museums/base.json?v=1').then(function(r){ return r.json(); }).then(function(b){ var pane=map.createPane('base'); pane.style.zIndex=250;
      b.c.forEach(function(c){ c.r.forEach(function(r){ L.polygon(r.map(function(p){ return [p[1],p[0]]; }),{pane:'base', className:c.d?'mu-cty in':'mu-cty', interactive:false}).addTo(map); }); });
      b.v.forEach(function(l){ L.polyline(l.map(function(p){ return [p[1],p[0]]; }),{pane:'base', className:'mu-rv', interactive:false}).addTo(map); });
      map.attributionControl.addAttribution('County lines: US Census Bureau · Rivers: USGS'); }).catch(function(){});
    lay=L.layerGroup().addTo(map);
    P.forEach(function(p){ var c=L.circleMarker([p.a,p.o],{radius:p.l==='town'?7:6, color:'#1d2733', weight:1.2, fillColor:COL[p.l], fillOpacity:.92, bubblingMouseEvents:false});
      c.bindPopup(function(){ return pop(p); },{maxWidth:260}); c.bindTooltip(p.n,{direction:'top', offset:[0,-6]}); p._m=c; });
    DRV.forEach(function(d){ var l=L.polyline(d.p,{color:COL.drive, weight:4, opacity:.8, dashArray:'8 6'}).bindTooltip(d.n,{sticky:true}); l.on('click',function(){ location.href=d.h; }); lines.push(l); });
    map.on('zoomend',function(){ cl(cur); });
    draw();
    base=window.psBase(map, box, $('#vmBase'), 'topo');
    $('#vmHome').hidden=false; $('#vmHome').addEventListener('click',function(){ map.fitBounds(map._home); }); };
  var need=function(){ if (window.L){ start(); return; } if (need.on) return; need.on=1;
    var l=document.createElement('link'); l.rel='stylesheet'; l.href='/vendor/leaflet-1.9.4/leaflet.css?v=1'; document.head.appendChild(l);
    var s=document.createElement('script'); s.src='/vendor/leaflet-1.9.4/leaflet.js?v=1'; s.onload=start; s.onerror=function(){ stat.textContent='The map could not load. The list below has every place.'; }; document.head.appendChild(s); };
  if (want || hs==='#today' || hs==='#tomorrow') need();
  else if ('IntersectionObserver' in window){ var io=new IntersectionObserver(function(e){ if (e.some(function(x){ return x.isIntersecting; })){ io.disconnect(); need(); } },{rootMargin:'300px'}); io.observe(box); } else need();
  draw();
})();
'''
pjs = json.dumps(pts, ensure_ascii=False, separators=(',',':')).replace('</', '<\\/')
JS = (JS.replace('__DATA__', pjs).replace('__COL__', json.dumps({k: c for k, _, c, _ in LAY}))
        .replace('__CODE__', json.dumps({k: cd for k, _, _, cd in LAY})).replace('__OVL__', json.dumps(OVL)).replace('__DRV__', json.dumps(DRIVES))
        .replace('__NOPIN__', json.dumps([{'n': d['name'], 's': d['dates2026']['start'], 'e': d['dates2026'].get('end') or d['dates2026']['start']} for d in load('seasons.json', []) if d.get('dates2026') and not d.get('ll')], ensure_ascii=False)))

body = f'''    <p class="crumb"><a href="/visit/">← Visit &amp; Plan</a></p>
    <p class="kicker">The whole valley, on one map</p>
    <h1>The valley map</h1>
    <p class="lede">Every place on Project Scroll that has a pin: {cnt.get('museum',0)} museums and historic places, {cnt.get('story',0)} stories, {cnt.get('fest',0)} festivals, {cnt.get('eat',0)+cnt.get('stay',0)} places to eat and stay, {cnt.get('out',0)} outdoor places, the walk stops, the old postcards, the lost towns and the old town plans. Pick a day to see what is open, switch the layers on and off, and open any pin for its story.</p>
    <p class="vm-today" id="vmSum" aria-live="polite" hidden></p>
    <div class="vm-tools vm-when" role="group" aria-label="When">
      <label class="vm-dsel">I’m visiting <select id="vmDay"><option value="">any day</option><option value="today">today</option><option value="tom">tomorrow</option><option value="pick">on a date…</option></select></label>
      <label class="vm-dsel" ><span class="sr">Date</span><input type="date" id="vmDate" hidden min="2026-01-01" max="2027-12-31"></label>
      <button type="button" class="btn" id="vmOpen" aria-pressed="false">Open now</button>
      <button type="button" class="btn" id="vmFree" aria-pressed="false">Free</button>
      <button type="button" class="btn" id="vmMonth" aria-pressed="false">Festivals this month</button>
    </div>
    <div class="vm-bar" role="group" aria-label="Map layers">{chips}</div>
    <div class="vm-tools">
      <label class="vm-q"><span class="sr">Find a place</span><input type="search" id="vmQ" placeholder="Find a place or town" autocomplete="off"></label>
      <button type="button" class="btn" id="vmNear">Near me</button>
      {basemap.buttons('topo','vmBase')}
      <button type="button" class="btn" id="vmHome" hidden>Whole valley</button>
      <button type="button" class="btn" id="vmShare">Share this view</button>
      <a class="btn" href="/visit/#build">My day<span id="vmDayN"></span></a>
      <span class="vm-stat" id="vmStat" aria-live="polite"></span>
    </div>
    <figure class="mu-mapf">
      <div class="mu-map vm-map" id="vmMap" role="region" aria-label="Map of every place on the site. Every place is also in the list below.">
        <p class="mu-mapph">The map opens here, with {N} pins.</p>
      </div>
      <figcaption class="vm-key">Pins sit at each place’s street address; stories without an address sit round their town. Close together, pins fold into a numbered circle: press it to zoom in. Zoom in on Cassopolis, Niles, Dowagiac or Paw Paw with the old town plans switched on to see the 1860 plan over today’s map. Map, Photo and Plain change the map underneath. ✓ marks places in your passport, ★ places in your day.</figcaption>
    </figure>
    <h2 id="vmListH">The places <span class="mu-n" id="vmN"></span></h2>
    <ol class="vm-list" id="vmList"></ol>
    <p class="note">“Open now” and the day you pick use each museum’s posted hours, and each festival’s 2026 dates; places with no posted hours drop out when a day is chosen. “Free” means free admission as posted. Your day list and passport stay on this device. Map pins come from each street address. The base map, with its town names, highways and street names, and the aerial photographs are from the USGS National Map, a free public-domain service of the US Geological Survey; your browser fetches its map pieces from the USGS while the map is open (choose “Plain” to stop that). County lines: US Census Bureau; rivers: USGS. “Near me” asks your browser for your location and uses it only on this page. “Directions” opens Google Maps. Hours and dates change: check each place before you go.</p>
    <p class="ctas"><a class="btn primary" href="/visit/">Plan a day out</a> <a class="btn" href="/museums/">Museums</a> <a class="btn" href="/food/">Food &amp; lodging</a> <a class="btn" href="/seasons/">Festivals</a> <a class="btn" href="/outdoors/">Outdoors</a></p>
<script>{basemap.BASE_JS}{JS}</script>
'''
page('valley-map/index.html', 'The valley map · every place on one map · Project Scroll',
     f'One map of the St. Joseph River valley with {N} places: museums, stories, festivals, places to eat and stay, outdoors, walk stops, old postcards, lost towns and 1860 town plans. Pick a day to see what is open.',
     body, og='https://projectscroll.com/og/valley-map.jpg?v=1')
print('valley map built', N, cnt)

# ---------- the home-page tile's live data: the dated festivals, placed on the tile picture ----------
_W, _H, _lat0, _lat1, _lon0, _lon1 = 960, 540, 41.45, 42.42, -86.95, -85.35
_k = math.cos(math.radians(41.95)); _sc = min(_W/((_lon1-_lon0)*_k), _H/(_lat1-_lat0)); _cx = (_lon0+_lon1)/2; _cy = (_lat0+_lat1)/2
def _xy(la, lo): return (round((_W/2+(lo-_cx)*_k*_sc)/_W*100, 2), round((_H/2-(la-_cy)*_sc)/_H*100, 2))
_ev = []
for d in load('seasons.json', []):
    dt = d.get('dates2026')
    if not dt: continue
    x, y = _xy(*d['ll']) if d.get('ll') else (None, None)
    _ev.append([d['name'], d['town'], dt['start'], dt.get('end') or dt['start'], x if x is not None and 0 <= x <= 100 else None, y if y is not None and 0 <= y <= 100 else None, slug(d['name'])])
open(ROOT/'valley-map'/'today.json', 'w').write(json.dumps({'n': N, 'ev': _ev}, ensure_ascii=False, separators=(',',':')))
print('valley map tile data', len(_ev))
