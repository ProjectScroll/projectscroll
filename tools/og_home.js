// Draws the home page's dark share card: NODE_PATH=$(npm root -g) node tools/og_home.js  -> /og-dark.png (1200x630)
const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
const R=path.resolve(__dirname,'..'); const F=f=>'file://'+path.join(R,'fonts',f); const I=f=>'file://'+path.join(R,'img',f);
(async()=>{const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1200,height:630}});
const tmp=path.join(require('os').tmpdir(),'ps-og-home.html'); fs.writeFileSync(tmp,`<html><head><style>
@font-face{font-family:D;src:url(${F('libre-caslon-display-latin-400-normal.woff2')})}
@font-face{font-family:T;src:url(${F('libre-caslon-text-latin-400-normal.woff2')})}
html,body{margin:0;width:1200px;height:630px;overflow:hidden}
body{background:#151B21 url(${I('bg-new-france-blue.jpg')}) center/cover;color:#EAE6DC;font-family:T,serif;display:flex;position:relative}
body::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(21,27,33,.96) 0 46%,rgba(21,27,33,.72) 66%,rgba(21,27,33,.25))}
.gold{position:absolute;left:0;right:0;top:0;height:5px;background:linear-gradient(90deg,#8f6a1f,#b8892b 30%,#e6c46a 50%,#b8892b 70%,#8f6a1f)}
.dia{position:absolute;left:50%;top:5px;width:14px;height:14px;transform:translate(-50%,-50%) rotate(45deg);background:linear-gradient(135deg,#e6c46a,#8f6a1f);box-shadow:0 0 0 3px #151B21}
.t{position:relative;flex:1;padding:66px 40px 48px 96px;display:flex;flex-direction:column}
.brand{display:flex;align-items:center;gap:14px;font-family:D;font-size:34px;color:#EAE6DC}
.brand svg{width:34px;height:34px}
.k{margin-top:auto;font-size:19px;letter-spacing:.14em;white-space:nowrap;text-transform:uppercase;color:#d4ab4f}
.h{font-family:D;font-size:104px;line-height:1.02;margin:14px 0 18px;color:#F4F1EA}
.h i{font-style:normal;color:#e26a5c;font-size:.45em;vertical-align:.9em;margin-left:4px}
.d{font-size:30px;line-height:1.3;color:#C8CFD6}
.d i{font-style:normal;color:#e26a5c}
.f{margin-top:34px;display:flex;align-items:center;gap:16px;font-size:20px;letter-spacing:.16em;white-space:nowrap;text-transform:uppercase;color:#d4ab4f}
.f span{display:inline-block;width:9px;height:9px;transform:rotate(45deg);background:#d4ab4f}
.pic{position:relative;width:430px;margin:36px 36px 36px 0;background:url(${I('heron-dawn.jpg')}) center 50%/cover;border:1px solid rgba(230,196,106,.55);box-shadow:0 30px 60px -30px #000}
</style></head><body><div class="gold"></div><div class="dia"></div><div class="t">
<div class="brand"><svg viewBox="0 0 32 32"><rect x="7" y="4" width="18" height="24" rx="2" fill="none" stroke="#EAE6DC" stroke-width="2"/><path d="M11 4v24" stroke="#d4ab4f" stroke-width="2"/><path d="M14 11h7M14 15h7M14 19h5" stroke="#EAE6DC" stroke-width="1.6"/></svg>Project Scroll</div>
<div class="k">A history hunt from the St. Joseph River Valley</div>
<div class="h">Every clue<br>is true.<i>*</i></div>
<div class="d"><i>*</i> And every answer is in the record.</div>
<div class="f">projectscroll.com <span></span> Cassopolis, Michigan</div>
</div><div class="pic"></div></body></html>`);
await p.goto('file://'+tmp); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
await p.screenshot({path:path.join(R,'og-dark.png'),type:'png'}); await b.close(); console.log('og-dark.png drawn');})();
