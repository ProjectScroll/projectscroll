"""Builds the family-history page and the family-legends page:  python3 _tools/build_families.py"""
import sys, pathlib, json; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page

M = {'D': ('kD', 'Document'), 'P': ('kP', 'Period print'), 'C': ('kC', 'County history'), 'M': ('kM', 'Compiled'),
     'T': ('kT', 'Tradition'), 'I': ('kI', 'Inference'), 'R': ('kR', 'Reading'), 'H': ('kH', 'Hypothesis'), 'F': ('kF', 'Field')}

# The specimen family. Every name is invented; the method is the one we use.
# n = Ahnentafel number: 1 the subject, 2n the father of n, 2n+1 the mother of n.
FAM = {
 1: {'n': 'You', 'd': 'The person the history is written for', 'f': []},
 2: {'n': 'Walter J. Brandt', 'd': '1921 – 1988', 'f': [
     ['Born 3 March 1921, Toledo, Ohio', 'D', 'His birth certificate, filed the same week.'],
     ['Died 14 November 1988', 'D', 'His death certificate.'],
     ['Served in the Navy, 1942–1945', 'D', 'His discharge paper, kept by the family.']]},
 3: {'n': 'Ruth E. Lindqvist', 'd': '1924 – 2009', 'f': [
     ['Born 1924, Ishpeming, Michigan', 'P', 'Her obituary. Her birth record has not yet been seen.'],
     ['Married Walter Brandt, 1947', 'D', 'The county marriage record, which names both sets of parents.']]},
 4: {'n': 'Otto Brandt', 'd': '1890 – 1957', 'f': [
     ['Born 1890, Ohio', 'D', 'The 1900, 1910 and 1920 censuses agree on the year and the state.'],
     ['A cabinetmaker all his working life', 'C', 'A county history of 1915 has a short sketch of him, written while he was alive.']]},
 5: {'n': 'Clara ?', 'd': '1894 – 1971', 'q': 1, 'f': [
     ['Wife of Otto Brandt', 'D', 'Their marriage record.'],
     ['Her own surname is not recorded', 'I', 'Every record we have found names her under her husband’s surname, which tells us nothing about her father’s. So she is shown as “Clara ?”, never as “Clara Brandt” by birth.'],
     ['The family says she was “a Miller from Indiana”', 'T', 'Recorded exactly as told. Worth testing, not yet a fact.'],
     ['Her death certificate should name her father', 'H', 'Filed under Brandt, her married name. That is where we would look first.']]},
 6: {'n': 'Nils Lindqvist', 'd': '1888 – 1960', 'f': [
     ['Born 1888, Sweden', 'D', 'His naturalization papers.'],
     ['Came to Michigan to work in the iron mines', 'R', 'Our reading of the 1910 census, which lists him as a miner in an iron-mining town.']]},
 7: {'n': 'Hanna Bergström', 'd': '1891 – 1983', 'f': [
     ['Born 1891, Sweden', 'D', 'Her naturalization papers, and her parish’s own birth register.']]},
 8: {'n': 'August Brandt', 'd': 'about 1862 – 1931', 'f': [
     ['Born about 1862', 'I', 'Worked out from his age at death. No birth record has been found, so the year is printed with “about”, and it stays that way until a record turns up.'],
     ['Died 1931', 'D', 'His death certificate.']]},
 9: {'n': 'Wilhelmina Krause', 'd': '1866 – 1940', 'f': [
     ['Her maiden name is Krause', 'D', 'The baptism record of her son Otto names both parents in full.']]},
 12: {'n': 'Per Lindqvist', 'd': '1855 – 1922', 'f': [
     ['Father of Nils', 'D', 'The parish register in Sweden.']]},
 14: {'n': 'Johan Bergström', 'd': '1859 – 1931', 'f': [
     ['Father of Hanna', 'D', 'Hanna’s entry in the parish birth register.']]},
 15: {'n': 'Elin ?', 'd': '? – 1889 ⚠', 'q': 1, 'warn': 'A mother cannot die before her child is born. An online family tree gives Elin’s death as 1889, but her daughter Hanna was born in 1891. One of the two dates is wrong, and until we know which, the chart says so rather than hiding it.', 'f': [
     ['Mother of Hanna', 'D', 'Hanna’s entry in the parish birth register names her mother only as Elin.'],
     ['Died 1889', 'M', 'An online family tree, which cites no source for the date.']]},
}


def intake(kind):
    fam = kind == 'family'
    want = ('<label for="ikWant">What would you like?</label><select id="ikWant"><option>Not sure yet: advise me</option><option>A family register (descendants of one couple)</option><option>An ancestral monograph (all the ancestors of one person)</option><option>A full family history</option><option>One line, or one question, to begin with</option></select>') if fam else ''
    story_label = 'The family story, exactly as it was told' if not fam else 'Any family story, exactly as it was told <span class="h">(optional)</span>'
    return f"""    <div class="intake" id="intake">
      <p class="note" style="margin:0">Fill in what you can. This builds a tidy message for you to send us by email or Facebook Messenger. Nothing is sent by this page; your draft stays in your own browser.</p>
      <label for="ikName">Your first name</label><input type="text" id="ikName" autocomplete="given-name">
      <label for="ikWho">{'Who is it about?' if fam else 'Who is the story about?'} <span class="h">Full names, as far as you know them</span></label><input type="text" id="ikWho">
      <label for="ikWhere">Where did they live? <span class="h">Town, county, state or country</span></label><input type="text" id="ikWhere">
      <label for="ikWhen">Roughly when? <span class="h">Birth, marriage or death years, even guesses</span></label><input type="text" id="ikWhen">
      {want}
      <label for="ikStory">{story_label}</label><textarea id="ikStory"></textarea>
      <label for="ikTold">Who told it, and when did you first hear it? <span class="h">(optional)</span></label><input type="text" id="ikTold">
      <fieldset><legend>What does the family have?</legend><div class="chk">
        <label><input type="checkbox" value="a family Bible"> Family Bible</label><label><input type="checkbox" value="letters"> Letters</label><label><input type="checkbox" value="photographs"> Photographs</label><label><input type="checkbox" value="obituaries or clippings"> Obituaries or clippings</label><label><input type="checkbox" value="certificates"> Certificates</label><label><input type="checkbox" value="someone's family tree"> Someone’s family tree</label><label><input type="checkbox" value="DNA test results"> DNA results</label>
      </div></fieldset>
      <div class="out" id="ikOut" aria-live="polite"></div>
      <div class="btns"><button type="button" class="btn" id="ikCopy">Copy my message</button><a class="btn primary" href="mailto:research@projectscroll.com?subject={'A%20family%20legend' if kind=='legend' else 'A%20family%20history'}" id="ikMail">Send it by email</a><a class="btn" href="https://m.me/projectscroll" rel="noopener" id="ikSend">Open Messenger</a></div>
      <p class="note center" id="ikDone" aria-live="polite" style="margin:.5rem 0 0"></p>
    </div>
    <script>
    (function(){{ "use strict";
      const $=id=>document.getElementById(id), KEY='ps-intake-{kind}';
      const fields=['ikName','ikWho','ikWhere','ikWhen','ikStory','ikTold','ikWant'].map($).filter(Boolean);
      try{{ const saved=JSON.parse(localStorage.getItem(KEY)||'{{}}'); fields.forEach(f=>{{ if(saved[f.id]) f.value=saved[f.id]; }}); }}catch(e){{}}
      const boxes=[...document.querySelectorAll('#intake input[type=checkbox]')];
      function build(){{
        const v=id=>($(id)&&$(id).value.trim())||'';
        const has=boxes.filter(b=>b.checked).map(b=>b.value);
        const L=['Hello Project Scroll,', '', {'"I would like help with a family history."' if fam else '"I would like a family story tested against the records."'}, ''];
        if(v('ikWho')) L.push('Who: '+v('ikWho'));
        if(v('ikWhere')) L.push('Where: '+v('ikWhere'));
        if(v('ikWhen')) L.push('When: '+v('ikWhen'));
        if(v('ikWant')) L.push('What I would like: '+v('ikWant'));
        if(v('ikStory')) L.push('', 'The story, as told: '+v('ikStory'));
        if(v('ikTold')) L.push('Told by: '+v('ikTold'));
        if(has.length) L.push('', 'We have: '+has.join(', ')+'.');
        L.push('', 'Thank you'+(v('ikName')?',':'.'));
        if(v('ikName')) L.push(v('ikName'));
        $('ikOut').textContent=L.join('\\n');
        $('ikMail').href='mailto:research@projectscroll.com?subject='+encodeURIComponent('{'A family legend' if kind=='legend' else 'A family history'}')+'&body='+encodeURIComponent(L.join('\\n'));
        try{{ const o={{}}; fields.forEach(f=>o[f.id]=f.value); localStorage.setItem(KEY,JSON.stringify(o)); }}catch(e){{}}
      }}
      document.getElementById('intake').addEventListener('input',build); build();
      $('ikCopy').addEventListener('click',()=>{{
        const t=$('ikOut').textContent, ok=()=>{{ $('ikDone').textContent='Copied. Now paste it into an email or a Messenger message.'; }};
        if(navigator.clipboard) navigator.clipboard.writeText(t).then(ok,()=>{{ const r=document.createRange(); r.selectNodeContents($('ikOut')); getSelection().removeAllRanges(); getSelection().addRange(r); $('ikDone').textContent='Select-all is done: press copy on your keyboard.'; }});
      }});
    }})();
    </script>
"""

families = f'''    <p class="crumb"><a href="/services/">← Research services</a></p>
    <p class="kicker">Research services</p>
    <h1>Family histories, built to be checked</h1>
    <p class="lede" style="font-size:1.15rem">Most family trees are copied from other family trees. Ours are built from the records themselves: every name, date and place marked with where it came from, every gap shown honestly, and every family story kept exactly as it was told, beside the evidence that tests it.</p>

    <h2>What we make</h2>
    <div class="fammakes">
      <div><p class="k">Looking down</p><h3>A family register</h3><p>Every descendant of one couple, generation by generation, each person given a number, so that a reader can follow any branch from the first settlers to the present day. The form genealogists have trusted for 150 years.</p></div>
      <div><p class="k">Looking back</p><h3>An ancestral monograph</h3><p>Your ancestors, back as far as the records honestly go, on a single chart. Where a line stops, it says whose parents are wanting, so you can see at a glance what is known, what is not, and where to look next.</p></div>
      <div><p class="k">The whole story</p><h3>A family history</h3><p>Every line written up as a story, with the evidence beneath it: maps, records, a list of every source, an index of names and places, and the open questions set out for the next person to take up.</p></div>
    </div>

    <h2>A specimen monograph</h2>
    <p>Here is how an ancestral monograph works, using an invented family. Tap anyone to see what we know about them, and how we know it.</p>
    <div class="mono" id="mono">
      <p class="mono-tag">Specimen. The names are invented; the method is real.</p>
      <div class="mono-scroll"><div class="mono-grid" id="monoGrid" role="group" aria-label="Specimen pedigree chart, four generations"></div></div>
      <div class="mono-panel" id="monoPanel" aria-live="polite"><p class="note" style="margin:0">Tap a name in the chart.</p></div>
      <div class="mono-gaps" id="monoGaps"></div>
    </div>
    <ul class="dis monokey">
      <li><b>“Clara ?”</b> A question mark means the marriage is recorded but her own surname is not. Women are usually recorded under their husbands’ names, which is not the same as being born with them.</li>
      <li><b>“Wanting”</b> An empty box beside a known person is a real gap: someone we could find tomorrow. The boxes beyond the edge of the chart, behind Clara’s missing parents, are not gaps at all. There is nothing to look for there until her parents are found.</li>
      <li><b>The warning sign.</b> When two records cannot both be true, the chart flags the joint and leaves it in. Never solve a problem by deleting the evidence.</li>
    </ul>

    <h2>How a register reads</h2>
    <div class="regsample">
      <p><b>1. AUGUST¹ BRANDT</b> was born about 1862 <span class="mk sm kI">Inference</span> and died in 1931 <span class="mk sm kD">Document</span>. He married <b>WILHELMINA KRAUSE</b>, born in 1866 <span class="mk sm kD">Document</span>.</p>
      <p class="regkids">Children of August and Wilhelmina:</p>
      <p class="regkid"><span>+ 2</span><span>i.</span><span><b>OTTO²</b>, born 1890; married <b>CLARA ?</b></span></p>
      <p class="regkid"><span></span><span>ii.</span><span>Emma, born 1893; died 1894, aged one.</span></p>
      <p class="note" style="margin:.6rem 0 0">The small raised number is the generation. The plus sign means Otto’s own family is carried forward under his number, 2, so a reader can follow his line on down without losing the thread. (The same invented family as the chart above.)</p>
    </div>

    <h2>Lessons from our own desk</h2>
    <p>Every one learned the hard way, on a family history built at this desk.</p>
    <ol class="lessons">
      <li><b>A woman dies under her married name.</b> For years a death certificate went unfound because everyone searched for her under her maiden name. It was filed under her husband’s.</li>
      <li><b>Search the unusual name.</b> A rare surname finds the family and almost nobody else. A common one needs a place and a date beside it, or it finds thousands.</li>
      <li><b>A strong lead in the right county is still not a parent.</b> A well-documented man of the right name, in the right place, at the right time, turned out to be no relation at all. The answer was in a different family.</li>
      <li><b>An abstract is not a record.</b> A published summary of a colonial will gave two witnesses’ names and a probate date. The court’s own record disagreed on both.</li>
      <li><b>“About” must stay “about.”</b> A birth year worked out from an age at death was printed beside real dates, and soon looked like one. Estimates are marked as estimates, always.</li>
      <li><b>The best finds are in free books nobody opened.</b> Lines written off as dead ends turned out to be answered in county histories and family genealogies that had been free online for years. Dead ends don’t get searched.</li>
    </ol>

    <h2>Starting your family’s history</h2>
    <ol class="steps">
      <li><b>Tell us who.</b> One couple to work down from, or one person to work back from. Names, places, rough dates.</li>
      <li><b>Send what the family has.</b> Bible pages, letters, photographs, obituaries, old trees. We read every one, and we keep every family story exactly as it was told.</li>
      <li><b>Agree on the shape.</b> A register, a monograph, a full history, or a single line to begin with.</li>
      <li><b>We build it from the records.</b> Certificates, censuses, deeds, wills, church books, newspapers and county histories.</li>
      <li><b>You get a book you can trust.</b> Every statement marked, every source listed, every gap honest, ready to print, share and add to.</li>
    </ol>
    <h2 id="start">Tell us about your family</h2>
{intake('family')}
    <p class="center"><a class="btn" href="/sample/project-scroll-sample-family-register.pdf">See a sample family register (PDF)</a> <a class="btn" href="/legends/">Test a family legend</a></p>
    <script>
    (function(){{ "use strict";
      const F={json.dumps(FAM, ensure_ascii=False)};
      const M={json.dumps(M, ensure_ascii=False)};
      const grid=document.getElementById('monoGrid'), panel=document.getElementById('monoPanel'), gapsBox=document.getElementById('monoGaps');
      const rel=n=>({{1:'You',2:'Father',3:'Mother',4:'Grandfather',5:'Grandmother',6:'Grandfather',7:'Grandmother'}}[n]||(n%2?'Great-grandmother':'Great-grandfather'));
      const esc=s=>String(s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
      // which generation (column) and which row span each number takes in an 8-row grid
      for(let n=1;n<16;n++){{
        const g=Math.floor(Math.log2(n)), span=8>>g, row=(n-(1<<g))*span+1;
        const p=F[n], el=document.createElement(p?'button':'div');
        el.className='mono-box g'+g+(p?'':' empty')+(p&&p.q?' q':'')+(p&&p.warn?' warn':'');
        el.style.gridColumn=String(g+1); el.style.gridRow=row+' / span '+span;
        if(p){{ el.type='button'; el.dataset.n=n; el.innerHTML='<span class="r">'+rel(n)+'</span><b>'+esc(p.n)+'</b><span class="dt">'+esc(p.d)+'</span>'; }}
        else {{ const child=F[n>>1]; el.innerHTML='<span class="r">'+rel(n)+'</span><b>Wanting</b><span class="dt">'+(child?(n%2?'the mother of ':'the father of ')+esc(child.n):'')+'</span>'; }}
        grid.appendChild(el);
      }}
      function show(n){{
        const p=F[n]; grid.querySelectorAll('.mono-box').forEach(b=>b.classList.toggle('on',b.dataset.n==n));
        let h='<p class="mono-who"><span class="r">'+rel(n)+' · number '+n+'</span><b>'+esc(p.n)+'</b> '+esc(p.d)+'</p>';
        if(p.warn) h+='<p class="mono-warn">⚠ '+esc(p.warn)+'</p>';
        if(p.f.length){{ h+='<ul class="mono-facts">'; for(const [t,m,why] of p.f) h+='<li><span class="mk sm '+M[m][0]+'">'+M[m][1]+'</span> <b>'+esc(t)+'.</b> '+esc(why)+'</li>'; h+='</ul>'; }}
        else h+='<p class="note" style="margin:0">Every chart starts with the person it is for, and works back one generation at a time: number 2 is your father, number 3 your mother, and every father’s number is double his child’s.</p>';
        panel.innerHTML=h;
      }}
      grid.addEventListener('click',e=>{{ const b=e.target.closest('button.mono-box'); if(b) show(+b.dataset.n); }});
      const gaps=[]; for(let n=2;n<8;n++) if(F[n]){{ if(!F[2*n]) gaps.push('the father of '+F[n].n); if(!F[2*n+1]) gaps.push('the mother of '+F[n].n); }}
      gapsBox.innerHTML='<p><b>Wanting, in this chart:</b> '+gaps.map(esc).join(' · ')+'. <span class="note">'+gaps.length+' real gaps, each one a named person whose parents could be found.</span></p>';
      show(5);
    }})();
    </script>
'''
page('families/index.html', 'Family histories and registers · Project Scroll',
     'Family registers, ancestral monographs and full family histories, built from the records with every statement marked and every gap shown honestly.', families, og='https://projectscroll.com/og/families.jpg')

# ---------------------------------------------------------------- legends
LEG = [
 {'k': 'name', 't': 'Our name was changed at Ellis Island',
  'say': 'An inspector couldn’t spell it, so he wrote down something easier, and that became the family name.',
  'rec': 'Ellis Island inspectors did not write names down; they checked arrivals against passenger lists made at the port of departure. Names did change, often, but usually years later and by the family itself: at naturalization, at work, at school, or simply over time.',
  'how': ['Find the passenger list: it shows the name as written where the journey began.', 'Find the naturalization papers, which often record both the old name and the new one.', 'Follow the name census by census to see when the new spelling first appears.'],
  'odds': 'The change almost always happened. Ellis Island almost never did it.'},
 {'k': 'royal', 't': 'We descend from a famous family',
  'say': 'A lord, a king, a governor or a famous founder sits at the top of the tree.',
  'rec': 'Some of these are true. Many began as a name match: someone of the right surname, in roughly the right place, adopted into the tree a century ago and copied forward until it looked like fact.',
  'how': ['Test the line one link at a time, starting with the most recent. Every parent–child joint needs its own record.', 'Find who first printed the claim, and what they cited.', 'Check the famous person’s documented children against the one the family claims.'],
  'odds': 'Worth testing. Usually the line breaks at one particular joint, and finding it is a story in itself.'},
 {'k': 'princess', 't': 'Great-grandmother was a Cherokee princess',
  'say': 'A grandmother or great-grandmother was a Native princess, often said to be Cherokee.',
  'rec': 'The Cherokee Nation did not have princesses, and the story is so widespread that historians treat it as a family-legend pattern of its own. Some families do have Native ancestry, and the records that show it are specific: tribal rolls, agency censuses and treaty and allotment papers.',
  'how': ['Name the ancestor and place her in a census, with the people around her.', 'Search the tribal rolls of the place and period (for the Cherokee: the Dawes and Guion Miller rolls, and the earlier rolls before them).', 'A DNA test cannot show tribal membership; only the records and the nation itself can.'],
  'odds': 'The princess is almost never real. The ancestor sometimes is, and deserves to be found properly.'},
 {'k': 'brothers', 't': 'Three brothers came over together',
  'say': 'Three brothers arrived on one ship: one went north, one went south and one went west.',
  'rec': 'It is one of the most common stories in American family lore. Sometimes there were three brothers. Often there were three men of the same surname who were not related at all, later joined together to explain why the name turns up in different places.',
  'how': ['Find each man separately in the passenger lists, censuses and land records.', 'Look for a document that names them as brothers: a will, a deed, a probate file.', 'For male lines, a Y-DNA test can say whether their descendants share a father at all.'],
  'odds': 'Often half-true: the men were real; the brotherhood is the part to test.'},
 {'k': 'burned', 't': 'The courthouse burned, so there are no records',
  'say': 'Everything was lost in the fire, so there is no point looking.',
  'rec': 'Courthouses did burn, and records were lost. But deeds were often re-recorded afterward by the owners, and copies survive in state archives, churches, newspapers, tax rolls, military files and the records of neighboring counties.',
  'how': ['Find out exactly which years and which books were lost: it is rarely everything.', 'Look for deeds re-recorded after the fire.', 'Go around it: state census, tax lists, church registers, newspapers, pension files.'],
  'odds': 'The fire is usually real. “No records at all” almost never is.'},
 {'k': 'spelled', 't': 'Our name was always spelled this way',
  'say': 'The family has always spelled it exactly this way, so anyone spelled differently is not ours.',
  'rec': 'Spelling was not fixed until well into the 1900s. Clerks wrote what they heard, and the same man can appear under three spellings in three records. Searching only one spelling is the commonest reason a family “can’t be found”.',
  'how': ['Search every spelling you can say aloud the same way.', 'Use Soundex, the code old census indexes were built on (it is in our <a href="/toolkit/">toolkit</a>).', 'Judge a record by the people, place and dates around the name, not by the spelling.'],
  'odds': 'Nearly always untrue, and nearly always the key to finding the family again.'},
]

def leg_html(l):
    how = ''.join(f'<li>{h}</li>' for h in l['how'])
    return f'''<div class="lg-ans" data-k="{l['k']}" hidden>
        <p><span class="mk sm kT">Tradition</span> <b>What families say.</b> {l['say']}</p>
        <p><span class="mk sm kD">Document</span> <b>What the records usually show.</b> {l['rec']}</p>
        <p class="lg-how-h"><b>How we test it</b></p><ul class="dis">{how}</ul>
        <p class="lg-odds"><span class="mk sm kR">Reading</span> {l['odds']}</p>
      </div>'''

btns = ''.join(f'<button type="button" class="lg-btn" data-k="{l["k"]}" aria-pressed="false">{l["t"]}</button>' for l in LEG)
answers = '\n      '.join(leg_html(l) for l in LEG)
legends = f'''    <p class="crumb"><a href="/services/">← Research services</a></p>
    <p class="kicker">Mysteries in the family</p>
    <h1>Is the family story true?</h1>
    <p class="lede" style="font-size:1.15rem">Every family has a story that has been told so often nobody questions it. Some are true. Some are half-true. Some began as a guess a hundred years ago. The records can usually tell which.</p>

    <h2>Test a family legend</h2>
    <p>Choose the story your family tells.</p>
    <div class="lg" id="lg">
      <div class="lg-btns" role="group" aria-label="Family legends">{btns}</div>
      <div class="lg-out" id="lgOut" aria-live="polite">
      <p class="note lg-empty" style="margin:0">Pick a story above to see what the records usually say about it, and how we would test yours.</p>
      {answers}
      </div>
    </div>
    <p class="note">These are patterns, not verdicts. Your family’s story is its own case, and the records decide it.</p>

    <h2>A mystery from the published record</h2>
    <div class="solved">
      <p class="k">The Lord Baltimore bride</p>
      <p><span class="mk sm kM">Compiled</span> In 1925 a printed family history said that John Chenoweth, a colonial blacksmith, married Mary Calvert, of the line of the Lords of Baltimore, and that the couple settled by the Gunpowder River in Baltimore County, Maryland. Families have repeated it ever since.</p>
      <p><span class="mk sm kD">Document</span> The records of the time tell a plainer story. A tax roll of 1737 lists John and his family on <i>leased</i> land in Back River Upper Hundred; there is no record of him ever owning land in Baltimore County. He made his will in Frederick County, Virginia, on 11 April 1746. And no document of the period has been found that even proves his wife’s surname was Calvert.</p>
      <p><span class="mk sm kR">Reading</span> The noble bride is a tradition, not a record. The Chenoweth family’s own researchers reached the same conclusion: in their words, the tradition is “not supported by known facts.” The real John Chenoweth, a blacksmith on rented ground, is the more interesting man.</p>
      <p class="note" style="margin:0">Sources: Cora C. Hiatt, <i>History of the Chenoweth Family</i> (1925); “The First Family,” <a href="https://chenowethsite.com/ch0oth.htm">chenowethsite.com</a>, which sets out the tax roll, the will and the tradition. Settled by the family’s own researchers; shown here because it is the pattern exactly.</p>
    </div>

    <h2>Bring us your family’s story</h2>
    <p>Tell us the story exactly as it was told to you, who told it, and anything written down. We will record it word for word, find what the records say, and tell you honestly which parts hold up.</p>
{intake('legend')}
    <p class="center"><a class="btn" href="/families/">Family histories</a></p>
    <script>
    (function(){{ "use strict";
      const btns=[...document.querySelectorAll('.lg-btn')], ans=[...document.querySelectorAll('.lg-ans')], empty=document.querySelector('.lg-empty');
      btns.forEach(b=>b.addEventListener('click',()=>{{
        btns.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
        ans.forEach(a=>a.hidden=a.dataset.k!==b.dataset.k); empty.hidden=true;
      }}));
    }})();
    </script>
'''
page('legends/index.html', 'Is the family story true? · Project Scroll',
     'Test a family legend against the records: Ellis Island name changes, famous ancestors, the Cherokee princess, three brothers, burned courthouses and more.', legends, og='https://projectscroll.com/og/legends.jpg')
print('families + legends built')
