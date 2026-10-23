"""Scrollmarks: the page that explains the nine marks. The marks themselves are lifted from the home page's #marks section,
so the two never disagree.   python3 _tools/build_scrollmarks.py"""
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
R = pathlib.Path(__file__).parent.parent
s = open(R/'index.html').read()
i = s.index('<section id="marks"'); j = s.index('<div class="weigh"', i)
core = s[i:j]
core = core[core.index('<figure class="scale"'):]          # the scale, the nine definitions and the worked example
core = core.replace('href="#mk-', 'href="#mk-')
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a> · <a href="/discoveries/">Discoveries</a> · <a href="/lore/">Lore and legends</a></p>
    <p class="kicker">How we mark the evidence</p>
    <h1>Scrollmarks™</h1>
    <p class="lede">Not every source is worth the same. A death certificate filed the week a man died is not a story his grandson told sixty years later, and neither of them is our own opinion. Scrollmarks are the nine marks Project Scroll puts on every statement in its research, strongest first, so you can see at a glance what the record says and what we are arguing from it.</p>
    <div class="sm-page">{core}</div>
    <h2>Scrollmarks in our news stories</h2>
    <p>A news story is shorter than a research report, so its statements carry four marks, which fold the nine together: <span class="nw-tier d">Documented</span> for anything a record says (a document, a period print, a county history or a compiled source, named in the text), <span class="nw-tier r">Reading</span> for our interpretation, <span class="nw-tier o">Open</span> for what is not yet known, and <span class="nw-tier n">New finding</span> for something we found in the record that no earlier telling mentions. Every new finding is also listed on the <a href="/discoveries/">Discoveries</a> page, with the kind of finding it is.</p>
    <h2>Using Scrollmarks</h2>
    <p>The name Scrollmarks, the badges and the wording of these definitions are Project Scroll’s own. To use them in a publication, write to <a href="mailto:research@projectscroll.com?subject=Scrollmarks">research@projectscroll.com</a>.</p>
    <p class="ctas"><a class="btn primary" href="/notes/one-letter-two-certificates/">See them at work: One Letter, Two Certificates</a> <a class="btn" href="/#services">Bring us your mystery</a></p>
'''
page('scrollmarks/index.html', 'Scrollmarks: how we mark the evidence · Project Scroll', 'Scrollmarks are the nine marks Project Scroll puts on every statement in its research, from Document to Hypothesis, so readers can see what the record says and what is argued from it.', body)
print('scrollmarks built')
