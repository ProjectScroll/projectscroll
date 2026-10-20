"""The gazetteer: every place on the trail and the old map it is on, read from the home page's place band so the two never drift:  python3 _tools/build_places.py"""
import sys, re, html, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
R=pathlib.Path(__file__).resolve().parent.parent
s=(R/'index.html').read_text(encoding='utf-8')
band=s[s.index('id="pbTrack"'):s.index('</ul>', s.index('id="pbTrack"'))]
groups=[]; cur=None
for m in re.finditer(r'<li( class="([^"]*)")?>(.*?)</li>', band):
    cls, inner=m.group(2), m.group(3)
    if cls=='pb-hall': continue
    if cls=='pb-c':
        name=re.sub('<[^>]+>','',inner)
        if name=='St. Joseph River Valley': continue
        cur=[name, []]; groups.append(cur); continue
    a=re.search(r'<a href="([^"]+)"(?: title="([^"]*)")?>([^<]+)</a>', inner)
    if a: cur[1].append((a.group(3), a.group(1), html.unescape(a.group(2) or '')))
    else: cur[1].append((inner, None, ''))
def what(name, href, title):
    if not href: return 'Not yet on a map here'
    if href.startswith('/map/#twp-'): return title or 'Township plat, about 1928'
    if href.startswith('/map/#town-'): return title or 'On the old maps'
    return 'Its own page: history, and the 1860 plan laid over today’s streets'
sec=[]
for county, places in groups:
    rows=''.join(f'<tr><th scope="row">{html.escape(n)}</th><td>{html.escape(what(n,h,t))}</td><td>{"<a href=%s>Open</a>" % chr(34)+h+chr(34) if h else "—"}</td></tr>' for n,h,t in places)
    rows=''.join(f'<tr><th scope="row">{html.escape(n)}</th><td>{html.escape(what(n,h,t))}</td><td>' + ((f'<a href="{h}">Open the map</a>' if h.startswith('/map/') else f'<a href="{h}">Open its page</a>') if h else '—') + '</td></tr>' for n,h,t in places)
    sid=re.sub(r'[^a-z]+','-',county.lower()).strip('-')
    sec.append(f'''    <h2 id="{sid}">{html.escape(county)}</h2>
    <table class="gaz"><thead><tr><th scope="col">Place</th><th scope="col">On the old map</th><th scope="col"><span class="vh">Link</span></th></tr></thead><tbody>{rows}</tbody></table>
''')
n=sum(len(p) for _,p in groups); linked=sum(1 for _,p in groups for x in p if x[1])
toc=' · '.join(f'<a href="#{re.sub(r"[^a-z]+","-",c.lower()).strip("-")}">{html.escape(c)}</a>' for c,_ in groups)
body=f'''    <p class="crumb"><a href="/map/">← The map room</a></p>
    <p class="kicker compass">The gazetteer</p>
    <h1>Every place on the trail, on the old maps</h1>
    <p class="lede">The hunt began in Cassopolis, and the record runs out in every direction: up the St. Joseph River to Kalamazoo and down it to South Bend, across the line to Elkhart and Goshen, out to the lake shore. Here are all {n} places, county by county, and the map each one opens on: the 1860 wall map, the county maps of 1858, 1861 and 1863, the atlases of Berrien and Kent, and the township plats of about 1928.</p>
    <p class="note">{linked} of {n} open on a map. {toc}</p>
''' + ''.join(sec) + '''    <p class="note">Where a town had not yet been founded when its map was drawn, the link opens the township where it later grew, and says so. Corrections and better maps are welcome at <a href="mailto:research@projectscroll.com?subject=Gazetteer">research@projectscroll.com</a>.</p>
'''
page('places/index.html','Gazetteer: every place on the trail · Project Scroll','Every town, village and township on the Project Scroll trail, from Cassopolis to South Bend, Kalamazoo, Elkhart and the Lake Michigan shore, each linked to the old map it appears on.', body)
print('gazetteer', n, 'places,', linked, 'linked')
