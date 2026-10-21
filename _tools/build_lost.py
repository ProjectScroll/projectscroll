"""Lost towns of the valley, from the county histories.  python3 _tools/build_lost.py"""
import sys, pathlib, html; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E=html.escape
R='https://archive.org/details/historyofcasscou00roge'; M='https://archive.org/details/bad0870.0001.001.umich.edu'; G='https://archive.org/details/twentiethcentury00glov'
B='https://archive.org/details/historyofberrien00ensi'; C='https://archive.org/details/historyofstjosep00chap'; K='https://archive.org/details/historyofelkhart00chic'
T=[
 dict(n='Adamsport and Christiana',aka='later Adamsville',w='Ontwa Township, Cass County, Michigan',ll=(41.7853,-85.9939),
  b='Two little plats faced each other across Christiana Creek: Christiana, laid out by Moses Sage, and Adamsport, laid out by Sterling Adams. The creek turned a grist mill, and a hotel followed. In 1882 the place had 133 people, a hotel, a blacksmith shop, a store and the mill.',
  f='The two plats grew together under one name, Adamsville. When the railroads made new trading towns, it slipped back; by 1906 the mill was its only industry.',
  q=[('Both now are known by the name of Adamsville.','Rogers, 1875',R)],
  d='The histories disagree on dates: Rogers puts Adamsport in September 1832 and Christiana in 1834; Mathews has March 1833 and May 1831.'),
 dict(n='Williamsville',w='Porter Township, Cass County, Michigan',
  b='Josiah Williams laid it out in 1848 and had a hand in its first store. William R. Merritt’s store, opened in 1854, became “the trading place for miles around.” In 1882: two stores, two blacksmiths, a grist mill and a sawmill, one physician, 88 people.',
  f='It simply never grew.',
  q=[('Its population has never reached much beyond the hundred mark.','Glover, 1906',G)],
  d='Rogers says it was laid out in March 1848; Glover says the plat was filed on 5 July 1849.'),
 dict(n='Kessington',aka='also called Sailor',w='Mason Township, Cass County, Michigan',
  b='Moses McKessick platted 19 lots on the Chicago road in 1872. In 1882 it had his general store, a blacksmith shop, a United Brethren church, a few houses and a schoolhouse.',
  f='By 1906 the store and the smithy were gone.',
  q=[('one might drive over this site and notice nothing more remarkable at this country crossroads than a church and a school','Glover, 1906',G)],
  d='Laid out 12 April 1872 (Rogers); the plat was recorded on 22 July (Mathews) or 23 July (Glover).'),
 dict(n='Wakelee',w='where four Cass County townships meet, Michigan',ll=(41.98389,-85.87889),
  b='Levi Garwood laid it out in 1871 on the new Peninsular railroad, later the Grand Trunk, and it was named for the line’s first treasurer, C. Wakelee. In 1882 it had 150 people, a store, a hotel, a blacksmith and a steam sawmill.',
  f='It was a lumber station. When the timber was cut, the reason for it went too; it never incorporated, and its post office is long closed.',
  q=[('a large amount of lumber and wood is shipped from this point.','Mathews, 1882',M)]),
 dict(n='Venice',aka='a paper town',w='Wayne Township, Cass County, Michigan',
  b='In August 1836, at the height of the land boom, Orlando Crane platted Venice on the South Dowagiac Creek: 538 lots and two public squares.',
  f='Not one house was built and not one lot sold. The ground stayed farmland, and the city of Dowagiac later grew over it.',
  q=[('Nothing came of this attempt to boom the location; not a lot was sold','Glover, 1906',G)]),
 dict(n='New Coloma',w='Berrien County, Michigan',
  b='In 1869, while the railroad was being finished, speculators laid out village lots by the line and gave ground for the station. Houses and stores went up.',
  f='The stores closed for want of trade, buyers gave up their lots, and the speculators were left holding the buildings.',
  q=[('New Coloma became a barren reminder of promised greatness','History of Berrien and Van Buren Counties, 1880',B)]),
 dict(n='Dennison, then Lowell',w='across the river from South Bend, Indiana',
  b='In 1837 the company that bought the east bank of the St. Joseph laid out a town opposite South Bend for its water power and mills, and called it Dennison. It was later renamed Lowell.',
  f='It did not die; it was swallowed. South Bend annexed it and it became the city’s fourth ward.',
  q=[('Lowell became a part of the city of South Bend and formed the fourth ward.','Chapman, 1880',C)],
  d='Chapman gives the annexation as December 1866 in one place and 1868 in another.'),
 dict(n='Mount Pleasant',w='German Township, St. Joseph County, Indiana',
  b='Laid out in August 1836 on the Michigan road. It had the township’s first post office, a boot and shoe store, two blacksmith shops and two hotels.',
  f='Soon vacated.',
  q=[('to-day not even a trace of its ruins remain to mark its former existence','Chapman, 1880',C)]),
 dict(n='St. Joseph',aka='the first county seat',w='northwest of South Bend, Indiana',
  b='In 1830 the commissioners fixed the new county’s seat on ground two or three miles northwest of South Bend and laid out a town.',
  f='A year later they moved the seat, South Bend’s offers won, and the town was vacated without a building.',
  q=[('not a single house was ever erected in the place','Chapman, 1880',C)]),
 dict(n='Waterford',aka='Waterford Mills',w='south of Goshen, Elkhart County, Indiana',ll=(41.54306,-85.83056),
  b='Elias Baker built a log house and a grist mill on the Elkhart River in 1833, and the town was laid out in 1838. It had a store, a church and a post office, and in 1851 the county’s first pump factory.',
  f='In 1868 the dam came down and the mill, and then the pump works, moved to Goshen.',
  q=[('the Waterford dam was taken down and the mill removed to Goshen','History of Elkhart County, 1881',K)]),
]
def card(t):
    a=f' <span class="lt-aka">({E(t["aka"])})</span>' if t.get('aka') else ''
    mp=f' · <a href="https://www.openstreetmap.org/?mlat={t["ll"][0]}&amp;mlon={t["ll"][1]}#map=14/{t["ll"][0]}/{t["ll"][1]}" rel="noopener">on today’s map</a>' if t.get('ll') else ''
    qs=''.join(f'<blockquote><p>“{E(q)}”</p><cite><a href="{u}" rel="noopener">{E(s)}</a></cite></blockquote>' for q,s,u in t['q'])
    d=f'<p class="note">{E(t["d"])}</p>' if t.get('d') else ''
    return f'<article class="lt"><h2>{E(t["n"])}{a}</h2><p class="lt-w">{E(t["w"])}{mp}</p><p><b>What was there.</b> {E(t["b"])}</p><p><b>What happened.</b> {E(t["f"])}</p>{qs}{d}</article>'
body=f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Lost towns of the valley</p>
    <h1>Towns that are not there any more</h1>
    <p class="lede" style="font-size:1.15rem">Every county history has a page of places that were platted, named, given a mill or a store, and then left behind. Here are ten from the valley: why they were started, and what became of them.</p>
    <p>Most died the same way. A mill town grew up where a creek could turn a wheel; then the railroad came through somewhere else, trade followed the rails, and the mill was all that was left. Others never lived at all: paper towns drawn up in the land boom of 1836 and sold, or not sold, to people back East.</p>
    {''.join(card(t) for t in T)}
    <h2>How to find a lost town</h2>
    <ul class="dis">
      <li><b>Read the township chapter,</b> not the index. Lost villages are usually a paragraph near the end, under “villages” or “early settlement.”</li>
      <li><b>Look at the old county atlas.</b> A plat of a few blocks in the middle of farmland, with a mill on the creek, is a lost town. The <a href="/map/">map room</a> has the plates.</li>
      <li><b>Check the post office lists.</b> A post office that opened and then closed is often the only date you will get.</li>
      <li><b>Go and look.</b> A road name, a cemetery or a church on a crossroads is often all that survives.</li>
    </ul>
    <p class="note">Sources: Rogers, <i>History of Cass County</i> (1875); Mathews, <i>History of Cass County</i> (1882); Glover, <i>A Twentieth Century History of Cass County</i> (1906); <i>History of Berrien and Van Buren Counties</i> (1880); Chapman, <i>History of St. Joseph County, Indiana</i> (1880); <i>History of Elkhart County, Indiana</i> (1881), all read in the Internet Archive’s copies. Quotations are from the digitized text and the histories sometimes disagree with each other; where they do, both dates are given. Locations on today’s map are from the federal place-name database.</p>
'''
page('lost-towns/index.html','Lost towns of the valley · Project Scroll','Ten towns of the St. Joseph valley that were platted, named and then left behind, from the county histories: why they began and what became of them.',body,og='https://projectscroll.com/og/records.jpg')
print('lost towns built',len(T))
