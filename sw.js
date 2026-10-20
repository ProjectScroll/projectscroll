/* Project Scroll offline support.
   Pages: network first, so visitors always get the newest version when online; the saved copy is used only offline.
   Files with a version tag (?v=) and pictures: saved copy first, since their names change whenever they change. */
const CACHE = 'ps-7070a944';
const CORE = ['/', '/notes/', '/notes/one-letter-two-certificates/', '/404.html', '/map/', '/map/cassopolis/', '/map/niles/', '/map/dowagiac/', '/map/paw-paw/', '/families/', '/legends/', '/records/', '/glossary/', '/about/', '/privacy/', '/badges/', '/guide/death-certificate/', '/toolkit/', '/toolkit/toolkit.js?v=3', '/guide/old-handwriting/', '/notes/book/', '/search.json', '/site.min.css?v=7070a944', '/site.min.js?v=7070a944',
  '/img/heron-dawn.webp', '/img/doctors-window.jpg', '/img/two-certificates.jpg', '/favicon.svg', '/icons/icon-192.png',
  '/fonts/libre-caslon-display-latin-400-normal.woff2', '/fonts/libre-caslon-text-latin-400-normal.woff2',
  '/fonts/libre-caslon-text-latin-400-italic.woff2', '/fonts/libre-caslon-text-latin-700-normal.woff2'];
const save = (req, res) => (res && res.ok) ? caches.open(CACHE).then(c => c.put(req, res)) : Promise.resolve();
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => Promise.allSettled(CORE.map(u => c.add(new Request(u, {cache: 'reload'}))))).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(Promise.all([caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE && k !== 'ps-files').map(k => caches.delete(k)))), self.registration.navigationPreload ? self.registration.navigationPreload.enable().catch(() => {}) : Promise.resolve()]).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const req = e.request; const url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin) return;
  const isPage = req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html');
  if (isPage) {
    e.respondWith((e.preloadResponse ? e.preloadResponse.then(r => r || fetch(req)) : fetch(req)).then(res => { e.waitUntil(save(req, res.clone())); return res; })
      .catch(() => caches.match(req).then(r => r || caches.match('/404.html')).then(r => r || caches.match('/'))));
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
  if (/\.pdf$/.test(url.pathname)) { e.respondWith(caches.match(req).then(r => r || fetch(req))); return; }
  /* share cards are redrawn under the same names, so they are never served from the cache first */
  if (/^\/(og\/|og-dark\.|cases\/\d+\/card\.)/.test(url.pathname)) return;
  if (url.search.includes('v=') || /\.(png|jpg|webp|svg|woff2)$/.test(url.pathname)) {
    e.respondWith(caches.match(req).then(r => r || fetch(req).then(res => { e.waitUntil(save(req, res.clone())); return res; })));
  }
});
