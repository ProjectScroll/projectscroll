"""Names on the old maps: the business directories beside the town plans, as one searchable roll.
python3 _tools/build_names.py"""
import sys, pathlib, json, html; sys.path.insert(0, str(pathlib.Path(__file__).parent)); sys.path.insert(0, str(pathlib.Path(__file__).parent/'data'))
from pages import page
from directories import DIRS
SEE={'cassopolis':'/map/cassopolis/','niles':'/map/niles/','dowagiac':'/map/dowagiac/','paw-paw':'/map/paw-paw/','goshen':'/map/#town-goshen'}
rows=[]
for k,d in DIRS.items():
    for hd,nm,nt in d['entries']:
        q=nm.endswith('?'); rows.append([k,hd,nm.rstrip('?'),nt,1 if q else 0])
towns=[[k,d['name'],d['year'],d['src'],SEE[k]] for k,d in DIRS.items()]
# the soldiers' roll joins the directories, so one search finds a man in either
SOL=json.load(open(pathlib.Path(__file__).parent/'data'/'soldiers_6mi_d.json'))
for x in SOL: rows.append(['co-d',x['rank'],x['name'],x['notes'],0])
towns.append(['co-d','Company D, Sixth Michigan Infantry','1861','Mathews, History of Cass County (1882), pp. 119–120','/soldiers/'])
ND=len(rows)-len(SOL)
n=len(rows)
chips=''.join(f'<button type="button" class="btn nm-t" data-t="{k}" aria-pressed="false">{html.escape(nm)}, {y}</button>' for k,nm,y,_,_ in towns)
body=f'''    <p class="crumb"><a href="/map/">← The map room</a></p>
    <p class="kicker">Names on the old maps</p>
    <h1>Who was in town</h1>
    <p class="lede" style="font-size:1.15rem">Beside each town plan, the mapmakers printed a business directory: the lawyers, doctors, merchants, smiths, hotel keepers and county officers who paid to be listed. Here are {ND} of those entries from {['','one','two','three','four','five','six','seven','eight','nine'][len(DIRS)]} towns, with the {len(SOL)} men of Company D, Sixth Michigan Infantry, raised at Dowagiac in 1861, as one roll you can search. Type a surname, a trade or a town.</p>
    <div class="nm-bar">
      <label class="nm-q"><span>Search the roll</span><input type="search" id="nmQ" placeholder="A surname, a trade or a town" autocomplete="off" spellcheck="false"></label>
      <div class="nm-chips" role="group" aria-label="Show one town"><button type="button" class="btn nm-t" data-t="" aria-pressed="true">All towns</button>{chips}</div>
      <p class="nm-count" id="nmCount" aria-live="polite">{n} entries</p>
    </div>
    <div id="nmOut" class="nm-out"></div>
    <noscript><p class="note">Turn on JavaScript to search the roll. Each town’s directory can also be read on its plan in the <a href="/map/">map room</a>.</p></noscript>
    <h2>How to read the roll</h2>
    <ul class="dis">
      <li><b>As printed.</b> Names are spelled as the engraver cut them, abbreviations and all: Jas. for James, Wm. for William, Chas. for Charles. A spelling that looks wrong may be the engraver’s, or it may be how the family spelled it then.</li>
      <li><b>A question mark</b> after a name means the engraving is worn or crowded and we are not sure of our reading. Look at the plan yourself and tell us what you see.</li>
      <li><b>Who is missing.</b> A directory is not a census. It lists people who paid to appear, so most farmers, labourers, women and children are not here. A handful of entries are also held back because they would give away an answer in the hunt.</li>
      <li><b>Every entry links to its map.</b> Open it and find the name in the directory beside the plan.</li>
    </ul>
    <p class="note">Found someone of your own? A directory line is a start: it puts a person in a town, in a trade, in a year. Deeds, censuses, newspapers and probate files can take the story further. <a href="/research/">We can help.</a></p>
    <p class="note">Sources: the business directories printed beside the town plans on the <i>Map of the Counties of Cass, Van Buren and Berrien, Michigan</i> (Philadelphia: Geil, Harley &amp; Siverd, 1860), Library of Congress; and on Geil &amp; Harley’s <i>Map of Elkhart Co. Indiana</i> (1861), American Geographical Society Library, University of Wisconsin–Milwaukee Libraries. Public domain. Transcribed for Project Scroll.</p>
    <script>
    (function(){{ "use strict";
      var T={json.dumps({k:[nm,y,src,see] for k,nm,y,src,see in towns},ensure_ascii=False)}, R={json.dumps(rows,ensure_ascii=False)};
      var q=document.getElementById('nmQ'), out=document.getElementById('nmOut'), cnt=document.getElementById('nmCount'), chips=[].slice.call(document.querySelectorAll('.nm-t')), town='';
      var norm=function(s){{ return (s||'').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9 ]+/g,' ').replace(/\\s+/g,' ').trim(); }};
      R.forEach(function(r){{ r.push(norm(r[2]+' '+r[3]+' '+r[1]+' '+T[r[0]][0])); }});
      var esc=function(s){{ var d=document.createElement('div'); d.textContent=s; return d.innerHTML; }};
      var draw=function(){{
        var words=norm(q.value).split(' ').filter(Boolean), hits=R.filter(function(r){{ return (!town||r[0]===town) && words.every(function(w){{ return r[5].indexOf(w)>=0; }}); }});
        cnt.textContent=hits.length===R.length?R.length+' entries':hits.length+' of '+R.length+' entries'+(hits.length?'':'. Try fewer letters, or another spelling: the engravers were not consistent.');
        var html='', last='', lastH='';
        hits.forEach(function(r){{
          if (r[0]!==last){{ if (last) html+='</ul>'; var t=T[r[0]]; html+='<h2 class="nm-town">'+esc(t[0])+', '+t[1]+' <a href="'+t[3]+'">'+(r[0]==='co-d'?'see the whole roll →':'see the directory on the map →')+'</a></h2><ul class="nm-list">'; last=r[0]; lastH=''; }}
          html+='<li><b>'+esc(r[2])+(r[4]?'<span class="nm-u" title="Our reading of a worn or crowded engraving">?</span>':'')+'</b>'+(r[3]?' <span class="nm-n">'+esc(r[3])+'</span>':'')+' <span class="nm-h">'+esc(r[1])+'</span></li>';
        }});
        out.innerHTML=html?html+'</ul>':'';
        try{{ var u=new URL(location.href); if (q.value.trim()) u.searchParams.set('q',q.value.trim()); else u.searchParams.delete('q'); if (town) u.searchParams.set('town',town); else u.searchParams.delete('town'); history.replaceState(null,'',u); }}catch(e){{}}
      }};
      var setTown=function(t){{ town=t; chips.forEach(function(c){{ c.setAttribute('aria-pressed',String(c.dataset.t===t)); }}); draw(); }};
      chips.forEach(function(c){{ c.addEventListener('click',function(){{ setTown(c.dataset.t); }}); }});
      q.addEventListener('input',draw);
      try{{ var p=new URLSearchParams(location.search); if (p.get('q')) q.value=p.get('q'); if (p.get('town') && T[p.get('town')]) town=p.get('town'); }}catch(e){{}}
      setTown(town);
    }})();
    </script>
'''
page('names/index.html','Who was in town · Names on the old maps · Project Scroll',f'{n} names from the business directories printed beside the 1860 and 1861 town plans of Cassopolis, Dowagiac, Niles, Paw Paw and Goshen, and the roll of Company D, Sixth Michigan Infantry, searchable by surname, trade or town.',body,og='https://projectscroll.com/og/map.jpg')
print('names roll built:',n,'entries')
