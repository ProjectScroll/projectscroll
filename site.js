(function(){
  "use strict";
  let root=document.documentElement, btn=document.getElementById('theme');
  function themeNow(){ return root.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'); }
  function label(){ btn.textContent = themeNow()==='dark' ? 'Light' : 'Dark'; }
  label();
  btn.addEventListener('click', function(){
    let next = themeNow()==='dark' ? 'light' : 'dark';
    let apply = function(){ root.dataset.theme=next; try{localStorage.setItem('ps-theme',next);}catch(e){} label(); };
    if (document.startViewTransition && document.visibilityState==='visible' && !matchMedia('(prefers-reduced-motion: reduce)').matches){ let done=false; const go=function(){ if (!done){ done=true; apply(); } }; try{ document.startViewTransition(go); }catch(e){ go(); } setTimeout(go, 350); } else apply();
  });

  /* mobile menu */
  let menu=document.getElementById('menu'), bar=document.querySelector('.bar');
  if (menu && bar){
    menu.addEventListener('click', function(){ let o=bar.classList.toggle('open'); menu.setAttribute('aria-expanded', o?'true':'false'); menu.textContent=o?'Close':'Menu'; });
    bar.querySelectorAll('nav a').forEach(function(a){ a.addEventListener('click', function(){ bar.classList.remove('open'); menu.setAttribute('aria-expanded','false'); menu.textContent='Menu'; }); });
  }

  /* the asterisk leads to its footnote */
  let star=document.getElementById('star'), foot=document.getElementById('foot');
  if (star && foot) star.addEventListener('click', function(){
    foot.scrollIntoView({block:'center'}); foot.classList.add('lit');
    setTimeout(function(){ foot.classList.remove('lit'); }, 1600);
  });


  /* the message builder: fill in, copy, paste into Facebook (kept only in this browser as a draft) */
  let form=document.getElementById('msgform');
  if (form){
    let DK='ps-msg', fields=[].slice.call(form.querySelectorAll('input,textarea')), out=document.getElementById('copied');
    try{ let d=JSON.parse(localStorage.getItem(DK)||'{}'); fields.forEach(function(f){ if (d[f.name]) f.value=d[f.name]; }); }catch(e){}
    let store=function(){ let d={}; fields.forEach(function(f){ d[f.name]=f.value; }); try{ localStorage.setItem(DK, JSON.stringify(d)); }catch(e){} };
    fields.forEach(function(f){ f.addEventListener('input', store); });
    document.getElementById('copy').addEventListener('click', function(){
      let lines=fields.map(function(f){ return f.closest('label').querySelector('span').textContent+': '+f.value.trim(); });
      let txt='Hello Project Scroll,\n\n'+lines.join('\n');
      let done=function(){ const om=document.getElementById('openMsgr'); if (om) om.hidden=false; out.textContent='Copied. Now open Messenger and paste it.'; setTimeout(function(){ out.textContent=''; },5000); };
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, function(){ out.textContent='Your browser blocked copying. Select the text and copy it by hand.'; });
      else out.textContent='Your browser blocked copying. Select the text and copy it by hand.';
    });
    document.getElementById('clearmsg').addEventListener('click', function(){ fields.forEach(function(f){ f.value=''; }); store(); out.textContent='Cleared.'; setTimeout(function(){ out.textContent=''; },2000); });
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
      document.querySelectorAll('.filters button').forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.f===f?'true':'false'); });
    }
    document.querySelectorAll('.filters button').forEach(function(b){ b.addEventListener('click', function(){ filter(b.dataset.f); }); });
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
    const cl=document.getElementById('clueLink'); cl.href='#case-'+cur[3]; cl.textContent='It’s case '+cur[3]+' on the board';
  }catch(e){} }

  /* 14 works offline after a first visit */
  if ('serviceWorker' in navigator && (location.protocol==='https:' || location.hostname==='localhost')){ addEventListener('load', function(){ navigator.serviceWorker.register('/sw.js').catch(function(){}); }); }

  /* glossary: the first use of each term on the page gets a short definition */
  const GL={
    'plat':['Plat','A surveyor’s drawing of land divided into lots or parcels, with streets and boundaries. Village plats were filed with the county.'],
    'probate':['Probate','The court process that settles a dead person’s estate. Probate files can hold wills, inventories, heirs’ names and signatures.'],
    'informant':['Informant','The person who answered the questions on a certificate. Their memory, not the dead person’s, is what the form records.'],
    'county histories':['County histories','Thick volumes published from the 1870s to the 1910s, mostly from what local families supplied. Rich, but rarely checked.'],
    'field notes':['Field notes','The notebooks surveyors kept as they walked the land: distances, trees, streams and what they saw, line by line.'],
    'census':['Census','The national head-count taken every ten years. Old schedules list every person in a household, with ages and birthplaces.'],
    'transcription':['Transcription','A typed copy of an old handwritten record. Useful, but every copy can add mistakes, so check the original when you can.']
  };
  const host=document.querySelector('main'); let gi=0;
  if (host && 'showPopover' in HTMLElement.prototype){
    const used={};
    const walker=document.createTreeWalker(host, NodeFilter.SHOW_TEXT, {acceptNode:function(n){
      const p=n.parentElement; if (!p || p.closest('h1,h2,h3,button,a,summary,.mk,label,script,style,.gl,.tl .yr,.mstrip,.promo-marks,figcaption,[popover]')) return NodeFilter.FILTER_REJECT; return NodeFilter.FILTER_ACCEPT; }});
    const nodes=[]; while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function(n){
      Object.keys(GL).forEach(function(term){
        if (used[term] || !n.parentNode) return;
        const re=new RegExp('\\b('+term+')\\b','i'), m=n.nodeValue.match(re); if (!m) return;
        used[term]=true; gi++;
        const id='gl'+gi, after=n.splitText(m.index); after.nodeValue=after.nodeValue.slice(m[0].length);
        const b=document.createElement('button'); b.type='button'; b.className='gl'; b.textContent=m[0]; b.setAttribute('popovertarget',id); b.setAttribute('aria-label',m[0]+': what this means');
        const pop=document.createElement('div'); pop.id=id; pop.setAttribute('popover',''); pop.className='gloss'; pop.innerHTML='<b></b>'; pop.querySelector('b').textContent=GL[term][0]; pop.appendChild(document.createTextNode(GL[term][1]));
        n.parentNode.insertBefore(b, after); document.body.appendChild(pop);
        pop.addEventListener('toggle', function(e){ if (e.newState==='open'){ const r=b.getBoundingClientRect(), w=pop.offsetWidth; pop.style.left=Math.max(8,Math.min(innerWidth-w-8, r.left+r.width/2-w/2))+'px'; const below=r.bottom+8; pop.style.top=(below+pop.offsetHeight>innerHeight? r.top-pop.offsetHeight-8 : below)+'px'; } });
      });
    });
  }

  /* read aloud: each section can be read out by the device's own voice */
  if ('speechSynthesis' in window){
    let speaking=null;
    const stop=function(){ speechSynthesis.cancel(); if (speaking){ speaking.setAttribute('aria-pressed','false'); speaking.textContent='Listen'; } speaking=null; };
    document.querySelectorAll('main > section > .part, main.page > .kicker').forEach(function(part){
      const sec=part.closest('section') || part.closest('main');
      const b=document.createElement('button'); b.type='button'; b.className='listen'; b.textContent='Listen'; b.setAttribute('aria-pressed','false'); b.setAttribute('aria-label','Read this section aloud');
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

  /* for anyone who opens the browser's console */
  try{
    console.log('%cProject Scroll','font:28px Georgia,serif;color:#B3362B');
    console.log('%cYou found a back door. Every page has another side: view the page source, and read the note at the top.','font:14px Georgia,serif');
  }catch(e){}
})();
