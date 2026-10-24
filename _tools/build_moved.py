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

page('services/index.html', 'Services: research, imaging, design, LiDAR and film · Project Scroll',
     'Lost ancestors, family histories, legends tested against the record, forgotten places; digital imaging, graphic and web design, photography, 3D LiDAR, animation and film. An honest first read before you commit to anything.',
     CRUMB + frag('services', keep=('studio',)) + '\n    <p class="center"><a class="btn primary" href="/#contact">Tell us what you need</a> <a class="btn" href="/promotions/">Promotions for local businesses</a> <a class="btn" href="/research/">Research services, in detail</a></p>\n',
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
