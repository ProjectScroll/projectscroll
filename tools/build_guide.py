"""Builds the interactive 'How to read a death certificate' guide:  python3 tools/build_guide.py"""
import sys, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E=html.escape
# (number, label, x, y, w, h  [in a 1000x1300 form], who filled it, mark class, mark name, what it tells you, how far to trust it)
F=[
 (1,'Place of death',40,150,600,80,'The registrar or physician','kD','Document','The township, village or city, and often the street address or institution.','Strong: written down at the time, by someone whose job it was.'),
 (2,'Registered no.',660,150,300,80,'The local registrar','kD','Document','The certificate’s own number in the local register: your key for ordering a copy or finding it again.','Strong.'),
 (3,'Full name',40,250,920,80,'The informant','kD','Document','The name as the family gave it. Watch for initials, nicknames and spellings that differ from other records.','Good, but it is the informant’s version of the name.'),
 (4,'Sex · race · marital status',40,350,450,80,'The informant','kD','Document','Personal particulars as the informant described them. Married, widowed or single can point you to a spouse.','Usually right; check against the census.'),
 (5,'Date of birth',510,350,450,80,'The informant','kD','Document','The day the family believed the person was born.','Medium: remembered, sometimes decades later. Compare with the age box.'),
 (6,'Age: years, months, days',40,450,450,80,'The informant','kD','Document','Age to the day. Count back from the date of death and you have a birth date to test against everything else.','Medium: arithmetic mistakes and guesses are common.'),
 (7,'Occupation',510,450,450,80,'The informant','kD','Document','What the person did for a living. It can tie them to a trade directory, a union or a business.','Good.'),
 (8,'Birthplace',40,550,920,80,'The informant','kD','Document','State or country of birth. A lead to the census, to immigration records and to the family before they came.','Medium: often just a state or “Germany”.'),
 (9,'Father’s name and birthplace',40,650,920,90,'The informant','kD','Document','The parents’ names: often the only record that links one generation to the one before.','The weakest part of the form: the informant may never have met them. Treat it as a lead to prove.'),
 (10,'Mother’s maiden name and birthplace',40,760,920,90,'The informant','kD','Document','The mother’s family name before marriage, which opens a whole new line.','Weak in the same way; maiden names are often misremembered or left blank.'),
 (11,'Informant',40,870,920,80,'Signed by the informant','kD','Document','Who answered the questions, and often their address. A spouse or child was close; a neighbor or the undertaker was not.','The single most important box: it tells you how far to trust boxes 3 to 10.'),
 (12,'Date of death',40,970,450,80,'The physician','kD','Document','The day, and sometimes the hour, of death.','Strong: recorded at the time.'),
 (13,'Cause of death',510,970,450,160,'The physician or coroner','kD','Document','The medical cause and how long the illness lasted, in the language of its day: “dropsy”, “consumption”, “old age”.','Strong for the date; the medicine is of its time.'),
 (14,'Physician’s signature',40,1070,450,60,'The physician','kD','Document','Who attended. Their own papers or obituary can add detail.','Strong.'),
 (15,'Burial: place and date',40,1150,450,100,'The undertaker','kD','Document','The cemetery, the date of burial and sometimes removal to another town. Your route to the grave records, on paper.','Good. Read the stone on paper; there is no need to visit it.'),
 (16,'Undertaker · filed date',510,1150,450,100,'The undertaker and registrar','kD','Document','The funeral home and the day the certificate was filed. Funeral-home ledgers sometimes survive with more detail.','Strong. The filing date shows how soon after the death the form was made.'),
]
svg=['<svg viewBox="0 0 1000 1300" class="cert-svg" role="img" aria-label="A blank certificate of death, drawn as a guide"><rect x="10" y="10" width="980" height="1280" rx="6" class="paper"/><rect x="24" y="24" width="952" height="1252" rx="3" class="frame"/>',
     '<text x="500" y="78" class="t1">CERTIFICATE OF DEATH</text><text x="500" y="112" class="t2">State of ———— · Department of State · Division of Vital Statistics</text>']
for n,l,x,y,w,h,*_ in F:
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="box"/><text x="{x+12}" y="{y+24}" class="lbl">{E(l.upper())}</text><path d="M{x+12} {y+h-16} h{w-24}" class="line"/>')
svg.append('<text x="500" y="1275" class="t3">A generic form drawn for this guide. Real certificates vary by state and year.</text></svg>')
spots=''.join(f'<button type="button" class="spot" style="left:{(x+w-34)/10}%;top:{(y+10)/13}%" data-i="{i}" aria-label="Box {n}: {E(l)}">{n}</button>' for i,(n,l,x,y,w,h,*_) in enumerate(F))
items=''.join(f'<li><button type="button" data-i="{i}"><span class="num">{n}</span>{E(l)}</button></li>' for i,(n,l,*_) in enumerate(F))
data=[{'n':n,'l':l,'who':who,'k':k,'m':m,'what':what,'trust':trust} for n,l,x,y,w,h,who,k,m,what,trust in F]
import json
body=f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">A guide from the desk</p>
    <h1>How to read a death certificate</h1>
    <p class="lede" style="font-size:1.15rem">A death certificate is two records in one. The doctor wrote down the death, at the time. Someone else, the informant, answered questions about a whole life, on the hardest day. Tap any numbered box to see who filled it in, and how far to trust it.</p>
    <div class="guide">
      <div class="cert-wrap">{''.join(svg)}{spots}</div>
      <aside class="panel" id="panel" aria-live="polite">
        <p class="panel-k">Box <span id="pn">11</span></p><h2 id="pl">Informant</h2>
        <p><b>Filled in by:</b> <span id="pw"></span></p>
        <p id="pwhat"></p><p class="trust"><b>How far to trust it:</b> <span id="ptrust"></span></p>
        <p class="panel-nav"><button type="button" class="btn" id="prev">‹ Previous</button><button type="button" class="btn" id="next">Next ›</button></p>
      </aside>
    </div>
    <h2>Every box, in order</h2>
    <ol class="boxlist">{items}</ol>
    <h2>The rule of thumb</h2>
    <p>The top half (boxes 3 to 10) is <b>memory</b>: what the informant believed about a life. The bottom half (boxes 12 to 16) is <b>the event</b>: written by people who were there that week. When the two halves disagree with other records, trust the bottom half first, and weigh the top half by who the informant was.</p>
    <p class="remember"><b>Remember:</b> the dead person was never the informant. Everything in the top half is someone else’s memory, given on the hardest day, so find the informant’s name on the certificate and ask how well they knew the life they were describing.</p>
    <p>Michigan’s certificates from 1897 to 1952 are free to view at the <a href="https://michigan.access.preservica.com/death-certificates-1897-1952/">Archives of Michigan</a>. Elsewhere, try <a href="https://www.familysearch.org">FamilySearch</a> or your state archives.</p>
    <p class="ctas" style="margin-top:1.2rem"><a class="btn primary" href="/notes/one-letter-two-certificates/">See it in a real case</a><a class="btn" href="/worksheet/project-scroll-hunters-worksheet.pdf">Hunter’s worksheet (PDF)</a></p>
    <script type="application/json" id="gdata">{json.dumps(data,ensure_ascii=False)}</script>
    <script>
    (function(){{ var D=JSON.parse(document.getElementById('gdata').textContent), cur=10;
      var show=function(i){{ cur=(i+D.length)%D.length; var d=D[cur];
        document.getElementById('pn').textContent=d.n; document.getElementById('pl').textContent=d.l; document.getElementById('pw').textContent=d.who;
        document.getElementById('pwhat').textContent=d.what; document.getElementById('ptrust').textContent=d.trust;
        document.querySelectorAll('[data-i]').forEach(function(b){{ b.setAttribute('aria-pressed', +b.dataset.i===cur?'true':'false'); }}); }};
      document.querySelectorAll('[data-i]').forEach(function(b){{ b.addEventListener('click', function(){{ show(+b.dataset.i); if (b.closest('.boxlist') && innerWidth<900) document.getElementById('panel').scrollIntoView({{block:'nearest'}}); }}); }});
      document.getElementById('prev').addEventListener('click', function(){{ show(cur-1); }}); document.getElementById('next').addEventListener('click', function(){{ show(cur+1); }});
      show(10); }})();
    </script>
'''
page('guide/death-certificate/index.html','How to read a death certificate · Project Scroll','An interactive guide: tap each box of a death certificate to see who filled it in and how far to trust it.',body, og='https://projectscroll.com/og/death-certificate.jpg')
print('guide built')
