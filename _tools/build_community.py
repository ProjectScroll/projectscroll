"""Valley Voices (readers' stories, Who is this?, Ask the desk) and the corrections page.
python3 _tools/build_community.py   (data: _tools/data/voices.json and corrections.json, both optional)"""
import sys, pathlib, json, html
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E = html.escape
P = pathlib.Path(__file__).parent/'data'
def load(n): f=P/n; return json.load(open(f)) if f.exists() else []
V = load('voices.json')       # [{kind: voice|who|ask, title, text, by, town, date, img, answer, status}]
C = load('corrections.json')  # [{date, page, url, was, now, why}]

def items(kind, empty):
    xs = [v for v in V if v.get('kind')==kind]
    if not xs: return f'<p class="cm-empty">{empty}</p>'
    out = []
    for v in xs:
        img = f'<img src="{E(v["img"])}" alt="{E(v.get("alt") or v["title"])}" loading="lazy" decoding="async">' if v.get('img') else ''
        ans = f'<p class="cm-ans"><b>From the desk:</b> {E(v["answer"])}</p>' if v.get('answer') else ''
        tag = {'record':'Found in the record','memory':'Family memory','open':'Still open'}.get(v.get('status',''), '')
        out.append(f'<article class="cm-it">{img}<p class="mu-k">{E(v.get("town",""))}{" · "+E(v["date"]) if v.get("date") else ""}{" · <span class=cm-tag>"+tag+"</span>" if tag else ""}</p><h3>{E(v["title"])}</h3><p>{E(v.get("text",""))}</p>{ans}<p class="cm-by">{("Shared by "+E(v["by"])) if v.get("by") else "Shared by a reader"}</p></article>')
    return '<div class="cm-list">'+''.join(out)+'</div>'

body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">From the people of the valley</p>
    <h1>Valley Voices</h1>
    <p class="lede">The county histories were written by a few men in a few years. Everything else is still in the valley: a grandmother’s telling, a box of photographs, a face nobody has named in eighty years. This is where readers’ stories, unnamed photographs and questions are published, with their permission, beside what the record says.</p>
    <nav class="cm-nav" aria-label="On this page"><a href="#voices">Readers’ stories</a> · <a href="#who">Who is this?</a> · <a href="#ask">Ask the desk</a></nav>

    <section id="voices" aria-labelledby="cmV"><h2 id="cmV">Readers’ stories</h2>
      <p>Memories of a building, a business, a family or a day the town still talks about. Each one is marked plainly: <b>found in the record</b> when a document bears it out, <b>family memory</b> when it is a story we cannot yet check.</p>
      {items('voice', 'The first stories will appear here. Yours could be one of them.')}
      <p><a class="btn primary" href="/story/#family">Share a story</a></p></section>

    <section id="who" aria-labelledby="cmW"><h2 id="cmW">Who is this?</h2>
      <p>An old photograph with faces nobody has named, or a building nobody can place. We publish the picture, with your permission, and the valley helps put names to it. Every identification is checked against the record before we call it settled.</p>
      {items('who', 'No photographs yet. Send one from a family album or a shoebox at an estate sale; we will publish it here with what is known.')}
      <p><a class="btn primary" href="/story/#who">Send a photograph</a> <a class="btn" href="/news/where-is-this/">Where is this? A place puzzle</a></p></section>

    <section id="ask" aria-labelledby="cmA"><h2 id="cmA">Ask the desk</h2>
      <p>One reader’s question a month, answered from the record: why a road has its name, who built a house, what became of a town, where an ancestor is buried. Answers show their sources, like everything else on the site. If a question needs paid research, we say so and answer what we can for free.</p>
      {items('ask', 'The first question will be answered here. Ask yours.')}
      <p><a class="btn primary" href="/story/#ask">Ask a question</a></p></section>

    <h2>How it works</h2>
    <ul class="dis">
      <li><b>Nothing goes up without your yes.</b> Before anything is published, we send you exactly what would appear.</li>
      <li><b>Your name, or not.</b> You choose whether your name appears.</li>
      <li><b>Living people are protected.</b> We leave out anything private about people still living, and ask before naming anyone in a photograph.</li>
      <li><b>Memory and record stay apart.</b> A family story is never presented as a documented fact until a record shows it.</li>
    </ul>
    <p class="ctas"><a class="btn primary" href="/story/">Share your story</a> <a class="btn" href="/corrections/">Corrections</a></p>
'''
page('voices/index.html', 'Valley Voices · readers’ stories, photographs and questions · Project Scroll',
     'Readers’ stories of the St. Joseph River valley, unnamed old photographs for the valley to identify, and a monthly question answered from the record. Published only with permission.', body,
     og='https://projectscroll.com/og/about.jpg')

rows = ''.join(f'<tr><td>{E(c["date"])}</td><td><a href="{E(c["url"])}">{E(c["page"])}</a></td><td><b>Was:</b> {E(c["was"])}<br><b>Now:</b> {E(c["now"])}{("<br><small>"+E(c["why"])+"</small>") if c.get("why") else ""}</td></tr>' for c in sorted(C, key=lambda c: c['date'], reverse=True))
table = (f'<div class="tblwrap"><table class="cm-tbl"><caption>Corrections, newest first</caption><thead><tr><th scope="col">Date</th><th scope="col">Page</th><th scope="col">What changed</th></tr></thead><tbody>{rows}</tbody></table></div>'
         if C else '<p class="cm-empty">No corrections have been logged yet. When one is made, it will be listed here and noted on the page it changed.</p>')
cbody = f'''    <p class="crumb"><a href="/about/">← About</a></p>
    <p class="kicker">Every clue is true, so every error is fixed in the open</p>
    <h1>Corrections</h1>
    <p class="lede">When we get something wrong, we fix it, note it on the page it changed, and list it here with the date, what it said, what it says now and why. Small fixes of spelling and punctuation are not listed; anything that changes a fact is.</p>
    {table}
    <h2>Found an error?</h2>
    <p>Tell us what is wrong and, if you can, what record shows it. We check it against the source and write back either way.</p>
    <p class="ctas"><a class="btn primary" href="/story/#fix">Send a correction</a> <a class="btn" href="/sources/">The sources shelf</a></p>
'''
page('corrections/index.html', 'Corrections · Project Scroll',
     'Every factual correction made on Project Scroll, with the date, what the page said, what it says now and why.', cbody, og='https://projectscroll.com/og/about.jpg')
print('community pages built', len(V), len(C))
