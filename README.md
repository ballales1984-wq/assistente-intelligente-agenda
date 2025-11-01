# 🧠 Assistente Intelligente - Agenda & Diario

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![AI](https://img.shields.io/badge/AI-NLP-purple.svg)

**Un assistente intelligente che organizza la tua vita attraverso linguaggio naturale**

[Features](#-features) • [Demo](#-demo) • [Installazione](#-installazione) • [Documentazione](#-documentazione) • [Contribuire](#-contribuire)

</div>

---

## 🎯 Cos'è

Un'applicazione web intelligente che combina **Agenda**, **Diario Personale** e **Pianificazione Automatica** in un unico sistema. Scrivi in linguaggio naturale e l'AI capisce cosa vuoi fare, organizza il tuo tempo e tiene traccia delle tue riflessioni.

### ✨ In Poche Parole

Scrivi: *"Voglio studiare Python 3 ore a settimana"*  
→ **L'assistente** crea l'obiettivo e pianifica automaticamente le sessioni

Scrivi: *"Lunedì riunione dalle 10 alle 12"*  
→ **Il calendario** mostra l'impegno nella vista settimanale

Scrivi: *"Oggi ho parlato con Sara e ho capito i cicli for. Mi sento motivato!"*  
→ **Il diario** salva la riflessione ed estrae automaticamente: Sara, cicli for, Python, sentiment positivo 😊

---

## 🧩 Moduli principali

### 1. **Input Manager**
- Riceve input testuale
- Analizza obiettivi, impegni, preferenze
- Esempi di input:
  - "Studio Python 3h a settimana"
  - "Domenica vado al mare dalle 16 alle 20"
  - "Questa settimana voglio riposare di più"

### 2. **Profilo Utente**
- Parametri personalizzabili:
  - `stress_tollerato`: alto, medio, basso
  - `concentrazione`: ottima, media, scarsa
  - `priorità`: studio, sport, riposo, lavoro
  - `stile_vita`: intensivo, bilanciato, rilassato

### 3. **Obiettivi**
- Ogni obiettivo ha:
  - `nome`: es. "Studiare Python"
  - `durata_settimanale`: es. 3h
  - `scadenza`: es. 30 giorni
  - `intensità`: alta, media, bassa
  - `tipo`: studio, sport, progetto, personale

### 4. **Agenda Dinamica**
- Genera piano settimanale/mensile
- Incrocia:
  - Obiettivi
  - Impegni fissi
  - Parametri personali
- Output: tabella con orari, attività, suggerimenti

### 5. **Motore Adattivo**
- Rivede il piano in tempo reale
- Esempi:
  - "Hai finito lo studio, ora hai 3h libere"
  - "Alle 21 puoi fare ginnastica o rilassarti"
  - "Hai detto che sei stanco, riduco il carico"

### 6. **Interfaccia Testuale**
- Chat semplice (web o Telegram)
- Tu scrivi → lei risponde con piano, consigli, notifiche

---

## 🛠️ Tecnologie

| Funzione | Tecnologia |
|---------|------------|
| Backend | Python |
| Web App | Flask |
| Database | SQLite (iniziale), PostgreSQL (scalabile) |
| NLP | spaCy, GPT API (facoltativo) |
| Frontend | HTML/CSS base |
| Notifiche | Telegram Bot, email, o web alerts |

---

## 📁 Struttura Progetto

```
agenda/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user_profile.py
│   │   ├── obiettivo.py
│   │   └── impegno.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── input_manager.py
│   │   ├── agenda_dinamica.py
│   │   └── motore_adattivo.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── api.py
│   └── database/
│       └── db.py
├── static/
│   ├── css/
│   └── js/
├── templates/
│   └── index.html
├── config.py
├── requirements.txt
└── run.py
```

---

## 🚀 Come Iniziare

1. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

2. Avvia l'applicazione:
```bash
python run.py
```

3. Apri il browser su: `http://localhost:5000`

---

## 📅 Roadmap

- [x] Setup iniziale del progetto
- [ ] Definire struttura dati (variabili, tipi, valori)
- [ ] Scrivere prototipo base: Input testuale → piano settimanale
- [ ] Testare adattamento con parametri diversi
- [ ] Costruire interfaccia testuale
- [ ] Integrazione NLP per analisi input
- [ ] Sistema di notifiche
- [ ] Documentazione completa

---

## 📸 Screenshots

### 💬 Chat Intelligente
L'assistente capisce linguaggio naturale e distingue automaticamente tra agenda e diario.

### 📅 Calendario Settimanale
Vista timeline completa con tutti i tuoi impegni, obiettivi e pause.

### 📔 Diario Personale
Riflessioni automaticamente analizzate con estrazione di concetti chiave.

---

## 🌟 Casi d'Uso

### 👨‍🎓 Studente
```
"Studiare matematica 5 ore a settimana"
"Lunedì lezione dalle 9 alle 13"
"Oggi ho capito finalmente gli integrali!"
```
→ Piano studio ottimizzato + diario apprendimento

### 💼 Professionista
```
"Lavorare su progetto Alpha 10 ore a settimana"
"Mercoledì meeting dalle 15 alle 16"
"Riunione andata bene, cliente soddisfatto"
```
→ Gestione tempo lavoro + note professionali

### 🏃 Fitness Enthusiast
```
"Palestra 4 ore a settimana"
"Martedì allenamento dalle 18 alle 19"
"Nuovo record personale! Mi sento energico"
```
→ Schedule sport + tracking progressi

---

## 🛠️ Stack Tecnologico

- **Backend**: Python 3.8+ con Flask
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **AI/NLP**: Custom regex-based + sentiment analysis
- **Testing**: pytest

---

## 🗺️ Roadmap

### ✅ Completato
- [x] Chat intelligente NLP
- [x] Gestione obiettivi e impegni
- [x] Generazione piano settimanale
- [x] Diario personale con AI
- [x] Calendario settimanale visuale
- [x] Sentiment analysis
- [x] Estrazione concetti automatica

### 🚧 In Sviluppo
- [ ] Notifiche push/email/Telegram
- [ ] Export piano (PDF, iCal)
- [ ] PWA per mobile
- [ ] Drag & drop calendario
- [ ] Impegni ricorrenti UI

### 🔮 Futuro
- [ ] Integrazione Google Calendar
- [ ] GPT API per NLP avanzato
- [ ] Dashboard analytics avanzata
- [ ] Multi-utente
- [ ] App mobile nativa

---

## 👥 Contribuire

Contributi benvenuti! 

1. Fork il progetto
2. Crea un branch (`git checkout -b feature/AmazingFeature`)
3. Commit le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

---

## 📝 Licenza

Distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

---

## 🙏 Ringraziamenti

- Flask per il framework web
- SQLAlchemy per l'ORM
- Tutti i contributori

---

## 📧 Contatti

**Progetto Link**: [https://github.com/tuousername/agenda](https://github.com/tuousername/agenda)

---

<div align="center">

**Se ti piace il progetto, lascia una ⭐!**

Made with ❤️ and ☕

</div>

