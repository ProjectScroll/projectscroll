"""The libraries behind the stories: every library, archive and collection the news stories draw on, and which stories use each.
python3 _tools/build_libraries.py"""
import sys, json, re, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
R = pathlib.Path(__file__).resolve().parent.parent
E = lambda s: html.escape(str(s), quote=True)
N = json.load(open(R / '_tools/data/news.json'))
# host fragment -> (holder, kind, home, line)
H = [
 ('archive.org', 'Internet Archive', 'lib', 'https://archive.org/', 'Free scans of county histories, session laws, treaties and atlases, most of them from university libraries.'),
 ('hathitrust.org', 'HathiTrust Digital Library', 'lib', 'https://www.hathitrust.org/', 'The research libraries’ shared shelf of scanned books.'),
 ('umich.edu', 'University of Michigan Library', 'lib', 'https://www.lib.umich.edu/', 'Home of the Michigan County Histories collection, where most of the county books are read.'),
 ('umdl.umich.edu', 'University of Michigan Library', 'lib', 'https://www.lib.umich.edu/', ''),
 ('loc.gov', 'Library of Congress', 'lib', 'https://www.loc.gov/', 'Maps, bird’s-eye views, photographs and Chronicling America’s newspapers.'),
 ('hdl.handle.net', 'Library of Congress', 'lib', 'https://www.loc.gov/', ''),
 ('msu.edu', 'Michigan State University Libraries', 'lib', 'https://lib.msu.edu/', 'The map library’s scans of early Michigan maps.'),
 ('newspapers.library.in.gov', 'Indiana State Library: Hoosier State Chronicles', 'news', 'https://newspapers.library.in.gov/', 'Indiana’s free digitized newspapers.'),
 ('digital.library.in.gov', 'Indiana State Library: Indiana Memory', 'lib', 'https://digital.library.in.gov/', ''),
 ('digmichnews.cmich.edu', 'Digital Michigan Newspapers (Clarke Historical Library, Central Michigan University)', 'news', 'https://digmichnews.cmich.edu/', 'Michigan’s free digitized newspapers.'),
 ('cdnc.ucr.edu', 'California Digital Newspaper Collection (UC Riverside)', 'news', 'https://cdnc.ucr.edu/', ''),
 ('kpl.gov', 'Kalamazoo Public Library, Local History', 'lib', 'https://www.kpl.gov/local-history/', ''),
 ('cassdistrictlibrary.org', 'Cass District Library, Local History Branch', 'lib', 'https://www.cassdistrictlibrary.org/', ''),
 ('detroitpubliclibrary.org', 'Detroit Public Library, Burton Historical Collection', 'lib', 'https://digitalcollections.detroitpubliclibrary.org/', ''),
 ('nypl.org', 'New York Public Library', 'lib', 'https://www.nypl.org/', ''),
 ('search.library.wisc.edu', 'University of Wisconsin–Madison Libraries', 'lib', 'https://www.library.wisc.edu/', ''),
 ('lehigh.edu', 'Lehigh University: The Vault at Pfaff’s', 'lib', 'https://pfaffs.web.lehigh.edu/', ''),
 ('fulcrum.org', 'University of Michigan Press (Fulcrum, open access)', 'lib', 'https://www.fulcrum.org/', ''),
 ('okstate.edu', 'Oklahoma State University Libraries: Tribal Treaties Database', 'lib', 'https://treaties.okstate.edu/', ''),
 ('michiganology', 'Archives of Michigan (Michiganology)', 'lib', 'https://michiganology.org/', ''),
 ('nd.edu', 'University of Notre Dame: Building South Bend', 'lib', 'https://buildingsouthbend.nd.edu/', ''),
 ('pastperfectonline.com', 'Indiana Album', 'mus', 'https://www.indianaalbum.com/', ''),
 ('historymuseumsb.org', 'The History Museum, South Bend', 'mus', 'https://historymuseumsb.org/', ''),
 ('edwardsburgmuseum.org', 'Edwardsburg Area Historical Museum', 'mus', 'https://www.edwardsburgmuseum.org/', ''),
 ('ccmihistoricalsociety.org', 'Cass County Historical Society', 'mus', 'https://ccmihistoricalsociety.org/', ''),
 ('friendsofsilverbrook.org', 'Friends of Silverbrook Cemetery', 'mus', 'https://friendsofsilverbrook.org/', ''),
 ('montereyhistory.org', 'Monterey County Historical Society', 'mus', 'https://www.montereyhistory.org/', ''),
 ('doddridgecountyheritageguild.com', 'Doddridge County Heritage Guild', 'mus', 'https://doddridgecountyheritageguild.com/', ''),
 ('marktwainproject.org', 'Mark Twain Project (University of California, Berkeley)', 'lib', 'https://www.marktwainproject.org/', ''),
 ('wikimedia.org', 'Wikimedia Commons', 'web', 'https://commons.wikimedia.org/', ''),
 ('wikipedia.org', 'Wikipedia', 'web', 'https://en.wikipedia.org/', ''),
 ('hmdb.org', 'The Historical Marker Database', 'web', 'https://www.hmdb.org/', ''),
 ('wmuk.org', 'WMUK, Kalamazoo public radio', 'news', 'https://www.wmuk.org/', ''),
 ('wvpe.org', 'WVPE, Elkhart public radio', 'news', 'https://www.wvpe.org/', ''),
 ('leaderpub.com', 'Leader Publications (Dowagiac Daily News)', 'news', 'https://www.leaderpub.com/', ''),
 ('aol.com', 'South Bend Tribune (via AOL News)', 'news', 'https://www.southbendtribune.com/', ''),
]
KIND = [('lib', 'Libraries and archives', 'The libraries that hold the books, maps and papers, and put them online free.'),
        ('news', 'Newspapers and broadcasters', 'Digitized newspapers, and the news people who covered a story first.'),
        ('mus', 'Museums, historical societies and local groups', 'The people who keep a town’s pictures and papers in the town.'),
        ('web', 'Reference sites', 'Useful for pointers and pictures; every fact taken from them is checked against an original where we can.'),
        ('other', 'Other websites', '')]
def holder(u):
    host = re.sub(r'^https?://(www\.)?', '', u).split('/')[0]
    for frag, name, kind, home, line in H:
        if frag in host: return name, kind, home
    return host, 'other', 'https://' + host + '/'
lines = {name: line for frag, name, kind, home, line in H if line}
G = {}
nolink = []
for s in N['stories']:
    for x in s.get('sources', []):
        t, u = x[0], (x[1] if len(x) > 1 else '')
        if not u or not u.startswith('http'):
            if t and not t.lower().startswith(('not yet read', 'the books, newspapers')): nolink.append((t, s))
            continue
        name, kind, home = holder(u)
        g = G.setdefault(name, {'kind': kind, 'home': home, 'stories': {}})
        g['stories'].setdefault(s['slug'], (s, []))[1].append((t, u))
def block(name, g):
    n = sum(len(v[1]) for v in g['stories'].values()); k = len(g['stories'])
    items = ''.join(f'<li><a href="/news/{E(sl)}/">{E(st["headline"])}</a><ul>' + ''.join(f'<li><a href="{E(u)}" rel="noopener">{E(t)}</a></li>' for t, u in srcs) + '</ul></li>' for sl, (st, srcs) in g['stories'].items())
    line = lines.get(name, '')
    return (f'<details class="lb-h"><summary><span class="lb-n"><a href="{E(g["home"])}" rel="noopener">{E(name)}</a></span>'
            f'<span class="lb-c">{n} source{"s" if n != 1 else ""} · {k} stor{"ies" if k != 1 else "y"}</span></summary>'
            + (f'<p class="lb-l">{E(line)}</p>' if line else '') + f'<ul class="lb-s">{items}</ul></details>')
secs = ''
for kind, title, intro in KIND:
    hs = sorted(((n, g) for n, g in G.items() if g['kind'] == kind), key=lambda z: (-sum(len(v[1]) for v in z[1]['stories'].values()), z[0]))
    if not hs: continue
    secs += f'<section class="lb-sec"><h2>{E(title)}</h2>' + (f'<p>{E(intro)}</p>' if intro else '') + ''.join(block(n, g) for n, g in hs) + '</section>'
if nolink:
    secs += ('<section class="lb-sec"><h2>In print, on microfilm and in private hands</h2><p>Sources that are not online yet. Most can be read at the library named.</p><ul class="lb-p">'
             + ''.join(f'<li>{E(t)} <span class="lb-in">· in <a href="/news/{E(s["slug"])}/">{E(s["headline"])}</a></span></li>' for t, s in nolink) + '</ul></section>')
tot = sum(len(v[1]) for g in G.values() for v in g['stories'].values())
body = f'''    <p class="crumb"><a href="/">← Project Scroll</a> · <a href="/sources/">The sources shelf</a></p>
    <article class="lb">
    <p class="kicker">Thank you</p>
    <h1>The libraries behind the stories</h1>
    <p class="lede">Every story on Project Scroll is built from records someone kept. Here are the {len(G)} libraries, archives, papers and collections our news stories draw on, {tot} sources in all, and which stories use each one. Open any of them to see the stories and the exact items.</p>
    {secs}
    <p class="note">Built from the source lists of every news story, and updated each time a story is published. For the county histories and maps behind the hunt itself, with a word on how far to trust each, see <a href="/sources/">the sources shelf</a>. A source missing, or a link that has moved? <a href="mailto:research@projectscroll.com?subject=The%20libraries%20page">Tell us</a>.</p>
    </article>
'''
page('sources/libraries/index.html', 'The libraries behind the stories · Project Scroll', f'The {len(G)} libraries, archives and collections behind Project Scroll’s news stories, and which stories use each one.', body, og='https://projectscroll.com/og/records.jpg')
print('libraries', len(G), 'sources', tot, 'unlinked', len(nolink))
