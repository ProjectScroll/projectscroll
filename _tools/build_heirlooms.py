"""Heirlooms: things made or used in the valley and still kept by families. A form writes an email to the desk;
the cabinet shows only entries in data/heirlooms.json, each published with the owner's yes.  python3 _tools/build_heirlooms.py"""
import sys, json, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E = lambda s: html.escape(str(s), quote=True)
H = json.load(open(pathlib.Path(__file__).parent/'data'/'heirlooms.json'))

JS = r'''<script>
document.addEventListener('DOMContentLoaded', function(){ "use strict";
  var $=function(s){ return document.querySelector(s); }, f=$('#hlForm'), msg=$('#hlMsg'), KEY='ps-heirloom-draft';
  var F=['hlWhat','hlKind','hlMaker','hlWhen','hlFam','hlText','hlPics','hlName','hlTown'];
  try{ var d=JSON.parse(localStorage.getItem(KEY)||'{}'); F.forEach(function(id){ if (d[id]!=null) $('#'+id).value=d[id]; }); if (d.perm){ var r=f.querySelector('input[name=hperm][value="'+d.perm+'"]'); if (r) r.checked=true; } }catch(e){}
  var save=function(){ try{ var d={}; F.forEach(function(id){ d[id]=$('#'+id).value; }); var r=f.querySelector('input[name=hperm]:checked'); d.perm=r?r.value:''; localStorage.setItem(KEY, JSON.stringify(d)); }catch(e){} };
  f.addEventListener('input', save); f.addEventListener('change', save);
  var compose=function(){ var v=function(id){ return $('#'+id).value.trim(); }, r=f.querySelector('input[name=hperm]:checked');
    var L=['An heirloom for the Project Scroll cabinet','','What it is: '+v('hlWhat'),'Kind: '+$('#hlKind').selectedOptions[0].text];
    if (v('hlMaker')) L.push('Made by or where: '+v('hlMaker'));
    if (v('hlWhen')) L.push('About when: '+v('hlWhen'));
    if (v('hlFam')) L.push('How it came down: '+v('hlFam'));
    L.push('','ITS STORY',v('hlText')||'(not written)');
    if (v('hlPics')) L.push('','PHOTOGRAPHS I CAN SEND',v('hlPics'));
    L.push('','MAY IT GO IN THE CABINET?',r?r.parentNode.textContent.trim():'(not said)');
    L.push('','From: '+(v('hlName')||'(no name given)')+(v('hlTown')?', '+v('hlTown'):''));
    return {subject:'An heirloom: '+(v('hlWhat')||'from the valley'), body:L.join('\n')}; };
  f.addEventListener('submit', function(e){ e.preventDefault();
    if (!$('#hlWhat').value.trim()){ msg.textContent='Say what the heirloom is first.'; $('#hlWhat').focus(); return; }
    if (!f.querySelector('input[name=hperm]:checked')){ msg.textContent='Choose whether it may go in the cabinet, so we know what you want.'; f.querySelector('input[name=hperm]').focus(); return; }
    var c=compose(), url='mailto:research@projectscroll.com?subject='+encodeURIComponent(c.subject)+'&body='+encodeURIComponent(c.body);
    msg.textContent= url.length>1900 ? 'It is long, so your email program may cut it short. Press “Copy it” and paste it into an email to research@projectscroll.com instead.' : 'Your email program should open with it written in. Attach your photographs there, and press send. Nothing has been sent yet.';
    location.href=url; });
  $('#hlCopy').addEventListener('click', function(){ var c=compose(), t='To: research@projectscroll.com\nSubject: '+c.subject+'\n\n'+c.body;
    if (navigator.clipboard) navigator.clipboard.writeText(t).then(function(){ msg.textContent='Copied. Paste it into an email to research@projectscroll.com.'; }, function(){ msg.textContent='Your browser would not copy. Select the text and copy it by hand.'; }); });
  $('#hlClear').addEventListener('click', function(){ f.reset(); try{ localStorage.removeItem(KEY); }catch(e){} msg.textContent='Cleared.'; });
});
</script>'''

if H:
    cab = '<ul class="hl-cab">' + ''.join(f'<li class="hl-item" id="{E(h["id"])}"><figure><img src="{E(h["img"])}" alt="{E(h["alt"])}" loading="lazy" decoding="async"><figcaption><h3>{E(h["what"])}</h3><p>{E(h["story"])}</p><p class="credit">{E(h["by"])}</p></figcaption></figure></li>' for h in H) + '</ul>'
else:
    cab = '''<div class="hl-empty"><p><b>The cabinet is empty, and waiting for the first piece.</b> Every shelf will hold something a family in the valley still keeps, shown with its owner’s yes and in their words.</p>
      <p>The kinds of thing we hope to see:</p>
      <ul class="hl-kinds"><li>A Round Oak stove, or anything cast in Dowagiac</li><li>A Heddon lure, rod or tackle box</li><li>A quilt, a sampler or a coverlet, with the hands that made it</li><li>A family Bible with births and deaths written in</li><li>A crock, a jug or a churn from a valley pottery</li><li>A tool from the farm, the mill or the shop</li><li>A letter, a diary, a ledger or a receipt</li><li>A school medal, a band uniform, a lodge apron</li></ul></div>'''

body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Heirlooms</p>
    <h1>What the valley handed down</h1>
    <p class="lede" style="font-size:1.15rem">A stove from the Round Oak works. A lure carved in Dowagiac. A quilt pieced in a Porter Township farmhouse. Most of the valley’s history isn’t in a museum. It sits in a parlour, on a mantel, in a box in the attic. This is a cabinet for those things, and for the stories that came with them.</p>
    <section aria-labelledby="hlCH"><h2 id="hlCH">The cabinet</h2>
      {cab}</section>
    <section class="st-how" aria-labelledby="hlHowH"><h2 id="hlHowH">Add a piece</h2>
      <ol class="st-steps"><li><b>Tell us about it here.</b> The page writes an email for you. Nothing is sent until you press send.</li>
      <li><b>Send a photograph or two.</b> Attach them to the email: the whole thing, and any mark, label or signature on it.</li>
      <li><b>Nothing goes in the cabinet without your yes.</b> We send you exactly what would appear. You can say no, change it, or leave your name off. We never show where you live.</li></ol></section>
    <form class="rf st-form" id="hlForm" aria-labelledby="hlFH" novalidate>
      <h2 id="hlFH">Your heirloom</h2>
      <label class="st-wide"><span>What is it?</span><input id="hlWhat" type="text" maxlength="120" required placeholder="For example, my great-grandmother’s Round Oak parlour stove"></label>
      <label><span>What kind of thing?</span><select id="hlKind"><option>Made in the valley</option><option>Used in the valley</option><option>A paper, letter or book</option><option>A photograph</option><option>Something else</option></select></label>
      <label><span>Who made it, or where? <small>(if known)</small></span><input id="hlMaker" type="text" maxlength="120" placeholder="A maker’s mark, a factory, a person"></label>
      <label><span>About when?</span><input id="hlWhen" type="text" maxlength="60" placeholder="For example, about 1900"></label>
      <label><span>How did it come down to you?</span><input id="hlFam" type="text" maxlength="160" placeholder="For example, from my mother’s side"></label>
      <label class="st-wide"><span>Its story</span><textarea id="hlText" rows="7"></textarea></label>
      <label class="st-wide"><span>Photographs you can send <small>(optional)</small></span><input id="hlPics" type="text" maxlength="200" placeholder="For example, the front, and the maker’s plate"></label>
      <fieldset class="st-wide st-perm"><legend>May it go in the cabinet?</legend>
        <label><input type="radio" name="hperm" value="name"> Yes, with my name, once you have shown me what would appear</label>
        <label><input type="radio" name="hperm" value="anon"> Yes, but without my name</label>
        <label><input type="radio" name="hperm" value="desk"> No, it is only for the research desk</label></fieldset>
      <label><span>Your name <small>(optional)</small></span><input id="hlName" type="text" maxlength="60" autocomplete="name"></label>
      <label><span>Your town today <small>(optional)</small></span><input id="hlTown" type="text" maxlength="60" autocomplete="address-level2"></label>
      <p class="st-wide"><button class="btn primary" type="submit">Write the email</button> <button class="btn" type="button" id="hlCopy">Copy it</button> <button class="linkbtn" type="button" id="hlClear">Start over</button></p>
      <p class="st-wide mu-nmsg" id="hlMsg" aria-live="polite"></p>
    </form>
    <p class="note">Your draft is kept in this browser until you send it or start over. The site itself never receives it. We don’t value, buy or sell anything, and we never say where a piece is kept. If you know what valley factory made something, the <a href="/museums/">museums</a> and the <a href="/made-in-the-valley/">Made in the Valley</a> page may tell you more. Write to us directly at <a href="mailto:research@projectscroll.com">research@projectscroll.com</a>.</p>
''' + JS + '\n'
page('heirlooms/index.html', 'Heirlooms · Project Scroll', 'A cabinet of heirlooms from the St. Joseph River valley: stoves, lures, quilts, Bibles and tools still kept by families, shown with their owners’ yes. Add yours.', body, og='https://projectscroll.com/og/legends.jpg')
print('heirlooms built', len(H))
