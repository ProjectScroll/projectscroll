# An Atom feed of what is new: field notes, the document of the month, and the cases as they open.
import json, pathlib, re, datetime, html
R=pathlib.Path(__file__).resolve().parent.parent
entries=[]
def add(url,title,summary,date):
    entries.append((date,url,title,summary))
cases=json.load(open(R/'cases.json'))['cases']
def d(s):
    for f in ('%d %b %Y','%d %B %Y'):
        try: return datetime.datetime.strptime(s,f).date().isoformat()
        except Exception: pass
    return datetime.date.today().isoformat()
for c in cases:
    add(f'https://projectscroll.com/cases/{c["n"]}/', f'Case {c["n"]}: {c["question"]}', c.get('hallName',''), d(c.get('opened','')))
for p in sorted((R/'notes').rglob('index.html')):
    rel=p.relative_to(R).as_posix()
    if rel=='notes/index.html' or rel.startswith('notes/book'): continue
    s=p.read_text(encoding='utf-8'); t=re.search(r'<title>(.*?)</title>',s).group(1).split(' · ')[0]; desc=re.search(r'name="description" content="([^"]*)"',s).group(1)
    k=re.search(r'<p class="kicker">[^<]*?(\d{1,2} [A-Z][a-z]+ \d{4})',s)
    add('https://projectscroll.com/'+rel.replace('index.html',''), html.unescape(t), html.unescape(desc), d(k.group(1)) if k else '2026-10-18')
s=(R/'document/index.html').read_text(encoding='utf-8'); desc=re.search(r'name="description" content="([^"]*)"',s).group(1)
add('https://projectscroll.com/document/', 'Document of the month: October 2026', html.unescape(desc), '2026-10-19')
for _i,(_d,_u,_t,_s) in enumerate(json.load(open(R/'_tools'/'data'/'whatsnew.json'))):
    _b,_h=(_u.split('#',1)+[''])[:2]
    add('https://projectscroll.com'+_b+'?new='+_d+'-'+str(_i)+('#'+_h if _h else ''), _t, _s, _d)
for _n in json.load(open(R/'_tools'/'data'/'news.json'))['stories']:
    add('https://projectscroll.com/news/'+_n['slug']+'/', _n['headline'], _n['dek'], _n['date'])
entries.sort(reverse=True)
upd=entries[0][0]+'T12:00:00Z'
x=['<?xml version="1.0" encoding="utf-8"?>','<feed xmlns="http://www.w3.org/2005/Atom">','<title>Project Scroll</title>','<subtitle>An online treasure hunt through real history, from the St. Joseph River Valley. Every clue is true.</subtitle>',
   '<link href="https://projectscroll.com/"/>','<link rel="self" href="https://projectscroll.com/feed.xml"/>','<id>https://projectscroll.com/</id>',f'<updated>{upd}</updated>','<author><name>Project Scroll</name><email>research@projectscroll.com</email></author>']
for date,url,title,summary in entries:
    x.append(f'<entry><title>{html.escape(title)}</title><link href="{url}"/><id>{url}</id><updated>{date}T12:00:00Z</updated><summary>{html.escape(summary)}</summary></entry>')
x.append('</feed>')
(R/'feed.xml').write_text('\n'.join(x)+'\n', encoding='utf-8'); print('feed', len(entries), 'entries')
