/* each feature below runs inside its own guard: if one ever fails, the rest of the page keeps working */
/* the full stylesheet arrives as a print sheet so it never blocks the first paint (the first screen is styled inline); it is switched on here */
try{ document.querySelectorAll('link[data-full]').forEach(function(l){ l.media='all'; }); }catch(e){}
function psFail(err){ try{ console.error('[Project Scroll]', err); }catch(e){} }
(function(){
  "use strict";
  let root=document.documentElement, btn=document.getElementById('theme');
  function themeNow(){ return root.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'); }
  const MOON='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/></svg>';
  const SUN='<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M12 2.5v2.4M12 19.1v2.4M2.5 12h2.4M19.1 12h2.4M5.3 5.3l1.7 1.7M17 17l1.7 1.7M5.3 18.7 7 17M17 7l1.7-1.7" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/></svg>';
  function label(){ if (!btn) return; const d=themeNow()==='dark'; btn.innerHTML = d ? SUN : MOON; btn.setAttribute('aria-label', d ? 'Switch to light' : 'Switch to dark'); btn.title = d ? 'Light pages' : 'Dark pages'; btn.setAttribute('aria-pressed', String(d)); }
  label();
  btn.addEventListener('click', function(){
    let next = themeNow()==='dark' ? 'light' : 'dark';
    let apply = function(){ root.dataset.theme=next; try{localStorage.setItem('ps-theme',next);}catch(e){} label(); };
    { const r=btn.getBoundingClientRect(); root.style.setProperty('--vx', Math.round(r.left+r.width/2)+'px'); root.style.setProperty('--vy', Math.round(r.top+r.height/2)+'px'); root.classList.add('theme-sweep'); setTimeout(function(){ root.classList.remove('theme-sweep'); }, 900); }
    if (document.startViewTransition && document.visibilityState==='visible' && !matchMedia('(prefers-reduced-motion: reduce)').matches){ let done=false; const go=function(){ if (!done){ done=true; apply(); } }; try{ const vt=document.startViewTransition(go); [vt.ready, vt.finished, vt.updateCallbackDone].forEach(function(pr){ if (pr && pr.catch) pr.catch(function(){}); }); }catch(e){ go(); } setTimeout(go, 350); } else apply();
  });

  /* mobile menu */
  let menu=document.getElementById('menu'), bar=document.querySelector('.bar');
  if (menu && bar){
    menu.addEventListener('click', function(){ let o=bar.classList.toggle('open'); menu.setAttribute('aria-expanded', o?'true':'false'); menu.textContent=o?'Close':'Menu'; });
    bar.querySelectorAll('nav a').forEach(function(a){ a.addEventListener('click', function(){ bar.classList.remove('open'); menu.setAttribute('aria-expanded','false'); menu.textContent='Menu'; }); });
    document.addEventListener('click', function(e){ if (bar.classList.contains('open') && !bar.contains(e.target)){ bar.classList.remove('open'); menu.setAttribute('aria-expanded','false'); menu.textContent='Menu'; } });
    document.addEventListener('keydown', function(e){ if (e.key==='Escape' && bar.classList.contains('open')){ bar.classList.remove('open'); menu.setAttribute('aria-expanded','false'); menu.textContent='Menu'; menu.focus(); } });
  }

  /* the top bar gains a soft shadow once the page has scrolled */
  if (bar){ let bq=0; const lift=function(){ bq=0; bar.classList.toggle('lifted', scrollY>12); }; addEventListener('scroll', function(){ if (!bq) bq=requestAnimationFrame(lift); }, {passive:true}); lift(); }

  /* the asterisk leads to its footnote */
  let star=document.getElementById('star'), foot=document.getElementById('foot');
  if (star && foot) star.addEventListener('click', function(){
    foot.scrollIntoView({block:'center'}); foot.classList.add('lit');
    setTimeout(function(){ foot.classList.remove('lit'); }, 1600);
  });


  /* the message builder: fill in, copy, paste into Facebook (kept only in this browser as a draft) */
  let form=document.getElementById('msgform');
  if (form){
    form.addEventListener('submit', function(e){ e.preventDefault(); });
    let DK='ps-msg', fields=[].slice.call(form.querySelectorAll('input,textarea,select')), out=document.getElementById('copied');
    try{ let d=JSON.parse(localStorage.getItem(DK)||'{}'); fields.forEach(function(f){ if (d[f.name]) f.value=d[f.name]; }); }catch(e){}
    let store=function(){ let d={}; fields.forEach(function(f){ d[f.name]=f.value; }); try{ localStorage.setItem(DK, JSON.stringify(d)); }catch(e){} };
    let text=function(){ let lines=fields.filter(function(f){ return f.value.trim(); }).map(function(f){ return f.closest('label').querySelector('span').textContent+': '+f.value.trim(); }); return 'Hello Project Scroll,\n\n'+lines.join('\n'); };
    let em=document.getElementById('emailIt');
    let mail=function(){ if (!em) return; let need=(form.need&&form.need.value)||'My mystery'; em.href='mailto:research@projectscroll.com?subject='+encodeURIComponent(need)+'&body='+encodeURIComponent(text()); };
    fields.forEach(function(f){ f.addEventListener('input', function(){ store(); mail(); }); f.addEventListener('change', function(){ store(); mail(); }); }); mail();
    document.getElementById('copy').addEventListener('click', function(){
      let txt=text();
      let done=function(){ const om=document.getElementById('openMsgr'); if (om) om.hidden=false; out.textContent='Copied. Now open Messenger and paste it.'; setTimeout(function(){ out.textContent=''; },5000); };
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, function(){ out.textContent='Your browser blocked copying. Select the text and copy it by hand.'; });
      else out.textContent='Your browser blocked copying. Select the text and copy it by hand.';
    });
    document.getElementById('clearmsg').addEventListener('click', function(){ fields.forEach(function(f){ f.value=''; }); store(); mail(); out.textContent='Cleared.'; setTimeout(function(){ out.textContent=''; },2000); });
  }

  /* the "try it yourself" record puzzle */
  let verdict=document.getElementById('verdict');
  let answers={
    a:"Good pick. Record A was filled in about a month after he died, by someone close to the event, so it usually weighs more. But it doesn't prove he had no initial: the next step is a third, independent record, such as his obituary or his gravestone.",
    b:"Worth a look, but careful. Record B was filled in twenty-three years later, by someone remembering a man long gone, and the son carried that same initial. Closer to the event usually weighs more, so look for a third record before you believe it."
  };
  document.querySelectorAll('.card').forEach(function(c){
    c.setAttribute('aria-pressed','false');
    c.addEventListener('click', function(){
      document.querySelectorAll('.card').forEach(function(o){ o.setAttribute('aria-pressed','false'); });
      c.setAttribute('aria-pressed','true'); verdict.textContent=answers[c.dataset.pick]; let tm=document.getElementById('trymore'); if (tm) tm.hidden=false;
    });
  });

  /* mark the section you are reading in the top bar */
  let links={}; document.querySelectorAll('.bar nav a').forEach(function(a){ let h=a.getAttribute('href'); if (h.charAt(0)==='#') links[h.slice(1)]=a; });
  if ('IntersectionObserver' in window){
    let io=new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting && links[e.target.id]){
          Object.values(links).forEach(function(l){ l.removeAttribute('aria-current'); });
          links[e.target.id].setAttribute('aria-current','true');
        }
      });
    }, {rootMargin:'-40% 0px -55% 0px'});
    document.querySelectorAll('main section[id]').forEach(function(s){ io.observe(s); });
  }

  /* ---------- case board: filters, follow, copy a link ---------- */
  let board=document.querySelector('table.ledger');
  if (board){
    let KEY='ps-mine', mine=[];
    try{ mine=JSON.parse(localStorage.getItem(KEY)||'[]'); }catch(e){ mine=[]; }
    let save=function(){ try{ localStorage.setItem(KEY, JSON.stringify(mine)); }catch(e){} };
    let rows=[].slice.call(board.querySelectorAll('tr[id^="case-"]')), groups=[].slice.call(board.querySelectorAll('tr.group'));
    let countEl=document.getElementById('minecount'), emptyEl=document.getElementById('mineEmpty'), boardFilter='all';
    function paint(){
      rows.forEach(function(r){
        let on=mine.indexOf(r.id)>-1, b=r.querySelector('.follow');
        b.setAttribute('aria-pressed', on?'true':'false'); b.textContent=on?'★':'☆'; b.title=on?'Following: tap to stop':'Follow this case';
        let seal=document.querySelector('.seals a[href="#'+r.id+'"]'); if (seal) seal.classList.toggle('mine', on);
      });
      if (countEl) countEl.textContent = mine.length ? '('+mine.length+')' : '';
    }
    function filter(f){
      boardFilter=f;
      rows.forEach(function(r){ r.hidden = !(f==='all' || r.dataset.hall===f || (f==='mine' && mine.indexOf(r.id)>-1)); });
      groups.forEach(function(g){ let any=rows.some(function(r){ return r.dataset.hall===g.dataset.hall && !r.hidden; }); g.hidden=!any; });
      if (emptyEl) emptyEl.hidden = !(f==='mine' && mine.length===0);
      document.querySelectorAll('.filters button[data-f]').forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.f===f?'true':'false'); });
    }
    document.querySelectorAll('.filters button[data-f]').forEach(function(b){ b.addEventListener('click', function(){ filter(b.dataset.f); }); });
    let note=document.getElementById('caseCopied');
    rows.forEach(function(r){
      r.querySelector('.follow').addEventListener('click', function(){
        let i=mine.indexOf(r.id); if (i>-1) mine.splice(i,1); else mine.push(r.id); save(); paint(); if (boardFilter==='mine') filter('mine');
      });
      r.querySelector('.link').addEventListener('click', function(){
        let url=location.origin+location.pathname+'#'+r.id;
        if (navigator.share && matchMedia('(pointer:coarse)').matches){ navigator.share({title:'Project Scroll · Case '+r.id.split('-')[1], text:r.children[1].firstChild.textContent.trim(), url:url}).catch(function(){}); return; }
        let done=function(){ note.textContent='Link to case '+r.id.split('-')[1]+' copied. Paste it anywhere to share.'; setTimeout(function(){ note.textContent=''; },3500); };
        if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, function(){ note.textContent=url; }); else note.textContent=url;
      });
    });
    paint();
  }

  /* ---------- marking quiz ---------- */
  let quiz=document.getElementById('quiz');
  if (quiz){
    let items=[].slice.call(quiz.querySelectorAll('.qlist > li')), score=0, done=0, out=document.getElementById('qscore'), rs=document.getElementById('qreset');
    if (rs) rs.addEventListener('click', function(){ score=0; done=0; out.textContent=''; rs.hidden=true;
      items.forEach(function(li){ delete li.dataset.done; li.querySelectorAll('.qopts .mk').forEach(function(x){ x.classList.remove('right','wrong','dim'); x.removeAttribute('aria-disabled'); }); let w=li.querySelector('.qwhy'); w.hidden=true; let b=w.querySelector('b'); if (b) b.remove(); }); });
    items.forEach(function(li){
      let opts=[].slice.call(li.querySelectorAll('.qopts .mk'));
      opts.forEach(function(o){
        o.addEventListener('click', function(){
          if (li.dataset.done) return; li.dataset.done='1'; done++;
          let ok=o.classList.contains(li.dataset.a); if (ok) score++;
          opts.forEach(function(x){ if (x.classList.contains(li.dataset.a)) x.classList.add('right'); else if (x===o) x.classList.add('wrong'); else x.classList.add('dim'); x.setAttribute('aria-disabled','true'); });
          let why=li.querySelector('.qwhy'); why.hidden=false; why.insertAdjacentHTML('afterbegin', ok?'<b>Right.</b> ':'<b>Not quite.</b> ');
          out.textContent = done===items.length ? ('You marked '+score+' of '+items.length+' the way we would.'+(score===items.length?' A born record-keeper.':'')) : (score+' of '+done+' so far.'); if (done===items.length && rs) rs.hidden=false;
        });
      });
    });
  }

  /* ---------- timeline arrows ---------- */
  let tl=document.getElementById('tl');
  if (tl){
    let step=function(d){ tl.scrollBy({left:d*tl.clientWidth*0.8, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'}); };
    let pv=document.querySelector('.tl-nav.prev'), nx=document.querySelector('.tl-nav.next');
    if (pv) pv.addEventListener('click', function(){ step(-1); });
    if (nx) nx.addEventListener('click', function(){ step(1); });
    tl.addEventListener('keydown', function(e){ if (e.key==='ArrowRight'){ step(1); e.preventDefault(); } if (e.key==='ArrowLeft'){ step(-1); e.preventDefault(); } });
  }

  /* timeline: tally, counts on the filters, the ribbon below, and soft edges */
  try{ (function(){
    const t=document.getElementById('tl'); if (!t) return;
    const all=[].slice.call(t.children), dated=all.filter(function(li){ return !li.classList.contains('now'); });
    const sealed=dated.filter(function(li){ return li.classList.contains('sealed'); }).length;
    const tally=document.getElementById('tlTally');
    if (tally){ const b=tally.querySelectorAll('b'); if (b.length===3){ b[0].textContent=dated.length; b[1].textContent=dated.length-sealed; b[2].textContent=sealed; } }
    document.querySelectorAll('.tl-filters button').forEach(function(btn){
      const m=btn.dataset.m, n= m==='all' ? dated.length : dated.filter(function(li){ return li.querySelector('.mk.'+m); }).length;
      const c=document.createElement('span'); c.className='n'; c.textContent=n; c.setAttribute('aria-hidden','true');
      btn.appendChild(document.createTextNode(' ')); btn.appendChild(c); btn.setAttribute('aria-label', btn.firstChild.textContent.trim()+', '+n+(n===1?' date':' dates'));
    });
    const rib=document.getElementById('tlRibbon'), rail=rib && rib.querySelector('.rail'), win=rail && rail.querySelector('.win');
    const smooth=function(){ return matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'; };
    const edges=function(){
      const max=t.scrollWidth-t.clientWidth;
      t.classList.toggle('fl', t.scrollLeft>4); t.classList.toggle('fr', t.scrollLeft<max-4);
      if (win){ const sw=t.scrollWidth||1; win.style.left=(t.scrollLeft/sw*100)+'%'; win.style.width=Math.min(100,t.clientWidth/sw*100)+'%'; }
    };
    const build=function(){
      if (!rail) return;
      rail.querySelectorAll('.tick').forEach(function(x){ x.remove(); });
      const vis=all.filter(function(li){ return !li.hidden; }), n=vis.length;
      vis.forEach(function(li,i){
        const k=document.createElement('b'); k.className='tick'+(li.classList.contains('sealed')?' s':'')+(li.classList.contains('now')?' now':'');
        const mk=li.querySelector('.mk'); if (mk && !li.classList.contains('sealed')) k.classList.add('t'+[].slice.call(mk.classList).filter(function(c){ return /^k[A-Z]$/.test(c); })[0]);
        k.style.left=((i+.5)/n*100)+'%'; k.title=li.querySelector('.yr').textContent; k.dataset.y=k.title;
        k.addEventListener('click', function(e){ e.stopPropagation(); t.scrollTo({left:Math.max(0,li.offsetLeft-8), behavior:smooth()}); });
        rail.appendChild(k);
      });
      edges();
    };
    if (rail){
      let drag=false;
      const seek=function(e){ const r=rail.getBoundingClientRect(), f=Math.min(1,Math.max(0,(e.clientX-r.left)/r.width)); t.scrollLeft=f*t.scrollWidth-t.clientWidth/2; };
      rail.addEventListener('pointerdown', function(e){ if (e.target.classList.contains('tick')) return; drag=true; rail.setPointerCapture(e.pointerId); seek(e); });
      rail.addEventListener('pointermove', function(e){ if (drag) seek(e); });
      rail.addEventListener('pointerup', function(){ drag=false; });
      rail.addEventListener('pointercancel', function(){ drag=false; });
    }
    let eq=0; const edgesSoon=function(){ if (!eq) eq=requestAnimationFrame(function(){ eq=0; edges(); }); };
    t.addEventListener('scroll', edgesSoon, {passive:true}); window.addEventListener('resize', edgesSoon, {passive:true});
    document.querySelectorAll('.tl-filters button').forEach(function(b){ b.addEventListener('click', function(){ setTimeout(build,0); }); });
    build();
  })(); }catch(err){ psFail(err); }

  /* questions: open all, and open the one a link points at */
  let fa=document.getElementById('faqall'), faqs=[].slice.call(document.querySelectorAll('details.faq'));
  if (fa){ fa.addEventListener('click', function(){ let openAll=faqs.some(function(d){ return !d.open; }); faqs.forEach(function(d){ d.open=openAll; }); fa.textContent=openAll?'Close all answers':'Open all answers'; }); }

  /* back-to-top button appears once you are well down the scroll */
  let tt=document.querySelector('.totop');
  if (tt){ let onS=function(){ tt.hidden = scrollY < innerHeight*1.5; }; addEventListener('scroll', onS, {passive:true}); onS(); }

  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1 the ink writes itself, on a visitor's first visit only */
  try{ if (!reduce && !localStorage.getItem('ps-inked')){ document.documentElement.classList.add('ink'); localStorage.setItem('ps-inked','1'); } }catch(e){}

  /* 2 sections arrive as you scroll */
  if (!reduce && 'IntersectionObserver' in window){
    const blocks=[].slice.call(document.querySelectorAll('main > section, main > .plate2'));
    document.documentElement.classList.add('reveal');
    const ro=new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('in'); ro.unobserve(e.target); } }); }, {rootMargin:'0px 0px -8% 0px'});
    blocks.forEach(function(b){ ro.observe(b); });
    if (location.hash) blocks.forEach(function(b){ b.classList.add('in'); });
    addEventListener('beforeprint', function(){ blocks.forEach(function(b){ b.classList.add('in'); }); });
  }

  /* 3 magnifying glass over the certificates picture */
  const fig=document.getElementById('lensFig');
  if (fig){
    const img=fig.querySelector('img'), lens=fig.querySelector('.lens'), Z=2.6;
    const move=function(x,y){ const r=img.getBoundingClientRect(); const lx=Math.max(0,Math.min(r.width,x-r.left)), ly=Math.max(0,Math.min(r.height,y-r.top));
      lens.style.left=(img.offsetLeft+lx)+'px'; lens.style.top=(img.offsetTop+ly)+'px';
      lens.style.backgroundImage='url("'+(img.currentSrc||img.src)+'")'; lens.style.backgroundSize=(r.width*Z)+'px '+(r.height*Z)+'px';
      lens.style.backgroundPosition=(-(lx*Z-75))+'px '+(-(ly*Z-75))+'px'; };
    fig.addEventListener('pointerenter', function(e){ if (e.pointerType==='mouse') fig.classList.add('on'); });
    fig.addEventListener('pointerleave', function(){ fig.classList.remove('on'); });
    fig.addEventListener('pointermove', function(e){ if (e.pointerType==='mouse' || fig.classList.contains('on')) move(e.clientX,e.clientY); });
    fig.addEventListener('pointerdown', function(e){ if (e.pointerType!=='mouse'){ fig.classList.add('on'); move(e.clientX,e.clientY); } });
    ['pointerup','pointercancel'].forEach(function(t){ fig.addEventListener(t, function(e){ if (e.pointerType!=='mouse') fig.classList.remove('on'); }); });
    fig.addEventListener('touchmove', function(e){ if (fig.classList.contains('on')){ e.preventDefault(); const t=e.touches[0]; move(t.clientX,t.clientY); } }, {passive:false});
  }

  /* 4 + 7 solved cases get wax seals; the meter fills; published hints get a Hint button */
  const rowsAll=[].slice.call(document.querySelectorAll('tr[id^="case-"]'));
  if (rowsAll.length){
    let solved=0;
    rowsAll.forEach(function(r){
      const st=r.querySelector('.status'), seal=document.querySelector('.seals a[href="#'+r.id+'"]');
      if (r.dataset.solved){ solved++; st.textContent='Solved'; st.classList.add('solved');
        const by=document.createElement('span'); by.className='by'; by.textContent='Cracked by '+r.dataset.solved; r.children[1].appendChild(by);
        if (seal){ seal.classList.add('solved'); seal.title='Case '+r.id.split('-')[1]+': solved by '+r.dataset.solved; } }
      if (r.dataset.hint){ const hb=document.createElement('button'); hb.type='button'; hb.className='hintbtn'; hb.textContent='Hint'; hb.setAttribute('aria-expanded','false');
        const h=document.createElement('span'); h.className='hint'; h.textContent=r.dataset.hint; h.hidden=true;
        hb.addEventListener('click', function(){ h.hidden=!h.hidden; hb.setAttribute('aria-expanded', h.hidden?'false':'true'); hb.textContent=h.hidden?'Hint':'Hide hint'; });
        r.children[1].appendChild(hb); r.children[1].appendChild(h); }
    });
    const total=rowsAll.length, m=document.querySelector('.meter');
    if (m){ m.setAttribute('aria-label', solved+' of '+total+' cases solved'); setTimeout(function(){ m.firstElementChild.style.width=(solved/total*100)+'%'; }, 300); }
    const tb=document.querySelectorAll('.tally b'); if (tb.length>1){ tb[0].textContent=total-solved; tb[1].textContent=solved; } if (solved>0){ const sp=document.querySelectorAll('.tally > span'); if (sp[2]) sp[2].textContent = solved===total ? 'Every case is cracked. New halls are coming.' : 'The hunt is on.'; }
  }

  /* 8 is my question answerable? */
  const ck=document.getElementById('checker');
  if (ck){
    const items=[].slice.call(ck.querySelectorAll('.ck li')), out=document.getElementById('ckOut');
    const verdict=function(a){
      const n=a.reduce(function(x,y){return x+y;},0);
      if (a[3]===0) return '<p><b>Possibly, with care.</b> Records after about 1950 are often closed for privacy, and we don’t locate living people. Older family members, newspapers and published sources can still help.</p>';
      if (n===4) return '<p><b>Very likely.</b> A name, a place and a rough date are exactly what the old records are indexed by. This is the kind of question we answer.</p>';
      if (n===3) return '<p><b>Likely.</b> One piece is missing, but the other three usually lead to it. Tell us what you have.</p>';
      if (n===2) return '<p><b>Worth a look.</b> It will take more digging, and we’ll tell you honestly in our first reply whether the records are likely to hold the answer.</p>';
      return '<p><b>Hard, but not hopeless.</b> Family papers, a photograph or a story can be the thread. Send what you have and we’ll say plainly what is possible.</p>';
    };
    const answers=[null,null,null,null];
    items.forEach(function(li,i){ li.querySelectorAll('button').forEach(function(b){ b.setAttribute('aria-pressed','false'); b.addEventListener('click', function(){
      li.querySelectorAll('button').forEach(function(x){ x.setAttribute('aria-pressed', x===b?'true':'false'); }); answers[i]=+b.dataset.v;
      if (answers.every(function(v){ return v!==null; })){ out.innerHTML=verdict(answers)+'<p><a class="btn primary" href="#contact">Bring us your mystery</a></p>'; out.hidden=false; }
    }); }); });
  }

  /* 9 weigh the evidence */
  const wg=document.getElementById('weigh');
  if (wg){
    const beam=document.getElementById('beam'), pl=document.getElementById('panL'), pr=document.getElementById('panR'), wo=document.getElementById('weighOut');
    const load={L:[],R:[]};
    const draw=function(){
      const sum=function(a){ return a.reduce(function(x,y){ return x+y.w; },0); }, L=sum(load.L), R=sum(load.R);
      const ang=Math.max(-16,Math.min(16,(R-L)*2.2));
      beam.style.transform='rotate('+ang+'deg)'; pl.style.transform='rotate('+(-ang)+'deg)'; pr.style.transform='rotate('+(-ang)+'deg)';
      wg.querySelectorAll('.side').forEach(function(sd){ const a=load[sd.dataset.side]; sd.querySelector('.pile').textContent = a.length ? a.map(function(x){ return x.n; }).join(' · ') : ''; });
      if (!load.L.length && !load.R.length) wo.textContent='The scale is level. Add a record to either side.';
      else if (L===R) wo.textContent='Balanced. Time to look for a third, independent record.';
      else { const heavy=L>R?'A':'B', many=(L>R?load.L:load.R).length < (L>R?load.R:load.L).length;
        wo.textContent='Side '+heavy+' weighs more'+(many?', even with fewer records.':'.'); }
    };
    wg.querySelectorAll('.side').forEach(function(sd){ sd.querySelectorAll('.adds .mk').forEach(function(b){ b.addEventListener('click', function(){
      if (load[sd.dataset.side].length>=8) return; load[sd.dataset.side].push({w:+b.dataset.w, n:b.textContent.replace('+ ','')}); draw(); }); }); });
    document.getElementById('weighReset').addEventListener('click', function(){ load.L=[]; load.R=[]; draw(); });
  }

  /* 10 timeline filter */
  const tlf=document.querySelectorAll('.tl-filters button');
  tlf.forEach(function(b){ b.addEventListener('click', function(){
    tlf.forEach(function(x){ x.setAttribute('aria-pressed', x===b?'true':'false'); });
    document.querySelectorAll('#tl > li').forEach(function(li){ li.hidden = !(b.dataset.m==='all' || li.classList.contains('now') || li.querySelector('.mk.'+b.dataset.m)); });
    const t=document.getElementById('tl'); if (t) t.scrollLeft=0;
  }); });

  /* 11 search the questions */
  const fq=document.getElementById('faqq');
  if (fq){
    const ds=[].slice.call(document.querySelectorAll('details.faq')), none=document.getElementById('faqnone');
    ds.forEach(function(d){ d.dataset.text=d.textContent.toLowerCase(); });
    fq.addEventListener('input', function(){
      const v=fq.value.trim().toLowerCase(); let shown=0;
      ds.forEach(function(d){ const hit=!v || v.split(/\s+/).every(function(w){ return d.dataset.text.indexOf(w)>-1; }); d.hidden=!hit; if (hit) shown++; if (v && hit) d.open=true; if (!v) d.open=false; });
      none.hidden = shown>0;
    });
  }

  /* 13 the clue of the week changes itself on schedule */
  const cj=document.getElementById('clues');
  if (cj){ try{
    const list=JSON.parse(cj.textContent), today=new Date(); let cur=list[0];
    list.forEach(function(c){ if (new Date(c[0]+'T00:00:00')<=today) cur=c; });
    document.getElementById('clueLbl').textContent='Clue of the week · '+cur[1];
    document.getElementById('clueText').textContent=cur[2];
    const cl=document.getElementById('clueLink'); cl.href='#case-'+cur[3]; cl.textContent='It’s Case '+cur[3]+' on the case board';
  }catch(e){} }

  /* the whisper: the open questions, one at a time, under the hero; and a red dot on Hunt while this week's clue is fresh */
  try{
    const W=document.getElementById('whisper'), WQ=document.getElementById('whisperQ'), raw=document.getElementById('clues');
    if (W && WQ && raw){
      const all=JSON.parse(raw.textContent), today=new Date().toISOString().slice(0,10);
      const out=all.filter(function(c){ return c[0]<=today; }); const list=(out.length?out:all.slice(0,1)).slice().reverse();
      if (list.length){
        let i=0; const show=function(){ const c=list[i%list.length]; WQ.textContent=c[2]; WQ.href='#case-'+c[3]; W.hidden=false; };
        show();
        const still=matchMedia('(prefers-reduced-motion: reduce)').matches;
        let hold=false; W.addEventListener('pointerenter', function(){ hold=true; }); W.addEventListener('pointerleave', function(){ hold=false; });
        if (list.length>1 && !still) setInterval(function(){ if (hold) return; W.classList.add('fade'); setTimeout(function(){ i++; show(); W.classList.remove('fade'); }, 480); }, 7000);
        const latest=out.length?out[out.length-1][0]:null;
        if (latest && (Date.parse(today)-Date.parse(latest))/864e5<7){ const h=document.querySelector('.bar nav a[href="#hunt"]'); if (h){ h.classList.add('fresh'); h.title='A new clue this week'; } }
      }
    }
  }catch(e){}

  /* 14 works offline after a first visit */
  if ('serviceWorker' in navigator && (location.protocol==='https:' || location.hostname==='localhost' || location.hostname==='127.0.0.1')){ addEventListener('load', function(){ navigator.serviceWorker.register('/sw.js').catch(function(){}); }); }

  /* glossary: the first use of each term on the page gets a short definition */
  const GL={
    'plat':['Plat','A surveyor’s drawing of land divided into lots or parcels, with streets and boundaries. Village plats were filed with the county.'],
    'probate':['Probate','The court process that settles a dead person’s estate. Probate files can hold wills, inventories, heirs’ names and signatures.'],
    'informant':['Informant','The person who answered the questions on a certificate. Their memory, not the dead person’s, is what the form records.'],
    'clues':['Clues','What the hunt gives you to start with: a line in a post, a date on the scroll, a word in a cipher. Every clue is true; none of them is the whole answer.'],
    'mysteries':['Mysteries','The hunt’s open cases: questions the county histories left hanging, each with a real answer waiting in a book, a map or a certificate. Crack one and your name goes on the board.'],
    'pages':['Pages','Two kinds. The printed and handwritten pages the hunt sends you to: county histories, registers, deeds, lodge proceedings and the newspapers of the day, most free online. And the social media pages where the hunt is played: Project Scroll’s own, and the halls that open as it goes.'],
    'websites':['Websites','The free archives where the record now lives: the Library of Congress, HathiTrust, FamilySearch, the Internet Archive, state archives and county pages. The hunt links the exact page.'],
    'county histories':['County histories','Thick volumes published from the 1870s to the 1910s, mostly from what local families supplied. Rich, but rarely checked.'],
    'lore':['Lore','What a place says about itself: the stories passed around a lake, a township or a lodge, told without a page to point to. Lore is where a hunt often starts; the record is where it ends.'],
    'local legends':['Local legends','The famous ancestor, the buried treasure, the river under the ground. Some are true. We read each one against the record.'],
    'legends':['Legends','The stories families and towns tell about themselves: the famous ancestor, the buried treasure, the river under the ground. Some are true. We read each one against the record.'],
    'survey maps':['Survey maps','Maps drawn from the government land surveys that first measured the country into townships and square-mile sections, with the lakes, streams and early roads the surveyors found.'],
    'certificates':['Certificates','The forms filed for a birth, a marriage or a death. A death certificate gives the date, place and cause, and often the parents’ names; Michigan required them from 1897. The answers came from an informant, not the person named.'],
    'forgotten newspapers':['Forgotten newspapers','Small-town papers of the 1800s and early 1900s, many surviving only on microfilm or in a few libraries. Their notices, gossip and obituaries often record what no official paper did.'],
    'field notes':['Field notes','The notebooks surveyors kept as they walked the land: distances, trees, streams and what they saw, line by line.'],
    'census':['Census','The national head-count taken every ten years. Old schedules list every person in a household, with ages and birthplaces.'],
    'transcription':['Transcription','A typed copy of an old handwritten record. Useful, but every copy can add mistakes, so check the original when you can.']
  };
  const host=document.querySelector('main'); let gi=0; const used={};
  const glossaryRun=function(scope){ if (scope && 'showPopover' in HTMLElement.prototype){
    const walker=document.createTreeWalker(scope, NodeFilter.SHOW_TEXT, {acceptNode:function(n){
      const p=n.parentElement; if (!p || p.closest('h1,h2,h3,button,a,summary,.mk,label,script,style,.gl,.tl .yr,.mstrip,.promo-marks,figcaption,[popover],svg,[role="img"],[role="button"],[tabindex],.cert-svg')) return NodeFilter.FILTER_REJECT; return NodeFilter.FILTER_ACCEPT; }});
    const nodes=[]; while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function(n){
      let cur=n;
      while (cur && cur.parentNode){
        let best=null;
        Object.keys(GL).forEach(function(term){
          if (used[term]) return;
          const m=cur.nodeValue.match(new RegExp('\\b('+term+')\\b','i'));
          if (m && (!best || m.index<best.m.index)) best={term:term, m:m};
        });
        if (!best) break;
        const term=best.term, m=best.m; used[term]=true; gi++;
        const id='gl'+gi, after=cur.splitText(m.index); after.nodeValue=after.nodeValue.slice(m[0].length);
        const b=document.createElement('button'); b.type='button'; b.className='gl'; b.textContent=m[0]; b.setAttribute('popovertarget',id); b.setAttribute('aria-label',m[0]+': what this means');
        const pop=document.createElement('div'); pop.id=id; pop.setAttribute('popover',''); pop.className='gloss'; pop.innerHTML='<b></b>'; pop.querySelector('b').textContent=GL[term][0]; pop.appendChild(document.createTextNode(GL[term][1]));
        const pm=after.nodeValue.match(/^[,.;:!?)’”]+/);
        if (pm){ const w=document.createElement('span'); w.className='glw'; w.appendChild(b); w.appendChild(document.createTextNode(pm[0])); after.nodeValue=after.nodeValue.slice(pm[0].length); cur.parentNode.insertBefore(w, after); } else cur.parentNode.insertBefore(b, after);
        document.body.appendChild(pop);
        if (CSS.supports && CSS.supports('anchor-name','--a')){ b.style.anchorName='--'+id; pop.style.positionAnchor='--'+id; pop.classList.add('anchored'); }
        pop.addEventListener('toggle', function(e){ if (pop.classList.contains('anchored')) return; if (e.newState==='open'){ const r=b.getBoundingClientRect(), w=pop.offsetWidth; pop.style.left=Math.max(8,Math.min(innerWidth-w-8, r.left+r.width/2-w/2))+'px'; const below=r.bottom+8; pop.style.top=(below+pop.offsetHeight>innerHeight? r.top-pop.offsetHeight-8 : below)+'px'; } });
        cur=after;
      }
    });
  } };
  /* the walk over every text node waits for an idle moment, so it never delays the first paint or the first tap */
  const hero=document.querySelector('.hero'); if (hero) glossaryRun(hero);  /* the first screen at once, so nothing shifts after paint */
  (window.requestIdleCallback || function(f){ setTimeout(f, 1); })(function(){ glossaryRun(host); }, {timeout:1500});

  /* read aloud: each section can be read out by the device's own voice */
  if ('speechSynthesis' in window){
    let speaking=null;
    const stop=function(){ speechSynthesis.cancel(); if (speaking){ speaking.setAttribute('aria-pressed','false'); speaking.textContent='Listen'; } speaking=null; };
    document.querySelectorAll('main > section > .part, main.page > .kicker').forEach(function(part){
      const sec=part.closest('section') || part.closest('main');
      const b=document.createElement('button'); b.type='button'; b.className='listen'; b.textContent='Listen'; b.setAttribute('aria-pressed','false'); b.title='Read this section aloud';
      part.appendChild(b);
      b.addEventListener('click', function(){
        if (speaking===b){ stop(); return; } stop();
        const clone=sec.cloneNode(true); clone.querySelectorAll('.listen,.mk,button,svg,script,style,[hidden],.mstrip,.tools,.seals,.filters,figure,input,textarea').forEach(function(x){ x.remove(); });
        const text=clone.innerText || clone.textContent; const u=new SpeechSynthesisUtterance(text.replace(/\s+/g,' ').trim());
        u.rate=.95; u.lang='en-US'; u.onend=u.onerror=function(){ if (speaking===b) stop(); };
        speaking=b; b.setAttribute('aria-pressed','true'); b.textContent='Stop'; speechSynthesis.speak(u);
      });
    });
    addEventListener('pagehide', stop);
  }

  /* search the whole site */
  const sdlg=document.getElementById('searchDlg'), sbtn=document.getElementById('searchBtn');
  if (sdlg && sbtn && sdlg.showModal){
    let idx=null; const q=document.getElementById('searchQ'), res=document.getElementById('searchRes');
    const sf=document.querySelector('form.search-in'); if (sf) sf.addEventListener('submit', function(e){ e.preventDefault(); });
    const esc=function(t){ return t.replace(/[&<>"]/g,function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
    const open=function(){ if (!sdlg.open) sdlg.showModal(); q.focus(); if (!idx) fetch('/search.json?v='+((document.querySelector('script[src*="site.min.js"]')||{src:''}).src.split('v=')[1]||'1')).then(function(r){ return r.json(); }).then(function(d){ idx=d; run(); }).catch(function(){ res.innerHTML='<li class="note">Search is not available offline yet.</li>'; }); };
    const run=function(){
      const v=q.value.trim().toLowerCase(); if (!idx){ return; } if (!v){ res.innerHTML=''; return; }
      const words=v.split(/\s+/);
      const hits=idx.map(function(d){ const T=d.t.toLowerCase(), X=d.x.toLowerCase(); let sc=0;
        for (const w of words){ const inT=T.indexOf(w)>-1, inX=X.indexOf(w)>-1; if (!inT && !inX) return null; sc+= (inT?10:0) + (inX?1:0); }
        return {d:d, sc:sc}; }).filter(Boolean).sort(function(a,b){ return b.sc-a.sc; }).slice(0,8);
      { const sc=document.getElementById('searchCount'); if (sc) sc.textContent=hits.length ? hits.length+(hits.length===1?' result':' results') : 'Nothing found'; }
      if (!hits.length){ res.innerHTML='<li class="note">Nothing found for “'+esc(q.value)+'”.</li>'; return; }
      res.innerHTML=hits.map(function(h){ const X=h.d.x, i=Math.max(0, X.toLowerCase().indexOf(words[0])-60); let snip=(i>0?'…':'')+X.slice(i, i+170)+'…';
        { const ws=words.filter(function(w){ return w.length>1; }).map(function(w){ return w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); });
          if (ws.length){ const rx=new RegExp('('+ws.join('|')+')','ig'); snip=snip.split(rx).map(function(part,k){ return k%2 ? '<mark class="hl">'+esc(part)+'</mark>' : esc(part); }).join(''); } else snip=esc(snip); }
        return '<li><a href="'+h.d.u+'"><b>'+esc(h.d.t)+'</b><span>'+snip+'</span></a></li>'; }).join('');
    };
    sbtn.addEventListener('click', open); q.addEventListener('input', run);
    document.getElementById('searchClose').addEventListener('click', function(){ sdlg.close(); });
    sdlg.addEventListener('click', function(e){ if (e.target===sdlg) sdlg.close(); });
    res.addEventListener('click', function(e){ if (e.target.closest('a')) sdlg.close(); });
    addEventListener('keydown', function(e){ if (e.key==='/' && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName) && !sdlg.open){ e.preventDefault(); open(); } });
  }

  /* a private notebook on each case page */
  const nb=document.getElementById('casenote');
  if (nb){
    const n=nb.dataset.case, key='ps-note-'+n, ta=document.getElementById('noteText'), nout=document.getElementById('noteOut');
    try{ ta.value=localStorage.getItem(key)||''; }catch(e){}
    ta.addEventListener('input', function(){ try{ localStorage.setItem(key, ta.value); }catch(e){} });
    const say=function(t){ nout.textContent=t; setTimeout(function(){ nout.textContent=''; },3500); };
    document.getElementById('noteCopy').addEventListener('click', function(){ const txt='My answer to Project Scroll case '+n+':\n\n'+ta.value.trim(); if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function(){ say('Copied. Paste it in the comments on Facebook.'); }, function(){ say('Copying was blocked; select the text and copy it.'); }); });
    document.getElementById('noteSave').addEventListener('click', function(){ const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([document.title+'\n\n'+ta.value],{type:'text/plain'})); a.download='project-scroll-case-'+n+'-notes.txt'; a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); },2000); });
  }
  const nbl=document.getElementById('nbList');
  if (nbl){
    const notes=[]; try{ for (let i=0;i<localStorage.length;i++){ const k=localStorage.key(i); if (/^ps-note-\d+$/.test(k) && localStorage.getItem(k).trim()) notes.push([+k.split('-')[2], localStorage.getItem(k)]); } }catch(e){}
    notes.sort(function(a,b){ return a[0]-b[0]; });
    if (notes.length){ nbl.innerHTML=''; notes.forEach(function(x){ const d=document.createElement('div'); d.className='nbitem'; const h=document.createElement('h2'); const a=document.createElement('a'); a.href='/cases/'+x[0]+'/'; a.textContent='Case '+x[0]; h.appendChild(a); const p=document.createElement('pre'); p.textContent=x[1]; d.appendChild(h); d.appendChild(p); nbl.appendChild(d); });
      document.getElementById('nbAll').hidden=false;
      document.getElementById('nbDl').addEventListener('click', function(){ const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([notes.map(function(x){ return 'CASE '+x[0]+'\n'+x[1]; }).join('\n\n---\n\n')],{type:'text/plain'})); a.download='project-scroll-notes.txt'; a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); }, 2000); });
      document.getElementById('nbClear').addEventListener('click', function(){ if (!confirm('Delete all your case notes on this device?')) return; notes.forEach(function(x){ try{ localStorage.removeItem('ps-note-'+x[0]); }catch(e){} }); location.reload(); }); }
  }

  /* for anyone who opens the browser's console */

  /* parts: a "next" link at the foot of each part, and a contents rail in the margin */
try{ (function(){
  const parts=[].slice.call(document.querySelectorAll('main > section')).filter(function(s){ return s.id && s.querySelector(':scope > .part') && s.querySelector(':scope > h2'); });
  if (parts.length<3) return;
  const label=function(s){ return { num:s.querySelector(':scope > .part').firstChild.textContent.replace(/^\s*Part\s*/i,'').trim(), title:s.querySelector(':scope > h2').textContent.trim() }; };
  parts.forEach(function(s,i){
    const nx=parts[i+1] || document.getElementById('contact'); if (!nx) return;
    const p=document.createElement('p'); p.className='nextpart';
    const a=document.createElement('a'); a.href='#'+nx.id;
    const L=parts[i+1] ? label(nx) : {num:'', title:(nx.querySelector('h2')||{}).textContent||'Contact'};
    a.innerHTML='<span>Next</span> '+(L.num?'<b>Part '+L.num+'</b> · ':'')+L.title+' <i aria-hidden="true">↓</i>';
    p.appendChild(a); s.appendChild(p);
  });
  const rail=document.createElement('nav'); rail.className='partrail'; rail.setAttribute('aria-label','Parts of this page');
  const links=parts.map(function(s){ const L=label(s), a=document.createElement('a'); a.href='#'+s.id; a.innerHTML='<b>'+L.num+'</b><span>'+L.title+'</span>'; rail.appendChild(a); return a; });
  document.body.appendChild(rail);
  if ('IntersectionObserver' in window){
    const io=new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting){ const i=parts.indexOf(e.target); links.forEach(function(a,j){ if (j===i) a.setAttribute('aria-current','true'); else a.removeAttribute('aria-current'); }); } }); }, {rootMargin:'-45% 0px -50% 0px'});
    parts.forEach(function(s){ io.observe(s); });
    const hero=document.querySelector('.hero'); if (hero){ new IntersectionObserver(function(es){ rail.classList.toggle('show', !es[0].isIntersecting); }).observe(hero); } else rail.classList.add('show');
  } else rail.classList.add('show');
})(); }catch(err){ psFail(err); }

/* the numbers strip counts up the first time it comes into view */
try{ (function(){
  const nums=[].slice.call(document.querySelectorAll('.stats b')); if (!nums.length || !('IntersectionObserver' in window)) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const io=new IntersectionObserver(function(es){ es.forEach(function(e){ if (!e.isIntersecting) return; io.unobserve(e.target);
    const el=e.target, end=parseInt(el.textContent,10); if (!(end>1)) return; const t0=performance.now(), d=900;
    const tick=function(t){ const k=Math.min(1,(t-t0)/d), v=Math.round(end*(1-Math.pow(1-k,3))); el.textContent=v; if (k<1) requestAnimationFrame(tick); else el.textContent=end; };
    el.textContent='0'; requestAnimationFrame(tick); }); }, {threshold:.6});
  nums.forEach(function(n){ io.observe(n); });
})(); }catch(err){ psFail(err); }

/* ---------- the tin-badge field book: badges earned around the site, kept in this browser only ---------- */
window.PS_BADGES=[
  ['candidate','Candidate','Open Project Scroll for the first time.'],
  ['regular','Regular','Come back on three different days.'],
  ['scroll','Read the walls','Read the home page from top to bottom.'],
  ['footnote','Footnote','Find what the little red star is hiding.'],
  ['casefile','Case reader','Open a case from the case board.'],
  ['follower','On the trail','Follow a case with its star.'],
  ['marks','Weigher','Mark a piece of evidence in “Try marking these yourself.”'],
  ['glossary','Plain English','Open a definition, or the glossary.'],
  ['mapper','Map room','Walk the 1860 wall map.'],
  ['thennow','Then and now','Lay an 1860 town plan over today’s streets.'],
  ['informant','Informant','Read the guide to the death certificate.'],
  ['oldhand','The old hand','Read the guide to old handwriting.'],
  ['records','Record keeper','Visit “Where the records are.”'],
  ['notes','Field notes','Open the book of field notes.'],
  ['legend','Legend tester','Test a family legend.'],
  ['toolkit','Toolmaker','Use a tool in the hunter’s toolkit.'],
  ['lantern','Lamplighter','Light the miner’s lamp in the top bar, then put it out.'],
  ['halter','Cipher breaker','Decode the hidden line, and say the word in your badge book.'],
  ['charter','Second cipher','Break the second line, which appears in your badge book once the first is broken.'],
  ['diamond','Eye for gold','Ask the gold diamond on the rule, and say its answer in your badge book.'],
  ['benefactor','Benefactor','Keep the hunt free as a friend of the hunt.'],
  ['patron','Patron','Fund a case on the board and see it opened.'],
  ['solver','Named on the board','Crack a case and be named as its solver on the case board.']
];
window.PS_RANKS=[[0,'Candidate'],[5,'Brother of the Halter'],[10,'Keeper of the Badge'],[15,'Recorder of the Hall'],[22,'Keeper of the Hall']];
try{ (function(){
  const KEY='ps-badges'; let got={};
  try{ got=JSON.parse(localStorage.getItem(KEY)||'{}')||{}; if (got.hewgag && !got.halter) got.halter=got.hewgag; if (got.credo && !got.charter) got.charter=got.credo; if (got.lamp && !got.lantern) got.lantern=got.lamp; delete got.hewgag; delete got.credo; delete got.lamp; }catch(e){ got={}; }
  let canStore=true; try{ localStorage.setItem('ps-t','1'); localStorage.removeItem('ps-t'); }catch(e){ canStore=false; }
  const save=function(){ try{ localStorage.setItem(KEY, JSON.stringify(got)); }catch(e){} };
  try{ const raw=localStorage.getItem(KEY)||''; if (/hewgag|credo/.test(raw)) save(); }catch(e){}
  const name=function(id){ const b=window.PS_BADGES.filter(function(x){ return x[0]===id; })[0]; return b?b[1]:id; };
  let toastEl=null, tq=[], showing=false;
  const showNext=function(){
    if (showing || !tq.length) return; showing=true; const id=tq.shift();
    if (!toastEl){ toastEl=document.createElement('div'); toastEl.className='btoast'; toastEl.setAttribute('role','status'); toastEl.setAttribute('aria-live','polite'); document.body.appendChild(toastEl);
      /* a new live region must be in the page before it is filled, or screen readers miss the first announcement */
      showing=false; tq.unshift(id); requestAnimationFrame(function(){ requestAnimationFrame(showNext); }); return; }
    toastEl.innerHTML='<svg viewBox="0 0 40 40" aria-hidden="true"><path class="tin" d="M20 2l4.7 9.6 10.5 1.5-7.6 7.4 1.8 10.5L20 26l-9.4 5 1.8-10.5-7.6-7.4 10.5-1.5z"/><circle cx="20" cy="17.5" r="4.2" class="boss"/></svg><span><small>Badge earned</small><b></b><a href="/badges/">Your badges</a></span>';
    toastEl.querySelector('b').textContent=name(id);
    { const x=document.createElement('button'); x.type='button'; x.className='bt-x'; x.setAttribute('aria-label','Close'); x.textContent='×'; x.addEventListener('click', function(){ toastEl.classList.remove('on'); }); toastEl.appendChild(x); }
    requestAnimationFrame(function(){ toastEl.classList.add('on'); });
    setTimeout(function(){ toastEl.classList.remove('on'); setTimeout(function(){ showing=false; showNext(); }, 450); }, 4200);
  };
  const earn=window.psEarn=function(id){ if (!canStore || got[id]) return false; got[id]=new Date().toISOString().slice(0,10); save(); tq.push(id); showNext(); document.dispatchEvent(new CustomEvent('ps-badge',{detail:id})); return true; };
  window.psBadges=function(){ return got; };
  const bl=document.getElementById('badgeLink'), bn=document.getElementById('badgeN');
  const showCount=function(){ if (!bl) return; const n=Object.keys(got).length, all=window.PS_BADGES.length;
    if (bn){ bn.textContent=n; bn.hidden=!n; } bl.setAttribute('aria-label','Your badges: '+n+' of '+all); bl.title='Your badges · '+n+' of '+all; };
  showCount(); document.addEventListener('ps-badge', function(){ showCount(); if (bl){ bl.classList.remove('ping'); void bl.offsetWidth; bl.classList.add('ping'); } });
  window.psResetBadges=function(){ got={}; save(); };
  /* days visited */
  try{ const d=new Date().toISOString().slice(0,10); let days=JSON.parse(localStorage.getItem('ps-days')||'[]'); if (days.indexOf(d)<0){ days.push(d); days=days.slice(-30); localStorage.setItem('ps-days', JSON.stringify(days)); } if (days.length>=3) setTimeout(function(){ earn('regular'); }, 2500); }catch(e){}
  setTimeout(function(){ earn('candidate'); }, 1500);
  const path=location.pathname;
  const byPath=[[/^\/cases\/\d+\/?$/,'casefile'],[/^\/map\/?$/,'mapper'],[/^\/map\/[a-z-]+\/?$/,'thennow'],[/^\/guide\/death-certificate\/?$/,'informant'],[/^\/guide\/old-handwriting\/?$/,'oldhand'],[/^\/records\/?$/,'records'],[/^\/glossary\/?$/,'glossary'],[/^\/notes\/book\/?$/,'notes']];
  byPath.forEach(function(r){ if (r[0].test(path)) setTimeout(function(){ earn(r[1]); }, 2200); });
  document.addEventListener('click', function(e){
    const t=e.target.closest && e.target.closest('button,a'); if (!t) return;
    if (t.id==='star') earn('footnote');
    else if (t.classList.contains('follow')) earn('follower');
    else if (t.classList.contains('gl')) earn('glossary');
    else if (t.closest('.qopts')) earn('marks');
    else if (/^\/legends\/?$/.test(path) && t.tagName==='BUTTON' && t.closest('main')) earn('legend');
  });
  if (/^\/toolkit\/?$/.test(path)){ const once=function(e){ if (e.target.closest && e.target.closest('.tool')){ earn('toolkit'); } }; document.addEventListener('input', once); document.addEventListener('change', once); }
  const ct=document.getElementById('contact');
  if (ct && 'IntersectionObserver' in window && document.getElementById('hunt')){ const io=new IntersectionObserver(function(es){ if (es[0].isIntersecting){ earn('scroll'); io.disconnect(); } }, {threshold:.25}); io.observe(ct); }
})(); }catch(err){ psFail(err); }

/* ---------- the clue of the week counts down to the next one ---------- */
try{ (function(){
  const cj=document.getElementById('clues'), box=document.getElementById('clueNext'); if (!cj || !box) return;
  let list=[]; try{ list=JSON.parse(cj.textContent); }catch(e){ return; }
  const tick=function(){
    const now=new Date(); const nx=list.filter(function(c){ return new Date(c[0]+'T00:00:00')>now; })[0];
    if (!nx){ box.textContent='The next clue is coming soon.'; return; }
    let ms=new Date(nx[0]+'T00:00:00')-now, d=Math.floor(ms/864e5), h=Math.floor(ms%864e5/36e5), m=Math.floor(ms%36e5/6e4);
    const pl=function(n,w){ return n+' '+w+(n===1?'':'s'); };
    box.textContent='Next clue in '+(d>0? pl(d,'day')+', '+pl(h,'hour') : h>0? pl(h,'hour')+', '+pl(m,'minute') : pl(Math.max(1,m),'minute'))+' · '+nx[1];
  };
  tick(); setInterval(tick, 30000);
})(); }catch(err){ psFail(err); }

/* ---------- on this day in the record ---------- */
try{ (function(){
  const box=document.getElementById('otd'), dj=document.getElementById('otdData'); if (!box || !dj) return;
  let L=[]; try{ L=JSON.parse(dj.textContent); }catch(e){ return; }
  const now=new Date(), y=now.getFullYear(), MON=['January','February','March','April','May','June','July','August','September','October','November','December'];
  const at=function(e,yr){ return new Date(yr, e[0]-1, e[1]); };
  const today=new Date(y, now.getMonth(), now.getDate());
  let hit=L.filter(function(e){ return e[0]===now.getMonth()+1 && e[1]===now.getDate(); })[0], lbl, days=0;
  if (hit){ lbl='On this day in the record'; }
  else { let best=null; L.forEach(function(e){ let d=at(e,y); if (d<today) d=at(e,y+1); const k=d-today; if (!best || k<best.k) best={e:e,k:k}; }); hit=best.e; days=Math.round(best.k/864e5); lbl='Coming up in the record · in '+days+(days===1?' day':' days'); }
  const S=L.slice().sort(function(a,b){ return (a[0]-b[0])||(a[1]-b[1])||(a[2]-b[2]); });
  const show=function(e,l){ box.querySelector('.otd-l').textContent=l; box.querySelector('.otd-d').textContent=e[1]+' '+MON[e[0]-1]+' '+e[2];
    box.querySelector('.otd-t').textContent=e[3]; box.querySelector('.otd-s').textContent=e[4]; };
  show(hit,lbl); box.hidden=false;
  /* turn through the calendar of the record, a day at a time */
  let i=S.indexOf(hit); const nav=box.querySelector('.otd-nav');
  if (nav && S.length>1){ nav.hidden=false;
    const go=function(d){ i=(i+d+S.length)%S.length; const e=S[i]; show(e, e===hit ? lbl : 'Elsewhere in the calendar of the record'); box.classList.remove('flip'); void box.offsetWidth; box.classList.add('flip'); };
    document.getElementById('otdPrev').addEventListener('click', function(){ go(-1); });
    document.getElementById('otdNext').addEventListener('click', function(){ go(1); }); }
})(); }catch(err){ psFail(err); }

/* links to other websites open in a new tab. The site's own menu (top bar, logo, footer, search results,
   parts rail) stays in the same tab, so Back works. Other links to the site's own pages still open a new tab. */
try{ (function(){
  const here=location.origin+location.pathname, MENU='.bar, footer.site nav, #searchRes, .partrail, .skip';
  const mark=function(a){
    const h=a.getAttribute('href'); if (!h || h.charAt(0)==='#' || /^(mailto:|tel:|javascript:)/i.test(h)) return;
    let u; try{ u=new URL(h, location.href); }catch(e){ return; }
    if (u.origin+u.pathname===here && u.hash) return;
    if (u.origin===location.origin && a.closest(MENU)){ if (a.target==='_blank') a.removeAttribute('target'); return; }
    a.target='_blank'; const r=(a.getAttribute('rel')||'').split(/\s+/); if (r.indexOf('noopener')<0) r.push('noopener'); a.setAttribute('rel', r.join(' ').trim());
  };
  document.querySelectorAll('a[href]').forEach(mark);
  document.addEventListener('click', function(e){ const a=e.target.closest && e.target.closest('a[href]'); if (a) mark(a); }, true);
})(); }catch(err){ psFail(err); }

/* ---------- the scroll: jump to an era ---------- */
try{ (function(){
  const t=document.getElementById('tl'), filters=document.querySelector('.tl-filters'); if (!t || !filters) return;
  const yearOf=function(li){ const y=(li.querySelector('.yr')||{}).textContent||''; if (/now/i.test(y)) return 99999; const n=parseInt(y.replace(/[^0-9]/g,''),10); return /BC/.test(y) ? -n : n; };
  const ERAS=[['Deep time',-1e9,1499],['1500s–1700s',1500,1799],['1800s',1800,1899],['1900s',1900,1999],['Now',2000,1e9]];
  const lis=[].slice.call(t.children), smooth=matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth';
  const row=document.createElement('div'); row.className='tl-eras'; row.setAttribute('role','group'); row.setAttribute('aria-label','Jump to an era');
  const lbl=document.createElement('span'); lbl.className='lbl'; lbl.textContent='Jump to'; row.appendChild(lbl);
  ERAS.forEach(function(e){
    const first=lis.filter(function(li){ const y=yearOf(li); return y>=e[1] && y<=e[2] && !li.hidden; })[0]; if (!first) return;
    const b=document.createElement('button'); b.type='button'; b.textContent=e[0];
    const n=lis.filter(function(li){ const y=yearOf(li); return y>=e[1] && y<=e[2] && li.classList.contains('sealed'); }).length;
    if (n) b.title=n+(n===1?' sealed date':' sealed dates');
    b.addEventListener('click', function(){ const f=lis.filter(function(li){ const y=yearOf(li); return y>=e[1] && y<=e[2] && !li.hidden; })[0]||first;
      t.scrollTo({left:Math.max(0,f.offsetLeft-8), behavior:smooth}); f.classList.remove('lit'); void f.offsetWidth; f.classList.add('lit'); });
    row.appendChild(b);
  });
  filters.insertAdjacentElement('afterend', row);
})(); }catch(err){ psFail(err); }

/* ---------- a case saved for offline: the page and its papers go into a cache that survives updates ---------- */
try{ (function(){
  const b=document.getElementById('saveOff'), msg=document.getElementById('saveOffMsg'); if (!b) return;
  if (!('caches' in window) || !('serviceWorker' in navigator)) return;
  const files=[location.pathname].concat([].slice.call(document.querySelectorAll('a[href$=".pdf"]')).map(function(a){ return a.getAttribute('href'); }));
  const tick=function(){ b.textContent='Saved for offline ✓'; b.disabled=true; };
  caches.open('ps-files').then(function(c){ return c.match(location.pathname); }).then(function(hit){ b.hidden=false; if (hit) tick(); }).catch(function(){ b.hidden=false; });
  b.addEventListener('click', function(){
    b.disabled=true; msg.textContent='Saving…';
    caches.open('ps-files').then(function(c){ return c.addAll(files.filter(function(u,i,a){ return a.indexOf(u)===i; })); })
      .then(function(){ tick(); msg.textContent='This case and its papers now open without a signal.'; setTimeout(function(){ msg.textContent=''; }, 5000); })
      .catch(function(){ b.disabled=false; msg.textContent='Could not save it. Try again when you are online.'; });
  });
  const pc=document.getElementById('printCase'); if (pc) pc.addEventListener('click', function(){ window.print(); });
})(); }catch(err){ psFail(err); }

/* ---------- search by voice, where the browser can listen ---------- */
try{ (function(){
  const SR=window.SpeechRecognition || window.webkitSpeechRecognition, q=document.getElementById('searchQ'); if (!SR || !q) return;
  const m=document.createElement('button'); m.type='button'; m.className='mic'; m.setAttribute('aria-label','Search by voice'); m.title='Search by voice';
  m.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M9 21h6"/></svg>';
  q.insertAdjacentElement('afterend', m);
  let rec=null;
  m.addEventListener('click', function(){
    if (rec){ rec.stop(); return; }
    rec=new SR(); rec.lang='en-US'; rec.interimResults=true; rec.maxAlternatives=1; m.classList.add('listening'); q.placeholder='Listening…';
    rec.onresult=function(e){ let t=''; for (let i=0;i<e.results.length;i++) t+=e.results[i][0].transcript; q.value=t.trim(); q.dispatchEvent(new Event('input',{bubbles:true})); };
    rec.onend=function(){ rec=null; m.classList.remove('listening'); q.placeholder='Search cases, field notes, guides…'; q.focus(); };
    rec.onerror=rec.onend;
    try{ rec.start(); }catch(e){ rec.onend(); }
  });
})(); }catch(err){ psFail(err); }

/* ---------- the ledger that travels: badges, follows and notes as one checked file, read back on another device ---------- */
try{ (function(){
  const out=document.getElementById('ledgerOut'), inp=document.getElementById('ledgerIn'), msg=document.getElementById('ledgerMsg'); if (!out || !inp) return;
  const KEYS=/^(ps-badges|ps-mine|ps-days|ps-note-\d+|ps-inked)$/;
  const gather=function(){ const d={}; for (let i=0;i<localStorage.length;i++){ const k=localStorage.key(i); if (KEYS.test(k)) d[k]=localStorage.getItem(k); } return d; };
  const sum=function(txt){ if (!(crypto && crypto.subtle)) return Promise.resolve(''); return crypto.subtle.digest('SHA-256', new TextEncoder().encode(txt)).then(function(h){ return [].slice.call(new Uint8Array(h)).map(function(b){ return ('0'+b.toString(16)).slice(-2); }).join(''); }); };
  out.addEventListener('click', function(){
    const data=gather(), body=JSON.stringify(data);
    sum(body).then(function(h){
      const file=JSON.stringify({site:'projectscroll.com', kind:'ledger', made:new Date().toISOString().slice(0,10), sha256:h, data:data}, null, 1);
      const blob=new Blob([file], {type:'application/json'}), name='project-scroll-ledger-'+new Date().toISOString().slice(0,10)+'.json';
      const f=new File([blob], name, {type:'application/json'});
      if (navigator.canShare && navigator.canShare({files:[f]})) return navigator.share({files:[f], title:'My Project Scroll ledger'}).catch(function(){});
      const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name; document.body.appendChild(a); a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 2000);
    }).then(function(){ msg.textContent='Your ledger is made. Open it on the other device from this same page.'; });
  });
  inp.addEventListener('change', function(){
    const f=inp.files && inp.files[0]; if (!f) return;
    f.text().then(function(t){
      let j; try{ j=JSON.parse(t); }catch(e){ msg.textContent='That file is not a ledger.'; return; }
      if (!j || j.kind!=='ledger' || !j.data){ msg.textContent='That file is not a Project Scroll ledger.'; return; }
      return sum(JSON.stringify(j.data)).then(function(h){
        if (j.sha256 && h && j.sha256!==h){ msg.textContent='That ledger has been altered since it was made, so it was not read.'; return; }
        let n=0; Object.keys(j.data).forEach(function(k){ if (!KEYS.test(k)) return;
          if (k==='ps-badges' || k==='ps-mine'){ try{ const cur=JSON.parse(localStorage.getItem(k)||(k==='ps-mine'?'[]':'{}')), add=JSON.parse(j.data[k]); if (Array.isArray(cur)){ add.forEach(function(x){ if (cur.indexOf(x)<0) cur.push(x); }); localStorage.setItem(k, JSON.stringify(cur)); } else { Object.keys(add).forEach(function(b){ if (!cur[b]) cur[b]=add[b]; }); localStorage.setItem(k, JSON.stringify(cur)); } n++; return; }catch(e){} }
          if (/^ps-note-/.test(k) && (localStorage.getItem(k)||'').trim()){ localStorage.setItem(k, (localStorage.getItem(k)+'\n\n'+j.data[k]).trim()); n++; return; }
          localStorage.setItem(k, j.data[k]); n++; });
        msg.textContent='Ledger read: '+n+' entries brought over, merged with what was already here.'; setTimeout(function(){ location.reload(); }, 1400);
      });
    });
  });
})(); }catch(err){ psFail(err); }

/* ---------- Draft 77: the visual set ---------- */
try{ (function(){
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* 12 a case's question writes itself the first time you open that case */
  const nb=document.getElementById('casenote');
  if (nb && !reduce){ try{ const k='ps-seen-'+nb.dataset.case; if (!localStorage.getItem(k)){ document.documentElement.classList.add('ink-case'); localStorage.setItem(k,'1'); } }catch(e){} }
  /* 13 the next sealed year glows: the hunt is coming for it */
  const tl=document.getElementById('tl');
  if (tl){ const lis=[].slice.call(tl.children); let first=lis.findIndex(function(li){ return !li.classList.contains('sealed'); }); if (first<0) first=-1;
    for (let i=first+1;i<lis.length;i++){ if (lis[i].classList.contains('sealed')){ lis[i].classList.add('next'); const m=lis[i].querySelector('.sealedmk'); if (m){ const t=document.createElement('span'); t.className='nextmk'; t.textContent='Next to open'; m.insertAdjacentElement('afterend', t); } break; } } }
  /* 14 dusk: in the hour either side of sunset on the reader's own clock, the paper warms (the stylesheet applies it to light pages only) */
  try{
    {
      const SUNSET=[17.5,18.1,18.8,20.2,20.7,21.2,21.1,20.6,19.7,18.9,17.4,17.1]; /* typical sunset, Great Lakes country, by month */
      const now=new Date(), h=now.getHours()+now.getMinutes()/60, ss=SUNSET[now.getMonth()];
      if (h>=ss-1 && h<=ss+1.2) document.documentElement.setAttribute('data-dusk','');
    }
  }catch(e){}
  /* 15 the map room: a lamp follows the pointer in the dark */
  const room=document.querySelector('.maproom');
  if (room && matchMedia('(hover:hover) and (pointer:fine)').matches){
    room.addEventListener('pointermove', function(e){ const r=room.getBoundingClientRect(); room.style.setProperty('--lx', ((e.clientX-r.left)/r.width*100).toFixed(1)+'%'); room.style.setProperty('--ly', ((e.clientY-r.top)/r.height*100).toFixed(1)+'%'); room.classList.add('lit'); }, {passive:true});
    room.addEventListener('pointerleave', function(){ room.classList.remove('lit'); });
  }
  /* 16 "last touched" stamps on the board */
  document.querySelectorAll('tr[data-touched]').forEach(function(tr){ const td=tr.querySelector('td.hall'); if (!td) return; const s=document.createElement('small'); s.className='touched'; s.textContent='touched '+tr.dataset.touched; td.appendChild(s); });
})(); }catch(err){ psFail(err); }

/* ---------- the masthead strip: the Osborn page first, the heron second, then the rest; a random pause between; click or hover to see more ---------- */
try{ (function(){
  const mh=document.getElementById('masthead'); if (!mh) return;
  const set=mh.dataset.set.split(';').map(function(x){ const p=x.split('|'); return {id:p[0], cap:p[1], pos:p[2]||'50% 50%', href:p[3]||'', tone:p[4]||'c'}; });
  const cap=mh.querySelector('.mh-cap'), nbtn=mh.querySelector('.mh-next'); let cur=mh.querySelector('.mh-pic');
  const ticks=document.createElement('div'); ticks.className='mh-ticks'; ticks.setAttribute('aria-hidden','true'); set.forEach(function(){ ticks.appendChild(document.createElement('i')); }); mh.appendChild(ticks);
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  let i=0; try{ const seen=localStorage.getItem('ps-strip'); if (seen!==null) i=(parseInt(seen,10)+1)%set.length; localStorage.setItem('ps-strip', String(i)); }catch(e){}
  const make=function(k){ const p=document.createElement('picture'); p.className='mh-pic '+k.tone; p.innerHTML='<source media="(max-width:700px)" srcset="/img/strip/'+k.id+'-800.webp"><img width="1600" height="400" alt="" decoding="async">'; const im=p.querySelector('img'); im.src='/img/strip/'+k.id+'.webp'; im.style.objectPosition=k.pos; return p; };
  const label=function(k){ [].forEach.call(ticks.children, function(t,j){ t.classList.toggle('on', j===set.indexOf(k)); }); cap.innerHTML=''; const n=document.createElement('span'); n.className='mh-n'; n.textContent=(set.indexOf(k)+1)+' / '+set.length; cap.appendChild(n); if (k.href){ const a=document.createElement('a'); a.href=k.href; a.textContent=k.cap; a.title='Open the page this comes from'; cap.appendChild(a); } else cap.appendChild(document.createTextNode(k.cap)); };
  const preload=function(k){ const im=new Image(); im.src='/img/strip/'+k.id+(innerWidth<=700?'-800':'')+'.webp'; };
  const show=function(k){ const n=make(k); mh.insertBefore(n, cap); const img=n.querySelector('img');
    const go=function(){ n.classList.add('on'); const old=cur; cur=n; label(k); if (!reduce){ mh.classList.remove('glint'); void mh.offsetWidth; mh.classList.add('glint'); } mh.classList.add('cap-show'); clearTimeout(mh._ct); mh._ct=setTimeout(function(){ mh.classList.remove('cap-show'); }, 4500); setTimeout(function(){ if (old && old!==cur) old.remove(); }, reduce?50:4200); };
    if (img.complete) go(); else img.addEventListener('load', go, {once:true}); };
  if (i!==0) show(set[i]); else { cur.querySelector('img').style.objectPosition=set[0].pos; cur.classList.add(set[0].tone); label(set[0]); }
  preload(set[(i+1)%set.length]); preload(set[(i+2)%set.length]);
  let t=null, seen=false;
  const next=function(){ i=(i+1)%set.length; show(set[i]); preload(set[(i+1)%set.length]); preload(set[(i+2)%set.length]); try{ localStorage.setItem('ps-strip', String(i)); }catch(e){} };
  const arm=function(){ clearTimeout(t); if (!seen || reduce) return; t=setTimeout(function(){ if (document.documentElement.classList.contains('calm')){ arm(); return; } next(); arm(); }, 20000+Math.random()*40000); };
  if ('IntersectionObserver' in window) new IntersectionObserver(function(es){ seen=es[0].isIntersecting; arm(); }, {threshold:.5}).observe(mh);
  const prev=function(){ i=(i+set.length-2)%set.length; next(); };
  const pbtn=mh.querySelector('.mh-prev'); if (pbtn) pbtn.addEventListener('click', function(e){ e.stopPropagation(); prev(); arm(); });
  const fbtn=mh.querySelector('.mh-full'); if (fbtn) fbtn.addEventListener('click', function(e){ e.stopPropagation(); let d=document.getElementById('plateDlg'); if (!d){ d=document.createElement('dialog'); d.id='plateDlg'; d.className='plate-dlg'; d.innerHTML='<img alt=""><p class="pd-cap"></p><p class="pd-nav"><button type="button" class="btn" id="pdPrev" aria-label="Previous plate">‹</button><span class="pd-n"></span><button type="button" class="btn" id="pdNext" aria-label="Next plate">›</button></p><button type="button" class="btn" id="pdClose">Close</button>'; document.body.appendChild(d); d.querySelector('#pdClose').addEventListener('click', function(){ d.close(); }); d.addEventListener('click', function(ev){ if (ev.target===d) d.close(); }); d.querySelector('#pdPrev').addEventListener('click', function(){ prev(); arm(); fill(); }); d.querySelector('#pdNext').addEventListener('click', function(){ next(); arm(); fill(); }); d.addEventListener('keydown', function(ev){ if (ev.key==='ArrowRight'){ next(); arm(); fill(); ev.preventDefault(); } else if (ev.key==='ArrowLeft'){ prev(); arm(); fill(); ev.preventDefault(); } }); }
    fill(); if (!d.open) d.showModal(); });
  const fill=function(){ const d=document.getElementById('plateDlg'); if (!d) return;
    const k=set[i]; d.querySelector('img').src='/img/strip/'+k.id+'.webp'; d.querySelector('.pd-n').textContent=(i+1)+' / '+set.length; const c=d.querySelector('.pd-cap'); c.innerHTML=''; if (k.href){ const a=document.createElement('a'); a.href=k.href; a.textContent=k.cap; c.appendChild(a); } else c.textContent=k.cap; };
  nbtn.addEventListener('click', function(e){ e.stopPropagation(); next(); arm(); });
  mh.addEventListener('pointerenter', function(){ clearTimeout(t); }); mh.addEventListener('pointerleave', function(){ arm(); });
  mh.tabIndex=0; mh.setAttribute('aria-label','The masthead plates: Enter opens, arrow keys turn the plates');
  const hint=document.createElement('span'); hint.className='mh-hint'; hint.setAttribute('aria-hidden','true'); hint.textContent='← → to turn · Enter to open'; mh.appendChild(hint);
  mh.addEventListener('keydown', function(e){ if (e.key==='ArrowRight'){ next(); arm(); e.preventDefault(); } else if (e.key==='ArrowLeft'){ prev(); arm(); e.preventDefault(); } else if (e.key==='Enter' && e.target===mh){ mh.classList.toggle('open'); } });
  mh.addEventListener('click', function(e){ if (e.target.closest('button')) return; mh.classList.toggle('open'); });
  mh.addEventListener('keydown', function(e){ if (e.key==='Escape') mh.classList.remove('open'); });
})(); }catch(err){ psFail(err); }

/* ---------- the miner's lamp: a warm glow that follows the pointer, off until it is lit ---------- */
try{ (function(){
  const b=document.getElementById('lamp'); if (!b) return;
  const fine=matchMedia('(hover:hover) and (pointer:fine)').matches; if (!fine){ b.hidden=true; return; }
  const root=document.documentElement; let veil=null, on=false, lit=false, raf=0, x=innerWidth/2, y=innerHeight/2;
  const paint=function(){ raf=0; if (veil){ veil.style.setProperty('--lx', x+'px'); veil.style.setProperty('--ly', y+'px'); } };
  const move=function(e){ x=e.clientX; y=e.clientY; if (!raf) raf=requestAnimationFrame(paint); };
  const sizeVeil=function(){ if (veil) veil.style.setProperty('--lr', Math.round(Math.max(innerWidth, innerHeight)*0.75)+'px'); };
  const set=function(v){
    on=v; b.setAttribute('aria-pressed', String(on)); b.setAttribute('aria-label', on?'Put out the miner’s lamp':'Light the miner’s lamp'); root.classList.toggle('lamp-on', on);
    if (on){ if (!veil){ veil=document.createElement('div'); veil.className='lamp-veil'; veil.setAttribute('aria-hidden','true'); document.body.appendChild(veil); } sizeVeil(); paint(); requestAnimationFrame(function(){ veil.classList.add('on'); }); addEventListener('pointermove', move, {passive:true}); lit=true; }
    else { if (veil) veil.classList.remove('on'); removeEventListener('pointermove', move); if (lit && window.psEarn) psEarn('lantern'); }
  };
  b.addEventListener('click', function(){ set(!on); });
  try{ localStorage.removeItem('ps-lamp'); localStorage.removeItem('ps-lantern'); }catch(e){}
  addEventListener('resize', sizeVeil, {passive:true});
})(); }catch(err){ psFail(err); }

/* ---------- the gold diamond on the rule answers, if asked ---------- */
try{ (function(){
  const bar=document.querySelector('.bar-in'); if (!bar) return;
  const d=document.createElement('button'); d.type='button'; d.className='diamond'; d.setAttribute('aria-label','The gold diamond'); d.title='Ask the diamond'; bar.appendChild(d);
  let strip=null, t=null;
  const LINES=['A book with a gold ribbon sits at the top of every page. Say what it is in your badge book.','What the lake forgets, I keep, line by line. Say my name in your badge book.','I am opened at the top of every page and closed at the foot. One word. Say it in your badge book.'];
  let i=0;
  d.addEventListener('click', function(){
    if (!strip){ strip=document.createElement('p'); strip.className='riddle'; strip.setAttribute('role','status'); strip.setAttribute('aria-live','polite'); document.querySelector('.bar').appendChild(strip); }
    strip.textContent=LINES[i++%LINES.length]; strip.classList.add('on'); d.classList.add('asked');
    clearTimeout(t); t=setTimeout(function(){ strip.classList.remove('on'); }, 9000);
  });
})(); }catch(err){ psFail(err); }

/* ---------- the top bar: a gold marker glides to the section you are reading, and follows the pointer ---------- */
try{ (function(){
  const nav=document.querySelector('.bar nav'); if (!nav) return;
  const ink=document.createElement('span'); ink.className='navink'; ink.setAttribute('aria-hidden','true'); nav.appendChild(ink);
  let hover=null;
  const place=function(){
    const a=hover || nav.querySelector('a[aria-current="true"]');
    if (!a || !a.offsetParent || getComputedStyle(nav).flexDirection==='column'){ ink.style.opacity='0'; return; }
    ink.style.opacity='1'; ink.style.width=a.offsetWidth+'px'; ink.style.transform='translateX('+a.offsetLeft+'px)';
  };
  new MutationObserver(place).observe(nav, {subtree:true, attributes:true, attributeFilter:['aria-current']});
  nav.querySelectorAll('a').forEach(function(a){ a.addEventListener('pointerenter', function(){ hover=a; place(); }); a.addEventListener('focus', function(){ hover=a; place(); }); a.addEventListener('blur', function(){ hover=null; place(); }); });
  nav.addEventListener('pointerleave', function(){ hover=null; place(); });
  addEventListener('resize', place, {passive:true}); if (document.fonts && document.fonts.ready) document.fonts.ready.then(place);
  place(); document.documentElement.classList.add('has-navink');
})(); }catch(err){ psFail(err); }

/* ---------- the scroll: the era buttons follow along as you read ---------- */
try{ (function(){
  const t=document.getElementById('tl'), row=document.querySelector('.tl-eras'); if (!t || !row) return;
  const btns=[].slice.call(row.querySelectorAll('button')); if (!btns.length) return;
  const yearOf=function(li){ const y=(li.querySelector('.yr')||{}).textContent||''; if (/now/i.test(y)) return 99999; const n=parseInt(y.replace(/[^0-9]/g,''),10); return /BC/.test(y) ? -n : n; };
  const eraOf=function(y){ return y<1500?'Deep time': y<1800?'1500s–1700s': y<1900?'1800s': y<2000?'1900s':'Now'; };
  let q=0; const spy=function(){ q=0; const lis=[].slice.call(t.children).filter(function(li){ return !li.hidden; });
    const mid=t.scrollLeft+t.clientWidth*0.35; let cur=lis[0];
    lis.forEach(function(li){ if (li.offsetLeft<=mid) cur=li; });
    if (t.scrollLeft+t.clientWidth>=t.scrollWidth-4) cur=lis[lis.length-1];
    const e=cur?eraOf(yearOf(cur)):''; btns.forEach(function(b){ if (b.textContent===e) b.setAttribute('aria-current','true'); else b.removeAttribute('aria-current'); }); };
  t.addEventListener('scroll', function(){ if (!q) q=requestAnimationFrame(spy); }, {passive:true}); spy();
})(); }catch(err){ psFail(err); }

/* ---------- the advertisement: a light catches the paper as the pointer moves ---------- */
try{ (function(){
  const ad=document.querySelector('.promo.ad'); if (!ad || !matchMedia('(hover: hover) and (pointer: fine)').matches || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  let q=0, x=0, y=0;
  ad.addEventListener('pointermove', function(e){ const r=ad.getBoundingClientRect(); x=(e.clientX-r.left)/r.width*100; y=(e.clientY-r.top)/r.height*100;
    if (!q) q=requestAnimationFrame(function(){ q=0; ad.style.setProperty('--gx', x.toFixed(1)+'%'); ad.style.setProperty('--gy', y.toFixed(1)+'%'); ad.classList.add('glow'); }); }, {passive:true});
  ad.addEventListener('pointerleave', function(){ ad.classList.remove('glow'); });
})(); }catch(err){ psFail(err); }

/* ---------- the advertisement: "Ask about this" fills in the message form for you ---------- */
try{ (function(){
  const sel=document.querySelector('#msgform select[name="need"]'); if (!sel) return;
  document.addEventListener('click', function(e){
    const a=e.target.closest && e.target.closest('[data-need]'); if (!a) return;
    const want=a.dataset.need; [].slice.call(sel.options).forEach(function(o){ if (o.textContent===want) sel.value=o.value||o.textContent; });
    sel.dispatchEvent(new Event('change', {bubbles:true}));
    setTimeout(function(){ const t=document.querySelector('#msgform textarea[name="mystery"]'); if (t) t.focus({preventScroll:true}); sel.classList.remove('flash'); void sel.offsetWidth; sel.classList.add('flash'); }, 650);
  });
})(); }catch(err){ psFail(err); }

/* ---------- the advertisement: "What do you have?" points to the right service ---------- */
try{ (function(){
  const box=document.getElementById('adFinder'), out=document.getElementById('adFa'); if (!box || !out) return;
  const A={
    q:['The research desk traces it through the record: certificates, deeds, censuses, county histories and old newspapers, every statement marked.','Research: a mystery or an ancestor'],
    photo:['The studio images it at high resolution, repairs what time has done to it, and studies its details: the clothes, the buildings, the signs in a window.','Image creation or restoration'],
    doc:['Imaging analysis brings faded ink back and makes a damaged or water-stained page readable again, and the desk reads what it says.','Imaging analysis'],
    place:['Old plats, survey notes and county atlases show what was there, and a 3D LiDAR model from public elevation surveys shows what the ground still remembers.','3D LiDAR imaging'],
    story:['We test it against the record and tell you honestly which parts hold up, which do not, and which are still open.','Testing a family legend'],
    book:['Historical research and fact-checking for authors, filmmakers and local groups, and a living document that keeps growing with the work.','Research for a book, film or group']
  };
  box.querySelectorAll('button[data-k]').forEach(function(b){
    b.addEventListener('click', function(){
      box.querySelectorAll('button[data-k]').forEach(function(x){ x.setAttribute('aria-pressed', String(x===b)); });
      const r=A[b.dataset.k]; out.textContent=r[0]+' ';
      const a=document.createElement('a'); a.href='#contact'; a.dataset.need=r[1]; a.textContent='Ask about this ›'; out.appendChild(a);
      out.hidden=false; out.classList.remove('in'); void out.offsetWidth; out.classList.add('in');
    });
  });
})(); }catch(err){ psFail(err); }

/* ---------- Part I: drag the scroll sideways with the mouse ---------- */
try{ (function(){
  const t=document.getElementById('tl'); if (!t || !matchMedia('(pointer: fine)').matches) return;
  let down=false, x0=0, s0=0, moved=false;
  t.addEventListener('pointerdown', function(e){ if (e.pointerType!=='mouse' || e.button!==0 || e.target.closest('a,button')) return; down=true; moved=false; x0=e.clientX; s0=t.scrollLeft; t.classList.add('grabbing'); });
  addEventListener('pointermove', function(e){ if (!down) return; const dx=e.clientX-x0; if (Math.abs(dx)>4) moved=true; if (moved){ t.style.scrollSnapType='none'; t.scrollLeft=s0-dx; } }, {passive:true});
  addEventListener('pointerup', function(){ if (!down) return; down=false; t.classList.remove('grabbing'); t.style.scrollSnapType=''; });
  t.addEventListener('click', function(e){ if (moved){ e.preventDefault(); e.stopPropagation(); moved=false; } }, true);
})(); }catch(err){ psFail(err); }

/* ---------- Ctrl+K or Cmd+K opens the search, as in most modern apps ---------- */
try{ addEventListener('keydown', function(e){ if ((e.ctrlKey || e.metaKey) && (e.key==='k' || e.key==='K')){ const b=document.getElementById('searchBtn'); if (b){ e.preventDefault(); b.click(); } } }); }catch(err){ psFail(err); }

/* ---------- the top bar: a gold tab names the part you are in while you scroll, then tucks away ---------- */
try{ (function(){
  const bi=document.querySelector('.bar-in'), bar=document.querySelector('.bar'); if (!bi || !bar) return;
  const tab=document.createElement('a'); tab.className='bar-tab'; tab.setAttribute('aria-hidden','true'); tab.tabIndex=-1; bi.appendChild(tab);
  const parts=[].slice.call(document.querySelectorAll('main section')).filter(function(s){ return s.id && s.querySelector(':scope > .part'); });
  if (!parts.length) return;
  let q=0, hideT=0;
  const sync=function(){ q=0; const line=bar.getBoundingClientRect().bottom+24; let cur=null;
    parts.forEach(function(s){ const r=s.getBoundingClientRect(); if (r.top<=line && r.bottom>line) cur=s; });
    if (!cur){ bar.classList.remove('has-tab'); return; }
    const pl=cur.querySelector(':scope > .part'), num=((pl && pl.firstChild && pl.firstChild.textContent)||'').replace(/^\s*Part\s*/i,'').trim(), title=((cur.querySelector('h2')||{}).textContent||'').trim();
    if (tab.dataset.k!==cur.id){ tab.dataset.k=cur.id; tab.innerHTML='<b>Part '+num+'</b> · '+title; tab.href='#'+cur.id; tab.classList.remove('flip'); void tab.offsetWidth; tab.classList.add('flip'); }
    bar.classList.add('has-tab'); };
  addEventListener('scroll', function(){ if (!q) q=requestAnimationFrame(sync); bar.classList.add('scrolling'); clearTimeout(hideT); hideT=setTimeout(function(){ bar.classList.remove('scrolling'); }, 1400); }, {passive:true});
  sync();
})(); }catch(err){ psFail(err); }

/* ---------- Part I: say which stretch of the scroll is in view ---------- */
try{ (function(){
  const t=document.getElementById('tl'), rib=document.getElementById('tlRibbon'); if (!t || !rib) return;
  const out=document.createElement('p'); out.className='tl-range'; out.setAttribute('aria-live','off'); rib.insertAdjacentElement('afterend', out);
  let q=0; const read=function(){ q=0; const L=t.scrollLeft, R=L+t.clientWidth;
    const vis=[].slice.call(t.children).filter(function(li){ return !li.hidden && li.offsetLeft+li.offsetWidth*0.6>L && li.offsetLeft+li.offsetWidth*0.4<R; });
    if (!vis.length){ out.textContent=''; return; }
    const y=function(li){ return (li.querySelector('.yr')||{}).textContent||''; }, sealed=vis.filter(function(li){ return li.classList.contains('sealed'); }).length;
    out.innerHTML='In view: <b>'+y(vis[0])+'</b>'+(vis.length>1?' to <b>'+y(vis[vis.length-1])+'</b>':'')+(sealed?' · '+sealed+' sealed':''); };
  t.addEventListener('scroll', function(){ if (!q) q=requestAnimationFrame(read); }, {passive:true}); addEventListener('resize', function(){ if (!q) q=requestAnimationFrame(read); }, {passive:true});
  document.querySelectorAll('.tl-filters button').forEach(function(b){ b.addEventListener('click', function(){ setTimeout(read, 60); }); });
  read();
})(); }catch(err){ psFail(err); }

/* ---------- add Project Scroll to a phone's home screen, where the browser offers it ---------- */
try{ (function(){
  let ev=null; const foot=document.querySelector('footer.site'); if (!foot) return;
  addEventListener('beforeinstallprompt', function(e){ e.preventDefault(); ev=e;
    if (document.getElementById('installBtn')) return;
    const b=document.createElement('button'); b.type='button'; b.id='installBtn'; b.className='installbtn'; b.textContent='Add Project Scroll to your home screen';
    b.addEventListener('click', function(){ if (!ev) return; ev.prompt(); ev.userChoice.finally(function(){ ev=null; b.remove(); }); });
    const m=foot.querySelector('.motto'); (m||foot.firstElementChild||foot).insertAdjacentElement('afterend', b); });
  addEventListener('appinstalled', function(){ const b=document.getElementById('installBtn'); if (b) b.remove(); });
})(); }catch(err){ psFail(err); }

/* ---------- Part I: type a year and the scroll goes there ---------- */
try{ (function(){
  const t=document.getElementById('tl'), row=document.querySelector('.tl-eras'); if (!t || !row) return;
  const yearOf=function(li){ const y=(li.querySelector('.yr')||{}).textContent||''; if (/now/i.test(y)) return 99999; const n=parseInt(y.replace(/[^0-9]/g,''),10); return /BC/.test(y) ? -n : n; };
  const f=document.createElement('form'); f.className='tl-go'; f.setAttribute('aria-label','Go to a year on the scroll');
  f.innerHTML='<label><span>Go to a year</span><input type="number" inputmode="numeric" min="-12000" max="2100" placeholder="1846" aria-label="A year, for example 1846"></label><button type="submit">Go</button>';
  row.insertAdjacentElement('afterend', f);
  const inp=f.querySelector('input'), smooth=matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth';
  f.addEventListener('submit', function(e){ e.preventDefault(); const y=parseInt(inp.value,10); if (isNaN(y)) return;
    const lis=[].slice.call(t.children).filter(function(li){ return !li.hidden && !li.classList.contains('now'); }); if (!lis.length) return;
    let best=lis[0]; lis.forEach(function(li){ if (Math.abs(yearOf(li)-y)<Math.abs(yearOf(best)-y)) best=li; });
    t.scrollTo({left:Math.max(0,best.offsetLeft-(t.clientWidth-best.offsetWidth)/2), behavior:smooth}); best.classList.remove('lit'); void best.offsetWidth; best.classList.add('lit'); });
})(); }catch(err){ psFail(err); }

/* ---------- where the hunt began: the place names drift past ---------- */
try{ (function(){
  const box=document.querySelector('.placeband'), tr=document.getElementById('pbTrack'); if (!box || !tr) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches){ box.classList.add('still'); const v=box.querySelector('.pb-view'); if (v){ v.tabIndex=0; v.setAttribute('role','region'); v.setAttribute('aria-label','Places, scroll sideways'); } return; }
  [].slice.call(tr.children).forEach(function(li){ const c=li.cloneNode(true); c.setAttribute('aria-hidden','true'); c.querySelectorAll('a,button').forEach(function(a){ a.tabIndex=-1; }); tr.appendChild(c); });
  const speed=function(){ box.style.setProperty('--pbdur', Math.max(40, Math.round(tr.scrollWidth/2/38))+'s'); };
  speed(); addEventListener('resize', speed, {passive:true}); box.classList.add('run');
  const pz=document.createElement('button'); pz.type='button'; pz.className='pb-pause'; pz.setAttribute('aria-label','Pause the place names'); pz.setAttribute('aria-pressed','false'); pz.innerHTML='<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="4" y="3" width="2.6" height="10" rx=".8"/><rect x="9.4" y="3" width="2.6" height="10" rx=".8"/></svg>';
  pz.addEventListener('click', function(){ const on=!box.classList.contains('held'); box.classList.toggle('held', on); pz.setAttribute('aria-pressed', String(on)); pz.setAttribute('aria-label', on?'Play the place names':'Pause the place names'); pz.innerHTML=on?'<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M5 3l8 5-8 5z"/></svg>':'<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="4" y="3" width="2.6" height="10" rx=".8"/><rect x="9.4" y="3" width="2.6" height="10" rx=".8"/></svg>'; });
  box.appendChild(pz);
})(); }catch(err){ psFail(err); }

/* ---------- Part I: every date has its own link, so a date can be shared ---------- */
try{ (function(){
  const t=document.getElementById('tl'); if (!t) return;
  const slug=function(y){ return 'y-'+y.toLowerCase().replace(/c\.\s*/,'c').replace(/[^0-9a-z]+/g,''); };
  const smooth=matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth';
  [].slice.call(t.children).forEach(function(li){ const yr=li.querySelector('.yr'); if (!yr || li.classList.contains('now')) return;
    li.id=slug(yr.textContent);
    const b=document.createElement('button'); b.type='button'; b.className='tl-link'; b.setAttribute('aria-label','Copy a link to '+yr.textContent); b.title='Copy a link to this date';
    b.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>';
    b.addEventListener('click', function(e){ e.stopPropagation(); const url=location.origin+location.pathname+'#'+li.id;
      const done=function(){ b.classList.add('ok'); b.title='Link copied'; setTimeout(function(){ b.classList.remove('ok'); b.title='Copy a link to this date'; }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, function(){}); else done(); history.replaceState(null,'','#'+li.id); });
    yr.insertAdjacentElement('afterend', b); });
  const go=function(){ const id=location.hash.slice(1); if (!/^y-/.test(id)) return; const li=document.getElementById(id); if (!li) return;
    const sec=document.getElementById('timeline'); if (sec) sec.scrollIntoView({behavior:smooth, block:'start'});
    setTimeout(function(){ t.scrollTo({left:Math.max(0,li.offsetLeft-(t.clientWidth-li.offsetWidth)/2), behavior:smooth}); li.classList.remove('lit'); void li.offsetWidth; li.classList.add('lit'); }, 500); };
  addEventListener('hashchange', go); if (location.hash) setTimeout(go, 400);
})(); }catch(err){ psFail(err); }

/* ---------- what's new on the trail: a moving ticker ---------- */
try{ (function(){
  const tk=document.querySelector('.ticker'), track=document.getElementById('tkTrack'); if (!tk || !track) return;
  const items=[].slice.call(track.children), still=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const dt=function(li){ const t=li.querySelector('time'); return t ? t.getAttribute('datetime') : ''; };
  /* what has appeared since this visitor last looked */
  let seen=null; try{ seen=localStorage.getItem('ps-news-seen'); }catch(e){}
  const newest=items.map(dt).sort().pop(); let fresh=0;
  if (seen) items.forEach(function(li){ if (dt(li)>seen){ li.classList.add('fresh'); fresh++; } });
  const fr=document.getElementById('tkFresh'); if (fr && fresh){ fr.textContent=fresh+' new'; fr.title='New since your last visit'; fr.hidden=false; }
  if (newest) setTimeout(function(){ try{ localStorage.setItem('ps-news-seen', newest); }catch(e){} }, 6000);
  /* the full list, for reading at leisure */
  const list=document.getElementById('tkList'), all=document.getElementById('tkAll');
  if (list) items.forEach(function(li){ const c=li.cloneNode(true); list.appendChild(c); });
  if (all && list) all.addEventListener('click', function(){ const o=list.hidden; list.hidden=!o; all.setAttribute('aria-expanded', String(o)); all.textContent=o?'Close':'All news'; tk.classList.toggle('expanded', o); });
  if (still) { tk.classList.add('still'); return; }
  /* a second copy of the items makes the loop seamless; it is hidden from screen readers and the keyboard */
  items.forEach(function(li){ const c=li.cloneNode(true); c.setAttribute('aria-hidden','true'); c.querySelectorAll('a').forEach(function(a){ a.tabIndex=-1; }); track.appendChild(c); });
  const speed=function(){ tk.style.setProperty('--tkdur', Math.max(20, Math.round(track.scrollWidth/2/55))+'s'); };
  speed(); addEventListener('resize', speed, {passive:true}); tk.classList.add('run');
  const pb=document.getElementById('tkPause'); let paused=false; try{ paused=localStorage.getItem('ps-ticker')==='paused'; }catch(e){}
  const sync=function(){ tk.classList.toggle('paused', paused); if (pb){ pb.setAttribute('aria-pressed', String(paused)); pb.setAttribute('aria-label', paused?'Play the news':'Pause the news'); } };
  if (pb){ pb.hidden=false; pb.addEventListener('click', function(){ paused=!paused; try{ localStorage.setItem('ps-ticker', paused?'paused':'run'); }catch(e){} sync(); }); }
  sync();
})(); }catch(err){ psFail(err); }

/* ---------- the case board: "Pick one for me" ---------- */
try{ (function(){
  const box=document.querySelector('#cases .filters'); if (!box) return;
  const b=document.createElement('button'); b.type='button'; b.className='pickcase'; b.textContent='🎲 Pick one for me'; b.title='Pick an open case at random'; box.appendChild(b);
  let last=null;
  b.addEventListener('click', function(){
    const open=[].slice.call(document.querySelectorAll('#cases tr[id^="case-"]')).filter(function(tr){ return !tr.hidden && !tr.querySelector('.status.solved'); });
    if (!open.length) return; let tr; do { tr=open[Math.floor(Math.random()*open.length)]; } while (open.length>1 && tr===last); last=tr;
    tr.scrollIntoView({block:'center', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
    tr.classList.remove('picked'); void tr.offsetWidth; tr.classList.add('picked');
    const a=tr.querySelector('a, button'); if (a) setTimeout(function(){ a.focus({preventScroll:true}); }, 500);
  });
})(); }catch(err){ psFail(err); }

/* ---------- then and now: the hotel corner slider ---------- */
try{ (function(){ const f=document.getElementById('tnc'), r=document.getElementById('tncRange'); if (!f||!r) return;
  const set=function(){ f.style.setProperty('--x', r.value+'%'); }; r.addEventListener('input', set); set();
  /* the first time the corner scrolls into view, the slider sweeps once on its own to show what it does */
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
  let touched=false; ['pointerdown','keydown','input'].forEach(function(ev){ r.addEventListener(ev, function(){ touched=true; }, {once:true}); });
  const io=new IntersectionObserver(function(es){ if (!es[0].isIntersecting) return; io.disconnect();
    const keys=[[0,50],[900,92],[2000,8],[3000,50]], t0=performance.now();
    const step=function(now){ if (touched) return; const t=now-t0; let i=0; while (i<keys.length-2 && t>keys[i+1][0]) i++;
      const a=keys[i], b=keys[i+1], k=Math.min(1,(t-a[0])/(b[0]-a[0])), e=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;
      r.value=String(Math.round(a[1]+(b[1]-a[1])*e)); set(); if (t<keys[keys.length-1][0]) requestAnimationFrame(step); };
    setTimeout(function(){ requestAnimationFrame(step); }, 400); }, {threshold:.7});
  io.observe(f); })(); }catch(err){ psFail(err); }

/* ---------- the trail map: a soft horn note when a lit hall is tapped ---------- */
try{ (function(){
  const halls=document.querySelectorAll('.trailmap .tm-hall'); if (!halls.length) return; let ac=null;
  const tmap=document.querySelector('.trailmap');
  if (tmap && 'IntersectionObserver' in window) new IntersectionObserver(function(es){ tmap.classList.toggle('inview', es[0].isIntersecting); }).observe(tmap); else if (tmap) tmap.classList.add('inview');
  const horn=function(){
    try{ ac=ac||new (window.AudioContext||window.webkitAudioContext)(); const t=ac.currentTime, g=ac.createGain(), lp=ac.createBiquadFilter();
      lp.type='lowpass'; lp.frequency.setValueAtTime(900,t); lp.frequency.linearRampToValueAtTime(1600,t+.25); lp.frequency.linearRampToValueAtTime(700,t+1.1);
      g.gain.setValueAtTime(0,t); g.gain.linearRampToValueAtTime(.12,t+.08); g.gain.setValueAtTime(.12,t+.7); g.gain.exponentialRampToValueAtTime(.0001,t+1.25);
      [1,1.5].forEach(function(m,k){ const o=ac.createOscillator(); o.type='sawtooth'; o.frequency.setValueAtTime(174*m,t); o.frequency.linearRampToValueAtTime(196*m,t+.18); o.connect(lp); o.start(t+(k?.03:0)); o.stop(t+1.3); });
      lp.connect(g); g.connect(ac.destination); }catch(e){}
  };
  halls.forEach(function(h){ h.setAttribute('tabindex','0'); h.setAttribute('role','button'); h.setAttribute('aria-label', (h.querySelector('.tm-name')||{}).textContent+': sound the horn');
    const go=function(){ horn(); h.classList.add('blow'); setTimeout(function(){ h.classList.remove('blow'); }, 900); };
    h.addEventListener('click', go); h.addEventListener('keydown', function(e){ if (e.key==='Enter'||e.key===' '){ e.preventDefault(); go(); } }); });
})(); }catch(err){ psFail(err); }

/* ---------- unsealing: a date that opens cracks its wax seal the first time a visitor sees it ---------- */
try{ (function(){
  const lis=document.querySelectorAll('#tl > li.unsealed'); if (!lis.length || !('IntersectionObserver' in window)) return;
  const io=new IntersectionObserver(function(es){ es.forEach(function(e){ if (!e.isIntersecting) return; io.unobserve(e.target);
    const k='ps-unsealed-'+(e.target.dataset.year||''); let seen=false; try{ seen=!!localStorage.getItem(k); localStorage.setItem(k,'1'); }catch(x){}
    if (!seen && !matchMedia('(prefers-reduced-motion: reduce)').matches) e.target.classList.add('cracking'); }); }, {threshold:.6});
  lis.forEach(function(li){ io.observe(li); });
})(); }catch(err){ psFail(err); }

/* ---------- the margins change with the season: maple and oak leaves, snow, petals, fireflies ---------- */
try{ (function(){
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || matchMedia('(prefers-reduced-data: reduce)').matches || innerWidth<1000 || !document.querySelector('.sheet')) return;
  const m=new Date().getMonth(), kind= (m===8||m===9||m===10)?'leaf' : (m===11||m===0||m===1)?'snow' : (m===3||m===4)?'petal' : (m>=5&&m<=7)?'fly' : null; if (!kind) return;
  const cv=document.createElement('canvas'); cv.className='season'; cv.setAttribute('aria-hidden','true'); document.body.appendChild(cv);
  const x=cv.getContext('2d'); const dpr=Math.min(2, window.devicePixelRatio||1); let W,H,rt=0;
  const fit=function(){ W=innerWidth; H=innerHeight; cv.width=W*dpr; cv.height=H*dpr; cv.style.width=W+'px'; cv.style.height=H+'px'; x.setTransform(dpr,0,0,dpr,0,0); };
  fit(); addEventListener('resize', function(){ clearTimeout(rt); rt=setTimeout(fit,150); }, {passive:true});
  /* leaf outlines on a 100-unit square, stem pointing down */
  const SHAPES={
    maple:'M50 3 L57 21 L66 15 L64 35 L80 23 L78 31 L96 30 L86 44 L94 50 L72 62 L76 72 L56 66 L52 70 L51 97 L49 97 L48 70 L44 66 L24 72 L28 62 L6 50 L14 44 L4 30 L22 31 L20 23 L36 35 L34 15 L43 21 Z',
    oak:'M50 4 C58 4 60 12 55 17 C64 12 74 18 66 27 L57 30 C70 26 84 36 70 44 L58 46 C74 46 84 58 68 60 L57 61 C68 64 70 76 58 74 C60 80 56 86 51 84 L51 97 L49 97 L49 84 C44 86 40 80 42 74 C30 76 32 64 43 61 L32 60 C16 58 26 46 42 46 L30 44 C16 36 30 26 43 30 L34 27 C26 18 36 12 45 17 C40 12 42 4 50 4 Z'
  };
  const VEINS={
    maple:'M50 97 L50 12 M50 60 L18 34 M50 60 L82 34 M50 64 L22 58 M50 64 L78 58',
    oak:'M50 96 L50 8 M50 24 L64 20 M50 24 L36 20 M50 38 L72 37 M50 38 L28 37 M50 53 L72 53 M50 53 L28 53 M50 67 L63 69 M50 67 L37 69'
  };
  const COLORS= kind==='leaf'?['#c8452a','#d97a1f','#b3362b','#e0a52e','#9c4a22','#cf6a2c'] : kind==='petal'?['#f2d3dc','#f7e6ea','#e8bfcb'] : ['#ffffff'];
  /* each leaf is drawn once into a small picture, then stamped every frame: cheap to animate */
  const sprite=function(shape,col){
    const S=64, c=document.createElement('canvas'); c.width=c.height=S*dpr; const g=c.getContext('2d'); g.scale(S*dpr/100,S*dpr/100);
    const body=new Path2D(SHAPES[shape]);
    const gr=g.createLinearGradient(0,0,100,100); gr.addColorStop(0,col); gr.addColorStop(1,'rgba(60,25,10,.55)');
    g.fillStyle=col; g.fill(body); g.globalCompositeOperation='source-atop'; g.globalAlpha=.35; g.fillStyle=gr; g.fillRect(0,0,100,100);
    g.globalCompositeOperation='source-over'; g.globalAlpha=1;
    g.strokeStyle='rgba(70,30,10,.45)'; g.lineWidth=1.4; g.stroke(body);
    g.strokeStyle='rgba(60,25,10,.55)'; g.lineWidth=1.6; g.lineCap='round'; g.stroke(new Path2D(VEINS[shape]));
    return c;
  };
  const SPR=[]; if (kind==='leaf') COLORS.forEach(function(col){ SPR.push(sprite('maple',col)); SPR.push(sprite('oak',col)); });
  const N= kind==='snow'?60 : kind==='fly'?22 : kind==='leaf'?18 : 26, P=[];
  const add=function(init){ P.push({x:Math.random()*W, y:init?Math.random()*H:-40,
    s:kind==='snow'?1+Math.random()*2.2 : kind==='fly'?1.6 : kind==='leaf'?24+Math.random()*18 : 5+Math.random()*5,
    vy:kind==='snow'?.3+Math.random()*.6 : kind==='fly'?0 : .45+Math.random()*.6,
    ph:Math.random()*6.28, sw:.6+Math.random()*1.2, c:COLORS[Math.floor(Math.random()*COLORS.length)],
    img:SPR.length?SPR[Math.floor(Math.random()*SPR.length)]:null, r:Math.random()*6.28, vr:(Math.random()-.5)*.02, tp:Math.random()*6.28, vt:.015+Math.random()*.03}); };
  for (let i=0;i<N;i++) add(true);
  /* moving the pointer through the margins stirs the leaves near it, like a breath of wind */
  let gx=-999, gy=-999, gvx=0;
  if (kind!=='fly') addEventListener('pointermove', function(e){ if (e.pointerType!=='mouse') return; gvx=Math.max(-12,Math.min(12,e.clientX-gx)); gx=e.clientX; gy=e.clientY; }, {passive:true});
  let raf=0, last=0, idleAt=performance.now()+15000;
  /* about 30 frames a second, and the leaves rest after fifteen seconds without a scroll or a pointer move */
  const loop=function(t){ raf=0; if (t>idleAt || document.hidden) return; if (t-last>=33){ last=t; tick(t); } raf=requestAnimationFrame(loop); };
  const wake=function(){ idleAt=performance.now()+15000; if (!raf && !document.hidden) raf=requestAnimationFrame(loop); };
  addEventListener('scroll', wake, {passive:true}); addEventListener('pointermove', wake, {passive:true});
  document.addEventListener('visibilitychange', function(){ cancelAnimationFrame(raf); raf=0; if (!document.hidden) wake(); });
  const tick=function(t){
    x.clearRect(0,0,W,H);
    gvx*=.9;
    P.forEach(function(p){
      p.ph+=.01;
      if (kind==='fly'){ p.x+=Math.cos(p.ph*1.3)*.4; p.y+=Math.sin(p.ph)*.3; }
      else { const dx=p.x-gx, dy=p.y-gy, d2=dx*dx+dy*dy; if (d2<6400){ const f=1-d2/6400; p.wx=(p.wx||0)+gvx*.05*f; p.wy=(p.wy||0)-1.2*f; p.vt+=.002*f; }
        p.wx=(p.wx||0)*.96; p.wy=(p.wy||0)*.94; p.vt=Math.max(.015,Math.min(.12,p.vt*.995));
        p.y+=p.vy+p.wy; p.x+=Math.sin(p.ph*p.sw)*.7+p.wx; p.r+=p.vr+Math.sin(p.ph*2)*.004+p.wx*.004; p.tp+=p.vt; }
      if (p.y>H+40){ p.y=-40; p.x=Math.random()*W; } if (p.y<-60) p.y=-60; if (p.x<-60) p.x=W+40; else if (p.x>W+60) p.x=-40;
      x.save(); x.translate(p.x,p.y); x.rotate(p.r);
      if (kind==='snow'){ x.globalAlpha=.75; x.fillStyle='#fff'; x.beginPath(); x.arc(0,0,p.s,0,6.28); x.fill(); }
      else if (kind==='fly'){ x.globalAlpha=.35+.35*Math.sin(t/400+p.ph*5); x.fillStyle='#fff3a6'; x.shadowColor='#ffe066'; x.shadowBlur=10; x.beginPath(); x.arc(0,0,p.s,0,6.28); x.fill(); }
      else if (p.img){ const flip=Math.cos(p.tp); x.scale(Math.abs(flip)<.12?.12*Math.sign(flip||1):flip,1); x.globalAlpha=.88; x.drawImage(p.img,-p.s/2,-p.s/2,p.s,p.s); }
      else { x.globalAlpha=.8; x.fillStyle=p.c; x.beginPath(); x.ellipse(0,0,p.s,p.s*.55,0,0,6.28); x.fill(); }
      x.restore();
    });
  };
  raf=requestAnimationFrame(loop);
})(); }catch(err){ psFail(err); }

  /* ---------- case pages: the live Facebook post, loaded only when asked ---------- */
  try{ (function(){
    document.querySelectorAll('.fp-live[data-post]').forEach(function(box){
      const btn=box.querySelector('button'); if (!btn) return;
      btn.addEventListener('click', function(){
        const url=box.dataset.post, w=Math.min(750, Math.max(350, box.clientWidth-2));
        const dark=(document.documentElement.dataset.theme||'')==='dark' || (!document.documentElement.dataset.theme && matchMedia('(prefers-color-scheme: dark)').matches);
        const f=document.createElement('iframe'); f.className='fp-frame'; f.title='The post on Facebook';
        f.src='https://www.facebook.com/plugins/post.php?href='+encodeURIComponent(url)+'&show_text=true&width='+w+(dark?'&theme=dark':'');
        f.width=String(w); f.height='720'; f.style.border='0'; f.setAttribute('referrerpolicy','strict-origin'); f.setAttribute('allowfullscreen','true'); f.setAttribute('loading','lazy');
        f.setAttribute('allow','autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share');
        box.innerHTML=''; box.appendChild(f); box.classList.add('loaded');
        const n=document.createElement('p'); n.className='note'; n.innerHTML='Shown by Facebook. If it stays blank, <a href="'+url+'">open the post there</a>.'; box.appendChild(n);
      });
    });
  })(); }catch(err){ psFail(err); }

  /* ---------- case pages: tap a page image to see it large ---------- */
  try{ (function(){
    const imgs=document.querySelectorAll('.fp-pics img'); if (!imgs.length) return;
    imgs.forEach(function(img){ img.tabIndex=0; img.setAttribute('role','button'); img.setAttribute('aria-label','Enlarge: '+img.alt);
      const open=function(){ const z=document.createElement(window.HTMLDialogElement?'dialog':'div'); z.className='fp-zoom'; if (z.tagName!=='DIALOG') z.setAttribute('role','dialog'); z.setAttribute('aria-label',img.alt);
        const big=document.createElement('img'); big.alt=img.alt; big.src=img.currentSrc.replace('-700.','-1200.').replace('-640.','.').replace('-1000.','.'); big.onerror=function(){ big.src=img.currentSrc; };
        const x=document.createElement('button'); x.type='button'; x.className='fp-x'; x.setAttribute('aria-label','Close'); x.textContent='×';
        z.appendChild(big); z.appendChild(x); document.body.appendChild(z); document.body.style.overflow='hidden';
        const close=function(){ if (z.open && z.close) z.close(); z.remove(); document.body.style.overflow=''; img.focus({preventScroll:true}); document.removeEventListener('keydown', esc); };
        const esc=function(e){ if (e.key==='Escape'){ e.preventDefault(); close(); } };
        z.addEventListener('click', close); z.addEventListener('cancel', function(e){ e.preventDefault(); close(); }); document.addEventListener('keydown', esc);
        if (z.showModal) z.showModal(); x.focus(); };
      img.addEventListener('click', open); img.addEventListener('keydown', function(e){ if (e.key==='Enter' || e.key===' '){ e.preventDefault(); open(); } }); });
  })(); }catch(err){ psFail(err); }

  /* ---------- the case board: your own progress on this device ---------- */
  try{ (function(){
    const tally=document.querySelector('#cases .tally'); if (!tally) return;
    let mine=[], notes=0; try{ mine=JSON.parse(localStorage.getItem('ps-mine')||'[]')||[]; for (let i=0;i<localStorage.length;i++){ const k=localStorage.key(i); if (/^ps-note-/.test(k) && (localStorage.getItem(k)||'').trim()) notes++; } }catch(e){ return; }
    if (!mine.length && !notes) return;
    const p=document.createElement('p'); p.className='mytally';
    p.textContent='On this device: following '+mine.length+(mine.length===1?' case':' cases')+(notes?', with notes on '+notes:'')+'.';
    tally.insertAdjacentElement('afterend', p);
  })(); }catch(err){ psFail(err); }

  /* ---------- Part I: the tally counts up when it comes into view ---------- */
  try{ (function(){
    const tally=document.getElementById('tlTally'); if (!tally || !('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const bs=[].slice.call(tally.querySelectorAll('b')); let done=false;
    new IntersectionObserver(function(es, io){ if (done || !es[0].isIntersecting) return; done=true; io.disconnect();
      bs.forEach(function(b){ const to=parseInt(b.textContent,10)||0, t0=performance.now(), d=900;
        const step=function(now){ const k=Math.min(1,(now-t0)/d), e=1-Math.pow(1-k,3); b.textContent=Math.round(to*e); if (k<1) requestAnimationFrame(step); };
        b.textContent='0'; requestAnimationFrame(step); }); }, {threshold:.6}).observe(tally);
  })(); }catch(err){ psFail(err); }

  /* ---------- the advertisement: share it with someone who needs it ---------- */
  try{ (function(){
    const box=document.querySelector('.promo.ad .ad-coupon'); if (!box) return;
    const p=document.createElement('p'); p.className='ad-share';
    const b=document.createElement('button'); b.type='button'; b.className='linkbtn'; b.textContent='Know someone who needs this? Share it ›'; p.appendChild(b); box.appendChild(p);
    const url=location.origin+'/services/', text='Project Scroll: research, imaging, design, 3D and film. Serving the St. Joseph River Valley and anywhere the records reach.';
    b.addEventListener('click', function(){
      if (navigator.share){ navigator.share({title:'Project Scroll · Professional services', text:text, url:url}).catch(function(){}); return; }
      const ok=function(){ b.textContent='Link copied. Paste it anywhere.'; setTimeout(function(){ b.textContent='Know someone who needs this? Share it ›'; }, 2400); };
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(ok, function(){}); });
  })(); }catch(err){ psFail(err); }

  /* ---------- the visit counter (Meta Pixel), off until the visitor says yes ---------- */
  try{ (function(){
    const PIXEL='3323345988054026', KEY='ps-consent';
    let state=null; try{ state=localStorage.getItem(KEY); }catch(e){}
    let loaded=false;
    function load(){
      if (loaded || typeof window.fbq==='function') return; loaded=true;
      !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
      fbq('init', PIXEL); fbq('track', 'PageView');
      const svc=document.getElementById('services');
      if (svc && 'IntersectionObserver' in window){ const io=new IntersectionObserver(function(es){ if (es.some(function(e){ return e.isIntersecting; })){ fbq('track','ViewContent',{content_name:'Professional services'}); io.disconnect(); } },{threshold:.4}); io.observe(svc); }
      document.addEventListener('click', function(ev){ const a=ev.target.closest && ev.target.closest('a[href^="https://m.me/"]'); if (a) fbq('track','Lead',{content_name:'Messenger'}); }, true);
    }
    function set(v){ state=v; try{ localStorage.setItem(KEY, v); }catch(e){} document.dispatchEvent(new CustomEvent('ps-consent',{detail:v})); if (v==='yes') load(); }
    window.psConsent=function(v){ if (v===undefined) return state; set(v); };
    if (state==='yes') load();
    /* the privacy page's own switch */
    const box=document.getElementById('consentbox');
    if (box){ const st=document.getElementById('consentState');
      const show=function(){ st.textContent = state==='yes' ? 'allowed' : state==='no' ? 'kept off' : 'not made yet (the counter is off)'; };
      show(); document.getElementById('consentYes').addEventListener('click', function(){ set('yes'); show(); });
      document.getElementById('consentNo').addEventListener('click', function(){ set('no'); show(); });
      document.addEventListener('ps-consent', show); }
    /* first-visit question, not on the privacy page itself */
    if (state===null && !box && !matchMedia('print').matches){
      const d=document.createElement('div'); d.className='consent'; d.setAttribute('role','region'); d.setAttribute('aria-label','Visit counter');
      d.innerHTML='<p>May we count your visit? A small Meta script would tell us which pages are read. Nothing you type is seen, and nothing loads until you say yes. <a href="/privacy/">What it does</a></p><p class="cbtns"><button type="button" class="btn primary" id="cYes">Allow</button><button type="button" class="btn" id="cNo">No thanks</button></p>';
      document.body.appendChild(d); requestAnimationFrame(function(){ requestAnimationFrame(function(){ d.classList.add('on'); }); });
      const go=function(v){ return function(){ set(v); d.classList.remove('on'); setTimeout(function(){ d.remove(); }, 400); }; };
      d.querySelector('#cYes').addEventListener('click', go('yes')); d.querySelector('#cNo').addEventListener('click', go('no'));
    }
  })(); }catch(err){ psFail(err); }

  try{ const kp=document.getElementById('keepPrint'); if (kp) kp.addEventListener('click', function(){ print(); }); }catch(e){}

  try{
    console.log('%cProject Scroll','font:28px Georgia,serif;color:#B3362B');
    console.log('%cYou found a back door. Every page has another side: view the page source, and read the note at the top.','font:14px Georgia,serif');
  }catch(e){}
})();

/* ---------- Draft 102: any then-and-now frame beyond the hotel corner, and the find-the-families challenge ---------- */
try{ (function(){ [].forEach.call(document.querySelectorAll('.tn2-frame'), function(f){ const r=f.querySelector('.tnc-range'); if (!r) return; const set=function(){ f.style.setProperty('--x', r.value+'%'); }; r.addEventListener('input', set); set();
    const old=f.querySelector('.tnc-old img'); if (old){ const fail=function(){ f.classList.add('tn-off'); r.disabled=true; const c=f.parentNode.querySelector('figcaption'); if (c && !c.querySelector('.tn-msg')){ const m=document.createElement('span'); m.className='tn-msg'; m.textContent=' The 1860 half comes from the Library of Congress, which did not answer just now; try again in a minute.'; c.insertBefore(m, c.querySelector('.credit')); } }; if (old.complete && old.naturalWidth===0 && old.currentSrc) fail(); else old.addEventListener('error', fail, {once:true}); } }); })(); }catch(err){ psFail(err); }
try{ (function(){
  /* every "find the names" box on the site: data-h holds the hashed answers, data-k the place it remembers, data-done the line it ends on */
  const h=function(s){ let x=5381; for (let i=0;i<s.length;i++){ x=((Math.imul(x,33))^s.charCodeAt(i))>>>0; } return x; };
  [].forEach.call(document.querySelectorAll('.namehunt[data-h]'), function(box){
    const form=box.querySelector('form'), inp=box.querySelector('input'), out=box.querySelector('.nh-out'), list=box.querySelector('.nh-found');
    const H=box.dataset.h.split(',').map(Number), key=box.dataset.k, total=H.length, word=box.dataset.word||'family', words=box.dataset.words||'families';
    let got=[]; try{ got=JSON.parse(localStorage.getItem(key)||'[]'); }catch(e){}
    const tally=function(){ return got.length+' of '+total+' found.'; };
    const draw=function(){ if (list){ list.innerHTML=''; got.forEach(function(n){ const li=document.createElement('li'); li.textContent=n; list.appendChild(li); }); } if (got.length) out.textContent=got.length===total?(box.dataset.done||'All found.'):tally(); };
    draw();
    form.addEventListener('submit', function(e){ e.preventDefault(); const raw=inp.value.trim(); let n=raw.toLowerCase().replace(/m\.?\s*d\.?$/,'').trim().split(/[\s.]+/).filter(Boolean).pop()||''; n=n.replace(/[^a-z]/g,''); if (!n) return;
      if (H.indexOf(h(n))<0 && n.length>3 && n.slice(-1)==='s' && H.indexOf(h(n.slice(0,-1)))>=0) n=n.slice(0,-1);
      const nice=n.charAt(0).toUpperCase()+n.slice(1);
      if (got.map(function(x){ return x.toLowerCase(); }).indexOf(n)>=0) out.textContent=(got.length===total && total===1)?(box.dataset.done||'Found.'):nice+' is already in your list. '+tally();
      else if (H.indexOf(h(n))>=0){ got.push(nice); try{ localStorage.setItem(key, JSON.stringify(got)); }catch(e){} draw(); if (got.length<total) out.textContent=(box.dataset.yes||'{n}: on both maps.').replace('{n}',nice)+' '+tally(); }
      else out.textContent=box.dataset.no||'Not one we matched. Check the spelling on both maps, or tell us if you think we missed one.';
      inp.value=''; inp.focus(); });
  });
})(); }catch(err){ psFail(err); }

/* ---------- Draft 103: a glint on each part's diamond, at its own moment; the footer trail draws itself when it comes into view ---------- */
try{ (function(){
  [].forEach.call(document.querySelectorAll('main > section + section, main > .plate2 + section'), function(s,i){ const g=document.createElement('i'); g.className='gemglint'; g.setAttribute('aria-hidden','true'); g.style.setProperty('--gd', (i*1.7%7).toFixed(1)+'s'); s.appendChild(g); });
  const t=document.querySelector('.trailx'); if (!t) return;
  if (!('IntersectionObserver' in window)){ t.classList.add('drawn'); return; }
  const io=new IntersectionObserver(function(es){ if (es[0].isIntersecting){ t.classList.add('drawn'); io.disconnect(); } }, {threshold:.6}); io.observe(t);
})(); }catch(err){ psFail(err); }

/* ---------- Draft 105: pause all motion (remembered), a note in the plate viewer, pan for a case, and the gold vein ---------- */
try{ (function(){
  const b=document.getElementById('calm'), H=document.documentElement;
  let on=false; try{ on=localStorage.getItem('ps-calm')==='1'; }catch(e){}
  const sync=function(){ H.classList.toggle('calm', on); if (b){ b.setAttribute('aria-pressed', String(on)); b.querySelector('span').textContent=on?'Let it move again':'Pause all motion'; } };
  sync(); if (b) b.addEventListener('click', function(){ on=!on; try{ localStorage.setItem('ps-calm', on?'1':'0'); }catch(e){} sync(); });
})(); }catch(err){ psFail(err); }
try{ (function(){
  /* the plate viewer says plainly which plates are record and which are illustration */
  const fb=document.querySelector('.mh-full'); if (!fb) return;
  fb.addEventListener('click', function(){ setTimeout(function(){ const d=document.getElementById('plateDlg'); if (!d || d.querySelector('.pd-note')) return; const n=document.createElement('p'); n.className='pd-note'; n.textContent='The plates mix the record with modern illustration. A caption that names a book, map, postcard or print is the record itself; the rest are artwork made to set the scene.'; d.insertBefore(n, d.querySelector('.pd-nav')); }, 0); });
})(); }catch(err){ psFail(err); }
try{ (function(){
  /* "Pick one for me" becomes a gold pan: give it a shake and a case settles out */
  const b=document.querySelector('.pickcase'); if (!b) return;
  b.innerHTML='<svg class="pan" viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="12" cy="13" rx="10" ry="5.2"/><ellipse cx="12" cy="12.2" rx="6.6" ry="3" class="pan-in"/><circle cx="10.4" cy="12" r=".9" class="nug"/><circle cx="13.6" cy="12.6" r=".7" class="nug"/><circle cx="12.4" cy="11.3" r=".55" class="nug"/></svg><span>Pan for a case</span>';
  b.title='Shake the pan: an open case settles out at random';
  b.addEventListener('click', function(){ b.classList.remove('panning'); void b.offsetWidth; b.classList.add('panning'); });
})(); }catch(err){ psFail(err); }
try{ (function(){
  /* the gold vein: a nugget on the reading thread for each part; it catches the light as you pass it */
  const parts=[].slice.call(document.querySelectorAll('main > section[id]')); if (parts.length<3 || !document.querySelector('.vprogress')) return;
  const vein=document.createElement('div'); vein.className='vein'; vein.setAttribute('aria-hidden','true'); document.body.appendChild(vein);
  const ns=parts.map(function(){ const i=document.createElement('i'); vein.appendChild(i); return i; });
  const place=function(){ const H=document.documentElement.scrollHeight-innerHeight; if (H<=0) return; parts.forEach(function(s,k){ const y=Math.min(1, Math.max(0, (s.getBoundingClientRect().top+scrollY-innerHeight*.35)/H)); ns[k].style.top=(y*100)+'%'; ns[k].dataset.y=y; }); hit(); };
  const hit=function(){ const H=document.documentElement.scrollHeight-innerHeight; const p=H>0?scrollY/H:0; ns.forEach(function(n){ n.classList.toggle('hit', p>=parseFloat(n.dataset.y||2)-.002); }); };
  let raf=0; addEventListener('scroll', function(){ if (!raf) raf=requestAnimationFrame(function(){ raf=0; hit(); }); }, {passive:true});
  addEventListener('resize', place, {passive:true}); addEventListener('load', place); setTimeout(place, 1500); place();
})(); }catch(err){ psFail(err); }
