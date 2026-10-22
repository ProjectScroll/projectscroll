"""Soldiers of the valley: Company D, Sixth Michigan Infantry, from Mathews (1882).  python3 _tools/build_soldiers.py"""
import sys, pathlib, json, html; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
E=html.escape
D=json.load(open(pathlib.Path(__file__).parent/'data'/'soldiers_6mi_d.json'))
ABBR=[('com.','commissioned'),('e.','enlisted'),('dis.','discharged'),('m. o.','mustered out'),('vet.','re-enlisted as a veteran'),('prom.','promoted'),('trans.','transferred'),('U. S. C. T.','United States Colored Troops')]
def fate(n):
    n=n.lower()
    if 'killed' in n or 'died of wounds' in n or 'of wounds' in n or 'died in action' in n: return 'k'
    if 'died' in n: return 'd'
    return ''
rows=''.join(f'<tr class="{fate(x["notes"])}"><td>{E(x["name"])}</td><td>{E(x["rank"])}</td><td>{E(x["notes"])}{" <span class=sic>[sic: Port Hudson was May 27, 1863]</span>" if "May 27, 1862" in x["notes"] else ""}</td><td>{E(x["page"])}</td></tr>' for x in D)
import re
MO={'Jan':1,'Feb':2,'March':3,'Mar':3,'April':4,'Apr':4,'May':5,'June':6,'July':7,'Aug':8,'Sept':9,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
EV=[]
for x in D:
    for cl in x['notes'].split(';'):
        for m in re.finditer(r'(Jan|Feb|March|Mar|April|Apr|May|June|July|Aug|Sept|Sep|Oct|Nov|Dec)\.? (\d{1,2}), (18\d\d)', cl):
            t=cl.strip().rstrip('.')
            if 'May 27, 1862' in t: t+=' [sic: Port Hudson was May 27, 1863]'
            EV.append([MO[m.group(1)], int(m.group(2)), int(m.group(3)), x['name'], x['rank'], t])
EVJ=json.dumps(EV, ensure_ascii=False)
k=sum(1 for x in D if fate(x['notes'])=='k'); dd=sum(1 for x in D if fate(x['notes'])=='d')
U='https://archive.org/details/bad0870.0001.001.umich.edu/page/'
body=f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">Soldiers of the valley</p>
    <h1>Company D, Sixth Michigan Infantry</h1>
    <p class="lede" style="font-size:1.15rem">In the summer of 1861 a company was raised at Dowagiac, the second organized in Cass County. Here are its {len(D)} men as the county history printed them in 1882: who they were, how they served, and how {k+dd} of them did not come home.</p>
    <h2>The company’s war</h2>
    <ul class="dis">
      <li><b>Raised at Dowagiac, summer 1861,</b> under Capt. Charles E. Clarke, with Frederick J. Clarke as first lieutenant. The regiment gathered at Kalamazoo and left for the East on 30 August 1861, 944 strong. <a href="{U}117" rel="noopener">Mathews, p. 117</a></li>
      <li><b>Baltimore, then the Mississippi.</b> After garrison duty at Baltimore it went to New Orleans and the lower Mississippi, fought at Baton Rouge on 5 August 1862, and in the assault on Port Hudson on 27 May 1863, where Lieutenant Frederick Clarke was killed. <a href="{U}117" rel="noopener">pp. 117–118</a></li>
      <li><b>Heavy artillery.</b> After Port Hudson the regiment became heavy artillery, served at Fort Morgan and in the siege of Mobile, and was paid off and discharged at Jackson, Michigan, on 5 September 1865. <a href="{U}118" rel="noopener">p. 118</a></li>
    </ul>
    <p>Of the men below, {k} were killed or died of wounds and {dd} died of disease: at Baltimore, New Orleans, Baton Rouge, Carrollton and, most of all, in the hot summer at Port Hudson. Disease killed more soldiers than battle in this war, and this company is no exception.</p>
    <aside class="sol-week" id="solWeek" hidden aria-labelledby="solWH"><h2 id="solWH">This week in Company D</h2><ul id="solWL"></ul><p class="note">From the roll below, as printed: commissions, enlistments, promotions, wounds and deaths that fell in this week of the year, in 1861 to 1865.</p></aside>
    <h2>The roll</h2>
    <p class="note">As printed in Mathews, pages 119–120, checked line by line against the page scans. Officers are listed first name first, privates surname first, as in the book. The men’s home townships are left off. Rows shaded red died in battle or of wounds; rows shaded grey died of disease.</p>
    <label class="nm-q"><span>Find a name</span><input type="search" id="solQ" placeholder="A surname" autocomplete="off" spellcheck="false"></label>
    <div class="tablewrap"><table class="roll" id="solT"><thead><tr><th scope="col">Name</th><th scope="col">Rank</th><th scope="col">Service, as printed</th><th scope="col">Page</th></tr></thead><tbody>{rows}</tbody></table></div>
    <h2>Reading the abbreviations</h2>
    <ul class="dis">{''.join(f'<li><b>{E(a)}</b> {E(b)}</li>' for a,b in ABBR)}</ul>
    <p class="note">A man in this roll is a lead. His service record and pension file at the National Archives can say far more: where he was wounded, who his widow was, where he lived after the war. A government headstone with a sunk shield marks many of these men’s graves; see <a href="/guide/gravestones/">reading old gravestones</a>. Source: Alfred Mathews, <i>History of Cass County, Michigan</i> (Chicago: Waterman, Watkins &amp; Co., 1882), pp. 117–120, read in the <a href="{U}119" rel="noopener">Internet Archive’s copy</a>. OCR errors were corrected against the scans; the book’s own date for Lieutenant Clarke’s death is kept as printed and marked.</p>
    <script>
    (function(){{ var EV={EVJ}, now=new Date(), y0=now.getFullYear(), doy=function(m,d){{ return Math.floor((new Date(2001,m-1,d)-new Date(2001,0,1))/864e5); }}, t=doy(now.getMonth()+1, now.getDate());
      var MN=['January','February','March','April','May','June','July','August','September','October','November','December'];
      var hit=EV.filter(function(e){{ var dd=doy(e[0],e[1])-t; if (dd<-3) dd+=365; return dd>=-3 && dd<=3; }}).sort(function(a,b){{ return a[2]-b[2] || a[0]-b[0] || a[1]-b[1]; }});
      if (!hit.length){{ hit=EV.map(function(e){{ var dd=doy(e[0],e[1])-t; if (dd<0) dd+=365; return [dd,e]; }}).filter(function(x){{ return x[0]<=31; }}).sort(function(a,b){{ return a[0]-b[0]; }}).slice(0,4).map(function(x){{ return x[1]; }}); if (hit.length) document.getElementById('solWH').textContent='Coming up in Company D'; }}
      if (hit.length){{ var ul=document.getElementById('solWL'); hit.slice(0,10).forEach(function(e){{ var li=document.createElement('li'); li.innerHTML='<b></b> <span></span> <i></i>'; li.children[0].textContent=e[1]+' '+MN[e[0]-1]+' '+e[2]+' ('+(y0-e[2])+' years ago).'; li.children[1].textContent=e[4]+' '+e[3]+':'; li.children[2].textContent='“'+e[5]+'”'; ul.appendChild(li); }}); document.getElementById('solWeek').hidden=false; }}
    }})();
    (function(){{ var q=document.getElementById('solQ'), rs=[].slice.call(document.querySelectorAll('#solT tbody tr'));
      q.addEventListener('input', function(){{ var v=q.value.trim().toLowerCase(); rs.forEach(function(r){{ r.hidden=v && r.firstChild.textContent.toLowerCase().indexOf(v)<0; }}); }}); }})();
    </script>
'''
page('soldiers/index.html','Company D, Sixth Michigan Infantry · Soldiers of the valley · Project Scroll',f'The {len(D)} men of Company D, Sixth Michigan Infantry, raised at Dowagiac in 1861, as Mathews printed them in 1882: rank, service, and who did not come home.',body,og='https://projectscroll.com/og/records.jpg')
print('soldiers built',len(D),k,dd)
