// Draws a 1200x630 share card for every news story, from its picture:  NODE_PATH=$(npm root -g) node _tools/news_cards.js
const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs'); const os=require('os');
const R=path.resolve(__dirname,'..'); const N=JSON.parse(fs.readFileSync(path.join(R,'_tools/data/news.json'),'utf8'));
const F=f=>'file://'+path.join(R,'fonts',f); const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
const items=N.stories.map(s=>({dir:'news/'+s.slug, k:s.kicker, h:s.headline, d:(s.sdek||s.dek), pos:(s.cardpos||'center'), img:path.join(R,s.pic[0].replace(/^\//,'')+'.webp')}));
items.push({dir:'hunt', k:'The hunt · Free to play', h:'Every clue is true.', img:path.join(R,'img/news/lead-hunt.webp'), tall:true, d:'Project Scroll now has a new, free online treasure hunt. Real mysteries hide in county histories, maps and old newspapers, and every answer is in the record.'});
(async()=>{const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1200,height:630}});
for (const c of items){ const size=c.h.length>52?50:c.h.length>34?58:68;
 const tmp=path.join(os.tmpdir(),'ps-ncard.html'); fs.writeFileSync(tmp,`<html><head><style>
 @font-face{font-family:D;src:url(${F('libre-caslon-display-latin-400-normal.woff2')})}
 @font-face{font-family:T;src:url(${F('libre-caslon-text-latin-400-normal.woff2')})}
 html,body{margin:0;width:1200px;height:630px;overflow:hidden}
 body{background:#fff;color:#1D2733;font-family:T,serif;display:flex}
 .pic{width:${c.tall?380:600}px;background:#1D2733 url('file://${c.img}') ${c.pos||'center'}/cover}
 .t{flex:1;padding:44px 52px 40px 48px;display:flex;flex-direction:column;border-left:6px solid #B8892B}
 .bar{display:flex;justify-content:space-between;border-top:4px double #1D2733;border-bottom:1px solid #C9CFC6;padding:8px 0;font-size:17px;letter-spacing:.18em;text-transform:uppercase;color:#4B5663}
 .k{margin:30px 0 10px;font-size:20px;letter-spacing:.16em;text-transform:uppercase;color:#B3362B}
 .h{font-family:D;font-size:${size}px;line-height:1.08;margin:0 0 18px}
 .d{font-size:22px;line-height:1.4;color:#4B5663;margin:0 0 auto;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
 .f{border-top:1.5px solid #C9CFC6;padding-top:14px;display:flex;justify-content:space-between;align-items:baseline;font-size:19px;color:#4B5663;white-space:nowrap}
 .f b{font-family:D;font-weight:400;font-size:28px;color:#1D2733}
 </style></head><body><div class="pic"></div><div class="t"><div class="bar"><span>Front page</span><span>News of the hunt</span></div>
 <div class="k">${esc(c.k)}</div><div class="h">${esc(c.h)}</div><div class="d">${esc(c.d)}</div><div class="f"><span><b>Project Scroll</b> · Every clue is true.</span><span>projectscroll.com</span></div></div></body></html>`);
 await p.goto('file://'+tmp); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(250);
 fs.mkdirSync(path.join(R,c.dir),{recursive:true}); await p.screenshot({path:path.join(R,c.dir,'card.jpg'),type:'jpeg',quality:86}); }
await b.close(); console.log('news cards drawn', items.length);})();
