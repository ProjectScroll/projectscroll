"""The valley letter: a monthly email. Until a mailing service is chosen, sign-up writes an email to the desk.
python3 _tools/build_newsletter.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
body = '''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Once a month, in your inbox</p>
    <h1>The valley letter</h1>
    <p class="lede">One short email a month from the St. Joseph River valley: the coming month’s festivals and fairs, a new story from the record, the document and the newspaper of the month, a recipe from the old cookbooks, and a clue for the hunt.</p>
    <ul class="dis">
      <li><b>Once a month.</b> No more, and never a sales pitch. Paid partners, when there are any, are labeled.</li>
      <li><b>Your address stays with us.</b> It is never sold, swapped or shared.</li>
      <li><b>One click to leave.</b> Every letter has an unsubscribe link.</li>
    </ul>
    <form class="nl-f" id="nlF" novalidate>
      <label for="nlE">Your email address</label>
      <div class="nl-row"><input type="email" id="nlE" autocomplete="email" required placeholder="you@example.com"><button type="submit" class="btn primary">Sign me up</button></div>
      <p class="nl-msg" id="nlM" aria-live="polite"></p>
    </form>
    <p class="note">The letter is starting up. Until its mailing service is in place, pressing “Sign me up” writes a short email to <b>research@projectscroll.com</b> in your own email program; nothing is sent until you press send there. We add you to the list by hand and confirm by reply.</p>
    <p class="ctas"><a class="btn" href="/seasons/">This month’s festivals</a> <a class="btn" href="/news/">The latest stories</a> <a class="btn" href="/feed.xml">The news feed (RSS)</a></p>
<script>
(function(){ var f=document.getElementById('nlF'), e=document.getElementById('nlE'), m=document.getElementById('nlM');
  f.addEventListener('submit',function(ev){ ev.preventDefault(); var v=e.value.trim();
    if (!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(v)){ m.textContent='Please check the email address.'; e.focus(); return; }
    location.href='mailto:research@projectscroll.com?subject='+encodeURIComponent('Sign me up for the valley letter')+'&body='+encodeURIComponent('Please add '+v+' to the valley letter.');
    m.textContent='Your email program should open with the message written. Press send there, and we will confirm by reply.'; });
})();
</script>
'''
page('newsletter/index.html', 'The valley letter · a monthly email · Project Scroll',
     'Sign up for the valley letter: one short email a month with the St. Joseph River valley’s festivals, a new story from the record, a recipe and a hunt clue.', body, og='https://projectscroll.com/og/about.jpg')
print('newsletter page built')
