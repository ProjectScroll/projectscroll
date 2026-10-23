"""Short town pages for the wider valley (data: _tools/data/towns.json). Towns marked partial in their notes are skipped.
python3 _tools/build_towns.py"""
import sys, pathlib, json, html, re
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E_ = html.escape
T = json.load(open(pathlib.Path(__file__).parent/'data'/'towns.json'))
SKIP = {'three-rivers'}          # not finished: the research ran out before the records and landmarks were found
done = [t for t in T if t['slug'] not in SKIP]
for t in done:
    others = ' · '.join(f'<a href="/{o["slug"]}/">{E_(o["name"])}</a>' for o in done if o is not t)
    facts = ''.join(f'<div><dt>{E_(a)}</dt><dd>{E_(b)}</dd></div>' for a, b in t['facts'])
    lm = ''.join(f'<li><b>{E_(l["name"])}</b>{(", " + E_(l["address"])) if l.get("address") else ""}. {E_(l.get("what",""))}</li>' for l in t.get('landmarks', []))
    cut = lambda c: re.sub(r'\s*\([^()]*(scan|snippet|search)[^()]*\)', '', re.split(r' — |; passages read|; its full-text', c)[0]).strip()
    bal = lambda c: c + ')' * (c.count('(') - c.count(')'))
    src = ''.join(f'<li>{E_(bal(cut(s["cite"])))}{(" <a href=" + chr(34) + E_(s["url"]) + chr(34) + " rel=noopener>link</a>") if s.get("url") else ""}</li>' for s in t.get('sources', []))
    body = f'''    <p class="crumb"><a href="/visit/">← Visit &amp; Plan</a></p>
    <p class="kicker">{E_(t["county"])}</p>
    <h1>{E_(t["name"])}</h1>
    <p class="lede">{E_(t["lede"])}</p>
    <h2>At a glance</h2>
    <dl class="tw-facts">{facts}</dl>
    {f'<h2>Worth a visit</h2><ul class="cg-list">{lm}</ul>' if lm else ''}
    <h2>Where the records are</h2>
    <p>{E_(t["where"])}</p>
    <h2>Sources</h2>
    <ul class="nw-src">{src}</ul>
    <p class="note">Dates and names are from the county histories and official sources listed here. Where they disagree, we say so. Know better? <a href="/story/#fix">Send a correction</a>.</p>
    <p class="ctas"><a class="btn" href="/valley-map/">The valley map</a> <a class="btn" href="/museums/">Museums</a> <a class="btn" href="/cemeteries/">Find a grave or an obituary</a></p>
    <p class="note">More towns: {others}</p>
'''
    page(f'{t["slug"]}/index.html', f'{t["name"]}, {t["state"]}: history and records · Project Scroll', t['lede'][:155].rsplit(' ', 1)[0] + '…', body)
print('towns built', len(done))
