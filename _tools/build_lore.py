"""Lore and legends of the valley: the hub for every story that wears the Legend ribbon or the Lore and legend kicker.
python3 _tools/build_lore.py   (reads _tools/data/news.json and top.json)"""
import sys, pathlib, json, html
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E_ = html.escape
R = pathlib.Path(__file__).parent
N = json.load(open(R/'data'/'news.json'))['stories']
TOP = dict(json.load(open(R/'data'/'top.json'))['top'])
L = [s for s in N if s.get('kicker') == 'Lore and legend' or TOP.get(s['slug']) == 'Legend']
def card(s):
    b = s['pic'][0]
    return (f'<li class="lr-card"><a href="/news/{s["slug"]}/"><picture><source type="image/avif" srcset="{b}-600.avif 600w, {b}.avif 1200w" sizes="(min-width:900px) 22rem, 92vw">'
            f'<img src="{b}-600.webp" srcset="{b}-600.webp 600w, {b}.webp 1200w" sizes="(min-width:900px) 22rem, 92vw" width="1200" height="675" alt="" loading="lazy" decoding="async"></picture>'
            f'<span class="nw-k">{E_(s["kicker"])}</span><b>{E_(s["headline"])}</b><span>{E_(s.get("sdek") or s["dek"])}</span></a></li>')
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a> · <a href="/news/">All the news</a></p>
    <p class="kicker">Lore and legends of the valley</p>
    <h1>Things in the dark</h1>
    <p class="lede">Monsters at the edge of the berry fields, a serpent in a spring-fed lake, a warning chalked on a tree. Every county keeps its stories. We take each one back to the oldest record we can find, and tell you which parts hold up, which don’t, and what nobody had noticed before.</p>
    <ul class="lr-list">{''.join(card(s) for s in L)}</ul>
    <aside class="lr-next"><p class="lr-next-h">A new legend every month</p><p>More of the valley’s stories are being tested against the record now, and one comes out each month: ghosts, lake serpents, lost villages and the strange things the old county histories set down without comment. The valley letter brings each one to your inbox.</p><p class="ctas"><a class="btn primary" href="/newsletter/">Get the valley letter</a> <a class="btn" href="mailto:research@projectscroll.com?subject=A%20legend%20for%20Project%20Scroll">Tell us a legend</a></p></aside>
    <h2>How we test a legend</h2>
    <ol class="dis"><li><b>Find the oldest telling.</b> Not the newest blog post: the first time it was printed, and who printed it.</li><li><b>Read the records around it.</b> Newspapers of the week, the county histories, the maps, the land entries.</li><li><b>Mark every statement.</b> Each one carries a Scrollmark, so you can see what the record says and what is our reading of it. <a href="/scrollmarks/">What the marks mean ›</a></li><li><b>Say what is new.</b> When we find something no telling has mentioned, it goes on the <a href="/discoveries/">Discoveries</a> page.</li></ol>
    <p class="note">Most of the places in these stories are private land and private shores. Please enjoy them from public roads, and never disturb a grave or a marker.</p>
'''
page('lore/index.html', 'Lore and legends of the valley · Project Scroll', 'Monsters, serpents, ghosts and warnings from the St. Joseph River valley, each taken back to the oldest record and tested: what holds up, what doesn’t, and what was never noticed before.', body)
print('lore built', len(L))
