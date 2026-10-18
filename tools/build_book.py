"""Builds the field notes as a book with turning pages:  python3 tools/build_book.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
P=[
 '<div class="bk-cover"><p class="bk-k">Project Scroll</p><p class="bk-t">Field Notes</p><p class="bk-s">Volume I</p><p class="bk-m">Lessons from the desk</p></div>',
 '<p class="bk-k">No. 1 · 17 October 2026</p><h2>One Letter, Two Certificates</h2><p class="drop">One letter. That’s all it was. A single middle initial, and it nearly turned one man into two.</p>',
 '<h3>The case</h3><p>A pioneer died in Michigan in 1912. The old county histories give him a plain first and last name. One of them adds “Senior.”</p><p>His own death certificate, filed about a month after he died, gives the same plain name. No initial at all.</p>',
 '<p>Then we found his son’s death certificate, from 1935. In the box for the father’s name, whoever answered the questions gave him a middle initial: the same one the son carried.</p><p><i>So which is right?</i></p>',
 '<h3>Then it got stranger</h3><p>His birthday: his death certificate and one of the county histories are two days apart.</p><p>His father’s birthplace: the certificate names one state. That same history names another.</p><p>Nobody lied. Each one is somebody’s memory.</p>',
 '<h3>What this teaches</h3><p>Every record was written by someone. A death certificate tells you what the informant believed, on a hard day.</p><p>One wrong initial can merge two men or split one, and send you chasing somebody else’s family for a month.</p>',
 '<h3>Four rules</h3><ol><li>Ask who gave the information, and when.</li><li>Keep looking. Records are weighed, not counted.</li><li>Write down both versions. Never quietly “fix” one.</li><li>Call it settled only when the evidence settles it.</li></ol>',
 '<h3>Where it stands</h3><p>The case is still open. The next witnesses: a newspaper notice from the days after his death, his probate file, and the cemetery’s records, read on paper.</p><p class="bk-end">More lessons will be bound into this book as they are posted.</p><p><a href="/notes/one-letter-two-certificates/">Read this case as a page</a></p>',
]
if len(P)%2: P.append('<p class="bk-end">·</p>')
leaves=''.join(f'<div class="leaf" style="--i:{i}"><div class="face front">{P[2*i]}<span class="pg">{2*i+1 if i else ""}</span></div><div class="face back">{P[2*i+1]}<span class="pg">{2*i+2}</span></div></div>' for i in range(len(P)//2))
body=f'''    <p class="crumb"><a href="/notes/">← Field notes</a></p>
    <p class="kicker">The field notes, bound</p>
    <h1>The book of field notes</h1>
    <p class="note">Click or tap the right-hand page to turn forward, the left-hand page to turn back. Arrow keys work too.</p>
  <div class="book-wrap"><div class="book" id="book" tabindex="0" aria-label="Field notes book. Use the arrow keys to turn pages." style="--n:{len(P)//2}">{leaves}</div></div>
    <p class="center bk-nav"><button type="button" class="btn" id="bkPrev">‹ Back</button> <span id="bkAt" class="note" aria-live="polite"></span> <button type="button" class="btn" id="bkNext">Turn ›</button></p>
    <script>
    (function(){{ var book=document.getElementById('book'), L=[].slice.call(book.querySelectorAll('.leaf')), at=0, at$=document.getElementById('bkAt');
      function draw(){{ L.forEach(function(l,i){{ l.classList.toggle('turned', i<at); l.style.zIndex = i<at ? i : L.length-i; }});
        book.classList.toggle('opened', at>0); book.classList.toggle('closed-end', at===L.length);
        at$.textContent = at===0 ? 'Cover' : at===L.length ? 'The end' : 'Pages '+(2*at)+'–'+(2*at+1); }}
      function go(d){{ at=Math.max(0,Math.min(L.length,at+d)); draw(); }}
      L.forEach(function(l,i){{ l.querySelector('.front').addEventListener('click', function(e){{ if (e.target.closest('a')) return; if (i===at) go(1); }});
        l.querySelector('.back').addEventListener('click', function(e){{ if (e.target.closest('a')) return; if (i===at-1) go(-1); }}); }});
      document.getElementById('bkNext').onclick=function(){{ go(1); }}; document.getElementById('bkPrev').onclick=function(){{ go(-1); }};
      book.addEventListener('keydown', function(e){{ if (e.key==='ArrowRight'){{ go(1); e.preventDefault(); }} if (e.key==='ArrowLeft'){{ go(-1); e.preventDefault(); }} }});
      var sx=null; book.addEventListener('touchstart', function(e){{ sx=e.touches[0].clientX; }}, {{passive:true}});
      book.addEventListener('touchend', function(e){{ if (sx===null) return; var dx=e.changedTouches[0].clientX-sx; if (Math.abs(dx)>40) go(dx<0?1:-1); sx=null; }});
      draw(); }})();
    </script>
'''
page('notes/book/index.html','The book of field notes · Project Scroll','The Project Scroll field notes as a small bound book with turning pages.',body)
print('book built')
