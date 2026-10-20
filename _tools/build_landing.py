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
      <li><b>On the map:</b> the 1860 Geil &amp; Harley wall map of Cass County, held by the Library of Congress, carries a plan of the village with lot numbers and owners; you can <a href="/map/cassopolis/">lay it over today’s streets</a>.</li>
      <li><b>Vital records:</b> Michigan death certificates from 1897 are free to read at the Archives of Michigan; <a href="/guide/death-certificate/">here is how to read one</a>.</li>
    </ul>
    <h2>What the hunt has found in Cassopolis</h2>
    <p>The hunt began here, with a joke secret society of 1846 whose story is told in both county histories, a village hotel that was hauled across town and turned into a mill, and a doctor who kept a bone. Each is an open case on <a href="/#cases">the case board</a>, and each has its first sources listed free online.</p>
    <ul>
      <li><a href="/cases/1/">Did the joke lodge of 1846 ever have a real charter?</a></li>
      <li><a href="/cases/2/">Where did the Union Hotel go when it became a mill?</a></li>
      <li><a href="/document/">Document of the month: one page of Rogers, 1875, read slowly</a></li>
      <li><a href="/notes/one-letter-two-certificates/">A field note: one letter, two certificates</a></li>
    </ul>
    <h2>Where to look next</h2>
    <p>For Cassopolis families and property, start with <a href="/records/">where the records are</a>: the county histories at the University of Michigan, the General Land Office tract books, the 1860 wall map, Michigan death certificates, and the Cass District Library’s Local History Branch in Cassopolis itself. The <a href="/glossary/">glossary</a> explains the words the old records use.</p>
    <p class="note">Project Scroll is independent research and is not affiliated with the Village of Cassopolis, Cass County, or any historical society. Corrections are welcome at <a href="mailto:research@projectscroll.com?subject=Cassopolis">research@projectscroll.com</a>.</p>
    <p class="ctas"><a class="btn primary" href="/#hunt">Play the hunt</a> <a class="btn" href="/map/cassopolis/">Cassopolis, 1860 and today</a> <a class="btn" href="/research/">Research services</a></p>
'''
page('cassopolis/index.html', 'Cassopolis, Michigan history: maps, county histories and records · Project Scroll',
     'The history of Cassopolis, Michigan, county seat of Cass County, from the record: the 1860 wall map, the 1875, 1882 and 1906 county histories, death certificates and newspapers, each linked where it is held. Free to read; a history hunt to play.', cass, og='https://projectscroll.com/og/cassopolis.jpg')

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
    <p>Cass, Berrien, Van Buren and St. Joseph counties in Michigan; St. Joseph and Elkhart counties in Indiana; and, through the digitised record, anywhere. We read the Michigan county histories, the General Land Office tract books and plats, Michigan and Indiana vital records, and the newspapers of the St. Joseph River Valley as a matter of course.</p>
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
page('research/index.html', 'Genealogy and local history research services · Michigan and Indiana · Project Scroll',
     'Professional genealogy and local history research from the St. Joseph River Valley: lost ancestors traced, family histories and registers built from original records, family legends tested. Every claim cited. An honest first read, free.', res, og='https://projectscroll.com/og/services.jpg')
print('landing pages built')
