"""Builds the map room:  python3 tools/build_map.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
IIIF='https://tile.loc.gov/image-services/iiif/service:gmd:gmd411:g4113:g4113c:la000324'
body=f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">The map room</p>
    <h1>The 1860 wall map</h1>
    <p class="lede" style="font-size:1.15rem">In 1860 Geil, Harley &amp; Siverd of Philadelphia engraved a great wall map of Cass, Van Buren and Berrien counties, Michigan: every township, the farms and the names of the people on them, with little town plans and pictures of houses around the border. The original is at the Library of Congress. Here you can walk over every inch of it.</p>
    <p class="note">Drag to move. Scroll, pinch or use the buttons to zoom. Nothing is marked: the hunt is yours.</p>
    <p class="tnpromo"><b>Then and now:</b> the 1860 town plans laid over today’s streets: <a href="/map/cassopolis/">Cassopolis</a> · <a href="/map/niles/">Niles</a> · <a href="/map/dowagiac/">Dowagiac</a> · <a href="/map/paw-paw/">Paw Paw</a></p>
  <div class="maproom">
    <div class="mapbar">
      <button type="button" class="btn" id="mzin" aria-label="Zoom in">+</button><button type="button" class="btn" id="mzout" aria-label="Zoom out">−</button><button type="button" class="btn" id="mhome">Whole map</button><button type="button" class="btn" id="mfull">Full screen</button>
      <span class="mapstat" id="mstat" aria-live="polite">Loading the map from the Library of Congress…</span>
    </div>
    <div id="osd" class="osd" role="application" aria-label="Zoomable 1860 wall map of Cass, Van Buren and Berrien counties"></div>
  </div>
    <h2>Things to look for</h2>
    <ul class="dis">
      <li>The small <b>town plans</b> along the top and left side, with streets, blocks and the names of buildings.</li>
      <li>The <b>business directories</b> printed in the margins, listing who kept which shop or hotel.</li>
      <li>The <b>engraved houses</b> around the border: the proudest farms and homes of 1860.</li>
      <li>Every <b>farm</b>, marked with its owner’s name and acreage. Find your family’s name on the land in 1860, then look for the same name in the deed books.</li>
    </ul>
    <p class="note">Source: <i>Map of the Counties of Cass, Van Buren and Berrien, Michigan</i> (Philadelphia: Geil, Harley &amp; Siverd, 1860). Library of Congress, Geography and Map Division, g4113c.la000324. Public domain. Shown through the Library’s own image service.</p>
    <script src="/vendor/openseadragon-4.1.1.min.js?v=1"></script>
    <script>
    (function(){{ var stat=document.getElementById('mstat');
      if (!window.OpenSeadragon){{ stat.textContent='The map viewer could not load. Try refreshing the page.'; return; }}
      var v=OpenSeadragon({{ id:'osd', tileSources:'{IIIF}/info.json', showNavigationControl:false, showNavigator:true, navigatorPosition:'BOTTOM_RIGHT',
        maxZoomPixelRatio:2.2, visibilityRatio:0.6, gestureSettingsMouse:{{clickToZoom:false, dblClickToZoom:true}}, crossOriginPolicy:'Anonymous', animationTime:0.9 }});
      v.addHandler('open', function(){{ stat.textContent='18,612 × 20,096 pixels, from the Library of Congress.'; }});
      v.addHandler('open-failed', function(){{ stat.textContent='The Library of Congress image service did not answer. Please try again in a minute.'; }});
      document.getElementById('mzin').onclick=function(){{ v.viewport.zoomBy(1.6); }};
      document.getElementById('mzout').onclick=function(){{ v.viewport.zoomBy(1/1.6); }};
      document.getElementById('mhome').onclick=function(){{ v.viewport.goHome(); }};
      document.getElementById('mfull').onclick=function(){{ v.setFullScreen(!v.isFullPage()); }};
    }})();
    </script>
'''
page('map/index.html','The map room · 1860 wall map · Project Scroll','Walk over every inch of the 1860 wall map of Cass, Van Buren and Berrien counties, Michigan, from the Library of Congress.',body, og='https://projectscroll.com/og/map.jpg')
print('map built')
