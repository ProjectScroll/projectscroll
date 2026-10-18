const BASE=process.env.BASE||'https://projectscroll.com';
const { chromium } = require('playwright');
const R=[]; const ok=(n,c,d='')=>R.push((c?'PASS ':'FAIL ')+n+(d?' — '+d:''));
(async()=>{const b=await chromium.launch();
for (const [w,cs,label] of [[1280,'light','computer/light'],[1280,'dark','computer/dark'],[390,'light','phone/light'],[390,'dark','phone/dark']]){
 const ctx=await b.newContext({viewport:{width:w,height:850},colorScheme:cs,permissions:['clipboard-read','clipboard-write']}); const q=await ctx.newPage();
 const errs=[]; q.on('pageerror',e=>errs.push(e.message)); q.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 const bad=[]; q.on('response',r=>{ if(r.url().includes('localhost') && r.status()>=400) bad.push(r.status()+' '+r.url()); });
 await q.goto(''+BASE+'/'); await q.waitForTimeout(700);
 const P=label+': ';
 // theme
 const bg=()=>q.evaluate(()=>getComputedStyle(document.body).backgroundColor);
 const b0=await bg(); await q.click('#theme'); await q.waitForTimeout(500); const b1=await bg();
 ok(P+'Light/Dark switches colors', b0!==b1, b0+' → '+b1);
 await q.reload(); await q.waitForTimeout(500); ok(P+'Light/Dark choice remembered after reload', (await bg())===b1);
 await q.click('#theme'); await q.waitForTimeout(500); ok(P+'Light/Dark switches back', (await bg())===b0);
 // overflow
 const sw=await q.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]); ok(P+'no sideways scrolling', sw[0]<=sw[1], sw.join('/'));
 // menu or nav
 if (w<880){ await q.click('#menu'); await q.waitForTimeout(200); const open=await q.evaluate(()=>getComputedStyle(document.querySelector('.bar nav')).display!=='none'); ok(P+'phone Menu opens',open);
   await q.click('.bar nav a[href="#cases"]'); await q.waitForTimeout(700); const closed=await q.evaluate(()=>!document.querySelector('.bar').classList.contains('open')); ok(P+'Menu closes after choosing a section',closed); }
 else { const tg=await q.evaluate(()=>[...document.querySelectorAll('.bar nav a')].every(a=>document.querySelector(a.getAttribute('href')))); ok(P+'every top-bar link has a section',tg); }
 // all anchor targets
 const missing=await q.evaluate(()=>[...document.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href')).filter(h=>h.length>1&&!document.querySelector(h))); ok(P+'every on-page link points somewhere', missing.length===0, missing.join(' '));
 const dup=await q.evaluate(()=>{const s={},d=[];document.querySelectorAll('[id]').forEach(e=>{if(s[e.id])d.push(e.id);s[e.id]=1});return d}); ok(P+'no duplicate ids', dup.length===0, dup.join(' '));
 // footnote
 await q.click('#star'); await q.waitForTimeout(300); ok(P+'asterisk lights its footnote', await q.evaluate(()=>document.getElementById('foot').classList.contains('lit')));
 // popovers
 await q.click('button[popovertarget="s2"]'); await q.waitForTimeout(300); const po=await q.evaluate(()=>document.getElementById('s2').matches(':popover-open')); ok(P+'source card opens',po);
 if(po){ await q.click('#s2 .close'); await q.waitForTimeout(300); ok(P+'source card closes', !(await q.evaluate(()=>document.getElementById('s2').matches(':popover-open')))); }
 // case board
 await q.click('.filters [data-f="h1"]'); let vis=await q.evaluate(()=>[...document.querySelectorAll('tr[id^=case-]')].filter(r=>!r.hidden).length); ok(P+'filter: first hall shows 2 cases',vis===2,String(vis));
 await q.click('.filters [data-f="h2"]'); vis=await q.evaluate(()=>[...document.querySelectorAll('tr[id^=case-]')].filter(r=>!r.hidden).length); ok(P+'filter: second hall shows 7',vis===7,String(vis));
 await q.click('.filters [data-f="desk"]'); vis=await q.evaluate(()=>[...document.querySelectorAll('tr[id^=case-]')].filter(r=>!r.hidden).length); ok(P+'filter: from the desk shows 1',vis===1,String(vis));
 await q.click('.filters [data-f="all"]');
 await q.click('#case-4 .follow'); await q.click('.filters [data-f="mine"]'); vis=await q.evaluate(()=>[...document.querySelectorAll('tr[id^=case-]')].filter(r=>!r.hidden).map(r=>r.id)); ok(P+'follow a case → My cases',vis.join()==='case-4',vis.join());
 await q.click('#case-4 .follow'); await q.click('.filters [data-f="all"]');
 await q.click('#case-4 .link'); await q.waitForTimeout(200); ok(P+'copy link to a case', /copied/i.test(await q.textContent('#caseCopied')));
 // quiz
 for (let i=1;i<=5;i++) await q.click(`#quiz .qlist > li:nth-child(${i}) .qopts .mk >> nth=1`);
 ok(P+'quiz scores all five', /of 5/.test(await q.textContent('#qscore')), await q.textContent('#qscore'));
 await q.click('#qreset'); ok(P+'quiz Try again resets', (await q.textContent('#qscore')).trim()==='');
 // timeline
 const tl0=await q.evaluate(()=>document.getElementById('tl').scrollLeft);
 if (w>=640){ await q.click('.tl-nav.next'); await q.waitForTimeout(700); } else { await q.evaluate(()=>document.getElementById('tl').scrollBy(300,0)); await q.waitForTimeout(300); }
 ok(P+'timeline moves', (await q.evaluate(()=>document.getElementById('tl').scrollLeft))>tl0);
 // try it
 await q.click('.card[data-pick="a"]'); ok(P+'two-record puzzle answers', (await q.textContent('#verdict')).length>20);
 // faq
 await q.click('#faqall'); ok(P+'open all answers', await q.evaluate(()=>[...document.querySelectorAll('details.faq')].every(d=>d.open)));
 // form
 await q.fill('[name=names]','Test Name'); await q.click('#copy'); await q.waitForTimeout(300);
 ok(P+'message form copies', /Copied/.test(await q.textContent('#copied')) && (await q.evaluate(()=>navigator.clipboard.readText())).includes('Test Name'), await q.textContent('#copied'));
 await q.click('#clearmsg'); ok(P+'message form clears', (await q.inputValue('[name=names]'))==='');
 // back to top
 await q.evaluate(()=>scrollTo(0,document.body.scrollHeight)); await q.waitForTimeout(400); ok(P+'back-to-top button appears', await q.evaluate(()=>!document.querySelector('.totop').hidden));
 // images
 await q.evaluate(()=>document.querySelectorAll('img').forEach(i=>i.loading='eager')); await q.waitForTimeout(900);
 const imgs=await q.evaluate(()=>[...document.querySelectorAll('img')].map(i=>(i.currentSrc||i.src).split('/').pop()+':'+i.naturalWidth)); ok(P+'all pictures load', imgs.every(s=>!s.endsWith(':0')), imgs.join(' '));
 ok(P+'no script errors', errs.length===0, errs.join(' | ')); ok(P+'no missing files', bad.length===0, bad.join(' '));
 await ctx.close(); }
// inner pages & files
const q=await b.newPage(); const urls=['/','/notes/','/notes/one-letter-two-certificates/','/404.html','/sample/project-scroll-sample-report.pdf','/worksheet/project-scroll-hunters-worksheet.pdf','/og.png','/favicon.svg','/robots.txt','/sitemap.xml','/site.css?v=29','/site.js?v=29','/img/heron-dawn.png','/img/doctors-window.jpg','/img/two-certificates.jpg','/img/heron-dawn.webp','/sw.js','/favicon.ico','/site.webmanifest','/feed.xml','/icons/icon-32.png','/icons/apple-touch-icon.png','/icons/icon-192.png','/icons/icon-512.png','/icons/icon-maskable-512.png'];
for (const u of urls){ const r=await q.request.get(BASE+u); ok('file '+u, r.status()===200, String(r.status())); }
for (const u of ['/notes/','/notes/one-letter-two-certificates/','/404.html']){ const p=await b.newPage(); const e=[]; p.on('pageerror',x=>e.push(x.message)); await p.goto(BASE+u); await p.waitForTimeout(400);
  const b0=await p.evaluate(()=>getComputedStyle(document.body).backgroundColor); await p.click('#theme'); await p.waitForTimeout(400); const b1=await p.evaluate(()=>getComputedStyle(document.body).backgroundColor);
  const links=await p.evaluate(()=>[...document.querySelectorAll('a[href^="/"]')].map(a=>a.getAttribute('href').split('#')[0]));
  let badl=[]; for (const l of [...new Set(links)]){ const r=await p.request.get(BASE+l); if(r.status()!==200) badl.push(l); }
  ok('page '+u+' Light/Dark works', b0!==b1); ok('page '+u+' links all work', badl.length===0, badl.join(' ')); ok('page '+u+' no script errors', e.length===0, e.join('|')); await p.close(); }
const fails=R.filter(r=>r.startsWith('FAIL')); console.log(R.join('\n')); console.log('\nTOTAL',R.length,'checks,',fails.length,'failed');
await b.close();})();
