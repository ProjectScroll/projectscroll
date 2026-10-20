// Draws a 1200x630 share card for each main page into /og/:  NODE_PATH=$(npm root -g) node tools/og_pages.js
const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
const R=path.resolve(__dirname,'..'); const F=f=>'file://'+path.join(R,'fonts',f); const I=f=>'file://'+path.join(R,'img',f);
const CARDS=[
 ['map','The map room','The 1860 wall map','Every farm, town plan and engraved house of three Michigan counties.',I('cass1860.webp'),'center 40%'],
 ['cassopolis','Then and now','Cassopolis, 1860 and today','The old town plan laid over today’s streets.',I('cass1860.webp'),'center 62%'],
 ['niles','Then and now','Niles, 1860 and today','The 1860 city plan laid over today’s streets.','file://'+path.join(R,'img/towns/niles1860.webp'),'center 55%'],
 ['dowagiac','Then and now','Dowagiac, 1860 and today','The 1860 town plan laid over today’s streets.','file://'+path.join(R,'img/towns/dowagiac1860.webp'),'center 40%'],
 ['pawpaw','Then and now','Paw Paw, 1860 and today','The 1860 town plan laid over today’s streets.','file://'+path.join(R,'img/towns/pawpaw1860.webp'),'center'],
 ['south-bend','Then and now','South Bend, 1863 and today','The Stokes plan laid over today’s streets, and two renamed streets to find.','file://'+path.join(R,'_tools/towns/ogsrc/sb.jpg'),'center'],
 ['goshen','Then and now','Goshen, 1861 and today','The county-seat plan laid over today’s streets, and two renamed streets to find.','file://'+path.join(R,'_tools/towns/ogsrc/go.jpg'),'center'],
 ['elkhart','Then and now','Elkhart, 1861 and today','The town on the point between two rivers, laid over today’s streets.','file://'+path.join(R,'_tools/towns/ogsrc/el.jpg'),'center'],
 ['then-and-now','Then and now','Seven towns, then and now','Seven old town plans laid over today’s streets, and twelve renamed streets to find.','file://'+path.join(R,'_tools/towns/ogsrc/go.jpg'),'center 40%'],
 ['families','Research services','Family histories, built to be checked','Registers, monographs and family books, every statement marked.',I('two-certificates.jpg'),'center'],
 ['legends','Mysteries in the family','Is the family story true?','Ellis Island, the famous ancestor, the three brothers: tested against the records.',I('doctors-window.jpg'),'center'],
 ['toolkit','The hunter’s toolkit','Tools for reading the record','Faded ink, ages at death, Soundex codes and cousins.',I('two-certificates.jpg'),'30% center'],
 ['death-certificate','A guide from the desk','How to read a death certificate','Who filled in each box, and how far to trust it.',I('two-certificates.jpg'),'center'],
 ['handwriting','A guide from the desk','Reading the old hand','The long s, ye, inst. and ult., double dates and more.',I('two-certificates.jpg'),'70% center'],
 ['notes','From the desk','Field notes','Short lessons from real cases.',I('heron-dawn.png'),'center 55%'],
 ['one-letter','Field notes · No. 1','One Letter, Two Certificates','Two death certificates disagree on a middle initial. Which to trust?',I('two-certificates.jpg'),'center'],
 ['book','Bound in leather','The book of field notes','Every lesson from the desk, in a book whose pages turn.',I('heron-dawn.png'),'center 55%'],
 ['records','From the desk','Where the records are','The free archives, newspapers and maps we search first.',I('doctors-window.jpg'),'center'],
 ['glossary','Plain English','The glossary','The words old records use, explained.',I('two-certificates.jpg'),'center'],
 ['about','About','Project Scroll','A history hunt anyone can play, and a research desk anyone can hire.',I('heron-dawn.png'),'center 55%'],
];
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
(async()=>{const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1200,height:630}});
for (const [slug,k,t,d,pic,pos] of CARDS){
 const size=t.length>34?62:t.length>24?72:84;
 const tmp=path.join(require('os').tmpdir(),'ps-og.html'); fs.writeFileSync(tmp,`<html><head><style>
 @font-face{font-family:D;src:url(${F('libre-caslon-display-latin-400-normal.woff2')})}
 @font-face{font-family:T;src:url(${F('libre-caslon-text-latin-400-normal.woff2')})}
 html,body{margin:0;width:1200px;height:630px;overflow:hidden}
 body{background:#E8ECE6;color:#1D2733;font-family:T,serif;display:flex;position:relative}
 .rule{position:absolute;left:58px;top:0;bottom:0;border-left:3px solid #B3362B;opacity:.85}
 .t{flex:1;padding:70px 52px 52px 104px;display:flex;flex-direction:column}
 .k{font-size:22px;letter-spacing:.14em;text-transform:uppercase;color:#B3362B}
 .h{font-family:D;font-size:${size}px;line-height:1.04;margin:22px 0 18px}
 .d{font-size:28px;line-height:1.35;color:#4B5663;margin:0 0 auto}
 .f{display:flex;justify-content:space-between;align-items:flex-end;border-top:1.5px solid #B9C2B8;padding-top:16px;font-size:22px;color:#4B5663}
 .f b{font-family:D;font-weight:400;font-size:30px;color:#1D2733}
 .pic{width:400px;background:url(${pic}) ${pos}/cover;border-left:1px solid #B9C2B8}
 </style></head><body><div class="rule"></div><div class="t"><div class="k">${esc(k)}</div><div class="h">${esc(t)}</div><div class="d">${esc(d)}</div>
 <div class="f"><span><b>Project Scroll</b> · Every clue is true.</span><span>projectscroll.com</span></div></div><div class="pic"></div></body></html>`);
 await p.goto('file://'+tmp); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(250);
 await p.screenshot({path:path.join(R,'og',slug+'.jpg'),type:'jpeg',quality:86}); }
await b.close(); console.log('share cards drawn',CARDS.length);})();
