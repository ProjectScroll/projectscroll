(function(){
  var root=document.documentElement, btn=document.getElementById('theme');
  function current(){ return root.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'); }
  function label(){ btn.textContent = current()==='dark' ? 'Light' : 'Dark'; }
  label();
  btn.addEventListener('click', function(){
    var next = current()==='dark' ? 'light' : 'dark';
    var apply = function(){ root.dataset.theme=next; try{localStorage.setItem('ps-theme',next);}catch(e){} label(); };
    if (document.startViewTransition && !matchMedia('(prefers-reduced-motion: reduce)').matches) document.startViewTransition(apply); else apply();
  });

  /* mobile menu */
  var menu=document.getElementById('menu'), bar=document.querySelector('.bar');
  if (menu && bar){
    menu.addEventListener('click', function(){ var o=bar.classList.toggle('open'); menu.setAttribute('aria-expanded', o?'true':'false'); menu.textContent=o?'Close':'Menu'; });
    bar.querySelectorAll('nav a').forEach(function(a){ a.addEventListener('click', function(){ bar.classList.remove('open'); menu.setAttribute('aria-expanded','false'); menu.textContent='Menu'; }); });
  }

  /* the asterisk leads to its footnote */
  var star=document.getElementById('star'), foot=document.getElementById('foot');
  if (star && foot) star.addEventListener('click', function(){
    foot.scrollIntoView({block:'center'}); foot.classList.add('lit');
    setTimeout(function(){ foot.classList.remove('lit'); }, 1600);
  });


  /* copy the message outline */
  var copyBtn=document.getElementById('copy');
  if (copyBtn) copyBtn.addEventListener('click', function(){
    var txt=document.getElementById('tmpl').textContent, out=document.getElementById('copied');
    var done=function(){ out.textContent='Copied. Paste it into your Facebook message.'; setTimeout(function(){out.textContent='';},4000); };
    if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, function(){ out.textContent='Select the outline and copy it.'; });
    else out.textContent='Select the outline and copy it.';
  });

  /* the "try it yourself" record puzzle */
  var verdict=document.getElementById('verdict');
  var answers={
    a:"Good pick. Record A was filled in about a month after he died, by someone close to the event, so it usually weighs more. But it doesn't prove he had no initial: the next step is a third, independent record, such as his obituary or his gravestone.",
    b:"Worth a look, but careful. Record B was filled in twenty-three years later, by someone remembering a man long gone, and the son carried that same initial. Closer to the event usually weighs more, so look for a third record before you believe it."
  };
  document.querySelectorAll('.card').forEach(function(c){
    c.setAttribute('aria-pressed','false');
    c.addEventListener('click', function(){
      document.querySelectorAll('.card').forEach(function(o){ o.setAttribute('aria-pressed','false'); });
      c.setAttribute('aria-pressed','true'); verdict.textContent=answers[c.dataset.pick];
    });
  });

  /* mark the section you are reading in the top bar */
  var links={}; document.querySelectorAll('.bar nav a').forEach(function(a){ var h=a.getAttribute('href'); if (h.charAt(0)==='#') links[h.slice(1)]=a; });
  if ('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(entries){
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
  var board=document.querySelector('table.ledger');
  if (board){
    var KEY='ps-mine', mine=[];
    try{ mine=JSON.parse(localStorage.getItem(KEY)||'[]'); }catch(e){ mine=[]; }
    var save=function(){ try{ localStorage.setItem(KEY, JSON.stringify(mine)); }catch(e){} };
    var rows=[].slice.call(board.querySelectorAll('tr[id^="case-"]')), groups=[].slice.call(board.querySelectorAll('tr.group'));
    var countEl=document.getElementById('minecount'), emptyEl=document.getElementById('mineEmpty'), current='all';
    function paint(){
      rows.forEach(function(r){
        var on=mine.indexOf(r.id)>-1, b=r.querySelector('.follow');
        b.setAttribute('aria-pressed', on?'true':'false'); b.textContent=on?'★':'☆'; b.title=on?'Following: tap to stop':'Follow this case';
        var seal=document.querySelector('.seals a[href="#'+r.id+'"]'); if (seal) seal.classList.toggle('mine', on);
      });
      if (countEl) countEl.textContent = mine.length ? '('+mine.length+')' : '';
    }
    function filter(f){
      current=f;
      rows.forEach(function(r){ r.hidden = !(f==='all' || r.dataset.hall===f || (f==='mine' && mine.indexOf(r.id)>-1)); });
      groups.forEach(function(g){ var any=rows.some(function(r){ return r.dataset.hall===g.dataset.hall && !r.hidden; }); g.hidden=!any; });
      if (emptyEl) emptyEl.hidden = !(f==='mine' && mine.length===0);
      document.querySelectorAll('.filters button').forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.f===f?'true':'false'); });
    }
    document.querySelectorAll('.filters button').forEach(function(b){ b.addEventListener('click', function(){ filter(b.dataset.f); }); });
    var note=document.getElementById('caseCopied');
    rows.forEach(function(r){
      r.querySelector('.follow').addEventListener('click', function(){
        var i=mine.indexOf(r.id); if (i>-1) mine.splice(i,1); else mine.push(r.id); save(); paint(); if (current==='mine') filter('mine');
      });
      r.querySelector('.link').addEventListener('click', function(){
        var url=location.origin+location.pathname+'#'+r.id;
        var done=function(){ note.textContent='Link to case '+r.id.split('-')[1]+' copied. Paste it anywhere to share.'; setTimeout(function(){ note.textContent=''; },3500); };
        if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, function(){ note.textContent=url; }); else note.textContent=url;
      });
    });
    paint();
  }

  /* ---------- marking quiz ---------- */
  var quiz=document.getElementById('quiz');
  if (quiz){
    var items=[].slice.call(quiz.querySelectorAll('.qlist > li')), score=0, done=0, out=document.getElementById('qscore');
    items.forEach(function(li){
      var opts=[].slice.call(li.querySelectorAll('.qopts .mk'));
      opts.forEach(function(o){
        o.addEventListener('click', function(){
          if (li.dataset.done) return; li.dataset.done='1'; done++;
          var ok=o.classList.contains(li.dataset.a); if (ok) score++;
          opts.forEach(function(x){ if (x.classList.contains(li.dataset.a)) x.classList.add('right'); else if (x===o) x.classList.add('wrong'); else x.classList.add('dim'); x.setAttribute('aria-disabled','true'); });
          var why=li.querySelector('.qwhy'); why.hidden=false; why.insertAdjacentHTML('afterbegin', ok?'<b>Right.</b> ':'<b>Not quite.</b> ');
          out.textContent = done===items.length ? ('You marked '+score+' of '+items.length+' the way we would.') : (score+' of '+done+' so far.');
        });
      });
    });
  }

  /* ---------- timeline arrows ---------- */
  var tl=document.getElementById('tl');
  if (tl){
    var step=function(d){ tl.scrollBy({left:d*tl.clientWidth*0.8, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'}); };
    var pv=document.querySelector('.tl-nav.prev'), nx=document.querySelector('.tl-nav.next');
    if (pv) pv.addEventListener('click', function(){ step(-1); });
    if (nx) nx.addEventListener('click', function(){ step(1); });
    tl.addEventListener('keydown', function(e){ if (e.key==='ArrowRight'){ step(1); e.preventDefault(); } if (e.key==='ArrowLeft'){ step(-1); e.preventDefault(); } });
  }

  /* for anyone who opens the browser's console */
  try{
    console.log('%cProject Scroll','font:28px Georgia,serif;color:#B3362B');
    console.log('%cYou found a back door. Every page has another side: view the page source, and read the note at the top.','font:14px Georgia,serif');
  }catch(e){}
})();
