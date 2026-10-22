/* Project Scroll offline support.
   Pages: network first, so visitors always get the newest version when online; the saved copy is used only offline.
   Files with a version tag (?v=) and pictures: saved copy first, since their names change whenever they change. */
const CACHE = 'ps-07e9e490';
const CORE = ['/', '/notes/', '/notes/one-letter-two-certificates/', '/404.html', '/map/', '/map/cassopolis/', '/map/cassopolis/today.json?v=1', '/map/niles/', '/map/niles/today.json?v=1', '/map/dowagiac/', '/map/dowagiac/today.json?v=1', '/map/paw-paw/', '/map/paw-paw/today.json?v=1', '/map/south-bend/', '/map/south-bend/today.json?v=1', '/map/goshen/', '/map/goshen/today.json?v=1', '/map/elkhart/', '/map/elkhart/today.json?v=1', '/map/then-and-now/', '/names/', '/almanac/', '/almanac.json', '/sources/', '/junior/', '/guide/gravestones/', '/postcards/', '/roads-and-rails/','/lost-towns/','/newspaper/','/museums/','/walk/','/walk/dowagiac/','/people/','/food/','/seasons/','/passport/','/visit/','/postcards/','/img/cass1860.webp','/museums/base.json?v=1','/vendor/leaflet-1.9.4/leaflet.js?v=1','/vendor/leaflet-1.9.4/leaflet.css?v=1','/map/3d/cassopolis/','/map/3d/valley/','/soldiers/', '/classrooms/', '/families/', '/legends/', '/records/', '/glossary/', '/about/', '/privacy/', '/badges/', '/guide/death-certificate/', '/toolkit/', '/toolkit/toolkit.js?v=3', '/guide/old-handwriting/', '/notes/book/', '/search.json', '/site.min.css?v=07e9e490', '/site.min.js?v=07e9e490',
  '/img/heron-dawn.webp', '/img/doctors-window.jpg', '/img/two-certificates.jpg', '/favicon.svg', '/icons/icon-192.png?v=2',
  '/fonts/libre-caslon-display-latin-400-normal.woff2', '/fonts/libre-caslon-text-latin-400-normal.woff2',
  '/fonts/libre-caslon-text-latin-400-italic.woff2', '/fonts/libre-caslon-text-latin-700-normal.woff2'];
const save = (req, res) => (res && res.ok) ? caches.open(CACHE).then(c => c.put(req, res)) : Promise.resolve();
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => Promise.allSettled(CORE.map(u => c.add(new Request(u, {cache: 'reload'}))))).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(Promise.all([caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE && k !== 'ps-files' && k !== 'ps-plans').map(k => caches.delete(k)))), self.registration.navigationPreload ? self.registration.navigationPreload.enable().catch(() => {}) : Promise.resolve()]).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const req = e.request; const url = new URL(req.url);
  /* the old town plans laid over today's streets come from the libraries' image services; once seen, keep them, so a town can be walked without signal */
  if (req.method === 'GET' && /^(tile\.loc\.gov|cdm17272\.contentdm\.oclc\.org)$/.test(url.hostname) && /\/(1790|1890|2400),\/0\/default\.jpg$/.test(url.pathname)) {
    e.respondWith(caches.open('ps-plans').then(c => c.match(req).then(hit => hit || fetch(req).then(res => {
      /* a readable answer is kept only if it is good; a library that does not allow reading gives an opaque one, kept as it is. Thirty plans at most. */
      if (res.ok || res.type === 'opaque') e.waitUntil(c.put(req, res.clone()).then(() => c.keys()).then(k => k.length > 30 ? c.delete(k[0]) : null));
      return res; }))));
    return;
  }
  if (req.method !== 'GET' || url.origin !== location.origin) return;
  const isPage = req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html');
  /* a page is saved under its address alone, so links carrying tracking tags (fbclid and the like) share one copy */
  const pageKey = new Request(url.origin + url.pathname);
  if (isPage) {
    e.respondWith((e.preloadResponse ? e.preloadResponse.then(r => r || fetch(req)) : fetch(req)).then(res => { if (!res.redirected) e.waitUntil(save(pageKey, res.clone())); return res; })
      .catch(() => caches.match(pageKey).then(r => r || caches.match('/404.html')).then(r => r || caches.match('/'))));
    return;
  }
  /* a page that asks for a fresh copy, or the case list, goes to the network first */
  if (req.cache === 'no-store' || url.pathname === '/cases.json') { e.respondWith(fetch(req).then(res => { if (url.pathname === '/cases.json') e.waitUntil(save(req, res.clone())); return res; }).catch(() => caches.match(req, {ignoreSearch: true}))); return; }
  /* the search index: the saved copy at once, refreshed in the background, so search works offline */
  if (url.pathname.endsWith('.json')) {
    e.respondWith(caches.match(req, {ignoreSearch: true}).then(hit => {
      const net = fetch(req).then(res => { e.waitUntil(save(req, res.clone())); return res; });
      if (hit) { e.waitUntil(net.catch(() => {})); return hit; }
      return net;
    }));
    return;
  }
  /* case files saved for offline (PDFs, worksheets): the saved copy first, the network otherwise */
  if (/\.pdf$/.test(url.pathname)) { e.respondWith(caches.match(req).then(hit => { const net = fetch(req).then(res => { if (res.ok && hit) e.waitUntil(caches.open('ps-files').then(c => c.put(req, res.clone()))); return res; }); if (hit) { e.waitUntil(net.catch(() => {})); return hit; } return net; })); return; }
  /* share cards are redrawn under the same names, so they are never served from the cache first */
  if (/^\/(og\/|og-dark\.|cases\/\d+\/card\.)/.test(url.pathname)) return;
  /* files with a version tag never change under their name: the saved copy first */
  if (url.search.includes('v=') || /\.woff2$/.test(url.pathname)) {
    e.respondWith(caches.match(req).then(r => r || fetch(req).then(res => { e.waitUntil(save(req, res.clone())); return res; })));
    return;
  }
  /* pictures: the saved copy at once, and a fresh one fetched behind it, so a replaced picture shows on the next visit */
  if (/\.(png|jpg|jpeg|webp|avif|svg|gif)$/.test(url.pathname)) {
    e.respondWith(caches.match(req).then(hit => {
      const net = fetch(req).then(res => { e.waitUntil(save(req, res.clone())); return res; });
      if (hit) { e.waitUntil(net.catch(() => {})); return hit; }
      return net;
    }));
  }
});
