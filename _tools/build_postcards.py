"""Cassopolis on old postcards: stand where the photographer stood.  python3 _tools/build_postcards.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
from oldcards import gallery, D as OC, BY as OCB
import json, html as _h
SEND=open(pathlib.Path(__file__).parent/'pcsend.html').read()
_E=lambda x: _h.escape(str(x or ''), quote=True)
PAIRS=json.load(open(pathlib.Path(__file__).parent/'data'/'thennow_pairs.json'))
def pair(x):
    if x['card'] in OCB:
        d=OCB[x['card']]; old=f'/img/oldcards/{d["id"]}.webp'; title=d['title']; w,h=d['w'],d['h']
    else:
        old=f'/img/strip/{x["card"]}.webp'; title=x.get('title',''); w,h=1600,400
    return (f'<figure class="tn"><div class="tn-box" style="aspect-ratio:{w}/{h}"><img src="{x["photo"]}" alt="{_E(title)}, today, photographed by {_E(x["by"])}" loading="lazy">'
            f'<div class="tn-old"><img src="{old}" alt="{_E(title)}, on the old postcard" loading="lazy"></div><input type="range" min="0" max="100" value="50" aria-label="Slide between the old postcard and today"></div>'
            f'<figcaption><b>{_E(title)}</b>: the old card on the left, today on the right. Photograph by {_E(x["by"])}, {_E(x["date"])}.</figcaption></figure>')
PAIRSEC=('<section id="pairs" aria-labelledby="tnH"><h2 id="tnH">Then and now: your photographs</h2>'
  +(f'<div class="tn-grid">{"".join(pair(x) for x in PAIRS)}</div>' if PAIRS else
    '<p class="hl-empty"><b>The first pair is waiting for you.</b> Take the same picture as one of these postcards, from the same spot, and send it in. Your photograph will go here beside the old one, with a slider to move between then and now, and your name under it.</p>')
  +'</section>')
OCJS = r"""<script>
(function(){ "use strict";
  var q=document.getElementById('ocQ'), cnt=document.getElementById('ocCount'); if (!q) return;
  var figs=[].slice.call(document.querySelectorAll('#valley ~ .oc-grid .oc, .oc-grid .oc')), S='', Dd='';
  var run=function(){ var t=q.value.trim().toLowerCase().split(/\s+/).filter(Boolean), n=0;
    figs.forEach(function(f){ var ok=(!S || (' '+f.dataset.s+' ').indexOf(' '+S+' ')>=0) && (!Dd || f.dataset.d===Dd) && t.every(function(w){ return f.dataset.t.indexOf(w)>=0; }); f.hidden=!ok; if (ok) n++; });
    document.querySelectorAll('.oc-grid').forEach(function(g){ var any=[].some.call(g.children, function(c){ return !c.hidden; }); g.hidden=!any; var h=g.previousElementSibling; if (h && h.tagName==='H3') h.hidden=!any; });
    document.querySelectorAll('h2[id]').forEach(function(h){ if (!/michigan|indiana/.test(h.id)) return; var nx=h.nextElementSibling, any=false; while (nx && nx.tagName!=='H2'){ if (nx.classList.contains('oc-grid') && !nx.hidden) any=true; nx=nx.nextElementSibling; } h.hidden=!any; });
    cnt.textContent=n+(n===1?' picture':' pictures')+(n<figs.length?' of '+figs.length:''); };
  q.addEventListener('input', run);
  document.querySelectorAll('.oc-f').forEach(function(b){ b.addEventListener('click', function(){ S=(S===b.dataset.s)?'':b.dataset.s; document.querySelectorAll('.oc-f').forEach(function(x){ x.setAttribute('aria-pressed', String(x.dataset.s===S)); }); run(); }); });
  document.querySelectorAll('.oc-dd').forEach(function(b){ b.addEventListener('click', function(){ Dd=(Dd===b.dataset.d)?'':b.dataset.d; document.querySelectorAll('.oc-dd').forEach(function(x){ x.setAttribute('aria-pressed', String(x.dataset.d===Dd)); }); run(); }); });
  var m=/[?&]q=([^&]+)/.exec(location.search); if (m){ q.value=decodeURIComponent(m[1].replace(/\+/g,' ')); run(); }
})();
</script>"""

CARDS=[
 ('yerty','West side of Broadway, looking south','A Yerty postcard. The photographer stood on Broadway with the stores of the west side on the right.'),
 ('broadway1','Broadway in the days of wagons','Horses and wagons on the main street, the store fronts close together.'),
 ('carriages','Carriages drawn up on Broadway','A row of buggies at the hitching rail: a market day, or a meeting.'),
 ('broadway3','Broadway when the first cars came','Early motor cars among the last of the buggies.'),
 ('broadway2','A Cassopolis street, early 1900s','Which street is it? The trees, the walks and the buildings are the clues.'),
 ('roadtotown','The road to town','The way in from the country. Where did it come in, and is the road still there?'),
]
figs=''.join(f'''      <figure class="pc"><picture><source type="image/webp" srcset="/img/strip/{k}-800.webp 800w, /img/strip/{k}.webp 1600w" sizes="(min-width:900px) 46rem, 92vw"><img src="/img/strip/{k}-800.webp" width="1600" height="400" alt="{t}, Cassopolis, on an old postcard." loading="lazy" decoding="async"></picture>
        <figcaption><b>{t}.</b> {n} <a href="/map/cassopolis/#17.00/41.91160/-86.01250">Find it on the 1860 plan →</a></figcaption></figure>
''' for k,t,n in CARDS)
body=f'''    <p class="crumb"><a href="/map/">← The map room</a></p>
    <p class="kicker">Postcards, then and now</p>
    <h1>Stand where the photographer stood</h1>
    <p class="lede" style="font-size:1.15rem">Old postcards of Cassopolis, from the days of wagons to the first motor cars. Each one was taken from a spot you can still stand on. Find it, take the same picture today, and send it to us: we will set your photograph beside the old one here, with your name on it.</p>
{figs}
    <h2>How to rephotograph a postcard</h2>
    <ol class="dis">
      <li><b>Find the spot.</b> Line up two things that have not moved, a corner of a building and a street, and walk until they sit in the picture the way they sit on the card.</li>
      <li><b>Match the height.</b> Most old postcards were taken from about head height; some from an upstairs window. Hold the camera where the photographer’s eye was.</li>
      <li><b>Match the lens.</b> Use your phone’s ordinary camera, not the wide one, and do not zoom.</li>
      <li><b>Stay safe and on public ground.</b> Never step into the road for a shot, and never go onto private property without leave.</li>
      <li><b>Send it in</b> to <a href="mailto:research@projectscroll.com?subject=Rephotographed%20postcard">research@projectscroll.com</a>, saying which card and when you took it. By sending it you let us show it here with your name.</li>
    </ol>
    <p class="note">The pictures are taken from old postcards of Cassopolis. Each was published before 1931, or published without a copyright notice, and is in the public domain in the United States. The pairings will be added as readers send them in.</p>
    {PAIRSEC}
    <h2 id="valley">The valley on old postcards and photographs</h2>
    <p>{len(OC)} more views of the towns of the St. Joseph River valley, from Cassopolis to Michigan City: main streets, depots, courthouses, libraries, hotels, mills, fairs and parades, most of them between 1900 and 1930. Each one links to the library or archive that holds it. Press a picture to see it full size.</p>
    <nav class="oc-jump" aria-label="Jump to a town">{''.join(f'<a href="#{a}">{b}</a>' for a,b in [('cassopolis','Cassopolis'),('dowagiac','Dowagiac'),('edwardsburg','Edwardsburg'),('marcellus','Marcellus'),('vandalia','Vandalia'),('the-villages','Villages'),('niles','Niles'),('benton-harbor-and-st-joseph','Benton Harbor'),('south-haven','South Haven'),('three-rivers','Three Rivers'),('kalamazoo','Kalamazoo'),('south-bend-and-mishawaka','South Bend'),('elkhart','Elkhart'),('goshen','Goshen'),('la-porte','La Porte'),('michigan-city','Michigan City')])}</nav>
{gallery()}    <p class="note">Every picture here is in the public domain in the United States: published before 1931, or published without a copyright notice. The libraries named under each one hold the originals and are thanked for making them free to see; none of them endorses this site. Have an old postcard of the valley? <a href="/story/">Tell us about it</a>.</p>
'''+OCJS+SEND+'\n'
page('postcards/index.html','Old postcards and photographs of the valley · Project Scroll','Old postcards and photographs of Cassopolis, Dowagiac, Niles, South Bend, Elkhart, Goshen and the other towns of the St. Joseph River valley, about 1900 to 1945, each linked to the library that holds it.',body,og='https://projectscroll.com/og/cassopolis.jpg')
print('postcards built')
