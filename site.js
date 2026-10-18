(function(){
  "use strict";
  let root=document.documentElement, btn=document.getElementById('theme');
  function themeNow(){ return root.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'); }
  function label(){ btn.textContent = themeNow()==='dark' ? 'Light' : 'Dark'; }
  label();
  btn.addEventListener('click', function(){
    let next = themeNow()==='dark' ? 'light' : 'dark';
    let apply = function(){ root.dataset.theme=next; try{localStorage.setItem('ps-theme',next);}catch(e){} label(); };
    if (document.startViewTransition && !matchMedia('(prefers-reduced-motion: reduce)').matches) document.startViewTransition(apply); else apply();
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
      let done=function(){ out.textContent='Copied. Now paste it into your message to Project Scroll on Facebook.'; setTimeout(function(){ out.textContent=''; },5000); };
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

  /* for anyone who opens the browser's console */
  try{
    console.log('%cProject Scroll','font:28px Georgia,serif;color:#B3362B');
    console.log('%cYou found a back door. Every page has another side: view the page source, and read the note at the top.','font:14px Georgia,serif');
  }catch(e){}
})();
