"""Every page's share tags must sit inside <head>: a stray character in the head ends it early,
and Facebook then ignores the card.  python3 _tools/check/heads.py"""
import pathlib, sys
from html.parser import HTMLParser
R=pathlib.Path(__file__).resolve().parents[2]; bad=[]
class P(HTMLParser):
    def __init__(s): super().__init__(); s.inhead=True; s.og=0; s.why=''
    def handle_data(s,d):
        if s.inhead and d.strip() and not s.lasttag in ('title','script','style','noscript'): s.inhead=False; s.why=repr(d.strip()[:30])
    def handle_starttag(s,t,a):
        if t=='body' or t in ('div','img','aside','main','header','p','section'): s.inhead=False
        if t=='meta' and dict(a).get('property','').startswith('og:') and s.inhead: s.og+=1
for f in sorted(R.rglob('*.html')):
    if 'node_modules' in f.parts or 'vendor' in f.parts or '_tools' in f.parts: continue
    t=f.read_text(errors='ignore')
    if 'property="og:' not in t: continue
    p=P(); p.feed(t)
    if p.og==0: bad.append(f'{f.relative_to(R)}: share tags fall outside <head> {p.why}')
    import re as _re
    m=_re.search(r'property="og:image" content="https://projectscroll\.com/([^"?]+)',t)
    if not m: bad.append(f'{f.relative_to(R)}: no share picture')
    else:
        img=R/m.group(1)
        if not img.exists(): bad.append(f'{f.relative_to(R)}: share picture {m.group(1)} is missing')
        else:
            try:
                from PIL import Image
                w,h=Image.open(img).size
                if (w,h)!=(1200,630): bad.append(f'{f.relative_to(R)}: share picture is {w}x{h}, not 1200x630')
            except Exception as e: bad.append(f'{f.relative_to(R)}: share picture unreadable')
print('\n'.join(bad) or 'heads: every page keeps its share tags in <head>'); sys.exit(1 if bad else 0)
