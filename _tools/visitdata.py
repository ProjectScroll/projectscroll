"""Shared place data for Visit & Plan, the food page and the pocket guide: every place with a map pin,
the walks' starting points, town labels, and a small SVG map of the valley drawn from the museums base map."""
import json, re, pathlib, urllib.parse
P = pathlib.Path(__file__).parent/'data'
ROOT = pathlib.Path(__file__).parent.parent
ST = {'MI': 'Michigan', 'IN': 'Indiana'}
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
M = json.load(open(P/'museums.json'))
F = [d for d in json.load(open(P/'food.json')) if d.get('keep', True)]
W1 = json.load(open(P/'walk.json')); W2 = json.load(open(P/'walk-dowagiac.json'))

def _mid(rows, key):
    used, out = set(), {}
    for d in rows:
        s = slug(d['name'])
        if s in used: s = slug(d['name']+' '+d['town'])
        used.add(s); out[d['name']] = s
    return out
MID = _mid(M, 'm'); FID = _mid(F, 'f')

def clean_addr(a): return re.sub(r'\s*\((?:mailing|mail:)[^)]*\)', '', a or '').strip()

def mplace(d):
    a = clean_addr(d.get('address'))
    if d.get('ll') and (d.get('approx') or not re.match(r'^\d', a)):
        dest = d['name']+', '+d['town'].split(' (')[0].split(' /')[0]+', '+ST[d['state']]
    else:
        dest = d['name']+', '+a.split(' (')[0]
    return {'i': 'm:'+MID[d['name']], 'n': d['name'], 't': d['town'], 'k': d['kind'], 'g': 'Museums & historic places',
            'll': d.get('ll'), 'd': dest, 'oh': d.get('oh'), 'tz': d.get('tz'), 'u': '/museums/#'+MID[d['name']]}

def fplace(d):
    ll = d.get('ll')
    if isinstance(ll, str): ll = json.loads(ll)
    return {'i': 'f:'+FID[d['name']], 'n': d['name'], 't': d['town'], 'k': d.get('kind', ''),
            'g': 'Places to stay' if d['type'] == 'lodging' else 'Places to eat',
            'll': ll, 'd': d['name']+', '+(d.get('address') or d['town']), 'u': '/food/#'+FID[d['name']]}

WALKS = {
 'walk': {'i': 'w:walk', 'n': 'Broadway Virtual Walk (start)', 't': 'Cassopolis', 'k': 'walking tour', 'g': 'Walking tours',
          'll': [W1['stops'][1]['lat'], W1['stops'][1]['lon']], 'd': 'Cass District Library Local History Branch, 145 N. Broadway, Cassopolis, MI 49031', 'u': '/walk/'},
 'dowagiac': {'i': 'w:dowagiac', 'n': 'Front Street Virtual Walk (start)', 't': 'Dowagiac', 'k': 'walking tour', 'g': 'Walking tours',
          'll': [W2['stops'][0]['lat'], W2['stops'][0]['lon']], 'd': W2['stops'][0]['name']+', '+W2['stops'][0]['address'], 'u': '/walk/dowagiac/'},
}

def all_places():
    out = [WALKS['walk'], WALKS['dowagiac']]
    out += [mplace(d) for d in M if d.get('ll')]
    out += [fplace(d) for d in F if d.get('ll')]
    return out

BYM = {d['name']: d for d in M}; BYF = {d['name']: d for d in F}
def ref(r):
    """('m', name) | ('f', name) | ('w', key) | ('x', name, dest, ll) -> a place dict"""
    if r[0] == 'm': return mplace(BYM[r[1]])
    if r[0] == 'f': return fplace(BYF[r[1]])
    if r[0] == 'w': return WALKS[r[1]]
    return {'i': '', 'n': r[1], 'd': r[2], 'll': r[3] if len(r) > 3 else None}

def gmaps(dests):
    ds = []
    for d in dests:
        if d and (not ds or ds[-1] != d): ds.append(d)
    if not ds: return ''
    ds = ds[:10]
    q = 'https://www.google.com/maps/dir/?api=1&travelmode=driving&destination='+urllib.parse.quote(ds[-1])
    if len(ds) > 1: q += '&waypoints='+'%7C'.join(urllib.parse.quote(x) for x in ds[:-1])
    return q

TOWNS = [('Cassopolis', 41.9065, -86.0127), ('Dowagiac', 41.9836, -86.1061), ('Niles', 41.8296, -86.2528), ('Edwardsburg', 41.7984, -86.0847),
         ('Buchanan', 41.8273, -86.3610), ('Berrien Springs', 41.948, -86.3404), ('St. Joseph', 42.1161, -86.4935), ('Benton Harbor', 42.119, -86.4466),
         ('Coloma', 42.1814, -86.3126), ('South Haven', 42.4065, -86.2743), ('Paw Paw', 42.2178, -85.8911), ('Kalamazoo', 42.2765, -85.607),
         ('Three Rivers', 41.9448, -85.6336), ('Constantine', 41.8397, -85.6647), ('Marcellus', 42.0245, -85.8152), ('South Bend', 41.6758, -86.2521),
         ('Mishawaka', 41.6642, -86.1102), ('Elkhart', 41.6932, -85.9734), ('Goshen', 41.5856, -85.8343), ('Bristol', 41.7217, -85.8202),
         ('Middlebury', 41.6753, -85.7064), ('Shipshewana', 41.6731, -85.5803), ('Nappanee', 41.4428, -85.9994), ('La Porte', 41.5955, -86.7082),
         ('Michigan City', 41.7148, -86.9028), ('Three Oaks', 41.7987, -86.6106), ('Hickory Corners', 42.4402, -85.4201)]

def svg_map(pins=(), w=600, h=420, bounds=(41.40, -86.98, 42.47, -85.35), towns=True, ink='#1D2733', water='#3E7FA8', line='#9AA59A', fill='#F3F5F0'):
    """A plain SVG of the counties and rivers, with optional numbered pins [(lat, lon, label, colour)]."""
    b = json.load(open(ROOT/'museums'/'base.json'))
    s0, w0, n0, e0 = bounds
    import math
    kx = math.cos(math.radians((s0+n0)/2))
    sx = w/((e0-w0)*kx); sy = h/(n0-s0); sc = min(sx, sy)
    ox = (w-(e0-w0)*kx*sc)/2; oy = (h-(n0-s0)*sc)/2
    X = lambda lon: ox+(lon-w0)*kx*sc
    Y = lambda lat: oy+(n0-lat)*sc
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Map of the St. Joseph River valley">',
           f'<rect width="{w}" height="{h}" fill="#D7E6EE"/>']
    for c in b['c']:
        for r in c['r']:
            pts = ' '.join(f'{X(p[0]):.1f},{Y(p[1]):.1f}' for p in r)
            out.append(f'<polygon points="{pts}" fill="{fill}" stroke="{line}" stroke-width=".8"/>')
    for l in b['v']:
        pts = ' '.join(f'{X(p[0]):.1f},{Y(p[1]):.1f}' for p in l)
        out.append(f'<polyline points="{pts}" fill="none" stroke="{water}" stroke-width="1.1" stroke-linejoin="round"/>')
    if towns:
        LEFT = {'St. Joseph', 'Buchanan', 'Mishawaka', 'Middlebury'}; BELOW = {'Mishawaka', 'Middlebury', 'Benton Harbor'}
        for n, la, lo in TOWNS:
            if s0 < la < n0 and w0 < lo < e0:
                tx, an = (X(lo)-4, 'end') if n in LEFT else (X(lo)+4, 'start'); ty = Y(la)+10 if n in BELOW else Y(la)-3
                out.append(f'<circle cx="{X(lo):.1f}" cy="{Y(la):.1f}" r="1.8" fill="{ink}"/><text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{an}" font-family="Georgia,serif" font-size="9" fill="{ink}">{n}</text>')
        out.append(f'<text x="{X(-86.57):.1f}" y="{Y(41.93):.1f}" font-family="Georgia,serif" font-style="italic" font-size="9" fill="{water}" transform="rotate(-66 {X(-86.57):.1f} {Y(41.93):.1f})">St. Joseph River</text>')
        out.append(f'<text x="{X(-86.82):.1f}" y="{Y(42.25):.1f}" font-family="Georgia,serif" font-style="italic" font-size="12" fill="{water}">Lake Michigan</text>')
    seen = []
    for la, lo, lab, col in pins:
        x, y = X(lo), Y(la)
        k = sum(1 for (a, b) in seen if abs(a-x) < 9 and abs(b-y) < 9); seen.append((x, y)); x -= 9 + k*13
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{col}" stroke="#fff" stroke-width="1.2"/><text x="{x:.1f}" y="{y+3:.1f}" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" font-weight="700" fill="#fff">{lab}</text>')
    out.append('</svg>')
    return ''.join(out)
