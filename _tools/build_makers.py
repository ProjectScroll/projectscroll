"""Made in the Valley: the factories and farms that made the valley's name, each with what it made, its story,
how it ended, and where to see it today.  Data: data/makers.json.  python3 _tools/build_makers.py"""
import sys, json, re, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
import oldcards as O
E = lambda s: html.escape(str(s), quote=True)
H = pathlib.Path(__file__).parent/'data'
M = json.load(open(H/'makers.json'))
MU = {m['name']: m for m in json.load(open(H/'museums.json'))}
def smart(s):
    s = re.sub(r"(^|[\s(])'", r'\1“', s); s = re.sub(r"'(?=[\s.,;:)!?]|$)", '”', s); return s.replace("'", '’')
REG = [('Cass County, Michigan', ['round-oak-stove','dowagiac-drill','heddon']),
       ('Berrien and St. Joseph counties, Michigan', ['benton-harbor-fruit-market','whirlpool','kawneer','clark-equipment','sheffield-car']),
       ('Kalamazoo', ['kalamazoo-celery','gibson','upjohn','kalamazoo-stove','shakespeare','checker-motors']),
       ('South Bend and Mishawaka, Indiana', ['studebaker','oliver-chilled-plow','singer-south-bend','ball-band','bendix']),
       ('Elkhart, Nappanee and La Porte, Indiana', ['conn','miles-laboratories','coppes','rumely'])]
PC = {'round-oak-stove':['ps022','ps107'], 'dowagiac-drill':['ps013'], 'sheffield-car':['ps062'], 'benton-harbor-fruit-market':['ps051','ps050']}
SEE = {'round-oak-stove':['Dowagiac Area History Museum'], 'dowagiac-drill':['Dowagiac Area History Museum'], 'heddon':['Heddon Museum'],
       'studebaker':['Studebaker National Museum','Studebaker-Bendix Heritage Trail'], 'oliver-chilled-plow':['The History Museum'], 'bendix':['Studebaker-Bendix Heritage Trail'],
       'gibson':['Kalamazoo Valley Museum'], 'kalamazoo-stove':['Kalamazoo Valley Museum'], 'checker-motors':['Gilmore Car Museum','Kalamazoo Valley Museum'],
       'rumely':['La Porte County History Museum (La Porte County Historical Society)'], 'coppes':['Coppes Commons and Coppes History Museum']}
BY = {m['id']: m for m in M}
assert sorted(BY) == sorted(i for _, L in REG for i in L)
def card(m):
    k = m['id']; facts = []
    if m.get('founded'): facts.append(('Begun', m['founded']))
    if m.get('founder'): facts.append(('By', m['founder']))
    if m.get('made'): facts.append(('Made', m['made']))
    if m.get('peak'): facts.append(('At its height', m['peak']))
    if m.get('end'): facts.append(('How it ended', m['end']))
    if m.get('today'): facts.append(('Today', m['today']))
    dl = ''.join(f'<dt>{E(a)}</dt><dd>{E(smart(b))}</dd>' for a, b in facts)
    pcs = ''.join(f'<figure class="mk-pc">{O.pic(O.BY[i], "(min-width:900px) 16rem, 46vw")}<figcaption><a href="/postcards/#oc-{i}">{E(O.BY[i]["title"])}</a> · {E(O.BY[i]["date"])}</figcaption></figure>' for i in PC.get(k, []))
    see = [f'<a href="/museums/#{O.slug(n)}">{E(n.split(" (")[0])}</a>' for n in SEE.get(k, []) if n in MU]
    see += [f'<a href="{E(s["url"])}" rel="noopener">{E(s["place"].split(" (")[0])}</a>' for s in m.get('see_it', []) if not any(s['place'].startswith(n.split(' (')[0]) for n in SEE.get(k, []))]
    src = ' '.join(f'<a href="{E(u)}" rel="noopener">source {i}</a>' for i, u in enumerate(m['sources'], 1))
    return f'''<li class="mk" id="{k}"><p class="mu-k">{E(m['town'])}, {E(m['state'])}</p><h3>{E(m['name'])}</h3>
        {f'<div class="mk-pcs">{pcs}</div>' if pcs else ''}<p>{E(smart(m['story']))}</p><dl class="mk-dl">{dl}</dl>
        {f'<p class="mk-see"><b>See it:</b> {" · ".join(see)}</p>' if see else ''}<p class="wk-src">{src}</p></li>'''
secs = ''.join(f'<section aria-labelledby="mk-{O.slug(t)}"><h2 id="mk-{O.slug(t)}">{E(t)}</h2><ol class="mk-list">{"".join(card(BY[i]) for i in L)}</ol></section>' for t, L in REG)
nav = ' '.join(f'<a href="#mk-{O.slug(t)}">{E(t.split(",")[0])}</a>' for t, _ in REG)
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Made in the Valley</p>
    <h1>What the valley made</h1>
    <p class="lede" style="font-size:1.15rem">Stoves and seed drills, fishing lures and band horns, wagons, plows, guitars, rubber boots, washing machines, celery and peaches. For a century the towns of the St. Joseph River valley made things the whole country knew by name. Here are {len(M)} of the makers: who started them, what they made, how they ended, and where you can still see their work.</p>
    <p class="nm-chips mu-jump"><span class="mu-jl">Jump to:</span> {nav}</p>
{secs}
    <p class="vs-plan"><a class="btn" href="/heirlooms/">Have something one of them made? Add it to the heirloom cabinet</a></p>
    <p class="note">Each maker was checked against the sources linked under it in October 2026: museum and library pages, state historical markers, local newspapers and company histories. Where sources disagree on a date, we say so or give the range. The big claims (“largest in the world”) are the makers’ own boasts, as printed at the time. Corrections are welcome at <a href="mailto:research@projectscroll.com">research@projectscroll.com</a>.</p>
'''
page('made-in-the-valley/index.html', 'Made in the Valley · Project Scroll', f'The makers of the St. Joseph River valley: Round Oak stoves, Heddon lures, Studebaker wagons, Oliver plows, Conn horns, Gibson guitars, Kalamazoo celery and more. {len(M)} makers, their stories and where to see their work today.', body, og='https://projectscroll.com/og/legends.jpg')
print('makers built', len(M))
