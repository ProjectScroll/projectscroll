"""Explore by place: the home page's map of every story with a place, and its town list.
python3 _tools/build_placemap.py
The map drawing and the story groups come from _tools/data/storymap.json (made by the map tool from news.json);
this script writes the section into news/index.html (All the news) between <!--placemap--> and <!--/placemap-->. It used to sit on the home page."""
import json, pathlib, re, html
R = pathlib.Path(__file__).resolve().parent.parent
E = lambda s: html.escape(str(s), quote=True)
D = json.load(open(R / '_tools/data/storymap.json'))
N = {s['slug']: s for s in json.load(open(R / '_tools/data/news.json'))['stories']}
pid = lambda p: 'place-' + re.sub(r'[^a-z]+', '-', p.lower()).strip('-')
groups = sorted(D['groups'].items(), key=lambda kv: (-len(kv[1]), kv[0]))
li = ''.join(f'<li id="{pid(pl)}"><details><summary><b>{E(pl)}</b> <span>{len(ss)} {"story" if len(ss)==1 else "stories"}</span></summary><ul>'
             + ''.join(f'<li><a href="/news/{E(sl)}/">{E(N[sl]["headline"] if sl in N else h)}</a></li>' for sl, h in ss) + '</ul></details></li>' for pl, ss in groups)
n = sum(len(ss) for _, ss in groups)
SEC = (f'<!--placemap-->\n    <section class="sm" aria-labelledby="smH" data-placemap><div class="sm-head"><h2 id="smH">Explore by place</h2>'
       f'<p>{n} stories, {len(groups)} places, one map. Press a town to read its story; where there are several, pick from the list.</p></div>'
       f'<div class="sm-grid"><figure class="sm-fig">{D["svg"].replace('role="img"', 'role="group"', 1)}</figure><ul class="sm-list">{li}</ul></div></section>\n    <!--/placemap-->')
p = R / 'news/index.html'; s = open(p).read()
if '<!--placemap-->' in s:
    s = re.sub(r'<!--placemap-->.*?<!--/placemap-->', lambda m: SEC, s, flags=re.S)
else:
    raise SystemExit('no <!--placemap--> marker in news/index.html')
open(p, 'w').write(s)
print('placemap', len(groups), 'places', n, 'stories')
