// Service Worker per PWA - Assistente Intelligente
const CACHE_NAME = 'agenda-ai-v1.3.0';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/js/app.js',
  'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js'
];

// Installazione Service Worker
self.addEventListener('install', event => {
  console.log('📦 Service Worker: Installazione...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('✅ Cache aperta');
        return cache.addAll(urlsToCache);
      })
      .catch(err => console.log('⚠️ Errore cache:', err))
  );
});

// Attivazione Service Worker
self.addEventListener('activate', event => {
  console.log('✅ Service Worker: Attivato');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('🗑️ Rimuovo cache vecchia:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Intercetta richieste
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - restituisci la risposta dalla cache
        if (response) {
          return response;
        }
        
        // Altrimenti fetch dalla rete
        return fetch(event.request).then(response => {
          // Non cachare richieste non-GET o non-OK
          if (!response || response.status !== 200 || response.type === 'error') {
            return response;
          }
          
          // Clona la risposta
          const responseToCache = response.clone();
          
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
          
          return response;
        });
      })
      .catch(() => {
        // Fallback offline
        return new Response('Offline - Riconnetti per aggiornare', {
          status: 503,
          statusText: 'Service Unavailable'
        });
      })
  );
});

// Notifiche Push (per future implementazioni)
self.addEventListener('push', event => {
  const data = event.data ? event.data.json() : {};
  const title = data.title || '🔔 Promemoria';
  const options = {
    body: data.body || 'Hai un nuovo aggiornamento',
    icon: '/static/icon-192.png',
    badge: '/static/badge-72.png',
    vibrate: [200, 100, 200],
    data: data.url || '/'
  };
  
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Click su notifica
self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil(
    clients.openWindow(event.notification.data)
  );
});

