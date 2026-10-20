# The sitemap, from the pages that exist: every index.html not marked noindex, with its real last-modified date.
import pathlib, datetime
R=pathlib.Path(__file__).resolve().parent.parent
SKIP=('_tools','node_modules','.git','hunt','services','studio','notebook','keepsake')
urls=[]
for p in sorted(R.rglob('index.html')):
    rel=p.relative_to(R).as_posix()
    if any(rel.startswith(s+'/') for s in SKIP): continue
    s=p.read_text(encoding='utf-8', errors='ignore')
    if 'name="robots" content="noindex"' in s: continue
    loc='https://projectscroll.com/'+rel.replace('index.html','')
    mod=datetime.date.fromtimestamp(p.stat().st_mtime).isoformat()
    prio='1.0' if rel=='index.html' else ('0.8' if rel.count('/')==1 else '0.6')
    urls.append((loc,mod,prio))
urls.sort(key=lambda u:(u[0]!='https://projectscroll.com/', u[0]))
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{l}</loc><lastmod>{m}</lastmod><priority>{p}</priority></url>\n' for l,m,p in urls)+'</urlset>\n'
(R/'sitemap.xml').write_text(xml, encoding='utf-8'); print('sitemap', len(urls), 'urls')
