"""Two printables: the paper passport (a stamp box for every place the site's passport counts) and the teachers' pack
(a field-trip day, the rephotography worksheet and a record-reading worksheet). Metadata removed from both.
python3 _tools/build_booklets.py"""
import sys, pathlib, json, html
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import visitdata as V
E = lambda s: html.escape(str(s or ''), quote=True)
LOGO = '<svg viewBox="0 0 32 32" width="30" height="30"><rect x="7" y="4" width="18" height="24" rx="2" fill="none" stroke="#1D2733" stroke-width="2"/><path d="M11 4v24" stroke="#B3362B" stroke-width="2"/><path d="M14 11h7M14 15h7M14 19h5" stroke="#1D2733" stroke-width="1.6"/></svg>'
BASE = '''body{font-family:Georgia,"Times New Roman",serif; color:#1D2733; margin:0} h1{font-weight:400} h2{font-weight:400; border-bottom:1.5px solid #B8892B; padding-bottom:.15em}
.k{letter-spacing:.2em; text-transform:uppercase; font-size:7.5pt; color:#B8892B} .note{color:#4B5663} .site{color:#B3362B}'''

# ---------- the paper passport ----------
M = [d for d in V.M if d.get('ll')]
F = [d for d in V.F if d.get('ll')]
W1 = [s for s in V.W1['stops'] if s.get('keep', True)]; W2 = [s for s in V.W2['stops'] if s.get('keep', True)]
S = [d for d in json.load(open(V.P/'seasons.json')) if d.get('ll')]
def boxes(rows):
    return '<div class="g">' + ''.join(f'<div class="b"><div class="st"></div><p><b>{E(n)}</b><br>{E(t)}</p></div>' for n, t in rows) + '</div>'
secs = []
for st in ('MI', 'IN'):
    xs = sorted([d for d in M if d['state'] == st], key=lambda d: (d['county'], d['town'], d['name']))
    secs.append(f'<h2>Museums &amp; historic places · {V.ST[st]}</h2>' + boxes([(d['name'], d['town']) for d in xs]))
secs.append('<h2>Old Broadway, Cassopolis</h2>' + boxes([(s['name'], 'Stop '+str(i+1)) for i, s in enumerate(W1)]))
secs.append('<h2>Front Street, Dowagiac</h2>' + boxes([(s['name'], 'Stop '+str(i+1)) for i, s in enumerate(W2)]))
secs.append('<h2>Tables &amp; inns</h2>' + boxes([(d['name'], d['town']) for d in sorted(F, key=lambda d: (d['state'] != 'MI', d['town'], d['name']))]))
secs.append('<h2>Festivals</h2>' + boxes([(d['name'], d['town']) for d in sorted(S, key=lambda d: (d['month'], d['name']))]))
CSS1 = BASE + '''@page{size:5.5in 8.5in; margin:.45in .4in .5in} body{font-size:7pt}
.cover{box-sizing:border-box; height:7.3in; display:flex; flex-direction:column; justify-content:center; text-align:center; page-break-after:always; border:2px solid #B8892B; padding:.3in}
.cover h1{font-size:28pt; margin:.2em 0} .line{border-bottom:1px solid #1D2733; height:1.6em; margin:.6em 1.2in}
h2{font-size:10pt; margin:.9em 0 .4em; page-break-after:avoid}
.g{display:grid; grid-template-columns:repeat(4,1fr); gap:.08in} .b{border:1px solid #C9CFC6; padding:.04in; page-break-inside:avoid}
.st{height:.62in; border:1px dashed #C9B98F; margin-bottom:.03in} .b p{margin:0; font-size:6.3pt; line-height:1.2}'''
cover1 = (f'<div class="cover"><p class="k">Project Scroll</p>{LOGO}<h1>Passport</h1><p>of the St. Joseph River valley</p><div class="line"></div><p class="note">Name</p>'
          '<p class="note" style="margin-top:.4in">Ask for a stamp, a signature or a date at each place you visit, or write the date yourself. '
          'Press “I’m here” on the website too, and the stamp is kept on your phone, with badges at ten, twenty-five and fifty.</p><p class="site">projectscroll.com/passport</p></div>')
doc1 = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Passport</title><style>{CSS1}</style></head><body>{cover1}{"".join(secs)}</body></html>'

# ---------- the teachers' pack ----------
W = json.load(open(V.P/'walk.json'))
CSS2 = BASE + '''@page{size:8.5in 11in; margin:.6in .7in} body{font-size:10.5pt; line-height:1.45}
.pg{page-break-after:always} h1{font-size:22pt; margin:.1em 0 .3em} h2{font-size:13pt; margin:1em 0 .4em}
table{border-collapse:collapse; width:100%} td,th{border:1px solid #C9CFC6; padding:.35em .5em; vertical-align:top; text-align:left; font-size:10pt}
.ans td{height:2.3em} .box{border:1px solid #C9CFC6; height:2.6in; margin:.3em 0} li{margin:.25em 0}'''
p1 = f'''<div class="pg"><p class="k">Project Scroll · for teachers</p>{LOGO}<h1>A field day in Cassopolis</h1>
<p>A one-day local-history field trip for upper elementary through high school, built from the Local History Branch, the old courthouse and the Broadway walk. Everything on the walk is seen from the sidewalk.</p>
<h2>The day</h2><table><tr><th>When</th><th>Where</th><th>What students do</th></tr>
<tr><td>Morning</td><td>The Broadway walk, Cassopolis (eleven stops)</td><td>Walk old Broadway with the 1860 town plan. At each stop, note one thing that is the same as on the old plan and one that has changed.</td></tr>
<tr><td>Late morning</td><td>The Local History Branch, 145 N. Broadway (Mon–Thu)</td><td>Look at a county history, a directory and a plat map. Call ahead to arrange a class visit: 269-357-7823.</td></tr>
<tr><td>Lunch</td><td>Bring a picnic, or eat on Broadway</td><td>Compare prices in the 1899 newspaper of the month with today’s.</td></tr>
<tr><td>Afternoon</td><td>Photo spots on the walk</td><td>Rephotograph an old postcard (worksheet 1), from the sidewalk, never the road.</td></tr>
<tr><td>Back in class</td><td>Anywhere</td><td>Read a record together (worksheet 2), and send the class’s best then-and-now photo to Project Scroll.</td></tr></table>
<h2>Before you go</h2><ul><li>Check the Local History Branch’s hours and tell them you are coming.</li><li>Many buildings on the walk are homes and businesses: stay on public ground.</li>
<li>The walk works on a phone without a signal once opened: projectscroll.com/walk</li><li>Four free lessons, ready to teach, are at projectscroll.com/classrooms</li></ul>
<p class="note">Times and hours change: check each place before the trip. Project Scroll is independent and free to use in class.</p></div>'''
p2 = '''<div class="pg"><p class="k">Worksheet 1</p><h1>Stand where the photographer stood</h1><p>Name __________________________ Date ____________</p>
<ol><li>Which postcard did you choose? Write its title and date.<div class="box" style="height:.6in"></div></li>
<li>Find two things that have not moved since the card was made (a building corner, a street, a roofline).<div class="box" style="height:.7in"></div></li>
<li>Stand where the photographer stood. Use your ordinary camera, not the wide one, and do not zoom. Take the picture.</li>
<li>Draw or describe what has changed: buildings, signs, trees, the road, the people, the vehicles.<div class="box"></div></li>
<li>What has stayed the same? Why do you think it lasted?<div class="box" style="height:1.1in"></div></li></ol>
<p class="note">Send the best pair to research@projectscroll.com with a parent’s or teacher’s permission. It can go up on the website beside the old card, with the class’s name.</p></div>'''
p3 = '''<div class="pg"><p class="k">Worksheet 2</p><h1>Reading a record</h1><p>Name __________________________ Date ____________</p>
<p>Choose one old record: a death certificate, a census page, a directory line or a county-history paragraph. The guides at projectscroll.com/guide help with old handwriting and death certificates.</p>
<table class="ans"><tr><th style="width:38%">Question</th><th>Your answer</th></tr>
<tr><td>What kind of record is it?</td><td></td></tr><tr><td>Who made it, and when?</td><td></td></tr><tr><td>Who gave the information? Were they there?</td><td></td></tr>
<tr><td>Name one fact it states.</td><td></td></tr><tr><td>Where else could you check that fact?</td><td></td></tr><tr><td>Is anything hard to read? Copy it exactly, with [?] for the letters you can’t make out.</td><td></td></tr>
<tr><td>Does it disagree with another record? Which do you trust more, and why?</td><td></td></tr></table>
<h2>The rule of the hunt</h2><p>Every clue is true, and every answer is in the record. A good answer says where it was found: the record, the page, and a link if there is one.</p></div>'''
doc2 = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Teachers pack</title><style>{CSS2}</style></head><body>{p1}{p2}{p3}</body></html>'
try:
    n1 = V.html_to_pdf(doc1, V.ROOT/'passport'/'project-scroll-paper-passport.pdf', '5.5in', '8.5in')
    n2 = V.html_to_pdf(doc2, V.ROOT/'classrooms'/'project-scroll-teachers-pack.pdf', '8.5in', '11in')
    print('booklets built', n1, n2)
except Exception as e:
    print('booklets skipped:', e)
