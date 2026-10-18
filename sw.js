/* Project Scroll offline support.
   Pages: network first, so visitors always get the newest version when online; the saved copy is used only offline.
   Files with a version tag (?v=) and pictures: saved copy first, since their names change whenever they change. */
const CACHE = 'ps-v28';
const CORE = ['/', '/notes/', '/notes/one-letter-two-certificates/', '/404.html', '/map/', '/map/cassopolis/', '/families/', '/legends/', '/guide/death-certificate/', '/toolkit/', '/toolkit/toolkit.js?v=1', '/guide/old-handwriting/', '/notes/book/', '/search.json', '/site.css?v=28', '/site.js?v=28',
  '/img/heron-dawn.webp', '/img/doctors-window.jpg', '/img/two-certificates.jpg', '/favicon.svg', '/icons/icon-192.png',
  '/fonts/libre-caslon-display-latin-400-normal.woff2', '/fonts/libre-caslon-text-latin-400-normal.woff2',
  '/fonts/libre-caslon-text-latin-400-italic.woff2', '/fonts/libre-caslon-text-latin-700-normal.woff2'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const req = e.request; const url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin) return;
  const isPage = req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html');
  if (isPage) {
    e.respondWith(fetch(req).then(res => { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return res; })
      .catch(() => caches.match(req).then(r => r || caches.match('/'))));
    return;
  }
  if (url.search.includes('v=') || /\.(png|jpg|webp|svg|woff2)$/.test(url.pathname)) {
    e.respondWith(caches.match(req).then(r => r || fetch(req).then(res => { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return res; })));
  }
});
