# The sponsors page: who keeps the hunt free, what sponsorship buys and what it never buys, and the ledger.
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
M='mailto:research@projectscroll.com?subject='
body=f'''    <p class="crumb"><a href="/sponsor-and-advertise/">← Sponsor &amp; advertise</a></p>
    <p class="kicker">Keeping the hunt free</p>
    <h1>Sponsor the hunt</h1>
    <p class="lede">The hunt is free to play and always will be. The research behind it is not free to do: the scans, the certificates, the microfilm, the hours in the record. Sponsors pay for those. In return they are named, thanked, and shown exactly what their money bought.</p>

    <section class="pledge" aria-labelledby="pledgeH">
      <h2 id="pledgeH">What sponsorship buys, and what it never buys</h2>
      <p>Sponsorship funds the work. It does not choose a case, shape a finding, or see a report before readers do. No sponsor’s name goes beside evidence. If a sponsor ever asked for any of that, the money would go back. That is the whole bargain, and it is why a sponsor’s name on this site means something.</p>
    </section>

    <h2>Four ways in</h2>
    <div class="tiers">
      <section class="tier" aria-labelledby="t1">
        <p class="tier-k">Individuals</p><h3 id="t1">Friend of the hunt</h3><p class="tier-amt">Any amount, once or monthly</p>
        <ul><li>Named on this page (or anonymous, as you prefer)</li><li>The <b>Benefactor</b> tin badge in your field book</li><li>Thanked in the feed when a case you helped fund is solved</li></ul>
        <p class="tier-note">Most friends give $5 a month or $25 once. Every dollar goes to the record.</p>
        <p><a class="btn primary" href="{M}Friend%20of%20the%20hunt">Become a friend</a></p>
      </section>
      <section class="tier" aria-labelledby="t2">
        <p class="tier-k">Individuals and families</p><h3 id="t2">Patron of a case</h3><p class="tier-amt">$150 · one case</p>
        <ul><li>Underwrites the next case on the board: research hours, scans, certificates</li><li>Named on that case’s page: “Opened with the help of …”</li><li>A copy of the sourced report when the case closes</li><li>The <b>Patron</b> badge</li></ul>
        <p class="tier-note">Patrons fund the next case in line. They do not choose it, and they never choose the answer.</p>
        <p><a class="btn primary" href="{M}Patron%20of%20a%20case">Fund a case</a></p>
      </section>
      <section class="tier" aria-labelledby="t3">
        <p class="tier-k">Businesses</p><h3 id="t3">Business sponsor</h3><p class="tier-amt">$300 a year · three places</p>
        <ul><li>A card in the sponsors’ strip on the home page: your name, one line, a link</li><li>Named on this page and in the yearly ledger</li><li>Thanked once a quarter on Project Scroll’s Facebook page</li><li>Never placed beside a case’s evidence, never in a post</li></ul>
        <p class="tier-note">Set like the business cards in an old county newspaper. Three places only, so each is worth having.</p>
        <p><a class="btn primary" href="{M}Business%20sponsor">Ask about a place</a></p>
      </section>
      <section class="tier" aria-labelledby="t4">
        <p class="tier-k">Organizations</p><h3 id="t4">Underwriter</h3><p class="tier-amt">$1,000 and up · a season</p>
        <ul><li>Underwrites a whole hall of the hunt, a document series, or a year of the Document of the Month</li><li>“Presented with …” on the hall’s page and in the feed</li><li>A short letter of agreement, and the ledger line that shows what it paid for</li></ul>
        <p class="tier-note">For a library, a historical society, a lake association, a family reunion, a foundation. Research to your own question is a commission, not a sponsorship: <a href="/research/">the research desk</a>.</p>
        <p><a class="btn primary" href="{M}Underwriting">Talk to us</a></p>
      </section>
    </div>

    <h2>Other ways to keep it going</h2>
    <ul class="ways">
      <li><b>Give a document.</b> A scan of a county history, an atlas, a letter, a photograph of a place as it was. Credited by name on the page it opens.</li>
      <li><b>Give a record.</b> Buy one certificate or one microfilm reel for a case and we post the receipt in the ledger beside your name.</li>
      <li><b>Give your time.</b> Transcribe a page, read a reel, walk a cemetery with a camera. Every finding is marked with its finder.</li>
      <li><b>Give the hunt a room.</b> A library or society that hosts a hunt night gets the cases, the worksheets and the research desk for the evening.</li>
      <li><b>Remember it.</b> A gift in a will, to carry a hall of the hunt after its first sponsor. Ask us and we will send a line of wording.</li>
    </ul>

    <h2 id="ledger">The ledger</h2>
    <p>Every quarter, what came in and what it paid for, so that anyone can see the money went to the record.</p>
    <table class="ledger"><caption>Sponsorship ledger</caption>
      <thead><tr><th scope="col">Quarter</th><th scope="col">Received</th><th scope="col">Spent on</th></tr></thead>
      <tbody><tr><td>Autumn 2026</td><td>—</td><td>The first quarter. The ledger opens with the first gift.</td></tr></tbody>
    </table>

    <h2>Friends of the hunt</h2>
    <p class="note" id="friends">No names yet. The first will be here, and so will the hundredth.</p>

    <p class="note">Want a labelled place for your business instead? That is advertising, and it is kept separate: <a href="/advertise/">Advertise with us</a>.</p>
    <p class="note">Sponsorship is income to Project Scroll, an independent research desk, and is not a tax-deductible gift. Sponsors are listed with their permission and may be anonymous. Questions: <a href="mailto:research@projectscroll.com?subject=Sponsorship">research@projectscroll.com</a>.</p>
    <p class="ctas"><a class="btn primary" href="{M}Sponsorship">Write to the desk</a> <a class="btn" href="/#hunt">Play the hunt</a> <a class="btn" href="/research/">Research services</a></p>
'''
page('sponsors/index.html', 'Sponsor the hunt · keep the research free · Project Scroll',
     'Sponsor Project Scroll’s free history hunt: friends, patrons of a case, business sponsors and underwriters. What sponsorship buys, what it never buys, and a public ledger of what every gift paid for.', body, og='https://projectscroll.com/og/hunt.jpg')
print('sponsors page built')
