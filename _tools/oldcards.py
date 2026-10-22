"""Old postcards and photographs of the valley (public domain), held in img/oldcards/ with their sources in data/oldcards.json."""
import json, pathlib, html, re
D = json.load(open(pathlib.Path(__file__).parent/'data'/'oldcards.json'))
BY = {d['id']: d for d in D}
E = lambda s: html.escape(s or '', quote=True)
GROUPS = [
 ('Cass County, Michigan', [('Cassopolis',['Cassopolis']),('Dowagiac',['Dowagiac']),('Edwardsburg',['Edwardsburg']),('Marcellus',['Marcellus']),('Vandalia',['Vandalia']),('The villages',['Union (Cass County)','Penn (Cass County)','Adamsville (Cass County)','Adamsville'])]),
 ('Southwest Michigan', [('Niles',['Niles']),('Berrien Springs',['Berrien Springs']),('Benton Harbor and St. Joseph',['Benton Harbor','Benton Harbor / St. Joseph','St. Joseph']),('Coloma',['Coloma','Coloma (Paw Paw Lake)']),('Paw Paw',['Paw Paw']),('South Haven',['South Haven']),('Three Rivers',['Three Rivers']),('Constantine',['Constantine']),('White Pigeon',['White Pigeon']),('Kalamazoo',['Kalamazoo'])]),
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
SUBJ=[('streets','Main streets',r'\b(st\.?|street|broadway|main|avenue|birds? ?eye|view|looking|business)\b'),('rail','Depots & railways',r'depot|station|r\.\s?r|railway|train|special|hump|g\. ?t\.'),
 ('civic','Courthouses & halls',r'court ?house|city hall|post ?office|jail|water works|opera'),('schools','Schools & libraries',r'school|library'),
 ('churches','Churches',r'church|chapel'),('inns','Hotels & resorts',r'hotel|inn\b|resort|tavern|hall\b|cottage|pavil'),
 ('work','Mills, farms & industry',r'mill|shovel|works|factory|warehouse|market|peach|orchard|corn|fruit|switchboard|car co|lumber'),
 ('events','Events & people',r'parade|homecoming|day\b|fire|disaster|snow|giants|concert|chautauqua|dedication|contest|spectators|crowd|building the|men building|activities'),
 ('water','Rivers, lakes & parks',r'river|lake|pond|bridge|park|beach|slide|rocky')]
def subjects(d):
    t=d['title'].lower(); out=[k for k,_,rx in SUBJ if re.search(rx,t)]
    return out or ['streets']
def decade(d):
    m=re.search(r'(1[89]\d)\d', d.get('date') or '')
    return (m.group(1)+'0s') if m else ''
def fig(d, sizes='(min-width:900px) 22rem, 46vw'):
    st=' '.join([d['title'],d.get('place') or '',d.get('publisher') or '',d.get('date') or '']).lower()
    return f'<figure class="oc" id="oc-{d["id"]}" data-t="{E(st)}" data-s="{" ".join(subjects(d))}" data-d="{decade(d)}"><a href="/img/oldcards/{d["id"]}.webp" class="oc-a">{pic(d, sizes)}</a><figcaption>{cap(d)}</figcaption></figure>'
def strip(places, n=4, more='/postcards/'):
    xs = [d for d in D if d['place'] in places][:n]
    if not xs: return ''
    return ('    <h2>On old postcards</h2>\n    <div class="oc-grid oc-strip">' + ''.join(fig(d, '(min-width:900px) 14rem, 46vw') for d in xs) +
            f'</div>\n    <p class="note">From public-domain postcards and photographs, each linked to the library that holds it. <a href="{more}">See them all</a>.</p>\n')
def filters():
    decs=sorted({decade(d) for d in D if decade(d)})
    chips=''.join(f'<button type="button" class="btn oc-f" data-s="{k}" aria-pressed="false">{E(n)}</button>' for k,n,_ in SUBJ)
    dch=''.join(f'<button type="button" class="btn oc-dd" data-d="{x}" aria-pressed="false">{x}</button>' for x in decs)
    return ('    <div class="oc-filt" role="search" aria-label="Search the postcards"><label class="nm-q"><span>Search the pictures</span><input type="search" id="ocQ" placeholder="A town, a building, a publisher, a year" autocomplete="off" spellcheck="false"></label>'
            f'<div class="nm-chips" role="group" aria-label="What it shows">{chips}</div><div class="nm-chips" role="group" aria-label="When">{dch}</div>'
            f'<p class="nm-count" id="ocCount" aria-live="polite">{len(D)} pictures</p></div>\n')
def gallery():
    out = [filters()]
    for region, towns in GROUPS:
        out.append(f'    <h2 id="{slug(region)}">{E(region)}</h2>')
        for town, places in towns:
            xs = [d for d in D if d['place'] in places]
            if not xs: continue
            out.append(f'    <h3 id="{slug(town)}">{E(town)}</h3>\n    <div class="oc-grid">' + ''.join(fig(d) for d in xs) + '</div>')
    return '\n'.join(out) + '\n'
