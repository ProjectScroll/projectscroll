// Inlines each page's above-the-fold CSS and makes the full stylesheet non-blocking.
// Run after the stamp:  NODE_PATH=$(npm root -g) node _tools/critical.js   (needs the static server on PORT, default 8765,
// and postcss on NODE_PATH or in POSTCSS_DIR). For every page, the browser says which selectors style anything on the
// first screen (phone and desktop); the rule text itself is taken from site.min.css by PostCSS, so modern syntax
// (color-mix, light-dark, nesting) survives untouched. site.min.css then loads as a print sheet (never blocks paint)
// and site.js switches it to "all".
const {chromium}=require('playwright'); const fs=require('fs'), path=require('path');
const postcss=require(process.env.POSTCSS_DIR ? path.join(process.env.POSTCSS_DIR,'postcss') : 'postcss');
const R=path.resolve(__dirname,'..'), PORT=process.env.PORT||8765;
const pages=fs.readFileSync(path.join(__dirname,'pages.txt'),'utf8').split('\n').map(s=>s.trim().replace(/^\.\//,'')).filter(Boolean);
// the news pages and the hunt are made by build_news.py; take them all, so new stories get a first screen too
for (const extra of ['hunt/index.html','news/index.html'].concat(fs.readdirSync(path.join(R,'news'),{withFileTypes:true}).filter(d=>d.isDirectory()&&fs.existsSync(path.join(R,'news',d.name,'index.html'))).map(d=>'news/'+d.name+'/index.html'))) if (!pages.includes(extra)) pages.push(extra);
const VIEWS=[{width:412,height:915},{width:1280,height:900}];
const JSMADE=/\.(gl|glw|gloss|whisper|w-l|navink|listen|btoast|bt-x|diamond|riddle|fresh|mh-[a-z]+|totop|consent|keyhint|partrail|fp-zoom|search-res|mic|tl-thread|nextmk|touched|has-navink|lamp)\b|\[popover\]|html\.(ink|reveal|has-navink|lamp)/;
// the stylesheet as a flat list: [{wrap:[...conditions], sel, text}] in source order, plus the at-rules kept whole
const root=postcss.parse(fs.readFileSync(path.join(R,'site.min.css'),'utf8'));
const flat=[];
const walk=(node, wrap)=>{ node.each(n=>{
  if (n.type==='rule') flat.push({wrap, sel:n.selector, text:n.toString()});
  else if (n.type==='atrule' && (n.name==='media'||n.name==='supports'||n.name==='container')) walk(n, wrap.concat('@'+n.name+' '+n.params));
  else if (n.type==='atrule' && (n.name==='font-face'||n.name==='property'||n.name==='view-transition'||n.name==='layer')) flat.push({wrap, sel:null, text:n.toString(), always:true});
  else if (n.type==='atrule' && n.name==='keyframes') flat.push({wrap, sel:null, text:n.toString(), kf:n.params});
}); };
walk(root, []);
const selectors=[...new Set(flat.filter(f=>f.sel).map(f=>f.sel))];
(async()=>{
  const b=await chromium.launch(); let total=0;
  for (const rel of pages){
    const url='http://localhost:'+PORT+'/'+rel.replace(/index\.html$/,'');
    const hit=new Set();
    for (const v of VIEWS){
      const p=await b.newPage({viewport:v}); await p.route('**tile.loc.gov**', r=>r.abort());
      await p.goto(url,{waitUntil:'load'});
      const found=await p.evaluate(({sels, vh, jsmade})=>{
        const JS=new RegExp(jsmade); const limit=vh*1.25, out=[];
        const strip=s=>s.replace(/::?[a-zA-Z-]+(\([^()]*(\([^()]*\))?[^()]*\))?/g,'').replace(/\s*[>+~]\s*$/,'').trim();
        const near=sel=>{ try{ for (const e of document.querySelectorAll(sel)){ const r=e.getBoundingClientRect(); if (r.top<limit && r.bottom>-50 && (r.width||r.height)) return true; } }catch(e){} return false; };
        for (const sel of sels){ const parts=sel.split(/\s*,\s*/); const keep=parts.filter(s=>{ const t=strip(s); if (!t||t===':root'||t==='html'||t==='body'||t==='*'||/^html\[|^:root\[|^html\.|^:root:/.test(t)) return true; if (JS.test(s)) return true; return near(t); }); if (keep.length) out.push([sel, keep.length===parts.length?null:keep.join(',')]); }
        return out;
      }, {sels:selectors, vh:v.height, jsmade:JSMADE.source});
      for (const [sel, partial] of found){ const prev=hit.get?null:null; if (!hit.has(sel) || partial===null) hit.add(sel); if (partial) hit.add(sel+'\u0000'+partial); }
      await p.close();
    }
    // which partial selector lists to use (full wins if ever full)
    const partialFor={}; for (const h of hit){ if (h.includes('\u0000')){ const [s,pp]=h.split('\u0000'); if (!hit.has(s)) partialFor[s]=pp; } }
    const kept=flat.filter(f=>f.always || (f.sel && (hit.has(f.sel) || partialFor[f.sel])));
    const used=new Set(); kept.forEach(f=>{ const m=f.text.match(/animation(?:-name)?:\s*([^;}]+)/g); if (m) m.forEach(x=>x.replace(/animation(?:-name)?:\s*/,'').split(',').forEach(n=>{ const nm=n.trim().split(/\s+/).find(k=>/^[a-zA-Z_-][\w-]*$/.test(k)&&!/^(linear|ease|ease-in|ease-out|ease-in-out|infinite|both|forwards|backwards|alternate|normal|reverse|none|paused|running)$/.test(k)); if (nm) used.add(nm); })); });
    const all=kept.concat(flat.filter(f=>f.kf && used.has(f.kf)));
    all.sort((a,b)=>flat.indexOf(a)-flat.indexOf(b));
    let css='', cur=null; for (const f of all){ const text=(f.sel && partialFor[f.sel]) ? partialFor[f.sel]+f.text.slice(f.text.indexOf('{')) : f.text; const w=f.wrap.map(x=>x+'{').join(''); if (w!==cur){ if (cur!==null) css+='}'.repeat(cur.split('{').length-1); css+=w; cur=w; } css+=text; } if (cur!==null) css+='}'.repeat(cur.split('{').length-1);
    const file=path.join(R,rel); let html=fs.readFileSync(file,'utf8');
    html=html.replace(/<style id="crit">[\s\S]*?<\/style>\n?/,'').replace(/<noscript><link rel="stylesheet" href="\/site\.min\.css\?v=[^"]*"><\/noscript>\n?/,'');
    const m=html.match(/<link rel="stylesheet" href="(\/site\.min\.css\?v=[^"]*)"( media="print" data-full)?>/); if (!m){ console.log('skip', rel); continue; }
    html=html.replace(m[0], '<style id="crit">'+css+'</style>\n<link rel="stylesheet" href="'+m[1]+'" media="print" data-full>\n<noscript><link rel="stylesheet" href="'+m[1]+'"></noscript>');
    fs.writeFileSync(file, html); total+=css.length;
  }
  await b.close(); console.log('critical css: '+(total/1024/pages.length).toFixed(0)+' KB per page on average, '+pages.length+' pages');
})();
