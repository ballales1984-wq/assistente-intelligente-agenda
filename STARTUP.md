# 🚀 Come Avviare il Progetto

## ⚡ Quick Start (3 Passi)

### 1️⃣ Installa le dipendenze
```bash
pip install -r requirements.txt
```

### 2️⃣ Inizializza il database
```bash
python setup.py
```

### 3️⃣ Avvia l'applicazione
```bash
python run.py
```

✅ **Fatto!** Apri il browser su: **http://localhost:5000**

---

## 📋 Checklist Pre-Avvio

- [ ] Python 3.8+ installato (`python --version`)
- [ ] Tutte le dipendenze installate
- [ ] Database inizializzato
- [ ] Porta 5000 libera

---

## 🎯 Primi Passi nell'App

### 1. Usa la Chat
Prova questi comandi:
```
"Voglio studiare Python 3 ore a settimana"
"Domenica vado al mare dalle 16 alle 20"
"Sono stanco"
```

### 2. Genera il Piano
- Aggiungi almeno un obiettivo
- Clicca "✨ Genera Piano"
- Visualizza il tuo piano settimanale

### 3. Monitora i Progressi
- Controlla le statistiche
- Aggiorna i tuoi obiettivi
- Adatta il piano in tempo reale

---

## 🛠️ Comandi Utili

### Avvio normale
```bash
python run.py
```

### Avvio con debug
```bash
# Il debug è già attivo in run.py
# Vedrai log dettagliati nella console
```

### Reset database
```bash
# Elimina il database esistente
del agenda.db  # Windows
# oppure
rm agenda.db   # Linux/Mac

# Ricrea tutto
python setup.py
```

### Verifica installazione
```bash
python -c "from app import create_app; print('✅ Tutto OK!')"
```

---

## 🌐 Accesso

- **URL**: http://localhost:5000
- **Porta**: 5000
- **Host**: 0.0.0.0 (accessibile dalla rete locale)

### Accedere da altri dispositivi
Se vuoi accedere da smartphone/tablet sulla stessa rete:
1. Trova il tuo IP locale: `ipconfig` (Windows) o `ifconfig` (Mac/Linux)
2. Usa: `http://TUO_IP:5000`

---

## 📁 Struttura Progetto

```
agenda/
├── app/                    # Core applicazione
│   ├── __init__.py        # Factory Flask
│   ├── models/            # Modelli database
│   │   ├── user_profile.py
│   │   ├── obiettivo.py
│   │   └── impegno.py
│   ├── core/              # Logica business
│   │   ├── input_manager.py
│   │   ├── agenda_dinamica.py
│   │   └── motore_adattivo.py
│   └── routes/            # API endpoints
│       └── api.py
├── templates/             # HTML templates
│   └── index.html
├── static/                # CSS, JS, immagini
│   ├── css/
│   └── js/
├── config.py              # Configurazione
├── run.py                 # Entry point
├── setup.py               # Setup database
├── requirements.txt       # Dipendenze Python
├── README.md              # Panoramica progetto
├── TECHNICAL_DOCS.md      # Documentazione tecnica
├── GUIDA_RAPIDA.md        # Guida utente
└── STARTUP.md             # Questa guida
```

---

## 🔍 Troubleshooting

### Errore: Porta 5000 già in uso
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Errore: ModuleNotFoundError
```bash
pip install -r requirements.txt --upgrade
```

### Errore: Database locked
- Chiudi tutte le istanze dell'app
- Elimina `agenda.db-journal` se esiste
- Riavvia l'app

### L'interfaccia non si carica
- Verifica che Flask sia in esecuzione
- Controlla la console per errori
- Prova in modalità incognito

---

## 🎓 Risorse di Apprendimento

### Per Utenti
- **GUIDA_RAPIDA.md**: Come usare l'applicazione
- **Interface Web**: Tutorial interattivi

### Per Sviluppatori
- **TECHNICAL_DOCS.md**: Architettura e API
- **Codice**: Commenti inline nel codice

---

## 🤝 Supporto

Hai domande? Problemi? Idee?

1. Controlla la documentazione
2. Verifica i troubleshooting comuni
3. Leggi il codice (è ben commentato!)

---

## 🎉 Pronto per Iniziare!

Segui i 3 passi sopra e sei pronto a usare il tuo assistente intelligente!

**Buon planning! 🚀**

