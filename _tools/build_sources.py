"""The sources shelf: every book, map and archive the site draws on, with a line on how far to trust it.
python3 _tools/build_sources.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
H='http://hdl.loc.gov/loc.gmd/'
SHELF=[
 ('County histories', 'Written a generation or two after the events, mostly from the recollections of old settlers, and paid for by subscribers whose biographies they print. Rich in names and dates, wrong often enough that every fact should be checked against a deed, a census or a newspaper.', [
  ('Howard S. Rogers', 'History of Cass County, from 1825 to 1875', 'Cassopolis: W. H. Mansfield, 1875', 'https://name.umdl.umich.edu/BAD0871.0001.001', 'University of Michigan Library', 'The earliest county history, closest to the first settlers. Short, and often the source the later books copy.'),
  ('Alfred Mathews', 'History of Cass County, Michigan', 'Chicago: Waterman, Watkins &amp; Co., 1882', 'https://name.umdl.umich.edu/BAD0870.0001.001', 'University of Michigan Library', 'Much longer, with township and village histories and biographies. Repeats Rogers in places, adds new witnesses in others; its footnotes say who told what.'),
  ('L. H. Glover', 'A Twentieth Century History of Cass County, Michigan', 'Chicago: Lewis Publishing, 1906', 'https://name.umdl.umich.edu/ARH7771.0001.001', 'University of Michigan Library', 'The county as it stood a generation later. Good on churches, schools and businesses of its day; leans on the earlier books for the pioneer years.'),
  ('', 'Portrait and Biographical Record of Berrien and Cass Counties, Michigan', 'Chicago: Biographical Publishing Co., 1893', '', '', 'Subscription biographies, written with the families. Strong on births, marriages and children; kind to its subjects.'),
 ]),
 ('County and town maps', 'Landownership maps were sold by subscription, so the names on the farms and the directories beside the town plans are the people who paid. The streets, lots and buildings are usually true to the ground; the names are a snapshot of one year.', [
  ('Geil, Harley &amp; Siverd', 'Map of the Counties of Cass, Van Buren and Berrien, Michigan', 'Philadelphia, 1860', H+'g4113c.la000324', 'Library of Congress', 'The wall map at the heart of the map room, with its town plans and business directories.'),
  ('', 'Map of St. Joseph County, Michigan', '1858', H+'g4113s.la000356', 'Library of Congress', 'The neighbouring county two years earlier: Three Rivers, Constantine, Centreville, White Pigeon.'),
  ('Geil &amp; Harley', 'Map of Kalamazoo County, Michigan', '1861', H+'g4113k.la000336', 'Library of Congress', 'Kalamazoo, Portage, Schoolcraft and the ground where Vicksburg grew.'),
  ('M. W. Stokes', 'Map of St. Joseph Co., Indiana', 'South Bend, 1863', 'https://www.loc.gov/item/2013593163/', 'Library of Congress', 'South Bend and Lowell, Mishawaka and the townships, with engraved views.'),
  ('Geil &amp; Harley', 'Map of Elkhart Co. Indiana', 'Philadelphia: Samuel Geil, 1861', 'https://collections.lib.uwm.edu/digital/collection/agdm/id/21064', 'American Geographical Society Library, University of Wisconsin–Milwaukee', 'Goshen, Elkhart, Bristol, Middlebury and the farms between.'),
  ('W. W. Graves', 'Atlas of Berrien County, Michigan', 'Chicago: Rand McNally', 'https://name.umdl.umich.edu/2911279.0001.001', 'University of Michigan Library', 'Township plates with every farm, from Benton to Three Oaks.'),
  ('R. L. Polk &amp; Co.', 'Illustrated Historical Atlas of Kent County, Michigan', '1894', 'https://name.umdl.umich.edu/3927849.0001.001', 'University of Michigan Library', 'Grand Rapids Township and the city’s edge.'),
  ('', 'Plat book of Cass County, Michigan', 'about 1928', 'https://migenweb.org/cass/townships.htm', 'scans contributed by Ross Traverse to the Cass County MIGenWeb Project', 'The township sheets of about 1928, for following a farm from 1860 to the age of the automobile.'),
 ]),
 ('Views, plans and insurance maps', 'Bird’s-eye views were drawn to sell a town, so they flatter it, but the streets and big buildings are carefully placed. Fire-insurance maps were drawn for underwriters and are the most exact record of buildings there is.', [
  ('', 'Bird’s-eye views of Niles (1868), South Bend (1866, 1874, 1890), Kalamazoo (1874), Benton Harbor (1889) and Grand Rapids (1868)', '', 'https://www.loc.gov/collections/panoramic-maps/', 'Library of Congress, Panoramic Maps', 'Every house and tree, as the artist chose to show it.'),
  ('Sanborn Map Company', 'Fire insurance maps of the valley’s towns', 'from the 1880s', 'https://www.loc.gov/collections/sanborn-maps/', 'Library of Congress, through Wikimedia Commons', 'Building by building: wood or brick, stories, stores and stables.'),
  ('Jacques-Nicolas Bellin', 'Carte des Lacs du Canada', 'Paris, 1744', '', '', 'The Great Lakes as French mapmakers knew them, long before the first county was drawn.'),
 ]),
 ('Records to search yourself', 'The first-hand record: made at the time, by someone with a reason to get it right. Still not perfect; see the guides.', [
  ('Archives of Michigan', 'Michigan death certificates, 1897–1952', '', 'https://michigan.access.preservica.com/death-certificates-1897-1952/', 'Michiganology', 'Free to search and view. Read our <a href="/guide/death-certificate/">guide to the death certificate</a> first.'),
  ('Bureau of Land Management', 'General Land Office records', '', 'https://glorecords.blm.gov/', 'BLM', 'The first sale of every piece of public land, with the buyer’s name and the date.'),
  ('Library of Congress', 'Chronicling America', '', 'https://www.loc.gov/collections/chronicling-america/', 'Library of Congress', 'Digitized newspapers, searchable by word.'),
  ('Clarke Historical Library', 'Digital Michigan Newspapers', '', 'https://www.cmich.edu/research/cmu-library/collections/michigan-digital-newspapers', 'Central Michigan University', 'Michigan papers, including some from the valley.'),
  ('Indiana State Library', 'Hoosier State Chronicles', '', 'https://newspapers.library.in.gov/', 'Indiana State Library', 'Indiana papers, for South Bend, Elkhart and Goshen.'),
  ('Cass District Library', 'Cass County plat maps', '', 'https://www.cassdistrictlibrary.org/cass-county-plat-maps/', 'Cass District Library', 'Plat books of later years, for carrying a farm forward.'),
 ]),
]
out=[]
for shelf,trust,items in SHELF:
    lis=[]
    for au,ti,pub,url,held,note in items:
        t=f'<a href="{url}" rel="noopener"><i>{ti}</i></a>' if url else f'<i>{ti}</i>'
        lis.append(f'      <li>{(au+", ") if au else ""}{t}{(" ("+pub+")") if pub else ""}.{(" <span class=\"sh-h\">"+held+"</span>") if held else ""}<br><span class="sh-n">{note}</span></li>')
    out.append(f'''    <h2>{shelf}</h2>
    <p class="sh-t"><b>How far to trust them.</b> {trust}</p>
    <ul class="shelf">
{chr(10).join(lis)}
    </ul>''')
body=f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">The sources shelf</p>
    <h1>What the hunt is built on</h1>
    <p class="lede" style="font-size:1.15rem">Every clue on Project Scroll comes from a book, a map or a record you can open yourself. Here they are on one shelf, with where to read each one free and a plain word on how far to trust it.</p>
{chr(10).join(out)}
    <p class="note">For the free archives to search, country by country, see <a href="/records/">where the records are</a>. For the names in the town directories, see <a href="/names/">who was in town</a>.</p>
'''
page('sources/index.html','The sources shelf · Project Scroll','Every county history, map and archive Project Scroll draws on, with where to read it free and a plain word on how far to trust it.',body,og='https://projectscroll.com/og/records.jpg')
print('sources shelf built')
