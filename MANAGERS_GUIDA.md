# ⏰ Guida ai Manager Temporali

## 🎯 Concetto

I **3 Manager Temporali** estendono l'assistente con la capacità di analizzare **Passato**, gestire **Presente** e prevedere **Futuro**.

---

## 🧩 I Tre Manager

### 1. ⏮️ **PassatoManager** - Analisi Storico

Analizza quello che hai fatto, estrae pattern e genera insights.

#### Funzionalità Principali:
- 📊 Analisi periodi passati
- 📈 Statistiche dettagliate
- 🔍 Ricerca pattern ricorrenti
- 💡 Insights automatici
- 📉 Trend produttività e mood

#### Domande che Risponde:
- *"Cosa ho fatto la settimana scorsa?"*
- *"Quanto ho studiato questo mese?"*
- *"Quali sono i miei pattern di attività?"*
- *"Come è cambiato il mio mood?"*

---

### 2. 📅 **PresenteManager** - Gestione Oggi

Genera e adatta il piano della giornata corrente.

#### Funzionalità Principali:
- 📋 Piano dettagliato giornata
- ⏰ Cosa fare adesso
- 🔄 Adattamento a stato mentale
- 💡 Suggerimenti real-time
- ⚡ Gestione energia

#### Domande che Risponde:
- *"Cosa devo fare oggi?"*
- *"Cosa faccio adesso?"*
- *"Come adatto il piano? Sono stanco"*
- *"Quanto tempo libero ho oggi?"*

---

### 3. 🔮 **FuturoManager** - Proiezioni Future

Simula giorni futuri e proietta competenze nel tempo.

#### Funzionalità Principali:
- 🎯 Simulazione giornate future
- 📈 Proiezione competenze
- 🏆 Milestones previsti
- 📊 Previsione densità giorni
- 💡 Suggerimenti preparazione

#### Domande che Risponde:
- *"Come sarà il mio giovedì?"*
- *"Quanto saprò di Python tra 6 mesi?"*
- *"Come sarà la prossima settimana?"*
- *"Quando raggiungerò livello esperto?"*

---

## 💬 Come Usarle

### Metodo 1: Quick Actions (UI)

Nella chat, sotto gli esempi, trovi **"⏰ Domande Temporali"**:

```
⏮️ Cosa ho fatto?       → Analizza settimana scorsa
📅 Cosa faccio oggi?    → Piano di oggi
⏰ Cosa faccio adesso?  → Attività corrente
🔮 Come sarà giovedì?   → Simula prossimo giovedì
📈 Proiezione future    → Proietta competenze
```

### Metodo 2: API Dirette

```javascript
// Passato
GET  /api/passato/settimana-scorsa
POST /api/passato/periodo
POST /api/passato/pattern

// Presente
GET  /api/presente/oggi
GET  /api/presente/adesso
POST /api/presente/adatta

// Futuro
GET  /api/futuro/simula/<data>
GET  /api/futuro/giovedi
POST /api/futuro/proietta
GET  /api/futuro/prossima-settimana
```

---

## 📊 Esempi Pratici

### ⏮️ **Passato - Cosa ho fatto?**

**Click su**: ⏮️ Cosa ho fatto?

**Risposta:**
```
📊 Settimana Scorsa

📅 25 Ott → 31 Ott

📌 Impegni: 12
⏰ Ore totali: 28.5h
📔 Riflessioni: 5
😊 Sentiment: positivo

💡 Insights:
  • Hai dedicato più tempo a: studio (15h)
  • 😊 Sentiment medio del periodo: positivo
  • 👥 Hai interagito con: Sara, Marco, Luigi
  • 📅 Hai avuto attività in 6 giorni
```

---

### 📅 **Presente - Piano di Oggi**

**Click su**: 📅 Cosa faccio oggi?

**Risposta:**
```
📅 Piano di Oggi

📊 4 attività programmate
⏰ 6.5h occupate | 8.5h libere

⏭️ Prossimo: Riunione alle 14:00

💡 Suggerimenti:
  • ⏰ Hai 8.5h libere oggi
  • 💡 Potresti dedicare tempo a: Studio Python
  • 🌿 Giornata leggera - ottimo per riposare
```

---

### ⏰ **Presente - Adesso**

**Click su**: ⏰ Cosa faccio adesso?

**Risposta:**
```
🆓 Sei libero! Prossimo impegno: Riunione tra 45 minuti

💡 Suggerimenti:
  • 💤 Fai pause più frequenti
  • 🚶 Una breve passeggiata può aiutare
  • 💧 Assicurati di idratarti bene
```

---

### 🔮 **Futuro - Come sarà giovedì?**

**Click su**: 🔮 Come sarà giovedì?

**Risposta:**
```
🔮 Previsione Thursday

📅 2025-11-07 (tra 6 giorni)

📌 Impegni fissi: 2
🎯 Obiettivi previsti: 3
⏰ Densità prevista: piena

💡 Preparazione:
  • 📅 Tra 6 giorni - Pianifica in anticipo
  • 📊 Giornata intensa - Organizza bene la mattina
  • ⏰ Prima attività: Studio alle 09:00
```

---

### 📈 **Futuro - Proiezione Competenze**

**Click su**: 📈 Proiezione future

**Ti chiede:**
- Obiettivo: `Python`
- Mesi: `6`

**Risposta:**
```
📈 Proiezione Python

⏰ Ore totali: 72h
🎯 Livello stimato: intermedio
📊 Buone fondamenta, puoi affrontare progetti.
💯 Progress to mastery: 0.72%

🏆 Traguardi:
  • Mese 1: 🌱 Prime 10 ore - Hai rotto il ghiaccio!
  • Mese 3: 🔥 50 ore - Inizi a sentirti a tuo agio
  • Mese 6: 💯 100 ore - Fondamenta solide costruite
```

---

## 🧠 Logica Intelligente

### PassatoManager

```python
# Analizza impegni, riflessioni, obiettivi
# Raggruppa per tipo e calcola metriche
# Estrae pattern ricorrenti (giorni/orari preferiti)
# Calcola trend temporali
# Genera insights automatici
```

**Outputs:**
- Riepilogo attività per tipo
- Ore totali per categoria
- Sentiment medio periodo
- Parole chiave e persone
- Trend produttività/mood

### PresenteManager

```python
# Genera timeline giornaliera
# Calcola ore libere/occupate
# Trova prossimo impegno
# Adatta piano a stato emotivo
# Genera suggerimenti contestuali
```

**Outputs:**
- Timeline ordinata
- Metriche giornata (ore, densità)
- Prossimo impegno
- Suggerimenti personalizzati

### FuturoManager

```python
# Simula giorni futuri
# Analizza routine su giorni simili
# Prevede allocazione obiettivi
# Proietta competenze nel tempo
# Genera milestones
```

**Outputs:**
- Previsione densità giorno
- Routine prevista
- Proiezione competenze
- Milestones e traguardi
- Confronto con standard

---

## 📊 Algoritmi Chiave

### 1. **Stima Livello Competenza**

```
0-10h      → Principiante assoluto
10-100h    → Principiante
100-500h   → Intermedio
500-1000h  → Intermedio avanzato
1000-2000h → Avanzato
2000-5000h → Esperto
5000+h     → Master
```

### 2. **Calcolo Densità Giornata**

```
80%+ ore occupate  → Molto piena 🔥
60-80%             → Piena 📊
40-60%             → Moderata ⚖️
20-40%             → Leggera 🌿
<20%               → Molto leggera 😌
```

### 3. **Analisi Sentiment Periodo**

```
Score positivo > negativo  → Periodo positivo
Score negativo > positivo  → Periodo negativo
Score equilibrato          → Periodo neutro
```

### 4. **Pattern Ricorrenti**

```
Analizza ultime 4-8 settimane
Identifica giorni/ore più frequenti
Trova routine consolidate
Suggerisce ottimizzazioni
```

---

## 🎯 Casi d'Uso Pratici

### Scenario 1: Review Settimanale

**Ogni Domenica:**
```
Click: ⏮️ Cosa ho fatto?
```

**Ottieni:**
- Riepilogo settimana
- Ore dedicate per attività
- Sentiment generale
- Insights su produttività

**Azione:**
- Valuta progressi
- Adatta obiettivi settimana prossima
- Celebra successi

---

### Scenario 2: Planning Mattutino

**Ogni Mattina:**
```
Click: 📅 Cosa faccio oggi?
```

**Ottieni:**
- Piano completo giornata
- Ore libere/occupate
- Prossimo impegno
- Suggerimenti

**Azione:**
- Organizza mentalmente
- Prepara materiali necessari
- Ottimizza energia

---

### Scenario 3: Check Real-Time

**Durante il giorno:**
```
Click: ⏰ Cosa faccio adesso?
```

**Ottieni:**
- Attività corrente o tempo libero
- Prossimo impegno
- Tempo rimanente

**Azione:**
- Stay on track
- Gestisci transizioni
- Sfrutta pause

---

### Scenario 4: Preparazione Settimanale

**Venerdì/Domenica:**
```
Click: 🔮 Come sarà giovedì?
```

**Ottieni:**
- Previsione giorno specifico
- Impegni già schedulati
- Densità prevista
- Come prepararsi

**Azione:**
- Pianifica in anticipo
- Prepara materiali
- Gestisci aspettative

---

### Scenario 5: Goal Setting

**Quando imposti obiettivi:**
```
Click: 📈 Proiezione future
Input: "Python", "6 mesi"
```

**Ottieni:**
- Ore totali accumulate
- Livello raggiungibile
- Milestones intermedi
- Confronto standard

**Azione:**
- Valuta realismo obiettivi
- Celebra milestones
- Aggiusta ritmo se necessario

---

## 🔬 API Reference Rapida

### PassatoManager

```python
# Settimana scorsa
GET /api/passato/settimana-scorsa

# Periodo personalizzato
POST /api/passato/periodo
{
  "data_inizio": "2025-10-01",
  "data_fine": "2025-10-31"
}

# Pattern ricorrenti
POST /api/passato/pattern
{
  "data_inizio": "2025-09-01",
  "data_fine": "2025-10-31"
}
```

### PresenteManager

```python
# Piano oggi
GET /api/presente/oggi

# Cosa fare adesso
GET /api/presente/adesso

# Adatta piano a stato
POST /api/presente/adatta
{
  "stato": "stanco",
  "data": "2025-11-01"
}
```

### FuturoManager

```python
# Simula giorno futuro
GET /api/futuro/simula/2025-11-15

# Prossimo giovedì
GET /api/futuro/giovedi

# Proietta competenze
POST /api/futuro/proietta
{
  "obiettivo": "Python",
  "ore_settimanali": 3,
  "mesi": 6
}

# Prossima settimana
GET /api/futuro/prossima-settimana
```

---

## 💡 Tips & Best Practices

### Per Analisi Passato
- 📅 Fai review settimanali/mensili
- 📊 Monitora trend nel tempo
- 🎯 Usa insights per migliorare

### Per Piano Presente
- 🌅 Controlla piano ogni mattina
- ⏰ Check "adesso" durante il giorno
- 🔄 Adatta se cambia stato

### Per Proiezioni Futuro
- 🎯 Usa per goal setting realistici
- 📈 Verifica milestones regolarmente
- 🔮 Pianifica settimana prossima

---

## 🎨 Funzionalità Avanzate

### Pattern Recognition
- Identifica giorni/ore preferiti
- Trova routine consolidate
- Suggerisce ottimizzazioni

### Adaptive Planning
- Riduce carico se stanco
- Aumenta produttività se energico
- Riorganizza se stressato

### Predictive Simulation
- Prevede densità giorni
- Stima carico settimanale
- Suggerisce preparazione

---

## 📊 Metriche Calcolate

### Passato
- Ore totali per categoria
- Numero impegni
- Sentiment medio
- Tasso completamento obiettivi
- Trend produttività

### Presente
- Ore occupate/libere
- Densità giornata
- Tempo al prossimo impegno
- Stato giornata

### Futuro
- Densità prevista
- Ore totali obiettivo
- Livello competenza stimato
- Progress to mastery

---

## 🚀 Quick Start

### Prova Subito:

1. **Apri app**: http://localhost:5000
2. **Aggiungi dati** (obiettivi, impegni, diario)
3. **Click su quick actions** temporali
4. **Vedi le analisi** generate!

---

## 🎯 Integrazione nel Workflow

### Routine Quotidiana Consigliata:

**🌅 Mattina:**
```
1. Click: "📅 Cosa faccio oggi?"
2. Leggi piano e preparati
3. Mental planning
```

**☀️ Durante Giorno:**
```
1. Click: "⏰ Cosa faccio adesso?"
2. Stay on track
3. Gestisci transizioni
```

**🌙 Sera:**
```
1. Scrivi riflessione diario
2. (Domenica) Click: "⏮️ Cosa ho fatto?"
3. Review e planning prossima settimana
```

**📅 Fine Settimana:**
```
1. Review settimana con PassatoManager
2. Prevedi prossima con FuturoManager
3. Aggiusta obiettivi se necessario
```

---

## 🏆 Benefici

### 📈 Consapevolezza
- Vedi cosa hai fatto realmente
- Non solo cosa volevi fare

### ⚡ Efficienza
- Piano ottimizzato ogni giorno
- Adattato al tuo stato

### 🎯 Goal Achievement
- Proiezioni realistiche
- Milestones chiari
- Motivazione continua

### 🧠 Self-Improvement
- Pattern identificati
- Trend visibili
- Insights actionable

---

## 🔮 Esempio Completo

### Workflow Completo:

```
1. Lunedì mattina:
   → "📅 Cosa faccio oggi?"
   → Vedi piano giornata

2. Durante settimana:
   → Aggiungi impegni via chat
   → Scrivi riflessioni diario
   → Check "adesso" quando serve

3. Venerdì:
   → "🔮 Come sarà giovedì prossimo?"
   → Vedi previsione e preparati

4. Domenica:
   → "⏮️ Cosa ho fatto?"
   → Review settimana
   → Insights e pattern

5. Goal setting:
   → "📈 Proiezione Python 6 mesi"
   → Vedi livello raggiungibile
   → Motiva a continuare
```

---

## 🎉 Risultato

Con i **3 Manager Temporali** l'assistente diventa una **macchina del tempo** che:

- ⏮️ **Analizza** il tuo passato
- 📅 **Organizza** il tuo presente
- 🔮 **Prevede** il tuo futuro

**Tutto automatico. Tutto intelligente. Tutto per te! ⏰✨**

---

**Prova le domande temporali nell'app!** 🚀

http://localhost:5000

