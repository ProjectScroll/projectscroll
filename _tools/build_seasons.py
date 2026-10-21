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
    return f'''<li class="se" id="{slug(d['name'])}" data-m="{d['month']}" data-c="{E(d['county'])}"{exact} data-n="{E(d['name'])}" data-town="{E(d['town'])}" data-u="{E(d.get('url') or '')}" data-t="{E((d['name']+' '+d['town']+' '+d['county']+' '+d.get('what','')).lower())}">
        <p class="mu-k">{E(MON[d['month']])} · {E(d['town'])}, {E(d['state'])}{chk}</p>
        <h3>{E(d['name'])}</h3>
        <p class="se-w"><b>{when}</b><span class="se-d"></span></p>
        <p>{E(d.get('what',''))}</p>{hist}
        <p class="mu-acts">{link}{' · '+cal if cal else ''}</p>
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
    var past=new Date((e||s)+'T23:59:00')<now; t.textContent=' · '+fmt(s)+(e && e!==s? ' to '+fmt(e) : '')+(past? ' (this year’s has passed)' : '');
    if (!past && (new Date(s+'T00:00:00')-now)/864e5<=31){ li.classList.add('soon'); } });
  var draw=function(){ var w=q.value.trim().toLowerCase().split(/\s+/).filter(Boolean), c=cs.value, n=0;
    items.forEach(function(li){ var ok=(!mon || +li.dataset.m===mon) && (!c || li.dataset.c===c) && w.every(function(x){ return li.dataset.t.indexOf(x)>=0; }); li.hidden=!ok; if (ok) n++; });
    secs.forEach(function(s){ s.hidden=!s.querySelector('.se:not([hidden])'); });
    cnt.textContent=n===items.length? n+' events' : n+' of '+items.length+' events'; };
  mbs.forEach(function(b){ if (+b.dataset.m===m0) b.classList.add('cur'); b.addEventListener('click',function(){ var on=b.getAttribute('aria-pressed')!=='true'; mbs.forEach(function(x){ x.setAttribute('aria-pressed','false'); }); b.setAttribute('aria-pressed',String(on)); mon=on? +b.dataset.m : 0; draw(); }); });
  q.addEventListener('input',draw); cs.addEventListener('change',draw);
  /* coming up: the next few with known dates */
  var up=items.filter(function(li){ return li.dataset.start && new Date((li.dataset.end||li.dataset.start)+'T23:59:00')>=now; }).sort(function(a,b){ return a.dataset.start<b.dataset.start?-1:1; }).slice(0,4);
  var ul=$('#seUp'); if (up.length){ up.forEach(function(li){ var r=document.createElement('li'), a=document.createElement('a'); a.href='#'+li.id; a.textContent=li.dataset.n; r.appendChild(a); var s=document.createElement('span'); s.textContent=' · '+li.dataset.town+' · '+fmt(li.dataset.start); r.appendChild(s); ul.appendChild(r); }); $('#seUpW').hidden=false; }
  /* add to calendar: a small .ics file made on this device */
  var pad=function(n){ return ('0'+n).slice(-2); };
  $$('.se-cal').forEach(function(b){ b.addEventListener('click',function(){ var li=b.closest('.se'), s=li.dataset.start.replace(/-/g,''), e=new Date(li.dataset.end+'T12:00:00'); e.setDate(e.getDate()+1);
    var ee=e.getFullYear()+pad(e.getMonth()+1)+pad(e.getDate()), st=new Date(), stamp=st.getUTCFullYear()+pad(st.getUTCMonth()+1)+pad(st.getUTCDate())+'T'+pad(st.getUTCHours())+pad(st.getUTCMinutes())+'00Z';
    var esc=function(t){ return t.replace(/[\\,;]/g,function(m){ return '\\'+m; }).replace(/\n/g,'\\n'); };
    var ics=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Project Scroll//Seasons//EN','BEGIN:VEVENT','UID:'+li.id+'-'+s+'@projectscroll.com','DTSTAMP:'+stamp,'DTSTART;VALUE=DATE:'+s,'DTEND;VALUE=DATE:'+ee,'SUMMARY:'+esc(li.dataset.n),'LOCATION:'+esc(li.dataset.town),'DESCRIPTION:'+esc('Check the dates and times on the event’s own website before you go. '+(li.dataset.u||'')),(li.dataset.u?'URL:'+li.dataset.u:''),'END:VEVENT','END:VCALENDAR'].filter(Boolean).join('\r\n');
    var a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([ics],{type:'text/calendar'})); a.download=li.id+'.ics'; document.body.appendChild(a); a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); },500); }); });
  draw();
  var h=location.hash.slice(1); if (h){ var t=document.getElementById(h); if (t && t.classList.contains('se')){ t.classList.add('flash'); } }
})();
</script>'''
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Seasons &amp; festivals</p>
    <h1>When to come, and why to come back</h1>
    <p class="lede" style="font-size:1.15rem">{n} fairs, festivals, harvests, living-history days and holiday walks across the St. Joseph River valley, season by season. Most have run for decades; a few for more than a century. The season we are in comes first.</p>
    <div class="se-up" id="seUpW" hidden><p class="mu-jl">Coming up</p><ul id="seUp"></ul></div>
    <div class="mu-bar">
      <label class="nm-q"><span>Find an event</span><input type="search" id="seQ" placeholder="A town, a fair, a fruit…" autocomplete="off" spellcheck="false"></label>
      <div class="nm-chips se-mbs" role="group" aria-label="Show one month">{months}</div>
      <div class="nm-chips"><label class="mu-ol"><span class="vh">County</span><select id="seC"><option value="">Every county</option>{copts}</select></label></div>
      <p class="nm-count" id="seCount" aria-live="polite">{n} events</p>
    </div>
{secs}
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
page('seasons/index.html', 'Seasons & festivals of the valley · Project Scroll',
     f'{n} fairs, festivals, harvests, living-history days and holiday walks across the St. Joseph River valley in Michigan and Indiana, season by season, each checked against its own website.',
     body, og='https://projectscroll.com/og/records.jpg')
print('seasons built', n)
