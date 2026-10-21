"""List every outside link on the built site, one per line, with the pages that use it.
python3 _tools/check/outside.py   (used by the weekly link check; it only reads files)"""
import pathlib, re, collections
R=pathlib.Path(__file__).resolve().parents[2]; seen=collections.defaultdict(set)
for f in R.rglob('*.html'):
    if any(p.startswith(('_','.')) or p in ('vendor','node_modules') for p in f.relative_to(R).parts): continue
    for u in re.findall(r'href="(https?://[^"#]+)', f.read_text(errors='ignore')):
        u=u.replace('&amp;','&')
        if 'projectscroll.com' in u or 'facebook.com' in u or 'm.me/' in u: continue
        u=re.sub(r'(archive\.org/details/[^/]+)/page/.*',r'\1',u); u=re.sub(r'(tile\.loc\.gov/image-services/iiif/[^/]+)/.*',r'\1/info.json',u)
        seen[u].add('/'+str(f.relative_to(R)).replace('index.html',''))
for u in sorted(seen): print(u, '\t', ' '.join(sorted(seen[u])[:3]))
