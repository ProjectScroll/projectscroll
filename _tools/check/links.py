"""Every internal link, image and share card on the site must point at something that exists.
python3 _tools/check/links.py"""
import pathlib, re, sys, html
from urllib.parse import urlparse, unquote
R=pathlib.Path(__file__).resolve().parents[2]
pages=[f for f in R.rglob('*.html') if not set(f.parts)&{'node_modules','vendor','_tools','.git'}]
ids={}
def target(u, base):
    u=html.unescape(u); p=urlparse(u)
    if p.scheme in ('http','https'):
        if p.netloc!='projectscroll.com': return None
    elif p.scheme: return None
    path=unquote(p.path)
    if not path: return (base, p.fragment)
    f=(R/path.lstrip('/')) if path.startswith('/') else (base.parent/path)
    if f.is_dir() or path.endswith('/'): f=f/'index.html'
    return (f.resolve(), p.fragment)
bad=[]
for f in pages:
    t=f.read_text(errors='ignore')
    ids[f.resolve()]=set(re.findall(r'\sid="([^"]+)"',t))
for f in pages:
    t=f.read_text(errors='ignore')
    for attr,u in re.findall(r'\s(href|src|content)="([^"]+)"',t):
        if attr=='content' and not u.startswith('https://projectscroll.com/'): continue
        if u.startswith(('mailto:','tel:','javascript:','data:','#')) and not u.startswith('#'): continue
        if '{' in u or "'+" in u or '"+' in u: continue
        tg=target(u,f)
        if not tg: continue
        dest,frag=tg
        if not dest.exists(): bad.append(f'{f.relative_to(R)}: {u} -> missing'); continue
        if frag and dest.suffix=='.html' and frag not in ids.get(dest,set()) and not re.match(r'(town|map|twp|sanborn|case|q)-',frag) and frag not in ('top',):
            bad.append(f'{f.relative_to(R)}: {u} -> no #{frag}')
    if not re.search(r'<title>[^<]{3,}</title>',t): bad.append(f'{f.relative_to(R)}: no <title>')
    if 'name="description"' not in t and 'noindex' not in t: bad.append(f'{f.relative_to(R)}: no description')
bad=sorted(set(bad))
print('\n'.join(bad[:80]) if bad else f'links: {len(pages)} pages, every internal link and image found')
if len(bad)>80: print('…',len(bad),'in all')
sys.exit(1 if bad else 0)
