"""Writes the specimen family register as HTML, then prints it to PDF:
   python3 tools/build_register_pdf.py && NODE_PATH=$(npm root -g) node tools/print_register.js
The Brandt family is invented (the same specimen family as /families/). Every page says so."""
import pathlib
R = pathlib.Path(__file__).resolve().parent.parent
F = lambda f: (R / 'fonts' / f).as_uri()
MK = {'D': ('#1e3f27', 'Document'), 'P': ('#2d4c73', 'Period print'), 'C': ('#6b5a2a', 'County history'), 'M': ('#686868', 'Compiled'),
      'T': ('#5c3a6b', 'Tradition'), 'I': ('#7a6633', 'Inference'), 'R': ('#a3261a', 'Reading'), 'H': ('#a84d3b', 'Hypothesis')}
def m(k, n=None):
    c, t = MK[k]
    return f'<span class="mk" style="background:{c}">{t}</span>' + (f'<sup class="fn">{n}</sup>' if n else '')

html = f'''<!doctype html><html><head><meta charset="utf-8"><title>The Brandt Family: a specimen family register · Project Scroll</title><style>
@font-face{{font-family:D;src:url({F('libre-caslon-display-latin-400-normal.woff2')})}}
@font-face{{font-family:T;src:url({F('libre-caslon-text-latin-400-normal.woff2')})}}
@font-face{{font-family:T;font-style:italic;src:url({F('libre-caslon-text-latin-400-italic.woff2')})}}
@font-face{{font-family:T;font-weight:700;src:url({F('libre-caslon-text-latin-700-normal.woff2')})}}
@page{{size:Letter;margin:0.85in 0.9in 0.9in}}
body{{font-family:T,Georgia,serif;font-size:11pt;line-height:1.5;color:#1D2733;margin:0}}
h1,h2{{font-family:D,serif;font-weight:400}}
h2{{font-size:20pt;margin:0 0 .3em;color:#1D2733;border-bottom:1px solid #B9C2B8;padding-bottom:.15em}}
.k{{font-size:8.5pt;letter-spacing:.16em;text-transform:uppercase;color:#B3362B;margin:0 0 .2em}}
.mk{{display:inline-block;font-family:Arial,Helvetica,sans-serif;font-weight:700;font-size:6.2pt;letter-spacing:.04em;text-transform:uppercase;color:#fff;padding:0 .35em;border-radius:2px;vertical-align:.12em;margin-left:.15em;line-height:1.6}}
.fn{{font-size:7pt;color:#B3362B;margin-left:.05em}}
.page{{page-break-after:always}}
.cover{{height:8.9in;display:flex;flex-direction:column;justify-content:center;text-align:center;border-left:3px solid #B3362B;padding-left:.4in}}
.cover h1{{font-size:44pt;margin:.1em 0}}
.cover .sub{{font-size:15pt;font-style:italic;margin:0 0 1.4em}}
.spec{{border:1.5px solid #B3362B;color:#B3362B;padding:.5em .8em;font-size:10pt;margin:1.6em auto 0;max-width:4.6in}}
.entry{{margin:0 0 1.2em;break-inside:avoid}}
.entry .head{{margin:0}}
.kids{{font-style:italic;margin:.5em 0 .2em}}
.kid{{display:grid;grid-template-columns:.42in .32in 1fr;margin:.1em 0}}
.note{{font-size:9.5pt;color:#4B5663}}
.open li{{margin:.25em 0;font-size:10.5pt}}
table.ped{{border-collapse:separate;border-spacing:4pt;width:100%;font-size:9pt}}
table.ped td{{border:1px solid #B9C2B8;border-left:3px solid #2B4A41;padding:3pt 5pt;vertical-align:middle}}
table.ped td.want{{border-style:dashed;border-left:1px dashed #B9C2B8;color:#B3362B;font-style:italic}}
table.ped td.q{{border-left-color:#5c3a6b}} table.ped td.w{{border-left-color:#B3362B}}
table.ped b{{font-size:10pt}}
.src li{{margin:.1em 0;font-size:9pt}} .src{{margin:.2em 0}}
.idx{{columns:3;font-size:9.5pt;list-style:none;padding:0;margin:.3em 0}} .idx li{{margin:0}}
.foot{{position:fixed;bottom:-.55in;left:0;right:0;text-align:center;font-size:8pt;color:#8a8f96}}
</style></head><body>

<div class="page cover">
  <p class="k">Project Scroll · A family register</p>
  <h1>The Brandt Family</h1>
  <p class="sub">The descendants of August Brandt, about 1862 – 1931</p>
  <p>Three generations, every statement marked with where it came from</p>
  <p class="spec"><b>SPECIMEN.</b> The Brandts are an invented family, made to show how a Project Scroll family register reads. Every name, date and source in it is invented. The method is the one we use.</p>
</div>

<div class="page">
  <p class="k">Before you begin</p>
  <h2>How to read this register</h2>
  <p>A register starts with one couple and follows their descendants down, generation by generation. Every person who heads a family is given a number in bold, and keeps it.</p>
  <ul>
    <li><b>The small raised number</b> after a first name is the generation: OTTO² is in the second generation.</li>
    <li><b>The names in brackets</b> after a heading are the person’s line back to the beginning: “(Otto², August¹)”.</li>
    <li><b>Children</b> are listed under their parents with small roman numerals: i, ii, iii.</li>
    <li><b>A plus sign</b> in front of a child means that child’s own family is carried forward under the number beside it.</li>
    <li><b>“Clara ?”</b> means the marriage is recorded but her own surname is not. We never give a woman her husband’s surname as if she were born with it.</li>
    <li><b>Living people are not named.</b> A register is made to be shared, and the living are entitled to their privacy.</li>
  </ul>
  <h2 style="margin-top:1em">The marks</h2>
  <p>Every statement carries a mark saying what kind of evidence stands behind it, and a small red number pointing to the source list at the back.</p>
  <p>{m('D')} made at the time by someone whose job was to write it down &nbsp; {m('P')} printed at or near the time &nbsp; {m('C')} the old county histories &nbsp; {m('M')} a later compilation &nbsp; {m('T')} a family story, as told &nbsp; {m('I')} a step that follows from the records &nbsp; {m('R')} our interpretation &nbsp; {m('H')} an idea still to be tested</p>
  <p class="note">Records are weighed, not counted. A single document made at the time outweighs any number of later retellings.</p>
</div>

<div class="page">
  <p class="k">Generation one</p>
  <h2>August Brandt and Wilhelmina Krause</h2>
  <div class="entry">
    <p class="head"><b>1. AUGUST¹ BRANDT</b> was born about 1862 {m('I',1)}, a year worked out from his age at death; no record of his birth has yet been found, so the year stays “about” until one is. He died in 1931 {m('D',1)}. He married <b>WILHELMINA KRAUSE</b>, who was born in 1866 {m('D',2)} and died in 1940 {m('D',3)}. Her maiden name is given in full in the baptism record of their son Otto {m('D',2)}.</p>
    <p class="kids">Children of August and Wilhelmina (Krause) Brandt:</p>
    <p class="kid"><span>+ 2</span><span>i.</span><span><b>OTTO²</b>, born 1890 {m('D',4)}; married <b>CLARA ?</b>.</span></p>
    <p class="kid"><span></span><span>ii.</span><span>Emma, born 1893 {m('D',5)}; died 1894, aged one {m('D',5)}.</span></p>
  </div>
  <p class="note">The family says August “came over from Pomerania as a boy” {m('T',6)}. No passenger list or naturalization record has been found to test it. It is recorded here exactly as told, and listed among the open questions.</p>

  <p class="k" style="margin-top:1.6em">Generation two</p>
  <h2>Otto Brandt and Clara ?</h2>
  <div class="entry">
    <p class="head"><b>2. OTTO² BRANDT</b> (August¹) was born in Ohio in 1890; the censuses of 1900, 1910 and 1920 agree on the year and the state {m('D',4)}. He was a cabinetmaker all his working life {m('C',7)}, and died in 1957 {m('D',8)}. He married <b>CLARA ?</b>, born in 1894, died in 1971 {m('D',9)}. Every record so far names her under her married name, which tells us nothing about her father’s {m('I')}. The family says she was “a Miller from Indiana” {m('T',6)}; her death certificate, filed under Brandt, should name her father {m('H')}.</p>
    <p class="kids">Children of Otto and Clara (?) Brandt:</p>
    <p class="kid"><span>+ 3</span><span>i.</span><span><b>WALTER J.³</b>, born 3 March 1921 {m('D',10)}; married <b>RUTH E. LINDQVIST</b>.</span></p>
    <p class="kid"><span></span><span>ii.</span><span>Margaret, born 1923 {m('D',4)}; married Harold Feld; died 2015 {m('P',11)}.</span></p>
  </div>
</div>

<div class="page">
  <p class="k">Generation three</p>
  <h2>Walter J. Brandt and Ruth E. Lindqvist</h2>
  <div class="entry">
    <p class="head"><b>3. WALTER J.³ BRANDT</b> (Otto², August¹) was born on 3 March 1921 in Toledo, Ohio {m('D',10)}. He served in the Navy from 1942 to 1945 {m('D',12)} and died on 14 November 1988 {m('D',13)}. In 1947 he married <b>RUTH E. LINDQVIST</b> {m('D',14)}, the daughter of Nils Lindqvist and Hanna Bergström, as the marriage record states. Ruth was born in 1924 at Ishpeming, Michigan {m('P',15)} and died in 2009 {m('P',15)}.</p>
    <p class="kids">Children of Walter J. and Ruth E. (Lindqvist) Brandt:</p>
    <p class="kid"><span></span><span>i.</span><span>A son, living.</span></p>
    <p class="kid"><span></span><span>ii.</span><span>A daughter, living.</span></p>
  </div>

  <p class="k" style="margin-top:1.4em">Looking back</p>
  <h2>The ancestral monograph</h2>
  <p class="note" style="margin-top:0">The ancestors of Walter and Ruth’s children, four generations. Dashed boxes are real gaps: named people whose parents could be found.</p>
  <table class="ped">
    <tr><td rowspan="4"><b>Walter J. Brandt</b><br>1921 – 1988</td><td rowspan="2"><b>Otto Brandt</b><br>1890 – 1957</td><td><b>August Brandt</b><br>about 1862 – 1931</td></tr>
    <tr><td><b>Wilhelmina Krause</b><br>1866 – 1940</td></tr>
    <tr><td rowspan="2" class="q"><b>Clara ?</b><br>1894 – 1971</td><td class="want">Wanting: the father of Clara</td></tr>
    <tr><td class="want">Wanting: the mother of Clara</td></tr>
    <tr><td rowspan="4"><b>Ruth E. Lindqvist</b><br>1924 – 2009</td><td rowspan="2"><b>Nils Lindqvist</b><br>1888 – 1960</td><td><b>Per Lindqvist</b><br>1855 – 1922</td></tr>
    <tr><td class="want">Wanting: the mother of Nils</td></tr>
    <tr><td rowspan="2"><b>Hanna Bergström</b><br>1891 – 1983</td><td><b>Johan Bergström</b><br>1859 – 1931</td></tr>
    <tr><td class="w"><b>Elin ?</b><br>? – 1889 ⚠</td></tr>
  </table>
  <p class="note">⚠ An online tree gives Elin’s death as 1889, two years before her daughter Hanna was born in 1891. A mother cannot die before her child is born, so one of the two dates is wrong. The joint is flagged and left in until a record settles it.</p>
</div>

<div class="page">
  <p class="k">What is still open</p>
  <h2>Open questions, and where to look</h2>
  <ol class="open">
    <li><b>Who were Clara’s parents?</b> Her death certificate of 1971, filed under Brandt, should name her father and perhaps her mother’s maiden name. Her marriage record to Otto may name both.</li>
    <li><b>Was she “a Miller from Indiana”?</b> The family story, to be tested against the answer to question 1.</li>
    <li><b>When and where was August born?</b> A church record in Ohio, his naturalization papers if he was born abroad, or the 1900 census, which asked for the year of immigration.</li>
    <li><b>Did August come from Pomerania?</b> The same records would answer it.</li>
    <li><b>When did Elin die?</b> The Swedish parish’s burial register will settle which date is wrong.</li>
  </ol>
  <h2 style="margin-top:.8em">Sources</h2>
  <ol class="src">
    <li>Death certificate of August Brandt, 1931. <i>Specimen.</i></li>
    <li>Baptism record of Otto Brandt, 1890, naming both parents. <i>Specimen.</i></li>
    <li>Death certificate of Wilhelmina Brandt, 1940. <i>Specimen.</i></li>
    <li>United States census, 1900, 1910 and 1920, the Brandt household. <i>Specimen.</i></li>
    <li>Church register: baptism and burial of Emma Brandt, 1893–1894. <i>Specimen.</i></li>
    <li>Family tradition, as told to the compiler. <i>Specimen.</i></li>
    <li>A county history of 1915, sketch of Otto Brandt. <i>Specimen.</i></li>
    <li>Death certificate of Otto Brandt, 1957. <i>Specimen.</i></li>
    <li>Marriage record of Otto Brandt and Clara, and her gravestone. <i>Specimen.</i></li>
    <li>Birth certificate of Walter J. Brandt, Toledo, 1921. <i>Specimen.</i></li>
    <li>Obituary of Margaret Feld, 2015. <i>Specimen.</i></li>
    <li>Discharge paper of Walter J. Brandt, 1945, held by the family. <i>Specimen.</i></li>
    <li>Death certificate of Walter J. Brandt, 1988. <i>Specimen.</i></li>
    <li>Marriage record of Walter J. Brandt and Ruth E. Lindqvist, 1947, naming both sets of parents. <i>Specimen.</i></li>
    <li>Obituary of Ruth E. Brandt, 2009. <i>Specimen.</i></li>
  </ol>
  <h2 style="margin-top:.8em">Index of names</h2>
  <ul class="idx"><li>Bergström, Hanna</li><li>Bergström, Johan</li><li>Brandt, August <b>1</b></li><li>Brandt, Clara ? <b>2</b></li><li>Brandt, Emma</li><li>Brandt, Margaret</li><li>Brandt, Otto <b>2</b></li><li>Brandt, Walter J. <b>3</b></li><li>Elin ?</li><li>Feld, Harold</li><li>Krause, Wilhelmina <b>1</b></li><li>Lindqvist, Nils</li><li>Lindqvist, Per</li><li>Lindqvist, Ruth E. <b>3</b></li></ul>
  <p class="note" style="margin-top:.8em">A real Project Scroll register is built the same way from your family’s own records. Tell us about your family at projectscroll.com/families.</p>
</div>
</body></html>'''
(R / 'tools' / 'register.html').write_text(html)
print('register.html written')
