"""Share Your Story: a form that writes an email to the research desk. Nothing is sent by the site and nothing is published
without the teller's word and the desk's check against the record.  python3 _tools/build_story.py"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page

JS = r'''<script>
document.addEventListener('DOMContentLoaded', function(){ "use strict";
  var $=function(s){ return document.querySelector(s); }, f=$('#stForm'), msg=$('#stMsg'), KEY='ps-story-draft';
  setTimeout(function(){ try{ var hk=location.hash.slice(1), so=document.querySelector('#stKind option[value="'+hk+'"]'); if (so) so.selected=true; }catch(e){} },0);
  var F=['stName','stTown','stKind','stWhere','stWhen','stText','stHow','stPics'];
  /* a draft kept on this device only, so a long story is not lost if the page closes */
  try{ var d=JSON.parse(localStorage.getItem(KEY)||'{}'); F.forEach(function(id){ if (d[id]!=null) $('#'+id).value=d[id]; }); if (d.perm) { var r=f.querySelector('input[name=perm][value="'+d.perm+'"]'); if (r) r.checked=true; } }catch(e){}
  var save=function(){ try{ var d={}; F.forEach(function(id){ d[id]=$('#'+id).value; }); var r=f.querySelector('input[name=perm]:checked'); d.perm=r?r.value:''; localStorage.setItem(KEY, JSON.stringify(d)); }catch(e){} };
  f.addEventListener('input', save); f.addEventListener('change', save);
  var count=function(){ var n=$('#stText').value.trim().split(/\s+/).filter(Boolean).length; $('#stCount').textContent=n? n+(n===1?' word':' words') : ''; };
  $('#stText').addEventListener('input', count); count();
  var compose=function(){
    var v=function(id){ return $('#'+id).value.trim(); }, r=f.querySelector('input[name=perm]:checked');
    var kind=$('#stKind').selectedOptions[0].text;
    var lines=['A story for Project Scroll','','Kind: '+kind];
    if (v('stWhere')) lines.push('Where: '+v('stWhere'));
    if (v('stWhen')) lines.push('When: '+v('stWhen'));
    lines.push('','THE STORY',v('stText'),'','HOW I KNOW IT',v('stHow')||'(not said)');
    if (v('stPics')) lines.push('','PHOTOGRAPHS OR PAPERS I CAN SEND',v('stPics'));
    lines.push('','MAY IT BE SHARED?',r?r.parentNode.textContent.trim():'(not said)');
    lines.push('','From: '+(v('stName')||'(no name given)')+(v('stTown')?', '+v('stTown'):''));
    return {subject:'A story: '+(v('stWhere')||kind), body:lines.join('\n')};
  };
  f.addEventListener('submit', function(e){ e.preventDefault();
    if (!$('#stText').value.trim()){ msg.textContent='Write the story first: the box marked “The story” is empty.'; $('#stText').focus(); return; }
    if (!f.querySelector('input[name=perm]:checked')){ msg.textContent='Choose whether the story may be shared, so we know what you want.'; f.querySelector('input[name=perm]').focus(); return; }
    var c=compose(), url='mailto:research@projectscroll.com?subject='+encodeURIComponent(c.subject)+'&body='+encodeURIComponent(c.body);
    if (url.length>1900){ msg.textContent='The story is long, so your email program may cut it short. Press “Copy the story” and paste it into an email to research@projectscroll.com instead.'; }
    else msg.textContent='Your email program should open with the story written in. Attach any photographs there, and press send. Nothing has been sent yet.';
    location.href=url; if (window.psEarn) window.psEarn('teller'); });
  $('#stCopy').addEventListener('click', function(){ var c=compose(), t='To: research@projectscroll.com\nSubject: '+c.subject+'\n\n'+c.body;
    var done=function(){ msg.textContent='Copied. Paste it into an email to research@projectscroll.com.'; if (window.psEarn) window.psEarn('teller'); };
    if (navigator.clipboard) navigator.clipboard.writeText(t).then(done, function(){ msg.textContent='Your browser would not copy. Select the story and copy it by hand.'; }); });
  $('#stClear').addEventListener('click', function(){ f.reset(); try{ localStorage.removeItem(KEY); }catch(e){} count(); msg.textContent='Cleared.'; });
});
</script>'''

body = '''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Share your story</p>
    <h1>What do you know that the books don’t?</h1>
    <p class="lede" style="font-size:1.15rem">The county histories were written by a few men in a few years. Everything they left out is still in the valley: in a grandmother’s telling, a box of photographs, the deed in a drawer, the name on a barn. Tell us what you know, and how you know it.</p>
    <section class="st-how" aria-labelledby="stHowH"><h2 id="stHowH">What happens to it</h2>
      <ol class="st-steps"><li><b>You write it here.</b> The page writes an email for you. Nothing is sent until you press send in your own email program.</li>
      <li><b>We read it, and look for the record.</b> A story the record bears out is marked as found in the record. A story it can’t yet confirm is marked as family memory, with your name if you want it.</li>
      <li><b>Nothing goes on the site without your yes.</b> Before anything is published, we send you exactly what would appear, and you say yes, no, or change it.</li></ol>
      <p>Published stories, unnamed photographs and answered questions appear in <a href="/voices/">Valley Voices</a>; corrections are listed on the <a href="/corrections/">corrections page</a>.</p></section>
    <form class="rf st-form" id="stForm" aria-labelledby="stFH" novalidate>
      <h2 id="stFH">Your story</h2>
      <label><span>What kind of story?</span><select id="stKind"><option value="family">A family story</option><option value="place">A place, a building or a business</option><option value="photo">A photograph or a paper I have</option><option value="event">Something that happened</option><option value="who">Who is this? A photograph I can’t name</option><option value="ask">A question for Ask the desk</option><option value="listevent">An event for the valley calendar</option><option value="listplace">A place to add to the map</option><option value="fix">A correction to this site</option></select></label>
      <label><span>Where <small>(town, road or building)</small></span><input id="stWhere" type="text" maxlength="120" placeholder="For example, Front Street, Dowagiac"></label>
      <label><span>About when?</span><input id="stWhen" type="text" maxlength="60" placeholder="For example, the 1920s"></label>
      <label class="st-wide"><span>The story</span><textarea id="stText" rows="9" required aria-describedby="stCount stTip"></textarea><small id="stCount" aria-live="polite"></small></label>
      <p class="st-wide note" id="stTip">Please leave out anything private about people still living: their addresses, health or troubles. If a living person is part of the story, ask them first.</p>
      <label class="st-wide"><span>How do you know it? <small>(who told you, what paper shows it, or were you there)</small></span><textarea id="stHow" rows="3"></textarea></label>
      <label class="st-wide"><span>Photographs or papers you could send <small>(optional)</small></span><input id="stPics" type="text" maxlength="200" placeholder="For example, a 1910 postcard of the depot"></label>
      <fieldset class="st-wide st-perm"><legend>May it be shared?</legend>
        <label><input type="radio" name="perm" value="name"> Yes, with my name, once you have shown me what would appear</label>
        <label><input type="radio" name="perm" value="anon"> Yes, but without my name</label>
        <label><input type="radio" name="perm" value="desk"> No, it is only for the research desk</label></fieldset>
      <label><span>Your name <small>(optional)</small></span><input id="stName" type="text" maxlength="60" autocomplete="name"></label>
      <label><span>Your town today <small>(optional)</small></span><input id="stTown" type="text" maxlength="60" autocomplete="address-level2"></label>
      <p class="st-wide"><button class="btn primary" type="submit">Write the email</button> <button class="btn" type="button" id="stCopy">Copy the story</button> <button class="linkbtn" type="button" id="stClear">Start over</button></p>
      <p class="st-wide mu-nmsg" id="stMsg" aria-live="polite"></p>
    </form>
    <p class="note">Your draft is kept in this browser until you send it or start over, so a long story isn’t lost if the page closes. The site itself never receives it. Photographs: attach them to the email, or say what you have and we will ask. Write to us directly any time at <a href="mailto:research@projectscroll.com">research@projectscroll.com</a>.</p>
''' + JS + '\n'
page('story/index.html', 'Share your story · Project Scroll', 'Tell Project Scroll a story of the St. Joseph River valley: a family memory, a building, a photograph or a correction. The page writes an email for you, and nothing is published without your yes.', body, og='https://projectscroll.com/og/legends.jpg')
print('story built')
