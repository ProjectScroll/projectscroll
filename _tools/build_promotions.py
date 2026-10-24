"""The promotions page: how local businesses, organizations and people can be part of Project Scroll. python3 _tools/build_promotions.py"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pages import page
CARDS = [
 ('Sponsor a quest case', 'Your name on a real mystery of the valley.', ['Your business named as the sponsor of a case on the quest, on its page and in the Facebook post that opens it', 'A thank-you on the case board for as long as the case stands', 'A prize for the first solver, if you would like to offer one'], 'Sponsoring a case'),
 ('Your history, told', 'The story of your business, building, farm, church or club, from the record.', ['A researched feature story on Project Scroll, every fact sourced, with your own photographs', 'A share card ready for Facebook and email', 'A printed edition for your wall, your counter or your anniversary'], 'Our history, told'),
 ('Brought to you by', 'A place beside the stories people already read and share.', ['“Brought to you by” on a related story about your town or your trade', 'A listing on the Visit &amp; Plan pages, with directions and hours', 'A mention in the This Day in the Valley almanac'], 'A sponsorship line'),
 ('Events and anniversaries', 'A centennial, an open house, a homecoming or a reunion.', ['A timeline poster from your own records and ours', 'Ready-to-post Facebook posts, written and sized for you', 'A then-and-now photo pair of your place, past and present'], 'An event or anniversary'),
 ('See it from the air', 'Your place, the way nobody has seen it.', ['Drone photography and video', 'A 3D LiDAR fly-through of your property, your town or your trail', 'Restored historic photographs for menus, walls and websites'], 'Drone, video or 3D'),
 ('Design that lasts', 'For businesses, societies and organizations.', ['Websites built to be fast, readable and easy to keep up', 'Logos, signs, brochures and keepsakes', 'History signs with a QR code that opens your story on a phone'], 'Web or graphic design'),
]
cards = ''.join(f'''<section class="sv-col pr-card" aria-labelledby="pr{i}"><p class="sv-no" aria-hidden="true">No. {i+1}</p><h3 id="pr{i}">{t}</h3><p class="sv-d">{d}</p><ul>{"".join(f"<li>{x}</li>" for x in L)}</ul><p class="sv-ask"><a href="/#contact" data-need="{n}">Ask about this ›</a></p></section>''' for i,(t,d,L,n) in enumerate(CARDS))
body = f'''
    <p class="crumb"><a href="/">Front page</a> · <a href="/services/">Services</a> · Promotions</p>
    <aside class="promo sv mod pr-hero" aria-labelledby="prH">
      <i class="sv-orn o1" aria-hidden="true">❦</i><i class="sv-orn o2" aria-hidden="true">❦</i><i class="sv-orn o3" aria-hidden="true">❦</i><i class="sv-orn o4" aria-hidden="true">❦</i>
      <p class="sv-banner"><span>★ Promotions ★</span></p>
      <h1 class="promo-h" id="prH">Put your business in the story.</h1>
      <p class="sv-serve">For local businesses, organizations and families across the St. Joseph River valley</p>
      <p class="promo-lede">People come to Project Scroll for the valley’s true stories: its towns, lakes, mysteries and the families who built them. Promotions put your name beside those stories, honestly marked, and help keep the quest free for everyone.</p>
      <div class="sv-cols pr-cols">{cards}</div>
      <div class="sv-coupon">
        <p><b>Always marked, never bought.</b> Every promotion is labelled as sponsored. Sponsors never change what the record says, and every fact on the site stays sourced, whoever pays for the page it sits on.</p>
        <p class="sv-own"><b>Start with a conversation.</b> Tell us what you have in mind. We tell you what can be done, what it will take, and when, before you commit to anything.</p>
        <p class="promo-ctas"><a class="btn primary" href="/#contact" data-need="A promotion">Tell us what you need</a><a class="btn" href="/services/">All our services</a><a class="btn" href="/sponsors/">How sponsorship keeps the quest free</a></p>
      </div>
      <p class="sv-more">Or write to <a href="mailto:research@projectscroll.com?subject=Promotions">research@projectscroll.com</a>.</p>
    </aside>
'''
page('promotions/index.html', 'Promotions for local businesses and organizations · Project Scroll', 'Sponsor a quest case, have your history told from the record, or put your name beside the valley’s true stories. Promotions from Project Scroll, always marked as sponsored.', body)
print('promotions built')
