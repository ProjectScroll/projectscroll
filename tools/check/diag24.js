const BASE=process.env.BASE||'https://projectscroll.com';
const { chromium } = require('playwright');
const R=[]; const ok=(n,c,d='')=>R.push((c?'PASS ':'FAIL ')+n+(d?' — '+d:''));
(async()=>{const b=await chromium.launch();
for (const [w,cs,lab] of [[1280,'light','computer'],[390,'dark','phone']]){
 const ctx=await b.newContext({viewport:{width:w,height:850},colorScheme:cs,permissions:['clipboard-read','clipboard-write'],hasTouch:w<500}); const q=await ctx.newPage();
 const errs=[]; q.on('pageerror',e=>errs.push(e.message)); const P=lab+': ';
 await q.goto(''+BASE+'/'); await q.waitForTimeout(400);
 ok(P+'ink: headline writes itself on first visit', await q.evaluate(()=>document.documentElement.classList.contains('ink')));
 await q.reload(); await q.waitForTimeout(400); ok(P+'ink: not repeated on the next visit', !(await q.evaluate(()=>document.documentElement.classList.contains('ink'))));
 ok(P+'reveal: sections start hidden below the fold', await q.evaluate(()=>document.documentElement.classList.contains('reveal') && !document.getElementById('faq').classList.contains('in')));
 await q.evaluate(()=>document.getElementById('faq').scrollIntoView()); await q.waitForTimeout(900); ok(P+'reveal: a section appears when scrolled to', await q.evaluate(()=>document.getElementById('faq').classList.contains('in')));
 // clue rotation
 ok(P+'clue of the week matches today (18 Oct → 17 Oct clue)', /17 October/.test(await q.textContent('#clueLbl')));
 // checker
 for (const i of [1,2,3,4]) await q.click(`#checker .ck li:nth-child(${i}) button[data-v="1"]`);
 ok(P+'checker: all yes → Very likely', /Very likely/.test(await q.textContent('#ckOut')));
 await q.click('#checker .ck li:nth-child(4) button[data-v="0"]'); ok(P+'checker: after 1950 → privacy note', /1950/.test(await q.textContent('#ckOut')));
 // scale
 await q.click('#weigh .side[data-side="L"] .kD'); await q.click('#weigh .side[data-side="R"] .kT'); await q.click('#weigh .side[data-side="R"] .kT'); await q.waitForTimeout(900);
 const tr=await q.evaluate(()=>document.getElementById('beam').style.transform); ok(P+'scale tips toward the document', /rotate\(-/.test(tr), tr);
 ok(P+'scale explains "even with fewer records"', /fewer records/.test(await q.textContent('#weighOut')));
 await q.click('#weighReset'); ok(P+'scale empties', /level/.test(await q.textContent('#weighOut')));
 // timeline filter
 await q.click('.tl-filters [data-m="kT"]'); const vis=await q.evaluate(()=>[...document.querySelectorAll('#tl > li')].filter(l=>!l.hidden).length); ok(P+'timeline filter: Traditions shows 1 date + Now', vis===2, String(vis));
 await q.click('.tl-filters [data-m="all"]');
 // faq search
 await q.fill('#faqq','michigan'); let n=await q.evaluate(()=>[...document.querySelectorAll('details.faq')].filter(d=>!d.hidden).length); ok(P+'question search: "michigan" finds matches', n>=1 && n<7, String(n));
 await q.fill('#faqq','zzzz'); ok(P+'question search: no match shows a note', await q.evaluate(()=>!document.getElementById('faqnone').hidden));
 await q.fill('#faqq',''); n=await q.evaluate(()=>[...document.querySelectorAll('details.faq')].filter(d=>!d.hidden).length); ok(P+'question search: clearing shows all', n===12, String(n));
 // messenger
 await q.fill('[name=names]','Test'); await q.click('#copy'); await q.waitForTimeout(300); ok(P+'after copying, the Open Messenger button appears', await q.evaluate(()=>!document.getElementById('openMsgr').hidden));
 // magnifier
 const fig=q.locator('#lensFig img'); await fig.scrollIntoViewIfNeeded(); const bx=await fig.boundingBox();
 if (w>500){ await q.mouse.move(bx.x+bx.width/2,bx.y+bx.height/2); await q.mouse.move(bx.x+bx.width/2+10,bx.y+bx.height/2+5); await q.waitForTimeout(300);
   ok(P+'magnifying glass appears and shows the picture', await q.evaluate(()=>document.getElementById('lensFig').classList.contains('on') && /two-certificates/.test(document.querySelector('.lens').style.backgroundImage)));
   await q.screenshot({path:'D24_lens.png',clip:{x:bx.x-20,y:bx.y-20,width:bx.width+40,height:bx.height+60}}); }
 // sealed hall tooltip
 { const n=await q.evaluate(()=>[document.querySelectorAll('.trailmap .tm-hall').length, document.querySelectorAll('.trailmap .tm-sealed title').length]); ok(P+'trail map: 2 halls lit, the rest sealed with a note', n[0]===2 && n[1]===5, String(n)); }
 // meter + seals mechanism (simulated solved case + hint, then reload logic)
 ok(P+'meter reads 0 of 10', (await q.getAttribute('.meter','aria-label'))==='0 of 10 cases solved');
 errs.length===0 ? ok(P+'no script errors',true) : ok(P+'no script errors',false,errs.join('|'));
 await ctx.close(); }
// simulated solved case + hint on a copy of the page
const q=await b.newPage({viewport:{width:1280,height:900}}); await q.route('**/', async r=>{ const res=await r.fetch(); let t=await res.text(); t=t.replace('<tr id="case-3" data-hall="h2">','<tr id="case-3" data-hall="h2" data-solved="Jane Example" data-hint="Look for the deed in the county history’s chapter on the village.">'); r.fulfill({response:res,body:t,headers:{...res.headers(),'content-type':'text/html'}}); });
await q.goto(''+BASE+'/'); await q.waitForTimeout(1200);
ok('demo: solved case gets a wax seal', await q.evaluate(()=>document.querySelector('.seals a[href="#case-3"]').classList.contains('solved')));
ok('demo: status says Solved with the name', /Solved/.test(await q.textContent('#case-3 .status')) && /Jane Example/.test(await q.textContent('#case-3')));
ok('demo: meter and count update', (await q.getAttribute('.meter','aria-label'))==='1 of 10 cases solved' && (await q.textContent('.tally b >> nth=1'))==='1');
await q.click('#case-3 .hintbtn'); ok('demo: Hint button reveals the hint', await q.evaluate(()=>!document.querySelector('#case-3 .hint').hidden));
await q.addStyleTag({content:'.bar{position:static!important} html.reveal main > section > *{opacity:1!important;transform:none!important}'});
await q.evaluate(()=>document.getElementById('cases').scrollIntoView()); await q.waitForTimeout(700);
const cb=await q.locator('#cases').boundingBox(); await q.screenshot({path:'D24_cases_demo.png',clip:{x:cb.x,y:cb.y,width:cb.width,height:760}});
// offline
const ctx2=await b.newContext(); const p2=await ctx2.newPage(); await p2.goto(''+BASE+'/'); await p2.waitForTimeout(2500);
const sw=await p2.evaluate(async()=>{ const r=await navigator.serviceWorker.getRegistration(); return !!(r&&r.active); }); ok('offline: service worker installed', sw);
await ctx2.setOffline(true); let offOK=false; try{ await p2.reload({timeout:8000}); offOK=/Every clue is true/.test(await p2.textContent('h1')); }catch(e){} ok('offline: page still opens with no connection', offOK);
await ctx2.setOffline(false);
console.log(R.join('\n')); console.log('TOTAL',R.length,'checks,',R.filter(r=>r.startsWith('FAIL')).length,'failed'); await b.close();})();
