// Draws the home page's share card: NODE_PATH=$(npm root -g) node tools/og_home.js  -> /og-dark.png (1200x630)
// Draft 66: lighter iron-gall blue (matches the site's map background), hero copy and the three promises included.
const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
const R=path.resolve(__dirname,'..'); const F=f=>'file://'+path.join(R,'fonts',f); const I=f=>'file://'+path.join(R,'img',f);
(async()=>{const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1200,height:630}});
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
.h{font-family:D;font-size:84px;line-height:1;margin:10px 0 20px;color:#FFFDF7;white-space:nowrap}
.h i{font-style:normal;color:#f08a7c;font-size:.45em;vertical-align:.9em;margin-left:4px}
.d{font-size:24px;line-height:1.38;color:#DCE2E8;max-width:620px}
.d u{text-decoration:none;color:#F4F1EA;border-bottom:1.5px solid rgba(230,196,106,.75);padding-bottom:1px}
.c{margin-top:26px;display:flex;gap:24px;font-size:18px;color:#F4F1EA;white-space:nowrap}
.c span::before{content:"✓";color:#e6c46a;margin-right:8px}
.a{margin-top:18px;font-size:22px;color:#DCE2E8}.a i{font-style:normal;color:#f08a7c}
.f{margin-top:auto;display:flex;align-items:center;gap:14px;font-size:18px;letter-spacing:.16em;white-space:nowrap;text-transform:uppercase;color:#e6c46a}
.f span{display:inline-block;width:8px;height:8px;transform:rotate(45deg);background:#e6c46a}
.pic{position:relative;flex:1;margin:40px 40px 40px 0;background:url(${I('heron-dawn.jpg')}) center 50%/cover;border:1px solid rgba(230,196,106,.6);box-shadow:0 30px 60px -28px #000}
</style></head><body><div class="gold"></div><div class="gold b"></div><div class="dia"></div><div class="t">
<div class="brand"><svg viewBox="0 0 32 32"><rect x="7" y="4" width="18" height="24" rx="2" fill="none" stroke="#F4F1EA" stroke-width="2"/><path d="M11 4v24" stroke="#e6c46a" stroke-width="2"/><path d="M14 11h7M14 15h7M14 19h5" stroke="#F4F1EA" stroke-width="1.6"/></svg>Project Scroll</div>
<div class="k">A history hunt from the St. Joseph River Valley</div>
<div class="h">Every clue is true.<i>*</i></div>
<div class="d">Project Scroll is a history hunt played online. Real mysteries hide in <u>county histories</u>, <u>survey maps</u>, <u>certificates</u>, <u>forgotten newspapers</u> and <u>legends</u>. Every one of them can be solved by you.</div>
<div class="c"><span>Free to play</span><span>Solved with clues</span><span>Open to anyone, anywhere</span></div>
<div class="a"><i>*</i> And every answer is in the record.</div>
<div class="f">projectscroll.com <span></span> Cassopolis, Michigan</div>
</div><div class="pic"></div></body></html>`);
await p.goto('file://'+tmp); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
await p.screenshot({path:path.join(R,'og-dark.png'),type:'png'}); await b.close(); console.log('og-dark.png drawn');})();
