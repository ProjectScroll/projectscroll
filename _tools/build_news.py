"""News of the hunt: the front-page news block on the home page, a page for every story, the news index and the
hunt's own game page (/hunt/). Source of truth: _tools/data/news.json and cases.json.
python3 _tools/build_news.py"""
import json, re, html, sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pages import page, R
E = lambda s: html.escape(str(s), quote=True)
N = json.load(open(f'{R}/_tools/data/news.json')); L = N['lead']; S = N['stories']
CASES = json.load(open(f'{R}/cases.json'))['cases']
nopen = sum(1 for c in CASES if not c.get('solved')); ncracked = len(CASES) - nopen
halls = sorted({c['hall'] for c in CASES if c['hall'].startswith('h')})
def day(d, long=False):
    x = datetime.date.fromisoformat(d)
    return x.strftime('%-d %B %Y') if long else x.strftime('%-d %b')
def pic(src, w, h, alt, sizes, lazy=True, cls=''):
    a = '' if src.endswith('-270') or src.endswith('-700') or src.endswith('-800') else ''
    return (f'<picture><source type="image/avif" srcset="{src}.avif"><img{" class=\""+cls+"\"" if cls else ""} src="{src}.webp" width="{w}" height="{h}" alt="{E(alt)}" sizes="{sizes}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async"></picture>')

def npic(base, alt, sizes, lazy=True, cls=''):
    return (f'<picture><source type="image/avif" srcset="{base}-600.avif 600w, {base}.avif 1200w" sizes="{sizes}"><img{" class=\""+cls+"\"" if cls else ""} src="{base}-600.webp" srcset="{base}-600.webp 600w, {base}.webp 1200w" sizes="{sizes}" width="1200" height="675" alt="{E(alt)}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async"></picture>')
def sqpic(base, alt=''):
    return f'<picture><source type="image/avif" srcset="{base}-sq.avif"><img src="{base}-sq.webp" width="320" height="320" alt="{E(alt)}" loading="lazy" decoding="async"></picture>'
LP = L.get('pic')
LEADPIC = (f'<a class="nw-lp" href="{L["url"]}" tabindex="-1" aria-hidden="true"><picture><source media="(max-width:640px)" type="image/avif" srcset="/img/news/lead-hunt-band.avif"><source media="(max-width:640px)" srcset="/img/news/lead-hunt-band.webp">'
           f'<source type="image/avif" srcset="/img/news/lead-hunt-360.avif 360w, /img/news/lead-hunt.avif 720w" sizes="8rem"><img src="/img/news/lead-hunt-360.webp" srcset="/img/news/lead-hunt-360.webp 360w, /img/news/lead-hunt.webp 720w" sizes="8rem" width="720" height="1280" alt="" decoding="async"></picture></a>') if LP else ''
# ---------- 1. the front-page block on the home page ----------
NUGGET = ('<svg class="nw-nug" viewBox="0 0 64 50" aria-hidden="true">'
          '<path d="M6 30 10 16 22 7 37 5 50 10 59 22 57 35 46 44 28 46 13 41z" fill="#B7811C" stroke="#6E4A0C" stroke-width="1.3" stroke-linejoin="round"/>'
          '<path d="M10 16 22 7 37 5 33 17 20 21z" fill="#F7DC86"/><path d="M37 5 50 10 59 22 44 21 33 17z" fill="#E9BE4C"/>'
          '<path d="M6 30 10 16 20 21 18 33z" fill="#D9A73A"/><path d="M20 21 33 17 44 21 40 33 27 35 18 33z" fill="#F2CB5B"/>'
          '<path d="M44 21 59 22 57 35 40 33z" fill="#C8922A"/><path d="M18 33 27 35 28 46 13 41 6 30z" fill="#A9741A"/>'
          '<path d="M27 35 40 33 57 35 46 44 28 46z" fill="#8F6013"/>'
          '<path d="M23 11 30 9 27 14z" fill="#FFF8DD"/><path d="M52 3v7M48.5 6.5h7" stroke="#FFF3C0" stroke-width="1.4" stroke-linecap="round"/></svg>')
top, more = S[:4], S[4:]
brief = lambda s: (f'<article class="nw-b" data-d="{s["date"]}"><a class="nw-th" href="/news/{s["slug"]}/" tabindex="-1" aria-hidden="true">{sqpic(s["pic"][0])}</a><p class="nw-k">{E(s["kicker"])}<span class="nw-new" hidden> · New</span></p>'
                   f'<h2><a href="/news/{s["slug"]}/">{E(s["headline"])}</a></h2></article>')
line = lambda s: (f'<li data-d="{s["date"]}"><span class="nw-k">{E(s["kicker"])}</span> <a href="/news/{s["slug"]}/">{E(s["short"])}</a><span class="nw-new" hidden> · New</span></li>')
FEAT = '<span class="nw-feat-k"><span aria-hidden="true">★</span> Featured</span> · '
second = lambda s: (f'<article class="nw-s{" nw-feat" if s.get("featured") else ""}" data-d="{s["date"]}"><a class="nw-simg" href="/news/{s["slug"]}/" tabindex="-1" aria-hidden="true">{npic(s["pic"][0], "", "(min-width:900px) 16rem, 92vw", lazy=False)}{"<span class=nw-ribbon>Featured</span>" if s.get("featured") else ""}</a>'
                    f'<p class="nw-k">{E(s["kicker"])}<span class="nw-new" hidden> · New</span></p><h2><a href="/news/{s["slug"]}/">{E(s["headline"])}</a></h2><p class="nw-sd">{E(s.get("sdek") or s["dek"])}</p></article>')
line = lambda s: (f'<li data-d="{s["date"]}"><a class="nw-th" href="/news/{s["slug"]}/" tabindex="-1" aria-hidden="true">{sqpic(s["pic"][0])}</a><span class="nw-lt"><span class="nw-k">{E(s["kicker"])}</span> <a href="/news/{s["slug"]}/">{E(s["short"])}</a><span class="nw-new" hidden> · New</span></span></li>')
today = datetime.date.today()
BLOCK = f'''<!--news-->
      <div class="nw" role="region" aria-labelledby="nwLead">
        <p class="nw-bar"><span>Front page</span><time class="nw-date" id="nwDate" datetime="{today.isoformat()}">{today.strftime('%A, %-d %B %Y')}</time><span>News of the hunt</span></p>
        <div class="nw-paper">
        <article class="nw-lead">
          <p class="nw-k nw-play">{E(L["kicker"])} <span>· Free to play</span></p>{NUGGET}
          <h1 id="nwLead"><a href="{L["url"]}"><span class="foil">{E(L["headline"])}</span></a><button class="fn" type="button" id="star" aria-label="Read the footnote">*</button></h1>
          {LEADPIC}<p class="lede">{L["dek"]}</p>
          <p class="foot" id="foot"><span>*</span> And every answer is in the record.</p>
          <p class="nw-enter"><a href="{L["url"]}">Enter the hunt <span aria-hidden="true">›</span></a></p>
          <ul class="trust nw-trust"><li>Free to play</li><li>Solved with clues</li><li>Open to anyone, anywhere</li></ul>
        </article>
        <div class="nw-sec">{''.join(second(s) for s in S[:2])}</div>
        <ul class="nw-more" aria-label="More news">{''.join(line(s) for s in S[2:])}</ul>
        </div>
      </div>
      <script>(function(){{try{{var K='ps-news-last',last=localStorage.getItem(K)||'',t=new Date();var d=document.getElementById('nwDate');d.textContent=t.toLocaleDateString('en-US',{{weekday:'long',day:'numeric',month:'long',year:'numeric'}});d.setAttribute('datetime',t.toISOString().slice(0,10));if(last)document.querySelectorAll('.nw [data-d]').forEach(function(e){{if(e.dataset.d>last){{var n=e.querySelector('.nw-new');if(n)n.hidden=false;}}}});localStorage.setItem(K,t.toISOString().slice(0,10));}}catch(e){{}}}})();</script>
<!--/news-->'''
p = f'{R}/index.html'; s = open(p).read()
if '<!--news-->' not in s:
    a = s.index('      <h1><span class="foil">Every clue is true.</span>'); b = s.index('      <p class="ctas">')
    s = s[:a] + BLOCK + '\n' + s[b:]
else:
    s = re.sub(r'<!--news-->.*?<!--/news-->', lambda m: BLOCK, s, flags=re.S)
open(p, 'w').write(s)

# ---------- 2. a page for every story ----------

PICS = json.load(open(f'{R}/_tools/data/ecv_pics.json'))
def pic1(k, sizes, cls=''):
    alt, cap, lic, w, h = PICS[k]
    img = (f'<a class="nw-pz" href="/img/ecv/{k}.webp"><picture><source type="image/avif" srcset="/img/ecv/{k}-700.avif 700w, /img/ecv/{k}.avif {w}w" sizes="{sizes}">'
           f'<img src="/img/ecv/{k}-700.webp" srcset="/img/ecv/{k}-700.webp 700w, /img/ecv/{k}.webp {w}w" sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async"></picture></a>')
    return f'<figure class="nw-fig{cls}">{img}<figcaption>{cap} <span class="nw-lic">{lic}</span></figcaption></figure>'
def picblock(kind, keys):
    keys=[k.strip() for k in keys if k.strip()]
    if kind=='fig': return pic1(keys[0], '(min-width:800px) 22rem, 94vw', ' nw-fig-r')
    if kind=='wide': return pic1(keys[0], '(min-width:800px) 46rem, 94vw', ' nw-fig-w')
    if kind=='row': return '<div class="nw-fig-row">' + ''.join(pic1(k, '(min-width:800px) 15rem, 94vw') for k in keys) + '</div>'
    ks = keys or list(PICS)
    return '<div class="nw-album">' + ''.join(pic1(k, '(min-width:800px) 15rem, 46vw') for k in ks) + '</div>'
CONTRIB = '<div class="nw-contrib"><p class="nw-contrib-h">Write for Project Scroll</p><p>We welcome research, stories and finds from readers, families, historians and other researchers. Contributed articles carry the contributor’s name. Send your story, your sources or your idea to <a href="mailto:research@projectscroll.com?subject=A%20story%20for%20Project%20Scroll">research@projectscroll.com</a>.</p></div>'
SHARE = """<script>document.querySelectorAll('.nw-share').forEach(function(b){ b.addEventListener('click', function(){ var u=location.href.split('#')[0], t=b.dataset.t;
  if (navigator.share) navigator.share({title:t, url:u}).catch(function(){}); else if (navigator.clipboard) navigator.clipboard.writeText(u).then(function(){ b.textContent='Link copied ✓'; }); }); });</script>
"""
def morelist(skip):
    return '<ul class="nw-list">' + ''.join(f'<li><span class="nw-k">{E(x["kicker"])}</span> <a href="/news/{x["slug"]}/">{E(x["headline"])}</a> <time datetime="{x["date"]}">{day(x["date"])}</time></li>' for x in S if x['slug'] != skip) + '</ul>'
for k, st in enumerate(S):
    pc = st['pic']
    fig = f'<figure class="nw-fig">{npic(pc[0], pc[1], "(min-width:900px) 46rem, 100vw", lazy=False)}<figcaption>{E(pc[2])}</figcaption></figure>'
    gal = ('<div class="nw-gal">' + ''.join(f'<figure><a href="{E(g[0])}"><img src="{E(g[0])}" width="{g[1]}" height="{g[2]}" alt="{E(g[3])}" loading="lazy" decoding="async"></a><figcaption>{E(g[3])}</figcaption></figure>' for g in st['gallery']) + '</div>') if st.get('gallery') else ''
    words = len(re.sub('<[^>]+>', ' ', ' '.join(st['body'])).split()); mins = max(1, round(words/200))
    prv, nxt = S[k-1] if k else None, S[k+1] if k+1 < len(S) else None
    pn = '<nav class="nw-pn" aria-label="Previous and next story">' + (f'<a class="nw-prev" href="/news/{prv["slug"]}/"><span>‹ Previous story</span>{E(prv["headline"])}</a>' if prv else '<a class="nw-prev" href="/hunt/"><span>‹ The lead story</span>Every clue is true.</a>') + (f'<a class="nw-next" href="/news/{nxt["slug"]}/"><span>Next story ›</span>{E(nxt["headline"])}</a>' if nxt else '<a class="nw-next" href="/"><span>Back to ›</span>The front page</a>') + '</nav>'
    def para(x):
        m = re.match(r'^\{\{(fig|wide|row|album)(?::([^}]*))?\}\}$', x)
        if m: return picblock(m.group(1), (m.group(2) or '').split(','))
        if x.startswith('## '):
            t=x[3:]; return f'<h2 id="{re.sub(r"[^a-z0-9]+","-",t.lower()).strip("-")}">{t}</h2>'
        return x if re.match(r'<(aside|nav|blockquote|ul|ol|p|div|figure)\b', x) else f'<p>{x}</p>'
    if '{{toc}}' in st['body']:
        hs=[x[3:] for x in st['body'] if x.startswith('## ')]
        toc='<nav class="nw-toc" aria-label="On this page"><b>On this page</b><ol>'+''.join(f'<li><a href="#{re.sub(r"[^a-z0-9]+","-",h.lower()).strip("-")}">{h}</a></li>' for h in hs)+'<li><a href="#sources">Sources</a></li></ol></nav>'
        body = ''.join(toc if x=='{{toc}}' else para(x) for x in st['body'])
    else:
        body = ''.join(para(x) for x in st['body'])
    reveal = f'<details class="nw-reveal"><summary>Show the answer</summary>{st["reveal"]}</details>' if st.get('reveal') else ''
    cta = '<p class="nw-cta">' + ' '.join(f'<a class="btn{" primary" if i==0 else ""}" href="{E(u)}">{E(t)}</a>' for i,(t,u) in enumerate(st['cta'])) + '</p>'
    src = ('<div class="nw-src"><h2 id="sources">Sources</h2><ul>' + ''.join((f'<li><a href="{E(u)}" rel="noopener">{E(t)}</a></li>' if u else f'<li>{E(t)}</li>') for t,u in st['sources']) + '</ul></div>') if st['sources'] else ''
    who = st.get('credit')
    credit = (f'<div class="nw-about" role="note"><p class="nw-about-h">About this research</p>'
              + (f'<p class="nw-about-by">Discovery and research by <b>{E(who)}</b>.</p>' if who else '<p class="nw-about-by">Researched and written by the Project Scroll research desk.</p>')
              + '<p>Every fact on this page comes from a source listed above, and each one can be checked where it is held. If you find an error, or hold a record that adds to the story, write to <a href="mailto:research@projectscroll.com">research@projectscroll.com</a>; corrections are made and noted on the page.</p></div>')
    live = f'<div class="nw-live" role="note"><p class="nw-live-h"><span class="nw-dot" aria-hidden="true"></span>Live research document</p><p>{st["live"]}</p></div>' if st.get('live') else ''
    b = f'''    <p class="crumb"><a href="/">← Front page</a> · <a href="/news/">All the news</a></p>
    <article class="nw-art">
      <p class="kicker">{E(st["kicker"])}</p>
      <h1>{E(st["headline"])}</h1>
      <p class="lede">{E(st["dek"])}</p>
      {live}<p class="nw-by">{("By " + E(st["by"]) + " · ") if st.get("by") else ""}Project Scroll · {"First published " if st.get("updated") else ""}<time datetime="{st["date"]}">{day(st["date"], True)}</time>{(" · Updated <time datetime=\""+st["updated"]+"\">"+day(st["updated"], True)+"</time>") if st.get("updated") else ""} · {mins} min read <button type="button" class="linkbtn nw-share" data-t="{E(st["headline"])}">Share this story</button></p>
      {fig}
      <div class="nw-text">{body}{reveal}</div>
      {gal}
      {cta}
      {src}
      {credit}
      {CONTRIB}
      {pn}
    </article>
    <section class="nw-morebox" aria-labelledby="nwMoreH"><h2 id="nwMoreH">More news of the hunt</h2>{morelist(st["slug"])}</section>
'''
    b += SHARE
    import pages as _P
    _x={"datePublished":st["date"],"dateModified":st.get("modified") or st.get("updated") or st["date"],"image":[f'https://projectscroll.com{st["pic"][0]}.webp',f'https://projectscroll.com/news/{st["slug"]}/card.jpg'],"articleSection":"News of the hunt","mainEntityOfPage":f'https://projectscroll.com/news/{st["slug"]}/'}
    if st.get('by'): _x["author"]={"@type":"Person","name":st["by"]}
    if st.get('live'): _x["creativeWorkStatus"]="Live research document, updated as new records are found"
    _P.EXTRA[f'news/{st["slug"]}/index.html']=_x
    page(f'news/{st["slug"]}/index.html', f'{st["headline"]} · News of the hunt · Project Scroll', st['dek'], b, og=f'https://projectscroll.com/news/{st["slug"]}/card.jpg?v=1')

# ---------- 3. the news index ----------
cards = ''.join(f'''<li class="nw-card"><a href="/news/{x["slug"]}/">{npic(x["pic"][0], "", "(min-width:900px) 15rem, 100vw", cls="nw-cimg")}<span class="nw-k">{E(x["kicker"])} · <time datetime="{x["date"]}">{day(x["date"])}</time></span><b>{E(x["headline"])}</b><span>{E(x["dek"])}</span></a></li>''' for x in S)
b = f'''    <div class="nw-index"><p class="crumb"><a href="/">← Front page</a></p>
    <p class="kicker">News of the hunt</p>
    <h1>All the news</h1>
    <p class="lede">What’s new on the trail: new cases, new tools, new old pictures. The newest are on the front page too.</p>
    <article class="nw-card nw-card-lead"><a href="/hunt/"><span class="nw-k">{E(L["kicker"])}</span><b>{E(L["headline"])}</b><span>Project Scroll now has a new, free online treasure hunt. Here is how to play.</span></a></article>
    <ul class="nw-cards">{cards}</ul>
    {CONTRIB}
    <p class="note">Every story is also in the <a href="/feed.xml">news feed</a> and on <a href="https://www.facebook.com/projectscroll/">Project Scroll’s Facebook page</a>.</p></div>
'''
page('news/index.html', 'News of the hunt · Project Scroll', 'The latest from Project Scroll: new cases, new tools and new old pictures from the St. Joseph River valley.', b)

# ---------- 4. the hunt's own page, set up like a game ----------
HALL = {'h1': ('Hall I', 'The Cassopolis Hall of Comparative Ovations', 'Where the hunt began: a joke secret society of 1846 and the hotel where it danced.'),
        'h2': ('Hall II', 'A lake with no stream in and no stream out', 'A settler’s gift, a parchment deed, a mill with no stream, and a doctor who kept a bone.')}
def qtext(n):
    t = open(f'{R}/cases/{n}/index.html').read()
    return html.unescape(re.sub('<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S).group(1))).strip()
def tile(c):
    n = c['n']; q = qtext(n); st = f'Cracked by {E(c["solved"])}' if c.get('solved') else 'Open'
    return (f'<li class="hn-case{" solved" if c.get("solved") else ""}" data-case="{n}"><a href="/cases/{n}/"><span class="hn-n">Case {n}</span>'
            f'<span class="hn-q">{E(q)}</span><span class="hn-st"><span class="hn-badge">{st}</span><span class="hn-prog"></span></span></a></li>')
levels = ''
for i, h in enumerate(halls):
    a, nm, blurb = HALL[h]; cs = [c for c in CASES if c['hall'] == h]
    levels += (f'<section class="hn-level" aria-labelledby="hl{h}"><p class="hn-lv">Level {i+1} · {a} · <span class="hn-lit">Lit</span></p><h3 id="hl{h}">{E(nm)}</h3><p class="note">{E(blurb)}</p>'
               f'<ol class="hn-cases">{"".join(tile(c) for c in cs)}</ol></section>')
fog = ''.join(f'<li class="hn-fog"><span class="hn-lv">Level {len(halls)+k+1} · Hall {"III IV V".split()[k]}</span><span>In the fog</span><span class="note">Opens when the hunt gets there</span></li>' for k in range(3))
practice = [c for c in CASES if c['hall'] == 'desk']
FB1 = 'https://www.facebook.com/projectscroll/posts/pfbid02v8LvpApazxUZnzXDGX9z5WTPJX8LkGDUHDB3iQZyigMWMCuytPBfC6doeLBXbLdKl'
QUESTS = [('casefile', 'Open a case', 'Read the first source of any case.', '/cases/1/'), ('thennow', 'Lay an old town over today', 'Fade a town plan of the 1860s into today’s streets.', '/map/cassopolis/'),
          ('street', 'Find a street that changed its name', 'Every then-and-now town hides one.', '/map/then-and-now/'), ('mapper', 'Walk the 1860 wall map', 'The whole county, every farm and name.', '/map/'),
          ('lidar', 'Fly over Cassopolis', 'In 355,650 laser points.', '/map/3d/cassopolis/'), ('valley', 'Find the three lost towns', 'Hidden in the hills of the valley in 3D.', '/map/3d/valley/'),
          ('walker', 'Walk old Broadway', 'Eleven stops, from your chair or on the spot.', '/walk/'), ('junior', 'The junior hunt', 'Seven questions for young hunters.', '/junior/'),
          ('oldhand', 'Read old handwriting', 'The clerks’ ten tricks.', '/guide/old-handwriting/'), ('informant', 'Read a death certificate', 'Every box, and how far to trust it.', '/guide/death-certificate/')]
quests = ''.join(f'<li class="hn-quest" data-b="{b}"><a href="{u}"><b>{E(t)}</b><span>{E(d)}</span><span class="hn-done" hidden>Badge earned ✓</span></a></li>' for b,t,d,u in QUESTS)
JS = r'''<script>
document.addEventListener('DOMContentLoaded', function(){ "use strict";
  var got={}, B=window.PS_BADGES||[], RK=window.PS_RANKS||[[0,'Candidate']];
  try{ got=JSON.parse(localStorage.getItem('ps-badges')||'{}')||{}; }catch(e){}
  var n=B.filter(function(b){ return got[b[0]]; }).length, cur=RK.filter(function(r){ return n>=r[0]; }).pop(), nxt=RK.filter(function(r){ return n<r[0]; })[0];
  var $=function(id){ return document.getElementById(id); };
  $('hnRank').textContent=cur[1]; $('hnBadges').textContent=n+' of '+B.length;
  var lo=cur[0], hi=nxt?nxt[0]:B.length; $('hnBar').style.width=Math.max(4,Math.min(100,(n-lo)/Math.max(1,hi-lo)*100))+'%';
  $('hnNext').textContent=nxt? (nxt[0]-n)+' more badge'+(nxt[0]-n===1?'':'s')+' to '+nxt[1] : 'The highest rank in the hall';
  var mine=[]; try{ mine=JSON.parse(localStorage.getItem('ps-mine')||'[]')||[]; }catch(e){}
  var read=0; document.querySelectorAll('.hn-case').forEach(function(li){ var k=li.dataset.case, t={}; try{ t=JSON.parse(localStorage.getItem('ps-trail-'+k)||'{}')||{}; }catch(e){}
    var c=Object.keys(t).filter(function(x){ return t[x]; }).length; if (c){ read++; li.querySelector('.hn-prog').textContent=c+(c===1?' source':' sources')+' read'; li.classList.add('begun'); }
    if (mine.indexOf(+k)>=0 || mine.indexOf(k)>=0) li.classList.add('followed'); });
  $('hnCases').textContent=read;
  var first=null; document.querySelectorAll('.hn-quest').forEach(function(q){ if (got[q.dataset.b]){ q.classList.add('done'); q.querySelector('.hn-done').hidden=false; } else if (!first) first=q; });
  if (first){ var a=first.querySelector('a'); $('hnMove').href=a.getAttribute('href'); $('hnMoveT').textContent=first.querySelector('b').textContent; first.classList.add('next'); }
  $('hnCard').hidden=false;
});
</script>'''
b = f'''    <div class="hn"><p class="crumb"><a href="/">← Front page</a> · <a href="/news/">All the news</a></p>
    <div class="hn-head">
      <div>
        <figure class="hn-pic"><picture><source type="image/avif" srcset="/img/news/lead-hunt-360.avif 360w, /img/news/lead-hunt.avif 720w" sizes="10rem"><img src="/img/news/lead-hunt-360.webp" srcset="/img/news/lead-hunt-360.webp 360w, /img/news/lead-hunt.webp 720w" sizes="10rem" width="720" height="1280" alt="{E(L["pic"][1])}" decoding="async"></picture></figure>
        <p class="kicker">The hunt</p>
        <h1>Every clue is true.</h1>
        <p class="lede">Project Scroll now has a new, free online treasure hunt. Real mysteries, history and clues hide in county histories, survey maps, certificates, forgotten newspapers, lore and local legends. Every one of them can be solved by you, and every answer is in the record.</p>
        <ul class="hn-stats"><li><b>{nopen}</b> cases open</li><li><b>{len(halls)}</b> halls lit</li><li><b>Free</b> no sign-up</li></ul>
        <p class="nw-cta"><a class="btn primary" href="/cases/1/">Start with Case 1</a> <a class="btn" href="{FB1}">Open the first door on Facebook</a></p>
      </div>
      <aside class="hn-card" id="hnCard" hidden aria-labelledby="hnCardH">
        <p class="hn-lv" id="hnCardH">Your hunter’s card</p>
        <p class="hn-rank" id="hnRank">Candidate</p>
        <div class="hn-meter" aria-hidden="true"><span id="hnBar"></span></div>
        <p class="note" id="hnNext"></p>
        <dl><div><dt>Badges</dt><dd id="hnBadges">0</dd></div><div><dt>Cases begun</dt><dd id="hnCases">0</dd></div></dl>
        <p class="hn-move">Your next move: <a id="hnMove" href="/cases/1/"><span id="hnMoveT">Open a case</span> ›</a></p>
        <p class="note">Kept on this device only. <a href="/badges/">Your badge book</a></p>
      </aside>
    </div>

    <section aria-labelledby="hnHow"><h2 id="hnHow">How to play</h2>
      <ol class="hn-steps"><li><b>Find a clue.</b> Every mystery is posted on Project Scroll’s Facebook page, and each case has its own page with the first sources to open.</li>
      <li><b>Search the record.</b> Old books, maps and certificates, many of them free online.</li>
      <li><b>Post your answer.</b> In the comments, saying exactly where you found it: the book, the page, and a link.</li>
      <li><b>Get named.</b> The first solver is named in the next post and on the case board, for good.</li></ol></section>

    <section aria-labelledby="hnLevels"><h2 id="hnLevels">The levels</h2>
      <p>The hunt is laid out as a trail of halls. Each hall is a level with its own cases. A hall lights up when it opens; the rest of the trail is still in fog.</p>
      {levels}
      <ul class="hn-fogs">{fog}</ul>
    </section>

    <section aria-labelledby="hnTrain"><h2 id="hnTrain">Training ground</h2>
      <p>New to old records? Try the practice case first. It is a real puzzle from the research desk, with the full answer in the field notes once you have had a go.</p>
      <ol class="hn-cases">{"".join(tile(c) for c in practice)}</ol></section>

    <section aria-labelledby="hnSide"><h2 id="hnSide">Side quests</h2>
      <p>Badges for exploring. Each one moves you up the ranks, from Candidate to Keeper of the Hall.</p>
      <ul class="hn-quests">{quests}</ul>
      <p><a href="/badges/">All the badges, and the five ranks ›</a></p></section>

    <section aria-labelledby="hnSolvers"><h2 id="hnSolvers">The solvers</h2>
      <p>{"No case has been cracked yet. The first name on the board could be yours." if not ncracked else "Named on the case board, for good."}</p></section>

    <section aria-labelledby="hnRules"><h2 id="hnRules">The rules</h2>
      <ul class="hn-rules"><li><b>Read the record.</b> Every answer is in a book, on a map, or on a page.</li><li><b>Show your work.</b> A name without the page it came from is only a guess.</li>
      <li><b>Stay on paper.</b> Never dig, never go near a grave, and never set foot on anyone’s land.</li><li><b>Be kind.</b> These are real people, and their families are still here.</li></ul>
      <p class="note">Tools for the hunt: <a href="/records/">where the records are</a>, <a href="/glossary/">the glossary</a>, <a href="/toolkit/">the toolkit</a> and <a href="/worksheet/project-scroll-hunters-worksheet.pdf">the hunter’s worksheet (PDF)</a>.</p></section></div>
''' + JS + '\n'
page('hunt/index.html', 'The hunt: every clue is true · Project Scroll', 'Project Scroll’s free online treasure hunt: real mysteries of the St. Joseph River valley, solved from county histories, maps and certificates. Levels, side quests and badges, no sign-up.', b, og='https://projectscroll.com/hunt/card.jpg?v=1')
print('news built:', len(S), 'stories, the hunt page and the front page')
