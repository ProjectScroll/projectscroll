"""The terms-and-disclaimers page and the accessibility statement:  python3 _tools/build_legal.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page

terms='''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">The fine print</p>
    <h1>Terms and disclaimers</h1>
    <p class="lede">Project Scroll is a free treasure hunt through real history, and a research desk. These are the plain terms of playing, reading and hiring. By using the site you agree to them.</p>
    <h2 id="hunt">The hunt</h2>
    <ul>
      <li><b>Nothing is buried.</b> There is no physical treasure, cache or prize hidden anywhere. Every answer is in a book, a map, a certificate or a page.</li>
      <li><b>Never dig, never trespass.</b> Do not enter private land, disturb a grave, a cemetery, a burial ground or an archaeological site, or remove anything from the ground or from public land. Doing so can be a crime under state and federal law, and it is never needed to solve a case.</li>
      <li><b>Recognition, not prizes.</b> The only reward is your name on the case board and in the next post. Nothing is sold, no purchase is needed, and there is no entry fee.</li>
      <li><b>You play at your own risk</b> and are responsible for your own safety, travel and conduct. Be kind: the people in these records are real, and their families still live here.</li>
      <li><b>Facebook.</b> Clues are posted on Project Scroll’s Facebook page. Facebook is a service of Meta Platforms, Inc., which is not a sponsor of the hunt and does not run it; your use of Facebook is governed by its own terms.</li>
    </ul>
    <h2 id="history">The history on these pages</h2>
    <ul>
      <li><b>Drawn from the record, not guaranteed.</b> Dates, names and facts come from the published histories, maps, certificates and newspapers cited on each page, and those sources contain mistakes of their own. We mark how far each source can be trusted and correct what we get wrong: write to <a href="mailto:research@projectscroll.com?subject=Correction">research@projectscroll.com</a>.</li>
      <li><b>Not legal, title or survey advice.</b> The old maps and plats show land as it was drawn in their own day. They are not current property lines, deeds or surveys, and nothing here is legal, title, tax, medical or financial advice.</li>
      <li><b>Family stories.</b> Legends and traditions are reported as traditions and labelled so. A tradition on this site is not a claim that it happened.</li>
      <li><b>Pictures.</b> Maps, book pages, certificates and postcards are reproduced from public-domain originals and credited to the library or archive that holds them. Some masthead plates and illustrations are modern artwork made for Project Scroll to set a scene; they are not historical photographs and are not evidence. A caption that names a book, map, postcard or print is the record itself.</li>
    </ul>
    <h2 id="services">Research and studio commissions</h2>
    <ul>
      <li><b>Estimates first.</b> Every commission starts with an honest first read and a written estimate before you commit to anything.</li>
      <li><b>No promise of an answer.</b> Some records were never made, were lost, or are closed by law. We report what the record shows, including when it shows nothing.</li>
      <li><b>Your report is yours.</b> Nothing about your family is published or shared without your written word.</li>
    </ul>
    <h2 id="sponsors">Sponsorship</h2>
    <p>Sponsorship is income to Project Scroll, an independent research desk. It is not a charitable donation and is not tax-deductible. Sponsors are listed only with their permission. A sponsor’s name on the site is a thank-you, not an endorsement of the sponsor by Project Scroll or of Project Scroll by the sponsor. See <a href="/sponsors/">Sponsor the hunt</a>.</p>
    <h2 id="names">Names, links and affiliation</h2>
    <ul>
      <li>Project Scroll is independent. It is not affiliated with, endorsed by or speaking for any village, township, county, state, tribal nation, library, archive, historical society or fraternal organization named on the site.</li>
      <li>Names of organizations, publications and products belong to their owners and are used only to identify them.</li>
      <li>Links to other sites are offered for your research. We do not control those sites and are not responsible for their content or their privacy practices.</li>
    </ul>
    <h2 id="copyright">Copyright</h2>
    <p>The text, design and original artwork of Project Scroll are © 2026 Project Scroll. You are welcome to quote a passage with credit and a link; please ask before reusing whole pages. The original photographs, illustrations, artwork and studio images on this site may not be downloaded, copied or reused without written permission from Project Scroll. Public-domain maps and documents stay public domain: the credit line on each says where the original is held. To cite a page, use the form in the footer.</p>
    <h2 id="liability">Limits</h2>
    <p>The site is offered as it is, without warranties of any kind. To the extent the law allows, Project Scroll is not liable for any loss or harm arising from use of the site or reliance on its contents. These terms may change; the date below says when they last did.</p>
    <p class="note">Last updated 23 October 2026. Questions: <a href="mailto:research@projectscroll.com?subject=Terms">research@projectscroll.com</a>. See also the <a href="/privacy/">privacy page</a> and the <a href="/accessibility/">accessibility statement</a>.</p>
'''
page('terms/index.html','Terms and disclaimers · Project Scroll','The plain terms of Project Scroll: nothing is buried, never dig or trespass, recognition not prizes, history from the record but not guaranteed, and how pictures, sponsorship and copyright work.',terms)

acc='''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">For every reader</p>
    <h1>Accessibility</h1>
    <p class="lede">The hunt is open to anyone, anywhere, and that includes anyone who reads with a keyboard, a screen reader, a magnifier, captions or a steady page. We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.2 at level AA, and we test every change against them.</p>
    <h2 id="built-in">What is built in</h2>
    <ul>
      <li><b>Keyboard.</b> Every link, button, filter, map control and dialog works from the keyboard. A “Skip to the content” link is the first thing on every page. Press <kbd>/</kbd> or <kbd>Ctrl</kbd> <kbd>K</kbd> to search.</li>
      <li><b>Screen readers.</b> Pages use real headings, landmarks and labels. Pictures carry text descriptions; decorative ornaments are hidden from screen readers.</li>
      <li><b>Motion.</b> If your device asks for reduced motion, the gold leaf, glints, rolling place names and drawn trails hold still. The <b>Pause all motion</b> switch at the foot of every page does the same on any device, and remembers your choice.</li>
      <li><b>Light and dark.</b> The site follows your device, and the moon button switches by hand. Text and controls are checked for contrast in both.</li>
      <li><b>Listening.</b> The <b>Listen</b> buttons read a section aloud with your device’s own voice.</li>
      <li><b>Text size.</b> Zoom to 200% or more and the page reflows to one column without sideways scrolling.</li>
      <li><b>Print.</b> Every page prints cleanly, without the animations and controls.</li>
    </ul>
    <h2 id="limits">What is harder, and how we help</h2>
    <ul>
      <li><b>The deep-zoom maps</b> in the map room are pictures served by the Library of Congress. Their town names and directories are given in text beside them, and we will read any part of a map for you on request.</li>
      <li><b>Old handwriting and print.</b> Certificates and book pages are shown as pictures. Where a page is the subject of a case, its key lines are transcribed in the text; ask, and we will transcribe any page you need.</li>
      <li><b>Facebook.</b> Clues are posted on Facebook, whose accessibility is Meta’s. Every case also has its own page here.</li>
    </ul>
    <h2 id="help">Tell us</h2>
    <p>If anything on Project Scroll is hard to use, write to <a href="mailto:research@projectscroll.com?subject=Accessibility">research@projectscroll.com</a> with the page and what happened. We answer, and we fix what we can.</p>
    <p class="note">Last reviewed 20 October 2026.</p>
'''
page('accessibility/index.html','Accessibility · Project Scroll','How Project Scroll works with keyboards, screen readers, reduced motion, dark mode and zoom, what is harder, and how to ask for help.',acc)
print('legal pages built')
