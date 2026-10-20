# Two pages written for the searches people actually make: "Cassopolis history" and "genealogy research services (Michigan)".
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page

cass='''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Cass County, Michigan</p>
    <h1>Cassopolis, Michigan: its history, in the record</h1>
    <p class="lede">Cassopolis is the county seat of Cass County, Michigan, platted in 1831 and named for Lewis Cass, then governor of Michigan Territory. This page gathers what Project Scroll has opened so far on the village and its county: the maps, the county histories, the certificates and the newspapers, with a link to each record where it is held.</p>
    <h2>The village at a glance</h2>
    <ul>
      <li><b>Founded:</b> platted 1831; chosen as county seat the same year, a compromise between rival settlements.</li>
      <li><b>Named for:</b> Lewis Cass (1782–1866), governor of Michigan Territory 1813–31, later Secretary of War and of State.</li>
      <li><b>First published histories:</b> Howard S. Rogers, <i>History of Cass County, from 1825 to 1875</i> (Cassopolis, 1875); Alfred Mathews, <i>History of Cass County, Michigan</i> (Chicago, 1882); L. H. Glover, <i>A Twentieth Century History of Cass County</i> (Chicago, 1906).</li>
      <li><b>On the map:</b> the 1860 Geil &amp; Harley wall map of Cass County, held by the Library of Congress, carries a plan of the village with lot numbers and owners; you can <a href="/map/cassopolis/">lay it over today’s streets</a>, and the county’s township sheets of about 1928 are <a href="/map/#townships">in the map room</a>.</li>
      <li><b>Vital records:</b> Michigan death certificates from 1897 are free to read at the Archives of Michigan; <a href="/guide/death-certificate/">here is how to read one</a>.</li>
    </ul>
    <figure class="secfig land">
      <a href="/map/#more"><picture><source type="image/webp" srcset="/img/maps/cassopolis-directory-1860-640.webp 640w, /img/maps/cassopolis-directory-1860-1000.webp 1000w" sizes="(min-width:900px) 480px, 92vw"><img src="/img/maps/cassopolis-directory-1860-1000.jpg" srcset="/img/maps/cassopolis-directory-1860-640.jpg 640w, /img/maps/cassopolis-directory-1860-1000.jpg 1000w" sizes="(min-width:900px) 480px, 92vw" width="1000" height="548" loading="lazy" decoding="async" alt="Detail of the 1860 wall map: the business directory beside the Cassopolis plan, listing hotels, merchants, physicians and surgeons."></picture></a>
      <figcaption>Who kept the village in 1860: two hotels, three merchants and three physicians, engraved beside the Cassopolis plan on the county wall map. <span class="credit">Geil, Harley &amp; Siverd, 1860 · Library of Congress</span></figcaption>
    </figure>
    <h2>What the hunt has found in Cassopolis</h2>
    <p>The hunt began here, with a joke secret society of 1846 whose story is told in Rogers and Mathews, a village hotel that was hauled across town and turned into a mill, and a doctor who kept a bone. Each is an open case on <a href="/#cases">the case board</a>; the first two are listed here, and each has its sources free online.</p>
    <ul>
      <li><a href="/cases/1/">Did the joke lodge of 1846 ever have a real charter?</a></li>
      <li><a href="/cases/2/">Where did the Union Hotel go when it became a mill?</a></li>
      <li><a href="/document/">Document of the month: one page of Rogers, 1875, read slowly</a></li>
      <li><a href="/notes/one-letter-two-certificates/">A field note: one letter, two certificates</a></li>
    </ul>
    <h2>The other towns of the valley</h2>
    <p><a href="/dowagiac/">Dowagiac</a> · <a href="/niles/">Niles</a> · <a href="/paw-paw/">Paw Paw</a> — each with its history in the record and its 1860 plan laid over today’s streets.</p>
    <h2>Where to look next</h2>
    <p>For Cassopolis families and property, start with <a href="/records/">where the records are</a>: the county histories at the University of Michigan, the General Land Office tract books, the 1860 wall map, Michigan death certificates, and the Cass District Library’s Local History Branch in Cassopolis itself. The <a href="/glossary/">glossary</a> explains the words the old records use.</p>
    <p class="note">Project Scroll is independent research and is not affiliated with the Village of Cassopolis, Cass County, or any historical society. Corrections are welcome at <a href="mailto:research@projectscroll.com?subject=Cassopolis">research@projectscroll.com</a>.</p>
    <p class="ctas"><a class="btn primary" href="/#hunt">Play the hunt</a> <a class="btn" href="/map/cassopolis/">Cassopolis, 1860 and today</a> <a class="btn" href="/research/">Research services</a></p>
'''
page('cassopolis/index.html', 'Cassopolis, Michigan history and records · Project Scroll',
     'The history of Cassopolis, county seat of Cass County, Michigan, from the record: the 1860 map, the county histories of 1875, 1882 and 1906, certificates and newspapers, each linked where it is held.', cass, og='https://projectscroll.com/og/cassopolis.jpg')

res='''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Professional services</p>
    <h1>Genealogy and local history research services, Michigan and Indiana</h1>
    <p class="lede">Project Scroll’s research desk takes commissions: a lost ancestor traced, a family history or register built from original records, a family legend tested against the record, or local history research for an author, a film or a community group. Based in the St. Joseph River Valley of southwest Michigan and northern Indiana, working anywhere the records reach.</p>
    <h2>What we research</h2>
    <ul>
      <li><b>Lost ancestors.</b> One clear question, answered from certificates, deeds, censuses, county histories, maps and newspapers, every statement marked with its source.</li>
      <li><b>Family histories and registers.</b> Every descendant of one couple, or every ancestor of one person, built from the records and written to be checked. <a href="/families/">See a specimen</a>.</li>
      <li><b>Family legends tested.</b> The famous ancestor, the three brothers who came over together, the land that was taken. We find where the story began and what the records say. <a href="/legends/">How it works</a>.</li>
      <li><b>Local history for authors, films and groups.</b> Research to a brief, with a sourced report you own.</li>
      <li><b>A second pair of eyes.</b> A manuscript, chapter or article checked against its sources before it goes out.</li>
    </ul>
    <h2>Where we work</h2>
    <p>Cass, Berrien, Van Buren and St. Joseph counties in Michigan; St. Joseph and Elkhart counties in Indiana; and, wherever the records are online, anywhere. We read the Michigan county histories, the General Land Office tract books and plats, Michigan and Indiana vital records, and the newspapers of the St. Joseph River Valley as a matter of course.</p>
    <h2>How a commission works</h2>
    <ol>
      <li><b>Tell us what you have.</b> A name, a place, rough dates and what the family says. <a href="/#contact">The form</a> lays it out.</li>
      <li><b>An honest first read, free.</b> We tell you what the records are likely to show, and what it will take, before you commit to anything.</li>
      <li><b>The work, marked.</b> Every claim cited; every gap written down beside what was found.</li>
      <li><b>You own the report.</b> Nothing about your family is published or shared without your word.</li>
    </ol>
    <h2>Also from the studio</h2>
    <p>Digital imaging and restoration of photographs and documents, family-history book design, photography, 3D LiDAR landscape models and short films. <a href="/#studio">The studio</a>.</p>
    <p class="ctas"><a class="btn primary" href="/#contact">Ask about a commission</a> <a class="btn" href="/sample/project-scroll-sample-report.pdf">Sample report (PDF)</a> <a class="btn" href="mailto:research@projectscroll.com?subject=A%20research%20commission">research@projectscroll.com</a></p>
'''
page('research/index.html', 'Genealogy and local history research, Michigan and Indiana · Project Scroll',
     'Professional genealogy and local history research from the St. Joseph River Valley: lost ancestors traced, family histories built from the records, legends tested. Every claim cited.', res, og='https://projectscroll.com/og/services.jpg')
print('landing pages built')

# One page per place, in the same shape as Cassopolis: what the record holds, what the hunt has opened, where to look next.
PLACES=[
 ('dowagiac','Dowagiac','Cass County, Michigan',
  'Dowagiac grew where the Michigan Central Railroad crossed Dowagiac Creek in 1848, and was incorporated as a village in 1863 and a city in 1877. Its name is Potawatomi, from a word usually read as “fishing water.” It became the county’s manufacturing town: the Round Oak Stove works, founded by P. D. Beckwith in 1871, and the grain drills of the Dowagiac Manufacturing Company.',
  [('Founded','settled at the railroad crossing, 1848; village 1863; city 1877'),('Name','Potawatomi, for the creek; several spellings in the early record'),('In the county histories','Rogers (1875), Mathews (1882) and Glover (1906) each give the village its own chapter, with the first merchants, mills and churches named'),('On the map','the 1860 wall map carries a plan of Dowagiac with its lots; <a href="/map/dowagiac/">lay it over today’s streets</a>'),('Industry','Round Oak stoves from 1871; at its height in the 1910s the works employed about 1,200 of the town’s 5,000 people')],
  'Dowagiac’s records are thick: a weekly press from the 1860s and a daily later, the Round Oak company papers, and city directories from the 1890s that list the heads of every household. The desk reads them for Cass County families as a matter of course.',
  'https://projectscroll.com/og/dowagiac.jpg'),
 ('niles','Niles','Berrien County, Michigan',
  'Niles stands on the St. Joseph River beside the site of Fort St. Joseph: a Jesuit mission of 1691 and a French fort of 1697, and four flags have flown there — French, British, Spanish and American — which is why the city calls itself the City of Four Flags. The present town was settled in 1827 and named for Hezekiah Niles, the Baltimore newspaper editor.',
  [('Founded','the mission 1691, the fort 1697; the town settled 1827; village 1835; city 1859'),('Name','for Hezekiah Niles (1777–1839), editor of Niles’ Weekly Register'),('In the record','the Fort St. Joseph archaeological project of Western Michigan University; Ellis’s history of Berrien and Van Buren counties (1880) and Coolidge’s of Berrien (1906); the Niles Republican and Niles Democrat'),('On the map','the 1860 Geil &amp; Harley county map’s Niles inset shows the river through the plan; <a href="/map/niles/">lay it over today’s streets</a>'),('The hunt','Niles is the first town outside Cass County in the hunt, and the river road to it runs through the early cases')],
  'Niles holds the oldest written record in the valley, the Fort St. Joseph registers and the fur-trade accounts, and the best run of nineteenth-century newspapers in the two counties. For families on the Berrien side of the line, start here.',
  'https://projectscroll.com/og/niles.jpg'),
 ('paw-paw','Paw Paw','Van Buren County, Michigan',
  'Paw Paw, the seat of Van Buren County, takes its name from the Paw Paw River and the pawpaw trees that grew along it. Rodney Hinckley took up a farm on the river in 1832, a sawmill followed in 1833, and the village was incorporated in 1837; the Van Buren County Courthouse on Paw Paw Street is on the National Register of Historic Places.',
  [('Founded','settled 1832–33; incorporated 1837; the county seat'),('Name','from the Paw Paw River, itself named for the pawpaw tree'),('In the record','Ellis’s history of Berrien and Van Buren counties (1880) and Rowland’s of Van Buren (1912); the Paw Paw True Northerner, from the 1850s'),('On the map','the 1860 Geil &amp; Harley county map carries a plan of Paw Paw; <a href="/map/paw-paw/">lay it over today’s streets</a>'),('Wine country','grapes are the district’s crop; St. Julian and Warner Vineyards both began in Paw Paw, and the village holds a Wine and Harvest Festival each autumn')],
  'The county seat’s records — probate, deeds and the True Northerner — are the first stop for Van Buren families; the 1912 Rowland history is the fullest for the townships.',
  'https://projectscroll.com/og/pawpaw.jpg'),
]
for slug,name,county,lede,facts,where,og in PLACES:
    items=''.join(f'<li><b>{k}:</b> {v}.</li>' for k,v in facts)
    body=f'''    <p class="crumb"><a href="/cassopolis/">← The places</a></p>
    <p class="kicker">{county}</p>
    <h1>{name}, Michigan: its history, in the record</h1>
    <p class="lede">{lede}</p>
    <h2>The town at a glance</h2>
    <ul>{items}</ul>
    <h2>Where to look</h2>
    <p>{where} The <a href="/records/">records page</a> links each source where it is held, and the <a href="/glossary/">glossary</a> explains the words the old records use.</p>
    <p class="note">Project Scroll is independent research and is not affiliated with the {"Village" if slug=="paw-paw" else "City"} of {name} or any historical society. Corrections are welcome at <a href="mailto:research@projectscroll.com?subject={name}">research@projectscroll.com</a>.</p>
    <p class="ctas"><a class="btn primary" href="/map/{slug}/">{name}, 1860 and today</a> <a class="btn" href="/#hunt">Play the hunt</a> <a class="btn" href="/research/">Research services</a></p>
'''
    page(f'{slug}/index.html', f'{name}, Michigan history and records · Project Scroll',
         f'The history of {name}, Michigan ({county}) from the record: its founding and name, the county histories, the 1860 map over today’s streets, and where its records are held.', body, og=og)
print('place pages built')
