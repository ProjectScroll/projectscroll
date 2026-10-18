import os,re
def smart(t):
    t=re.sub(r"(\w)'(\w)",r"\1’\2",t)
    t=re.sub(r"(\s|^|\(|—)'",r"\1‘",t)
    t=t.replace("'","’")
    t=re.sub(r'(^|[\s(—\[])"',r'\1“',t)
    t=t.replace('"','”')
    return t
def proc(html):
    out=[];i=0
    for m in re.finditer(r'<(script|style|pre)\b.*?</\1>|<!--.*?-->|<[^>]+>',html,re.S):
        out.append(smart(html[i:m.start()])); out.append(m.group(0)); i=m.end()
    out.append(smart(html[i:])); return ''.join(out)
import pathlib
R=str(pathlib.Path(__file__).resolve().parent.parent)
def page(path, title, desc, body, canon=None, noindex=False, og='https://projectscroll.com/og.png'):
    canon = canon or 'https://projectscroll.com/'+path.replace('index.html','')
    head=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{canon}">'}
<meta name="theme-color" content="#E8ECE6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#151B21" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Project Scroll">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/icons/icon-32.png" type="image/png" sizes="32x32">
<link rel="alternate icon" href="/favicon.ico" sizes="16x16 32x32 48x48">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="Project Scroll field notes" href="/feed.xml">
<link rel="preload" href="/fonts/libre-caslon-display-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<script>try{{var t=localStorage.getItem('ps-theme'); if(t) document.documentElement.dataset.theme=t;}}catch(e){{}}</script>
<link rel="stylesheet" href="/site.css?v=37">
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
<header class="bar">
  <div class="bar-in">
    <a class="mark" href="/" aria-label="Project Scroll home">
      <svg viewBox="0 0 32 32" aria-hidden="true"><rect x="7" y="4" width="18" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M11 4v24" stroke="#B3362B" stroke-width="2"/><path d="M14 11h7M14 15h7M14 19h5" stroke="currentColor" stroke-width="1.6"/></svg>
      Project Scroll
    </a>
    <nav aria-label="Sections" id="sitenav">
      <a href="/#hunt">Hunt</a><a href="/#cases">Cases</a><a href="/#services">Research</a><a href="/notes/">Field notes</a><a href="/#contact">Contact</a>
    </nav>
    <button class="searchbtn" type="button" id="searchBtn" aria-label="Search the site" aria-haspopup="dialog"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
    <button class="menu" type="button" id="menu" aria-expanded="false" aria-controls="sitenav">Menu</button>
    <button class="theme" type="button" aria-label="Switch between light and dark" id="theme">Dark</button>
  </div>
</header>
<dialog class="search" id="searchDlg" aria-label="Search the site">
  <form method="dialog" class="search-in" onsubmit="return false"><input type="search" id="searchQ" placeholder="Search cases, field notes, guides…" autocomplete="off" aria-label="Search"><button type="button" class="linkbtn" id="searchClose">Close</button></form>
  <ol class="search-res" id="searchRes" aria-live="polite"></ol>
  <p class="note search-tip">Tip: press <kbd>/</kbd> anywhere to search.</p>
</dialog>
<div class="sheet" id="top">
  <main id="main" class="page">
'''
    foot='''  </main>
  <footer class="site">
    <div>
      <p class="motto">Every clue is true. Every answer is in the record.</p>
      <a class="fbfollow" href="https://www.facebook.com/projectscroll/" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.8 1.4-3.8 3.9v2.3H7.9v3h2.6V21z"/></svg>Follow the hunt on Facebook</a>
      <p>Project Scroll is independent historical research. Some mysteries open in an afternoon. Some take a season.</p>
    </div>
    <nav aria-label="Footer">
      <a href="/">Home</a><a href="/#cases">Case board</a><a href="/notes/">Field notes</a><a href="/map/">Map room</a><a href="/toolkit/">Toolkit</a><a href="/notes/book/">Book of notes</a><a href="/families/">Family histories</a><a href="/legends/">Family legends</a><a href="/records/">Where the records are</a><a href="/glossary/">Glossary</a><a href="/about/">About</a><a href="/privacy/">Privacy</a><a href="/guide/death-certificate/">Certificate guide</a><a href="/worksheet/project-scroll-hunters-worksheet.pdf">Hunter's worksheet</a><a href="/sample/project-scroll-sample-report.pdf">Sample report</a><a href="/#contact">Contact</a><a href="https://www.facebook.com/projectscroll/">Facebook</a>
    </nav>
    <p class="fine">© 2026 Project Scroll · <a href="#top">Back to the top</a> · <button type="button" class="lanternbtn" id="lanternBtn" hidden>Put out the lantern</button></p>
  </footer>
</div>
<script src="/site.js?v=37" defer></script>
</body>
</html>
'''
    full=os.path.join(R,path); os.makedirs(os.path.dirname(full),exist_ok=True)
    open(full,'w').write(proc(head+body+foot))

if __name__=='__main__':
    page('notes/one-letter-two-certificates/index.html',
     'One Letter, Two Certificates · Project Scroll field notes',
     'A pioneer, his son, two death certificates and one middle initial: what to do when old records disagree.',
    '''    <p class="crumb"><a href="/notes/">← All field notes</a></p>
        <p class="kicker">Field notes · No. 1 · 17 October 2026</p>
        <h1>One Letter, Two Certificates</h1>
        <p class="lede" style="font-size:1.2rem">One letter. That's all it was. A single middle initial, and it nearly turned one man into two.</p>

        <h2>The case</h2>
        <p>A pioneer died in Michigan in 1912. The old county histories give him a plain first and last name. One of them adds "Senior." <a class="mk sm kC" href="/#mk-county-history" title="What this mark means">County history</a></p>
        <p>His own death certificate, filed about a month after he died, gives the same plain name. No initial at all. <a class="mk sm kD" href="/#mk-document" title="What this mark means">Document</a></p>
        <p>Then we found his son's death certificate, from 1935. In the box for the father's name, whoever answered the questions gave him a middle initial: the same one the son carried. <a class="mk sm kD" href="/#mk-document" title="What this mark means">Document</a></p>
        <p>So which is right? Make your guess now. Ours is further down.</p>

        <h2>Then it got stranger</h2>
        <p>Once we started comparing every box, the records kept arguing.</p>
        <ul class="dis">
          <li><b>His birthday:</b> his death certificate and one of the county histories are two days apart.</li>
          <li><b>His father's birthplace:</b> the certificate names one state. That same history names another.</li>
        </ul>
        <p>One man, one family and three disagreements. Nobody lied. Each one is somebody's memory.</p>

        <h2>What this teaches</h2>
        <p><b>Every record was written by someone.</b> A death certificate tells you what the informant believed, on a hard day. Their name is usually on it. The father's was filed about a month after he died; the son's was filled in twenty-three years later, by someone remembering a man long gone. County histories have the same weakness: the family usually supplied the facts, often from memory, and nobody checked them.</p>
        <p><b>One letter can change everything.</b> Fathers and sons with the same name get tangled in the record all the time. One wrong initial can merge two men or split one, and send you chasing somebody else's family for a month.</p>
        <p><b>Watch out for "Senior."</b> In the 1800s it didn't always mean "father." Sometimes it only meant the older of two men with the same name in town, related or not. Here a son with the same name does turn up, so the label fits, but always check.</p>
        <p><b>Disagreement is a clue, not a failure.</b> Every mismatch tells you who was remembering, and when. Our guess, as promised: father and son shared a name, and in 1935 someone gave the father the son's initial too <a class="mk sm kR" href="/#mk-reading" title="What this mark means">Reading</a>. But a guess is not proof.</p>

        <h2>Four rules for when records disagree</h2>
        <ol class="notes" style="padding-left:1.3rem">
          <li>Ask who gave the information, and when. Closer to the event usually weighs more, but not always.</li>
          <li>Keep looking. A third, independent record can tip the balance, but records are weighed, not counted.</li>
          <li>Write down both versions and where each came from. Never quietly "fix" one.</li>
          <li>Call it settled only when the evidence settles it. Until then, it's an open question.</li>
        </ol>

        <h2>Where the case stands</h2>
        <p><span class="status">Open</span> Our next witness: a local newspaper notice from the days or weeks after his death. Then his probate file, and the cemetery's burial records or a transcription of his stone. Read the stone on paper. Don't go to it.</p>

        <p class="mstrip"><i>Marks, strongest first:</i> <span class="tD">Document</span> <span class="tP">Period print</span> <span class="tC">County history</span> <span class="tM">Compiled</span> <span class="tT">Tradition</span> <span class="tI">Inference</span> <span class="tR">Reading</span> <span class="tH">Hypothesis</span> <span class="tF">Field (our own survey)</span> <i>— <a href="/#marks">what the marks mean</a></i></p>

        <h2>Where to look, for free</h2>
        <ul class="dis">
          <li><a href="https://michigan.access.preservica.com/death-certificates-1897-1952/">Archives of Michigan, death certificates 1897–1952</a>. Free; for most years you can open the certificate itself, in the original handwriting.</li>
          <li><a href="https://www.familysearch.org">FamilySearch</a>. Birth, marriage and death records from all over the world, free with an account.</li>
          <li><a href="https://www.freebmd.org.uk">FreeBMD</a>. A free index of births, marriages and deaths in England and Wales from 1837; copies can be ordered from the <a href="https://www.gov.uk/order-copy-birth-death-marriage-certificate">General Register Office</a>, for a fee.</li>
          <li><a href="https://www.findagrave.com">Find a Grave</a>. Free transcriptions and photographs of gravestones. Read the stone on paper.</li>
        </ul>
        <p><b>Tip:</b> read every box, including the small print at the bottom. Ages are often given to the day, in years, months and days. Count back from the date of death and you have a birth date to check against everything else. Just remember the informant gave that age too.</p>
        <p><a class="btn dl" href="/worksheet/project-scroll-hunters-worksheet.pdf" download><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12m0 0-5-5m5 5 5-5M4 20h16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>The hunter's worksheet (PDF)</a></p>

        <h2>Your turn</h2>
        <p>Pick someone in your family who died long ago. Find two records that name them and compare every box: name, dates, parents, birthplaces. Do they disagree? Which would you believe, and why? The best mysteries start at home.</p>
        <p>Want to test yourself first? <a href="/#try">Try the two-record puzzle</a>. Got a mystery you can't crack? <a href="https://m.me/projectscroll">Message us on Facebook</a>, or see <a href="/#contact">how to start</a>. Tell us how you did in the comments on <a href="https://www.facebook.com/projectscroll/">Project Scroll's page</a>.</p>
    ''', og='https://projectscroll.com/og/one-letter.jpg')

    page('notes/index.html','Field notes · Project Scroll',
     'Lessons from the Project Scroll research desk: how to read old records, weigh them against each other and know when a question is settled.',
    '''    <p class="kicker">From the desk</p>
        <h1>Field notes</h1>
        <p>Short lessons from real cases: how to read an old record, weigh it against another, and know when a question is settled. A new one is added each time one is posted.</p>
        <p><a class="btn" href="/notes/book/">Open the field notes as a book</a></p>
    <ul class="notelist">
          <li><a href="/notes/one-letter-two-certificates/">One Letter, Two Certificates</a><span>No. 1 · 17 October 2026 · What to do when two old records tell you two different things.</span></li>
        </ul>
        <p><a class="btn dl" href="/worksheet/project-scroll-hunters-worksheet.pdf" download><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12m0 0-5-5m5 5 5-5M4 20h16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>The hunter's worksheet (PDF)</a></p>
    ''', og='https://projectscroll.com/og/notes.jpg')

    page('404.html','Not in the record · Project Scroll','This page is not in the record.',
    '''    <p class="kicker">Error 404</p>
        <h1>Not in the record.</h1>
        <p class="lede" style="font-size:1.2rem">We searched the index, the margins and the back pages. This page isn't here.</p>
        <p>It may have moved, or it may never have existed. A good record-keeper is honest about both.</p>
        <p class="ctas" style="margin-top:1.6rem"><a class="btn primary" href="/">Back to the first page</a><a class="btn" href="/#cases">See the case board</a></p>
    ''', noindex=True)
    print('pages written')
