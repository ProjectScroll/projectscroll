"""Builds the notebook page and the search index:  python3 _tools/build_misc.py"""
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
    if rel.startswith(('_tools/','tools/','hunt/','services/','studio/','keepsake/','notebook/')): continue
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
# each township sheet of about 1928 is its own result, so a search for "Calvin" or "Volinia" opens it
TWP=[('calvin','Calvin','Brownsville, Calvin Center'),('howard','Howard',''),('jefferson','Jefferson',''),('lagrange','LaGrange','LaGrange village, Cassopolis'),('marcellus','Marcellus','Marcellus village'),('mason','Mason',''),('milton','Milton',''),('newberg','Newberg',''),('ontwa','Ontwa','Edwardsburg, Adamsville'),('penn','Penn','Vandalia, Diamond Lake'),('pokagon','Pokagon','Pokagon village, Sumnerville'),('porter-north','Porter','Williamsville (north half)'),('porter-south','Porter','Union (south half)'),('silver-creek','Silver Creek','Indian Lake'),('volinia','Volinia','Nicholsville'),('wayne','Wayne','Glenwood')]
for k,n,v in TWP:
    docs.append({'u':'/map/#twp-'+k,'t':n+' Township plat, about 1928','x':n+' Township, Cass County, Michigan: the plat sheet of about 1928, every farm with its owner’s name and acreage. '+(('On the sheet: '+v+'. ') if v else '')+'Open it in the map room and compare the names with the 1860 wall map.'})
TOWNS=[('buchanan','Buchanan','its town plan on the 1860 wall map'),('berrien','Berrien Springs','the plan of Berrien, now Berrien Springs, on the 1860 wall map'),('decatur','Decatur','its town plan on the 1860 wall map'),('edwardsburg','Edwardsburg','its town plan on the 1860 wall map'),('lawton','Lawton','its town plan on the 1860 wall map'),('st-joseph','St. Joseph','its town plan on the 1860 wall map'),('three-rivers','Three Rivers','the 1858 map of St. Joseph County, Michigan'),('constantine','Constantine','the 1858 map of St. Joseph County, Michigan'),('centreville','Centreville','the 1858 map of St. Joseph County, Michigan'),('white-pigeon','White Pigeon','the 1858 map of St. Joseph County, Michigan'),('kalamazoo','Kalamazoo','Geil & Harley’s map of Kalamazoo County'),('coloma','Coloma','its town plan on the 1860 wall map'),('hartford','Hartford','the plan of Hartford Center on the 1860 wall map'),('lawrence','Lawrence','its town plan on the 1860 wall map'),('mattawan','Mattawan','its town plan on the 1860 wall map'),('south-bend','South Bend','its town plan on the 1863 map of St. Joseph County, Indiana'),('mishawaka','Mishawaka','its town plan on the 1863 map of St. Joseph County, Indiana'),('roseland','Roseland','the ground where it grew, on the 1863 map of St. Joseph County, Indiana'),('granger','Granger','Harris Township, where it grew, on the 1863 map of St. Joseph County, Indiana'),('osceola','Osceola','the 1863 map of St. Joseph County, Indiana'),('new-carlisle','New Carlisle','the 1863 map of St. Joseph County, Indiana'),('lakeville','Lakeville','the 1863 map of St. Joseph County, Indiana'),('north-liberty','North Liberty','the 1863 map of St. Joseph County, Indiana'),('walkerton','Walkerton','the 1863 map of St. Joseph County, Indiana'),('elkhart','Elkhart','its town plan on the 1861 map of Elkhart County, Indiana'),('goshen','Goshen','its town plan on the 1861 map of Elkhart County, Indiana'),('bristol','Bristol','its town plan on the 1861 map of Elkhart County, Indiana'),('middlebury','Middlebury','its town plan on the 1861 map of Elkhart County, Indiana'),('wakarusa','Wakarusa','its town plan on the 1861 map of Elkhart County, Indiana'),('benton-harbor','Benton Harbor','the Benton Township plate of Graves’s Atlas of Berrien County'),('grand-rapids','Grand Rapids','the Grand Rapids Township plate of Polk’s 1894 atlas of Kent County')]
for k,n,v in TOWNS:
    docs.append({'u':'/map/#town-'+k,'t':n+' on the old map','x':n+': '+v+', in the map room.'})
# the roll of names: one result per town directory, so a surname search finds it
sys.path.insert(0, str(pathlib.Path(__file__).parent/'data'))
from directories import DIRS
for k,d in DIRS.items():
    docs.append({'u':'/names/?town='+k,'t':'Names in the '+d['year']+' '+d['name']+' directory','x':d['name']+' business directory, '+d['year']+': '+'; '.join(nm.rstrip('?')+(', '+nt if nt else '') for _,nm,nt in d['entries'])})
pathlib.Path(R,'search.json').write_text(json.dumps(docs,ensure_ascii=False))
print('notebook + search index:',len(docs),'entries')
