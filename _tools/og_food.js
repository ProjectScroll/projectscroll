// Draws the colourful 1200x630 share cards for the food, sponsor and advertise pages into /og/:  NODE_PATH=$(npm root -g) node _tools/og_food.js
const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
const R=path.resolve(__dirname,'..'); const F=f=>'file://'+path.join(R,'fonts',f);
const PC=k=>'file://'+path.join(R,'img/oldcards',k+'-700.webp'); const FD=k=>'file://'+path.join(R,'img/food',k+'.webp');
// slug, kicker, title, line, main picture, its position, insets [[src, css]]
const CARDS=[
 ['food','Food, recipes & lodging','Eat, stay and cook in the valley','Places with a story, inns with a past, and recipes from the old cookbooks.',PC('ps052'),'center 45%',
   [[PC('ps050'),'left:-34px;bottom:26px;width:300px;transform:rotate(-4deg)']]],
 ['food-eat','Food, recipes & lodging','Places to eat with a story','Old banks and depots, stagecoach taverns, soda fountains, orchards and cider mills.',PC('ps057'),'left center',
   [[PC('ps051'),'right:26px;bottom:26px;width:290px;transform:rotate(3deg)']]],
 ['food-stay','Food, recipes & lodging','Places to stay in the valley','Inns and bed & breakfasts in houses with a past, each chosen for its history.',PC('ps053'),'center 50%',
   [[PC('ps091'),'left:-30px;bottom:24px;width:230px;transform:rotate(-3.5deg)']]],
 ['food-recipes','The valley kitchen','Old recipes, word for word','From the cookbooks and newspapers of the valley, 1896 to 1921, with notes for today’s kitchen.',PC('ps050'),'center 50%',
   [[FD('cover-three-rivers'),'left:40px;top:52px;width:200px;transform:rotate(-7deg)'],[FD('cover-dr-miles'),'left:150px;bottom:48px;width:300px;transform:rotate(4deg)']]],
 ['sponsor-and-advertise','Support the work','Sponsor & advertise','Two ways to be part of a free local-history hunt: pay for the research, or take a labeled place for your business.',PC('ps051'),'center 60%',
   [[PC('ps053'),'right:26px;bottom:26px;width:270px;transform:rotate(3deg)']]],
 ['advertise','For businesses in the valley','Advertise with Project Scroll','Partner cards, seasonal spots, Facebook features, passport stops and hunt prizes. Every paid place labeled.',PC('ps091'),'center 35%',
   [[FD('cover-dr-miles'),'right:30px;bottom:30px;width:280px;transform:rotate(4deg)']]],
 ['valley-map','The whole valley','The valley map','Museums, food, lodging, festivals, walks, lost towns and old town plans, all on one map.','file://'+path.join(R,'img/bellin-great-lakes-1744-1000.jpg'),'60% 70%',
   [[PC('ps051'),'right:26px;bottom:26px;width:260px;transform:rotate(3deg)'],[PC('ps053'),'left:-30px;top:40px;width:200px;transform:rotate(-4deg)']]],
];
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
(async()=>{const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1200,height:630}});
for (const [slug,k,t,d,pic,pos,ins] of CARDS){
 const size=t.length>28?64:72;
 const tmp=path.join(require('os').tmpdir(),'ps-ogf.html'); fs.writeFileSync(tmp,`<html><head><style>
 @font-face{font-family:D;src:url(${F('libre-caslon-display-latin-400-normal.woff2')})}
 @font-face{font-family:T;src:url(${F('libre-caslon-text-latin-400-normal.woff2')})}
 html,body{margin:0;width:1200px;height:630px;overflow:hidden}
 body{background:#F5ECD9;color:#2A1F17;font-family:T,serif;display:flex;position:relative}
 .t{width:560px;box-sizing:border-box;padding:62px 40px 46px 64px;display:flex;flex-direction:column;position:relative;z-index:2;
    background:linear-gradient(180deg,#F8F0DE,#F1E3C6)}
 .band{position:absolute;left:0;top:0;bottom:0;width:14px;background:repeating-linear-gradient(180deg,#B3362B 0 28px,#E9B949 28px 56px,#4E7A3A 56px 84px)}
 .k{font-size:21px;letter-spacing:.14em;text-transform:uppercase;color:#A6301F}
 .h{font-family:D;font-size:${size}px;line-height:1.04;margin:20px 0 18px;color:#2A1F17}
 .d{font-size:26px;line-height:1.36;color:#5A4A3C;margin:0 0 auto}
 .f{display:flex;justify-content:space-between;align-items:flex-end;border-top:1.5px solid #CDB58C;padding-top:14px;font-size:20px;color:#5A4A3C}
 .f b{font-family:D;font-weight:400;font-size:28px;color:#2A1F17}
 .pic{flex:1;position:relative;background:url(${pic}) ${pos}/cover}
 .pic:after{content:"";position:absolute;inset:0;box-shadow:inset 18px 0 30px -12px rgba(60,30,10,.35)}
 .in{position:absolute;border:7px solid #fffaf0;box-shadow:0 10px 26px rgba(0,0,0,.45);z-index:3}
 .in img{display:block;width:100%}
 </style></head><body><div class="t"><div class="band"></div><div class="k">${esc(k)}</div><div class="h">${esc(t)}</div><div class="d">${esc(d)}</div>
 <div class="f"><span><b>Project Scroll</b></span><span>projectscroll.com</span></div></div>
 <div class="pic">${ins.map(([s,c])=>`<div class="in" style="${c}"><img src="${s}"></div>`).join('')}</div></body></html>`);
 await p.goto('file://'+tmp); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
 await p.screenshot({path:path.join(R,'og',slug+'.jpg'),type:'jpeg',quality:86}); }
await b.close(); console.log('food share cards drawn',CARDS.length);})();
