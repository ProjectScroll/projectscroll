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
  var t=new Date().toISOString().slice(0,10), n=0;
  document.querySelectorAll('#vsComing li').forEach(function(li){ if (li.dataset.end<t || n>=6) li.hidden=true; else n++; });
  if (!n){ var p=document.getElementById('vsNone'); if (p) p.hidden=false; }
});
</script>'''
CARDS = [
 ('/food/#eat', 'Eat', f'{n_eat} places to eat with a story: old taverns, soda fountains, a diner beside an auto museum, orchards and farm markets.'),
 ('/food/#stay', 'Stay', f'{n_stay} inns, bed and breakfasts and historic hotels, from Kalamazoo to the lakeshore.'),
 ('/seasons/', 'What’s on', f'{len(S)} fairs, festivals, harvests and holiday walks on a twelve-month calendar you can subscribe to.'),
 ('/museums/', 'Museums & historic places', f'{len(M)} museums, historic houses, libraries and archives on one map, with “open today” and ready-made day trips.'),
 ('/walk/', 'Walk old Broadway', 'Eleven stops through downtown Cassopolis, with old postcards and the 1860 plan underfoot. Works offline.'),
 ('/walk/dowagiac/', 'Walk Front Street', 'Thirteen stops through downtown Dowagiac: the stove works, the lure makers and the railroad.'),
 ('/passport/', 'Your passport', 'Press “I’m here” at a museum, a stop, a table or a festival to collect stamps and print a certificate.'),
 ('/postcards/', 'Old postcards', 'More than a hundred views of the valley’s towns as they were, to compare with what you see today.'),
]
cards = ''.join(f'<li><a href="{h}"><b>{E(t)}</b><span>{E(d)}</span></a></li>' for h,t,d in CARDS)
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Visit &amp; Plan</p>
    <h1>Coming to the St. Joseph River valley</h1>
    <p class="lede" style="font-size:1.15rem">Cassopolis and the towns around it, from Kalamazoo to Lake Michigan and down into northern Indiana, are an easy trip from Chicago, Detroit and Indianapolis. Here is what to see, where to eat and stay, what’s on, and how to get here, all in one place.</p>
    <ul class="vs-cards">{cards}</ul>
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
        <li><b>Plan a day.</b> On the <a href="/museums/">museums map</a>, add places to <i>My trip</i> or load a ready-made day trip, then press “Best order” for the shortest way round.</li>
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
''' + JS + '\n'
page('visit/index.html', 'Visit & Plan: coming to Cassopolis and the St. Joseph River valley · Project Scroll',
     'Planning a trip to Cassopolis and the St. Joseph River valley: places to eat and stay with a story, festivals and fairs, museums, walking tours, getting here by car, air or train, and when to come.', body, og='https://projectscroll.com/og/cassopolis.jpg')
print('visit built', len(up))
