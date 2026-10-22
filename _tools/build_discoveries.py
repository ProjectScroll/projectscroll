"""Discoveries: every new finding on Project Scroll, with its story and its credit.
python3 _tools/build_discoveries.py"""
import sys, json, pathlib, html, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
R = pathlib.Path(__file__).resolve().parent.parent
E = lambda s: html.escape(str(s), quote=True)
M = ['January','February','March','April','May','June','July','August','September','October','November','December']
day = lambda d: (lambda x: f'{x.day} {M[x.month-1]} {x.year}')(datetime.date.fromisoformat(d))
N = json.load(open(R / '_tools/data/news.json'))
rows = [(x, s) for s in N['stories'] for x in s.get('finds', [])]
rows.sort(key=lambda r: r[0]['d'], reverse=True)
items = ''.join(f'<li><p><span class="nw-tier n">New finding</span> {x["t"]}</p><p class="dsc-s">In <a href="/news/{E(s["slug"])}/">{E(s["headline"])}</a> · found by Michael Urbanski, Project Scroll, {day(x["d"])}</p></li>' for x, s in rows)
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a> · <a href="/news/">All the news</a> · <a href="/sources/libraries/">The libraries behind the stories</a></p>
    <article class="dsc">
    <p class="kicker">Discoveries</p>
    <h1>What we have found</h1>
    <p class="lede">Most of what Project Scroll publishes was known to someone before us; we say where. These are the exceptions: facts found in the original records by Michael Urbanski for Project Scroll that we could not find in any published history, article or website. Each links to the story where it is set out, with its source and what we searched.</p>
    <ol class="dsc-list">{items}</ol>
    <p class="note">“New” means new to print as far as we can tell, not that nobody ever noticed. If you know of an earlier publication of any of these, <a href="mailto:research@projectscroll.com?subject=An%20earlier%20publication">tell us</a>, and we will credit it on the story and here. To cite a finding, cite the story, and credit Michael Urbanski, Project Scroll.</p>
    </article>
'''
page('discoveries/index.html', 'Discoveries · Project Scroll', f'{len(rows)} new findings from the original records, made by Michael Urbanski for Project Scroll: facts not found in any earlier published history.', body, og='https://projectscroll.com/og/records.jpg')
print('discoveries', len(rows))
