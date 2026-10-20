"""Builds a page and a share card for every case, the solver keepsake page, and syncs the case board.
Source of truth: cases.json. Run:  python3 _tools/build_cases.py   (then node _tools/cards.js to draw the share cards)"""
import json, re, html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pages import page, R
D=json.load(open(f'{R}/cases.json')); C=D['cases']; FB='https://www.facebook.com/projectscroll/'; HALLFB='https://www.facebook.com/comparativeovations/'
esc=html.escape
for c in C:
    n=c['n']; solved=c.get('solved')
    status=f'<span class="status solved">Solved</span> Cracked by {esc(solved)}' + (f' on {esc(c["solvedOn"])}' if c.get('solvedOn') else '') if solved else ('<span class="status">Practice</span> Nobody has settled it yet, including the desk. Bring the next witness, a newspaper notice or the probate file, with its page, and you are the first name on the board.' if n==10 else '<span class="status">Open</span> Nobody has cracked it yet.')
    hint=f'<h2>A hint</h2><p>{esc(c["hint"])}</p>' if c.get('hint') else ''
    keep=f'<p><a class="btn" href="/keepsake/?case={n}">Solver’s keepsake</a></p>' if solved else ''
    extra='<p><a href="/notes/one-letter-two-certificates/">Read the full case in the field notes</a>.</p>' if n==10 else ''
    fp=c.get('frompost'); frompost=''
    if fp and c.get('post'):
        pics=''.join(f'<figure><picture><source type="image/webp" srcset="{x["src"]}{"-700" if "/pages/" in x["src"] else ""}.webp"><img src="{x["src"]}{"-700" if "/pages/" in x["src"] else ""}.jpg" width="{x["w"]}" height="{x["h"]}" {"loading=\"lazy\"" if k else "fetchpriority=\"high\""} decoding="async" alt="{esc(x["alt"])}"></picture><figcaption>{x["cap"]}</figcaption></figure>' for k,x in enumerate(fp['photos']))
        frompost=f'''    <section class="frompost" aria-labelledby="fp{n}">
      <h2 id="fp{n}">From the post</h2>
      <p class="fp-lead">“{esc(fp['lead'])}” <a href="{esc(c['post'])}">Read the whole post on Facebook ›</a></p>
      <div class="fp-pics n{len(fp['photos'])}">{pics}</div>
      <div class="fp-live" id="fplive{n}" data-post="{esc(c['post'])}">
        <button type="button" class="btn" id="fpload{n}">Show the live post, with its likes and comments</button>
        <p class="note">Loads from Facebook only when you ask. <a href="/privacy/">What this site keeps.</a></p>
      </div>
    </section>
'''
    if c.get('start'):
        items=''.join(f'<li>{x["text"]} <a href="{esc(x["url"])}">{esc(x.get("label","Read it free online ›"))}</a></li>' for x in c['start'])
        starthere=f'<aside class="starthere" aria-labelledby="sh{n}"><h2 id="sh{n}">Start here</h2><ol>{items}</ol><p class="note">These are the first pages to open. The answer is in the record; the rest of the trail is yours.</p></aside>'
    elif c['hall']=='h2':
        starthere=f'<aside class="starthere" aria-labelledby="sh{n}"><h2 id="sh{n}">Start here</h2><p>This case belongs to the second hall. Its sources are posted on the hall’s own page, and that page is behind the first hall’s last door. Find the door, and the trail starts there.</p></aside>'
    else: starthere=''
    first=('Find the door first. This case’s sources are behind the first hall’s last case: solve that, and the trail opens.' if c['hall']=='h2' and not c.get('start') else 'Open the first source in “Start here” and read the whole passage, not only the lines that seem to answer. Copy out every name, date and place in it.')
    ladder=f'''<aside class="hintladder" data-case="{n}" aria-labelledby="hl{n}"><h2 id="hl{n}">Stuck? Three ways in</h2><p class="note">Open them one at a time, only as far as you need. They teach the method, not the answer.</p><ol>
      <li hidden><b>Read slowly.</b> {first}</li>
      <li hidden><b>Every name is a lead.</b> Look each person up in a second kind of record: a census, a deed index, a plat map, a cemetery list. Where two records made by different people agree, you are on firm ground.</li>
      <li hidden><b>Ask what the writer could not know.</b> A county history is a memory, written years later. Find a record made at the time, a newspaper, a plat, a certificate, and test the story against it. The answer is usually where the two disagree.</li>
    </ol><p><button type="button" class="btn hl-next">Show a way in</button> <span class="hl-n" aria-live="polite"></span></p></aside>'''
    body=f'''    <p class="crumb"><a href="/#cases">← The case board</a></p>
    <p class="kicker">Case {n} · {esc(c['hallName'])}</p>
    <h1 style="view-transition-name:case-{c['n']}">{esc(c['question'])}</h1>
    <p class="casestatus">{status}</p>
    <p class="note">Opened {esc(c['opened'])}.</p>
    {starthere}{frompost}{hint}{ladder}{extra}
    <h2>How to answer</h2>
    <ol class="steps">
      <li><b>Search the record.</b> {'The first sources are on the second hall’s page, behind the first hall’s last door; then follow where they lead:' if c['hall']=='h2' else 'Start with the “Start here” box above, then follow where it leads:'} old county histories, maps, certificates and newspapers, many of them free online.</li>
      <li><b>Post your answer</b> in the comments on <a href="{FB}">Project Scroll’s Facebook page</a>, and say exactly where you found it: the book or record, the page, and a link if there is one.</li>
      <li><b>Get named.</b> The first solver with the page to prove it is named in the next post and on the case board.</li>
    </ol>
    <div class="solvedbox"><h3>What counts as solved</h3><p>A case is solved when an answer is posted with the record it came from: the book or document, the page, and a link if there is one. The desk checks the page. If it says what you say it says, your name goes on the board, the case is marked Solved with your source beside it, and the next post names you. An answer without the page stays a guess, however right it is.</p></div>
    <p class="goodanswer"><b>A good answer looks like this:</b> “Case {n}: [your answer]. Found in [the book or record], p. [page], [link].” Use <b>Copy as a Facebook answer</b> in your notebook below, and it is laid out for you.</p>
    <p class="note">Everything is solved on paper. Never dig, never go near a grave, and never set foot on anyone’s land.</p>
    <p class="casekeep no-print"><button type="button" class="btn" id="saveOff" hidden>Save this case for offline</button><button type="button" class="btn" id="printCase">Print this case</button><span class="copied" id="saveOffMsg" aria-live="polite"></span></p>
    <p class="casetools"><span>Tools for the hunt:</span> <a href="/records/">Where the records are</a> <a href="/glossary/">The glossary</a> <a href="/toolkit/">The toolkit</a> <a href="/guide/old-handwriting/">Reading the old hand</a> <a href="/worksheet/project-scroll-hunters-worksheet.pdf">The hunter’s worksheet (PDF)</a></p>
    <div class="notebook" id="casenote" data-case="{n}">
      <h2>Your notebook for this case</h2>
      <p class="note">Jot down what you find and where. It is saved only on this device, and nobody else can see it. <a href="/notebook/">All your notes</a></p>
      <label for="noteText" class="vh">Your notes for this case</label>
      <textarea id="noteText" rows="7" placeholder="Record · where I found it (book, page, link) · what it says"></textarea>
      <p class="nbbtns"><button type="button" class="btn" id="noteCopy">Copy as a Facebook answer</button><button type="button" class="btn" id="noteSave">Download as a text file</button><span class="copied" id="noteOut" aria-live="polite"></span></p>
    </div>
    {keep}
    <p class="ctas" style="margin-top:1.4rem"><a class="btn primary" href="{c.get('post') or (HALLFB if c['hall']=='h1' else FB)}">{'Read the post on Facebook' if c.get('post') else 'Start on Facebook'}</a><a class="btn" href="/#cases">All cases</a><button type="button" class="btn" id="sharecase">Share this case</button></p>
    <p class="copied" id="shareout" aria-live="polite"></p>
    <script>document.getElementById('sharecase').addEventListener('click',function(){{var u=location.href.split('#')[0],t=document.title;if(navigator.share){{navigator.share({{title:t,url:u}}).catch(function(){{}});}}else if(navigator.clipboard){{navigator.clipboard.writeText(u).then(function(){{document.getElementById('shareout').textContent='Link copied.';}},function(){{document.getElementById('shareout').textContent=u;}});}}}});</script>
'''
    page(f'cases/{n}/index.html', (lambda q: f'Case {n}: {q} · Project Scroll' if len(q)<=50 else f'Case {n}: {q[:47].rsplit(" ",1)[0]}… · Project Scroll')(c['question'].split('?')[0].strip()+('?' if '?' in c['question'] else '')), (c['question']+' An open case in the Project Scroll history hunt, '+c['hallName'].split(' · ')[0].lower()+': the first sources to open, free online, and how to post an answer.')[:160].rsplit(' ',1)[0] if len(c['question'])<120 else c['question'][:157]+'…', body, og=f'https://projectscroll.com/cases/{n}/card.jpg')
    # card source for the drawing script
pathlib.Path(f'{R}/_tools/cards.json').write_text(json.dumps(C, ensure_ascii=False))

# keepsake page (reads cases.json in the browser; shows a certificate only for a solved case)
kbody='''    <p class="crumb no-print"><a href="/#cases">← The case board</a></p>
    <div id="keep"><p class="kicker">Solver’s keepsake</p><h1>No case cracked yet</h1><p>When one is, its solver’s name goes on a keepsake here, ready to print. Could the first one be yours? Choose a solved case on <a href="/#cases">the case board</a>.</p></div>
    <p class="center no-print" id="keepbtns" hidden><button type="button" class="btn primary" id="keepPrint">Print or save as PDF</button></p>
    <script>
    (function(){ var n=+new URLSearchParams(location.search).get('case'); if(!n) return;
      fetch('/cases.json',{cache:'no-store'}).then(function(r){return r.json()}).then(function(d){
        var c=d.cases.filter(function(x){return x.n===n})[0]; if(!c||!c.solved) return;
        var k=document.getElementById('keep'); k.className='cert'; k.innerHTML='';
        var add=function(tag,cls,txt){var e=document.createElement(tag); if(cls)e.className=cls; e.textContent=txt; k.appendChild(e); return e;};
        add('p','cert-k','Project Scroll'); add('p','cert-s','This keepsake records that'); add('p','cert-name',c.solved);
        add('p','cert-s','was named by Project Scroll as the solver of'); add('p','cert-case','Case '+c.n+': '+c.question);
        add('p','cert-d',(c.solvedOn?c.solvedOn+' · ':'')+c.hallName); add('p','cert-motto','Every clue is true. Every answer is in the record.');
        add('p','cert-note','A keepsake, not an official record. The case board at projectscroll.com is the record of who solved what.');
        document.getElementById('keepbtns').hidden=false; document.title='Keepsake · Case '+c.n+' · '+c.solved; if(window.psEarn) window.psEarn('solver'); });
    })();
    </script>
'''
page('keepsake/index.html','Solver’s keepsake · Project Scroll','A keepsake for solvers of Project Scroll cases.',kbody,noindex=True)

# sync the case board on the home page
p=f'{R}/index.html'; s=open(p).read()
for c in C:
    attrs=f' data-hall="{c["hall"]}"'+(f' data-touched="{esc(c["touched"])}"' if c.get('touched') else '')+(f' data-solved="{esc(c["solved"])}"' if c.get('solved') else '')+(f' data-hint="{esc(c["hint"])}"' if c.get('hint') else '')
    s=re.sub(rf'<tr id="case-{c["n"]}" data-hall="\w+"[^>]*>', f'<tr id="case-{c["n"]}"{attrs}>', s)
    # question text links to its page
    s=re.sub(rf'(<tr id="case-{c["n"]}"[^>]*><td class="no">{c["n"]}</td><td>)(?!<a class="qlink")(.*?)(?=( <a href="/notes/|<span class="tools"|</td>))', lambda m: m.group(1)+f'<a class="qlink" href="/cases/{c["n"]}/" style="view-transition-name:case-{c["n"]}">'+m.group(2).strip()+'</a>', s, count=1, flags=re.S)
s=re.sub(r'<caption>Last updated [^<]*</caption>', f'<caption>Last updated {D["updated_text"] if "updated_text" in D else "18 October 2026"}.</caption>', s)
open(p,'w').write(s)
print('built', len(C), 'case pages')
