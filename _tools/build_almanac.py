"""This day in the valley: dated events from the county histories, each with its book and page.
python3 _tools/build_almanac.py"""
import sys, pathlib, json, html; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page, R
d=json.load(open(pathlib.Path(__file__).parent/'data'/'almanac_raw.json'))
d.sort(key=lambda x:(x['md'],x['year']))
out=[{'md':x['md'],'y':x['year'],'p':x['place'],'t':x['text'],'s':x['source'],'pg':x['page'],'u':x['url']} for x in d]
pathlib.Path(R,'almanac.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')))
M=['January','February','March','April','May','June','July','August','September','October','November','December']
secs=[]
for i,mn in enumerate(M):
    items=[x for x in out if int(x['md'][:2])==i+1]
    if not items: continue
    lis=''.join(f'<li id="d-{x["md"]}-{x["y"]}"><span class="al-d">{int(x["md"][3:])} {mn}, {x["y"]}</span> <b>{html.escape(x["p"])}.</b> {html.escape(x["t"])} <a class="al-s" href="{html.escape(x["u"])}" rel="noopener">{html.escape(x["s"])}, p. {html.escape(x["pg"])}</a></li>' for x in items)
    secs.append(f'    <h2 id="{mn.lower()}">{mn}</h2>\n    <ol class="alm">{lis}</ol>')
jump=' · '.join(f'<a href="#{m.lower()}">{m[:3]}</a>' for m in M)
body=f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">This day in the valley</p>
    <h1>The valley’s almanac</h1>
    <p class="lede" style="font-size:1.15rem">{len(out)} days the county histories remember to the date: a first train, a first newspaper, a fire, a charter, a church dedicated. Every one carries the book and page it comes from, so you can open the record and read it yourself.</p>
    <p class="al-today" id="alToday" aria-live="polite"></p>
    <p class="note al-jump">{jump}</p>
{chr(10).join(secs)}
    <p class="note">From Rogers’s <i>History of Cass County</i> (1875), Mathews’s <i>History of Cass County, Michigan</i> (1882), Glover’s <i>Twentieth Century History of Cass County</i> (1906), the <i>History of Berrien and Van Buren Counties</i> (1880), and Chapman’s histories of St. Joseph County, Indiana (1880) and Elkhart County, Indiana (1881), read in the Internet Archive’s copies. Where two books disagree on a date, the entry says so. The books themselves can be wrong; see <a href="/sources/">the sources shelf</a>.</p>
    <script>
    (function(){{ var n=new Date(), md=('0'+(n.getMonth()+1)).slice(-2)+'-'+('0'+n.getDate()).slice(-2); var el=[].slice.call(document.querySelectorAll('.alm li')).filter(function(li){{ return li.id.slice(2,7)===md; }}); var t=document.getElementById('alToday');
      if (el.length){{ el.forEach(function(li){{ li.classList.add('today'); }}); t.innerHTML='Today’s date is in the almanac. <a href="#'+el[0].id+'">See what happened on this day →</a>'; }} }})();
    </script>
'''
body += '''    <aside class="follow-box" aria-label="Follow along"><p><b>Never miss the next one.</b> New pages, papers and dates are announced on <a href="https://www.facebook.com/projectscroll/" rel="noopener">Project Scroll on Facebook</a> the day they go up, and in the site’s <a href="/feed.xml">news feed</a> for feed readers.</p></aside>
'''

page('almanac/index.html','The valley’s almanac · This day in the valley · Project Scroll',f'{len(out)} dated days from the county histories of the St. Joseph River Valley, each with its book and page: first trains, first newspapers, fires, charters and dedications.',body,og='https://projectscroll.com/og/records.jpg')
print('almanac built:',len(out),'days')
