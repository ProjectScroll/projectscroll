"""Find Your People: the record finder (three questions, an answer list of records and where they are kept) and the people tools in one place.
python3 _tools/build_people.py"""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page

# county seats: where the county's own books are kept (clerk, probate court, register of deeds / recorder)
COUNTIES = [
  ('cass-mi','Cass County, Michigan','Cassopolis','MI'), ('berrien-mi','Berrien County, Michigan','St. Joseph','MI'),
  ('vanburen-mi','Van Buren County, Michigan','Paw Paw','MI'), ('stjoseph-mi','St. Joseph County, Michigan','Centreville','MI'),
  ('kalamazoo-mi','Kalamazoo County, Michigan','Kalamazoo','MI'), ('stjoseph-in','St. Joseph County, Indiana','South Bend','IN'),
  ('elkhart-in','Elkhart County, Indiana','Goshen','IN'), ('lagrange-in','LaGrange County, Indiana','LaGrange','IN'),
  ('laporte-in','LaPorte County, Indiana','La Porte','IN'), ('other','Somewhere else','','')]
opts = ''.join(f'<option value="{k}">{n}</option>' for k, n, s, st in COUNTIES)
seats = json.dumps({k: [n, s, st] for k, n, s, st in COUNTIES}, ensure_ascii=False)

JS = r'''<script>
(function(){ "use strict";
  var SEAT=__SEATS__;
  var $=function(s){ return document.querySelector(s); };
  var f=$('#rfForm'), out=$('#rfOut'), list=$('#rfList'), head=$('#rfHead');
  /* each suggestion: what, why, where (link), and when it applies */
  var S=[
    {id:'names', w:['live','any'], t:'Who was in town', d:'Our own index of names from the old directories and rolls of the valley’s towns. Start here: one search, every list at once.', u:function(n){ return '/names/'+(n?'?q='+encodeURIComponent(n):''); }, on:'site', era:[0,1,2,3]},
    {id:'census', w:['live','birth','any'], t:'The federal census', d:'Every ten years from 1790, a list of households. From 1850 every person is named, with age and birthplace; 1880 adds each person’s relation to the head and their parents’ birthplaces. Most of the 1890 census is lost. Free on FamilySearch.', u:function(){ return 'https://www.familysearch.org/search/collection/list?keywords=census'; }, era:[0,1,2,3], st:['MI','IN','']},
    {id:'mi-vital', w:['birth','marriage','death'], t:'Michigan county birth, marriage and death registers', d:'Michigan counties began keeping registers of births and deaths in 1867, and marriage returns from the same year. The county clerk holds the originals; many are filmed and indexed on FamilySearch.', u:function(){ return 'https://www.familysearch.org/en/wiki/Michigan_Vital_Records'; }, era:[1,2,3], st:['MI']},
    {id:'mi-death', w:['death'], t:'Michigan death certificates, 1897–1952', d:'The state’s death certificates, with cause of death, parents’ names and the burial place. Free to search and view on Michiganology.', u:function(){ return 'https://michiganology.org/'; }, era:[2,3], st:['MI']},
    {id:'in-vital', w:['birth','death'], t:'Indiana state birth and death records', d:'Indiana’s state death certificates begin in 1899 and its state birth records in 1907; before that, the county health office kept them. The FamilySearch wiki gives what survives for each county.', u:function(){ return 'https://www.familysearch.org/en/wiki/Indiana_Vital_Records'; }, era:[2,3], st:['IN']},
    {id:'in-marr', w:['marriage'], t:'Indiana county marriage books', d:'Indiana’s county clerks kept marriage records from each county’s founding. Many are indexed and filmed on FamilySearch.', u:function(){ return 'https://www.familysearch.org/en/wiki/Indiana_Vital_Records'; }, era:[0,1,2,3], st:['IN']},
    {id:'church', w:['birth','marriage','death'], t:'Church records', d:'Before the counties kept registers, baptisms, marriages and burials were written by the church. Find the denomination, then ask the congregation or its archive.', u:function(){ return 'https://www.familysearch.org/en/wiki/Church_Records'; }, era:[0,1]},
    {id:'stone', w:['death'], t:'The gravestone', d:'A stone can give dates, a maiden name, a regiment or a family lot. Our guide shows how to read a weathered one.', u:function(){ return '/guide/gravestones/'; }, on:'site', era:[0,1,2,3]},
    {id:'dcguide', w:['death'], t:'Reading a death certificate', d:'What each box means, and which answers to trust: the informant knew some things and guessed others.', u:function(){ return '/guide/death-certificate/'; }, on:'site', era:[2,3]},
    {id:'probate', w:['death','land','family'], t:'Probate and wills', d:'When someone died owning property, the probate court opened a file: the will, the heirs, sometimes every child named and where they lived. Kept by the county probate court.', u:function(){ return 'https://www.familysearch.org/en/wiki/United_States_Probate_Records'; }, era:[0,1,2,3], seat:'probate court'},
    {id:'land', w:['land','live'], t:'Land: the first sale and the deeds after', d:'The first sale of each piece of federal land is a land patent, free to search at the Bureau of Land Management. Every later sale is a deed, kept by the county register of deeds (Michigan) or recorder (Indiana).', u:function(){ return 'https://glorecords.blm.gov/'; }, era:[0,1,2], seat:'register of deeds or recorder'},
    {id:'plats', w:['land','live'], t:'Plat maps and atlases', d:'County atlases and plat books put the family’s name on the farm. Many are in our map room; the University of Michigan holds the county histories and atlases in full text.', u:function(){ return '/map/'; }, on:'site', era:[1,2,3]},
    {id:'soldiers', w:['military'], t:'Soldiers of the valley', d:'Our roll of Company D, Sixth Michigan Infantry, and the valley’s other soldiers, each with the record behind the name.', u:function(){ return '/soldiers/'; }, on:'site', era:[1,2]},
    {id:'nara', w:['military'], t:'Service and pension files', d:'The National Archives holds army service records and the pension files of soldiers and widows, which are often the richest family records there are.', u:function(){ return 'https://www.archives.gov/research/genealogy'; }, era:[0,1,2,3]},
    {id:'papers', w:['story','death','marriage','any'], t:'The old newspapers', d:'Obituaries, marriages, visits, accidents and the weekly town news. Free on Chronicling America, Michigan Digital Newspapers and Hoosier State Chronicles.', u:function(n,st){ return st==='IN'? 'https://newspapers.library.in.gov/' : 'https://digmichnews.cmich.edu/'; }, era:[1,2,3]},
    {id:'paper-month', w:['story'], t:'Newspaper of the month', d:'One old front page of the valley each month, read for you, with the names on it.', u:function(){ return '/newspaper/'; }, on:'site', era:[1,2]},
    {id:'histories', w:['story','family','any'], t:'The county histories', d:'The 1870s and 1880s county histories have biographies of hundreds of early families, often with the family’s own account of where they came from.', u:function(){ return 'https://quod.lib.umich.edu/m/micounty/'; }, era:[0,1,2], st:['MI']},
    {id:'histories-in', w:['story','family','any'], t:'The county histories', d:'Indiana’s county histories carry family biographies too; the INGenWeb county sites transcribe many.', u:function(){ return 'http://www.ingenweb.org/'; }, era:[0,1,2], st:['IN']},
    {id:'families', w:['family'], t:'Families of the valley', d:'Family histories we have written up, with their sources.', u:function(){ return '/families/'; }, on:'site', era:[0,1,2,3]},
    {id:'origin', w:['origin'], t:'Where they came from', d:'The census birthplace column, then the county history biography, then naturalization papers. For a family from abroad, follow the records page’s list for that country.', u:function(){ return '/records/#beyond-the-united-states'; }, on:'site', era:[0,1,2,3]},
    {id:'natz', w:['origin'], t:'Naturalization and passenger lists', d:'Papers filed in the county court or later federal courts, and the ships’ lists of arrivals. The National Archives explains which exists for which years.', u:function(){ return 'https://www.archives.gov/research/naturalization'; }, era:[1,2,3]},
    {id:'hand', w:['any','birth','marriage','death','land'], t:'Reading old handwriting', d:'The letters that trip everyone up, the long s, and the abbreviations clerks used.', u:function(){ return '/guide/old-handwriting/'; }, on:'site', era:[0,1,2]},
    {id:'wiki', w:['any','birth','marriage','death','land','military','live','family','origin','story'], t:'The FamilySearch Research Wiki for the county', d:'What records exist for the county, which years survive, and where they are kept.', u:function(n,st,c){ return 'https://www.familysearch.org/en/wiki/'+(c? encodeURIComponent(c.replace(/ /g,'_')+'_Genealogy').replace(/%2C/g,',') : 'Main_Page'); }, era:[0,1,2,3]}
  ];
  var ERA=['before 1850','1850 to 1880','1880 to 1920','after 1920'];
  f.addEventListener('submit', function(e){ e.preventDefault();
    var name=$('#rfName').value.trim(), c=$('#rfCounty').value, era=+$('#rfEra').value, want=$('#rfWant').value;
    var seat=SEAT[c]||['','',''], st=seat[2], county=seat[0].replace(', Michigan','').replace(', Indiana','');
    var ok=S.filter(function(s){ return (s.w.indexOf(want)>=0) && s.era.indexOf(era)>=0 && (!s.st || s.st.indexOf(st)>=0 || (!st && s.st.indexOf('')>=0)); });
    if (st) ok=ok.filter(function(s){ return !s.st || s.st.indexOf(st)>=0; });
    ok.sort(function(a,b){ return (b.on==='site')-(a.on==='site'); });
    if (name){ var place=st? county+', '+(st==='MI'?'Michigan':'Indiana') : '';
      ok.splice(ok.filter(function(s){ return s.on==='site'; }).length, 0, {t:'Search FamilySearch for '+name+(place?' in '+place:''), d:'The free FamilySearch index, searched for this surname'+(place?' anywhere in the county':'')+'. A free account is needed to see the records.', u:function(){ return 'https://www.familysearch.org/search/record/results?q.surname='+encodeURIComponent(name)+(place?'&q.anyPlace='+encodeURIComponent(place):''); }}); }
    list.innerHTML='';
    ok.forEach(function(s,i){ var li=document.createElement('li'), a=document.createElement('a'); a.href=s.u(name,st,st? county+', '+(st==='MI'?'Michigan':'Indiana') : '');
      if (!s.on) a.rel='noopener'; var b=document.createElement('b'); b.textContent=s.t; a.appendChild(b); li.appendChild(a);
      if (s.on==='site'){ var k=document.createElement('span'); k.className='rf-here'; k.textContent='on this site'; li.appendChild(k); }
      var p=document.createElement('p'); p.textContent=s.d+(s.seat && seat[1]? ' In '+county+', ask the '+s.seat+' at '+seat[1]+'.' : ''); li.appendChild(p); list.appendChild(li); });
    var where=seat[1]? ' The county’s own books are kept at the courthouse and county offices in '+seat[1]+'.' : '';
    head.textContent=(name? 'For '+name+', ' : 'For your person, ')+ERA[era]+(seat[0]&&c!=='other'? ', in '+seat[0] : '')+': '+ok.length+' places to look, best first.'+where;
    out.hidden=false; out.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth', block:'start'}); head.focus({preventScroll:true});
    try{ localStorage.setItem('ps-rf', JSON.stringify({c:c, era:era, want:want})); }catch(e){}
    history.replaceState(null,'','?'+new URLSearchParams({c:c, e:era, w:want}).toString()+'#rfOut'); });
  /* share the list: the link carries the answers, so it opens with the same list */
  $('#rfShare').addEventListener('click',function(){ var m=$('#rfShareMsg'), qs=new URLSearchParams(location.search), nm=$('#rfName').value.trim(); if (nm) qs.set('n',nm); var url=location.origin+location.pathname+'?'+qs.toString();
    if (navigator.share){ navigator.share({title:'Where to look', text:head.textContent, url:url}).catch(function(){}); return; }
    if (navigator.clipboard) navigator.clipboard.writeText(url).then(function(){ m.textContent='Link copied.'; },function(){ m.textContent=url; }); else m.textContent=url; });
  $('#rfPrint').addEventListener('click',function(){ window.print(); });
  var sp=new URLSearchParams(location.search);
  if (sp.get('c') && SEAT[sp.get('c')]){ $('#rfCounty').value=sp.get('c'); $('#rfEra').value=String(Math.max(0,Math.min(3,+sp.get('e')||0))); var wv=sp.get('w'); if ([].some.call($('#rfWant').options,function(o){ return o.value===wv; })) $('#rfWant').value=wv; $('#rfName').value=(sp.get('n')||'').slice(0,40);
    setTimeout(function(){ f.requestSubmit ? f.requestSubmit() : f.dispatchEvent(new Event('submit')); },60); }
  try{ var p=JSON.parse(localStorage.getItem('ps-rf')||'null'); if (p && !location.search){ $('#rfCounty').value=p.c; $('#rfEra').value=p.era; $('#rfWant').value=p.want; } }catch(e){}
})();
</script>'''.replace('__SEATS__', seats)

TOOLS = [('/names/','Who was in town','Names from the old directories and rolls of the valley’s towns, searched all at once.'),
         ('/soldiers/','Soldiers of the valley','Company D, Sixth Michigan Infantry, and the valley’s other soldiers.'),
         ('/families/','Families','Family histories from the valley, with their sources.'),
         ('/records/','Where the records are','The free sources we search first, at home and abroad.'),
         ('/sources/','The sources shelf','The books and maps this site is built from.'),
         ('/guide/old-handwriting/','Reading old handwriting','The long s, the clerks’ shorthand, and the letters that fool everyone.'),
         ('/guide/death-certificate/','Reading a death certificate','What each box means and which answers to trust.'),
         ('/guide/gravestones/','Reading old gravestones','Dates, symbols and the stones that are hard to read.'),
         ('/museums/','Research rooms near you','Libraries, archives and societies in the museums directory: filter by “Help for researchers”.')]
tools = ''.join(f'<li class="pp-t"><a href="{u}"><b>{t}</b><span>{d}</span></a></li>' for u, t, d in TOOLS)

body = f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Find your people</p>
    <figure class="pg-art"><picture><source type="image/avif" srcset="/img/card-people-art-270.avif 270w, /img/card-people-art.avif 540w" sizes="8rem"><img class="vt-people" src="/img/card-people-art-270.webp" srcset="/img/card-people-art-270.webp 270w, /img/card-people-art.webp 540w" sizes="8rem" width="540" height="960" alt="" decoding="async"></picture></figure>
    <h1>Who were they, and where is it written?</h1>
    <p class="lede" style="font-size:1.15rem">Everyone who lived in the valley left a trail of paper: a census line, a deed, a notice in the weekly paper, a name on a stone. Answer three questions and the record finder lists where to look first, on this site and in the free collections, and which county office keeps the books.</p>
    <form class="rf" id="rfForm" aria-labelledby="rfH">
      <h2 id="rfH">The record finder</h2>
      <label><span>Their surname <small>(optional, for the name search)</small></span><input id="rfName" type="text" autocomplete="off" spellcheck="false" placeholder="For example, Smith"></label>
      <label><span>Where did they live?</span><select id="rfCounty">{opts}</select></label>
      <label><span>About when?</span><select id="rfEra"><option value="0">Before 1850</option><option value="1" selected>1850 to 1880</option><option value="2">1880 to 1920</option><option value="3">After 1920</option></select></label>
      <label><span>What do you want to find?</span><select id="rfWant"><option value="any">Anything at all</option><option value="live">Where they lived</option><option value="birth">A birth</option><option value="marriage">A marriage</option><option value="death">A death or burial</option><option value="military">A soldier</option><option value="land">Their land</option><option value="family">Their family and heirs</option><option value="origin">Where they came from</option><option value="story">Their story in the papers</option></select></label>
      <p><button class="btn primary" type="submit">Show me where to look</button></p>
    </form>
    <section class="rf-out" id="rfOut" hidden aria-live="polite"><h2 id="rfHead" tabindex="-1"></h2><ol class="rf-list" id="rfList"></ol>
      <p class="mu-tacts"><button type="button" class="btn" id="rfShare">Share this list</button> <button type="button" class="btn" id="rfPrint">Print it</button> <span class="mu-nmsg" id="rfShareMsg" aria-live="polite"></span></p>
      <p class="note">Nothing you type is sent anywhere unless you share the link yourself; a shared link carries your three answers and the surname, if you typed one. The page’s own address never holds the surname. The list is a starting order, not a guarantee: records were lost, burned or never kept in some places and years. The <a href="/records/">records page</a> has the rest.</p></section>
    <h2>The people tools</h2>
    <ul class="pp-tools">{tools}</ul>
    <h2>Three habits that find more</h2>
    <ul class="dis">
      <li><b>Spell it every way.</b> Clerks wrote what they heard. Try the name as it sounds.</li>
      <li><b>Read the neighbours.</b> The families on either side in a census are often in-laws; the witnesses to a deed are often kin.</li>
      <li><b>Go back to the original.</b> An index finds the record. The record itself is the evidence.</li>
    </ul>
    <p class="note">Found someone who belongs on this site? <a href="/#contact">Tell us</a>, with the record that shows it.</p>
{JS}
'''
page('people/index.html', 'Find your people · The record finder · Project Scroll',
     'Answer three questions and the record finder lists where to look for a person in the St. Joseph River valley: census, vital records, deeds, probate, soldiers and the old newspapers, and which county office keeps the books.',
     body, og='https://projectscroll.com/og/records.jpg')
print('people built')
