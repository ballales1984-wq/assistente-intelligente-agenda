# 📚 Documentazione Tecnica

## 🏗️ Architettura

### Modelli Dati

#### 1. UserProfile
Rappresenta il profilo personalizzato dell'utente.

**Campi:**
- `stress_tollerato`: `alto`, `medio`, `basso`
- `concentrazione`: `ottima`, `media`, `scarsa`
- `priorita`: `studio`, `sport`, `riposo`, `lavoro`, `bilanciato`
- `stile_vita`: `intensivo`, `bilanciato`, `rilassato`
- `ora_inizio_giornata`: Ora di inizio attività (default 08:00)
- `ora_fine_giornata`: Ora di fine attività (default 23:00)
- `ore_sonno_desiderate`: Ore di sonno desiderate (default 8)

#### 2. Obiettivo
Rappresenta un obiettivo da raggiungere.

**Campi:**
- `nome`: Nome dell'obiettivo
- `descrizione`: Descrizione dettagliata
- `tipo`: `studio`, `sport`, `progetto`, `personale`, `lavoro`
- `durata_settimanale`: Ore dedicate a settimana
- `scadenza`: Data entro cui completare (opzionale)
- `intensita`: `alta`, `media`, `bassa`
- `flessibilita`: Quanto può essere spostato nel tempo
- `orari_preferiti`: Es. "mattina", "pomeriggio", "sera"
- `giorni_preferiti`: Es. "lun,mer,ven"
- `ore_completate`: Tracking del progresso
- `attivo`: Se l'obiettivo è ancora valido

#### 3. Impegno
Rappresenta un impegno fisso in agenda.

**Campi:**
- `nome`: Nome dell'impegno
- `descrizione`: Descrizione
- `tipo`: `lavoro`, `appuntamento`, `evento`, `personale`
- `data_inizio`: Data e ora di inizio
- `data_fine`: Data e ora di fine
- `ricorrente`: Se l'impegno si ripete
- `pattern_ricorrenza`: `giornaliero`, `settimanale`, `mensile`
- `giorni_settimana`: Giorni della settimana se ricorrente
- `spostabile`: Se può essere riposizionato
- `priorita`: Da 1 a 10

---

## 🧠 Moduli Core

### 1. InputManager
Analizza l'input testuale dell'utente ed estrae informazioni strutturate.

**Pattern riconosciuti:**
- Obiettivo con ore: "Voglio studiare Python 3 ore a settimana"
- Impegno specifico: "Domenica vado al mare dalle 16 alle 20"
- Stato emotivo: "Sono stanco"
- Preferenza riposo: "Voglio riposare di più"

**Metodi principali:**
```python
InputManager.analizza_input(testo: str) -> Dict[str, Any]
```

**Output:**
```python
{
    'tipo': 'obiettivo' | 'impegno' | 'stato' | 'preferenza' | 'sconosciuto',
    'dati': {...},
    'testo_originale': 'testo input'
}
```

### 2. AgendaDinamica
Genera il piano settimanale basato su obiettivi, impegni e profilo utente.

**Algoritmo:**
1. Recupera obiettivi attivi e impegni della settimana
2. Per ogni giorno:
   - Posiziona impegni fissi
   - Calcola slot temporali liberi
   - Distribuisce obiettivi negli slot in base a:
     - Preferenze orarie
     - Giorni preferiti
     - Intensità dell'attività
     - Stile di vita dell'utente
   - Aggiunge pause intelligenti
3. Ordina attività per orario

**Metodi principali:**
```python
agenda = AgendaDinamica(user_profile)
piano = agenda.genera_piano_settimanale(data_inizio=None)
```

**Output:**
```python
[
    {
        'tipo': 'obiettivo' | 'impegno' | 'pausa',
        'nome': 'Nome attività',
        'data_inizio': datetime,
        'data_fine': datetime,
        'durata_ore': float,
        'intensita': 'alta' | 'media' | 'bassa',
        ...
    }
]
```

### 3. MotoreAdattivo
Adatta il piano in tempo reale in base allo stato dell'utente.

**Funzionalità:**
- Aggiorna stato emotivo/fisico
- Gestisce completamento attività
- Ricalcola tempo libero
- Genera suggerimenti contestuali
- Adatta il piano per nuovi eventi
- Analizza produttività

**Metodi principali:**
```python
motore = MotoreAdattivo(user_profile)

# Aggiorna stato
suggerimenti = motore.aggiorna_stato('energia', 'bassa')

# Completamento attività
risultato = motore.attivita_completata(attivita, tempo_effettivo=2.5)

# Adatta piano
nuovo_piano = motore.adatta_piano(piano_originale, nuovo_evento)

# Statistiche
stats = motore.analizza_produttivita(periodo_giorni=7)
```

---

## 🔌 API Endpoints

### Profilo
- `GET /api/profilo` - Recupera profilo utente
- `POST /api/profilo` - Crea/aggiorna profilo

### Chat
- `POST /api/chat` - Invia messaggio testuale
  ```json
  {
    "messaggio": "Voglio studiare Python 3 ore a settimana"
  }
  ```

### Obiettivi
- `GET /api/obiettivi` - Lista obiettivi attivi
- `POST /api/obiettivi` - Crea nuovo obiettivo
- `PUT /api/obiettivi/<id>` - Modifica obiettivo
- `DELETE /api/obiettivi/<id>` - Elimina obiettivo

### Impegni
- `GET /api/impegni` - Lista impegni futuri
- `POST /api/impegni` - Crea nuovo impegno

### Piano
- `GET /api/piano` - Genera piano settimanale

### Statistiche
- `GET /api/statistiche` - Recupera statistiche produttività

---

## 🎨 Logica di Pianificazione

### Priorità di Allocazione
1. **Impegni fissi** (non spostabili)
2. **Obiettivi ad alta priorità** con scadenza imminente
3. **Obiettivi ad alta intensità** negli slot ottimali
4. **Obiettivi medi/bassi** negli slot rimanenti
5. **Pause** dopo attività intense

### Considerazioni per Slot
- **Mattina (6-12)**: Studio, attività che richiedono concentrazione
- **Pomeriggio (12-18)**: Attività moderate, progetti
- **Sera (18-23)**: Sport, attività sociali, relax
- **Notte (23-6)**: Solo se specificato dall'utente

### Adattamenti in Base allo Stile di Vita
- **Intensivo**: 
  - Pause brevi (15 min)
  - Carico alto di attività
  - Focus su obiettivi prioritari
  
- **Bilanciato**:
  - Pause medie (30 min)
  - Equilibrio tra lavoro e riposo
  - Distribuzione equa
  
- **Rilassato**:
  - Pause lunghe (45 min)
  - Carico ridotto
  - Priorità al benessere

### Gestione Stress e Energia
- **Stress alto** → Riduzione carico, più pause
- **Energia bassa** → Attività leggere, posticipo attività intense
- **Concentrazione scarsa** → Slot brevi, pause frequenti

---

## 🚀 Estensioni Future

### NLP Avanzato
- Integrazione GPT per comprensione linguaggio naturale
- Riconoscimento contesto e intenti complessi
- Supporto multi-lingua

### Notifiche Intelligenti
- Push notifications web
- Integrazione Telegram Bot
- Email reminders
- SMS alerts

### Analytics
- Dashboard con grafici
- Trend produttività
- Heatmap attività
- Suggerimenti ML-based

### Integrations
- Google Calendar sync
- Todoist integration
- Notion export
- Apple Health / Google Fit

### Mobile App
- Progressive Web App (PWA)
- React Native app
- Widget iOS/Android

---

## 📊 Database Schema

```sql
-- user_profiles
CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    stress_tollerato VARCHAR(20) DEFAULT 'medio',
    concentrazione VARCHAR(20) DEFAULT 'media',
    priorita VARCHAR(50) DEFAULT 'bilanciato',
    stile_vita VARCHAR(20) DEFAULT 'bilanciato',
    ora_inizio_giornata TIME,
    ora_fine_giornata TIME,
    ore_sonno_desiderate INTEGER DEFAULT 8,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- obiettivi
CREATE TABLE obiettivi (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    nome VARCHAR(200) NOT NULL,
    descrizione TEXT,
    tipo VARCHAR(50) NOT NULL,
    durata_settimanale FLOAT NOT NULL,
    scadenza DATE,
    intensita VARCHAR(20) DEFAULT 'media',
    flessibilita VARCHAR(20) DEFAULT 'media',
    orari_preferiti VARCHAR(100),
    giorni_preferiti VARCHAR(100),
    ore_completate FLOAT DEFAULT 0.0,
    attivo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_profiles(id)
);

-- impegni
CREATE TABLE impegni (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    nome VARCHAR(200) NOT NULL,
    descrizione TEXT,
    tipo VARCHAR(50),
    data_inizio TIMESTAMP NOT NULL,
    data_fine TIMESTAMP NOT NULL,
    ricorrente BOOLEAN DEFAULT 0,
    pattern_ricorrenza VARCHAR(50),
    giorni_settimana VARCHAR(50),
    spostabile BOOLEAN DEFAULT 0,
    priorita INTEGER DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_profiles(id)
);
```

---

## 🧪 Testing

### Unit Tests
```bash
# Installa pytest
pip install pytest pytest-cov

# Esegui test
pytest tests/ -v --cov=app
```

### Test Manuali
1. Crea profilo utente
2. Aggiungi obiettivo via chat
3. Aggiungi impegno via chat
4. Genera piano settimanale
5. Verifica adattamento in tempo reale

---

## 🐛 Debugging

### Log Flask
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Query Database
```bash
sqlite3 agenda.db
sqlite> SELECT * FROM obiettivi;
sqlite> .exit
```

### Test API con curl
```bash
# Test chat
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messaggio": "Voglio studiare Python 3 ore a settimana"}'

# Test piano
curl http://localhost:5000/api/piano
```

---

## 📝 Best Practices

### Codice
- Seguire PEP 8 per Python
- Docstrings per tutte le funzioni
- Type hints quando possibile
- Gestione errori con try-except

### Database
- Usare transazioni per operazioni multiple
- Index su campi frequentemente cercati
- Backup regolari

### Sicurezza
- Validare sempre input utente
- Sanitize SQL queries (usa ORM)
- HTTPS in produzione
- Environment variables per secrets

