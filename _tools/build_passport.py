"""The passport: every stamp a visitor has earned on this device (museums, the walks, tables, festivals), the milestones,
the season's trail, and a certificate to print. python3 _tools/build_passport.py"""
import sys, pathlib, json, re
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
P = pathlib.Path(__file__).parent/'data'
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
names = {}
used = set()
for d in json.load(open(P/'museums.json')):
    s = slug(d['name']); s = slug(d['name']+' '+d['town']) if s in used else s; used.add(s)
    names['ps-mu-stamp|'+s] = [d['name'], d['town'].split(' (')[0], '/museums/#'+s]
for f, key, url in (('walk.json','ps-walk-stamp','/walk/'), ('walk-dowagiac.json','ps-walk-dowagiac-stamp','/walk/dowagiac/')):
    for st in json.load(open(P/f))['stops']:
        names[key+'|'+st['id']] = [st['name'], 'Cassopolis' if key=='ps-walk-stamp' else 'Dowagiac', url+'#'+st['id']]
used = set()
for d in json.load(open(P/'food.json')):
    s = slug(d['name']+' '+d['town']) if slug(d['name']) in used else slug(d['name']); used.add(s)
    names['ps-food-stamp|'+s] = [d['name'], d['town'], '/food/#'+s]
for d in json.load(open(P/'seasons.json')):
    names['ps-fest|'+slug(d['name'])] = [d['name'], d['town'], '/seasons/#'+slug(d['name'])]
N = json.dumps(names, ensure_ascii=False, separators=(',',':')).replace('</','<\\/')

JS = r'''<script>
document.addEventListener('DOMContentLoaded', function(){ "use strict";
  var NAMES=__NAMES__, $=function(s){ return document.querySelector(s); };
  var KIND={museum:'Museums & sites', walk:'Walk stops', table:'Tables & inns', festival:'Festivals'};
  var all=(window.psStamps? window.psStamps() : []).map(function(s){ var k=s.key+'|'+s.id;
    if (s.key==='ps-fest-stamp'){ var base=s.id.replace(/-\d{4}$/,''); k='ps-fest|'+base; s.year=s.id.slice(-4); }
    var n=NAMES[k]||[s.id,'',''];
    return {name:n[0], town:n[1], href:n[2], date:s.date, kind:s.kind, year:s.year}; }).sort(function(a,b){ return a.date<b.date?-1:1; });
  var n=all.length;
  $('#ppN').textContent=n; $('#ppNone').hidden=n>0; $('#ppHave').hidden=n===0;
  var counts={}; all.forEach(function(s){ counts[s.kind]=(counts[s.kind]||0)+1; });
  $('#ppKinds').textContent=Object.keys(KIND).map(function(k){ return KIND[k]+': '+(counts[k]||0); }).join(' · ');
  /* milestones */
  var M=[10,25,50], next=M.filter(function(m){ return n<m; })[0];
  $('#ppBar').style.setProperty('--p', Math.min(100, Math.round(n/50*100))+'%'); $('#ppBar').setAttribute('aria-valuenow', String(n));
  M.forEach(function(m){ var el=document.querySelector('.pp-m[data-m="'+m+'"]'); if (el) el.classList.toggle('done', n>=m); });
  $('#ppNext').textContent=next? (next-n)+' more to '+next+' stamps.' : 'All three milestones reached. Remarkable.';
  /* the stamps */
  var ul=$('#ppList'); all.forEach(function(s,i){ var li=document.createElement('li'), a=document.createElement('a'); a.className='mu-stamp pp-'+s.kind; a.href=s.href||'#';
    var t=document.createElement('span'); t.textContent=s.town; var b=document.createElement('b'); b.textContent=s.name; var d=document.createElement('time'); d.textContent=s.date; var k=document.createElement('span'); k.className='pp-k'; k.textContent=({museum:'Museum',walk:'Walk',table:'Table',festival:'Festival'})[s.kind]||'';
    a.appendChild(k); a.appendChild(t); a.appendChild(b); a.appendChild(d); li.appendChild(a); ul.appendChild(li); });
  /* the fall trail */
  var has=function(k,id){ return all.some(function(s){ return s.href && s.href.indexOf(id)>=0; }); };
  [['bonneyville-mill','/museums/#bonneyville-mill'],['jollay-orchards','/food/#jollay-orchards'],['dowagiac-area-history-museum','/museums/#dowagiac-area-history-museum']].forEach(function(x){ var el=document.querySelector('.pp-trail [data-id="'+x[0]+'"]'); if (el && has(null,x[0])) el.classList.add('done'); });
  /* the certificate */
  var cn=$('#ppName'); try{ cn.value=localStorage.getItem('ps-pp-name')||''; }catch(e){}
  $('#ppCert').disabled=n<10; $('#ppCertMsg').textContent=n<10? 'The certificate opens at ten stamps.' : '';
  $('#ppCert').addEventListener('click',function(){ var nm=cn.value.trim(); try{ localStorage.setItem('ps-pp-name',nm); }catch(e){}
    $('#cfName').textContent=nm||'A seeker of the valley'; $('#cfN').textContent=n; $('#cfMile').textContent=n>=50?'Fifty stamps':n>=25?'Twenty-five stamps':'Ten stamps';
    $('#cfDate').textContent=new Date().toLocaleDateString('en-US',{year:'numeric', month:'long', day:'numeric'});
    $('#cfList').textContent=all.slice(0,60).map(function(s){ return s.name; }).join(' · ');
    document.documentElement.classList.add('pp-printing'); window.print(); });
  addEventListener('afterprint',function(){ document.documentElement.classList.remove('pp-printing'); });
  if (window.psStampCheck) window.psStampCheck();
});
</script>'''.replace('__NAMES__', N)

body = '''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Your passport</p>
    <h1>Every place you have stood</h1>
    <p class="lede" style="font-size:1.15rem">Press “I’m here” at a museum, a stop on a walk, a table or a festival, and its stamp lands here. Ten, twenty-five and fifty stamps each earn a badge, and the certificate is yours to print.</p>
    <section class="pp-sum" aria-labelledby="ppH"><h2 id="ppH"><span id="ppN">0</span> stamps</h2>
      <p class="pp-kinds" id="ppKinds"></p>
      <div class="pp-bar" id="ppBar" role="meter" aria-valuemin="0" aria-valuemax="50" aria-valuenow="0" aria-label="Stamps toward fifty"><span></span>
        <b class="pp-m" data-m="10" style="--at:20%">10</b><b class="pp-m" data-m="25" style="--at:50%">25</b><b class="pp-m" data-m="50" style="--at:100%">50</b></div>
      <p class="pp-next" id="ppNext"></p></section>
    <p id="ppNone" class="note">No stamps yet. Start with the <a href="/museums/">museums</a>, a <a href="/walk/">walk</a>, a <a href="/food/">table</a> or this season’s <a href="/seasons/">festivals</a>: each has an “I’m here” button that works when you are standing there.</p>
    <div id="ppHave" hidden><ol class="mu-stamps pp-list" id="ppList"></ol></div>
    <section class="pp-trail" aria-labelledby="ppTH"><h2 id="ppTH">This season’s trail: the harvest</h2>
      <p>Between September and November, stamp all three: the mill that grinds the grain, the orchard that has farmed the same ground since 1857, and the town where the stoves were made. All three in one fall earns the harvest badge.</p>
      <ol class="pp-tl"><li data-id="bonneyville-mill"><a href="/museums/#bonneyville-mill">Bonneyville Mill</a>, Bristol, Indiana</li><li data-id="jollay-orchards"><a href="/food/#jollay-orchards">Jollay Orchards</a>, Coloma, Michigan</li><li data-id="dowagiac-area-history-museum"><a href="/museums/#dowagiac-area-history-museum">Dowagiac Area History Museum</a>, Dowagiac, Michigan</li></ol>
      <p class="note">A new trail opens each season. Check the mill’s and the museum’s hours before you go.</p></section>
    <section aria-labelledby="ppPH"><h2 id="ppPH">A paper passport</h2>
      <p>Prefer paper? Print the passport booklet: a box for every museum, walk stop, table and festival the site counts, to fill with stamps, signatures or dates as you go. Print it double-sided, fold it, and take it with you.</p>
      <p><a class="btn" href="/passport/project-scroll-paper-passport.pdf" download>Download the paper passport (PDF)</a></p></section>
    <section aria-labelledby="ppCH"><h2 id="ppCH">Your certificate</h2>
      <p><label class="pp-nl">Name for the certificate <input id="ppName" type="text" maxlength="40" autocomplete="name" placeholder="As you would like it written"></label> <button type="button" class="btn primary" id="ppCert">Print my certificate</button> <span class="mu-nmsg" id="ppCertMsg"></span></p>
      <p class="note">The name stays on this device and is only printed. Nothing about your stamps leaves it either.</p></section>
    <div class="pp-cf" id="ppCf" aria-hidden="true"><div class="cf-in"><p class="cf-k">Project Scroll · The St. Joseph River Valley</p><p class="cf-t">Certificate of the Passport</p><p class="cf-p">This certifies that</p><p class="cf-n" id="cfName"></p><p class="cf-p">has stood in <b id="cfN"></b> places of the valley’s past and earned the mark of</p><p class="cf-m" id="cfMile"></p><p class="cf-l" id="cfList"></p><p class="cf-d">Given <span id="cfDate"></span> · Every clue is true. Every answer is in the record.</p></div></div>
''' + JS + '\n'
page('passport/index.html', 'Your passport · Project Scroll', 'Your passport of the St. Joseph River valley: every museum, walk stop, table and festival you have stamped by standing there, with milestones, a seasonal trail and a certificate to print.', body, og='https://projectscroll.com/og/records.jpg')
print('passport built', len(names))
