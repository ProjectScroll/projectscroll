"""Find a grave or an obituary: county by county, where the records are. python3 _tools/build_cemeteries.py (data: _tools/data/cemeteries.json)"""
import sys, pathlib, json, html, re
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E_ = html.escape
G = json.load(open(pathlib.Path(__file__).parent/'data'/'cemeteries.json'))
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def items(xs, extra=()):
    out = []
    for x in xs:
        nm = f'<a href="{E_(x["url"])}" rel="noopener">{E_(x["name"])}</a>' if x.get('url') else E_(x['name'])
        bits = [E_(x.get('what', ''))] + [f'<b>{lab}:</b> {E_(x[k])}' for k, lab in extra if x.get(k)]
        out.append(f'<li><b>{nm}</b>. ' + ' '.join(b for b in bits if b) + '</li>')
    return '<ul class="cg-list">' + ''.join(out) + '</ul>'
secs, nav = [], []
for c in G:
    sid = slug(c['county'] + ' ' + c['state']); name = f'{c["county"]} County, {c["state"]}'
    nav.append(f'<a href="#{sid}">{E_(name)}</a>')
    walk = ''.join(f'<li><b>{E_(w["name"])}</b>{(", " + E_(w["address"])) if w.get("address") else ""}. {E_(w.get("why", ""))}{(" <a href=" + chr(34) + E_(w["url"]) + chr(34) + " rel=noopener>More</a>") if w.get("url") else ""}</li>' for w in c.get('walk', []))
    secs.append(f'''    <section id="{sid}" aria-labelledby="{sid}-h" class="cg-c"><h2 id="{sid}-h">{E_(name)}</h2>
      <h3>Burials and cemetery records</h3>{items(c.get("burials", []))}
      <h3>Obituaries</h3>{items(c.get("obituaries", []), (("years", "Years"), ("how", "How to get a copy")))}
      <h3>Death records</h3>{items(c.get("deaths", []))}
      {f'<h3>Old cemeteries you can walk</h3><ul class="cg-list">{walk}</ul>' if walk else ''}
      {f'<p class="note">{E_(c["notes"])}</p>' if c.get("notes") else ''}
    </section>''')
body = f'''    <p class="crumb"><a href="/people/">← Family research</a></p>
    <p class="kicker">Family research, county by county</p>
    <h1>Find a grave or an obituary</h1>
    <p class="lede">Where the burial records, obituary indexes and death certificates are for the seven counties of the St. Joseph River valley, and how to ask for a copy. Each entry links to the office or library that holds the record. Fees and hours change: check before you write or go.</p>
    <nav class="cg-nav" aria-label="Counties">{" · ".join(nav)}</nav>
{"".join(secs)}
    <h2>Good manners in old cemeteries</h2>
    <ul class="dis"><li>Visit in daylight, keep to the paths, and leave everything as you found it.</li><li>Never rub, chalk or clean a stone; photograph it in raking light instead. Our <a href="/guide/gravestones/">gravestone guide</a> shows how.</li><li>Township cemeteries belong to the township: the clerk or sexton keeps the lot records.</li></ul>
    <p class="ctas"><a class="btn primary" href="/research/">Ask us to find it</a> <a class="btn" href="/guide/death-certificate/">Reading a death certificate</a> <a class="btn" href="/people/">Family research</a></p>
'''
page('cemeteries/index.html', 'Find a grave or an obituary · seven counties · Project Scroll',
     'Where to find burial records, obituary indexes and death certificates in Cass, Berrien, Van Buren and St. Joseph counties, Michigan, and St. Joseph, Elkhart and LaPorte counties, Indiana.', body)
print('cemeteries built', len(G))
