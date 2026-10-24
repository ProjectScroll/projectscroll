import os,re
def smart(t):
    t=re.sub(r"(\w)'(\w)",r"\1’\2",t)
    t=re.sub(r"(\s|^|\(|—)'",r"\1‘",t)
    t=t.replace("'","’")
    t=re.sub(r'(^|[\s(—\[])"',r'\1“',t)
    t=t.replace('"','”')
    return t
def proc(html):
    out=[];i=0
    for m in re.finditer(r'<(script|style|pre)\b.*?</\1>|<!--.*?-->|<[^>]+>',html,re.S):
        out.append(smart(html[i:m.start()])); out.append(m.group(0)); i=m.end()
    out.append(smart(html[i:])); return ''.join(out)
import pathlib, json as _json, html as _html, datetime as _dt
R=str(pathlib.Path(__file__).resolve().parent.parent)
RECORD_HOSTS=('loc.gov','hathitrust.org','archive.org','familysearch.org','michiganology.org','umich.edu','glorecords.blm.gov','ancestry','findagrave','newspapers.com','chroniclingamerica','digmichnews','cmich.edu','michigan.gov','rumsey','books.google','jstor','worldcat','openlibrary','wikisource','gutenberg','nypl','cassdistrictlibrary','seekingmichigan','preservica')
def colophon(body):
    """Sources cited on this page: every outbound link in the body to a record-holding site, once each, in order."""
    import re, html as _h
    seen=[]; out=[]
    for m in re.finditer(r'<a\s[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', body, re.S):
        url, text = m.group(1), re.sub('<[^>]+>','',m.group(2)).strip()
        host=re.sub(r'^https?://(www\.)?','',url).split('/')[0]
        if not any(h in url for h in RECORD_HOSTS): continue
        if url in seen or not text or len(text)>140: continue
        if 'class="btn' not in m.group(0)[:60] and (re.match(r'^(read it|read the|open|see|view|free online|read it free online)\b', text, re.I) or len(text)<6):
            li=body.rfind('<li>', 0, m.start()); seg=body[li+4:m.start()] if li>=0 and m.start()-li<600 else body[max(0,m.start()-260):m.start()]
            seg=re.sub(r'^[^<]*?>','',seg) if seg.find('>')!=-1 and (seg.find('<')==-1 or seg.find('>')<seg.find('<')) else seg
            seg=re.sub(r'\s+',' ',re.sub('<[^>]+>','',seg)).strip(' :;,—–-')
            cite=re.match(r'^(.*?\(\d{4}\)[^.]*)', seg)
            text=(cite.group(1) if cite else re.split(r'(?<=[.!?])\s+', seg)[0]).strip(' :;,—–-')[:140] or text
            text=re.sub(r',?\s*p{1,2}\.?$','',text).rstrip(',')
        seen.append(url); out.append((url, text, host))
    if not out: return ''
    HOLD={'umich.edu':'University of Michigan Library','loc.gov':'Library of Congress','hathitrust.org':'HathiTrust','archive.org':'Internet Archive','familysearch.org':'FamilySearch (free account)','michiganology.org':'Archives of Michigan','preservica.com':'Archives of Michigan','findagrave.com':'Find a Grave','glorecords.blm.gov':'Bureau of Land Management, General Land Office records','cmich.edu':'Central Michigan University','chroniclingamerica':'Library of Congress, Chronicling America','cassdistrictlibrary.org':'Cass District Library','migenweb.org':'Cass County MIGenWeb Project'}
    def holder(h):
        for k,v in HOLD.items():
            if k in h: return v
        return h
    items=''.join('<li><a href="%s" rel="noopener">%s</a>%s</li>' % (_h.escape(u, quote=True), _h.escape(t), '' if holder(h).split(' ')[0].lower() in t.lower() else ' <span class="col-host">'+_h.escape(holder(h))+'</span>') for u,t,h in out)
    return ('    <aside class="colophon" aria-labelledby="colH">\n      <h2 id="colH">Sources cited on this page</h2>\n      <ol>%s</ol>\n'
            '      <p class="note">Every link above opens the source where it is held. If one has moved, <a href="mailto:research@projectscroll.com?subject=A%%20broken%%20link">tell us</a>.</p>\n    </aside>\n') % items

EXTRA={}  # per-page schema fields set by a builder (dates, authors)
def schema(path, title, desc, canon, og):
    import json, datetime, os
    top=path.split('/')[0]; parts=[p for p in path.replace('index.html','').split('/') if p]
    crumbs=[{"@type":"ListItem","position":1,"name":"Project Scroll","item":"https://projectscroll.com/"}]
    names={'news':'News of the hunt','hunt':'The hunt','notes':'Field notes','map':'Map room','cases':'Cases','guide':'Guides','families':'Family histories','legends':'Family legends','records':'Where the records are','glossary':'Glossary','toolkit':'Toolkit','badges':'Badges','about':'About','document':'Document of the month','privacy':'Privacy','cassopolis':'Cassopolis','research':'Research services','food':'Food & Recipes'}
    url='https://projectscroll.com/'
    for i,p in enumerate(parts):
        url+=p+'/'; crumbs.append({"@type":"ListItem","position":i+2,"name":names.get(p, title.split(' · ')[0]) if i<len(parts)-1 else title.split(' · ')[0],"item":url})
    kind='NewsArticle' if (top=='news' and len(parts)==2) else ('Article' if top in ('notes','cases','document') else 'WebPage')
    try: mod=datetime.date.fromtimestamp(os.path.getmtime(os.path.join(R, path))).isoformat()
    except Exception: mod=datetime.date.today().isoformat()
    g=[{"@type":"BreadcrumbList","itemListElement":crumbs},
       {"@type":kind,"@id":canon+"#page","url":canon,"name":title.split(' · ')[0],"headline":title.split(' · ')[0],"description":desc,"image":og,"inLanguage":"en-US","isPartOf":{"@id":"https://projectscroll.com/#site"},"publisher":{"@id":"https://projectscroll.com/#org"},"dateModified":mod}]
    if kind in ('Article','NewsArticle'): g[1]["author"]={"@id":"https://projectscroll.com/#org"}
    if path in EXTRA: g[1].update(EXTRA[path])
    # the towns are places: say so, with where they are, so search engines can file each page under its town
    PL={'cassopolis':('Cassopolis','Michigan',41.9117,-86.0097),'niles':('Niles','Michigan',41.8298,-86.2541),'dowagiac':('Dowagiac','Michigan',41.9842,-86.1086),'paw-paw':('Paw Paw','Michigan',42.2178,-85.8911),
        'south-bend':('South Bend','Indiana',41.6764,-86.2520),'goshen':('Goshen','Indiana',41.5823,-85.8345),'elkhart':('Elkhart','Indiana',41.6820,-85.9767)}
    slug=parts[-1] if parts else ''
    if slug in PL and (top=='map' or len(parts)==1):
        n,st,la,lo=PL[slug]
        g.append({"@type":"City","@id":"https://projectscroll.com/#place-"+slug,"name":n,"geo":{"@type":"GeoCoordinates","latitude":la,"longitude":lo},"containedInPlace":{"@type":"State","name":st}})
        g[1]["about"]={"@id":"https://projectscroll.com/#place-"+slug}
    return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@graph":g}, ensure_ascii=False)+'</script>'


def sharebar(canon, title, og):
    """Plain links to share the page on the common networks (no logos, no trackers); copy and the device's own share sheet are added by site.js."""
    from urllib.parse import quote
    import re as _re, html as _h
    t = _h.unescape(_re.sub(r'\s*·\s*(News of the hunt|Project Scroll|Field notes).*$', '', title))
    u, tt, img = quote(canon, safe=''), quote(t, safe=''), quote(og.split('?')[0], safe='')
    L = [('Facebook', f'https://www.facebook.com/sharer/sharer.php?u={u}'),
         ('X', f'https://x.com/intent/post?url={u}&amp;text={tt}'),
         ('Bluesky', f'https://bsky.app/intent/compose?text={tt}%20{u}'),
         ('Reddit', f'https://www.reddit.com/submit?url={u}&amp;title={tt}'),
         ('LinkedIn', f'https://www.linkedin.com/sharing/share-offsite/?url={u}'),
         ('Pinterest', f'https://www.pinterest.com/pin/create/button/?url={u}&amp;media={img}&amp;description={tt}'),
         ('Email', f'mailto:?subject={tt}&amp;body={tt}%0A%0A{u}')]
    a = ''.join(f'<a class="sb-l" href="{h}" rel="noopener nofollow">{n}</a>' for n, h in L)
    return (f'<aside class="sharebar" aria-label="Share this page" data-share data-url="{_h.escape(canon)}" data-title="{_h.escape(t)}">'
            f'<p class="sb-h">Share this page</p><div class="sb-row">{a}'
            '<button type="button" class="sb-l sb-copy">Copy link</button><button type="button" class="sb-l sb-more" hidden>More…</button></div></aside>\n')

def page(path, title, desc, body, canon=None, noindex=False, og='https://projectscroll.com/og-dark.jpg?v=7'):
    canon = canon or 'https://projectscroll.com/'+path.replace('index.html','')
    top=path.split('/')[0]
    accent=' data-accent="desk"' if top in ('families','legends','about') else (' data-accent="hunt"' if top in ('cases','notes','badges','map','toolkit','glossary','records','guide','document','notebook','keepsake') else '')
    import html as _h
    title=_h.escape(title, quote=True); desc=_h.escape(desc, quote=True)
    head=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{canon}">'}
{schema(path, title, desc, canon, og) if not noindex else ''}
<meta name="theme-color" content="#E8ECE6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#151B21" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Project Scroll">
<meta property="fb:app_id" content="2627955700977491">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg?v=2" type="image/svg+xml">
<link rel="icon" href="/icons/icon-32.png" type="image/jpeg" sizes="32x32">
<link rel="alternate icon" href="/favicon.ico?v=2" sizes="16x16 32x32 48x48">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png?v=2">
<link rel="alternate" type="application/atom+xml" title="Project Scroll: new cases, field notes and documents" href="/feed.xml">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/fonts/libre-caslon-display-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/libre-caslon-text-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<script>document.documentElement.classList.add('js');try{{var t=localStorage.getItem('ps-theme'); if(t) document.documentElement.dataset.theme=t;}}catch(e){{}}</script>
<link rel="stylesheet" href="/site.min.css?v=e7cdba41">
<script type="speculationrules">{{"prefetch":[{{"where":{{"and":[{{"href_matches":"/*"}},{{"not":{{"href_matches":["/*.pdf","/*.zip","/*.xml","/*.json"]}}}},{{"not":{{"selector_matches":"[download], [target=_blank]"}}}}]}},"eagerness":"moderate"}}],"prerender":[{{"where":{{"and":[{{"selector_matches":".bar a, .toolrow .nd a, .crumb a, footer nav a, .partrail a, .search-res a"}},{{"href_matches":"/*"}},{{"not":{{"href_matches":["/*.pdf","/map/3d/*"]}}}}]}},"eagerness":"conservative"}}]}}</script>
</head>
<body>
<span class="vprogress" aria-hidden="true"></span>
<a class="skip" href="#main">Skip to the content</a>
<aside class="masthead" id="masthead" aria-label="Plates from the record" data-set="heron-leaves|A heron in the lily pads, autumn|50% 55%||c;rogers|Rogers, History of Cass County, 1875, p. 253|50% 38%|/document/|g;squirrel|A flying squirrel at night|50% 4%||c;food-peppers|Stuffed peppers|50% 50%|/food/recipes/|c;trunk|A forgotten trunk in an attic|50% 50%||c;spark|Light and fire meet|50% 50%||c;mathews|Mathews, History of Cass County, 1882, p. 174|50% 50%|/cases/1/|g;cabin-autumn|The Pioneer Log Cabin Museum, Cassopolis, in autumn|50% 50%||c;window|A window on a lake|50% 50%||c;dowagiac|Dowagiac in 1860, from the county wall map|50% 50%|/map/dowagiac/|c;jefferson|A township plat, Cass County, with its lakes|50% 50%||g;food-fritters|Apple fritters, warm from the fryer|50% 50%|/food/recipes/|c;ball|A ball in a village hall, long ago|50% 50%||c;bellin|Bellin’s Carte des Lacs du Canada, 1744|50% 50%||c;roadtotown|The road to town, Cassopolis, on an old postcard|50% 62%|/map/cassopolis/|g;cabin-postcard|The Pioneer Log Cabin, Cassopolis, on an old postcard|50% 50%||g;trapper|A trap set at the edge of the ice|50% 50%||c;niles|Niles in 1860, the river through the plan|50% 50%|/map/niles/|c;islandhouse|The Island House, Diamond Lake, Cassopolis, on a postcard|50% 50%||g;food-luncheon|A luncheon still life, John F. Francis, about 1860|50% 45%|/food/|c;weaver|A snowshoe woven by a cabin on the water|50% 50%||c;wallmap|The 1860 wall map of the county, at the Library of Congress|50% 50%|/map/|c;broadway1|Broadway, Cassopolis, in the days of wagons|50% 55%|/map/cassopolis/|g;cabin-inside|Inside the log cabin museum|50% 50%||c;diamond|A stone held up to the light|50% 50%||c;pawpaw|Paw Paw in 1860, from the county wall map|50% 50%|/map/paw-paw/|c;crowdcars|Laying the first log of the Pioneer Log Cabin, Cassopolis, 23 May 1923, on a postcard of the day|50% 50%||g;food-beets|Fresh beets at a farm market|50% 50%|/food/recipes/|c;alpine|A sunset out West|50% 50%||c;bellin-river|Bellin, 1744: the lake of the Illinois and the river of the Miamis|50% 50%|/#timeline|c;yerty|West side of Broadway looking south, Cassopolis, a Yerty postcard|50% 60%|/map/cassopolis/|g;cabin-kitchen|A pioneer kitchen set for supper|50% 50%||c;columbian|An allegory of the Columbian Exposition, 1893|50% 50%||c;wallmap2|The 1860 wall map, lower sheet|50% 50%|/map/|c;shovels|Men with shovels at the shore|50% 50%||g;food-huckleberries|Picking wild huckleberries|50% 50%|/food/recipes/|c;ages|Every age at once|50% 50%||c;threemen|Three men on the road|50% 50%||c;carriages|Carriages drawn up on Broadway, Cassopolis|50% 50%|/map/cassopolis/|g;reenactors|Living history: a reenactors’ camp|50% 50%||c;spirit|A figure on a tree, in the morning light|50% 50%||c;unionhotel|The Union Hotel, and a notice on the post|50% 50%|/cases/1/|c;broadway3|Broadway, Cassopolis, when the first cars came|50% 50%|/map/cassopolis/|g;food-tomatoes|Ripe tomatoes, sliced and held to the light|50% 50%|/food/recipes/|c;stone|A stone held up to the light|50% 50%||c;oxen|Oxen, a cart and an island house|50% 50%||c;packtrain|Four men, a string of mules and a dusty street|50% 18%|/#hunt|g;broadway-postcard|Broadway, Cassopolis, on an old postcard|50% 50%||c;sawyer|A sawyer cutting wood|50% 50%|/cases/7/|c;engine|A train into Dowagiac|50% 50%||c;broadway2|A Cassopolis street, early 1900s|50% 50%|/map/cassopolis/|g;food-potato-soup|A bowl of potato soup|40% 50%|/food/recipes/|c;campfire|A fire by the water, and the stars|50% 50%||c;letter|A letter read on the porch, first snow|50% 50%||c;barroom|A bar-room, from an old photograph|50% 50%||g;model-a|An old Ford on a summer street|50% 50%||c;bass|A bass, a lure and a lazy afternoon|50% 30%||c;couple|Two who settled here|50% 50%||c;saloon|A saloon counter, from an old print|50% 50%||g;food-still-life|A still life of fruit, American, about 1870|50% 50%|/food/|c;footprint|A footprint in the frost|50% 50%||c;bonnet|An evening in Cassopolis|50% 50%||c;directory|Hotels, merchants, physicians: Cassopolis in 1860|50% 50%|/map/cassopolis/|g;holiday-pavilion|A pavilion lit for the holidays|50% 50%||c;nightwalk|Three on the ice, by night|50% 50%||c;hearth|Children by the hearth|50% 50%||c;royce|Indian land cessions in Michigan, Royce, 1899|50% 50%|/map/|g;food-corn|Sweet corn on an old plate|50% 50%|/food/recipes/|c;ladle|A cabin in the pines, at sunset|50% 40%||c;templar|A ceremony in the frost|50% 35%||c;candles|A dance by candlelight|50% 50%||c;holiday-band|A brass band among the holiday lights|50% 50%||c;parade|A parade with plumes and a drum|50% 50%||c;hunter|A hunter in the swamp, flintlock raised|50% 50%||c;running|Two running through the woods|50% 50%||c;food-market|The Benton Harbor fruit market, on an old postcard|50% 50%|/food/#fields|c;cabin-sunset|A purple sunset over the water behind the log cabin, Cassopolis|50% 50%||c;initiation|An initiation, as the lodge might have held it|50% 50%|/cases/1/|c;corner|A farmhouse at a crossroads, from the air|50% 50%||c;history|The county history, open on the desk|50% 50%|/records/|c;hall|The hall, the banner and the whole lodge|50% 50%|/cases/1/|c;lodge|A room illuminated by lamplight and moon|50% 50%||c;certificates|Two certificates on a desk|50% 50%|/notes/one-letter-two-certificates/|c;reel|A reel on the boards, by the fire|50% 50%||c">
  <picture class="mh-pic on"><source type="image/avif" media="(max-width:700px)" srcset="/img/strip/heron-leaves-800.avif"><source type="image/avif" srcset="/img/strip/heron-leaves.avif"><source media="(max-width:700px)" srcset="/img/strip/heron-leaves-800.webp"><img src="/img/strip/heron-leaves.webp" width="1600" height="400" alt="" fetchpriority="low" decoding="async"></picture>
  <p class="mh-cap"><span class="mh-n">1 / 84</span> A heron in the lily pads, autumn</p>
  <button type="button" class="mh-prev" aria-label="Previous plate" title="Previous plate">‹</button><button type="button" class="mh-next" aria-label="Next plate" title="Next plate">›</button><button type="button" class="mh-full" aria-label="See the whole plate" title="See the whole plate">⤢</button>
</aside>
<header class="bar">
  <div class="bar-in">
    <a class="mark" href="/" aria-label="Project Scroll home">
      <svg viewBox="0 0 32 32" aria-hidden="true"><rect x="7" y="4" width="18" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M11 4v24" stroke="#B3362B" stroke-width="2"/><path d="M14 11h7M14 15h7M14 19h5" stroke="currentColor" stroke-width="1.6"/></svg>
      Project Scroll
    </a>
    <nav aria-label="Sections" id="sitenav">
      <a href="/hunt/">Hunt</a><a href="/news/">News</a><a href="/food/">Food &amp; Recipes</a><a href="/cases/">Cases</a><a href="/services/">Services</a><a href="/#contact">Contact</a>
    </nav>
    <button class="searchbtn" type="button" id="searchBtn" aria-label="Search the site" aria-haspopup="dialog"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
    <a class="badgelink" id="badgeLink" href="/badges/" aria-label="Your badges"><svg viewBox="0 0 40 40" aria-hidden="true"><path d="M20 3l4.6 9.4 10.4 1.5-7.5 7.3 1.8 10.3L20 26.6l-9.3 4.9 1.8-10.3-7.5-7.3 10.4-1.5z" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round"/></svg><span class="bn" id="badgeN" hidden></span></a>
    <button class="menu" type="button" id="menu" aria-expanded="false" aria-controls="sitenav">Menu</button>
    <button class="theme" type="button" aria-label="Switch to dark" id="theme">Dark</button>
    <button class="lamp" type="button" id="lamp" aria-label="Light the miner’s lamp" aria-pressed="false" title="The miner’s lamp: a glow that follows your pointer"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle class="glow" cx="12" cy="13.4" r="4.6" stroke="none"/><circle class="glow-in" cx="12" cy="14" r="2.6" stroke="none"/><path d="M12 2v1.6M9 3.6h6M8 6.4h8l-.7 2H8.7z"/><path class="glass" d="M8.6 8.4v8.3l1.4 1.8h4l1.4-1.8V8.4"/><path class="shine" d="M9.6 9.6v6.2" stroke-width="1" opacity=".55"/><path d="M8.4 18.5h7.2M10.2 18.5v2h3.6v-2"/><path class="flame" d="M12 8.8c-1.9 2-2.6 3.4-2.6 4.9a2.6 2.6 0 0 0 5.2 0c0-1.5-.7-2.9-2.6-4.9z" stroke="none"/><path class="flame-in" d="M12 11.8c-.9 1-1.2 1.7-1.2 2.4a1.2 1.2 0 0 0 2.4 0c0-.7-.3-1.4-1.2-2.4z" stroke="none"/><path class="ray" d="M12 7.6v-1.4M15.9 10.2l1-1M8.1 10.2l-1-1M16.6 14.2h1.4M5.9 14.2h1.4" stroke-width="1.1"/></svg></button>
  </div>
</header>
<dialog class="search" id="searchDlg" aria-label="Search the site">
  <form method="dialog" class="search-in"><input type="search" id="searchQ" placeholder="Search cases, field notes, guides…" autocomplete="off" aria-label="Search"><button type="submit" class="vh">Search</button><button type="button" class="linkbtn" id="searchClose">Close</button></form>
  <p class="vh" id="searchCount" aria-live="polite"></p>
  <ol class="search-res" id="searchRes"></ol>
  <p class="note search-tip">Tip: press <kbd>/</kbd> or <kbd>Ctrl</kbd> <kbd>K</kbd> anywhere to search.</p>
</dialog>
<div class="sheet" id="top">
<nav class="toolrow" aria-label="Visit and plan, research tools, sponsor and advertise"><div class="tr-nav"><a class="tr-visit" href="/visit/">Visit &amp; Plan</a><span class="navdrop"><button type="button" class="nd-b" aria-expanded="false" aria-controls="ndTools">Research tools</button><span class="nd" id="ndTools" hidden><span class="nd-h">Maps</span><a href="/map/">The map room</a><a href="/map/then-and-now/">Seven towns, then and now</a><a href="/map/3d/valley/">The valley in 3D</a><a href="/map/3d/cassopolis/">Cassopolis in LiDAR</a><a href="/places/">The gazetteer</a><a href="/map/#sanborn">Sanborn fire-insurance sheets</a><a href="/postcards/">Old postcards &amp; photos</a><a href="/roads-and-rails/">Roads, rails and mills</a><a href="/lost-towns/">Lost towns of the valley</a><a href="/place-names/">How the towns got their names</a><span class="nd-h">Research</span><a href="/discoveries/">Discoveries: what we’ve found</a><a href="/names/">Who was in town</a><a href="/soldiers/">Soldiers of the valley</a><a href="/newspaper/">Newspaper of the month</a><a href="/almanac/">This day in the valley</a><a href="/museums/">Museums &amp; historic places</a><a href="/passport/">Your passport</a><a href="/story/">Share your story</a><a href="/made-in-the-valley/">Made in the Valley</a><a href="/heirlooms/">Heirlooms</a><a href="/sources/">The sources shelf</a><a href="/sources/libraries/">The libraries behind the stories</a><a href="/records/">Finding the records</a><a href="/toolkit/">The research toolkit</a><a href="/guide/old-handwriting/">Reading old handwriting</a><a href="/guide/death-certificate/">Reading a death certificate</a><a href="/guide/gravestones/">Reading old gravestones</a><a href="/glossary/">Glossary</a><a href="/families/">Families</a><a href="/legends/">Legends</a><a href="/lore/">Lore and legends</a><a href="/classrooms/">For classrooms</a></span></span><form class="tr-find" action="/names/" method="get" role="search" aria-label="Find a name"><input type="search" name="q" placeholder="Find a name" aria-label="Find a name in the old directories and rolls" autocomplete="off" spellcheck="false" enterkeyhint="search"><button type="submit" aria-label="Find"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></form></div><p class="pb-sponsor"><a href="/sponsor-and-advertise/"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 2.5h4M5.5 4h5l-.6 1H6.1zM6 5.2c-1.1 1-1.6 2.3-1.6 3.6 0 2.3 1.6 4 3.6 4s3.6-1.7 3.6-4c0-1.3-.5-2.6-1.6-3.6M8 7.4c-.7.8-1 1.5-1 2.2a1 1 0 0 0 2 0c0-.7-.3-1.4-1-2.2zM6 12.8h4v1H6z"/></svg><span>Keep the lanterns lit</span><b>Sponsor &amp; advertise</b></a></p></nav>
  <main id="main" class="page"{accent}>
'''
    share = '' if noindex or path in ('404.html','index.html') or (path.startswith('news/') and path!='news/index.html') else sharebar(canon, title, og)
    foot=share+colophon(body)+'''  </main>
  <div class="trailx" aria-hidden="true"><svg viewBox="0 0 640 64" focusable="false"><defs><mask id="trailM" maskUnits="userSpaceOnUse"><path class="tx-draw" pathLength="1" d="M52 36C96 12 136 56 186 34S276 10 326 34 426 58 478 30 560 20 590 32"/></mask></defs><g class="tx-compass"><circle cx="26" cy="32" r="15"/><circle cx="26" cy="32" r="10.5"/><path class="tx-n" d="M26 19l3 13h-6z"/><path d="M26 45l3-13h-6z"/><path d="M13 32h26M26 17v30"/></g><path class="tx-path" mask="url(#trailM)" d="M52 36C96 12 136 56 186 34S276 10 326 34 426 58 478 30 560 20 590 32"/><g class="tx-x"><path d="M598 22l18 20M616 22l-18 20"/></g><g class="tx-gem"><path d="M607 10l3.2 3.2-3.2 7.6-3.2-7.6z"/><path class="tx-spark" d="M607 2v6M607 22v-1M600 12h-3M614 12h3"/></g></svg></div>
  <footer class="site">
    <div>
      <p class="motto">Every clue is true. Every answer is in the record.</p>
      <p class="fmail"><a href="mailto:research@projectscroll.com">research@projectscroll.com</a></p>
      <p class="fmail"><a href="/sponsor-and-advertise/">Sponsor &amp; advertise</a></p>
      <p class="calmrow"><button type="button" class="calmbtn" id="calm" aria-pressed="false"><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="4" y="3" width="2.6" height="10" rx=".8"/><rect x="9.4" y="3" width="2.6" height="10" rx=".8"/></svg><span>Pause all motion</span></button></p>
      <a class="fbfollow" href="https://www.facebook.com/projectscroll/" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.8 1.4-3.8 3.9v2.3H7.9v3h2.6V21z"/></svg>Follow the hunt on Facebook</a>
      <p>Project Scroll is independent historical research from the St. Joseph River Valley (<a href="/cassopolis/">Cassopolis</a>, Dowagiac, Niles and beyond), with a studio for digital imaging, design, photography, 3D LiDAR, animation and video. Some mysteries open in an afternoon. Some take a season.</p>
    </div>
    <nav aria-label="Footer">
      <a href="/">Home</a><a href="/cases/">Case board</a><a href="/notes/">Field notes</a><a href="/map/">Map room</a><a href="/junior/">Junior hunt</a><a href="/classrooms/">Classrooms</a><a href="/places/">Gazetteer</a><a href="/names/">Names</a><a href="/sources/">Sources</a><a href="/almanac/">Almanac</a><a href="/toolkit/">Toolkit</a><a href="/notes/book/">Book of notes</a><a href="/families/">Family histories</a><a href="/legends/">Family legends</a><a href="/lore/">Lore and legends</a><a href="/services/#studio">Studio</a><a href="/records/">Where the records are</a><a href="/glossary/">Glossary</a><a href="/about/">About</a><a href="/badges/">Your badges</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a><a href="/accessibility/">Accessibility</a><a href="/guide/death-certificate/">Certificate guide</a><a href="/worksheet/project-scroll-hunters-worksheet.pdf">Hunter's worksheet</a><a href="/sample/project-scroll-sample-report.pdf">Sample report</a><a href="/#contact">Contact</a><a href="https://www.facebook.com/projectscroll/">Facebook</a>
    </nav>
    <p class="cite">To cite a page: Project Scroll, “[page title],” projectscroll.com/[path], dated as shown on the page, accessed [date]. Quote the date on the page, not today’s.</p>
<p class="fine">© 2026 Project Scroll · <a href="#top">Back to the top</a></p>
    <p class="cipherline"><span role="img" aria-label="A line written in code">ESP HZCO TD SLWEPC. DLJ TE TY JZFC MLORP MZZV.</span></p>
  </footer>
</div>
<script src="/site.min.js?v=e7cdba41" defer></script>
</body>
</html>
'''
    full=os.path.join(R,path); os.makedirs(os.path.dirname(full),exist_ok=True)
    open(full,'w').write(proc(head+body+foot))

if __name__=='__main__':
    page('notes/one-letter-two-certificates/index.html',
     'One Letter, Two Certificates · Project Scroll field notes',
     'A pioneer, his son, two death certificates and one middle initial: what to do when old records disagree.',
    '''    <p class="crumb"><a href="/notes/">← All field notes</a></p>
        <p class="kicker">Field notes · No. 1 · 17 October 2026</p>
        <h1>One Letter, Two Certificates</h1>
        <p class="lede" style="font-size:1.2rem">One letter. That's all it was. A single middle initial, and it nearly turned one man into two.</p>

        <h2>The case</h2>
        <p>A pioneer died in Michigan in 1912. The old county histories give him a plain first and last name. One of them adds "Senior." <a class="mk sm kC" href="/scrollmarks/#mk-county-history" title="What this mark means">County history</a></p>
        <p>His own death certificate, filed about a month after he died, gives the same plain name. No initial at all. <a class="mk sm kD" href="/scrollmarks/#mk-document" title="What this mark means">Document</a></p>
        <p>Then we found his son's death certificate, from 1935. In the box for the father's name, whoever answered the questions gave him a middle initial: the same one the son carried. <a class="mk sm kD" href="/scrollmarks/#mk-document" title="What this mark means">Document</a></p>
        <p>So which is right? Make your guess now. Ours is further down.</p>

        <h2>Then it got stranger</h2>
        <p>Once we started comparing every box, the records kept arguing.</p>
        <ul class="dis">
          <li><b>His birthday:</b> his death certificate and one of the county histories are two days apart.</li>
          <li><b>His father's birthplace:</b> the certificate names one state. That same history names another.</li>
        </ul>
        <p>One man, one family and three disagreements. Nobody lied. Each one is somebody's memory.</p>

        <h2>What this teaches</h2>
        <p><b>Every record was written by someone.</b> A death certificate tells you what the informant believed, on a hard day. Their name is usually on it. The father's was filed about a month after he died; the son's was filled in twenty-three years later, by someone remembering a man long gone. County histories have the same weakness: the family usually supplied the facts, often from memory, and nobody checked them.</p>
        <p><b>One letter can change everything.</b> Fathers and sons with the same name get tangled in the record all the time. One wrong initial can merge two men or split one, and send you chasing somebody else's family for a month.</p>
        <p><b>Watch out for "Senior."</b> In the 1800s it didn't always mean "father." Sometimes it only meant the older of two men with the same name in town, related or not. Here a son with the same name does turn up, so the label fits, but always check.</p>
        <p><b>Disagreement is a clue, not a failure.</b> Every mismatch tells you who was remembering, and when. Our guess, as promised: father and son shared a name, and in 1935 someone gave the father the son's initial too <a class="mk sm kR" href="/scrollmarks/#mk-reading" title="What this mark means">Reading</a>. But a guess is not proof.</p>

        <h2>Four rules for when records disagree</h2>
        <ol class="notes" style="padding-left:1.3rem">
          <li>Ask who gave the information, and when. Closer to the event usually weighs more, but not always.</li>
          <li>Keep looking. A third, independent record can tip the balance, but records are weighed, not counted.</li>
          <li>Write down both versions and where each came from. Never quietly "fix" one.</li>
          <li>Call it settled only when the evidence settles it. Until then, it's an open question.</li>
        </ol>

        <h2>Where the case stands</h2>
        <p><span class="status">Open</span> Our next witness: a local newspaper notice from the days or weeks after his death. Then his probate file, and the cemetery's burial records or a transcription of his stone. Read the stone on paper. Don't go to it.</p>

        <p class="mstrip"><i>Scrollmarks, strongest first:</i> <span class="tD">Document</span> <span class="tP">Period print</span> <span class="tC">County history</span> <span class="tM">Compiled</span> <span class="tT">Tradition</span> <span class="tF">Field (seen at first hand)</span> <span class="tI">Inference</span> <span class="tR">Reading</span> <span class="tH">Hypothesis</span> <i>— <a href="/scrollmarks/">what the marks mean</a></i></p>

        <h2>Where to look, for free</h2>
        <ul class="dis">
          <li><a href="https://michigan.access.preservica.com/death-certificates-1897-1952/">Archives of Michigan, death certificates 1897–1952</a>. Free; for most years you can open the certificate itself, in the original handwriting.</li>
          <li><a href="https://www.familysearch.org">FamilySearch</a>. Birth, marriage and death records from all over the world, free with an account.</li>
          <li><a href="https://michiganology.org/vital-records/">Michiganology: vital records</a>. The State of Michigan’s own index to its births, marriages and deaths.</li>
          <li><a href="https://quod.lib.umich.edu/m/micounty/">Michigan County Histories and Atlases</a>. The University of Michigan’s free scans of the county histories, Rogers, Mathews and Glover among them.</li>
          <li><a href="https://www.findagrave.com">Find a Grave</a>. Free transcriptions and photographs of gravestones. Read the stone on paper.</li>
        </ul>
        <p><b>Tip:</b> read every box, including the small print at the bottom. Ages are often given to the day, in years, months and days. Count back from the date of death and you have a birth date to check against everything else. Just remember the informant gave that age too.</p>
        <p><a class="btn dl" href="/worksheet/project-scroll-hunters-worksheet.pdf" download><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12m0 0-5-5m5 5 5-5M4 20h16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>The hunter's worksheet (PDF)</a></p>

        <h2>Your turn</h2>
        <p>Pick someone in your family who died long ago. Find two records that name them and compare every box: name, dates, parents, birthplaces. Do they disagree? Which would you believe, and why? The best mysteries start at home.</p>
        <p>Want to test yourself first? <a href="/notes/from-the-desk/#try">Try the two-record puzzle</a>. Got a mystery you can't crack? Write to <a href="mailto:research@projectscroll.com?subject=My%20mystery">research@projectscroll.com</a>, <a href="https://m.me/projectscroll">message us on Facebook</a>, or <a href="/#contact">start with a question</a>. Tell us how you did in the comments on <a href="https://www.facebook.com/projectscroll/">Project Scroll's page</a>.</p>
    ''', og='https://projectscroll.com/og/one-letter.jpg')

    page('notes/index.html','Field notes · Project Scroll',
     'Lessons from the Project Scroll research desk: how to read old records, weigh them against each other and know when a question is settled.',
    '''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">From the desk</p>
        <h1>Field notes</h1>
        <p>Short lessons from real cases: how to read an old record, weigh it against another, and know when a question is settled. A new lesson is bound in each time a case teaches one.</p>
        <p><a class="btn" href="/notes/book/">Open the field notes as a book</a></p>
    <aside class="notes-lesson" aria-labelledby="nlH"><p class="nl-k">From the desk · Lesson No. 1</p><h2 id="nlH">Two old records, two different stories</h2><p>What to do when the records disagree, with the person of the month, the tools of the trade, and a record to weigh yourself.</p><p><a class="btn primary" href="/notes/from-the-desk/">Read Lesson No. 1</a> <a class="btn" href="/notes/from-the-desk/#try">Try the two-record puzzle</a></p></aside>
    <aside class="whatsnew" aria-labelledby="wnH"><h2 id="wnH">New on the site</h2><ul>'''+''.join(f'<li><time datetime="{_d}">{_dt.date.fromisoformat(_d).strftime("%-d %b")}</time> <a href="{_u}">{_html.escape(_t)}</a> <span>{_html.escape(_s)}</span></li>' for _d,_u,_t,_s in _json.load(open(pathlib.Path(__file__).parent/'data'/'whatsnew.json'))[:8])+'''</ul></aside>
    <ul class="notelist">
          <li><a href="/notes/one-letter-two-certificates/">One Letter, Two Certificates</a><span>No. 1 · 17 October 2026 · What to do when two old records tell you two different things.</span></li>
        </ul>
            <h2>Still open at the desk</h2>
    <ul class="dis">
      <li><b>Case 10.</b> The next witnesses are a local newspaper notice from the weeks after the pioneer’s death, his probate file, and the cemetery’s burial record.</li>
      <li><b>Person of the month.</b> James M. Shepard was three in 1846. Who told him the lodge’s story?</li>
      <li><b>Case 1.</b> Did the joke lodge’s charter ever exist as a document, or only as a word in a retelling?</li>
    </ul>
    <p class="note">When one is answered, it becomes a field note.</p>
<p><a class="btn dl" href="/worksheet/project-scroll-hunters-worksheet.pdf" download><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12m0 0-5-5m5 5 5-5M4 20h16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>The hunter's worksheet (PDF)</a></p>
    ''', og='https://projectscroll.com/og/notes.jpg')

    page('404.html','Not in the record · Project Scroll','This page is not in the record.',
    '''    <p class="kicker">Error 404</p>
        <h1>Not in the record.</h1>
        <p class="lede" style="font-size:1.2rem">We searched the index, the margins and the back pages. This page isn't here.</p>
        <p class="foolsgold"><span class="fg-pan" aria-hidden="true"></span><b>Fool’s gold.</b> It glitters, but it isn’t here: a forty-niner would call this one pyrite.</p>
        <p>It may have moved, or it may never have existed. A good record-keeper is honest about both. Press <kbd>/</kbd> to search the site, or pick up the trail below.</p>
        <aside class="lostq" aria-labelledby="lqH"><h2 id="lqH">While you are lost</h2><p>Pages go missing; so do towns. The 1860 wall map has a little plan of a Berrien County village that was called simply “Berrien”. What is it called today?</p>
          <form class="lq-f" autocomplete="off"><label for="lqIn">Its name today</label><input id="lqIn" type="text" maxlength="40" spellcheck="false"><button class="btn" type="submit">Check</button></form><p class="lq-out" aria-live="polite"></p></aside>
        <script>(function(){ var f=document.querySelector('.lq-f'); if(!f) return; var h=function(s){ var x=5381; for(var i=0;i<s.length;i++) x=((Math.imul(x,33))^s.charCodeAt(i))>>>0; return x; };
          f.addEventListener('submit',function(e){ e.preventDefault(); var v=document.getElementById('lqIn').value.toLowerCase().replace(/[^a-z]/g,''), o=document.querySelector('.lq-out');
            if (h(v)===554842722) o.innerHTML='Found it, and so are you. <a href="/map/#town-berrien">See the 1860 plan of Berrien in the map room →</a>'; else o.textContent='Not that one. It sits on the St. Joseph River, and today it carries a second word.'; }); })();</script>
        <p class="ctas" style="margin-top:1.6rem"><a class="btn primary" href="/">Back to the first page</a><a class="btn" href="/cases/">See the case board</a></p>
    ''', noindex=True)
    print('pages written')
