"""Draws the hunt's trail map into index.html: python3 tools/build_trailmap.py
To open a hall, set its 'open' to True (and give it a name and a short line)."""
import pathlib, re
HALLS = [
  {'n':'I',   'open':True,  'name':'The first hall',  'line':'The lodge of 1846'},
  {'n':'II',  'open':True,  'name':'The second hall', 'line':'No stream in, no stream out'},
  {'n':'III', 'open':False},
  {'n':'IV',  'open':False},
  {'n':'V',   'open':False},
  {'n':'VI',  'open':False},
  {'n':'VII', 'open':False},
]
PTS = [(70,168),(190,98),(300,160),(410,92),(515,150),(610,86),(680,140)]
def path(pts):
    d=f'M{pts[0][0]} {pts[0][1]}'
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        mx=(x0+x1)/2; d+=f' C{mx} {y0} {mx} {y1} {x1} {y1}'
    return d
lit=[i for i,h in enumerate(HALLS) if h['open']]; last=max(lit)
nopen=len(lit)
svg=[f'<svg viewBox="0 0 740 250" role="img" aria-labelledby="tmT tmD"><title id="tmT">The trail of the hunt</title><desc id="tmD">{nopen} halls are open and lit on the trail. The rest of the trail lies in fog until each hall opens.</desc>',
 '<defs><radialGradient id="tmFog"><stop offset="0" class="tm-f0"/><stop offset=".55" class="tm-f1"/><stop offset="1" class="tm-f2"/></radialGradient></defs>',
 f'<path class="tm-trail" d="{path(PTS)}"/>',
 f'<path class="tm-walked" d="{path(PTS[:last+1])}"/>']
for i,(h,(x,y)) in enumerate(zip(HALLS,PTS)):
    if h['open']:
        ty = y+38 if y>120 else y-44
        svg.append(f'<g class="tm-hall"><circle cx="{x}" cy="{y}" r="17"/><text x="{x}" y="{y+5}" text-anchor="middle" class="tm-n">{h["n"]}</text>'
                   f'<text x="{x}" y="{ty}" text-anchor="middle" class="tm-name">{h["name"]}</text><text x="{x}" y="{ty+17}" text-anchor="middle" class="tm-line">{h["line"]}</text></g>')
    else:
        svg.append(f'<g class="tm-sealed"><title>Hall {h["n"]}: sealed until the hall before it is solved</title><circle cx="{x}" cy="{y}" r="13"/><text x="{x}" y="{y+5}" text-anchor="middle">?</text></g>')
fx=PTS[last+1][0]-30 if last+1<len(PTS) else 760
svg.append(f'<g class="tm-fog"><ellipse cx="{fx+200}" cy="125" rx="170" ry="95"/><ellipse cx="{fx+380}" cy="115" rx="190" ry="105"/><ellipse cx="{fx+95}" cy="185" rx="85" ry="55"/></g>')
svg.append('<g class="tm-rose" transform="translate(705 34)"><circle r="16"/><path d="M0 -20 L4 0 L0 20 L-4 0 Z"/><text y="-24" text-anchor="middle">N</text></g>')
svg.append('</svg>')
fig=('<figure class="trailmap" aria-label="The trail of the hunt">\n        '+''.join(svg)+
     f'\n        <figcaption>Halls light up on the trail as they open. {nopen} are lit; the rest of the way is still in fog.</figcaption>\n      </figure>')
p=pathlib.Path(__file__).resolve().parent.parent/'index.html'; s=p.read_text(encoding='utf-8')
new=re.sub(r'<figure class="(?:halls|trailmap)".*?</figure>', fig, s, count=1, flags=re.S)
assert new!=s or fig in s
p.write_text(new, encoding='utf-8'); print('trail map drawn:', nopen, 'open')
