# 💰 Guida al Sistema Gestione Spese

## 🎯 Cos'è

Il **Sistema Gestione Spese** è un modulo completo integrato nell'assistente che ti permette di tracciare, analizzare e controllare le tue spese quotidiane con categorizzazione automatica e insights intelligenti.

---

## ✨ Funzionalità Principali

### 1. **Tracking Automatico**
- 💬 Input linguaggio naturale
- 🏷️ Categorizzazione automatica (10 categorie)
- ⏰ Data e ora automatiche
- 📊 Calcolo totali real-time

### 2. **Categorie Automatiche**
```
🍕 Cibo: pranzo, cena, spesa, ristorante, bar
🚗 Trasporti: benzina, metro, taxi, treno
🎮 Svago: cinema, teatro, bar, pub
💊 Salute: farmacia, medico, palestra, sport
🏠 Casa: affitto, bollette, luce, gas
👕 Abbigliamento: vestiti, scarpe, negozio
💻 Tecnologia: computer, software, abbonamenti
📚 Istruzione: libri, corsi, università
🎁 Regali: compleanno, natale, festa
📦 Altro: tutto il resto
```

### 3. **Analisi Intelligenti**
- 📊 Breakdown per categoria
- 📈 Trend mensili
- 💡 Insights automatici
- 🎯 Budget check con proiezioni
- ⚠️ Alert superamento budget

### 4. **Statistiche**
- Oggi / Settimana / Mese
- Media giornaliera
- Top spese
- Necessarie vs Voluttuarie
- Confronto periodi

---

## 💬 Come Registrare Spese

### Input Naturale nella Chat

#### Formato Base:
```
"Spesa 12 euro per pranzo"
"Speso 5 euro di caffè"
"Pagato 50 euro benzina"
"Ho speso 20 euro per cinema"
```

#### Varianti Supportate:
```
"12 euro per pranzo"           → Riconosce importo e descrizione
"Spesa 15,50 euro colazione"   → Supporta decimali con virgola
"50 euro benzina"              → Ordine flessibile
"Pagato 8€ parcheggio"         → Supporta simbolo €
```

#### Con Data:
```
"Ieri spesa 30 euro supermercato"  → Registra per ieri
"Spesa 12 euro pranzo"             → Default: oggi
```

### Categorizzazione Automatica

L'AI riconosce la categoria dalla descrizione:

```
"Spesa 12 euro pranzo"         → Categoria: cibo
"50 euro benzina"              → Categoria: trasporti
"20 euro cinema"               → Categoria: svago
"15 euro farmacia"             → Categoria: salute
"10 euro palestra"             → Categoria: salute
"5 euro caffè"                 → Categoria: cibo
```

---

## 📊 Esempi Completi

### Esempio 1: Spesa Pranzo
```
Input: "Spesa 12 euro per pranzo"

Risposta:
💰 Spesa registrata!

💵 Importo: €12.00
📝 Descrizione: Pranzo
🏷️ Categoria: cibo

📊 Totale oggi: €12.00
```

### Esempio 2: Benzina
```
Input: "Pagato 50 euro benzina"

Risposta:
💰 Spesa registrata!

💵 Importo: €50.00
📝 Descrizione: Benzina
🏷️ Categoria: trasporti

📊 Totale oggi: €62.00
```

### Esempio 3: Cinema Ieri
```
Input: "Ieri spesa 15 euro cinema"

Risposta:
💰 Spesa registrata!

💵 Importo: €15.00
📝 Descrizione: Cinema
🏷️ Categoria: svago

📊 Totale oggi: €62.00  (riferito a oggi, spesa salvata per ieri)
```

---

## 💡 Domande Quick Actions

### 💵 Speso Oggi?
```
Click: "💵 Speso oggi?"

Risposta:
💰 Spese di Oggi

💵 Totale: €62.00
📌 Numero spese: 5
📊 Media: €12.40

🏷️ Per categoria:
  • cibo: €27.00
  • trasporti: €50.00
  • svago: €15.00

💡 Insights:
  • 📊 Categoria principale: trasporti (€50.00, 45.2%)
  • ✅ Buon equilibrio: 24.2% voluttuarie
  • 💰 Media giornaliera: €62.00
```

### 📊 Speso Settimana?
```
Click: "📊 Speso settimana?"

Risposta:
📊 Spese della Settimana

📅 28 Ott → 3 Nov

💵 Totale: €342.50
📌 Numero spese: 28
📊 Media giornaliera: €48.93

🏷️ Per categoria:
  • cibo: €150.00
  • trasporti: €100.00
  • svago: €60.00
  • salute: €32.50

💡 Insights:
  • 📊 Categoria principale: cibo (€150.00, 43.8%)
  • ✅ Buon equilibrio: 17.5% voluttuarie
```

### 📈 Speso Mese?
```
Click: "📈 Speso mese?"

Risposta:
📈 Spese del Mese

📅 1 Ott → 31 Ott

💵 Totale: €1,235.80
📌 Numero spese: 97
📊 Media giornaliera: €39.87

🏷️ Per categoria:
  • cibo: €450.00
  • trasporti: €280.00
  • casa: €200.00
  • svago: €150.00
  • salute: €89.80
  • altro: €66.00
```

### 🎯 Check Budget
```
Click: "🎯 Check budget"
Input: €1200

Risposta:
🟢 Budget Check

💰 Budget: €1200.00
💸 Speso: €735.40 (61.3%)
💵 Rimanente: €464.60
📅 Giorni rimanenti: 10
📊 Budget giornaliero: €46.46/giorno

🔮 Proiezione fine mese: €1,134.67

🟢 Tutto ok! Proiezione: €1,134.67. Risparmierai circa €65.33
```

---

## 🎨 UI - Sezione Budget & Spese

### Card Budget & Spese (a destra)

```
┌─────────────────────────────┐
│ 💰 Budget & Spese            │
├─────────────────────────────┤
│  Oggi:          €62.00       │
│  Questa Sett:   €342.50      │
│  Questo Mese:   €1,235.80    │
├─────────────────────────────┤
│  Ultime Spese:               │
│  💰 €50.00 Benzina • 1 Nov   │
│  💰 €12.00 Pranzo • 1 Nov    │
│  💰 €15.00 Cinema • 31 Ott   │
│  💰 €8.50 Caffè • 31 Ott     │
│  💰 €30.00 Spesa • 31 Ott    │
│                              │
│  ...e altre 23 spese         │
├─────────────────────────────┤
│     [🔄 Aggiorna]            │
└─────────────────────────────┘
```

---

## 🔌 API Endpoints

### CRUD Spese
```
GET    /api/spese              → Lista spese recenti
POST   /api/spese              → Crea nuova spesa
GET    /api/spese/<id>         → Dettaglio spesa
PUT    /api/spese/<id>         → Modifica spesa
DELETE /api/spese/<id>         → Elimina spesa
```

### Analisi
```
GET  /api/spese/oggi           → Spese di oggi
GET  /api/spese/settimana      → Spese settimana
GET  /api/spese/mese           → Spese mese
POST /api/spese/budget         → Check budget
GET  /api/spese/categoria/<cat> → Stats categoria
GET  /api/spese/top            → Top spese
```

---

## 💡 Use Cases Pratici

### Scenario 1: Tracking Giornaliero
```
Mattina: "5 euro caffè"
Pranzo: "Spesa 12 euro pranzo"
Pomeriggio: "30 euro spesa supermercato"
Sera: "Quanto ho speso oggi?"
→ Vedi: €47.00 con breakdown categorie
```

### Scenario 2: Budget Mensile
```
Inizio mese: "🎯 Check budget" → €1000
Metà mese: Controlli di nuovo
→ Vedi: Speso €580, rimangono €420, budget giornaliero €28
→ Proiezione: €1,042 (attenzione!)
→ Aggiusti comportamento
```

### Scenario 3: Analisi Categoria
```
Fine mese: Guardi breakdown
→ Vedi: Cibo €450 (37%), Trasporti €280 (23%)
→ Insights: "Categoria principale: cibo"
→ Decidi: Ridurre pranzi fuori, cucinare di più
```

---

## 📊 Insights Automatici

### L'AI Genera:

#### Su Categorie:
```
"📊 Categoria principale: cibo (€150.00, 43.8%)"
"🏷️ Trasporti in aumento rispetto a mese scorso"
```

#### Su Equilibrio:
```
"✅ Buon equilibrio: 17.5% voluttuarie"
"💡 40.2% di spese voluttuarie - Considera di ridurre"
```

#### Su Media:
```
"💰 Media giornaliera: €39.87"
"📊 Sopra la media del mese scorso"
```

---

## 🎯 Budget Check Features

### Cosa Calcola:

- **Speso**: Quanto hai già speso
- **Rimanente**: Quanto ti resta
- **Percentuale**: % budget usato
- **Giorni rimanenti**: Fino a fine mese
- **Budget giornaliero**: Quanto puoi spendere/giorno
- **Proiezione**: Stima fine mese
- **Alert**: Avvisi intelligenti

### Alert System:

```
🟢 OK (< 80%)
→ "Tutto ok! Risparmierai €XX"

🟡 ATTENZIONE (80-99%)
→ "Hai usato 85%! Proiezione: €XXX"

🔴 SUPERATO (≥ 100%)
→ "BUDGET SUPERATO! Hai speso il 105%"
```

---

## 📈 Statistiche Categoria

### Analisi Profonda Per Categoria:

```
GET /api/spese/categoria/cibo?mesi=3

Risposta:
{
  "categoria": "cibo",
  "periodo_mesi": 3,
  "totale": €1,350.00,
  "num_spese": 89,
  "media": €15.17,
  "max": {
    "importo": €85.00,
    "descrizione": "Cena ristorante",
    "data": "2025-10-15"
  },
  "min": {
    "importo": €2.50,
    "descrizione": "Caffè",
    "data": "2025-09-20"
  },
  "trend": "stabile"
}
```

---

## 🎨 Integrazione Completa

### Con Diario:
```
"Oggi pranzo €12. Ho parlato con Sara del progetto"
→ Salva spesa (€12, cibo)
→ Salva diario (Sara, progetto)
```

### Con Agenda:
```
"Lunedì dalle 12 alle 13 pranzo con Marco, spesa 25 euro"
→ Crea impegno (Lunedì 12-13)
→ Registra spesa (€25, cibo)
```

### Con Manager Temporali:
- **Passato**: "Quanto ho speso settimana scorsa?"
- **Presente**: "Posso permettermi €30 oggi?"
- **Futuro**: "Proiezione spese fine mese?"

---

## 💡 Pattern Riconosciuti

### ✅ Formato Accettati:

```
"spesa X euro per Y"
"speso X euro Y"
"pagato X euro Y"
"X euro per Y"
"X€ Y"
"costo X euro"
```

### ✅ Esempi Validi:

```
"Spesa 12 euro pranzo"          ✅
"Speso 5,50 euro caffè"         ✅
"Pagato 50€ benzina"            ✅
"15 euro per cinema"            ✅
"Ho speso 8 euro parcheggio"    ✅
"Ieri 25 euro cena"             ✅
```

---

## 📊 Dashboard Budget

### Nella UI Vedi:

```
💰 Budget & Spese
├─ Oggi:          €62.00
├─ Questa Sett:   €342.50
└─ Questo Mese:   €1,235.80

Ultime Spese:
• €50.00 Benzina
• €12.00 Pranzo
• €15.00 Cinema
...
```

### Quick Actions:
```
💵 Speso oggi?       → Analisi giornata
📊 Speso settimana?  → Analisi settimana
📈 Speso mese?       → Analisi mese
🎯 Check budget      → Controllo budget (input importo)
```

---

## 🎯 Workflow Consigliato

### Quotidiano:
```
Mattina: "5 euro caffè"
Pranzo: "12 euro pranzo"
Sera: "💵 Speso oggi?" → Controllo
```

### Settimanale (Domenica):
```
"📊 Speso settimana?"
→ Review spese
→ Identifica aree migliorabili
```

### Mensile (Fine mese):
```
"📈 Speso mese?"
"🎯 Check budget" (€1200)
→ Analisi completa
→ Planning mese prossimo
```

---

## 🔮 Proiezioni Budget

### L'AI Calcola:

**Scenario 1: Sotto Budget**
```
Budget: €1000
Speso: €620 (giorno 20/31)
Media: €31/giorno
Proiezione: €961
→ 🟢 Risparmierai €39!
```

**Scenario 2: Rischio**
```
Budget: €1000
Speso: €850 (giorno 20/31)
Media: €42.50/giorno
Proiezione: €1,317
→ 🟡 Rischi €317 di superamento!
→ Budget giornaliero: €13.64/giorno (rimanenti 11 giorni)
```

**Scenario 3: Superato**
```
Budget: €1000
Speso: €1,050 (giorno 20/31)
→ 🔴 BUDGET SUPERATO!
→ Hai già speso il 105%
```

---

## 📈 Statistiche Avanzate

### Confronto Mesi:
```python
# Via API
POST /api/passato/periodo
{
  "data_inizio": "2025-09-01",
  "data_fine": "2025-09-30"
}

# Poi confronta con mese corrente
```

### Top Spese:
```
GET /api/spese/top?limite=10&giorni=30

→ Top 10 spese più alte ultimo mese
```

### Per Categoria:
```
GET /api/spese/categoria/cibo?mesi=6

→ Analisi 6 mesi categoria cibo
→ Trend, max, min, media
```

---

## 🎨 Esempi Input Variati

### Cibo:
```
"12 euro pranzo"
"5,50 euro caffè"
"30 euro spesa"
"25 euro pizza"
"8 euro colazione"
```

### Trasporti:
```
"50 euro benzina"
"2,50 euro metro"
"15 euro parcheggio"
"120 euro treno"
```

### Svago:
```
"20 euro cinema"
"15 euro teatro"
"50 euro concerto"
"30 euro bar"
```

### Salute:
```
"15 euro farmacia"
"80 euro dentista"
"40 euro palestra"
"12 euro integratori"
```

---

## 💎 Features Uniche

### 1. **Zero Configurazione**
Scrivi naturalmente, categorizza automaticamente

### 2. **Integrazione Totale**
Combina con diario e agenda in un solo input

### 3. **AI Insights**
Suggerimenti automatici su come ottimizzare

### 4. **Proiezioni Real-Time**
Vedi dove andrai a finire a fine mese

### 5. **Multi-Periodo**
Oggi, settimana, mese, custom

---

## 🚀 Prova Subito!

### 1. Apri App:
```
http://localhost:5000
```

### 2. Scrivi nella Chat:
```
"Spesa 12 euro per pranzo"
"5 euro caffè"
"50 euro benzina"
```

### 3. Click Quick Actions:
```
💵 Speso oggi?
📊 Speso settimana?
🎯 Check budget
```

### 4. Guarda Card "Budget & Spese"
Vedi totali e ultime spese!

---

## 🎯 Pro Tips

### ✅ DO - Fai Così:
- Registra spese subito dopo averle fatte
- Usa descrizioni chiare
- Check budget settimanalmente
- Review mensile per ottimizzazioni

### ❌ DON'T - Evita:
- Non aspettare fine giornata
- Non essere troppo generico
- Non dimenticare spese piccole (caffè, etc.)

---

## 🏆 Benefici

### 💰 **Consapevolezza**
- Sai esattamente dove vanno i soldi
- Nessuna sorpresa fine mese

### 📊 **Control**
- Budget check real-time
- Proiezioni accurate
- Decisioni informate

### 🎯 **Ottimizzazione**
- Identifica sprechi
- Riduci spese inutili
- Risparmia di più

### 📈 **Crescita**
- Trend visibili
- Pattern identificati
- Miglioramento continuo

---

## 🔗 Integrazione con Manager Temporali

### PassatoManager + Spese:
```
"Cosa ho fatto settimana scorsa?"
→ Include anche analisi spese del periodo
```

### PresenteManager + Spese:
```
"Cosa posso fare oggi?"
→ Considera budget rimanente giornaliero
```

### FuturoManager + Spese:
```
"Come sarà giovedì?"
→ Prevede spese basate su routine
```

---

## 🎉 Risultato

**Un Sistema Completo di Gestione Finanziaria Personale!**

- 💬 Input naturale
- 🏷️ Categorizzazione automatica
- 📊 Analisi real-time
- 🎯 Budget tracking
- 🔮 Proiezioni future
- 💡 Insights intelligenti

**Tutto integrato con agenda e diario! 💰✨**

---

**Inizia a tracciare le tue spese adesso!** 🚀

http://localhost:5000

