"""Newspaper of the month: one page of a valley paper, read closely.  python3 _tools/build_newspaper.py"""
import sys, pathlib, html; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E=html.escape
I='https://tile.loc.gov/image-services/iiif/service:ndnp:mimtptc:batch_mimtptc_gaylord_ver02:data:sn85033781:00296023826:1899020101:0414'
P='https://www.loc.gov/resource/sn85033781/1899-02-01/ed-1/?sp=8'
CL=[
 ('Our local markets','540,560,1100,1890',
  'This is what Paw Paw dealers paid farmers that week, not what the shops charged. Butter 12 cents (a pound), eggs 14 cents (a dozen), potatoes 25 cents and wheat 65 cents (a bushel). The units were so well known that the paper did not print them. Cattle and hogs were priced by the pound, “on foot” (alive) or dressed. Above the list, the corner of an advertisement for Royal Baking Powder: “Absolutely Pure,” seven years before the Pure Food and Drug Act.'),
 ('The farmers vote','540,3080,1100,1180',
  'A winter farmers’ institute in Van Buren County passed these resolutions. Senators “should be elected by the people”: in 1899 state legislatures still chose them, and the Seventeenth Amendment did not change that until 1913. County officers should draw a salary instead of keeping fees. And fruit should carry “the name and address of the shipper,” an early demand for honest labels from the fruit belt.'),
 ('A dollar a bushel','540,4160,1100,900',
  'A. S. Packard of Covert, “one of the most successful peach growers in the county,” told the institute that his last crop came to about 3,000 bushels and averaged him over a dollar a bushel. Peaches were the money crop of the Michigan fruit belt, and the paper promised to print his paper in full.'),
 ('At what age should a child read?','540,7870,1100,940',
  'The evening session argued about schools. The institute’s president thought a child should be in the second reader by five or six “if it were not for the laziness of parents.” Alice Bangs disagreed: no child ought to begin before six. The paper calls her Miss in one line and Mrs. in the next; the rest of the report says the audience nodded with her.'),
 ('The war at the opera house','1620,5680,1100,1280',
  'Six months after the fighting with Spain ended, a travelling company brought moving pictures of it to Longwell’s opera house for one night, Saturday, 4 February. The Lumière cinématographe had been shown for the first time only four years before. Many “war films” of the day were staged re-enactments, so the audience could not always tell what was real. Admission was 10 and 20 cents.'),
 ('Every soldier, life size','1600,8150,5300,1250',
  'The advertisement across the foot of the page made the real promise: the reviews of the Michigan volunteer regiments would show “every soldier from Paw Paw and vicinity life size so that each and every one can readily be recognized.” Another notice on the page says that at Grand Rapids parents saw sons who had since been buried in Cuba.'),
 ('Saw edges','3770,6000,1110,1100',
  'Men wore detachable starched collars, and a badly ironed one left a rough edge that cut the neck. The Model Steam Laundry on South Kalamazoo Street claimed to be the only laundry in southern Michigan that could take the “saw edges” off.'),
]
def fig(i,t,r,txt):
    from PIL import Image
    W,H=Image.open(pathlib.Path(__file__).parent.parent/f'img/news/c{i}.webp').size; sw=500 if W==900 else 800
    return f'''    <section class="np" id="c{i}"><h2>{E(t)}</h2>
      <figure><a href="{I}/{r}/full/0/default.jpg" rel="noopener" title="Open this clipping at full size at the Library of Congress"><img src="/img/news/c{i}.webp" srcset="/img/news/c{i}-s.webp {sw}w, /img/news/c{i}.webp {W}w" sizes="(min-width:900px) 40rem, 92vw" width="{W}" height="{H}" alt="{E(t)}: a clipping from page 8 of the True Northerner, 1 February 1899." loading="{'eager' if i==0 else 'lazy'}" decoding="async"></a></figure>
      <p>{E(txt)}</p></section>
'''
Q=[('What did a Paw Paw dealer pay for a dozen eggs?','14 cents.'),('Who chose United States senators in 1899?','The state legislatures. Direct election came with the Seventeenth Amendment in 1913.'),('How many bushels of peaches did Mr. Packard grow?','About 3,000, at over a dollar a bushel.'),('What was showing at Longwell’s opera house on 4 February?','Moving pictures of the Spanish-American War, by a Lumière cinématographe company.')]
body=f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Newspaper of the month</p>
    <h1>The True Northerner, 1 February 1899</h1>
    <p class="lede" style="font-size:1.15rem">One page of an old valley paper, read slowly. This month: the back page of Paw Paw’s weekly, in the middle of a Michigan winter, with egg prices, a farmers’ meeting and the war with Spain at the opera house.</p>
    <p>The <i>True Northerner</i> was the weekly of Paw Paw, the seat of Van Buren County. Its back page that week was a working page: the market report, the end of a long account of a farmers’ institute, the circuit court, real-estate sales, and the advertisements that paid for it all. Tap any clipping to see it at full size, or <a href="{P}" rel="noopener">open the whole page</a> at the Library of Congress.</p>
{''.join(fig(i,*c) for i,c in enumerate(CL))}
    <h2>Read the page yourself</h2>
    <div class="npq">{''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in Q)}</div>
    <h2>Reading an old paper</h2>
    <ul class="dis">
      <li><b>Start with the ads and the markets.</b> They tell you what things cost, who kept which shop, and what people wanted to buy.</li>
      <li><b>Read the “continued from” stories.</b> The front page opens a story; the back page often holds the names.</li>
      <li><b>Do not trust the typed text.</b> The searchable text behind a scanned page is machine-read: here it turns “Eggs” into “Kpgs.” Search it, then read the picture.</li>
      <li><b>Find your own town’s paper.</b> Chronicling America and Michigan’s digital newspapers are free. See the <a href="/sources/">sources shelf</a>.</li>
    </ul>
    <p class="note">Source: <i>The True Northerner</i> (Paw Paw, Mich.), 1 February 1899, page 8, digitized by Central Michigan University’s Clarke Historical Library for Chronicling America, Library of Congress. The clippings were cut from the Library’s scan; tap one to open it at full size there. Every quotation on this page was checked against the page image.</p>
'''
page('newspaper/index.html','The True Northerner, 1 February 1899 · Newspaper of the month · Project Scroll','One page of an old valley paper, read slowly: the back page of Paw Paw’s True Northerner for 1 February 1899, with egg prices, a farmers’ institute and the Spanish-American War at the opera house.',body,og='https://projectscroll.com/og/records.jpg')
print('newspaper built',len(CL))
