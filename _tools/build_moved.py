"""Pages for the sections that moved off the home page: the case board, our services, the questions, and Lesson No. 1.
Their text lives in _tools/data/home/*.html (build_cases.py keeps the case board there up to date).   python3 _tools/build_moved.py"""
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
R = pathlib.Path(__file__).resolve().parents[1]; H = R / '_tools/data/home'
def frag(n, keep=()):
    t = (H / f'{n}.html').read_text()
    t = re.sub(r'\s*<p class="part">[^<]*</p>', '', t)                      # the home page's part numbers
    for a in ('contact', 'hunt', 'timeline'):
        t = t.replace(f'href="#{a}"', f'href="/#{a}"')
    for a, b in (('services', '/services/'), ('studio', '/services/#studio'), ('cases', '/cases/'), ('marks', '/scrollmarks/'), ('method', '/scrollmarks/#method'), ('faq', '/faq/')):
        if a not in keep: t = t.replace(f'href="#{a}"', f'href="{b}"')
    t = t.replace('href="#mk-', 'href="/scrollmarks/#mk-')
    return t
CRUMB = '    <p class="crumb"><a href="/">← Project Scroll</a></p>\n'

page('cases/index.html', 'The case board · Project Scroll',
     'Every mystery the Project Scroll hunt has posted, where each one stands, and who has cracked it. Free to play; every answer is in the record.',
     CRUMB + frag('cases', keep=('cases',)) + '\n    <p class="center"><a class="btn" href="/#hunt">How the hunt works</a> <a class="btn" href="/treasure-hunt-quest/">The hunt: your hunter’s card</a></p>\n',
     og='https://projectscroll.com/og/hunt.jpg')


ALL = [
 ('Family research', 'Lost ancestors, family lines and the questions that have stumped a family for years.', ['Lost ancestors traced through the records', 'Brick walls broken, or honestly explained', 'Every statement marked, every source cited'], 'Research: a mystery or an ancestor'),
 ('Family histories and registers', 'Your family’s story, written and bound to last.', ['Family histories and monographs', 'Registers of every descendant, laid out by generation', 'Printed books and keepsake editions'], 'Research: a mystery or an ancestor'),
 ('Legends, tested', 'The story your grandmother told, put to the record.', ['Family legends checked against the documents', 'What is true, what grew, and where it came from', 'Written up so the next generation has the facts'], 'Research: a mystery or an ancestor'),
 ('Places, maps and land', 'Forgotten towns, old roads, surveys and the land under your feet.', ['Land records, plats and survey notes read and explained', 'Then-and-now maps of a farm, a street or a town', 'House and building histories'], 'Research: a mystery or an ancestor'),
 ('Research for authors, films and groups', 'Historical research for people who publish.', ['Background research for books, films and exhibits', 'Fact-checking before you publish', 'Lodges, societies, heirlooms and old organizations'], 'Research: a mystery or an ancestor'),
 ('Digital imaging and restoration', 'Old photographs and papers brought back to life.', ['High-resolution imaging of photographs, documents and maps', 'Imaging analysis: faded ink, damaged pages, hidden detail', 'Restoration and colour, done with care'], 'Digital imaging or scanning'),
 ('Design', 'Graphic and web design that lasts.', ['Websites for families, societies and small businesses', 'Books, charts, posters and keepsakes', 'Logos, signs and brochures'], 'Digital imaging or scanning'),
 ('Photography, drone and film', 'Your place and your people, seen properly.', ['Photography and drone photography', 'Video production: family films and interviews', 'Short films for events and anniversaries'], '3D LiDAR imaging'),
 ('3D LiDAR and animation', 'The ground itself, in three dimensions.', ['3D LiDAR models of land, towns and trails', 'Fly-throughs and places as they were', 'Old maps laid over the real ground'], '3D LiDAR imaging'),
 ('Living documents', 'Research that keeps growing.', ['Timelines and research pages that update as records turn up', 'Shareable pages and print editions', 'Every change dated and noted'], 'Research: a mystery or an ancestor'),
 ('Promotions', 'For local businesses and organizations.', ['Sponsor a quest case', 'Your history, told from the record', 'Events, anniversaries and “brought to you by”'], 'A promotion'),
]
ALLH = ('<aside class="promo sv mod pr-hero sv-all" aria-labelledby="svAllH" id="all"><i class="sv-orn o1" aria-hidden="true">❦</i><i class="sv-orn o2" aria-hidden="true">❦</i><i class="sv-orn o3" aria-hidden="true">❦</i><i class="sv-orn o4" aria-hidden="true">❦</i>'
        '<p class="sv-banner"><span>★ Every service, in full ★</span></p><h2 class="promo-h" id="svAllH">Everything the desk and the studio do.</h2>'
        '<p class="promo-lede">Pick one, or put several together. Every commission starts with an honest first read, and you own the report.</p><div class="sv-cols pr-cols">'
        + ''.join(f'<section class="sv-col pr-card" aria-labelledby="sa{i}"><p class="sv-no" aria-hidden="true">No. {i+1}</p><h3 id="sa{i}">{t}</h3><p class="sv-d">{d}</p><ul>{"".join(f"<li>{x}</li>" for x in L)}</ul><p class="sv-ask"><a href="{"/promotions/" if t=="Promotions" else "/#contact"}" data-need="{n}">{"See the promotions ›" if t=="Promotions" else "Ask about this ›"}</a></p></section>' for i,(t,d,L,n) in enumerate(ALL))
        + '</div><p class="promo-ctas"><a class="btn primary" href="/#contact">Tell us what you need</a><a class="btn" href="/promotions/">Promotions</a><a class="btn" href="/research/">Research services, in detail</a></p></aside>\n')
page('services/index.html', 'Services: research, imaging, design, LiDAR and film · Project Scroll',
     'Lost ancestors, family histories, legends tested against the record, forgotten places; digital imaging, graphic and web design, photography, 3D LiDAR, animation and film. An honest first read before you commit to anything.',
     CRUMB + frag('services', keep=('studio',)) + '\n    ' + ALLH + '    <p class="center"><a class="btn primary" href="/#contact">Tell us what you need</a> <a class="btn" href="/promotions/">Promotions for local businesses</a> <a class="btn" href="/research/">Research services, in detail</a></p>\n',
     og='https://projectscroll.com/og/services.jpg')

ld = (H / 'faq-ld.html').read_text() if (H / 'faq-ld.html').exists() else ''
page('faq/index.html', 'Questions people ask · Project Scroll',
     'Does the hunt cost anything? Do I have to go anywhere? Can you help with my own family’s mystery? Answers to the questions people ask Project Scroll.',
     CRUMB + frag('faq') + '\n    ' + ld + '    <p class="center"><a class="btn primary" href="/#contact">Ask us something else</a></p>\n')

page('notes/from-the-desk/index.html', 'From the field notes: Lesson No. 1 · Project Scroll',
     'Lesson No. 1 from the desk: two old records, two different stories, and what to do. With the person of the month and a record to weigh yourself.',
     '    <p class="crumb"><a href="/notes/">← Field notes</a></p>\n' + frag('notes') + '\n')
print('moved pages built')

# ---- three small pieces that left the home page, injected into the pages that now carry them ----
def inject(path, key, frag_name, before):
    f = R / path; s = f.read_text(); frag = (H / frag_name).read_text().strip()
    blk = f'<!--{key}-->\n    {frag}\n    <!--/{key}-->\n    '
    if f'<!--{key}-->' in s:
        s = re.sub(rf'<!--{key}-->.*?<!--/{key}-->\n    ', lambda m: blk, s, flags=re.S)
    else:
        i = s.index(before); s = s[:i] + blk + s[i:]
    f.write_text(s)
inject('map/index.html', 'mom', 'mom.html', '<h2 id="look">')                 # Map of the month, in the map room
inject('lore/index.html', 'plate2', 'plate2.html', '\n  </main>'.lstrip('\n'))  # the window and the glacial-age quote
inject('about/index.html', 'stats', 'stats.html', '\n  </main>'.lstrip('\n'))  # the four numbers
print('moved pieces injected')
