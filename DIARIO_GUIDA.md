# 📔 Guida al Diario Personale Intelligente

## 🎯 Cos'è il Diario?

Il diario è una funzionalità che ti permette di scrivere riflessioni libere, pensieri personali, apprendimenti e note che vengono **automaticamente analizzate** e categorizzate dall'intelligenza artificiale.

---

## ✨ Funzionalità Principali

### 1. **Scrittura Libera**
Scrivi come parleresti con un amico. L'assistente capisce la differenza tra:
- **Agenda**: Impegni strutturati con orari
- **Diario**: Riflessioni personali e pensieri

### 2. **Estrazione Automatica**
Dall'intelligenza AI estrae automaticamente:
- 👥 **Persone** menzionate (es. "Sara", "Marco")
- 🏷️ **Parole chiave** più importanti
- 😊 **Sentiment** (positivo, neutro, negativo)
- 💭 **Emozioni** espresse (felice, motivato, stanco, etc.)

### 3. **Ricerca Intelligente**
Cerca nel diario per:
- Parole chiave
- Periodo temporale
- Sentiment/emozione
- Persona menzionata

---

## 📝 Come Usare il Diario

### Esempi di Input Diario

```
"Oggi ho parlato con Sara e ho capito i cicli for in Python. 
Mi sento motivato e voglio continuare a studiare!"
```

**L'assistente estrae:**
- Persona: Sara
- Argomenti: Python, cicli for, studiare
- Sentiment: positivo
- Emozione: motivato

---

```
"Ieri alla palestra ho fatto un ottimo allenamento. 
Ho incontrato Marco e abbiamo parlato del progetto."
```

**L'assistente estrae:**
- Persone: Marco
- Argomenti: palestra, allenamento, progetto
- Sentiment: positivo
- Data: Ieri

---

```
"Mi sento stanco oggi. Non ho voglia di studiare 
ma devo finire l'esercizio di matematica."
```

**L'assistente estrae:**
- Argomenti: studiare, matematica, esercizio
- Sentiment: negativo
- Emozione: stanco
- Data: Oggi

---

## 🧠 Come l'AI Distingue Agenda vs Diario

### È **AGENDA** se:
- ✅ Contiene orari precisi ("dalle 10 alle 12")
- ✅ Menziona giorni della settimana per eventi futuri
- ✅ Ha struttura organizzativa ("studio", "riunione", "palestra")
- ✅ È breve e conciso

**Esempio Agenda:**
```
"Lunedì studio Python dalle 10 alle 12"
"Mercoledì riunione alle 15"
```

### È **DIARIO** se:
- ✅ Contiene riflessioni personali
- ✅ Menziona persone con cui hai parlato
- ✅ Esprime emozioni e sentimenti
- ✅ Descrive apprendimenti o esperienze
- ✅ È più lungo e discorsivo (10+ parole)

**Esempio Diario:**
```
"Ho capito finalmente come funzionano i dizionari. 
Sara mi ha spiegato tutto molto bene e ora mi sento pronto 
per l'esame."
```

---

## 🎨 Concetti Estratti Automaticamente

### 1. **Persone**
Nomi propri che iniziano con maiuscola:
- "Sara", "Marco", "Luigi"
- Esclusi giorni settimana: "Lunedì", "Martedì"

### 2. **Parole Chiave**
Parole significative (4+ lettere) escludendo stop words:
- ✅ Include: "Python", "studiare", "allenamento", "progetto"
- ❌ Esclude: "il", "la", "con", "per", "ho", "sono"

### 3. **Emozioni Riconosciute**
- 😊 Positive: felice, motivato, entusiasta, sereno
- 😐 Neutre: normale, tranquillo
- 😔 Negative: triste, stanco, stressato, annoiato, ansioso

### 4. **Sentiment Globale**
Calcolato in base alle emozioni presenti:
- **Positivo**: più emozioni positive
- **Negativo**: più emozioni negative
- **Neutro**: equilibrio o assenza di emozioni chiare

---

## 📊 Visualizzazione

### Nell'Interfaccia
Il diario mostra:
- 📅 Data dell'entry
- 😊 Emoji sentiment
- 📝 Testo (anteprima 100 caratteri)
- 🏷️ Top 3 parole chiave

### Esempio Visuale
```
😊 1 Nov 2025
Oggi ho parlato con Sara e ho capito i cicli for in Python...
🏷️ Python, cicli, Sara
```

---

## 🔍 API Endpoints Disponibili

### GET `/api/diario`
Recupera ultime 30 entry del diario

### POST `/api/diario`
Crea nuova entry
```json
{
  "testo": "Oggi ho imparato...",
  "data": "2025-11-01"  // opzionale
}
```

### POST `/api/diario/cerca`
Cerca nel diario
```json
{
  "parola_chiave": "Python",
  "data_inizio": "2025-10-01",
  "data_fine": "2025-11-01",
  "sentiment": "positivo"
}
```

### DELETE `/api/diario/<id>`
Elimina una entry

---

## 💡 Tips per Scrivere Bene

### ✅ DO - Fai Così
- Scrivi naturalmente, come parleresti
- Esprimi emozioni e sentimenti
- Menziona persone, luoghi, argomenti
- Descrivi cosa hai imparato
- Rifletti su esperienze

### ❌ DON'T - Evita
- Non essere troppo generico
- Non usare solo abbreviazioni
- Non scrivere frasi troppo corte (< 10 parole)
- Non fare solo liste

---

## 🎯 Casi d'Uso Pratici

### 📚 Tracking Apprendimento
```
"Oggi ho capito finalmente i puntatori in C. 
Marco mi ha spiegato con un esempio pratico ed è stato 
molto chiaro. Ora voglio esercitarmi di più."
```
→ Tiene traccia di cosa hai imparato e con chi

### 🏃 Diario Sportivo
```
"Allenamento intenso oggi. Ho corso 5km in 25 minuti, 
nuovo record personale! Mi sento energico e motivato 
per continuare."
```
→ Traccia progressi e stato fisico/mentale

### 💼 Riflessioni Professionali
```
"La riunione con il cliente è andata bene. Luigi ha 
apprezzato la presentazione e abbiamo deciso di 
procedere con il progetto. Mi sento sollevato."
```
→ Documenta eventi lavorativi e persone

### 🧘 Mindfulness
```
"Oggi mi sento ansioso per l'esame. Ho studiato molto 
ma ho paura di non ricordare tutto. Devo rilassarmi."
```
→ Esprime emozioni e stati d'animo

---

## 🔮 Funzionalità Future

### In Sviluppo
- 📈 Grafici sentiment nel tempo
- 🔗 Collegamenti automatici tra entry correlate
- 📸 Supporto allegati immagini
- 🎙️ Dettatura vocale
- 🤖 Suggerimenti basati su pattern personali

### AI Avanzata
- Riconoscimento temi ricorrenti
- Suggerimenti proattivi
- Correlazione tra mood e produttività
- Generazione insights settimanali

---

## 🎉 Prova Subito!

Scrivi nella chat:

```
"Oggi ho parlato con Sara e ho capito i cicli for in Python. 
Mi sento motivato!"
```

E guarda come l'assistente estrae automaticamente tutti i concetti! 📔✨

---

**Creato per aiutarti a riflettere, crescere e ricordare! 💫**

