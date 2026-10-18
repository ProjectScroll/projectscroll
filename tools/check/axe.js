const BASE=process.env.BASE||'https://projectscroll.com';
const { chromium } = require('playwright'); const fs=require('fs');
const axe=fs.readFileSync(require('path').join(process.env.NODE_PATH,'axe-core/axe.min.js'),'utf8');
(async()=>{const b=await chromium.launch();
for (const [u,cs] of [['/','light'],['/','dark'],['/notes/one-letter-two-certificates/','light'],['/notes/one-letter-two-certificates/','dark'],['/404.html','light'],['/cases/4/','light'],['/guide/death-certificate/','light'],['/guide/death-certificate/','dark'],['/map/','light'],['/keepsake/?case=3','light'],['/toolkit/','light'],['/toolkit/','dark'],['/guide/old-handwriting/','light'],['/notes/book/','light'],['/notebook/','light']]){
 const q=await b.newPage({viewport:{width:1280,height:900},colorScheme:cs,reducedMotion:'reduce'}); await q.goto(BASE+u); await q.waitForTimeout(800);
 await q.addScriptTag({content:axe}); const r=await q.evaluate(async()=>await axe.run(document,{runOnly:['wcag2a','wcag2aa','best-practice']}));
 console.log('==',u,cs,'violations:',r.violations.length);
 for (const v of r.violations){ console.log(' -',v.id,v.impact,v.nodes.length,'|',v.nodes.slice(0,4).map(n=>n.target.join(' ')+' :: '+(n.any[0]?.message||'').slice(0,110)).join(' || ')); } await q.close();}
await b.close();})();
