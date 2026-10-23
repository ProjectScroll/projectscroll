"""Seasons & Festivals: the valley's yearly fairs, festivals, harvests and holiday walks, month by month.
python3 _tools/build_seasons.py   (data in _tools/data/seasons.json, each event checked against its own website)"""
import sys, pathlib, json, html, re
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E = html.escape
D = [d for d in json.load(open(pathlib.Path(__file__).parent/'data'/'seasons.json')) if d.get('keep', True)]
MON = ['','January','February','March','April','May','June','July','August','September','October','November','December']
SEAS = [('spring','Spring','Blossoms, sap buckets and the first open days', [3,4,5]), ('summer','Summer','County fairs, band concerts and festivals', [6,7,8]),
        ('fall','Fall','Harvest, cider, colour and living history', [9,10,11]), ('winter','Winter','Lights, Christmas walks and warm rooms', [12,1,2])]
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def iso(d):
    for k in ('dates2026','dates2027'):
        v = d.get(k)
        if isinstance(v, dict) and v.get('start'): return v
    return None
import math as _m
_F=[x for x in json.load(open(pathlib.Path(__file__).parent/'data'/'food.json')) if x.get('ll') and x.get('type')=='restaurant']
def _km(a,b):
    r=_m.pi/180; dl=(b[0]-a[0])*r; dn=(b[1]-a[1])*r; h=_m.sin(dl/2)**2+_m.cos(a[0]*r)*_m.cos(b[0]*r)*_m.sin(dn/2)**2; return 12742*_m.asin(_m.sqrt(h))
def _fid(n): return re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-')
def eatnear(d):
    if not d.get('ll'): return ''
    xs=sorted(((_km(d['ll'],x['ll'] if isinstance(x['ll'],list) else json.loads(x['ll'])),x) for x in _F), key=lambda t:t[0])
    xs=[(k,x) for k,x in xs if k<=12][:2]
    if not xs: return ''
    return '<p class="fd-near">A table nearby: '+' · '.join(f'<a href="/food/{"stay" if x.get("type")=="lodging" else "eat"}/#{_fid(x["name"])}">{E(x["name"])}</a> ({(k*0.621371):.0f} mi)' if k*0.621371>=1 else f'<a href="/food/{"stay" if x.get("type")=="lodging" else "eat"}/#{_fid(x["name"])}">{E(x["name"])}</a> (in town)' for k,x in xs)+'</p>'
def card(d):
    dt = iso(d)
    when = E(d.get('when') or '')
    exact = ''
    if dt:
        exact = f' data-start="{E(dt["start"])}" data-end="{E(dt.get("end") or dt["start"])}"'
    hist = f'<p class="se-h">{E(d["history"])}</p>' if d.get('history') else ''
    link = f'<a class="mu-go" href="{E(d["url"])}" rel="noopener">Their website ›</a>' if d.get('url') else '<span class="mu-none">No website: ask locally</span>'
    chk = '' if d.get('verified') else '<span class="mu-chk" title="We could not confirm the latest dates online. Check before you go.">check the dates</span>'
    cal = '<button type="button" class="linkbtn se-cal">Add to my calendar</button>' if dt else ''
    stp = '<p class="mu-me"><button type="button" class="mu-sb se-sb" hidden>I’m here: stamp it</button></p><p class="mu-msg" aria-live="polite"></p>' if (dt and d.get('ll')) else ''
    return f'''<li class="se" id="{slug(d['name'])}"{(' data-ll="'+str(d['ll'][0])+','+str(d['ll'][1])+'"') if d.get('ll') else ''} data-m="{d['month']}" data-c="{E(d['county'])}"{exact} data-n="{E(d['name'])}" data-town="{E(d['town'])}" data-u="{E(d.get('url') or '')}" data-t="{E((d['name']+' '+d['town']+' '+d['county']+' '+d.get('what','')).lower())}">
        <p class="mu-k">{E(MON[d['month']])} · {E(d['town'])}, {E(d['state'])}{chk}</p>
        <h3>{E(d['name'])}</h3>
        <p class="se-w"><b>{when}</b><span class="se-d"></span></p>
        <p>{E(d.get('what',''))}</p>{hist}
        {eatnear(d)}<p class="mu-acts">{link}{' · '+cal if cal else ''}{(' · <button type="button" class="mu-tb fd-add" data-i="s:'+slug(d['name'])+'" aria-pressed="false">Add to my day</button>') if d.get('ll') else ''}</p>
        {stp}
      </li>'''
secs = ''
for k, t, sub, ms in SEAS:
    evs = sorted([d for d in D if d['month'] in ms], key=lambda d: (ms.index(d['month']), d['name']))
    secs += f'''    <section class="se-s" id="{k}" data-ms="{','.join(map(str,ms))}"><h2>{t} <span class="mu-n">{len(evs)} events</span></h2><p class="se-sub">{sub}</p>
      <ul class="se-list">{''.join(card(d) for d in evs)}</ul></section>
'''
counties = sorted({d['county']+'|'+d['state'] for d in D}, key=lambda x: (x.split('|')[1]!='MI', x))
copts = ''.join(f'<option value="{E(c.split("|")[0])}">{E(c.split("|")[0])} County, {"Michigan" if c.split("|")[1]=="MI" else "Indiana"}</option>' for c in counties)
months = ''.join(f'<button type="button" class="se-mb" data-m="{i}" aria-pressed="false">{MON[i][:3]}</button>' for i in range(1,13))
n = len(D)
items = []
for d in D:
    dt = iso(d)
    if not dt: continue
    ev = {'@type':'Event','name':d['name'],'startDate':dt['start'],'endDate':dt.get('end') or dt['start'],'eventStatus':'https://schema.org/EventScheduled',
          'eventAttendanceMode':'https://schema.org/OfflineEventAttendanceMode','description':d.get('what',''),
          'location':{'@type':'Place','name':d['town'],'address':{'@type':'PostalAddress','addressLocality':d['town'],'addressRegion':d['state'],'addressCountry':'US'}}}
    if d.get('url'): ev['url'] = d['url']
    items.append(ev)
ld = ('<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':items}, ensure_ascii=False).replace('</','<\\/')+'</script>') if items else ''
import datetime
def icsx(t): return t.replace('\\','\\\\').replace(',','\\,').replace(';','\\;').replace('\n','\\n')
today = datetime.date.today().isoformat(); stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
ev = []
for d in D:
    dt = iso(d)
    if not dt or (dt.get('end') or dt['start']) < today: continue
    e = datetime.date.fromisoformat(dt.get('end') or dt['start']) + datetime.timedelta(days=1)
    lines = ['BEGIN:VEVENT', f'UID:{slug(d["name"])}-{dt["start"].replace("-","")}@projectscroll.com', 'DTSTAMP:'+stamp, 'DTSTART;VALUE=DATE:'+dt['start'].replace('-',''), 'DTEND;VALUE=DATE:'+e.strftime('%Y%m%d'),
             'SUMMARY:'+icsx(d['name']), 'LOCATION:'+icsx(d['town']+', '+d['state']), 'DESCRIPTION:'+icsx((d.get('what') or '')+' Check the dates and times on the event’s own website before you go. More: https://projectscroll.com/seasons/#'+slug(d['name']))]
    if d.get('url'): lines.append('URL:'+d['url'])
    ev.append('\r\n'.join(lines+['END:VEVENT']))
ics = '\r\n'.join(['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Project Scroll//Seasons and festivals of the valley//EN','CALSCALE:GREGORIAN','METHOD:PUBLISH','X-WR-CALNAME:Seasons & festivals of the St. Joseph River valley','X-WR-CALDESC:Fairs, festivals and harvests from projectscroll.com/seasons/','REFRESH-INTERVAL;VALUE=DURATION:P1W','X-PUBLISHED-TTL:P1W']+ev+['END:VCALENDAR'])+'\r\n'
pathlib.Path(pathlib.Path(__file__).parent.parent/'seasons').mkdir(exist_ok=True)
open(pathlib.Path(__file__).parent.parent/'seasons'/'valley.ics','w',newline='').write(ics)
nev = len(ev)
JS = r'''<script>
(function(){ "use strict";
  var $=function(s){ return document.querySelector(s); }, $$=function(s){ return [].slice.call(document.querySelectorAll(s)); };
  var items=$$('.se'), secs=$$('.se-s'), q=$('#seQ'), cs=$('#seC'), mbs=$$('.se-mb'), cnt=$('#seCount'), mon=0;
  var now=new Date(), m0=now.getMonth()+1, MON=['','January','February','March','April','May','June','July','August','September','October','November','December'];
  /* the season we are in comes first */
  var cur=secs.filter(function(s){ return s.dataset.ms.split(',').map(Number).indexOf(m0)>=0; })[0];
  if (cur){ cur.classList.add('now'); cur.querySelector('h2').insertAdjacentHTML('beforeend',' <span class="se-now">now</span>'); cur.parentNode.insertBefore(cur, secs[0]); }
  var fmt=function(s){ var d=new Date(s+'T12:00:00'); return d.toLocaleDateString('en-US',{weekday:'short', month:'short', day:'numeric', year:'numeric'}); };
  items.forEach(function(li){ var s=li.dataset.start, e=li.dataset.end; if (!s) return; var t=li.querySelector('.se-d');
    var past=new Date((e||s)+'T23:59:00')<now, on=!past && new Date(s+'T00:00:00')<=now; t.textContent=' · '+fmt(s)+(e && e!==s? ' to '+fmt(e) : '')+(past? ' (this year’s has passed)' : on? ' (on now)' : ''); if (on) li.classList.add('soon');
    if (!past && (new Date(s+'T00:00:00')-now)/864e5<=31){ li.classList.add('soon'); } });
  var wk=false, wb=$('#seWk'), sat=new Date(now); sat.setHours(0,0,0,0); var dw=sat.getDay(); if (dw!==6 && dw!==0) sat.setDate(sat.getDate()+(6-dw)); else if (dw===0) sat.setDate(sat.getDate()-1);
  var sun=new Date(sat); sun.setDate(sat.getDate()+1); sun.setHours(23,59,0,0);
  var onWk=function(li){ if (!li.dataset.start) return false; var a=new Date(li.dataset.start+'T00:00:00'), b=new Date((li.dataset.end||li.dataset.start)+'T23:59:00'); return a<=sun && b>=sat; };
  var draw=function(){ var w=q.value.trim().toLowerCase().split(/\s+/).filter(Boolean), c=cs.value, n=0;
    items.forEach(function(li){ var ok=(!wk || onWk(li)) && (!mon || +li.dataset.m===mon) && (!c || li.dataset.c===c) && w.every(function(x){ return li.dataset.t.indexOf(x)>=0; }); li.hidden=!ok; if (ok) n++; });
    secs.forEach(function(s){ s.hidden=!s.querySelector('.se:not([hidden])'); });
    cnt.textContent=n===items.length? n+' events' : n+' of '+items.length+' events'; };
  mbs.forEach(function(b){ if (+b.dataset.m===m0) b.classList.add('cur'); b.addEventListener('click',function(){ var on=b.getAttribute('aria-pressed')!=='true'; mbs.forEach(function(x){ x.setAttribute('aria-pressed','false'); }); b.setAttribute('aria-pressed',String(on)); mon=on? +b.dataset.m : 0; draw(); }); });
  q.addEventListener('input',draw); cs.addEventListener('change',draw);
  wb.addEventListener('click',function(){ wk=!wk; wb.setAttribute('aria-pressed',String(wk)); if (wk){ mon=0; mbs.forEach(function(x){ x.setAttribute('aria-pressed','false'); }); } draw(); if (wk && !items.some(function(li){ return !li.hidden; })) cnt.textContent='Nothing with set dates this weekend. Try the month.'; });
  /* coming up: the next few with known dates */
  var up=items.filter(function(li){ return li.dataset.start && new Date((li.dataset.end||li.dataset.start)+'T23:59:00')>=now; }).sort(function(a,b){ return a.dataset.start<b.dataset.start?-1:1; }).slice(0,4);
  var ul=$('#seUp'); if (up.length){ up.forEach(function(li){ var r=document.createElement('li'), a=document.createElement('a'); a.href='#'+li.id; a.textContent=li.dataset.n; r.appendChild(a); var s=document.createElement('span'); var on=new Date(li.dataset.start+'T00:00:00')<=now; s.textContent=' · '+li.dataset.town+' · '+(on? 'on now, until '+fmt(li.dataset.end) : fmt(li.dataset.start)); r.appendChild(s); ul.appendChild(r); }); $('#seUpW').hidden=false; }
  /* this weekend: Friday to Sunday, or the rest of it if today is a weekend day */
  (function(){ var t=new Date(); t.setHours(0,0,0,0); var d=t.getDay(), f=new Date(t);
    if (d>=1 && d<=4) f.setDate(t.getDate()+(5-d)); var su=new Date(t); su.setDate(t.getDate()+((7-d)%7)); if (d>=1 && d<=4) su=new Date(f.getTime()+2*864e5);
    var hits=$$('.se[data-start]').filter(function(li){ var s=new Date(li.dataset.start+'T00:00:00'), e=new Date(li.dataset.end+'T00:00:00'); return s<=su && e>=(d===0||d>=5? t : f); });
    var wk=$('#seWk'); hits.forEach(function(li){ var r=document.createElement('li'), a=document.createElement('a'); a.href='#'+li.id; a.textContent=li.dataset.n; r.appendChild(a); var s=document.createElement('span'); s.textContent=' · '+li.dataset.town; r.appendChild(s); wk.appendChild(r); });
    var o={weekday:'short',month:'short',day:'numeric'}; $('#seWkH').textContent='This weekend in the valley · '+(d===0||d>=5? t : f).toLocaleDateString('en-US',o)+' to '+su.toLocaleDateString('en-US',o);
    if (!hits.length){ var nx=$$('.se[data-start]').filter(function(li){ return new Date(li.dataset.start+'T00:00:00')>su; }).sort(function(a,b){ return a.dataset.start<b.dataset.start?-1:1; })[0];
      $('#seWkN').innerHTML=''; var p=$('#seWkN'); p.textContent='Nothing on our calendar this weekend. '; if (nx){ var a=document.createElement('a'); a.href='#'+nx.id; a.textContent=nx.dataset.n; p.appendChild(document.createTextNode('Next: ')); p.appendChild(a); p.appendChild(document.createTextNode(', '+nx.dataset.town+', '+new Date(nx.dataset.start+'T00:00:00').toLocaleDateString('en-US',{month:'long',day:'numeric'})+'. The museums are open most weekends: ')); var m=document.createElement('a'); m.href='/museums/'; m.textContent='see what is open'; p.appendChild(m); p.appendChild(document.createTextNode('.')); } }
    $('#seWkW').hidden=false; })();
  /* add to calendar: a small .ics file made on this device */
  var pad=function(n){ return ('0'+n).slice(-2); };
  $$('.se-cal').forEach(function(b){ b.addEventListener('click',function(){ var li=b.closest('.se'), s=li.dataset.start.replace(/-/g,''), e=new Date(li.dataset.end+'T12:00:00'); e.setDate(e.getDate()+1);
    var ee=e.getFullYear()+pad(e.getMonth()+1)+pad(e.getDate()), st=new Date(), stamp=st.getUTCFullYear()+pad(st.getUTCMonth()+1)+pad(st.getUTCDate())+'T'+pad(st.getUTCHours())+pad(st.getUTCMinutes())+'00Z';
    var esc=function(t){ return t.replace(/[\\,;]/g,function(m){ return '\\'+m; }).replace(/\n/g,'\\n'); };
    var ics=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Project Scroll//Seasons//EN','BEGIN:VEVENT','UID:'+li.id+'-'+s+'@projectscroll.com','DTSTAMP:'+stamp,'DTSTART;VALUE=DATE:'+s,'DTEND;VALUE=DATE:'+ee,'SUMMARY:'+esc(li.dataset.n),'LOCATION:'+esc(li.dataset.town),'DESCRIPTION:'+esc('Check the dates and times on the event’s own website before you go. '+(li.dataset.u||'')),(li.dataset.u?'URL:'+li.dataset.u:''),'END:VEVENT','END:VCALENDAR'].filter(Boolean).join('\r\n');
    var a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([ics],{type:'text/calendar'})); a.download=li.id+'.ics'; document.body.appendChild(a); a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); },500); }); });
  /* the twelve-month calendar, drawn on this device from the events above */
  var grid=$('#scGrid'), smsg=$('#scMsg'), day=null, DN=['S','M','T','W','T','F','S'];
  var ymd=function(d){ return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2); };
  var byDay={}; items.forEach(function(li){ if (!li.dataset.start) return; var a=new Date(li.dataset.start+'T12:00:00'), b=new Date((li.dataset.end||li.dataset.start)+'T12:00:00');
    for (var d=new Date(a), k=0; d<=b && k<400; d.setDate(d.getDate()+1), k++){ var key=ymd(d); (byDay[key]=byDay[key]||[]).push(li); } });
  var tkey=ymd(now);
  for (var i=0;i<12;i++){ var first=new Date(now.getFullYear(), now.getMonth()+i, 1), m=first.getMonth()+1, y=first.getFullYear();
    var box=document.createElement('div'); box.className='sc-m';
    var hb=document.createElement('button'); hb.type='button'; hb.className='sc-mh'; hb.textContent=MON[m]+' '+y; hb.dataset.m=m;
    var usual=items.filter(function(li){ return +li.dataset.m===m; }).length; hb.setAttribute('aria-label',MON[m]+' '+y+': '+usual+' events usually this month');
    hb.addEventListener('click',(function(mm){ return function(){ day=null; mon=mm; mbs.forEach(function(x){ x.setAttribute('aria-pressed',String(+x.dataset.m===mm)); }); draw(); smsg.textContent='Showing the events usually held in '+MON[mm]+'.'; $('#'+(secs.filter(function(s){ return !s.hidden; })[0]||{id:'seCal'}).id).scrollIntoView({behavior:'smooth', block:'start'}); }; })(m));
    box.appendChild(hb);
    var t=document.createElement('div'); t.className='sc-d'; t.setAttribute('role','group'); t.setAttribute('aria-label',MON[m]+' '+y);
    DN.forEach(function(n){ var e=document.createElement('span'); e.className='sc-dn'; e.textContent=n; e.setAttribute('aria-hidden','true'); t.appendChild(e); });
    for (var b=0;b<first.getDay();b++){ var e=document.createElement('span'); e.className='sc-x'; t.appendChild(e); }
    var last=new Date(y, m, 0).getDate();
    for (var dd=1; dd<=last; dd++){ var key=y+'-'+('0'+m).slice(-2)+'-'+('0'+dd).slice(-2), evs=byDay[key]||[], c;
      if (evs.length){ c=document.createElement('button'); c.type='button'; c.className='sc-on'; c.setAttribute('aria-label',MON[m]+' '+dd+': '+evs.map(function(li){ return li.dataset.n; }).join(', '));
        c.title=evs.map(function(li){ return li.dataset.n; }).join('\n');
        c.addEventListener('click',(function(k,list){ return function(){ day=k; mon=0; mbs.forEach(function(x){ x.setAttribute('aria-pressed','false'); }); items.forEach(function(li){ li.hidden=list.indexOf(li)<0; }); secs.forEach(function(s){ s.hidden=!s.querySelector('.se:not([hidden])'); });
          cnt.textContent=list.length+' of '+items.length+' events'; smsg.textContent=fmt(k)+': '+list.map(function(li){ return li.dataset.n; }).join(' · ')+'.'; list[0].scrollIntoView({behavior:'smooth', block:'center'}); }; })(key, evs)); }
      else { c=document.createElement('span'); }
      c.textContent=dd; if (key===tkey) c.classList.add('sc-today'); if (key<tkey) c.classList.add('sc-past'); t.appendChild(c); }
    box.appendChild(t); grid.appendChild(box); }
  /* a festival stamp: only on the days of the event, and only in or near its town */
  var est={}; try{ est=JSON.parse(localStorage.getItem('ps-fest-stamp')||'{}')||{}; }catch(e){}
  var km=function(a,b){ var R=6371, r=Math.PI/180, dl=(b[0]-a[0])*r, dn=(b[1]-a[1])*r, h=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a[0]*r)*Math.cos(b[0]*r)*Math.sin(dn/2)*Math.sin(dn/2); return 2*R*Math.asin(Math.sqrt(h)); };
  items.forEach(function(li){ var b=li.querySelector('.se-sb'), m=li.querySelector('.mu-msg'); if (!b) return;
    var open=new Date(li.dataset.start+'T00:00:00')<=now && new Date((li.dataset.end||li.dataset.start)+'T23:59:00')>=now;
    var set=function(){ var k=li.id+'-'+li.dataset.start.slice(0,4); b.hidden=!navigator.geolocation || (!open && !est[k]); b.disabled=!!est[k]; b.textContent=est[k]? 'Stamped ✓ '+est[k] : 'I’m here: stamp it'; }; set();
    b.addEventListener('click',function(){ m.textContent='Checking where you are…';
      navigator.geolocation.getCurrentPosition(function(p){ var d=km([p.coords.latitude,p.coords.longitude], li.dataset.ll.split(',').map(Number));
        if (d<=10){ est[li.id+'-'+li.dataset.start.slice(0,4)]=new Date().toISOString().slice(0,10); try{ localStorage.setItem('ps-fest-stamp',JSON.stringify(est)); }catch(e){} set(); m.innerHTML='Stamped. It is in your <a href="/passport/">passport</a>, on this device only.'; if (window.psEarn) window.psEarn('stamp'); if (window.psStampCheck) window.psStampCheck(); }
        else m.textContent='You look to be about '+Math.round(d*.621371)+' mi from '+li.dataset.town+'. The stamp works at the festival.'; },
        function(){ m.textContent='No location shared, so nothing changed.'; }, {enableHighAccuracy:false, timeout:20000, maximumAge:60000}); }); });
  draw();
  var h=location.hash.slice(1); if (h){ var t=document.getElementById(h); if (t && t.classList.contains('se')){ t.classList.add('flash'); } }
})();
</script>'''
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Seasons &amp; festivals</p>
    <figure class="pg-art"><picture><source type="image/avif" srcset="/img/card-seasons-art-270.avif 270w, /img/card-seasons-art.avif 540w" sizes="8rem"><img class="vt-seasons" src="/img/card-seasons-art-270.webp" srcset="/img/card-seasons-art-270.webp 270w, /img/card-seasons-art.webp 540w" sizes="8rem" width="540" height="960" alt="" decoding="async"></picture></figure>
    <h1>When to come, and why to come back</h1>
    <p class="lede" style="font-size:1.15rem">Here are {n} fairs, festivals, harvests, living-history days and holiday walks across the St. Joseph River valley, season by season. Most have run for decades; a few for more than a century. The season we are in comes first.</p>
    <div class="se-up se-wk" id="seWkW" hidden><p class="mu-jl" id="seWkH">This weekend in the valley</p><ul id="seWk"></ul><p class="se-wkn" id="seWkN"></p></div>
    <div class="se-up" id="seUpW" hidden><p class="mu-jl">Coming up</p><ul id="seUp"></ul></div>
    <div class="mu-bar">
      <label class="nm-q"><span>Find an event</span><input type="search" id="seQ" placeholder="A town, a fair, a fruit…" autocomplete="off" spellcheck="false"></label>
      <div class="nm-chips se-mbs" role="group" aria-label="Show one month">{months}</div>
      <div class="nm-chips"><button type="button" class="btn" id="seWk" aria-pressed="false">This weekend</button><label class="mu-ol"><span class="vh">County</span><select id="seC"><option value="">Every county</option>{copts}</select></label></div>
      <p class="nm-count" id="seCount" aria-live="polite">{n} events</p>
    </div>
    <section class="sc" id="seCal" aria-labelledby="scH"><h2 id="scH">The year ahead</h2>
      <p class="sc-k">Twelve months from this one. Gold days have an event with set dates; press a day or a month to see its events. <span class="sc-key"><i class="sc-on"></i> event day <i class="sc-today"></i> today</span></p>
      <div class="sc-grid" id="scGrid"></div>
      <p class="mu-nmsg" id="scMsg" aria-live="polite"></p></section>
{secs}
    <h2>Keep the calendar</h2>
    <p>All {nev} events with set dates, in one calendar file. <a class="btn" href="webcal://projectscroll.com/seasons/valley.ics">Subscribe in your calendar</a> <a class="btn" href="/seasons/valley.ics" download>Download the file</a></p>
    <p class="note">Subscribing keeps the dates up to date as we add the next year’s; your calendar app checks the file about once a week. It holds only the event dates, nothing about you.</p>
    <h2>Before you go</h2>
    <ul class="dis">
      <li><b>Check the dates.</b> Most events keep the same weekend each year, but the exact days are set by the organisers. Their own website has the latest.</li>
      <li><b>Make a weekend of it.</b> Pair an event with the <a href="/museums/">museums</a> nearby and somewhere to <a href="/food/">eat and stay</a>.</li>
      <li><b>Know of one we missed?</b> <a href="/#contact">Tell us</a>, with its website.</li>
    </ul>
    <p class="note">Every event here was checked against its own website, or a city, county or tourism page, in October 2026. Events marked “check the dates” had not yet posted their next dates. “Add to my calendar” makes a calendar file on your device; nothing is sent anywhere.</p>
{ld}
{JS}
'''
body += """<script>
(function(){ var day=[]; try{ day=JSON.parse(localStorage.getItem('ps-day')||'[]')||[]; }catch(e){}
  var bs=[].slice.call(document.querySelectorAll('.fd-add'));
  var paint=function(){ bs.forEach(function(b){ var on=day.indexOf(b.dataset.i)>=0; b.setAttribute('aria-pressed',String(on)); b.textContent=on?'On my day ✓':'Add to my day'; }); };
  bs.forEach(function(b){ b.addEventListener('click',function(){ var i=day.indexOf(b.dataset.i); if (i>=0) day.splice(i,1); else day.push(b.dataset.i); try{ localStorage.setItem('ps-day',JSON.stringify(day)); }catch(e){} paint(); }); });
  paint(); })();
</script>
"""

page('seasons/index.html', 'Seasons & festivals of the valley · Project Scroll',
     f'{n} fairs, festivals, harvests, living-history days and holiday walks across the St. Joseph River valley in Michigan and Indiana, season by season, each checked against its own website.',
     body, og='https://projectscroll.com/og/records.jpg')
print('seasons built', n)
