"""Builds 'Reading the old hand':  python3 _tools/build_hand.py"""
import sys, pathlib, json, html; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E=html.escape
CARDS=[
 ('ſ','The long s','Looks like an f without the full crossbar. Used at the start or middle of a word until about 1800: “Congreſs”, “ſon”, “Miſsiſsippi”. Read it as an ordinary s.'),
 ('ye','“Ye” means “the”','The y stands for an old letter, thorn (þ), pronounced “th”. “Ye olde inn” was always read “the old inn”. Likewise “yt” = that, “ym” = them.'),
 ('Wm · Jno · Chas','Shortened first names','Clerks raised the last letters: Wm = William, Jno = John (not Jonathan), Chas = Charles, Thos = Thomas, Jas = James, Geo = George, Saml = Samuel, Benj = Benjamin.'),
 ('inst. · ult. · prox.','Which month?','“The 4th inst.” = the 4th of this month. “The 20th ult.” = the 20th of last month. “The 2nd prox.” = the 2nd of next month. Check the date of the letter or newspaper to know which month.'),
 ('do.','Ditto','“do.” under an entry means “the same as above.” Census takers and clerks used it for repeated surnames, birthplaces and occupations.'),
 ('&c.','Et cetera','The ampersand plus c: “and so on”. Often written as a looped sign that can look like a letter.'),
 ('1745/6','Double dates','Before 1752 in England and its colonies, the new year began on 25 March. A date between January and March is often written with both years. Use the later one for today’s calendar.'),
 ('relict · consort','On gravestones','“Relict of John Smith” = his widow (she outlived him). “Consort of” = his wife, who died while he was living.'),
 ('dec’d · Esq.','In deeds and wills','dec’d = deceased. Esq. = Esquire, a courtesy for a lawyer or a man of standing, not a title of nobility.'),
 ('71y 4m 12d','Ages to the day','Age at death in years, months and days. Count back from the date of death with the <a href="/toolkit/#age">age calculator</a>.'),
]
Q=[
 ('A letter dated 10 June says “your note of the 28th ult.” When was the note written?',['28 June','28 May','28 July'],1,'“ult.” means last month: 28 May.'),
 ('In a 1790 newspaper you read “Congreſs”. What does it say?',['Congrefs','Congress','Congrefſ'],1,'That f-like letter is the long s.'),
 ('A census line reads “Jno Smith” and below it “do. do.” What is the second person’s name?',['John Smith','Jonathan Smith','Unknown'],0,'Jno is John, and do. repeats the line above.'),
 ('A gravestone reads “Mary, relict of Amos Hale.” What does it tell you?',['Mary died before Amos','Mary was Amos’s widow','Mary was Amos’s daughter'],1,'A relict outlived her husband.'),
 ('A baptism is dated “12 February 1734/5”. Which year is it on today’s calendar?',['1734','1735'],1,'Use the later year for January to March dates before 1752.'),
 ('“Ye Olde Tavern” was read aloud as…',['“Yee Old Tavern”','“The Old Tavern”'],1,'The y stands for the old letter thorn, “th”.'),
]
cards=''.join(f'<div class="hcard"><p class="glyph">{c[0]}</p><h3>{E(c[1])}</h3><p>{c[2]}</p></div>' for c in CARDS)
quiz=''.join(f'<li data-a="{a}"><p>{E(q)}</p><div class="qopts2">'+''.join(f'<button type="button" data-i="{i}">{E(o)}</button>' for i,o in enumerate(opts))+f'</div><p class="qwhy" hidden>{E(why)}</p></li>' for q,opts,a,why in Q)
body=f'''    <p class="crumb"><a href="/toolkit/">← The hunter’s toolkit</a></p>
    <p class="kicker">A guide from the desk</p>
    <h1>Reading the old hand</h1>
    <p class="lede" style="font-size:1.15rem">The writing in old records is not hard once you know ten tricks the clerks used. Here they are, with a short quiz at the end.</p>
    <h2>The clerks’ tricks</h2>
    <div class="hcards">{cards}</div>
    <h2>Test yourself</h2>
    <p class="note">Six questions. <span id="hq" aria-live="polite"></span></p>
    <ol class="hquiz">{quiz}</ol>
    <p class="ctas" style="margin-top:1.4rem"><a class="btn primary" href="/toolkit/">Back to the toolkit</a><a class="btn" href="/guide/death-certificate/">How to read a death certificate</a></p>
    <script>
    (function(){{ var items=[].slice.call(document.querySelectorAll('.hquiz > li')), s=0, n=0, out=document.getElementById('hq');
      items.forEach(function(li){{ li.querySelectorAll('button').forEach(function(b){{ b.addEventListener('click', function(){{
        if (li.dataset.done) return; li.dataset.done=1; n++; var ok=b.dataset.i===li.dataset.a; if (ok) s++;
        li.querySelectorAll('button').forEach(function(x){{ x.disabled=true; if (x.dataset.i===li.dataset.a) x.classList.add('right'); else if (x===b) x.classList.add('wrong'); }});
        var w=li.querySelector('.qwhy'); w.hidden=false; w.insertAdjacentHTML('afterbegin', ok?'<b>Right.</b> ':'<b>Not quite.</b> ');
        out.textContent = n===items.length ? ('You read '+s+' of '+items.length+' like a clerk.') : (s+' of '+n+' so far.'); }}); }}); }}); }})();
    </script>
'''
page('guide/old-handwriting/index.html','Reading the old hand · Project Scroll','The handwriting tricks and abbreviations of old records explained: the long s, ye, inst. and ult., double dates and more, with a quiz.',body, og='https://projectscroll.com/og/handwriting.jpg')
print('hand built')
