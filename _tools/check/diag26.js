const BASE=process.env.BASE||'https://projectscroll.com';
const { chromium } = require('playwright'); const path=require('path');
const R=[]; const ok=(n,c,d='')=>R.push((c?'PASS ':'FAIL ')+n+(d?' — '+d:''));
(async()=>{const b=await chromium.launch();
for (const [w,cs,lab] of [[1280,'light','computer'],[390,'dark','phone']]){
 const ctx=await b.newContext({viewport:{width:w,height:850},colorScheme:cs,permissions:['clipboard-read','clipboard-write']}); const q=await ctx.newPage(); const errs=[]; q.on('pageerror',e=>errs.push(e.message)); q.on('console',m=>{if(m.type()==='error'&&!/favicon/.test(m.text()))errs.push(m.text())}); const P=lab+': ';
 // search
 await q.goto(BASE+'/'); await q.waitForTimeout(500);
 await q.click('#searchBtn'); await q.fill('#searchQ','soundex'); await q.waitForTimeout(700);
 let hits=await q.evaluate(()=>[...document.querySelectorAll('#searchRes a')].map(a=>a.getAttribute('href'))); ok(P+'search finds the toolkit for "soundex"', hits.includes('/toolkit/'), hits.join(' '));
 await q.fill('#searchQ','parchment deed'); await q.waitForTimeout(300); hits=await q.evaluate(()=>[...document.querySelectorAll('#searchRes a')].map(a=>a.getAttribute('href'))); ok(P+'search finds case 4 for "parchment deed"', hits[0]==='/cases/4/', hits.join(' '));
 await q.keyboard.press('Escape'); await q.keyboard.press('/'); ok(P+'"/" opens search', await q.evaluate(()=>document.getElementById('searchDlg').open)); await q.keyboard.press('Escape');
 // toolkit
 await q.goto(BASE+'/toolkit/'); await q.waitForTimeout(500);
 ok(P+'age calculator: 15 Mar 1912, 71y 4m 12d → 3 Nov 1840', /3 November 1840/.test(await q.textContent('#aOut')), await q.textContent('#aOut'));
 await q.fill('#sx','Robert'); ok(P+'Soundex: Robert → R163', /R163/.test(await q.textContent('#sxOut')));
 await q.fill('#sx','Ashcraft'); ok(P+'Soundex: Ashcraft → A261 (H/W rule)', /A261/.test(await q.textContent('#sxOut')));
 await q.fill('#sx','Tymczak'); ok(P+'Soundex: Tymczak → T522', /T522/.test(await q.textContent('#sxOut')));
 ok(P+'cousin: 3 and 4 → second cousins once removed', /2nd cousins once removed/.test(await q.textContent('#cOut')), await q.textContent('#cOut'));
 await q.selectOption('#cA','1'); await q.selectOption('#cB','3'); ok(P+'cousin: child and great-grandchild → great-aunt or uncle', /great-aunt or great-uncle/.test(await q.textContent('#cOut')), await q.textContent('#cOut'));
 await q.setInputFiles('#inkfile', path.join(__dirname,'..','..','img','two-certificates.jpg')); await q.waitForTimeout(800);
 await q.fill('#kC','80'); await q.dispatchEvent('#kC','input'); await q.fill('#kL','60'); await q.dispatchEvent('#kL','input'); await q.check('#kG'); await q.waitForTimeout(500);
 const px=await q.evaluate(()=>{const c=document.getElementById('inkc'); const d=c.getContext('2d').getImageData(c.width/2,c.height/2,1,1).data; return [c.width,c.height,d[0]===d[1]&&d[1]===d[2]]}); ok(P+'ink enhancer loads a photo and goes black and white', px[0]>0 && px[2], px.join(','));
 const [dl]=await Promise.all([q.waitForEvent('download'), q.click('#kSave')]); ok(P+'ink enhancer saves the clearer copy', /enhanced-two-certificates\.png/.test(dl.suggestedFilename()), dl.suggestedFilename());
 if (lab==='computer'){ await q.addStyleTag({content:'.bar{position:static!important}'}); await q.locator('#ink').screenshot({path:'D26_ink.png'}); }
 const sw=await q.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]); ok(P+'toolkit: no sideways scrolling', sw[0]<=sw[1], sw.join('/'));
 // handwriting
 await q.goto(BASE+'/guide/old-handwriting/'); await q.waitForTimeout(400);
 await q.click('.hquiz > li:nth-child(1) button[data-i="1"]'); ok(P+'handwriting quiz marks an answer', /Right/.test(await q.textContent('.hquiz > li:nth-child(1) .qwhy')));
 ok(P+'ten handwriting cards', await q.evaluate(()=>document.querySelectorAll('.hcard').length===10));
 // book
 await q.goto(BASE+'/notes/book/'); await q.waitForTimeout(500);
 ok(P+'book opens closed on its cover', /Cover/.test(await q.textContent('#bkAt')));
 await q.click('#bkNext'); await q.waitForTimeout(1000); await q.click('#bkNext'); await q.waitForTimeout(1000);
 ok(P+'book pages turn', /Pages 4–5/.test(await q.textContent('#bkAt')), await q.textContent('#bkAt'));
 if (lab==='computer'){ await q.addStyleTag({content:'.bar{position:static!important}'}); await q.locator('.book-wrap').screenshot({path:'D26_book.png'}); }
 await q.click('#bkPrev'); await q.waitForTimeout(900); ok(P+'book turns back', /Pages 2–3/.test(await q.textContent('#bkAt')));
 const bw=await q.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]); ok(P+'book: no sideways scrolling', bw[0]<=bw[1], bw.join('/'));
 // notebook
 await q.goto(BASE+'/cases/4/'); await q.waitForTimeout(400); await q.fill('#noteText','Checked the 1882 county history, p. 120: nothing yet.');
 await q.reload(); await q.waitForTimeout(400); ok(P+'case notebook keeps your note', /p\. 120/.test(await q.inputValue('#noteText')));
 await q.click('#noteCopy'); await q.waitForTimeout(300); if (lab==='computer') ok(P+'notebook copies a Facebook answer', /case 4/.test(await q.evaluate(()=>navigator.clipboard.readText())));
 await q.goto(BASE+'/notebook/'); await q.waitForTimeout(400); ok(P+'notebook page lists the note', /Case 4/.test(await q.textContent('#nbList')));
 ok(P+'no script errors', errs.length===0, errs.join(' | ')); await ctx.close(); }
for (const u of ['/search.json','/toolkit/toolkit.js?v=1','/notes/book/','/guide/old-handwriting/','/notebook/']){ const r=await (await b.newPage()).request.get(BASE+u); ok('file '+u, r.status()===200, String(r.status())); }
console.log(R.join('\n')); console.log('TOTAL',R.length,'checks,',R.filter(r=>r.startsWith('FAIL')).length,'failed'); await b.close();})();
