"""Weekly freshness report for the listing pages (museums, food & lodging, seasons, the walks).
python3 _tools/check/listings.py            prints what needs a human look
python3 _tools/check/listings.py --urls     prints every official website to re-check (one per line: page | name | url)
Report only: it never changes anything."""
import json, os, sys, datetime, glob
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(R, '_tools', 'data')
def load(n):
    p = os.path.join(D, n)
    return json.load(open(p)) if os.path.exists(p) else []
today = datetime.date.today().isoformat()
museums, food, seasons = load('museums.json'), load('food.json'), load('seasons.json')
walks = []
for p in sorted(glob.glob(os.path.join(D, 'walk*.json'))):
    w = json.load(open(p)); walks.append((os.path.basename(p), w.get('stops', [])))
if '--urls' in sys.argv:
    for page, xs in (('museums', museums), ('food', food), ('seasons', seasons)):
        for d in xs:
            if d.get('url'): print(f"{page} | {d['name']} | {d['url']}")
    sys.exit(0)
out = []
# festivals whose known dates are past: their next dates need finding
past = [d['name'] for d in seasons if isinstance(d.get('dates2026'), dict) and (d['dates2026'].get('end') or d['dates2026']['start']) < today]
nodate = [d['name'] for d in seasons if not d.get('dates2026')]
if past: out.append('SEASONS — this year’s dates have passed; look for next year’s on the event’s own site:\n  ' + '\n  '.join(past))
if nodate: out.append('SEASONS — no dates yet (check whether they are posted now):\n  ' + '\n  '.join(nodate))
for page, xs in (('MUSEUMS', museums), ('FOOD & LODGING', food), ('SEASONS', seasons)):
    u = [d['name'] for d in xs if not d.get('verified')]
    if u: out.append(f'{page} — still marked “check before you go”:\n  ' + '\n  '.join(u))
    n = [d['name'] for d in xs if not d.get('url')]
    if n: out.append(f'{page} — no official website on file:\n  ' + '\n  '.join(n))
for f, st in walks:
    u = [s['name'] for s in st if not s.get('verified')]
    if u: out.append(f'WALK ({f}) — stops not yet confirmed:\n  ' + '\n  '.join(u))
print('\n\n'.join(out) if out else 'All listings confirmed and dated.')
