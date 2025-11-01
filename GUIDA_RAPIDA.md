# 🚀 Guida Rapida

## Installazione

### 1. Installa Python
Assicurati di avere Python 3.8+ installato:
```bash
python --version
```

### 2. Installa dipendenze
```bash
pip install -r requirements.txt
```

### 3. Setup database
```bash
python setup.py
```

### 4. Avvia l'applicazione
```bash
python run.py
```

### 5. Apri il browser
Vai su: http://localhost:5000

---

## 💬 Come usare la Chat

### Esempi di comandi

#### 📚 Aggiungere un obiettivo
```
"Voglio studiare Python 3 ore a settimana"
"Fare palestra 4 ore a settimana"
"Imparare inglese 2 ore a settimana"
```

#### 📅 Aggiungere un impegno
```
"Domenica vado al mare dalle 16 alle 20"
"Lunedì ho riunione dalle 10 alle 12"
"Venerdì cena con amici alle 20"
```

#### 😴 Comunicare il tuo stato
```
"Sono stanco"
"Sono concentrato"
"Sono stressato"
"Voglio riposare di più"
```

---

## 🎯 Gestire gli Obiettivi

1. **Aggiungi obiettivi** tramite chat o API
2. **Visualizza obiettivi** nella sezione "I Tuoi Obiettivi"
3. **Aggiorna** cliccando sul pulsante Aggiorna
4. Gli obiettivi vengono automaticamente **distribuiti** nel piano settimanale

---

## 📅 Generare il Piano

1. **Aggiungi almeno un obiettivo**
2. Clicca su **"✨ Genera Piano"**
3. Il sistema creerà un piano settimanale ottimizzato
4. Il piano considera:
   - I tuoi obiettivi
   - I tuoi impegni fissi
   - Le tue preferenze
   - Il tuo stile di vita

---

## 📊 Visualizzare Statistiche

- **Obiettivi totali**: Quanti obiettivi hai
- **Ore completate**: Quanto hai lavorato
- **Tasso completamento**: Percentuale di successo

Clicca "🔄 Aggiorna" per vedere i dati più recenti.

---

## 🔧 Personalizzazione Profilo

Puoi modificare il tuo profilo via API:

```bash
curl -X POST http://localhost:5000/api/profilo \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Mario",
    "stress_tollerato": "basso",
    "concentrazione": "ottima",
    "stile_vita": "intensivo"
  }'
```

### Parametri disponibili:

- **stress_tollerato**: `alto`, `medio`, `basso`
- **concentrazione**: `ottima`, `media`, `scarsa`
- **priorita**: `studio`, `sport`, `riposo`, `lavoro`, `bilanciato`
- **stile_vita**: `intensivo`, `bilanciato`, `rilassato`

---

## 🎨 Esempi di Utilizzo

### Scenario 1: Studente
```
"Studiare matematica 4 ore a settimana"
"Studiare fisica 3 ore a settimana"
"Palestra 3 ore a settimana"
"Lunedì lezione dalle 9 alle 13"
"Mercoledì lezione dalle 14 alle 18"
```

### Scenario 2: Lavoratore
```
"Progetto X 10 ore a settimana"
"Sport 3 ore a settimana"
"Lunedì-Venerdì lavoro dalle 9 alle 18"
"Mercoledì riunione dalle 15 alle 16"
```

### Scenario 3: Bilanciato
```
"Imparare chitarra 2 ore a settimana"
"Leggere libri 3 ore a settimana"
"Meditazione 1 ora a settimana"
"Voglio riposare di più"
```

---

## 🐛 Risoluzione Problemi

### Errore: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Errore: "Database locked"
Chiudi altre istanze dell'applicazione.

### Il piano è vuoto
Assicurati di aver aggiunto almeno un obiettivo.

### La chat non risponde
Verifica che il server Flask sia in esecuzione:
```bash
python run.py
```

---

## 📚 Risorse

- **README.md**: Panoramica generale
- **TECHNICAL_DOCS.md**: Documentazione tecnica completa
- **API**: http://localhost:5000/api/*

---

## 💡 Tips & Tricks

1. **Usa i quick actions** per esempi veloci
2. **Genera il piano** ogni settimana per rimanere aggiornato
3. **Monitora le statistiche** per vedere i tuoi progressi
4. **Comunica il tuo stato** per ricevere suggerimenti personalizzati
5. **Sperimenta** con diversi obiettivi e impegni

---

## 🎉 Divertiti!

L'assistente è progettato per aiutarti a organizzare la tua vita.
Più lo usi, più diventa utile! 🚀

