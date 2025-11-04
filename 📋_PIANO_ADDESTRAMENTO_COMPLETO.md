# 🎯 PIANO COMPLETO: ADDESTRAMENTO & IMPLEMENTAZIONE APP

**Data creazione:** 5 Novembre 2025  
**Obiettivo:** Portare l'app da MVP (95%) a prodotto maturo (100%)  
**Durata stimata:** 30-45 giorni  
**Focus:** NLP Training + Feature Implementation + UX Polish

---

## 📊 STATO ATTUALE (POST-TEST)

### ✅ FUNZIONANTE (95%)
- Chat AI con NLP base
- Gestione impegni/spese/obiettivi
- Calendario interattivo
- Previsioni AI
- 9 lingue supportate
- Mobile UX (appena deployed)
- Community sharing
- Export (PDF, iCal, CSV, JSON)
- Fingerprinting auth

### ⚠️ DA MIGLIORARE (5%)
- NLP: Riconoscimento formati non standard
- Real-time updates (budget sidebar)
- Grafici Analytics (placeholder)
- Test coverage < 50%
- Performance (cache non ottimale)
- Smart Links (DuckDuckGo implementato, YouTube/Amazon no)

---

## 🎓 FASE 1: ADDESTRAMENTO NLP (Priorità ALTA)

### **Obiettivo:** Portare riconoscimento da 75% a 95%+

### 1.1 Raccolta Dati Training (5 giorni)
```
TASK:
✓ Creare dataset di 1000+ frasi reali
✓ Categorizzare per tipo (obiettivo, impegno, spesa, diario)
✓ Annotare varianti linguistiche

TOOL:
- Script Python per generazione automatica varianti
- Crowdsourcing da utenti beta (se disponibili)
- Data augmentation (sinonimi, riformulazioni)

OUTPUT:
📁 data/nlp_training/
  ├── obiettivi_1000.json
  ├── impegni_1000.json
  ├── spese_1000.json
  └── diario_1000.json
```

**Esempi di varianti da addestrare:**
```python
# Impegni - Varianti temporali
"Giovedì riunione team ore 10"  # ❌ Ora fallisce
"Riunione team giovedì alle 10" # ✅ Alternativa
"10am giovedì meeting team"      # ❌ Da addestrare
"Giovedì 10:00 riunione"         # ❌ Da addestrare

# Spese - Formati multipli
"35 euro cena"        # ✅ Funziona
"Cena 35€"            # ❌ Da testare
"Ho speso 35 a cena"  # ❌ Da addestrare
"35,00 per cena"      # ❌ Da addestrare
```

### 1.2 Training del Modello (7 giorni)
```python
# File: app/core/nlp_trainer.py

import spacy
from spacy.training import Example
import random

class NLPTrainer:
    def __init__(self):
        self.nlp = spacy.blank("it")
        self.ner = self.nlp.add_pipe("ner")
        
    def train(self, training_data, iterations=30):
        """
        Training data format:
        [
            ("Giovedì riunione team ore 10", {
                "entities": [
                    (0, 8, "GIORNO"),
                    (9, 17, "EVENTO"),
                    (23, 30, "ORA")
                ]
            })
        ]
        """
        optimizer = self.nlp.create_optimizer()
        
        for i in range(iterations):
            random.shuffle(training_data)
            losses = {}
            
            for text, annotations in training_data:
                doc = self.nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                self.nlp.update([example], sgd=optimizer, losses=losses)
            
            print(f"Iteration {i+1}, Losses: {losses}")
        
        # Salva modello
        self.nlp.to_disk("models/nlp_italian_v2")
        
    def evaluate(self, test_data):
        """Valuta accuratezza su test set"""
        correct = 0
        total = len(test_data)
        
        for text, expected_type in test_data:
            doc = self.nlp(text)
            predicted = self.classify(doc)
            if predicted == expected_type:
                correct += 1
        
        accuracy = (correct / total) * 100
        print(f"Accuracy: {accuracy:.2f}%")
        return accuracy
```

**Metriche Target:**
- Accuratezza obiettivi: 90%+ → **95%+**
- Accuratezza impegni: 85%+ → **95%+**
- Accuratezza spese: 95%+ → **98%+**
- Accuratezza diario: 80%+ → **90%+**

### 1.3 Integrazione & Testing (3 giorni)
```bash
# Test A/B tra vecchio e nuovo modello
python scripts/nlp_ab_test.py --old models/nlp_italian_v1 --new models/nlp_italian_v2

# Deploy graduale (canary)
# 10% utenti → nuovo modello
# 90% utenti → vecchio modello
# Monitoraggio errori per 48h
```

---

## 🚀 FASE 2: IMPLEMENTAZIONE SMART LINKS (Priorità ALTA)

### **Obiettivo:** Completare YouTube & Amazon integration

### 2.1 YouTube Search (3 giorni)
```python
# File: app/integrations/youtube_search.py

from googleapiclient.discovery import build
from app import cache
import os

class YouTubeSearchService:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        
    @cache.cached(timeout=86400, key_prefix='yt_search')  # 24h cache
    def search(self, query, max_results=5):
        """
        Cerca video su YouTube
        
        Returns:
        [
            {
                'title': 'Come programmare in Python',
                'url': 'https://youtube.com/watch?v=...',
                'channel': 'Programmatore Italiano',
                'thumbnail': 'https://...',
                'duration': '15:30',
                'views': '125K'
            }
        ]
        """
        try:
            request = self.youtube.search().list(
                q=query,
                part='snippet',
                type='video',
                maxResults=max_results,
                regionCode='IT',
                relevanceLanguage='it'
            )
            response = request.execute()
            
            results = []
            for item in response['items']:
                video_id = item['id']['videoId']
                snippet = item['snippet']
                
                # Get video details (duration, views)
                video_request = self.youtube.videos().list(
                    part='contentDetails,statistics',
                    id=video_id
                )
                video_response = video_request.execute()
                video_data = video_response['items'][0]
                
                results.append({
                    'title': snippet['title'],
                    'url': f'https://youtube.com/watch?v={video_id}',
                    'channel': snippet['channelTitle'],
                    'thumbnail': snippet['thumbnails']['medium']['url'],
                    'duration': self._parse_duration(
                        video_data['contentDetails']['duration']
                    ),
                    'views': self._format_views(
                        video_data['statistics']['viewCount']
                    ),
                    'published': snippet['publishedAt']
                })
            
            return results
            
        except Exception as e:
            print(f"YouTube API Error: {e}")
            return []
    
    def _parse_duration(self, iso_duration):
        """Converte PT15M30S → 15:30"""
        import re
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_duration)
        h, m, s = match.groups()
        h = int(h) if h else 0
        m = int(m) if m else 0
        s = int(s) if s else 0
        
        if h > 0:
            return f"{h}:{m:02d}:{s:02d}"
        else:
            return f"{m}:{s:02d}"
    
    def _format_views(self, views):
        """Formatta 125000 → 125K"""
        views = int(views)
        if views >= 1_000_000:
            return f"{views/1_000_000:.1f}M"
        elif views >= 1_000:
            return f"{views/1_000:.0f}K"
        else:
            return str(views)
```

**Frontend Integration:**
```javascript
// In templates/index.html - aggiungiMessaggioSmartLinks()

if (data.youtube_results) {
    html += `
    <div class="smart-links-section">
        <div class="smart-links-header">
            📺 <strong>Video YouTube</strong>
        </div>
        <div class="youtube-results">
            ${data.youtube_results.map((video, i) => `
                <div class="youtube-card">
                    <div class="youtube-thumbnail">
                        <img src="${video.thumbnail}" alt="${video.title}">
                        <span class="duration">${video.duration}</span>
                    </div>
                    <div class="youtube-info">
                        <a href="${video.url}" target="_blank" class="video-title">
                            ${video.title}
                        </a>
                        <div class="video-meta">
                            ${video.channel} • ${video.views} views
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    </div>
    `;
}
```

### 2.2 Amazon Search (4 giorni)
```python
# File: app/integrations/amazon_search.py

import requests
from bs4 import BeautifulSoup
from app import cache

class AmazonSearchService:
    """
    NOTA: Amazon non ha API pubblica gratuita.
    Usiamo web scraping (attenzione a robots.txt) 
    O Alternative: Amazon Product Advertising API (richiede account affiliato)
    """
    
    def __init__(self):
        self.base_url = "https://www.amazon.it"
        self.affiliate_tag = os.getenv('AMAZON_AFFILIATE_TAG', '')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AgendaBot/1.0)',
            'Accept-Language': 'it-IT,it;q=0.9'
        }
    
    @cache.cached(timeout=43200, key_prefix='amz_search')  # 12h cache
    def search(self, query, max_results=5):
        """
        Cerca prodotti su Amazon
        
        ALTERNATIVE (se scraping blocca):
        1. Amazon Product Advertising API
        2. RapidAPI Amazon scraper
        3. ScraperAPI proxy
        """
        try:
            url = f"{self.base_url}/s?k={query.replace(' ', '+')}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 503:
                # Amazon ha bloccato lo scraping
                return self._fallback_search(query)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []
            
            for item in soup.select('.s-result-item')[:max_results]:
                try:
                    title_elem = item.select_one('h2 a span')
                    price_elem = item.select_one('.a-price-whole')
                    rating_elem = item.select_one('.a-icon-star-small')
                    image_elem = item.select_one('.s-image')
                    asin = item.get('data-asin')
                    
                    if not all([title_elem, asin]):
                        continue
                    
                    product_url = f"{self.base_url}/dp/{asin}"
                    if self.affiliate_tag:
                        product_url += f"?tag={self.affiliate_tag}"
                    
                    products.append({
                        'title': title_elem.text.strip(),
                        'price': price_elem.text.strip() if price_elem else 'N/A',
                        'rating': rating_elem.text.split()[0] if rating_elem else None,
                        'url': product_url,
                        'image': image_elem.get('src') if image_elem else None,
                        'asin': asin
                    })
                    
                except Exception as e:
                    continue
            
            return products
            
        except Exception as e:
            print(f"Amazon Search Error: {e}")
            return self._fallback_search(query)
    
    def _fallback_search(self, query):
        """Fallback se scraping fallisce - usa Google Shopping"""
        # Implementa ricerca alternativa via Google Shopping API
        # O reindirizza a pagina ricerca Amazon
        return [{
            'title': f'Cerca "{query}" su Amazon',
            'price': 'Clicca per vedere',
            'url': f'{self.base_url}/s?k={query.replace(" ", "+")}',
            'image': '/static/images/amazon_placeholder.png',
            'fallback': True
        }]
```

### 2.3 Smart Links Manager Update (2 giorni)
```python
# File: app/core/smart_links.py - UPDATE

class SmartLinksManager:
    def __init__(self):
        self.web_search = WebSearchService()
        self.youtube_search = YouTubeSearchService()
        self.amazon_search = AmazonSearchService()
    
    def process_message(self, user_input: str) -> dict:
        """Rileva intent e chiama servizio appropriato"""
        
        # Pattern matching migliorato
        patterns = {
            'youtube': [
                r'(?:video|tutorial|guarda|vedere)\s+(.+)',
                r'(?:come|imparare)\s+(?:a\s+)?(.+)',
                r'youtube\s+(.+)'
            ],
            'amazon': [
                r'(?:compra|acquista|cerca prodotto)\s+(.+)',
                r'(?:quanto costa|prezzo)\s+(.+)',
                r'amazon\s+(.+)'
            ],
            'web': [
                r'(?:cerca|ricerca|informazioni su)\s+(.+)',
                r'(?:cos[\'']è|cosa è|che cos[\'']è)\s+(.+)',
                r'web\s+(.+)'
            ]
        }
        
        for intent, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, user_input.lower())
                if match:
                    query = match.group(1)
                    return self._execute_search(intent, query, user_input)
        
        return {'has_smart_links': False}
    
    def _execute_search(self, intent, query, original_input):
        """Esegue ricerca e formatta risultati"""
        results = {
            'has_smart_links': True,
            'intent': intent,
            'query': query,
            'original_input': original_input
        }
        
        if intent == 'youtube':
            results['youtube_results'] = self.youtube_search.search(query)
        elif intent == 'amazon':
            results['amazon_results'] = self.amazon_search.search(query)
        elif intent == 'web':
            results['web_results'] = self.web_search.search(query)
        
        return results
```

---

## 📊 FASE 3: ANALYTICS & GRAFICI (Priorità MEDIA)

### **Obiettivo:** Trasformare placeholder in grafici reali

### 3.1 Backend Analytics (3 giorni)
```python
# File: app/routes/analytics.py

@bp.route('/api/analytics/spese-categoria', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)  # 1h cache
def get_spese_per_categoria():
    """
    Ritorna spese aggregate per categoria
    
    Returns:
    {
        "labels": ["Cibo", "Trasporti", "Svago", "Altro"],
        "data": [120, 45, 30, 25],
        "total": 220
    }
    """
    periodo = request.args.get('periodo', 'mese')  # mese, settimana, anno
    user_ip = get_user_ip()
    
    # Query spese per periodo
    if periodo == 'mese':
        start_date = datetime.now().replace(day=1)
    elif periodo == 'settimana':
        start_date = datetime.now() - timedelta(days=7)
    else:  # anno
        start_date = datetime.now().replace(month=1, day=1)
    
    spese = Spesa.query.filter(
        Spesa.ip_hash == hashlib.sha256(user_ip.encode()).hexdigest(),
        Spesa.data >= start_date
    ).all()
    
    # Aggrega per categoria
    categoria_totals = {}
    for spesa in spese:
        cat = spesa.categoria or 'altro'
        categoria_totals[cat] = categoria_totals.get(cat, 0) + spesa.importo
    
    # Ordina per importo
    sorted_cats = sorted(
        categoria_totals.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return jsonify({
        'labels': [cat.title() for cat, _ in sorted_cats],
        'data': [total for _, total in sorted_cats],
        'total': sum(categoria_totals.values()),
        'periodo': periodo
    })


@bp.route('/api/analytics/tempo-obiettivi', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)
def get_tempo_per_obiettivo():
    """
    Ritorna tempo dedicato ad ogni obiettivo
    
    Returns:
    {
        "labels": ["Python", "Javascript", "Inglese"],
        "data": [15.5, 10.0, 5.0],
        "total_hours": 30.5
    }
    """
    user_ip = get_user_ip()
    periodo_giorni = int(request.args.get('giorni', 30))
    
    obiettivi = Obiettivo.query.filter_by(
        ip_hash=hashlib.sha256(user_ip.encode()).hexdigest()
    ).all()
    
    # Calcola ore completate per ogni obiettivo
    obiettivo_hours = []
    for obj in obiettivi:
        ore_completate = obj.ore_completate or 0
        if ore_completate > 0:
            obiettivo_hours.append({
                'nome': obj.nome,
                'ore': ore_completate
            })
    
    # Ordina per ore
    obiettivo_hours.sort(key=lambda x: x['ore'], reverse=True)
    
    return jsonify({
        'labels': [o['nome'] for o in obiettivo_hours],
        'data': [o['ore'] for o in obiettivo_hours],
        'total_hours': sum(o['ore'] for o in obiettivo_hours)
    })


@bp.route('/api/analytics/trend-spese', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)
def get_trend_spese():
    """
    Ritorna trend spese ultimi N giorni
    
    Returns:
    {
        "labels": ["1 Nov", "2 Nov", "3 Nov", ...],
        "data": [45, 30, 120, ...],
        "average": 65
    }
    """
    user_ip = get_user_ip()
    giorni = int(request.args.get('giorni', 30))
    
    start_date = datetime.now() - timedelta(days=giorni)
    
    spese = Spesa.query.filter(
        Spesa.ip_hash == hashlib.sha256(user_ip.encode()).hexdigest(),
        Spesa.data >= start_date
    ).order_by(Spesa.data).all()
    
    # Aggrega per giorno
    daily_totals = {}
    for spesa in spese:
        day_key = spesa.data.strftime('%d %b')
        daily_totals[day_key] = daily_totals.get(day_key, 0) + spesa.importo
    
    # Riempi giorni mancanti con 0
    current = start_date
    labels = []
    data = []
    while current <= datetime.now():
        day_key = current.strftime('%d %b')
        labels.append(day_key)
        data.append(daily_totals.get(day_key, 0))
        current += timedelta(days=1)
    
    average = sum(data) / len(data) if data else 0
    
    return jsonify({
        'labels': labels,
        'data': data,
        'average': round(average, 2)
    })
```

### 3.2 Frontend Chart.js (2 giorni)
```javascript
// In templates/index.html - updateAnalytics()

async function updateAnalytics() {
    try {
        // 1. Spese per Categoria
        const speseRes = await fetch('/api/analytics/spese-categoria?periodo=mese');
        const speseData = await speseRes.json();
        
        const speseCategoriaChart = new Chart(
            document.getElementById('speseCategoriaChart'),
            {
                type: 'doughnut',
                data: {
                    labels: speseData.labels,
                    datasets: [{
                        data: speseData.data,
                        backgroundColor: [
                            '#3b82f6', '#10b981', '#f59e0b', 
                            '#ef4444', '#8b5cf6', '#ec4899'
                        ],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: '#cbd5e1' }
                        },
                        tooltip: {
                            callbacks: {
                                label: (context) => {
                                    const value = context.parsed;
                                    const total = speseData.total;
                                    const percent = ((value/total)*100).toFixed(1);
                                    return `€${value} (${percent}%)`;
                                }
                            }
                        }
                    }
                }
            }
        );
        
        // 2. Tempo per Obiettivo
        const tempoRes = await fetch('/api/analytics/tempo-obiettivi');
        const tempoData = await tempoRes.json();
        
        const tempoObiettiviChart = new Chart(
            document.getElementById('tempoObiettiviChart'),
            {
                type: 'bar',
                data: {
                    labels: tempoData.labels,
                    datasets: [{
                        label: 'Ore',
                        data: tempoData.data,
                        backgroundColor: '#3b82f6',
                        borderColor: '#60a5fa',
                        borderWidth: 2,
                        borderRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { color: '#94a3b8' },
                            grid: { color: 'rgba(148, 163, 184, 0.1)' }
                        },
                        x: {
                            ticks: { color: '#94a3b8' },
                            grid: { display: false }
                        }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            }
        );
        
        // 3. Trend Spese
        const trendRes = await fetch('/api/analytics/trend-spese?giorni=30');
        const trendData = await trendRes.json();
        
        const trendSpeseChart = new Chart(
            document.getElementById('trendSpeseChart'),
            {
                type: 'line',
                data: {
                    labels: trendData.labels,
                    datasets: [{
                        label: 'Spese Giornaliere',
                        data: trendData.data,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointRadius: 4,
                        pointBackgroundColor: '#3b82f6',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { 
                                color: '#94a3b8',
                                callback: (value) => `€${value}`
                            },
                            grid: { color: 'rgba(148, 163, 184, 0.1)' }
                        },
                        x: {
                            ticks: { 
                                color: '#94a3b8',
                                maxRotation: 45,
                                minRotation: 45
                            },
                            grid: { display: false }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: (context) => `€${context.parsed.y.toFixed(2)}`
                            }
                        }
                    }
                }
            }
        );
        
        console.log('✅ Analytics charts loaded');
        
    } catch (error) {
        console.error('❌ Analytics error:', error);
    }
}
```

---

## 🧪 FASE 4: TEST COVERAGE (Priorità ALTA)

### **Obiettivo:** Portare coverage da 40% a 80%+

### 4.1 Unit Tests Expansion (5 giorni)
```python
# File: tests/test_nlp_advanced.py

import pytest
from app.core.input_manager import InputManager

class TestNLPAdvanced:
    """Test avanzati per NLP con varianti multiple"""
    
    @pytest.fixture
    def manager(self):
        return InputManager()
    
    # ========================================
    # IMPEGNI - 50 varianti
    # ========================================
    
    @pytest.mark.parametrize("input_text,expected", [
        ("Giovedì riunione team ore 10", "impegno"),
        ("Riunione team giovedì alle 10", "impegno"),
        ("10am giovedì meeting team", "impegno"),
        ("Giovedì 10:00 riunione", "impegno"),
        ("Meeting domani mattina", "impegno"),
        ("Domani dottore ore 15", "impegno"),
        ("15:30 appuntamento dentista", "impegno"),
        ("Pranzo con Marco lunedì", "impegno"),
        ("Lunedì dalle 9 alle 17 lavoro", "impegno"),
        ("9-17 ufficio martedì", "impegno"),
        # ... altri 40 varianti
    ])
    def test_impegni_varianti(self, manager, input_text, expected):
        result = manager.analizza_input(input_text)
        assert result['tipo'] == expected, f"Failed for: {input_text}"
    
    # ========================================
    # SPESE - 50 varianti
    # ========================================
    
    @pytest.mark.parametrize("input_text,expected_importo,expected_cat", [
        ("35 euro cena", 35.0, "cibo"),
        ("Cena 35€", 35.0, "cibo"),
        ("Ho speso 35 a cena", 35.0, "cibo"),
        ("35,00 per cena", 35.0, "cibo"),
        ("Comprato libro 12.50", 12.5, "svago"),
        ("Benzina 60 euro", 60.0, "trasporti"),
        ("60€ di benzina", 60.0, "trasporti"),
        ("Pagato affitto 800", 800.0, "casa"),
        ("Spesa supermercato 45", 45.0, "cibo"),
        ("Cinema 12 euro", 12.0, "svago"),
        # ... altri 40 varianti
    ])
    def test_spese_varianti(self, manager, input_text, expected_importo, expected_cat):
        result = manager.analizza_input(input_text)
        assert result['tipo'] == 'spesa'
        assert abs(result['importo'] - expected_importo) < 0.01
        assert result['categoria'] == expected_cat
    
    # ========================================
    # OBIETTIVI - 30 varianti
    # ========================================
    
    @pytest.mark.parametrize("input_text", [
        "Voglio studiare Python 3 ore a settimana",
        "Studio Python 3h/settimana",
        "Obiettivo: imparare Python (3 ore settimanali)",
        "Dedico 3 ore a Python ogni settimana",
        "Python 3 ore settimanali come obiettivo",
        # ... altri 25 varianti
    ])
    def test_obiettivi_varianti(self, manager, input_text):
        result = manager.analizza_input(input_text)
        assert result['tipo'] == 'obiettivo'
        assert 'python' in result['nome'].lower()
        assert result['ore_settimanali'] == 3.0
    
    # ========================================
    # DIARIO - 20 varianti
    # ========================================
    
    @pytest.mark.parametrize("input_text", [
        "Oggi mi sento felice",
        "Giornata fantastica!",
        "Mi sento un po' giù",
        "Stanco ma soddisfatto",
        "Pensieri: bella giornata",
        # ... altri 15 varianti
    ])
    def test_diario_varianti(self, manager, input_text):
        result = manager.analizza_input(input_text)
        assert result['tipo'] == 'diario'
        assert result['testo'] == input_text
```

### 4.2 Integration Tests (3 giorni)
```python
# File: tests/test_integration.py

class TestIntegrationFlows:
    """Test end-to-end di flussi completi"""
    
    def test_full_user_journey(self, client, session):
        """
        Simula utente che:
        1. Crea obiettivo
        2. Aggiunge impegno
        3. Registra spesa
        4. Scrive diario
        5. Visualizza statistiche
        6. Esporta dati
        """
        
        # 1. Crea obiettivo
        res1 = client.post('/api/chat', json={
            'messaggio': 'Voglio studiare Python 3 ore a settimana'
        })
        assert res1.status_code == 200
        data1 = res1.get_json()
        assert 'obiettivo' in data1['tipo'].lower()
        
        # 2. Aggiunge impegno
        res2 = client.post('/api/chat', json={
            'messaggio': 'Domani riunione 10-12'
        })
        assert res2.status_code == 200
        data2 = res2.get_json()
        assert 'impegno' in data2['tipo'].lower()
        
        # 3. Registra spesa
        res3 = client.post('/api/chat', json={
            'messaggio': 'Speso 35 euro cena'
        })
        assert res3.status_code == 200
        data3 = res3.get_json()
        assert 'spesa' in data3['tipo'].lower()
        
        # 4. Verifica statistiche
        res4 = client.get('/api/statistiche')
        assert res4.status_code == 200
        stats = res4.get_json()
        assert stats['obiettivi_totali'] == 1
        assert stats['impegni_totali'] == 1
        assert stats['spese_totali'] > 0
        
        # 5. Export JSON
        res5 = client.get('/api/export?formato=json')
        assert res5.status_code == 200
        export_data = res5.get_json()
        assert len(export_data['obiettivi']) == 1
        assert len(export_data['impegni']) == 1
        
    def test_smart_links_flow(self, client):
        """Test Smart Links YouTube + Amazon + Web"""
        
        # YouTube
        res1 = client.post('/api/chat', json={
            'messaggio': 'video tutorial python'
        })
        data1 = res1.get_json()
        assert data1.get('smart_links') == True
        assert 'youtube_results' in data1
        
        # Amazon
        res2 = client.post('/api/chat', json={
            'messaggio': 'compra libro python'
        })
        data2 = res2.get_json()
        assert 'amazon_results' in data2
        
        # Web
        res3 = client.post('/api/chat', json={
            'messaggio': 'cerca guida python'
        })
        data3 = res3.get_json()
        assert 'web_results' in data3
```

---

## ⚡ FASE 5: PERFORMANCE & SCALING (Priorità MEDIA)

### 5.1 Database Optimization (3 giorni)
```python
# File: app/models/base.py - Aggiungi indici

class Spesa(db.Model):
    __tablename__ = 'spese'
    
    # ... campi esistenti ...
    
    # NUOVI INDICI per performance
    __table_args__ = (
        db.Index('idx_spesa_ip_data', 'ip_hash', 'data'),
        db.Index('idx_spesa_categoria', 'categoria'),
        db.Index('idx_spesa_importo', 'importo'),
    )

class Impegno(db.Model):
    __tablename__ = 'impegni'
    
    # ... campi esistenti ...
    
    __table_args__ = (
        db.Index('idx_impegno_ip_data', 'ip_hash', 'data_inizio'),
        db.Index('idx_impegno_data_range', 'data_inizio', 'data_fine'),
    )

class Obiettivo(db.Model):
    __tablename__ = 'obiettivi'
    
    # ... campi esistenti ...
    
    __table_args__ = (
        db.Index('idx_obiettivo_ip', 'ip_hash'),
        db.Index('idx_obiettivo_completato', 'completato'),
    )
```

**Migration per indici:**
```bash
# File: migrations/add_performance_indexes.py

from alembic import op

def upgrade():
    # Spese
    op.create_index('idx_spesa_ip_data', 'spese', ['ip_hash', 'data'])
    op.create_index('idx_spesa_categoria', 'spese', ['categoria'])
    op.create_index('idx_spesa_importo', 'spese', ['importo'])
    
    # Impegni
    op.create_index('idx_impegno_ip_data', 'impegni', ['ip_hash', 'data_inizio'])
    op.create_index('idx_impegno_data_range', 'impegni', ['data_inizio', 'data_fine'])
    
    # Obiettivi
    op.create_index('idx_obiettivo_ip', 'obiettivi', ['ip_hash'])
    op.create_index('idx_obiettivo_completato', 'obiettivi', ['completato'])

def downgrade():
    op.drop_index('idx_spesa_ip_data', 'spese')
    # ... altri drop ...
```

### 5.2 Query Optimization (2 giorni)
```python
# File: app/routes/api.py - Ottimizza query N+1

@bp.route('/api/statistiche', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def get_statistiche():
    user_ip = get_user_ip()
    ip_hash = hashlib.sha256(user_ip.encode()).hexdigest()
    
    # PRIMA (N+1 query):
    # obiettivi = Obiettivo.query.filter_by(ip_hash=ip_hash).all()
    # for obj in obiettivi:
    #     ore = obj.calcola_ore_completate()  # Query per ogni obiettivo!
    
    # DOPO (1 query con JOIN):
    from sqlalchemy import func
    
    obiettivi_stats = db.session.query(
        Obiettivo,
        func.coalesce(func.sum(Impegno.durata), 0).label('ore_totali')
    ).outerjoin(
        Impegno,
        db.and_(
            Impegno.obiettivo_id == Obiettivo.id,
            Impegno.completato == True
        )
    ).filter(
        Obiettivo.ip_hash == ip_hash
    ).group_by(Obiettivo.id).all()
    
    return jsonify({
        'obiettivi': [
            {
                'nome': obj.nome,
                'ore_completate': float(ore_totali),
                'progresso': (float(ore_totali) / obj.ore_settimanali * 100)
                             if obj.ore_settimanali > 0 else 0
            }
            for obj, ore_totali in obiettivi_stats
        ]
    })
```

### 5.3 Redis Caching Expansion (2 giorni)
```python
# File: app/core/cache_config.py

from flask_caching import Cache

cache = Cache()

# Configurazione stratificata
CACHE_CONFIG = {
    # Layer 1: Response cache (veloce, volatile)
    'CACHE_TYPE': 'redis' if os.getenv('REDIS_URL') else 'simple',
    'CACHE_REDIS_URL': os.getenv('REDIS_URL'),
    'CACHE_DEFAULT_TIMEOUT': 300,  # 5 min default
    
    # Layer 2: Query cache (medio, persistente)
    'CACHE_KEY_PREFIX': 'agenda_',
    'CACHE_QUERY_TIMEOUT': 3600,  # 1h per query
    
    # Layer 3: Static data cache (lungo, raramente cambia)
    'CACHE_STATIC_TIMEOUT': 86400,  # 24h per dati statici
}

def init_cache(app):
    cache.init_app(app, config=CACHE_CONFIG)
    
    # Pre-warm cache con dati comuni
    with app.app_context():
        cache.set('app_version', '2.0.0', timeout=0)  # Never expire
        cache.set('supported_languages', [
            'it', 'en', 'es', 'zh', 'ru', 'hi', 'ar'
        ], timeout=0)


# Decorator personalizzati
def cache_user_data(timeout=300):
    """Cache per-user con IP hash come key"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_ip = get_user_ip()
            cache_key = f"user_{hashlib.sha256(user_ip.encode()).hexdigest()}_{f.__name__}"
            
            # Check cache
            cached = cache.get(cache_key)
            if cached is not None:
                return cached
            
            # Execute function
            result = f(*args, **kwargs)
            
            # Save to cache
            cache.set(cache_key, result, timeout=timeout)
            return result
        
        return decorated_function
    return decorator
```

---

## 🎨 FASE 6: UX POLISH (Priorità MEDIA)

### 6.1 Real-time Updates (3 giorni)
```javascript
// File: templates/index.html - Aggiungi WebSocket per updates

let ws = null;

function initWebSocket() {
    ws = new WebSocket(`ws://${window.location.host}/ws`);
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        switch(data.type) {
            case 'budget_update':
                updateBudgetDisplay(data.payload);
                break;
            case 'obiettivo_progress':
                updateObiettivoProgress(data.obiettivo_id, data.progresso);
                break;
            case 'new_impegno':
                addImpegnoToCalendar(data.payload);
                break;
        }
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        // Fallback to polling
        startPolling();
    };
}

function updateBudgetDisplay(budgetData) {
    document.querySelector('.budget-oggi').textContent = `€${budgetData.oggi}`;
    document.querySelector('.budget-settimana').textContent = `€${budgetData.settimana}`;
    document.querySelector('.budget-mese').textContent = `€${budgetData.mese}`;
    
    // Animazione
    document.querySelector('.card.budget').classList.add('highlight-update');
    setTimeout(() => {
        document.querySelector('.card.budget').classList.remove('highlight-update');
    }, 1000);
}
```

**Backend WebSocket:**
```python
# File: app/websocket.py

from flask_sock import Sock
sock = Sock()

@sock.route('/ws')
def websocket(ws):
    user_ip = request.remote_addr
    
    while True:
        # Keep connection alive
        data = ws.receive()
        
        if data:
            # Handle client messages if needed
            pass

def broadcast_budget_update(user_ip, budget_data):
    """Invia aggiornamento budget a tutti i client dell'utente"""
    # Implementa broadcast logic
    pass
```

### 6.2 Loading States & Skeletons (2 giorni)
```css
/* File: static/css/loading.css */

.skeleton {
    background: linear-gradient(
        90deg,
        rgba(255, 255, 255, 0.05) 25%,
        rgba(255, 255, 255, 0.1) 50%,
        rgba(255, 255, 255, 0.05) 75%
    );
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
    border-radius: 8px;
}

@keyframes loading {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

.skeleton-card {
    height: 200px;
    margin-bottom: 20px;
}

.skeleton-text {
    height: 16px;
    margin-bottom: 8px;
    width: 80%;
}

.skeleton-button {
    height: 40px;
    width: 120px;
}
```

---

## 🌍 FASE 7: MULTILANG IMPROVEMENTS (Priorità BASSA)

### 7.1 Auto-Translation System (4 giorni)
```python
# File: scripts/auto_translate.py

from googletrans import Translator
import json

class AutoTranslator:
    def __init__(self):
        self.translator = Translator()
        self.supported_langs = ['en', 'es', 'zh-cn', 'ru', 'hi', 'ar']
    
    def translate_template(self, base_file, target_lang):
        """
        Traduce automaticamente un template HTML
        Preserva markup e JavaScript
        """
        with open(base_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Estrai testo traducibile (regex per tag HTML)
        import re
        text_pattern = r'>([^<]+)<'
        matches = re.finditer(text_pattern, content)
        
        translations = {}
        for match in matches:
            original_text = match.group(1).strip()
            if original_text and len(original_text) > 1:
                try:
                    translated = self.translator.translate(
                        original_text,
                        src='it',
                        dest=target_lang
                    ).text
                    translations[original_text] = translated
                except Exception as e:
                    print(f"Translation error: {e}")
        
        # Applica traduzioni
        translated_content = content
        for original, translated in translations.items():
            translated_content = translated_content.replace(
                f'>{original}<',
                f'>{translated}<'
            )
        
        # Salva
        output_file = base_file.replace('.html', f'_{target_lang}.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        print(f"✅ Translated {base_file} → {output_file}")
        print(f"   Translated {len(translations)} strings")
```

---

## 📦 DELIVERABLES & TIMELINE

### **ROADMAP 45 GIORNI:**

| Fase | Durata | Giorni | Priority |
|------|---------|---------|----------|
| **FASE 1: NLP Training** | 15 giorni | 1-15 | 🔴 ALTA |
| **FASE 2: Smart Links** | 9 giorni | 16-24 | 🔴 ALTA |
| **FASE 3: Analytics** | 5 giorni | 25-29 | 🟡 MEDIA |
| **FASE 4: Test Coverage** | 8 giorni | 30-37 | 🔴 ALTA |
| **FASE 5: Performance** | 7 giorni | 38-44 | 🟡 MEDIA |
| **FASE 6: UX Polish** | 5 giorni | (parallel) | 🟡 MEDIA |
| **FASE 7: Multilang** | 4 giorni | (parallel) | 🟢 BASSA |

### **MILESTONE:**
- ✅ **Giorno 15:** NLP 95%+ accuracy
- ✅ **Giorno 24:** Smart Links completo (YT+AMZ+Web)
- ✅ **Giorno 29:** Analytics live con grafici
- ✅ **Giorno 37:** Test coverage 80%+
- ✅ **Giorno 44:** Performance ottimizzata
- 🎉 **Giorno 45:** **RELEASE 2.0!**

---

## 🎯 METRICHE DI SUCCESSO

### **BEFORE (MVP 1.0):**
- NLP Accuracy: 75%
- Test Coverage: 40%
- Page Load: 2.5s
- API Response: 800ms
- Smart Links: 1/3 (Web only)
- Analytics: Placeholder
- Real-time: No

### **AFTER (v2.0 - Target):**
- NLP Accuracy: **95%+** ✅
- Test Coverage: **80%+** ✅
- Page Load: **1.2s** ✅ (50% faster)
- API Response: **300ms** ✅ (60% faster)
- Smart Links: **3/3** ✅ (YouTube, Amazon, Web)
- Analytics: **Live charts** ✅
- Real-time: **WebSocket** ✅

---

## 📚 RISORSE NECESSARIE

### **API Keys:**
- YouTube Data API v3 (gratuita, 10k richieste/giorno)
- Amazon Product Advertising API (richiede account affiliato)
- Google Cloud Translation API (opzionale, $20/1M chars)

### **Servizi Esterni:**
- Redis Cloud (gratuito fino a 30MB)
- GitHub Actions (gratuito per progetti open-source)
- Sentry.io (error tracking, gratuito fino a 5k eventi/mese)

### **Python Packages:**
```txt
# requirements_training.txt
spacy>=3.5.0
spacy-transformers>=1.2.0
it-core-news-sm @ https://github.com/explosion/spacy-models/releases/download/it_core_news_sm-3.5.0/it_core_news_sm-3.5.0-py3-none-any.whl
google-api-python-client>=2.80.0
googletrans==4.0.0rc1
beautifulsoup4>=4.11.0
flask-sock>=0.6.0
```

---

## 🚨 RISCHI & MITIGAZIONI

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| Amazon scraping bloccato | Alta | Alto | Usa API ufficiale o servizi terzi |
| YouTube API quota exceeded | Media | Medio | Cache aggressiva (24h), fallback a ricerca Google |
| NLP training richiede troppo tempo | Bassa | Alto | Usa modelli pre-trained (spaCy IT) |
| Test coverage rallenta sviluppo | Media | Basso | Parallelizza con sviluppo feature |
| Redis costo aumenta | Bassa | Medio | Monitoraggio + fallback a SimpleCache |

---

## 📝 CHECKLIST FINALE

**Prima di ogni deploy:**
- [ ] Test pass (pytest -v)
- [ ] Linter pass (black, isort)
- [ ] Coverage > target
- [ ] Performance benchmark
- [ ] Security audit
- [ ] Backup database
- [ ] Rollback plan pronto

**Dopo deploy:**
- [ ] Smoke test su produzione
- [ ] Monitoring attivo (Sentry, logs)
- [ ] User feedback raccolto
- [ ] Metriche registrate
- [ ] Documentazione aggiornata

---

## 🎉 CONCLUSIONE

Questo piano porta l'app da **MVP funzionale (95%)** a **prodotto maturo e scalabile (100%)**. 

**Focus principale:**
1. 🎓 **NLP Training** - Fondamentale per UX
2. 🔗 **Smart Links** - Differenziatore competitivo
3. 🧪 **Test Coverage** - Qualità del codice
4. ⚡ **Performance** - Scalabilità

**Risultato finale:** App pronta per **10k+ utenti**, **Product Hunt #1**, e **monetizzazione**.

---

**NEXT STEP:** Iniziare FASE 1 (NLP Training) o prioritizzare diversamente?
