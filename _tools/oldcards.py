"""Old postcards and photographs of the valley (public domain), held in img/oldcards/ with their sources in data/oldcards.json."""
import json, pathlib, html, re
D = json.load(open(pathlib.Path(__file__).parent/'data'/'oldcards.json'))
BY = {d['id']: d for d in D}
E = lambda s: html.escape(s or '', quote=True)
GROUPS = [
 ('Cass County, Michigan', [('Cassopolis',['Cassopolis']),('Dowagiac',['Dowagiac']),('Edwardsburg',['Edwardsburg']),('Marcellus',['Marcellus']),('Vandalia',['Vandalia']),('The villages',['Union (Cass County)','Penn (Cass County)','Adamsville (Cass County)','Adamsville'])]),
 ('Southwest Michigan', [('Niles',['Niles']),('Berrien Springs',['Berrien Springs']),('Benton Harbor and St. Joseph',['Benton Harbor','Benton Harbor / St. Joseph','St. Joseph']),('Coloma',['Coloma','Coloma (Paw Paw Lake)']),('Paw Paw',['Paw Paw']),('South Haven',['South Haven']),('Three Rivers',['Three Rivers']),('Constantine',['Constantine']),('Kalamazoo',['Kalamazoo'])]),
 ('Northern Indiana', [('South Bend and Mishawaka',['South Bend','South Bend / Mishawaka','Mishawaka']),('Elkhart',['Elkhart']),('Goshen',['Goshen']),('Bristol',['Bristol']),('La Porte',['La Porte']),('Michigan City',['Michigan City'])]),
]
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
SHORT={'David V. Tinder Collection of Michigan Photography, William L. Clements Library, University of Michigan':'Tinder Collection, Clements Library, University of Michigan'}
def credit(d): return SHORT.get(d['credit'], d['credit'])
def cap(d, short=False):
    bits = [d['date']] if d.get('date') else []
    if d.get('publisher') and not short: bits.append(d['publisher'])
    meta = ', '.join(bits)
    src = f' · <a href="{E(d["url"])}" rel="noopener">source</a>' if d.get('url') else ''
    return f'<b>{E(d["title"])}</b>{(" · "+E(meta)) if meta else ""} <span class="credit">{E(credit(d))}{src}</span>'
def pic(d, sizes, lazy=True, cls=''):
    k = d['id']
    return (f'<picture><source type="image/avif" srcset="/img/oldcards/{k}-700.avif 700w, /img/oldcards/{k}.avif {d["w"]}w" sizes="{sizes}">'
            f'<img{(" class=\""+cls+"\"") if cls else ""} src="/img/oldcards/{k}-700.webp" srcset="/img/oldcards/{k}-700.webp 700w, /img/oldcards/{k}.webp {d["w"]}w" sizes="{sizes}" width="{d["w"]}" height="{d["h"]}" alt="{E(d["title"])}, on an old postcard"{" loading=\"lazy\"" if lazy else ""} decoding="async"></picture>')
def fig(d, sizes='(min-width:900px) 22rem, 46vw'):
    return f'<figure class="oc" id="oc-{d["id"]}"><a href="/img/oldcards/{d["id"]}.webp" class="oc-a">{pic(d, sizes)}</a><figcaption>{cap(d)}</figcaption></figure>'
def strip(places, n=4, more='/postcards/'):
    xs = [d for d in D if d['place'] in places][:n]
    if not xs: return ''
    return ('    <h2>On old postcards</h2>\n    <div class="oc-grid oc-strip">' + ''.join(fig(d, '(min-width:900px) 14rem, 46vw') for d in xs) +
            f'</div>\n    <p class="note">From public-domain postcards and photographs, each linked to the library that holds it. <a href="{more}">See them all</a>.</p>\n')
def gallery():
    out = []
    for region, towns in GROUPS:
        out.append(f'    <h2 id="{slug(region)}">{E(region)}</h2>')
        for town, places in towns:
            xs = [d for d in D if d['place'] in places]
            if not xs: continue
            out.append(f'    <h3 id="{slug(town)}">{E(town)}</h3>\n    <div class="oc-grid">' + ''.join(fig(d) for d in xs) + '</div>')
    return '\n'.join(out) + '\n'
