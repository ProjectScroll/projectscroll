"""Builds 'Reading old gravestones':  python3 _tools/build_stones.py"""
import sys, pathlib, html; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E=html.escape
CARDS=[
 ('willow · urn','Willow and urn','A weeping willow over an urn: mourning, carved most often from about the 1790s to the 1850s. A rough date for a stone whose numbers have worn away.'),
 ('lamb','A lamb','Usually a child’s grave. Lambs on small stones are among the commonest carvings of the 1800s.'),
 ('a hand','A hand pointing up','Hope of heaven. A hand reaching down from a cloud is God calling the soul home; it does not mean a sudden death, though it is often read that way.'),
 ('two hands','Clasped hands','A farewell, or a marriage. Look at the cuffs: a man’s and a woman’s sleeve mean husband and wife.'),
 ('FLT','Three linked rings','The Odd Fellows, a fraternal order: Friendship, Love and Truth. A lead to a lodge’s records and its burial benefit.'),
 ('square · compass','Square and compass','The Freemasons. Like the rings, it points to a lodge that may have kept minutes and paid for the funeral.'),
 ('G.A.R.','A bronze star or flag holder','The Grand Army of the Republic, the society of Union veterans of the Civil War. The man was a soldier; look for his regiment.'),
 ('a shield','A marble stone with a sunk shield','A government headstone for a Union soldier, with his company and regiment cut in the shield: the key to his service record and pension file.'),
 ('ætat · æ','In the 74th year of his age','“Ætat.” or “æ.” means aged. “In the 74th year of his age” means he was 73: the 74th year began on his 73rd birthday.'),
 ('23y 4m 12d','Ages to the day','Age in years, months and days. Count back from the date of death to the birth date with the <a href="/toolkit/#age">age calculator</a>.'),
 ('consort · relict','Wife or widow','“Consort of” means his wife, who died while he lived. “Relict of” means his widow, who outlived him.'),
 ('marble · granite','What it is made of','Marble, white or grey, was usual from about the 1830s to 1900 and dissolves slowly in the rain, so its letters soften. Granite took over from the late 1800s. A hollow, blue-grey stone with crisp letters is “white bronze”, cast zinc, sold from the 1870s to about 1914.'),
]
Q=[
 ('A stone reads “in the 74th year of his age.” How old was he?',['73','74','75'],0,'The 74th year begins on the 73rd birthday.'),
 ('A small stone is carved with a lamb. Whose grave is it most likely to be?',['A shepherd’s','A child’s','A minister’s'],1,'Lambs mark children’s graves.'),
 ('Three linked rings with the letters F L T stand for…',['The Odd Fellows','The Freemasons','A church choir'],0,'Friendship, Love and Truth, the Odd Fellows’ motto.'),
 ('An upright marble stone has a sunk shield with a company and regiment. What is it?',['A family monument','A government headstone for a Union soldier','A lodge marker'],1,'And it tells you which regiment’s records to search.'),
 ('A blue-grey stone sounds hollow when tapped and its letters are as sharp as new. It is probably…',['Slate','Granite','White bronze (zinc)'],2,'Cast zinc, sold from the 1870s to about 1914.'),
]
cards=''.join(f'<div class="hcard"><p class="glyph">{g}</p><h3>{E(t)}</h3><p>{d}</p></div>' for g,t,d in CARDS)
quiz=''.join(f'<li data-a="{a}"><p>{E(q)}</p><p class="qopts">'+''.join(f'<button type="button" class="btn" data-i="{i}">{E(o)}</button>' for i,o in enumerate(opts))+f'</p><p class="qwhy" hidden>{E(w)}</p></li>' for q,opts,a,w in Q)
body=f'''    <p class="crumb"><a href="/toolkit/">← The hunter’s toolkit</a></p>
    <p class="kicker">A guide from the desk</p>
    <h1>Reading old gravestones</h1>
    <p class="lede" style="font-size:1.15rem">A gravestone is a record, cut in stone by a family that wanted to be remembered. It is also often wrong: carved years after the death, from memory, by a stonecutter paid by the letter. Here is how to read one, and how far to trust it.</p>
    <h2>What the stone is telling you</h2>
    <div class="hcards">{cards}</div>
    <h2>How far to trust a stone</h2>
    <ul class="dis">
      <li><b>When was it carved?</b> Many stones were put up years after the burial, and a family stone listing several people was often cut all at once, long after the first death. The dates on it are memories.</li>
      <li><b>Who paid for it?</b> The family, so the stone says what the family believed: the age they remembered, the spelling they used.</li>
      <li><b>Check it against a record made at the time:</b> a death certificate, a church burial register, a newspaper notice, the cemetery’s own book. Where they disagree, the record made at the time usually wins. See <a href="/guide/death-certificate/">how to read a death certificate</a>.</li>
      <li><b>A missing stone is not a missing grave.</b> Wooden markers rotted, stones broke and were cleared away, and many people never had a stone at all.</li>
    </ul>
    <h2>Reading a worn stone, without harming it</h2>
    <ul class="dis">
      <li><b>Use raking light.</b> Hold a mirror or a torch low and to one side so the light skims across the face; the letters appear in shadow. Try different times of day.</li>
      <li><b>Photograph it</b> straight on and at an angle, with the light coming from several sides.</li>
      <li><b>Never</b> use shaving cream, flour, chalk, bleach, wire brushes or household cleaners. They stay in the stone and eat it. Do not make rubbings of soft, flaking or leaning stones; on a sound stone, ask the cemetery first.</li>
      <li><b>Leave it as you found it.</b> Do not lean on stones, prop them up or move pieces. Report damage to the cemetery’s keeper.</li>
    </ul>
    <h2>Be a good visitor</h2>
    <ul class="dis">
      <li>Keep to the paths and the cemetery’s hours, and ask permission before entering a private family plot.</li>
      <li>Never dig, probe or disturb the ground, and never take anything away. It is wrong, and in Michigan and Indiana, as elsewhere, it can be a crime. No case on Project Scroll ever needs it.</li>
      <li>Remember the families. The people buried here have descendants nearby.</li>
    </ul>
    <h2>Test yourself</h2>
    <p class="note">Five questions. <span id="hq" aria-live="polite"></span></p>
    <ol class="hquiz">{quiz}</ol>
    <p class="note">Finding a stone: indexes such as <a href="https://www.findagrave.com" rel="noopener">Find a Grave</a> are built by volunteers from photographs; use them to find a stone, then read the stone, or its photograph, yourself.</p>
    <p class="ctas" style="margin-top:1.4rem"><a class="btn primary" href="/toolkit/">Back to the toolkit</a><a class="btn" href="/guide/old-handwriting/">Reading the old hand</a></p>
    <script>
    (function(){{ var items=[].slice.call(document.querySelectorAll('.hquiz > li')), s=0, n=0, out=document.getElementById('hq');
      items.forEach(function(li){{ li.querySelectorAll('button').forEach(function(b){{ b.addEventListener('click', function(){{
        if (li.dataset.done) return; li.dataset.done=1; n++; var ok=b.dataset.i===li.dataset.a; if (ok) s++;
        li.querySelectorAll('button').forEach(function(x){{ x.disabled=true; if (x.dataset.i===li.dataset.a) x.classList.add('right'); else if (x===b) x.classList.add('wrong'); }});
        var w=li.querySelector('.qwhy'); w.hidden=false; w.insertAdjacentHTML('afterbegin', ok?'<b>Right.</b> ':'<b>Not quite.</b> ');
        out.textContent = n===items.length ? ('You read '+s+' of '+items.length+' like a stonecutter.') : (s+' of '+n+' so far.'); }}); }}); }}); }})();
    </script>
'''
page('guide/gravestones/index.html','How do I read an old gravestone? · Project Scroll','How to read old gravestones: carved symbols, ages and abbreviations, what the stone is made of, how far to trust it, and how to read a worn stone without harming it.',body,og='https://projectscroll.com/og/death-certificate.jpg')
print('stones built')
