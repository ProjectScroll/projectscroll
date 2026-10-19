// Draws the home page's share card: NODE_PATH=$(npm root -g) node tools/og_home.js  -> /og-dark.png (1200x630)
// Draft 66: lighter iron-gall blue (matches the site's map background), hero copy and the three promises included.
const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
const R=path.resolve(__dirname,'..'); const F=f=>'file://'+path.join(R,'fonts',f); const I=f=>'file://'+path.join(R,'img',f);
const CARDS=[
 {out:'og-dark.png', pic:'heron-dawn.jpg', k:'A history hunt from the St. Joseph River Valley', h:'Every clue is true.', star:true,
  d:'Project Scroll is an online history hunt. Real mysteries hide in <u>county histories</u>, <u>survey maps</u>, <u>certificates</u>, <u>forgotten newspapers</u> and <u>legends</u>. Every one of them can be solved by you.',
  c:['Free to play','Solved with clues','Open to anyone, anywhere'], a:'<i>*</i> And every answer is in the record.', f:'projectscroll.com <span></span> Cassopolis, Michigan'},
 {out:'og/hunt.png', pic:'pack-train.jpg', k:'The hunt · ten open cases', h:'Pick a case. Open the record.', hs:66, star:false,
  d:'Ten mysteries from one Michigan county, each begun as a single question. The clues are real pages: <u>county histories</u>, <u>plat maps</u>, <u>certificates</u> and <u>old newspapers</u>. Crack one and the keepsake is yours.',
  c:['Free to play','Start with any case','Badges as you go'], a:'Every clue is true. Every answer is in the record.', f:'projectscroll.com/hunt <span></span> Cassopolis, Michigan'},
 {out:'og/services.png', pic:'death-register.jpg', k:'Professional services · now taking commissions', h:'Research, done properly.', hs:66, star:false,
  d:'Lost ancestors, family histories, legends tested against the record, forgotten places and land. Every source cited, every statement marked, and what we could not find written down beside what we could.',
  c:['Honest first read','You own the report','Nothing published without your word'], a:'Serving the St. Joseph River Valley and anywhere the records reach.', f:'projectscroll.com/services <span></span> Cassopolis, Michigan'},
 {out:'og/studio.png', pic:'wall-map-1860.jpg', k:'The studio · imaging, design, 3D and film', h:'Imaging, 3D and film.', hs:66, star:false,
  d:'Digital imaging of photographs, documents, maps and heirlooms; analysis of faded ink and damaged pages; graphic design, photography and video; landscapes rebuilt in three dimensions from LiDAR; living documents.',
  c:['Digital imaging','3D LiDAR and animation','Design, photo and video'], a:'The same desk that runs the hunt, hired for your project.', f:'projectscroll.com/studio <span></span> Cassopolis, Michigan'},
 {out:'og/document.png', pic:'pages/rogers-1875-p253-1200.jpg', k:'Document of the month · October 2026', h:'One page, read slowly.', hs:66,
  d:'Page 253 of Rogers’s 1875 <u>History of Cass County</u>: the first printing of the joke lodge of 1846, told to the historian by a man who was three years old when it happened.',
  c:['Free to read online','How to read it','The opening clue of Case 1'], a:'Every clue is true. Every answer is in the record.', f:'projectscroll.com/document <span></span> Cassopolis, Michigan'},
];
(async()=>{const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1200,height:630}});
for (const C of CARDS){
const tmp=path.join(require('os').tmpdir(),'ps-og-home.html'); fs.writeFileSync(tmp,`<html><head><style>
@font-face{font-family:D;src:url(${F('libre-caslon-display-latin-400-normal.woff2')})}
@font-face{font-family:T;src:url(${F('libre-caslon-text-latin-400-normal.woff2')})}
html,body{margin:0;width:1200px;height:630px;overflow:hidden}
body{background:#22364A url(${I('bg-new-france-blue.jpg')}) center/cover;color:#EAE6DC;font-family:T,serif;display:flex;position:relative}
body::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(34,54,74,.94) 0 48%,rgba(34,54,74,.78) 64%,rgba(34,54,74,.35))}
.gold{position:absolute;left:0;right:0;top:0;height:6px;background:linear-gradient(90deg,#8f6a1f,#b8892b 30%,#e6c46a 50%,#b8892b 70%,#8f6a1f)}
.gold.b{top:auto;bottom:0;height:3px;opacity:.7}
.dia{position:absolute;left:50%;top:6px;width:14px;height:14px;transform:translate(-50%,-50%) rotate(45deg);background:linear-gradient(135deg,#e6c46a,#8f6a1f);box-shadow:0 0 0 3px #22364A}
.t{position:relative;flex:none;width:720px;box-sizing:border-box;padding:54px 10px 44px 84px;display:flex;flex-direction:column}
.brand{display:flex;align-items:center;gap:13px;font-family:D;font-size:32px;color:#F4F1EA}
.brand svg{width:32px;height:32px}
.k{margin-top:40px;font-size:17px;letter-spacing:.14em;white-space:nowrap;text-transform:uppercase;color:#e6c46a}
.k b{font-weight:400;color:#c8cfd6}
.h{font-family:D;font-size:${C.hs||84}px;line-height:1.02;margin:10px 0 18px;color:#FFFDF7}
.h i{font-style:normal;color:#f08a7c;font-size:.45em;vertical-align:.9em;margin-left:4px}
.d{font-size:${C.hs?22:24}px;line-height:1.38;color:#DCE2E8;max-width:620px}
.d u{text-decoration:none;color:#F4F1EA;border-bottom:1.5px solid rgba(230,196,106,.75);padding-bottom:1px}
.c{margin-top:22px;display:flex;flex-wrap:wrap;gap:8px 22px;font-size:18px;color:#F4F1EA;white-space:nowrap}
.c span::before{content:"✓";color:#e6c46a;margin-right:8px}
.a{margin-top:18px;font-size:22px;color:#DCE2E8}.a i{font-style:normal;color:#f08a7c}
.f{margin-top:auto;display:flex;align-items:center;gap:12px;font-size:16px;letter-spacing:.12em;white-space:nowrap;text-transform:uppercase;color:#e6c46a}
.f span{display:inline-block;width:8px;height:8px;transform:rotate(45deg);background:#e6c46a}
.pic{position:relative;flex:1;margin:40px 40px 40px 0;background:url(${I(C.pic)}) center 50%/cover;border:1px solid rgba(230,196,106,.6);box-shadow:0 30px 60px -28px #000}
</style></head><body><div class="gold"></div><div class="gold b"></div><div class="dia"></div><div class="t">
<div class="brand"><svg viewBox="0 0 32 32"><rect x="7" y="4" width="18" height="24" rx="2" fill="none" stroke="#F4F1EA" stroke-width="2"/><path d="M11 4v24" stroke="#e6c46a" stroke-width="2"/><path d="M14 11h7M14 15h7M14 19h5" stroke="#F4F1EA" stroke-width="1.6"/></svg>Project Scroll</div>
<div class="k">${C.k}</div>
<div class="h">${C.h}${C.star?"<i>*</i>":""}</div>
<div class="d">${C.d}</div>
<div class="c">${C.c.map(x=>"<span>"+x+"</span>").join("")}</div>
<div class="a">${C.a}</div>
<div class="f">${C.f}</div>
</div><div class="pic"></div></body></html>`);
await p.goto('file://'+tmp); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
await p.screenshot({path:path.join(R,C.out),type:'png'}); await p.screenshot({path:path.join(R,C.out.replace(/\.png$/,'.jpg')),type:'jpeg',quality:86}); console.log(C.out,'drawn (png + jpg)'); }
await b.close();})();
