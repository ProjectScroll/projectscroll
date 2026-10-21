"""Cassopolis on old postcards: stand where the photographer stood.  python3 _tools/build_postcards.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
CARDS=[
 ('yerty','West side of Broadway, looking south','A Yerty postcard. The photographer stood on Broadway with the stores of the west side on the right.'),
 ('broadway1','Broadway in the days of wagons','Horses and wagons on the main street, the store fronts close together.'),
 ('carriages','Carriages drawn up on Broadway','A row of buggies at the hitching rail: a market day, or a meeting.'),
 ('broadway3','Broadway when the first cars came','Early motor cars among the last of the buggies.'),
 ('broadway2','A Cassopolis street, early 1900s','Which street is it? The trees, the walks and the buildings are the clues.'),
 ('roadtotown','The road to town','The way in from the country. Where did it come in, and is the road still there?'),
]
figs=''.join(f'''      <figure class="pc"><picture><source type="image/webp" srcset="/img/strip/{k}-800.webp 800w, /img/strip/{k}.webp 1600w" sizes="(min-width:900px) 46rem, 92vw"><img src="/img/strip/{k}-800.webp" width="1600" height="400" alt="{t}, Cassopolis, on an old postcard." loading="lazy" decoding="async"></picture>
        <figcaption><b>{t}.</b> {n} <a href="/map/cassopolis/#17.00/41.91160/-86.01250">Find it on the 1860 plan →</a></figcaption></figure>
''' for k,t,n in CARDS)
body=f'''    <p class="crumb"><a href="/map/">← The map room</a></p>
    <p class="kicker">Postcards, then and now</p>
    <h1>Stand where the photographer stood</h1>
    <p class="lede" style="font-size:1.15rem">Old postcards of Cassopolis, from the days of wagons to the first motor cars. Each one was taken from a spot you can still stand on. Find it, take the same picture today, and send it to us: we will set your photograph beside the old one here, with your name on it.</p>
{figs}
    <h2>How to rephotograph a postcard</h2>
    <ol class="dis">
      <li><b>Find the spot.</b> Line up two things that have not moved, a corner of a building and a street, and walk until they sit in the picture the way they sit on the card.</li>
      <li><b>Match the height.</b> Most old postcards were taken from about head height; some from an upstairs window. Hold the camera where the photographer’s eye was.</li>
      <li><b>Match the lens.</b> Use your phone’s ordinary camera, not the wide one, and do not zoom.</li>
      <li><b>Stay safe and on public ground.</b> Never step into the road for a shot, and never go onto private property without leave.</li>
      <li><b>Send it in</b> to <a href="mailto:research@projectscroll.com?subject=Rephotographed%20postcard">research@projectscroll.com</a>, saying which card and when you took it. By sending it you let us show it here with your name.</li>
    </ol>
    <p class="note">The pictures are taken from old postcards of Cassopolis. Each was published before 1931, or published without a copyright notice, and is in the public domain in the United States. The pairings will be added as readers send them in.</p>
'''
page('postcards/index.html','Stand where the photographer stood · Postcards, then and now · Project Scroll','Old postcards of Cassopolis, Michigan, from the days of wagons to the first cars: find where each was taken, take it again today, and see the two side by side.',body,og='https://projectscroll.com/og/cassopolis.jpg')
print('postcards built')
