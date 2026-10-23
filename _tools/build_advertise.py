# The sponsor & advertise hub (/sponsor-and-advertise/) and the advertising page (/advertise/).
# Sponsorship keeps the hunt and the research free; advertising is a labeled place for a local business. Rates on request.
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
M = 'mailto:research@projectscroll.com?subject='

RULES = '''    <section class="pledge" aria-labeledby="rulesH">
      <h2 id="rulesH">The ground rules</h2>
      <ul class="ad-rules">
        <li><b>Every paid place is labeled.</b> A sponsor is called a sponsor and an advertisement is marked “Paid partner”, on the page and on Facebook.</li>
        <li><b>Money never changes a listing.</b> The places to eat and stay, the museums and the trips are chosen for their history. Paying does not add a place, move it up, or change what we say about it.</li>
        <li><b>Never inside the evidence.</b> No advertisement or sponsor’s name is placed inside a story’s evidence, a case, or a finding. Nobody who pays sees a story before readers do.</li>
        <li><b>Only what we would visit ourselves.</b> We take advertising from local businesses, museums, societies and events in the valley, and we can say no.</li>
      </ul>
    </section>
'''

hub = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Support the work, or be seen beside it</p>
    <h1>Sponsor &amp; advertise</h1>
    <p class="lede">Project Scroll is a free history hunt and a research desk for the St. Joseph River valley. There are two ways to be part of it. <b>Sponsors</b> pay for the research that keeps the hunt free. <b>Advertisers</b> buy a clearly labeled place in front of the people who read the stories, plan the trips and follow the hunt.</p>

    <div class="tiers ad-doors">
      <section class="tier" aria-labeledby="dS">
        <p class="tier-k">Keep the hunt free</p><h3 id="dS">Sponsor the hunt</h3><p class="tier-amt">For people, families, businesses and societies</p>
        <ul><li>Pays for the scans, certificates, microfilm and research hours behind each case</li><li>Named and thanked, with a public ledger of what every gift paid for</li><li>Four ways in, from a friend of the hunt to an underwriter</li></ul>
        <p class="tier-note">Sponsorship funds the work. It never chooses a case or shapes a finding.</p>
        <p><a class="btn primary" href="/sponsors/">How sponsorship works</a></p>
      </section>
      <section class="tier" aria-labeledby="dA">
        <p class="tier-k">Be seen in the valley</p><h3 id="dA">Advertise with us</h3><p class="tier-amt">For local businesses, museums and events</p>
        <ul><li>A labeled partner card on the pages where people plan a day out</li><li>A seasonal spot, a Facebook feature, a stop on the passport, or a prize for the hunt</li><li>Rates on request</li></ul>
        <p class="tier-note">Every advertisement is marked as paid, and none is ever placed inside a story’s evidence.</p>
        <p><a class="btn primary" href="/advertise/">See the ways to advertise</a></p>
      </section>
    </div>

    <h2>Which is right for you?</h2>
    <table class="ad-cmp"><caption>Sponsoring and advertising, side by side</caption>
      <thead><tr><th scope="col"></th><th scope="col">Sponsor</th><th scope="col">Advertise</th></tr></thead>
      <tbody>
        <tr><td class="hall">What it pays for</td><td>The research behind the free hunt</td><td>A place for your business in front of readers</td></tr>
        <tr><td class="hall">What you get</td><td>Your name, a thank-you, and the ledger line that shows where the money went</td><td>A labeled card, a seasonal spot, a Facebook feature, a passport stop or a hunt prize</td></tr>
        <tr><td class="hall">Who it suits</td><td>Anyone who wants local history researched and kept free</td><td>Restaurants, inns, shops, museums, societies and events in the valley</td></tr>
        <tr><td class="hall">How it is shown</td><td>“Sponsor”, on the sponsors page and where it helped</td><td>“Paid partner”, on every placement</td></tr>
        <tr><td class="hall">Cost</td><td><a href="/sponsors/">See the sponsor page</a></td><td>Ask us for rates</td></tr>
      </tbody>
    </table>

{RULES}
    <p class="note">Questions, or not sure which fits? Write to <a href="mailto:research@projectscroll.com?subject=Sponsor%20or%20advertise">research@projectscroll.com</a>.</p>
    <p class="ctas"><a class="btn primary" href="/sponsors/">Sponsor the hunt</a> <a class="btn primary" href="/advertise/">Advertise with us</a> <a class="btn" href="{M}Sponsor%20or%20advertise">Write to the desk</a></p>
'''

def prod(k, h, what, where, subj):
    return f'''      <section class="tier" aria-labeledby="{k}">
        <p class="tier-k">Paid partner</p><h3 id="{k}">{h}</h3><p class="tier-amt">Ask us for rates</p>
        <ul>{''.join(f'<li>{x}</li>' for x in what)}</ul>
        <p class="tier-note">{where}</p>
        <p><a class="btn primary" href="{M}{subj}">Ask about this</a></p>
      </section>
'''

adv = f'''    <p class="crumb"><a href="/sponsor-and-advertise/">← Sponsor &amp; advertise</a></p>
    <p class="kicker">For businesses, museums and events in the valley</p>
    <h1>Advertise with Project Scroll</h1>
    <p class="lede">People come to Project Scroll to read the valley’s history, play the hunt, and plan a day out: where to eat, where to stay, which museum to see. A local business can have a place beside that, clearly labeled and never mixed into the history itself.</p>

    <h2>Ways to advertise</h2>
    <div class="tiers">
{prod('a1', 'Featured partner card', ['A card with your name, a photograph, one line and a link', 'Placed on the pages where people plan a visit, such as Visit &amp; Plan and the food, stay and seasons pages', 'Marked “Paid partner” and kept apart from the chosen listings'], 'The card sits beside the listings, never among them. A place we already list stays exactly as it is.', 'Featured%20partner%20card')}
{prod('a2', 'Seasonal spot', ['One season on the seasons page: autumn color, a winter evening, spring blossom or a summer lake', 'Your card beside that season’s ideas for a day out', 'A good fit for an orchard, an inn, a festival or a shop with a busy season'], 'Booked a season at a time, with only a few spots in each.', 'Seasonal%20spot')}
{prod('a3', 'Facebook feature', ['A post about your business on Project Scroll’s Facebook page, with your pictures', 'Marked with Facebook’s own paid-partnership label', 'Written in the house style: plain, warm and accurate'], 'We write it with you and you see it before it goes out. History posts are never paid for.', 'Facebook%20feature')}
{prod('a4', 'Passport stop', ['A stamp for your business in the valley passport', 'Visitors who come in collect it on their trip', 'A good fit for a museum, a shop, a café or a historic inn'], 'The stop is marked as a partner stop, apart from the history stamps.', 'Passport%20stop')}
{prod('a5', 'Hunt prize', ['Give a prize for the hunt: a meal, a night’s stay, a book, a tour', 'Named as the prize’s giver when it is announced and awarded', 'Thanked on Facebook when the prize is won'], 'A prize never changes a clue, a case or an answer.', 'Hunt%20prize')}
      <section class="tier" aria-labelledby="a6">
        <p class="tier-k">Or</p><h3 id="a6">Something else in mind?</h3><p class="tier-amt">Ask us</p>
        <ul><li>An event, an open house, a reunion or a festival in the valley</li><li>Several placements together, for a season or a year</li><li>Paying for the research instead: that is <a href="/sponsors/">sponsorship</a></li></ul>
        <p class="tier-note">Tell us what you have in mind and we will say what fits, and what does not.</p>
        <p><a class="btn" href="{M}Advertising%20idea">Write to the desk</a></p>
      </section>
    </div>

{RULES}
    <h2>How it works</h2>
    <ol class="ad-steps">
      <li><b>Write to us</b> at <a href="mailto:research@projectscroll.com?subject=Advertising">research@projectscroll.com</a> with your business, the placement you have in mind, and when.</li>
      <li><b>We send rates</b> and the dates that are open, and say plainly if a placement is not a good fit.</li>
      <li><b>You send words and pictures,</b> or we write the card with you. You see it before it goes up.</li>
      <li><b>It goes up labeled,</b> for the time agreed, and comes down when it ends.</li>
    </ol>

    <p class="note">Advertising is separate from sponsorship. If you would rather pay for the research that keeps the hunt free, see <a href="/sponsors/">Sponsor the hunt</a>. Advertising enquiries: <a href="mailto:research@projectscroll.com?subject=Advertising">research@projectscroll.com</a>.</p>
    <p class="ctas"><a class="btn primary" href="{M}Advertising">Ask us for rates</a> <a class="btn" href="/sponsors/">Sponsor the hunt</a> <a class="btn" href="/visit/">Visit &amp; Plan</a></p>
'''

page('sponsor-and-advertise/index.html', 'Sponsor & advertise · Project Scroll',
     'Two ways to support Project Scroll’s free local-history hunt: sponsor the research, or advertise a valley business in a clearly labeled place. Ground rules and contact.',
     hub, og='https://projectscroll.com/og/sponsor-and-advertise.jpg?v=1')
page('advertise/index.html', 'Advertise with Project Scroll · Project Scroll',
     'Advertise a business, museum or event in the St. Joseph River valley on Project Scroll: featured partner cards, seasonal spots, Facebook features, passport stops and hunt prizes. Every paid place labeled. Ask us for rates.',
     adv, og='https://projectscroll.com/og/advertise.jpg?v=1')
print('sponsor & advertise pages built')
