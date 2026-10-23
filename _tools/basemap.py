"""The modern base map under every Leaflet map on the site: the USGS National Map (public domain, no key, no tracking).
  Map   = USGS Topo: town names, highways, roads and street names, lakes and rivers
  Photo = USGS aerial photographs; PHOTO_NAMES adds the names over them
  Plain = nothing from outside: only the site's own county lines and rivers

BASE_JS defines window.psBase(map, box, group, first): box gets class "osm" while tiles show (so the site's own
county fills turn clear); group is a container of <button data-base="topo|photo|plain"> made by buttons()."""

SERVICES = {'topo': 'USGSTopo', 'photo': 'USGSImageryOnly', 'photonames': 'USGSImageryTopo'}
CREDIT = 'Base map: <a href="https://www.usgs.gov/programs/national-geospatial-program/national-map">USGS The National Map</a>'

def buttons(first='topo', ids='', opts=(('topo', 'Map'), ('photo', 'Photo'), ('plain', 'Plain'))):
    """the little Map | Photo | Plain switch"""
    b = ''.join(f'<button type="button" data-base="{k}" aria-pressed="{str(k == first).lower()}">{t}</button>' for k, t in opts)
    return f'<span class="ps-base" role="group" aria-label="Base map" hidden{(" id=" + chr(34) + ids + chr(34)) if ids else ""}>{b}</span>'

BASE_JS = r'''
window.psBase=window.psBase||function(map, box, group, first){
  var U='https://basemap.nationalmap.gov/arcgis/rest/services/', S={topo:'USGSTopo', photo:'USGSImageryOnly', photonames:'USGSImageryTopo'}, L1={}, cur='plain';
  var CR='Base map: <a href="https://www.usgs.gov/programs/national-geospatial-program/national-map">USGS The National Map</a>';
  var pane=map.getPane('psbase')||map.createPane('psbase'); pane.style.zIndex=150;
  var set=function(k){ if (k===cur) return; if (L1[cur]) map.removeLayer(L1[cur]); cur=k;
    if (S[k]){ if (!L1[k]) L1[k]=L.tileLayer(U+S[k]+'/MapServer/tile/{z}/{y}/{x}',{pane:'psbase', maxNativeZoom:16, maxZoom:20, attribution:CR, crossOrigin:false}); L1[k].addTo(map); }
    if (box) box.classList.toggle('osm', !!S[k]); if (box) box.classList.toggle('photo', k==='photo'||k==='photonames');
    map.fire('psbase',{base:k});
    if (group) [].forEach.call(group.querySelectorAll('[data-base]'),function(b){ b.setAttribute('aria-pressed', String(b.dataset.base===k || (k==='photonames' && b.dataset.base==='photo'))); }); };
  if (group){ group.hidden=false; group.addEventListener('click',function(e){ var b=e.target.closest('[data-base]'); if (b) set(b.dataset.base); }); }
  set(first||'topo');
  return {set:set, get:function(){ return cur; }};
};
'''
