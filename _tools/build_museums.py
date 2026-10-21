"""Museums, historic places and research rooms of the valley: a directory by county.
python3 _tools/build_museums.py   (data in _tools/data/museums.json, every entry checked against its own website)"""
import sys, pathlib, json, html, re
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E = html.escape
D = json.load(open(pathlib.Path(__file__).parent/'data'/'museums.json'))
ORDER = [('Cass','MI'),('Berrien','MI'),('Van Buren','MI'),('St. Joseph','MI'),('Kalamazoo','MI'),('St. Joseph','IN'),('Elkhart','IN'),('LaGrange','IN'),('LaPorte','IN')]
KIND = {'museum':'Museum','historic house':'Historic house','historic site':'Historic site','historical society':'Society','library local history':'Library history room','library':'Library','archive':'Archive'}
SKIP = re.compile(r'(wikipedia|rootsweb|third-party|i could|not seen|see report|blocked|fetch|sbags|directory page|from the page|from a |per a |migenweb|official home page|community directory|not to be confused|county coverage|is in massachusetts)', re.I)
def when(n):
    parts = [p.strip() for p in re.split(r'(?<=[.;])\s+', n or '') if p.strip()]
    keep = [p for p in parts if not SKIP.search(p)]
    return ' '.join(keep)
def norm_county(d):
    c = d['county'].split(' (')[0]
    return (c if c != 'Regional' else 'Kalamazoo', d['state'])
groups = {}
for d in D: groups.setdefault(norm_county(d), []).append(d)
keys = [k for k in ORDER if k in groups] + [k for k in groups if k not in ORDER]
ST = {'MI':'Michigan','IN':'Indiana'}
def cid(k): return re.sub(r'[^a-z]+','-',(k[0]+'-'+k[1]).lower()).strip('-')
def card(d):
    w = d['hours'] if 'hours' in d else when(d.get('note'))
    url = d.get('url')
    link = f'<a class="mu-go" href="{E(url)}" rel="noopener">Their website ›</a>' if url else '<span class="mu-go">No website: check locally before you go</span>'
    chk = '' if d.get('verified') else '<span class="mu-chk" title="We could not confirm this one online. Check before you travel.">check before you go</span>'
    return f'''<li class="mu" data-k="{E(d['kind'])}" data-t="{E((d['name']+' '+d['town']+' '+d['what']+' '+d.get('research','')).lower())}">
        <p class="mu-k">{E(KIND.get(d['kind'], d['kind']))} · {E(d['town'])}{chk}</p>
        <h3>{E(d['name'])}</h3>
        <p>{E(d['what'])}</p>
        {f'<p class="mu-r"><b>For researchers:</b> {E(d["research"])}</p>' if d.get('research') else ''}
        {f'<p class="mu-w">{E(w)}</p>' if w else ''}
        <p class="mu-a">{E(d['address'])}</p>
        <p>{link}</p>
      </li>'''
sections = ''.join(f'''    <section class="mu-c" id="{cid(k)}"><h2>{E(k[0])} County, {ST[k[1]]}</h2>
      <ul class="mu-list">{''.join(card(d) for d in sorted(groups[k], key=lambda x:(x['town'], x['name'])))}</ul></section>
''' for k in keys)
chips = ''.join(f'<a class="btn mu-cj" href="#{cid(k)}">{E(k[0])}, {k[1]}</a>' for k in keys)
kinds = ''.join(f'<button type="button" class="btn mu-f" data-k="{k}" aria-pressed="false">{v}</button>' for k,v in KIND.items())
n = len(D)
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Museums &amp; historic places</p>
    <h1>Where the valley keeps its past</h1>
    <p class="lede" style="font-size:1.15rem">{n} museums, historic houses, libraries, research rooms and archives across the St. Joseph River valley and its neighbours, from the log cabin in Cassopolis to the Studebaker collection in South Bend. The hunt starts on this website. It finishes in places like these.</p>
    <div class="mu-bar">
      <label class="nm-q"><span>Find a place</span><input type="search" id="muQ" placeholder="A town, a museum or a subject" autocomplete="off" spellcheck="false"></label>
      <div class="nm-chips" role="group" aria-label="Show one kind of place"><button type="button" class="btn mu-f" data-k="" aria-pressed="true">Everything</button>{kinds}</div>
      <p class="nm-chips mu-jump">{chips}</p>
      <p class="nm-count" id="muCount" aria-live="polite">{n} places</p>
    </div>
{sections}
    <h2>Before you go</h2>
    <ul class="dis">
      <li><b>Check the hours.</b> Many of these places are run by volunteers and open only some days or some seasons. Their own websites have the latest.</li>
      <li><b>Researchers, write ahead.</b> Archives and research rooms often keep their records off the floor. A note a week before lets them have your boxes ready.</li>
      <li><b>Bring what you know.</b> Names, dates, the township, and a copy of anything you found here. Staff can do far more with a good question.</li>
      <li><b>Know of a place we missed?</b> <a href="/#contact">Tell us</a> and we will add it.</li>
    </ul>
    <p class="note">Every place on this page was checked against its own website, or a city, county, library or university page about it, in October 2026. Places marked “check before you go” could not be confirmed online. Hours change: always look at the place’s own site before travelling.</p>
    <script>
    (function(){{ "use strict";
      var q=document.getElementById('muQ'), cnt=document.getElementById('muCount'), items=[].slice.call(document.querySelectorAll('.mu')), secs=[].slice.call(document.querySelectorAll('.mu-c')), fs=[].slice.call(document.querySelectorAll('.mu-f')), kind='';
      var draw=function(){{ var w=q.value.trim().toLowerCase().split(/\\s+/).filter(Boolean), n=0;
        items.forEach(function(li){{ var ok=(!kind||li.dataset.k===kind) && w.every(function(x){{ return li.dataset.t.indexOf(x)>=0; }}); li.hidden=!ok; if (ok) n++; }});
        secs.forEach(function(s){{ s.hidden=!s.querySelector('.mu:not([hidden])'); }});
        cnt.textContent=n===items.length? n+' places' : n+' of '+items.length+' places'; }};
      fs.forEach(function(b){{ b.addEventListener('click',function(){{ kind=b.dataset.k; fs.forEach(function(x){{ x.setAttribute('aria-pressed',String(x===b)); }}); draw(); }}); }});
      q.addEventListener('input',draw);
    }})();
    </script>
'''
page('museums/index.html', 'Museums & historic places of the valley · Project Scroll',
     f'{n} museums, historic houses, research rooms and archives across the St. Joseph River valley in Michigan and Indiana, each checked against its own website, grouped by county.',
     body, og='https://projectscroll.com/og/records.jpg')
print('museums built', n, len(keys), 'counties')
