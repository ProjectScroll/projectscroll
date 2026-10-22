"""The pocket guide: the ready-made days, the two walks and a map of the valley on one sheet (letter, both sides,
folds in three), printed to /visit/project-scroll-pocket-guide.pdf with every bit of document metadata removed.
python3 _tools/build_pocket.py   (needs Playwright's Chromium; skipped quietly if it is missing)"""
import sys, pathlib, json, html, re, subprocess, os, importlib.util
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import visitdata as V
ROOT = pathlib.Path(__file__).parent.parent
E = lambda s: html.escape(str(s), quote=True)
spec = importlib.util.spec_from_file_location('bv', pathlib.Path(__file__).parent/'build_visit.py')
# read DAYS from build_visit without building the page again
src = open(pathlib.Path(__file__).parent/'build_visit.py').read()
ns = {}
exec(src[src.index('DAYS=['):src.index('import oldcards as O')], {'V': V}, ns)
DAYS = ns['DAYS']
COL = ['#B3362B','#2E7D56','#2F6DB5','#8A5A9E','#C77A12','#0F8B8D','#A23B72','#5B7F1F','#6B4F2A']
pins = []
for i,(k,t,w,st) in enumerate(DAYS):
    for a,b,h,r in st:
        if r:
            p = V.ref(r)
            if p.get('ll'): pins.append((p['ll'][0], p['ll'][1], str(i+1), COL[i])); break
svg = V.svg_map(pins, w=520, h=470)
def day(i, d):
    k,t,w,st = d
    rows = ''.join(f'<li><b>{E(a)}</b> {E(b)}</li>' for a,b,h,r in st)
    return f'<div class="day"><h3><span style="background:{COL[i]}">{i+1}</span>{E(t)}</h3><p class="w">{E(w)}</p><ul>{rows}</ul></div>'
D = [day(i,d) for i,d in enumerate(DAYS)]
W1 = json.load(open(V.P/'walk.json')); W2 = json.load(open(V.P/'walk-dowagiac.json'))
def walk(t, W, u):
    S = [s for s in W['stops'] if s.get('keep', True)]
    return f'<div class="walk"><h3>{E(t)}</h3><ol>' + ''.join(f'<li>{E(s["name"])}</li>' for s in S) + f'</ol><p class="u">{u}</p></div>'
LOGO = '<svg viewBox="0 0 32 32" width="34" height="34"><rect x="7" y="4" width="18" height="24" rx="2" fill="none" stroke="#1D2733" stroke-width="2"/><path d="M11 4v24" stroke="#B3362B" stroke-width="2"/><path d="M14 11h7M14 15h7M14 19h5" stroke="#1D2733" stroke-width="1.6"/></svg>'
CSS = '''@page{size:11in 8.5in; margin:0}
*{box-sizing:border-box} body{margin:0; font-family:Georgia,"Times New Roman",serif; color:#1D2733; font-size:7.6pt; line-height:1.28}
.sheet{width:11in; height:8.5in; display:grid; grid-template-columns:repeat(3,1fr); page-break-after:always}
.p{padding:.32in .3in; border-right:1px dashed #C9CFC6; overflow:hidden} .p:last-child{border-right:0}
h2{font-size:11pt; margin:0 0 .5em; font-weight:400; letter-spacing:.02em; border-bottom:1.5px solid #B8892B; padding-bottom:.2em}
h3{font-size:8.6pt; margin:.2em 0 .15em; display:flex; align-items:center; gap:.4em}
h3 span{display:inline-grid; place-items:center; width:1.35em; height:1.35em; border-radius:50%; color:#fff; font:700 7pt Arial,sans-serif; flex:none}
.day{margin-bottom:.75em} .day ul{margin:.2em 0 0; padding-left:1em} .day li{margin:.08em 0} .w{margin:0; color:#4B5663; font-style:italic}
.walk ol{margin:.2em 0 .3em; padding-left:1.4em; columns:1} .u{margin:0 0 .8em; color:#2E7D56}
.cover{display:flex; flex-direction:column; justify-content:space-between; background:#E8ECE6}
.cover h1{font-size:24pt; font-weight:400; margin:.2em 0 .1em} .cover .k{letter-spacing:.18em; text-transform:uppercase; font-size:7pt; color:#B8892B}
.cover .big{font-size:13pt; line-height:1.35} .cover .site{font-size:12pt; color:#B3362B; letter-spacing:.06em}
.map svg{width:100%; height:auto; border:1px solid #C9CFC6} .note{color:#4B5663; font-size:6.8pt}
ul.tips{padding-left:1em; margin:.2em 0} ul.tips li{margin:.15em 0}'''
cover = f'''<div class="p cover"><div><p class="k">Pocket guide</p>{LOGO}<h1>Project Scroll</h1><p class="big">Days out in the St. Joseph River valley: museums, walks, old taverns and orchards, from Kalamazoo to the lakeshore and into northern Indiana.</p></div>
<div><p class="big"><i>Every clue is true.</i></p><p class="site">projectscroll.com/visit</p><p class="note">Open any day in Google Maps, see what is open today, or build your own day at projectscroll.com/visit. Hours change: check each place before you go.</p></div></div>'''
tips = '''<h2>Good to know</h2><ul class="tips">
<li><b>Check before you go.</b> Many museums are run by volunteers and open a few days a week, some only in summer.</li>
<li><b>Mind the clock.</b> La Porte County, Indiana, including La Porte and Michigan City, keeps Central time.</li>
<li><b>Amish country.</b> Many businesses close on Sundays. Slow down and pass buggies wide.</li>
<li><b>Be a good guest.</b> Look from the sidewalk; never go onto private property without leave.</li></ul><p class="note">Project Scroll is free and independent, kept going by sponsors: projectscroll.com/sponsors</p>'''
p1 = f'<div class="sheet"><div class="p"><h2>Days out</h2>{D[0]}{D[1]}{D[2]}</div><div class="p"><h2>More days</h2>{D[3]}{D[4]}{D[5]}</div>{cover}</div>'
p2 = (f'<div class="sheet"><div class="p map"><h2>The valley</h2>{svg}<p class="note">Numbers mark where each day begins. County lines: US Census Bureau. Rivers: USGS.</p>{tips}</div>'
      f'<div class="p"><h2>Further afield</h2>{D[6]}{D[7]}{D[8]}</div>'
      f'<div class="p"><h2>Two walks</h2>{walk("Old Broadway, Cassopolis", W1, "projectscroll.com/walk")}{walk("Front Street, Dowagiac", W2, "projectscroll.com/walk/dowagiac")}'
      f'<p class="note">The walks work on your phone without a signal once opened. Press “I’m here” at each stop for a stamp in your passport.</p></div></div>')
doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Project Scroll pocket guide</title><style>{CSS}</style></head><body>{p1}{p2}</body></html>'
cache = ROOT/'_tools'/'.cache'; cache.mkdir(exist_ok=True)
hp = cache/'pocket.html'; hp.write_text(doc)
out = ROOT/'visit'/'project-scroll-pocket-guide.pdf'; tmp = cache/'pocket-raw.pdf'
js = f'''const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{hp}');await p.pdf({{path:'{tmp}',width:'11in',height:'8.5in',printBackground:true}});await b.close();}})();'''
try:
    root = subprocess.run(['npm','root','-g'], capture_output=True, text=True).stdout.strip()
    subprocess.run(['node','-e',js], check=True, env={**os.environ, 'NODE_PATH': root}, capture_output=True, timeout=120)
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(str(tmp)); w = PdfWriter()
    for pg in r.pages: w.add_page(pg)
    w._info = None
    try: del w._root_object['/Metadata']
    except KeyError: pass
    with open(out, 'wb') as f: w.write(f)
    r2 = PdfReader(str(out)); print('pocket guide built', len(r2.pages), 'pages; metadata:', r2.metadata)
except Exception as e:
    print('pocket guide skipped:', e)
