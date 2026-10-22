"""The valley kitchen as a little booklet: every recipe and household hint on the food page, word for word as printed,
with the note on making it today and the source. Printed to /food/valley-kitchen-recipes.pdf, metadata removed.
python3 _tools/build_recipebook.py"""
import sys, pathlib, json, html
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import visitdata as V
E = lambda s: html.escape(str(s or ''), quote=True)
R = [d for d in json.load(open(V.P/'recipes.json')) if d.get('keep', True)]
R = [d for d in R if d['kind'] == 'recipe'] + [d for d in R if d['kind'] == 'hint']
CSS = '''@page{size:5.5in 8.5in; margin:.55in .5in .6in}
body{font-family:Georgia,"Times New Roman",serif; color:#1D2733; font-size:10pt; line-height:1.4; margin:0}
.cover{height:7.3in; display:flex; flex-direction:column; justify-content:center; text-align:center; page-break-after:always}
.cover h1{font-size:26pt; font-weight:400; margin:.2em 0} .k{letter-spacing:.2em; text-transform:uppercase; font-size:7.5pt; color:#B8892B}
.cover p{margin:.4em 0} .site{color:#B3362B; letter-spacing:.06em}
.r{page-break-inside:avoid; margin:0 0 1.4em; border-top:1px solid #C9CFC6; padding-top:.8em}
.r h2{font-size:14pt; font-weight:400; margin:.1em 0 .3em} .r .m{font-size:7.5pt; letter-spacing:.14em; text-transform:uppercase; color:#B8892B; margin:0}
blockquote{margin:.4em 0; padding-left:.8em; border-left:2px solid #B8892B; font-style:italic}
.today{font-size:9pt} .src{font-size:8pt; color:#4B5663} .note{font-size:8pt; color:#4B5663}'''
def one(d):
    meta = ('Household hint' if d['kind'] == 'hint' else 'Recipe') + (' · '+d['source_place'] if d.get('source_place') else '') + (', '+str(d['year']) if d.get('year') else '')
    return (f'<div class="r"><p class="m">{E(meta)}</p><h2>{E(d["title"])}</h2><blockquote>{E(d["text"])}</blockquote>'
            + (f'<p class="today"><b>Making it today.</b> {E(d["modern"])}</p>' if d.get('modern') else '')
            + f'<p class="src">From {E(d["source_title"])}{(", "+E(d["contributor"])) if d.get("contributor") else ""}.</p></div>')
cover = ('<div class="cover"><p class="k">Project Scroll</p><h1>The Valley Kitchen</h1><p>Recipes and household hints from the old cookbooks and newspapers of the St. Joseph River valley, printed word for word, with a note on making each one today.</p>'
         '<p class="note">Every recipe here was published before 1929 and is in the public domain. The notes on making them today are ours.</p><p class="site">projectscroll.com/food</p></div>')
doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>The Valley Kitchen</title><style>{CSS}</style></head><body>{cover}{"".join(one(d) for d in R)}</body></html>'
try:
    n = V.html_to_pdf(doc, V.ROOT/'food'/'valley-kitchen-recipes.pdf', '5.5in', '8.5in')
    print('recipe booklet built', n, 'pages')
except Exception as e:
    print('recipe booklet skipped:', e)
