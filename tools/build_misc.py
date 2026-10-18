"""Builds the notebook page and the search index:  python3 tools/build_misc.py"""
import sys, pathlib, re, json, html; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page, R
page('notebook/index.html','Your notebook · Project Scroll','Your private notes on Project Scroll cases, kept only on this device.','''    <p class="crumb"><a href="/#cases">← The case board</a></p>
    <p class="kicker">Private to this device</p>
    <h1>Your notebook</h1>
    <p>Notes you have written on case pages. They are stored only in this browser: nobody else can see them, and clearing your browser data erases them.</p>
    <div id="nbList"><p class="note">You haven’t written any notes yet. Open a case from <a href="/#cases">the case board</a> to start.</p></div>
    <p class="nbbtns" id="nbAll" hidden><button type="button" class="btn" id="nbDl">Download all notes</button><button type="button" class="btn" id="nbClear">Erase all notes</button></p>
''', noindex=True)
# search index from the built pages
docs=[]
for f in sorted(pathlib.Path(R).rglob('index.html')):
    rel=f.relative_to(R).as_posix()
    if rel.startswith(('tools/','keepsake/','notebook/')): continue
    t=f.read_text()
    url='/'+rel.replace('index.html','')
    title=re.search(r'<title>(.*?)</title>',t,re.S).group(1)
    title=html.unescape(title.split(' · ')[0])
    main=re.search(r'<main[^>]*>(.*?)</main>',t,re.S); body=main.group(1) if main else t
    body=re.sub(r'<(script|style|svg|nav|button|template)\b.*?</\1>','',body,flags=re.S)
    if url=='/':
        # split the home page into its sections
        for m in re.finditer(r'<section id="([\w-]+)"[^>]*>(.*?)</section>',body,re.S):
            h=re.search(r'<h2>(.*?)</h2>',m.group(2)); txt=html.unescape(re.sub(r'<[^>]+>',' ',m.group(2)))
            docs.append({'u':'/#'+m.group(1),'t':html.unescape(re.sub('<[^>]+>','',h.group(1))) if h else m.group(1),'x':re.sub(r'\s+',' ',txt).strip()[:4000]})
        continue
    txt=html.unescape(re.sub(r'<[^>]+>',' ',body))
    docs.append({'u':url,'t':title,'x':re.sub(r'\s+',' ',txt).strip()[:4000]})
G={'Plat':'A surveyor’s drawing of land divided into lots or parcels.','Probate':'The court process that settles a dead person’s estate.','Informant':'The person who answered the questions on a certificate.','Census':'The national head-count taken every ten years.','Soundex':'A code that groups surnames that sound alike, used in old census indexes.','Relict':'A widow: a woman who outlived her husband.'}
for k,v in G.items(): docs.append({'u':'/toolkit/' if k=='Soundex' else '/guide/old-handwriting/' if k=='Relict' else '/#marks','t':'Glossary: '+k,'x':v})
pathlib.Path(R,'search.json').write_text(json.dumps(docs,ensure_ascii=False))
print('notebook + search index:',len(docs),'entries')
