"""Builds the records directory, the glossary and the about page:  python3 _tools/build_more.py"""
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
  ('INGenWeb', 'https://www.ingenweb.org/', 'Indiana’s county volunteer sites, many with transcribed county-history biographies.', 'free'),
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
  ('Library and Archives Canada', 'https://library-archives.canada.ca/eng', 'Canadian census, immigration and military records.', 'free'),
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
      <li><b>Read the whole page.</b> Neighbors in a census are often in-laws, and witnesses to a deed are often kin.</li>
      <li><b>Go back to the original.</b> Indexes and transcriptions are for finding things. The record itself is the evidence.</li>
    </ul>
    <h2>Did you know?</h2>
    <ul class="dis">
      <li>Most of the 1890 United States census was lost after a fire in Washington in January 1921.</li>
      <li>Each federal census opens to the public 72 years after it was taken.</li>
      <li>The 1850 census was the first to name every free person in a household. Before it, only the head of the household was named.</li>
      <li>Civil registration of births, marriages and deaths in England and Wales began on 1 July 1837.</li>
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
 ('County history', 'The big county histories printed from the 1870s to the 1910s. Many biographies in them were paid for by the people they describe, so they tend to be reliable on what the family knew well, and generous on everything else; dates and places still need a document.'),
 ('Deed', 'The written record of land changing hands, copied into the county’s deed books. Deeds often name wives, heirs and neighbors, and sometimes say where a seller had moved to.'),
 ('Double dating', 'Dates such as “10 February 1731/2.” Before 1752, England and its colonies began the new year on 25 March, so January to March dates were often written with both years.'),
 ('Et ux.', 'Latin, “and wife,” in deeds and court records: “John Smith et ux.” means John and his wife.'),
 ('Executor', 'The person named in a will to carry it out. Compare administrator.'),
 ('Field notes', 'A surveyor’s notebook from the original land survey, recording every line walked: the trees, streams, soil and sometimes the people met along the way.'),
 ('General Land Office', 'The federal office that surveyed and sold public land, from 1812 until it became part of the Bureau of Land Management in 1946. Its plats, field notes and patents are free online.'),
 ('Informant', 'The person who answered the questions on a certificate. On a death certificate the dead person was never the informant, so everything on it is someone else’s memory.'),
 ('Instant and ultimo', 'Old newspaper shorthand: “the 4th inst.” means the 4th of this month; “the 20th ult.” the 20th of last month.'),
 ('Intestate', 'Having died without a will. The court then appoints an administrator and divides the estate by law.'),
 ('Land patent', 'The first transfer of a piece of land from the government to a private owner.'),
 ('Lore', 'What a place says about itself: the stories passed around a lake, a township or a lodge, told without a page to point to. Lore is where a hunt often starts; the record is where it ends.'),
 ('Local legend', 'The famous ancestor, the buried treasure, the river under the ground. Some are true. The desk reads each one against the record and says which.'),
 ('Maiden name', 'A woman’s surname before marriage. Most records name married women only by their husbands’ surnames, which is why a woman’s own family is the commonest gap in any tree.'),
 ('mtDNA and Y-DNA', 'Two DNA tests that follow one line each: mitochondrial DNA passes from mother to child down the all-female line; Y-DNA passes from father to son down the all-male line.'),
 ('Naturalization', 'The process of becoming a citizen. Older files often have two parts: a declaration of intention (“first papers”) and, years later, a petition. Later ones can name the town of birth and the ship.'),
 ('Pedigree collapse', 'When the same ancestor appears more than once in a family tree because cousins married. It means fewer separate ancestors than the arithmetic of doubling would suggest.'),
 ('Plat', 'A surveyor’s drawing of land divided into lots or parcels, such as a town plan or a subdivision.'),
 ('Probate', 'The court process that settles a dead person’s estate. A probate file can hold the will, an inventory of belongings, and the names of every heir.'),
 ('Register system', 'The standard way of numbering a family register, used by American genealogists since the 1800s. Each descendant gets a number, and the children of each couple are listed with small roman numerals.'),
 ('Relict', 'A widow, or less often a widower: someone who outlived their husband or wife.'),
 ('Section, township and range', 'The survey grid of the public-land states. A survey township is six miles square and divided into 36 sections of one square mile (640 acres). A land description such as “NE¼ of section 12, T5S R14W” pins down a farm exactly.'),
 ('Soundex', 'A code that groups surnames that sound alike: a letter and three digits, so Robert and Rupert both come out as R163. Old census indexes were built on it. Try it in our <a href="/toolkit/#soundex">toolkit</a>.'),
 ('Tract book', 'The land office’s ledger of sales, arranged by section, showing who first bought each piece of land and when.'),
 ('Transcription', 'A written copy of a record, word for word. Better than an abstract, but every copy is a chance for a new mistake.'),
 ('Vital records', 'Records of births, marriages and deaths. Most states only required them from the late 1800s or early 1900s.'),
]
G += [
 ('Senior', 'In the 1800s, not always “father.” Sometimes it only meant the older of two men with the same name in town, related or not. Junior was the younger.'),
 ('Ditto (do.)', '“The same as above.” Census takers and clerks used it, or a pair of marks, for repeated surnames, birthplaces and occupations.'),
 ('Long s (ſ)', 'An s that looks like an f without the full crossbar, used at the start or in the middle of a word until about 1800. “Congreſs” is Congress.'),
]
G.sort(key=lambda x: x[0].lower())
gl = ''.join(f'<div class="gentry" id="g-{re.sub(r"[^a-z]+","-",t.lower()).strip("-")}"><dt>{t}</dt><dd>{d}</dd></div>' for t, d in G)
letters = sorted({t[0] for t, _ in G})
glossary = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">From the desk</p>
    <h1>The glossary</h1>
    <p class="lede" style="font-size:1.15rem">The words old records use, and the words we use about them, in plain English. Learn a handful, and an old deed or gravestone starts to talk.</p>
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
    <p class="lede" style="font-size:1.15rem">Project Scroll is independent historical research: an online treasure hunt anyone can play, a research desk anyone can hire, and a studio for digital imaging, design, photography, 3D LiDAR, animation and video. All of it runs on one rule. Every clue is true, and every answer is in the record.</p>
    <h2>Who we are</h2>
    <p>Project Scroll is run by an independent researcher and author who writes narrative nonfiction about the history of the Great Lakes country, and who trained in visual communications. The research behind those books is the same research we offer you: old certificates, deeds, surveys, county histories and newspapers, read line by line and compared until they agree, or until we can say exactly why they don’t.</p>
    <h2>What we offer</h2>
    <p><b>Professional research.</b> Lost ancestors, family histories and registers, family legends tested against the record, forgotten places, maps and land surveys, heirlooms, lodges and old societies, historical research for authors, films and local groups, and a second pair of eyes on anything you mean to publish. <a href="/#services">Research services</a>.</p>
    <p><b>Imaging, design and video.</b> Digital imaging of photographs, documents, maps and heirlooms; imaging analysis of faded ink, damaged pages and the details in old photographs; image creation and restoration; graphic design for family books, charts, covers and keepsakes; photography; and video production, from family-history films to recorded interviews.</p>
    <p><b>3D and living documents.</b> Landscapes modeled in three dimensions from public LiDAR elevation surveys, 3D animations and fly-throughs, every reconstruction labeled as one, and living documents: research papers, timelines and family records that keep growing as new evidence turns up, with every change dated. <a href="/#studio">The studio</a>.</p>
    <p>Every commission starts with an honest first read: what can be done, and what it will take, before you commit to anything.</p>
    <h2>What we believe</h2>
    <ul class="dis">
      <li><b>The record decides.</b> Not the family tree online, not the story everybody tells, not what we hoped to find.</li>
      <li><b>Every statement is marked.</b> You can always see whether a fact comes from a document, a book, a family story or our own reading. <a href="/#marks">How we mark the evidence</a>.</li>
      <li><b>Gaps are shown, not filled.</b> An honest “not yet known” is worth more than a confident guess.</li>
      <li><b>Corrections are welcome.</b> If you know better, tell us. The record is bigger than any one of us.</li>
      <li><b>Places and people are respected.</b> The hunt never asks anyone to dig, to disturb a grave or a mound, or to go looking for anyone’s home.</li>
    </ul>
    <h2>When we get something wrong</h2>
    <p>We will. When a reader or a new document shows that a page of this site is mistaken, we change the page, date the change on it, and say what was wrong, rather than quietly replacing the words. A case that was called solved on a bad reading is reopened and says so. If you have found an error, write to <a href="mailto:research@projectscroll.com?subject=A%20correction">research@projectscroll.com</a> or <a href="https://m.me/projectscroll">tell us</a> on Facebook; corrections are credited to the person who sent them, by name or not, as they prefer.</p>
    <h2>The record behind this site</h2>
    <p>The dates on the scroll, the person of the month and the then-and-now maps are built from the same sources the hunt asks you to open: Rogers (1875), Mathews (1882), Glover (1906), the 1860 wall map at the Library of Congress, and Michigan death certificates at the Archives of Michigan. Where a page of this site makes a claim, the source is on the page or one click away. If it is not, that is a correction we owe.</p>
    <h2>Where it started</h2>
    <p>Project Scroll began in Cassopolis, Michigan, with a few questions the county history couldn’t answer. It doesn’t stop there. The hunt and the desk now take on questions from anywhere the records reach.</p>
    <p class="center"><a class="btn" href="/#hunt">Play the hunt</a> <a class="btn" href="/#services">Research services</a> <a class="btn" href="/#studio">Imaging, design and video</a> <a class="btn" href="/#contact">Get in touch</a></p>
'''
page('about/index.html', 'About · Project Scroll',
     'Project Scroll is independent historical research: an online treasure hunt anyone can play, a research desk anyone can hire, and a studio for digital imaging, design, photography, 3D LiDAR, animation and video.', about,
     og='https://projectscroll.com/og/about.jpg')

# ------------------------------------------------------------------ privacy
priv = '''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Privacy</p>
    <h1>What this site keeps</h1>
    <p class="lede">Almost nothing. Project Scroll has no accounts and no ads of its own. One thing is optional and off until you say yes: a visit counter from Meta, used to see how the hunt is found and, later, to show Project Scroll’s own advertisements to people who have been here. You choose on your first visit, and you can change your mind here.</p>
    <div class="consentbox" id="consentbox">
      <p><b>Your choice on this device:</b> <span id="consentState">not made yet</span></p>
      <p><button type="button" class="btn" id="consentYes">Allow the visit counter</button> <button type="button" class="btn" id="consentNo">Keep it off</button></p>
    </div>
    <h2>Kept in your own browser</h2>
    <p>A few things are remembered so the site works the way you left it. They are stored in your browser on this device, nobody else can see them, and we never receive them.</p>
    <ul class="dis">
      <li><b>Light or dark.</b> The page colors you chose.</li>
      <li><b>The lantern.</b> Whether you put it out.</li>
      <li><b>The opening flourish.</b> That you have already seen the ink draw itself on your first visit, so it does not replay.</li>
      <li><b>Your tin badges.</b> The badges you have earned around the site, and the days you visited, so the “Regular” badge can count them.</li>
      <li><b>Your followed cases.</b> The cases you starred on the case board.</li>
      <li><b>Your case notes.</b> Anything you write in a case notebook. <a href="/notebook/">See all your notes</a>.</li>
      <li><b>Your answer about the visit counter.</b> Allow or keep off, so you are not asked again.</li>
      <li><b>Your drafts.</b> What you type into the message form and the family-history and family-legend forms, so it survives a reload. Nothing is sent from those forms; you copy the text and send it yourself.</li>
    </ul>
    <p>To clear all of it, clear this site’s data in your browser settings.</p>
    <h2>Sent to other sites</h2>
    <ul class="dis">
      <li><b>The map room.</b> The 1860 wall map is shown straight from the Library of Congress, so your browser asks the Library’s image server (tile.loc.gov) for the pieces of the map you look at.</li>
      <li><b>Facebook.</b> Links to Project Scroll’s Facebook pages and Messenger simply take you there. On a case page you can choose to show the live Facebook post; only then does your browser load it from Facebook, under Facebook’s own terms. Until you click, nothing from Facebook is loaded.</li>
      <li><b>The Meta visit counter (only if you allow it).</b> If you choose “Allow”, your browser loads a small script from Meta (the Meta Pixel) that tells Meta which pages of this site you looked at, and when. Meta may match that to a Facebook or Instagram account if you have one, under <a href="https://www.facebook.com/privacy/policy/" target="_blank" rel="noopener">Meta’s privacy policy</a>. We use it to see which parts of the hunt and the studio are visited, and later to show Project Scroll’s own advertisements on Facebook and Instagram to people who have been here. It records page views, when the Services section is read, and when the Messenger button is pressed. It never sees what you type: your notes, drafts and messages stay in your browser as before. If you choose “Keep it off”, or make no choice, nothing from Meta is loaded, and nothing is counted.</li>
    </ul>
    <h2>When you write to us</h2>
    <p>Email to research@projectscroll.com lands in a mailbox hosted for us by GoDaddy on Microsoft 365, under <a href="https://www.godaddy.com/legal/agreements/privacy-policy" target="_blank" rel="noopener">GoDaddy’s privacy policy</a>; messages sent through Facebook travel under Facebook’s own terms. Either way, what you tell us about your family is used to answer your question and for nothing else, and is never sold or shared.</p>
    <p class="center"><a class="btn" href="/">Back to Project Scroll</a> <a class="btn" href="/#contact">Get in touch</a></p>
'''
page('privacy/index.html', 'Privacy · Project Scroll',
     'What projectscroll.com keeps: no accounts, no ads of its own, and a Meta visit counter that stays off until you allow it. Your settings and notes stay in your own browser.', priv)

# ------------------------------------------------------------------ badges
badges = '''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Your field book</p>
    <h1>Your tin badges</h1>
    <p class="lede">In the winter of 1846–47, two hundred badges of the “Ancient and Honorable Order” were worn at a ball in Cassopolis. Not one is known to survive. Here you can earn your own: twenty-one of them: twenty for the things you do as you explore the site, and one for cracking a case, with five ranks on the way from Candidate to Keeper of the Hall.</p>
    <p class="brank" id="brank"></p>
    <ol class="rladder" id="rladder" aria-label="The five ranks"></ol>
    <p class="bcount" id="bcount" aria-live="polite"></p>
    <ol class="badgebook" id="badgebook"></ol>
    <div class="sayword" id="sayword">
      <h2>Say the word</h2>
      <p>Somewhere on every page of this site, a line is written in code. Turn it with the cipher wheel in the <a href="/toolkit/#cipher">hunter’s toolkit</a>, and it will tell you what to do.</p>
      <form id="wordform" class="formrow" autocomplete="off"><label>The word <input type="text" id="word" spellcheck="false"></label><button type="submit" class="btn primary">Say it</button></form>
      <p class="note" id="wordmsg" aria-live="polite"></p>
    </div>
    <div class="sayword" id="second" hidden>
      <h2>The second line</h2>
      <p>You broke the first. Here is a harder one, and the cipher wheel alone will not open it. Look at the wheel’s other setting.</p>
      <p class="cipherline big">GSV HVXLMW DLIW RH XSZIGVI. ML DSVVO DROO GFIM RG. SLOW RG GL Z NRIILI.</p>
      <form id="word2form" class="formrow" autocomplete="off"><label>The second word <input type="text" id="word2" spellcheck="false"></label><button type="submit" class="btn primary">Say it</button></form>
      <p class="note" id="word2msg" aria-live="polite"></p>
    </div>
    <div class="ledgerbox" id="ledgerbox">
      <h2>Carry your ledger</h2>
      <p>Your badges, followed cases and notebook live only in this browser. To carry them to another device, take your ledger with you: a small file, made here, that Project Scroll on another device can read back. Nothing is sent to us.</p>
      <p class="formrow"><button type="button" class="btn primary" id="ledgerOut">Take my ledger</button> <label class="btn" for="ledgerIn">Bring a ledger back</label><input type="file" id="ledgerIn" accept=".json,application/json" class="vh"></p>
      <p class="note" id="ledgerMsg" aria-live="polite"></p>
    </div>
    <div class="charterbox" id="charterbox" hidden>
      <h2>Your charter</h2>
      <p>Every badge earned. You may print your charter: type your name as you want it written, then print.</p>
      <form id="charterform" class="formrow" autocomplete="off"><label>Your name <input type="text" id="cname" maxlength="60"></label><button type="submit" class="btn primary">Print my charter</button></form>
      <p class="note">Your charter is made on this device. Nothing is sent anywhere.</p>
    </div>
    <div class="charter" id="charter" aria-hidden="true"><p class="ch-top">Project Scroll</p><p class="ch-h">Charter of the Hall</p><p class="ch-b">Know all by these presents that</p><p class="ch-name" id="chName"></p><p class="ch-b">having read the walls, followed the record, broken both ciphers and earned every one of the tin badges, is hereby received as</p><p class="ch-rank">Keeper of the Hall</p><p class="ch-b">with all the honor and none of the dignity that any such title has ever carried.</p><p class="ch-date" id="chDate"></p><p class="ch-motto">Every clue is true. Every answer is in the record.</p></div>
    <p class="note">Your badges are kept only in this browser, on this device. Nobody else can see them, and we never receive them. <button type="button" class="linkbtn" id="breset">Start the field book over</button></p>
    <script>
    document.addEventListener('DOMContentLoaded', function(){
      const ol=document.getElementById('badgebook'), cnt=document.getElementById('bcount'); if (!ol || !window.PS_BADGES) return;
      const draw=function(){ const got=window.psBadges(); let n=0; ol.innerHTML='';
        window.PS_BADGES.forEach(function(b,i){ const has=!!got[b[0]]; if (has) n++;
          const li=document.createElement('li'); li.className=has?'won':'';
          li.innerHTML='<svg viewBox="0 0 40 40" aria-hidden="true"><path class="tin" d="M20 2l4.7 9.6 10.5 1.5-7.6 7.4 1.8 10.5L20 26l-9.4 5 1.8-10.5-7.6-7.4 10.5-1.5z"/><circle cx="20" cy="17.5" r="4.2" class="boss"/></svg><b></b><span></span><small></small>';
          li.querySelector('b').textContent=b[1]; li.querySelector('span').textContent=b[2];
          li.querySelector('small').textContent=has?('Earned '+got[b[0]]):'Not yet';
          ol.appendChild(li); });
        cnt.textContent=n+' of '+window.PS_BADGES.length+' badges earned';
        let rk=window.PS_RANKS[0][1]; window.PS_RANKS.forEach(function(r){ if (n>=r[0]) rk=r[1]; });
        document.getElementById('brank').innerHTML='Your rank: <b></b>'; document.querySelector('#brank b').textContent=rk;
        const lad=document.getElementById('rladder'); if (lad){ lad.innerHTML=''; window.PS_RANKS.forEach(function(r,i){ const li=document.createElement('li'); const nx=window.PS_RANKS[i+1];
          li.innerHTML='<b></b><span></span>'; li.querySelector('b').textContent=r[1]; li.querySelector('span').textContent=(r[0]===0?'from the start':r[0]+' badges'+(nx?'':' (every one)'));
          if (r[1]===rk) li.className='here'; else if (n>=r[0]) li.className='past'; lad.appendChild(li); }); }
        document.getElementById('second').hidden=!(got.halter||got.hewgag);
        document.getElementById('charterbox').hidden=(window.PS_BADGES.filter(function(b){ return b[0]!=='solver' && !got[b[0]]; }).length>0);
      };
      draw(); document.addEventListener('ps-badge', function(){ setTimeout(draw,50); });
      document.getElementById('wordform').addEventListener('submit', function(e){ e.preventDefault();
        const w=document.getElementById('word').value.trim().toLowerCase(), m=document.getElementById('wordmsg');
        if (!w){ m.textContent='Type the word first.'; return; }
        if (w==='halter'){ window.psEarn('halter'); m.textContent='That is the word. Two hundred badges were worn to a ball on it.'; draw(); }
        else if (w==='ledger'){ window.psEarn('diamond'); m.textContent='The diamond keeps its word. The book at the top of every page is a ledger, and so is this one.'; draw(); }
        else m.textContent='That is not the word. Turn the wheel again.'; });
      document.getElementById('word2form').addEventListener('submit', function(e){ e.preventDefault();
        const w=document.getElementById('word2').value.trim().toLowerCase(), m=document.getElementById('word2msg');
        if (!w){ m.textContent='Type the word first.'; return; }
        if (w==='charter'){ window.psEarn('charter'); m.textContent='That is the word. Even the man who wrote the story wasn’t sure of it.'; draw(); }
        else m.textContent='Not that one. Try the mirror.'; });
      document.body.appendChild(document.getElementById('charter'));
      document.getElementById('charterform').addEventListener('submit', function(e){ e.preventDefault();
        const nm=document.getElementById('cname').value.trim(); document.getElementById('chName').textContent=nm||'________________________';
        document.getElementById('chDate').textContent='Given this '+new Date().toLocaleDateString('en-US',{day:'numeric',month:'long',year:'numeric'});
        document.body.classList.add('printing-charter'); addEventListener('afterprint', function(){ document.body.classList.remove('printing-charter'); }, {once:true}); window.print(); });
      document.getElementById('breset').addEventListener('click', function(){ window.psResetBadges(); draw(); });
    });
    </script>
'''
page('badges/index.html', 'Your tin badges · Project Scroll',
     'Earn tin badges as you explore Project Scroll: read a case, walk the map room, use the toolkit and crack the hidden line. Kept in your own browser.', badges)
print('records, glossary, about, privacy, badges built')

# ------------------------------------------------------------------ share doors
# Short addresses with their own share cards. A link to /#services shows the home card on Facebook
# (the part after # is never sent), so /services/ carries the Services card and steps straight through.
for slug, title, desc, og, tgt in [
  ('hunt', 'The hunt · Project Scroll', 'Ten mysteries from one Michigan county, each begun as a single question. Free to play, solved with clues from real pages. Every clue is true, and every answer is in the record.', 'hunt', '/#hunt'),
  ('services', 'Professional research · Project Scroll', 'Lost ancestors, family histories, legends tested against the record, forgotten places and land. Every source cited, every statement marked. An honest first read before you commit to anything.', 'services', '/#services'),
  ('studio', 'The studio · Project Scroll', 'Digital imaging, imaging analysis, graphic design, photography, video, 3D LiDAR landscapes, animation and living documents, from the desk that runs the hunt.', 'studio', '/#studio'),
]:
    body=f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <h1>{title.split(' · ')[0]}</h1>
    <p class="lede">{desc}</p>
    <p class="center"><a class="btn primary" href="{tgt}">Open it on the main page</a></p>
    <script>location.replace('{tgt}');</script>
'''
    page(f'{slug}/index.html', title, desc, body, noindex=True, og=f'https://projectscroll.com/og/{og}.jpg')

# ------------------------------------------------------------------ document of the month
doc = '''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Document of the month · October 2026</p>
    <h1>One page of Rogers, 1875</h1>
    <p class="lede">Every month we put one real page on the table and read it slowly. This month: page 253 of Howard S. Rogers’s <i>History of Cass County, from 1825 to 1875</i>, the first time the joke lodge of 1846 was ever printed, with the man who told it to Rogers only a footnote away.</p>
    <figure class="docfig">
      <a href="/img/pages/rogers-1875-p253-1200.jpg"><picture><source type="image/webp" srcset="/img/pages/rogers-1875-p253-700.webp 700w, /img/pages/rogers-1875-p253-1200.webp 1200w" sizes="(min-width:900px) 700px, 92vw"><img src="/img/pages/rogers-1875-p253-700.jpg" width="700" height="1091" alt="Page 253 of Rogers’s 1875 History of Cass County, with the paragraphs on the 1846 lodge boxed in red." fetchpriority="high" decoding="async"></picture></a>
      <figcaption>Rogers, 1875, p. 253. The boxed paragraphs are the lodge story. Tap or click the page to see it full size.</figcaption>
    </figure>
    <h2>What it is</h2>
    <p>Rogers was Cass County’s first historian. His book came out in 1875, fifty years after the county’s first land entries, while people who had seen 1846 were still alive to be asked. That is the book’s value and its danger at once: it is close to the events, and it is made of what people remembered.</p>
    <h2>How to read it</h2>
    <ul class="dis">
      <li><b>Read past the quotation.</b> Rogers quotes a long passage and then adds a few words of his own. The words after the closing quotation mark are where a careful reader slows down.</li>
      <li><b>Watch the punctuation.</b> On the next page a single question mark sits inside a parenthesis. A question mark in a county history is a historian telling you, as plainly as he dared, that he is not sure.</li>
      <li><b>Find the teller.</b> The passage is a quotation, and Rogers was not there in 1846. Seven years later Alfred Mathews reprinted the passage and put the teller’s name in a footnote: James M. Shepard, who was three years old in 1846. <a href="/#pom">Who told him?</a></li>
      <li><b>Count what can be counted.</b> Two hundred badges, one ball, one winter. Each number is a thing that might have left a record somewhere else: a newspaper, a bill, a diary, a badge in a drawer.</li>
    </ul>
    <h2>Read it yourself</h2>
    <p>The whole book is free online in the University of Michigan’s county-histories collection: <a href="https://name.umdl.umich.edu/BAD0871.0001.001" target="_blank" rel="noopener">Rogers, <i>History of Cass County, from 1825 to 1875</i></a>. Go to pages 253–254. Then compare <a href="https://name.umdl.umich.edu/BAD0870.0001.001" target="_blank" rel="noopener">Mathews, 1882</a>, page 174, where the same story is printed again, and notice what is missing.</p>
    <p>This page is the opening clue of <a href="/cases/1/">Case 1</a>. If you read it closely enough, you may not need the rest.</p>
    <h2>Next month</h2>
    <p>This is the first document of the month. The next is chosen on the first of November.</p>
    <p class="center"><a class="btn primary" href="/cases/1/">Open Case 1</a> <a class="btn" href="/records/">Where the records are</a> <a class="btn" href="/">Back to Project Scroll</a></p>
'''
page('document/index.html', 'Document of the month · Project Scroll',
     'One real page, read slowly, every month. October 2026: page 253 of Rogers’s 1875 History of Cass County, the first printing of the joke lodge of 1846.', doc,
     og='https://projectscroll.com/og/document.jpg')
