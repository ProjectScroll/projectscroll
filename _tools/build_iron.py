"""Roads, rails, bridges and mills: how the valley was joined.  python3 _tools/build_iron.py"""
import sys, pathlib, json, html; sys.path.insert(0, str(pathlib.Path(__file__).parent)); sys.path.insert(0, str(pathlib.Path(__file__).parent/'data'))
from pages import page
from directories import DIRS
A=json.load(open(pathlib.Path(__file__).parent/'data'/'almanac_raw.json'))
M=['January','February','March','April','May','June','July','August','September','October','November','December']
KEY=('rail','train','iron was laid','plank','bridge','canal')
ev=sorted([x for x in A if any(k in (x['text']+' '+x['quote']).lower().replace('bainbridge','') for k in KEY)], key=lambda x:(x['year'],x['md']))
lis=''.join(f'<li><span class="al-d">{int(x["md"][3:])} {M[int(x["md"][:2])-1]} {x["year"]}</span> <b>{html.escape(x["place"])}.</b> {html.escape(x["text"])} <a class="al-s" href="{html.escape(x["url"])}" rel="noopener">{html.escape(x["source"])}, p. {html.escape(x["page"])}</a></li>' for x in ev)
mills=[]
for k,d in DIRS.items():
    for hd,nm,nt in d['entries']:
        if 'mill' in (hd+' '+nt).lower() or 'furnace' in (hd+' '+nt).lower() or 'machin' in (hd+' '+nt).lower():
            mills.append(f'<li><b>{html.escape(nm.rstrip("?"))}</b>, {html.escape(nt or hd)} <span class="nm-h">{d["name"]}, {d["year"]}</span></li>')
TN=[('niles','Niles','the Michigan Central, its depot on the river, and the mill race'),('dowagiac','Dowagiac','the Michigan Central on its long diagonal, the freight house and Herndon Mills'),('goshen','Goshen','the railroad and its Depot Grounds, the race and Rock Run'),('elkhart','Elkhart','the Michigan Southern &amp; Northern Indiana and its Goshen branch'),('south-bend','South Bend','the bend of the river and its bridges')]
tn=''.join(f'<li><a href="/map/{s}/">{n}</a>: {w}</li>' for s,n,w in TN)
body=f'''    <p class="crumb"><a href="/map/">← The map room</a></p>
    <p class="kicker">Roads, rails, bridges and mills</p>
    <h1>How the valley was joined</h1>
    <p class="lede" style="font-size:1.15rem">First came the canals that were never dug and the plank roads that were. Then the bridges over the St. Joseph, and at last the iron road, which decided which towns would grow and which would wait. Here it is in the order it happened, each date from the county histories with its page.</p>
    <h2>The dates</h2>
    <ol class="alm">{lis}</ol>
    <h2>See it on the old plans</h2>
    <p>The railroads are drawn on the town plans, and today’s tracks are drawn under them. Fade between the two:</p>
    <ul class="dis">{tn}</ul>
    <h2>The mills and works in the directories</h2>
    <p>Water and steam turned the valley’s mills. These are the millers, founders and machinists who paid to be listed beside the town plans of 1860 and 1861. See them all in <a href="/names/">who was in town</a>.</p>
    <ul class="nm-list">{''.join(mills)}</ul>
    <p class="note">Dates from the county histories listed on <a href="/sources/">the sources shelf</a>, read in the Internet Archive’s copies; the mills from the business directories beside the town plans. The more dates in <a href="/almanac/">the valley’s almanac</a>.</p>
'''
page('roads-and-rails/index.html','How the valley was joined · Roads, rails, bridges and mills · Project Scroll','Canals, plank roads, bridges, railroads and mills of the St. Joseph River Valley, in the order they came, each date from the county histories with its page.',body,og='https://projectscroll.com/og/map.jpg')
print('roads and rails built:',len(ev),'dates,',len(mills),'mills')
