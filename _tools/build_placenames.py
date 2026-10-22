"""The place-names map: every story in "How the valley's towns got their names" on one map.
python3 _tools/build_placenames.py"""
import sys, json, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
R = pathlib.Path(__file__).resolve().parent.parent
E = lambda s: html.escape(str(s), quote=True)
N = json.load(open(R / '_tools/data/news.json'))
T = [s for s in N['stories'] if s.get('series') == 'names']
svg = open(R / '_tools/data/placenames_map.svg').read()
cards = ''.join(f'''<li><a href="/news/{E(s["slug"])}/"><picture><source type="image/avif" srcset="{s["pic"][0]}-sq.avif"><img src="{s["pic"][0]}-sq.webp" width="320" height="320" alt="" loading="lazy" decoding="async"></picture><b>{E(s["town"])}</b><span>{E(s["sdek"])}</span></a></li>''' for s in T)
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a> · <a href="/news/">All the news</a></p>
    <article class="pn">
    <p class="kicker">A series</p>
    <h1>How the valley’s towns got their names</h1>
    <p class="lede">Every town in the valley has a story about its name, and most of the stories are only half the record. In this series we go back to the plats, the acts, the post-office lists and the county histories for each one: the oldest spellings, the legends against the record, and what nobody wrote down. Press a town on the map to read its story.</p>
    <figure class="nw-map pn-fig">{svg}<figcaption>{len(T)} towns so far. State outline: U.S. Census Bureau, via us-atlas; rivers: Natural Earth (public domain), simplified.</figcaption></figure>
    <ul class="pn-cards">{cards}</ul>
    <p class="note">Which town should be next? <a href="mailto:research@projectscroll.com?subject=How%20the%20towns%20got%20their%20names">Tell us</a>, and send any record of a name’s origin you know of.</p>
    </article>
'''
page('place-names/index.html', 'How the valley’s towns got their names · Project Scroll', f'How {len(T)} towns of the St. Joseph and Kalamazoo valleys got their names, from the record: {", ".join(s["town"] for s in T)}.', body, og='https://projectscroll.com/og/records.jpg')
print('place names', len(T))
