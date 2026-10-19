// Draws a 1200x630 share card for every case:  NODE_PATH=$(npm root -g) node tools/cards.js
const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
const R=path.resolve(__dirname,'..'); const C=JSON.parse(fs.readFileSync(path.join(R,'tools/cards.json'),'utf8'));
const F=f=>'file://'+path.join(R,'fonts',f);
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
(async()=>{const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1200,height:630}});
for (const c of C){
 const q=c.question, size=q.length>95?48:q.length>70?54:60;
 const tmp=path.join(require('os').tmpdir(),'ps-card.html'); fs.writeFileSync(tmp,`<html><head><style>
 @font-face{font-family:D;src:url(${F('libre-caslon-display-latin-400-normal.woff2')})}
 @font-face{font-family:T;src:url(${F('libre-caslon-text-latin-400-normal.woff2')})}
 html,body{margin:0;width:1200px;height:630px;overflow:hidden}
 body{background:#E8ECE6;color:#1D2733;font-family:T,serif;display:flex;position:relative}
 .rule{position:absolute;left:58px;top:0;bottom:0;border-left:3px solid #B3362B;opacity:.85}
 .t{flex:1;padding:64px 56px 52px 104px;display:flex;flex-direction:column}
 .k{font-size:22px;letter-spacing:.14em;text-transform:uppercase;color:#B3362B}
 .n{font-family:D;font-size:120px;line-height:.9;color:#B3362B;margin:10px 0 6px}
 .q{font-family:D;font-size:${size}px;line-height:1.12;margin:0 0 auto}
 .f{display:flex;justify-content:space-between;align-items:flex-end;border-top:1.5px solid #B9C2B8;padding-top:16px;font-size:22px;color:#4B5663}
 .f b{font-family:D;font-weight:400;font-size:30px;color:#1D2733}
 .st{display:inline-block;font-size:18px;letter-spacing:.1em;text-transform:uppercase;border:2px solid ${c.solved?'#2B4A41':'#B3362B'};color:${c.solved?'#fff':'#B3362B'};background:${c.solved?'#2B4A41':'transparent'};border-radius:20px;padding:2px 14px;margin-left:14px;vertical-align:middle}
 .pic{width:300px;background:url(file://${path.join(R,'img/heron-dawn.png')}) center 55%/cover;border-left:1px solid #B9C2B8}
 </style></head><body><div class="rule"></div><div class="t">
 <div class="k">${esc(c.hallName.split(' · ')[0])}<span class="st">${c.solved?'Solved':'Open'}</span></div>
 <div class="n">Case ${c.n}</div><div class="q">${esc(q)}</div>
 <div class="f"><span><b>Project Scroll</b> · Every clue is true.</span><span>projectscroll.com</span></div></div><div class="pic"></div></body></html>`); await p.goto('file://'+tmp);
 await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300); fs.mkdirSync(path.join(R,'cases',String(c.n)),{recursive:true});
 await p.screenshot({path:path.join(R,'cases',String(c.n),'card.png')}); }
await b.close(); console.log('cards drawn',C.length);})();
