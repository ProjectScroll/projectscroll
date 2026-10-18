"""Builds the records directory, the glossary and the about page:  python3 tools/build_more.py"""
import sys, pathlib, re; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page

# ------------------------------------------------------------------ records
REC = [
 ('Everywhere', 'Start here, wherever your people lived', [
  ('FamilySearch', 'https://www.familysearch.org/', 'Free with an account. Billions of indexed records and millions of filmed ones: censuses, vital records, probate, land and church books worldwide.', 'free'),
  ('The FamilySearch Research Wiki', 'https://www.familysearch.org/en/wiki/', 'What records exist for any country, state or county, and where they are kept. The best first stop for a new place.', 'free'),
  ('Internet Archive', 'https://archive.org/', 'County histories, family genealogies, city directories and old books, free to read and search.', 'free'),
  ('HathiTrust', 'https://www.hathitrust.org/', 'Millions of digitized library books. Full text search finds a name inside books you didn’t know existed.', 'free'),
  ('Chronicling America', 'https://www.loc.gov/collections/chronicling-america/', 'The Library of Congress’s free historic newspapers, from every state.', 'free'),
  ('National Archives: genealogy', 'https://www.archives.gov/research/genealogy', 'Census, military service and pension files, immigration and naturalization records of the United States.', 'free'),
  ('Library of Congress maps', 'https://www.loc.gov/maps/', 'County wall maps, atlases, town plans and panoramic views, many in deep zoom.', 'free'),
  ('David Rumsey Map Collection', 'https://www.davidrumsey.com/', 'Over a hundred thousand historic maps and atlases online, free to view.', 'free'),
  ('Land patents (BLM General Land Office)', 'https://glorecords.blm.gov/', 'The first sale of federal land to a private owner, with surveyors’ plats and field notes, for the public-land states.', 'free'),
  ('USGenWeb', 'https://usgenweb.org/', 'Volunteer sites for every state and county: transcribed records, cemetery lists, biographies and local know-how.', 'free'),
  ('Ellis Island passenger search', 'https://heritage.statueofliberty.org/', 'Arrival lists for the port of New York, 1820–1957.', 'free'),
 ]),
 ('Michigan', 'Where Project Scroll began', [
  ('Michiganology: vital records', 'https://michiganology.org/vital-records/', 'The Archives of Michigan’s death certificates, 1897–1952, and more, free to search and view.', 'free'),
  ('Michigan County Histories and Atlases', 'https://quod.lib.umich.edu/m/micounty', 'The University of Michigan’s collection of the old county histories and atlases, full text.', 'free'),
  ('Michigan Digital Newspapers', 'https://www.cmich.edu/research/cmu-library/collections/michigan-digital-newspapers', 'Central Michigan University’s portal to digitized Michigan newspapers.', 'free'),
  ('MIGenWeb', 'https://www.migenweb.org/', 'Michigan’s county volunteer sites.', 'free'),
 ]),
 ('Indiana', 'Next door', [
  ('Hoosier State Chronicles', 'https://newspapers.library.in.gov/', 'Indiana’s free digital historic newspaper program.', 'free'),
  ('INGenWeb', 'https://ingenweb.org/', 'Indiana’s county volunteer sites, many with transcribed county-history biographies.', 'free'),
 ]),
 ('Ohio', 'Where so many Michigan and Indiana families came from', [
  ('Ohio death records guide', 'https://ohiohistory.libguides.com/vital/death', 'The Ohio History Connection’s guide to Ohio death certificates and indexes, by period.', 'free'),
 ]),
 ('Beyond the United States', 'Following a family home', [
  ('FreeBMD (England and Wales)', 'https://www.freebmd.org.uk/', 'Free index of births, marriages and deaths registered from 1837.', 'free'),
  ('Irish Genealogy', 'https://www.irishgenealogy.ie/', 'Ireland’s free civil birth, marriage and death records and church records.', 'free'),
  ('Riksarkivet (Sweden)', 'https://sok.riksarkivet.se/', 'The Swedish National Archives: church books and household examination rolls, free to view.', 'free'),
  ('Matricula', 'https://data.matricula-online.eu/', 'Catholic parish registers from Germany, Austria, Poland and elsewhere, free to view.', 'free'),
  ('Archion', 'https://www.archion.de/', 'Protestant church books of Germany. Paid, and worth it when a German village is known.', 'paid'),
  ('ScotlandsPeople', 'https://www.scotlandspeople.gov.uk/', 'Scotland’s official records: parish registers, statutory registers, wills. Pay per view.', 'paid'),
  ('Library and Archives Canada', 'https://www.bac-lac.gc.ca/', 'Canadian census, immigration and military records.', 'free'),
 ]),
]
def recsec(name, sub, items):
    lis = ''.join(f'<li><a href="{u}" rel="noopener">{t}</a>{" <span class=\"paid\">paid</span>" if f=="paid" else ""}<span class="d">{d}</span></li>' for t, u, d, f in items)
    sid = re.sub(r'[^a-z]+', '-', name.lower()).strip('-')
    return f'<div class="recsec" id="{sid}"><h2>{name}</h2><p class="note" style="margin-top:-.4rem">{sub}</p><ul class="reclist">{lis}</ul></div>'
nav = ' · '.join(f'<a href="#{re.sub(r"[^a-z]+","-",n.lower()).strip("-")}">{n}</a>' for n, _, _ in REC)
records = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">From the desk</p>
    <h1>Where the records are</h1>
    <p class="lede" style="font-size:1.15rem">The places we search first, nearly all of them free. Most mysteries that stay unsolved stay that way because nobody opened the right free book.</p>
    <p class="recfilter"><label for="recQ">Find a source</label> <input type="search" id="recQ" placeholder="Try “newspapers”, “Ohio” or “church”" autocomplete="off"></p>
    <p class="center recnav">{nav}</p>
    {''.join(recsec(*r) for r in REC)}
    <p class="recnone" id="recNone" hidden>Nothing matches that. Try a shorter word.</p>
    <h2>Three habits that find more</h2>
    <ul class="dis">
      <li><b>Search the unusual name.</b> A rare surname, spelled every way it can be said, finds the family and almost nobody else.</li>
      <li><b>Read the whole page.</b> Neighbours in a census are often in-laws, and witnesses to a deed are often kin.</li>
      <li><b>Go back to the original.</b> Indexes and transcriptions are for finding things. The record itself is the evidence.</li>
    </ul>
    <p class="note">This list grows as the desk works further afield. Know a free source we should add? <a href="/#contact">Tell us</a>.</p>
    <script>
    (function(){{ "use strict";
      const q=document.getElementById('recQ'), items=[...document.querySelectorAll('.reclist li')], secs=[...document.querySelectorAll('.recsec')], none=document.getElementById('recNone');
      q.addEventListener('input',()=>{{ const t=q.value.trim().toLowerCase(); let any=0;
        items.forEach(li=>{{ const hit=!t||(li.textContent+' '+li.closest('.recsec').querySelector('h2').textContent).toLowerCase().includes(t); li.hidden=!hit; if(hit) any++; }});
        secs.forEach(s=>s.hidden=![...s.querySelectorAll('li')].some(li=>!li.hidden)); none.hidden=!!any; }});
    }})();
    </script>
'''
page('records/index.html', 'Where the records are · Project Scroll',
     'The free archives, newspapers, maps and record collections Project Scroll searches first, for Michigan, Indiana, Ohio, the whole United States and beyond.', records,
     og='https://projectscroll.com/og/records.jpg')

# ------------------------------------------------------------------ glossary
G = [
 ('Abstract', 'A summary of a document, such as a deed or will, giving its main points. Useful for finding the original, but not the record itself: abstracts drop words and sometimes get names and dates wrong.'),
 ('Administrator', 'The person a court appoints to settle the estate of someone who died without a will. Compare executor.'),
 ('Ahnentafel', 'German for “ancestor table.” A numbering system for a pedigree: the subject is 1, a person’s father is double their number and their mother double plus one. So 2 is the father, 3 the mother, 4 the father’s father.'),
 ('Census', 'A count of the population. The United States has taken one every ten years since 1790; from 1850 it names every free person in the household (enslaved people were counted on separate schedules, usually without names, until 1870). Most of the 1890 census was destroyed after a fire in 1921. Each census is opened to the public 72 years after it was taken.'),
 ('Consort', 'A husband or wife. Often seen on old gravestones: “Mary, consort of John Smith.”'),
 ('County history', 'The big county histories printed from the 1870s to the 1910s. Many biographies in them were paid for by the people they describe, so they tend to be accurate on names and dates and generous on everything else.'),
 ('Deed', 'The written record of land changing hands, copied into the county’s deed books. Deeds often name wives, heirs and neighbours, and sometimes say where a seller had moved to.'),
 ('Double dating', 'Dates such as “10 February 1731/2.” Before 1752, England and its colonies began the new year on 25 March, so January to March dates were often written with both years.'),
 ('Et ux.', 'Latin, “and wife,” in deeds and court records: “John Smith et ux.” means John and his wife.'),
 ('Executor', 'The person named in a will to carry it out. Compare administrator.'),
 ('Field notes', 'A surveyor’s notebook from the original land survey, recording every line walked: the trees, streams, soil and sometimes the people met along the way.'),
 ('General Land Office', 'The federal office that surveyed and sold public land, from 1812 until it became part of the Bureau of Land Management in 1946. Its plats, field notes and patents are online free.'),
 ('Informant', 'The person who answered the questions on a certificate. On a death certificate the dead person was never the informant, so everything on it is someone else’s memory.'),
 ('Instant and ultimo', 'Old newspaper shorthand: “the 4th inst.” means the 4th of this month; “the 20th ult.” the 20th of last month.'),
 ('Intestate', 'Having died without a will. The court then appoints an administrator and divides the estate by law.'),
 ('Land patent', 'The first transfer of a piece of land from the government to a private owner.'),
 ('Maiden name', 'A woman’s surname before marriage. Most records name married women only by their husbands’ surnames, which is why a woman’s own family is the commonest gap in any tree.'),
 ('mtDNA and Y-DNA', 'Two DNA tests that follow one line each: mitochondrial DNA passes from mother to child down the all-female line; Y-DNA passes from father to son down the all-male line.'),
 ('Naturalization', 'The process of becoming a citizen. Older files often have two parts: a declaration of intention (“first papers”) and, years later, a petition. Later ones can name the town of birth and the ship.'),
 ('Pedigree collapse', 'When the same ancestor appears more than once in a family tree because cousins married. It means fewer separate ancestors than the arithmetic of doubling would suggest.'),
 ('Plat', 'A surveyor’s drawing of land divided into lots or parcels, such as a town plan or a subdivision.'),
 ('Probate', 'The court process that settles a dead person’s estate. A probate file can hold the will, an inventory of belongings, and the names of every heir.'),
 ('Register system', 'The standard way of numbering a family register, used by American genealogists since the 1800s. Each descendant gets a number, and the children of each couple are listed with small roman numerals.'),
 ('Relict', 'A widow, or less often a widower: someone who outlived their husband or wife.'),
 ('Section, township and range', 'The survey grid of the public-land states. A survey township is six miles square and divided into 36 sections of one square mile (640 acres). A land description such as “NE¼ of section 12, T5S R14W” pins down a farm exactly.'),
 ('Soundex', 'A code that groups surnames that sound alike: a letter and three digits, so Robert and Rupert both come out as R163. Old census indexes were built on it. Try it in our <a href="/toolkit/">toolkit</a>.'),
 ('Tract book', 'The land office’s ledger of sales, arranged by section, showing who first bought each piece of land and when.'),
 ('Transcription', 'A written copy of a record, word for word. Better than an abstract, but every copy is a chance for a new mistake.'),
 ('Vital records', 'Records of births, marriages and deaths. Most states only required them from the late 1800s or early 1900s.'),
]
gl = ''.join(f'<div class="gl" id="g-{re.sub(r"[^a-z]+","-",t.lower()).strip("-")}"><dt>{t}</dt><dd>{d}</dd></div>' for t, d in G)
letters = sorted({t[0] for t, _ in G})
glossary = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">From the desk</p>
    <h1>The glossary</h1>
    <p class="lede" style="font-size:1.15rem">The words old records use, and the words we use about them, in plain English.</p>
    <p class="recfilter"><label for="glQ">Find a word</label> <input type="search" id="glQ" placeholder="Try “widow” or “survey”" autocomplete="off"></p>
    <dl class="glossary">{gl}</dl>
    <p class="recnone" id="glNone" hidden>No word matches that.</p>
    <p class="note">A word we should add? <a href="/#contact">Tell us</a>.</p>
    <script>
    (function(){{ "use strict";
      const q=document.getElementById('glQ'), items=[...document.querySelectorAll('.gl')], none=document.getElementById('glNone');
      q.addEventListener('input',()=>{{ const t=q.value.trim().toLowerCase(); let any=0; items.forEach(d=>{{ const hit=!t||d.textContent.toLowerCase().includes(t); d.hidden=!hit; if(hit) any++; }}); none.hidden=!!any; }});
    }})();
    </script>
'''
page('glossary/index.html', 'The glossary · Project Scroll',
     'Plain-English meanings of the words in old records: probate, relict, plat, informant, Soundex, ahnentafel, township and range, and more.', glossary,
     og='https://projectscroll.com/og/glossary.jpg')

# ------------------------------------------------------------------ about
about = '''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">About</p>
    <h1>About Project Scroll</h1>
    <p class="lede" style="font-size:1.15rem">Project Scroll is independent historical research: a history hunt anyone can play, and a research desk anyone can hire. Both run on one rule. Every clue is true, and every answer is in the record.</p>
    <h2>Who we are</h2>
    <p>Project Scroll is run by an independent researcher and author who writes narrative nonfiction about the history of the Great Lakes country, and who was trained in visual communications. The research behind those books is the same research we offer you: old certificates, deeds, surveys, county histories and newspapers, read line by line and compared until they agree, or until we can say exactly why they don’t.</p>
    <h2>What we believe</h2>
    <ul class="dis">
      <li><b>The record decides.</b> Not the family tree online, not the story everybody tells, not what we hoped to find.</li>
      <li><b>Every statement is marked.</b> You can always see whether a fact comes from a document, a book, a family story or our own reading. <a href="/#marks">How we mark the evidence</a>.</li>
      <li><b>Gaps are shown, not filled.</b> An honest “not yet known” is worth more than a confident guess.</li>
      <li><b>Corrections are welcome.</b> If you know better, tell us. The record is bigger than any one of us.</li>
      <li><b>Places and people are respected.</b> The hunt never asks anyone to dig, to disturb a grave or a mound, or to go looking for anyone’s home.</li>
    </ul>
    <h2>Where it started</h2>
    <p>Project Scroll began in Cassopolis, Michigan, with a few questions the county history couldn’t answer. It doesn’t stop there. The hunt and the desk now take on questions from anywhere the records reach.</p>
    <p class="center"><a class="btn" href="/#hunt">Play the hunt</a> <a class="btn" href="/#services">Research services</a> <a class="btn" href="/#contact">Get in touch</a></p>
'''
page('about/index.html', 'About · Project Scroll',
     'Project Scroll is independent historical research: a history hunt anyone can play and a research desk anyone can hire, where every clue is true.', about,
     og='https://projectscroll.com/og/about.jpg')

# ------------------------------------------------------------------ privacy
priv = '''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Privacy</p>
    <h1>What this site keeps</h1>
    <p class="lede">Almost nothing, and none of it leaves your device. Project Scroll has no ads, no analytics, no tracking and no accounts.</p>
    <h2>Kept in your own browser</h2>
    <p>A few things are remembered so the site works the way you left it. They are stored in your browser on this device, nobody else can see them, and we never receive them.</p>
    <ul class="dis">
      <li><b>Light or dark.</b> The page colors you chose.</li>
      <li><b>The lantern.</b> Whether you put it out.</li>
      <li><b>The opening flourish.</b> That you have already seen the ink draw itself on your first visit, so it does not replay.</li>
      <li><b>Your followed cases.</b> The cases you starred on the case board.</li>
      <li><b>Your case notes.</b> Anything you write in a case notebook. <a href="/notebook/">See all your notes</a>.</li>
      <li><b>Your drafts.</b> What you type into the message form and the family-history and family-legend forms, so it survives a reload. Nothing is sent from those forms; you copy the text and send it yourself.</li>
    </ul>
    <p>To clear all of it, clear this site’s data in your browser settings.</p>
    <h2>Sent to other sites</h2>
    <ul class="dis">
      <li><b>The map room.</b> The 1860 wall map is shown straight from the Library of Congress, so your browser asks the Library’s image server (tile.loc.gov) for the pieces of the map you look at.</li>
      <li><b>Facebook.</b> Links to Project Scroll’s Facebook page and Messenger simply take you there. Nothing from Facebook is loaded on these pages until you click.</li>
    </ul>
    <h2>When you write to us</h2>
    <p>Messages reach us through Facebook, under Facebook’s own privacy terms. What you tell us about your family is used to answer your question and for nothing else.</p>
    <p class="center"><a class="btn" href="/">Back to Project Scroll</a> <a class="btn" href="/#contact">Get in touch</a></p>
'''
page('privacy/index.html', 'Privacy · Project Scroll',
     'What projectscroll.com keeps: no ads, no analytics, no tracking. A few settings and notes stay in your own browser.', priv)
print('records, glossary, about, privacy built')
