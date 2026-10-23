"""Legends and lore of the valley: the stories the valley tells, each tested against the earliest record.
python3 _tools/build_lore.py   (data in _tools/data/lore.json)

Each item: id, title, town, county, state, told (as told today, html-safe text), told_src [title,url],
record (what the earliest sources say), verdict (True / Partly true / No record / False / Open), verdict_note,
sources [[citation,url],...], img, alt, cap (optional picture), new (bool), new_note, quiz {claim, answer: true|false|none, note}."""
import sys, json, pathlib, html, re
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
R = pathlib.Path(__file__).resolve().parent.parent
E = lambda s: html.escape(str(s), quote=True)
L = [x for x in json.load(open(R/'_tools/data/lore.json')) if x.get('keep', True)]
VC = {'True':'t', 'Partly true':'p', 'No record':'n', 'False':'f', 'Open':'o'}
from PIL import Image as _I
def wh(src):
    try:
        with _I.open(R/src.lstrip('/')) as im: return f' width="{im.size[0]}" height="{im.size[1]}"'
    except Exception: return ''
def item(x):
    v = x['verdict']; vc = VC.get(v, 'o')
    pic = ''
    if x.get('img'):
        pic = (f'<figure class="lo-pic"><a class="nw-pz" href="{E(x["img"])}"><img src="{E(x["img"])}"{wh(x["img"])} alt="{E(x.get("alt",""))}" loading="lazy" decoding="async"></a>'
               f'<figcaption>{x.get("cap","")}</figcaption></figure>')
    told_src = f' <span class="lo-ts">(as told by <a href="{E(x["told_src"][1])}" rel="noopener">{E(x["told_src"][0])}</a>)</span>' if x.get('told_src') else ''
    src = ''.join(f'<li>{"<a href=" + chr(34) + E(u) + chr(34) + " rel=" + chr(34) + "noopener" + chr(34) + ">" + c + "</a>" if u else c}</li>' for c, u in x.get('sources', []))
    new = f'<p class="lo-new"><span class="nw-tier n">New finding</span> {x["new_note"]}</p>' if x.get('new') and x.get('new_note') else ''
    return f'''<li class="lo" id="{E(x['id'])}" data-v="{vc}" data-tw="{E(x['town'])}" data-t="{E((x['title']+' '+x['town']+' '+x.get('county','')+' '+x['told']+' '+x['record']).lower())}">
      <p class="mu-k">{E(x['town'])}{(', '+E(x['county'])+' County') if x.get('county') else ''}{(', '+E(x['state'])) if x.get('state') else ''}</p>
      <h3>{E(x['title'])}</h3>
      {pic}
      <div class="lo-told"><p class="lo-h">The story</p><p>{x['told']}{told_src}</p></div>
      <div class="lo-rec"><p class="lo-h">What the record says</p><p>{x['record']}</p></div>
      <p class="lo-v lo-{vc}"><b>{E(v)}.</b> {x.get('verdict_note','')}</p>
      {new}
      <details class="lo-s"><summary>Sources</summary><ul>{src}</ul></details>
    </li>'''
items = ''.join(item(x) for x in L)
QZ = [x for x in L if x.get('quiz')]
quiz = ''.join(f'<div class="nw-myth" data-a="{x["quiz"]["answer"]}"><p class="nw-myth-c">“{E(x["quiz"]["claim"])}”</p><div class="nw-myth-ans"><p class="nw-myth-v">{E({"true":"True","false":"False","none":"No record"}[x["quiz"]["answer"]])}</p><p>{x["quiz"].get("note","")} <a href="#{E(x["id"])}">Read it ›</a></p></div></div>' for x in QZ[:10])
towns = sorted({x['town'] for x in L})
topt = ''.join(f'<option value="{E(t)}">{E(t)}</option>' for t in towns)
counts = {k: sum(1 for x in L if x['verdict'] == k) for k in VC}
vchips = '<button type="button" class="btn lo-f" data-v="" aria-pressed="true">Every verdict</button>' + ''.join(f'<button type="button" class="btn lo-f" data-v="{VC[k]}" aria-pressed="false">{E(k)} ({n})</button>' for k, n in counts.items() if n)
JS = r'''<script>
(function(){ "use strict";
  var $=function(s){ return document.querySelector(s); }, $$=function(s){ return [].slice.call(document.querySelectorAll(s)); };
  var li=$$('.lo'), q=$('#loQ'), tw=$('#loT'), fs=$$('.lo-f'), v='', cnt=$('#loCount');
  var draw=function(){ var w=q.value.trim().toLowerCase().split(/\s+/).filter(Boolean), t=tw.value, n=0;
    li.forEach(function(x){ var ok=(!v||x.dataset.v===v) && (!t||x.dataset.tw===t) && w.every(function(k){ return x.dataset.t.indexOf(k)>=0; }); x.hidden=!ok; if (ok) n++; });
    cnt.textContent=n===li.length? n+' stories' : n+' of '+li.length+' stories'; $('#loNone').hidden=n>0; };
  q.addEventListener('input',draw); tw.addEventListener('change',draw);
  fs.forEach(function(b){ b.addEventListener('click',function(){ v=b.dataset.v; fs.forEach(function(x){ x.setAttribute('aria-pressed',String(x===b)); }); draw(); }); });
  draw();
})();
</script>'''
ld = '<script type="application/ld+json">' + json.dumps({'@context':'https://schema.org','@type':'ItemList','name':'Legends and lore of the St. Joseph River valley','itemListElement':[{'@type':'ListItem','position':i+1,'name':x['title'],'url':'https://projectscroll.com/lore/#'+x['id']} for i,x in enumerate(L)]}, ensure_ascii=False) + '</script>'
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Legends and lore</p>
    <h1>Story or record? The legends of the valley</h1>
    <p class="lede" style="font-size:1.15rem">Every valley has its stories: gold in a well, a ghost on the stairs, a fort that flew four flags. Some are true, some grew in the telling, and some have no record at all. Here are {len(L)} of the St. Joseph River valley’s, each traced back to the earliest page we could find, with our verdict.</p>
    <div class="nw-brethren"><p class="nw-br-h">How to read this page</p><p>Each story is told the way it is told today, then set against what the oldest records actually say. The verdict is <b>True</b>, <b>Partly true</b>, <b>False</b>, <b>No record</b> (nothing written down that we can find, which is not the same as false) or <b>Open</b> (the record is not yet clear). A <span class="nw-tier n">New finding</span> is a detail from the record that we could not find in any modern telling. Every source is listed with its story.</p></div>
    <h2>Story or record? Play along</h2>
    <p>Make your call on each one: true, false, or no record either way. Then see what the paper shows.</p>
    <div class="nw-myths" data-quiz data-msgs="You read the record like an old editor.|A good eye for a source.|Read on: the record has surprises.">{quiz}</div>
    <h2>The stories</h2>
    <div class="mu-bar">
      <label class="nm-q"><span>Find a story</span><input type="search" id="loQ" placeholder="A town, a word, a name" autocomplete="off" spellcheck="false"></label>
      <div class="nm-chips" role="group" aria-label="Show one verdict">{vchips}</div>
      <label class="rc-pl"><span>Town</span><select id="loT"><option value="">Every town</option>{topt}</select></label>
      <p class="nm-count" id="loCount" aria-live="polite">{len(L)} stories</p>
    </div>
    <ul class="lo-list">{items}</ul>
    <p class="rc-none" id="loNone" hidden>No story matches. Try another word or town.</p>
    <h2>Know a story we should test?</h2>
    <p>Every town has one we have not heard. <a href="mailto:research@projectscroll.com?subject=A%20valley%20legend">Write to us</a> with the story as you heard it and where, and we will go looking for the record.</p>
    <p class="vs-plan"><a class="btn" href="/lost-towns/">Lost towns of the valley</a> <a class="btn" href="/place-names/">How the towns got their names</a> <a class="btn" href="/legends/">Test a family legend</a></p>
{ld}
{JS}
'''
page('lore/index.html', 'Legends and lore of the valley · Project Scroll',
     f'{len(L)} legends, tall tales and ghost stories of the St. Joseph River valley, each tested against the earliest record: true, partly true, false or no record.',
     body)
print('lore built', len(L))
