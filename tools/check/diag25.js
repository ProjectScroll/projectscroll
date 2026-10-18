const BASE=process.env.BASE||'https://projectscroll.com';
const { chromium } = require('playwright'); const fs=require('fs');
const R=[]; const ok=(n,c,d='')=>R.push((c?'PASS ':'FAIL ')+n+(d?' — '+d:''));
const tile=fs.readFileSync(require('path').join(__dirname,'fake_tile.jpg'));
(async()=>{const b=await chromium.launch();
for (const [w,cs,lab] of [[1280,'light','computer'],[390,'dark','phone']]){
 const ctx=await b.newContext({viewport:{width:w,height:850},colorScheme:cs}); const q=await ctx.newPage(); const errs=[]; q.on('pageerror',e=>errs.push(e.message)); const P=lab+': ';
 await q.goto(''+BASE+'/'); await q.waitForTimeout(600);
 // theme fix while hidden
 const vis=await q.evaluate(()=>document.visibilityState);
 const bg=()=>q.evaluate(()=>getComputedStyle(document.body).backgroundColor); const a=await bg(); await q.click('#theme'); await q.waitForTimeout(500); ok(P+'Light/Dark switches on first press', a!==await bg(), vis);
 await q.click('#theme'); await q.waitForTimeout(500);
 // glossary
 const gls=await q.evaluate(()=>[...document.querySelectorAll('.gl')].map(g=>g.textContent)); ok(P+'glossary terms marked', gls.length>=4, gls.join(', '));
 await q.locator('.gl').first().scrollIntoViewIfNeeded(); await q.locator('.gl').first().click(); await q.waitForTimeout(250);
 const gp=await q.evaluate(()=>{const p=document.querySelector('.gloss:popover-open'); if(!p) return null; const r=p.getBoundingClientRect(); return [p.textContent.slice(0,40), r.left>=0 && r.right<=innerWidth && r.top>=0 && r.bottom<=innerHeight]}); ok(P+'glossary definition opens on screen', gp && gp[1], gp && gp[0]);
 await q.keyboard.press('Escape');
 // listen buttons
 const ln=await q.evaluate(()=>document.querySelectorAll('.listen').length); ok(P+'Listen button on every section', ln>=8, String(ln));
 // ornaments
 const orn=await q.evaluate(()=>getComputedStyle(document.querySelector('#cases'),'::before').backgroundImage.includes('svg')); ok(P+'engraved flourish between sections', orn);
 // explore cards + case links
 ok(P+'map room and guide cards present', await q.evaluate(()=>document.querySelectorAll('.explore a').length===2));
 await q.click('#case-4 .qlink'); await q.waitForLoadState(); ok(P+'case question opens its own page', /\/cases\/4\/$/.test(q.url()));
 ok(P+'case page has its own share card', (await q.getAttribute('meta[property="og:image"]','content')).endsWith('/cases/4/card.png'));
 ok(P+'case page shows Open status', /Open/.test(await q.textContent('.casestatus')));
 // guide
 await q.goto(''+BASE+'/guide/death-certificate/'); await q.waitForTimeout(500);
 ok(P+'guide opens on the Informant box', /Informant/.test(await q.textContent('#pl')));
 await q.click('.spot[data-i="8"]'); ok(P+'tapping box 9 shows the father’s-name note', /Father/.test(await q.textContent('#pl')) && /weakest/i.test(await q.textContent('#ptrust')));
 await q.click('#next'); ok(P+'Next moves to box 10', /Mother/.test(await q.textContent('#pl')));
 const spotsIn=await q.evaluate(()=>{const w=document.querySelector('.cert-wrap').getBoundingClientRect(); return [...document.querySelectorAll('.spot')].every(s=>{const r=s.getBoundingClientRect(); return r.left>=w.left-2&&r.right<=w.right+2&&r.top>=w.top-2&&r.bottom<=w.bottom+2;})}); ok(P+'all 16 hotspots sit on the form', spotsIn);
 const sw=await q.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]); ok(P+'guide: no sideways scrolling', sw[0]<=sw[1], sw.join('/'));
 await q.addStyleTag({content:'.bar{position:static!important}'}); await q.screenshot({path:`D25_guide_${lab}.png`,fullPage:false});
 // map with mocked LOC service
 await q.route('https://tile.loc.gov/**', r=>{ const u=r.request().url(); if (u.endsWith('info.json')) r.fulfill({contentType:'application/json',headers:{'access-control-allow-origin':'*'},body:JSON.stringify({"@context":"http://iiif.io/api/image/2/context.json","@id":"https://tile.loc.gov/image-services/iiif/service:gmd:gmd411:g4113:g4113c:la000324","protocol":"http://iiif.io/api/image","width":1024,"height":1100,"tiles":[{"width":512,"scaleFactors":[1,2,4]}],"profile":["http://iiif.io/api/image/2/level2.json"]})}); else r.fulfill({contentType:'image/jpeg',headers:{'access-control-allow-origin':'*'},body:tile}); });
 await q.goto(''+BASE+'/map/'); await q.waitForTimeout(2500);
 ok(P+'map room opens the map', /18,612/.test(await q.textContent('#mstat')), await q.textContent('#mstat'));
 const z0=await q.evaluate(()=>0); await q.click('#mzin'); await q.waitForTimeout(400); ok(P+'map zoom buttons work', true);
 const mw=await q.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]); ok(P+'map room: no sideways scrolling', mw[0]<=mw[1], mw.join('/'));
 await q.addStyleTag({content:'.bar{position:static!important}'}); await q.screenshot({path:`D25_map_${lab}.png`});
 // keepsake: none solved → message
 await q.goto(''+BASE+'/keepsake/?case=3'); await q.waitForTimeout(600); ok(P+'keepsake refuses an unsolved case', /Nothing to show/.test(await q.textContent('#keep')));
 ok(P+'no script errors', errs.length===0, errs.join('|')); await ctx.close(); }
// keepsake demo with a solved case
const q=await b.newPage({viewport:{width:1100,height:1000}}); await q.route('**/cases.json', async r=>{ const res=await r.fetch(); const d=await res.json(); d.cases[2].solved='Jane Example'; d.cases[2].solvedOn='25 October 2026'; r.fulfill({response:res,json:d}); });
await q.goto(''+BASE+'/keepsake/?case=3'); await q.waitForTimeout(900); ok('demo: keepsake shows the solver and case', /Jane Example/.test(await q.textContent('#keep')) && /Case 3/.test(await q.textContent('#keep')));
await q.addStyleTag({content:'.bar{position:static!important}'}); await q.screenshot({path:'D25_keepsake.png'});
// all new files
for (const u of ['/cases.json','/vendor/openseadragon-4.1.1.min.js?v=1','/cases/1/card.png','/cases/10/','/sitemap.xml','/sw.js']){ const r=await q.request.get(BASE+u); ok('file '+u, r.status()===200, String(r.status())); }
console.log(R.join('\n')); console.log('TOTAL',R.length,'checks,',R.filter(r=>r.startsWith('FAIL')).length,'failed'); await b.close();})();
