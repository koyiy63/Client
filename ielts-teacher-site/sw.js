const CACHE = 'ielts-teacher-v1';
const ASSETS = [
  '/ielts-teacher-site/',
  '/ielts-teacher-site/index.html',
  '/ielts-teacher-site/guide.html',
  '/ielts-teacher-site/tips.html',
  '/ielts-teacher-site/resources.html',
  '/ielts-teacher-site/contact.html',
  '/ielts-teacher-site/assets/styles.css',
  '/ielts-teacher-site/assets/script.js'
];
self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))));
});
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (url.origin === location.origin) {
    e.respondWith(
      caches.match(e.request).then((res) => res || fetch(e.request).then((resp) => {
        const copy = resp.clone();
        caches.open(CACHE).then((c) => c.put(e.request, copy));
        return resp;
      }).catch(() => caches.match('/ielts-teacher-site/index.html')))
    );
  }
});