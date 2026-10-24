"""Discoveries: every new finding on Project Scroll, with its record, its story, what we searched, and its credit.
python3 _tools/build_discoveries.py

Each finding lives in its story's "finds" list in _tools/data/news.json:
  {"id": "short-slug", "t": "the finding (html)", "d": "YYYY-MM-DD", "s": "what we searched (html)",
   "town": "Cassopolis", "img": "/img/...webp", "alt": "what the crop shows", "cap": "the record, short"}
id, town, img, alt and cap are optional; the story's square lead image stands in when img is absent."""
import sys, json, pathlib, html, datetime, re
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
R = pathlib.Path(__file__).resolve().parent.parent
E = lambda s: html.escape(str(s), quote=True)
M = ['January','February','March','April','May','June','July','August','September','October','November','December']
day = lambda d: (lambda x: f'{x.day} {M[x.month-1]} {x.year}')(datetime.date.fromisoformat(d))
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
N = json.load(open(R / '_tools/data/news.json'))
_FD = json.load(open(R / '_tools/data/finds.json'))
def _fres(x):
    if 'ref' not in x: return x
    k, i = x['ref'].split('#'); y = next(z for z in _FD[k] if z.get('id') == i)
    return dict(y, shared=k)
_DATES = {s['slug']: s['date'] for s in N['stories']}
for _s in N['stories']:
    if _s['slug'] in _FD: _s['finds'] = [dict(_fres(x), d=_fres(x).get('d') or _DATES.get(_fres(x).get('shared') or _s['slug'])) for x in _FD[_s['slug']]]
_ORD = [k for k in _FD if not k.startswith('_')]
rows = [(x, s) for s in sorted(N['stories'], key=lambda s: _ORD.index(s['slug']) if s['slug'] in _ORD else 99) for x in s.get('finds', []) if not x.get('shared')]
rows.sort(key=lambda r: r[0]['d'], reverse=True)

SEAL = ('<svg class="dsc-seal" viewBox="0 0 60 60" aria-hidden="true"><g transform="translate(30 30)">'
        + ''.join(f'<path d="M0-29 5-22-5-22z" fill="#B7811C" transform="rotate({i*22.5})"/>' for i in range(16))
        + '<circle r="22" fill="#E9BE4C" stroke="#6E4A0C" stroke-width="1.3"/><circle r="18" fill="none" stroke="#FFF3C0" stroke-width="1" stroke-dasharray="2 2"/>'
        '<path d="M-14-8 0-17 14-8" fill="none" stroke="#F7DC86" stroke-width="1.2"/><text y="5" text-anchor="middle" font-family="Georgia,serif" font-size="12.5" font-weight="700" fill="#4a300a" letter-spacing=".5">NEW</text></g></svg>')

def town(x, s):
    return x.get('town') or s.get('town') or 'The valley'

def item(i, x, s):
    fid = x.get('id') or f'{s["slug"]}-{i}'
    cap = f'<span class="dsc-cap">{E(x["cap"])}</span>' if x.get('cap') else ''
    if x.get('img'):
        pic = f'<img src="{E(x["img"])}" alt="{E(x.get("alt", ""))}" loading="lazy" decoding="async">'
    else:
        a, b, c = (x.get('card') or f'{s["headline"]}||').split('|')
        pic = f'<span class="dsc-card"><b>{E(a)}</b><span>{E(b)}</span><i>{E(c)}</i></span>'
    srch = f'<div class="dsc-srch"><p class="dsc-srch-h">What we searched</p><p>{x["s"]}</p></div>' if x.get('s') else ''
    tw = town(x, s)
    return (f'<li id="{E(fid)}" data-town="{E(slug(tw))}"><span class="dsc-pic">{pic}{SEAL}{cap}</span>'
            f'<div class="dsc-body"><p class="dsc-tw">{E(tw)}{(" <span class=\"dsc-kind\">"+E(x["kind"])+"</span>") if x.get("kind") else ""}</p><p class="dsc-t">{x["t"]}</p>'
            f'<p class="dsc-s">In <a href="/news/{E(s["slug"])}/">{E(s["headline"])}</a> · found by Michael Urbanski, Project Scroll, {day(x["d"])}</p>'
            f'{srch}<p class="dsc-act"><a class="dsc-link" href="#{E(fid)}" data-dsclink>Link to this finding</a></p></div></li>')

items = ''.join(item(i, x, s) for i, (x, s) in enumerate(rows, 1))
towns = sorted({town(x, s) for x, s in rows}, key=lambda t: (-sum(1 for x, s in rows if town(x, s) == t), t))
chips = ('<div class="dsc-filter" data-dscfilter hidden role="group" aria-label="Show findings by town"><button type="button" aria-pressed="true" data-t="">All <span>' + str(len(rows)) + '</span></button>'
         + ''.join(f'<button type="button" aria-pressed="false" data-t="{E(slug(t))}">{E(t)} <span>{sum(1 for x, s in rows if town(x, s) == t)}</span></button>' for t in towns)
         + '</div>') if len(towns) > 1 else ''
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a> · <a href="/news/">All the news</a> · <a href="/sources/libraries/">The libraries behind the stories</a></p>
    <article class="dsc">
    <p class="kicker">Discoveries</p>
    <h1>What we’ve found</h1>
    <p class="lede">Most of what Project Scroll publishes was known to someone before us; we say where. These are the exceptions: facts found in the original records by Michael Urbanski for Project Scroll that we could not find in any published history, article or website. Each shows the record it came from, links to the story where it is set out with its source, and lists what we searched before calling it new.</p>
    {chips}
    <p class="dsc-kinds"><b>Kinds of finding.</b> <i>New record</i>: a fact in no published account. <i>Earliest record</i>: the first appearance in print, earlier than any account gives. <i>Correction</i>: the record says otherwise than the accounts. <i>Connection</i>: two records that had not been put together. <i>Identification</i>: an unnamed source named. <i>Map reading</i>: a fact read from a map. <i>Compilation</i>: a list that did not exist. <i>Myth tested</i>: a story traced and found to have no early source.</p>
    <ol class="dsc-list">{items}</ol>
    <p class="dsc-none" hidden>No findings for that town yet.</p>
    <p class="note">“New” means new to print as far as we can tell, not that nobody ever noticed. If you know of an earlier publication of any of these, <a href="mailto:research@projectscroll.com?subject=An%20earlier%20publication">tell us</a>, and we will credit it on the story and here. To cite a finding, cite the story, and credit Michael Urbanski, Project Scroll.</p>
    </article>
'''
page('discoveries/index.html', 'Discoveries · Project Scroll', f'{len(rows)} new findings from the original records, made by Michael Urbanski for Project Scroll: facts not found in any earlier published history.', body, og='https://projectscroll.com/og/discoveries.jpg')
json.dump({'count': len(rows)}, open(R / '_tools/data/discoveries_count.json', 'w'))
print('discoveries', len(rows))
