"""Old postcards pinned on the map room: one pin per town, the town's cards in its popup."""
import json, html
from oldcards import D, slug, credit
E = lambda s: html.escape(s or '', quote=True)
LL = {'Cassopolis':(41.9065,-86.0127),'Dowagiac':(41.9836,-86.1061),'Edwardsburg':(41.7984,-86.0847),'Marcellus':(42.0245,-85.8152),'Vandalia':(41.9191,-85.933),
 'Union (Cass County)':(41.783,-85.867),'Penn (Cass County)':(41.95,-85.925),'Adamsville (Cass County)':(41.7853,-85.9939),'Adamsville':(41.7853,-85.9939),
 'Niles':(41.8296,-86.2528),'Berrien Springs':(41.948,-86.3404),'Benton Harbor':(42.119,-86.4466),'Benton Harbor / St. Joseph':(42.113,-86.47),'St. Joseph':(42.1161,-86.4935),
 'Coloma':(42.1814,-86.3126),'Coloma (Paw Paw Lake)':(42.2,-86.27),'Paw Paw':(42.2178,-85.8911),'South Haven':(42.4065,-86.2743),'Three Rivers':(41.9448,-85.6336),
 'Constantine':(41.8397,-85.6647),'Kalamazoo':(42.2765,-85.607),'South Bend':(41.6758,-86.2521),'South Bend / Mishawaka':(41.67,-86.2),'Mishawaka':(41.6642,-86.1102),
 'Elkhart':(41.6932,-85.9734),'Goshen':(41.5856,-85.8343),'Bristol':(41.7217,-85.8202),'La Porte':(41.5955,-86.7082),'Michigan City':(41.7148,-86.9028)}
def section():
    towns = {}
    for d in D:
        ll = LL.get(d['place'])
        if not ll: continue
        key = '%.3f,%.3f' % ll
        t = towns.setdefault(key, {'ll': ll, 'n': d['place'].split(' (')[0].split(' / ')[0], 'c': []})
        t['c'].append([d['id'], d['title'], d.get('date') or ''])
    data = json.dumps(list(towns.values()), ensure_ascii=False, separators=(',',':')).replace('</','<\\/')
    js = r'''<script>
(function(){ "use strict";
  var box=document.getElementById('pcMap'); if (!box) return; var T=__T__, map=null;
  var start=function(){ if (map || !window.L) return; box.querySelector('.mu-mapph') && box.querySelector('.mu-mapph').remove();
    map=L.map(box,{zoomSnap:.25, minZoom:7, maxZoom:14, scrollWheelZoom:false, maxBounds:[[40.9,-87.9],[42.95,-84.3]]}); map.attributionControl.setPrefix(false);
    map.fitBounds([[41.5,-86.95],[42.45,-85.55]]);
    map.on('focus click',function(){ map.scrollWheelZoom.enable(); }); map.on('blur mouseout',function(){ map.scrollWheelZoom.disable(); });
    fetch('/museums/base.json?v=1').then(function(r){ return r.json(); }).then(function(b){ var pane=map.createPane('base'); pane.style.zIndex=250;
      b.c.forEach(function(c){ c.r.forEach(function(r){ L.polygon(r.map(function(p){ return [p[1],p[0]]; }),{pane:'base', className:c.d?'mu-cty in':'mu-cty', interactive:false}).addTo(map); }); });
      b.v.forEach(function(l){ L.polyline(l.map(function(p){ return [p[1],p[0]]; }),{pane:'base', className:'mu-rv', interactive:false}).addTo(map); });
      map.attributionControl.addAttribution('County lines: US Census Bureau · Rivers: USGS'); }).catch(function(){});
    T.forEach(function(t){ var n=t.c.length, r=Math.min(16, 6+Math.sqrt(n)*2.4);
      var c=L.circleMarker(t.ll,{radius:r, className:'pc-pin', bubblingMouseEvents:false}).addTo(map);
      c.bindTooltip(t.n+': '+n+(n===1?' picture':' pictures'),{direction:'top', offset:[0,-r]});
      c.on('click',function(){ var div=document.createElement('div'); div.className='pc-pop';
        var h=document.createElement('p'); h.className='pc-ph'; h.textContent=t.n+' on old postcards'; div.appendChild(h);
        var g=document.createElement('div'); g.className='pc-pg';
        t.c.slice(0,6).forEach(function(x){ var a=document.createElement('a'); a.href='/postcards/#oc-'+x[0]; a.title=x[1]+(x[2]?' · '+x[2]:''); var im=document.createElement('img'); im.src='/img/oldcards/'+x[0]+'-700.webp'; im.alt=x[1]; im.loading='lazy'; im.width=120; im.height=80; a.appendChild(im); g.appendChild(a); });
        div.appendChild(g); var m=document.createElement('a'); m.className='pc-more'; m.href='/postcards/?q='+encodeURIComponent(t.n.toLowerCase())+'#valley'; m.textContent=(n>6?'See all '+n:'See them')+' in the gallery ›'; div.appendChild(m);
        c.bindPopup(div,{maxWidth:300, minWidth:260}).openPopup(); }); });
  };
  var need=function(){ if (window.L){ start(); return; } if (need.on) return; need.on=1;
    if (!document.querySelector('link[href*="leaflet.css"]')){ var l=document.createElement('link'); l.rel='stylesheet'; l.href='/vendor/leaflet-1.9.4/leaflet.css?v=1'; document.head.appendChild(l); }
    var s=document.createElement('script'); s.src='/vendor/leaflet-1.9.4/leaflet.js?v=1'; s.onload=start; document.head.appendChild(s); };
  if ('IntersectionObserver' in window){ var io=new IntersectionObserver(function(e){ if (e.some(function(x){ return x.isIntersecting; })){ io.disconnect(); need(); } },{rootMargin:'300px'}); io.observe(box); } else need();
})();
</script>'''.replace('__T__', data)
    total = len(D)
    return (f'''    <section class="pcmap" id="pcmap" aria-labelledby="pcmH">
      <h2 id="pcmH">Old postcards on the map</h2>
      <p>{total} old postcards and photographs of {len(towns)} towns, each pinned where it was taken. Press a town to see its pictures, then open any one in the <a href="/postcards/">postcards gallery</a>.</p>
      <div class="mu-map pc-map" id="pcMap" role="region" aria-label="Map of the towns on the old postcards. Every picture is also in the postcards gallery."><p class="mu-mapph">The map loads here.</p></div>
    </section>
''' + js + '\n')
