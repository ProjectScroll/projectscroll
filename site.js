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

  /* for anyone who opens the browser's console */
  try{
    console.log('%cProject Scroll','font:28px Georgia,serif;color:#B3362B');
    console.log('%cYou found a back door. Every page has another side: view the page source, and read the note at the top.','font:14px Georgia,serif');
  }catch(e){}
})();
