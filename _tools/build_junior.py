"""The junior hunt and the classroom page.  python3 _tools/build_junior.py"""
import sys, pathlib, html, re; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E=html.escape
def h(w):
    x=5381
    for c in w: x=((x*33)&0xffffffff)^ord(c)
    return x
norm=lambda s: re.sub(r'[^a-z0-9]','',s.lower())
Q=[
 ('How many hotels are listed in the 1860 Cassopolis directory?', ['2','two'], '<a href="/names/?town=cassopolis">Who was in Cassopolis</a>', 'Count the entries under “Hotels”.'),
 ('H. B. Shurter of Cassopolis printed a newspaper. What was it called?', ['nationaldemocrat','thenationaldemocrat'], '<a href="/names/?q=Shurter">Search the roll for Shurter</a>', 'Look at what is written after his name.'),
 ('What did A. B. Culver of Paw Paw make?', ['guns','gun','gunsmith','agunsmith','firearms','rifles'], '<a href="/names/?town=paw-paw">Who was in Paw Paw</a>', 'His trade is written beside his name.'),
 ('G. A. Colby of Dowagiac ran a mill. What was it called?', ['herndonmills','herndonmill','herndon'], '<a href="/names/?q=Colby">Search the roll for Colby</a>', 'Then find the mill at the bottom of the Dowagiac plan.'),
 ('Name one of the flouring mills in the 1860 Niles directory.', ['industrial','dakota','depot','volant'], '<a href="/names/?q=mill&amp;town=niles">Mills in Niles</a>', 'They had names, in quotation marks.'),
 ('On the 1861 plan of Goshen, what building stands in the square between Third and Main?', ['courthouse','thecourthouse','countycourthouse'], '<a href="/map/goshen/">Goshen, 1861 and today</a>', 'It has a cross-shaped roof. Zoom in.'),
 ('Who was the Post Master of Paw Paw in 1860?', ['ajsortore','sortore','asortore'], '<a href="/names/?town=paw-paw">Who was in Paw Paw</a>', 'Look under “Miscellaneous”.'),
]
items=''.join(f'''      <li class="jq" data-h="{','.join(str(h(a)) for a in acc)}"><p class="jq-q">{E(q)}</p><p class="jq-where">Look here: {where}. <span class="jq-tip">{E(tip)}</span></p>
        <form class="jq-f" autocomplete="off"><label class="vh" for="jq{i}">Your answer</label><input id="jq{i}" type="text" maxlength="40" spellcheck="false"><button class="btn" type="submit">Check</button></form><p class="jq-out" aria-live="polite"></p></li>
''' for i,(q,acc,where,tip) in enumerate(Q))
body=f'''    <p class="crumb"><a href="/#hunt">← The hunt</a></p>
    <p class="kicker">The junior hunt</p>
    <h1>Junior surveyors</h1>
    <p class="lede" style="font-size:1.15rem">Seven questions for young hunters and their families. Every answer is on an old map or in an old directory, and every question tells you where to look. Find all seven and earn the Junior surveyor badge.</p>
    <p class="jtally" id="jTally" aria-live="polite">0 of {len(Q)} found.</p>
    <ol class="junior">
{items}    </ol>
    <p class="note">Grown-ups: there is nothing to buy and nothing to sign up for. Answers are kept only in this browser. For lessons built on the same maps, see <a href="/classrooms/">Project Scroll for classrooms</a>.</p>
    <script>
    (function(){{ var h=function(s){{ var x=5381; for (var i=0;i<s.length;i++){{ x=((Math.imul(x,33))^s.charCodeAt(i))>>>0; }} return x; }};
      var K='ps-junior', got={{}}; try{{ got=JSON.parse(localStorage.getItem(K)||'{{}}')||{{}}; }}catch(e){{}}
      var qs=[].slice.call(document.querySelectorAll('.jq')), tally=document.getElementById('jTally');
      var draw=function(){{ var n=0; qs.forEach(function(li,i){{ if (got[i]){{ n++; li.classList.add('done'); li.querySelector('.jq-out').textContent='Found: '+got[i]+'.'; li.querySelector('input').value=got[i]; }} }}); tally.textContent=n+' of '+qs.length+' found.'+(n===qs.length?' Every one! You are a Junior surveyor.':''); if (n===qs.length && window.psEarn) window.psEarn('junior'); }};
      qs.forEach(function(li,i){{ var H=li.dataset.h.split(',').map(Number), f=li.querySelector('form'), inp=li.querySelector('input'), out=li.querySelector('.jq-out');
        f.addEventListener('submit',function(e){{ e.preventDefault(); var v=inp.value.trim(), n=v.toLowerCase().replace(/[^a-z0-9]/g,''); if (!n) return;
          if (H.indexOf(h(n))>=0){{ got[i]=v; try{{ localStorage.setItem(K,JSON.stringify(got)); }}catch(e){{}} draw(); }} else out.textContent='Not quite. Look again where the question says, and check your spelling.'; }}); }});
      draw(); }})();
    </script>
'''
page('junior/index.html','Junior surveyors · The junior hunt · Project Scroll','Seven questions for young hunters and their families, every answer on an old map or in an old directory of the St. Joseph River Valley, with a badge for finding them all.',body,og='https://projectscroll.com/og/hunt.jpg')
L=[
 ('Then and now','Grades 3 and up · 40 minutes','Map reading, change over time','<a href="/map/then-and-now/">Seven towns, then and now</a>',[
   'Choose a town near your school. Open its page and fade slowly from the old plan to today.',
   'List three things that are still there (a street, a square, a river crossing) and three that are gone.',
   'Find the street that changed its name, using the challenge on the page.',
   'Talk about it: why might a town rename a street? Who decides?'],
  'Walk the street, if you can, with the “Where am I?” button on a phone, and photograph what stands there now.'),
 ('Who was in town','Grades 4 to 8 · 45 minutes','Primary sources as data, graphs','<a href="/names/">Who was in town</a>',[
   'Pick one town’s 1860 or 1861 business directory.',
   'Sort the entries into trades: law, medicine, food, building, transport, making things.',
   'Make a bar graph of the trades. Which town had the most lawyers? The most shoemakers?',
   'Ask: who is missing from a directory that people paid to be listed in? (Most farmers, labourers, women and children.)'],
  'Compare two towns, or a directory of today, and write what changed.'),
 ('This day in the valley','Grades 6 to 12 · 45 minutes','Primary and secondary sources, citation','<a href="/almanac/">The valley’s almanac</a>',[
   'Find the almanac entry nearest to today’s date, or a student’s birthday.',
   'Open the county history page it cites. Read the whole paragraph around the date.',
   'Decide: was the writer there? How many years after the event did they write? Who told them?',
   'Write a one-sentence citation for the source, with book, year and page.'],
  'Look for the same event in a newspaper of the time and compare the two accounts.'),
 ('Weighing the evidence','Grades 6 to 12 · 50 minutes','Evaluating sources, reasoning from evidence','<a href="/guide/gravestones/">Reading gravestones</a> and <a href="/guide/death-certificate/">the death certificate guide</a>',[
   'Read the guide together. List who made a gravestone, a death certificate and a county history, and when.',
   'Give pairs a disagreement: an age on a stone and an age on a certificate that differ by a year.',
   'Each pair decides which to trust and writes why, using the guide’s questions.',
   'Share: what extra record would settle it?'],
  'Play one of the open cases on the case board as a class, and post the class’s answer.'),
]
les=''.join(f'''    <section class="lesson"><h2>{E(t)}</h2><p class="ls-m">{E(g)} · {E(sk)}</p><p><b>You need:</b> {need} and a screen or printed copies.</p><ol>{''.join('<li>'+E(x)+'</li>' for x in steps)}</ol><p><b>Going further:</b> {E(ext)}</p></section>
''' for t,g,sk,need,steps,ext in L)
body2=f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">For teachers</p>
    <h1>Project Scroll for classrooms</h1>
    <p class="lede" style="font-size:1.15rem">Four ready lessons in local history and map reading, built on the real maps, directories and county histories of the St. Joseph River Valley. Free, nothing to sign up for, and nothing collected from students. Print this page and go.</p>
{les}    <h2>Notes for teachers</h2>
    <ul class="dis">
      <li><b>Every source is public domain</b> and credited where it is held. Students can open the original every time.</li>
      <li><b>The junior hunt</b>, seven questions answered from the maps and directories, makes a good warm-up: <a href="/junior/">Junior surveyors</a>.</li>
      <li><b>Nothing to dig, nowhere to trespass.</b> Every answer is in a book, a map or a record. Please teach the same rule on any field trip.</li>
      <li>Ideas, corrections, or a class that solved a case? Write to <a href="mailto:research@projectscroll.com?subject=Classroom">research@projectscroll.com</a>.</li>
    </ul>
'''
body2 = body2.replace('    <h1>Project Scroll for classrooms</h1>', '''    <h1>Project Scroll for classrooms</h1>
    <aside class="follow-box"><p><b>New: the teachers’ pack.</b> A one-day field trip to Cassopolis (the Broadway walk, the Local History Branch and the photo spots), with two printable worksheets: rephotographing an old postcard, and reading an old record. <a class="btn" href="/classrooms/project-scroll-teachers-pack.pdf" download>Download the teachers’ pack (PDF)</a></p></aside>''', 1)

page('classrooms/index.html','Project Scroll for classrooms · Project Scroll','Four free, ready lessons in local history and map reading for grades 3 to 12, built on the real 1860s maps, directories and county histories of the St. Joseph River Valley.',body2,og='https://projectscroll.com/og/hunt.jpg')
print('junior and classrooms built')
