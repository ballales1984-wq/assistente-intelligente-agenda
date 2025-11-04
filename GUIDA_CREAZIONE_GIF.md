# 🎬 GUIDA: Crea GIF Animate per Homepage

## 🎯 GIF da Creare (4 totali)

### 1. **chat-to-goal.gif** - Chat → Obiettivo Creato
**Durata:** 5-8 secondi  
**Dimensioni:** 800x500px  
**Size target:** < 2MB

**Script:**
```
1. Focus su chat (2s)
2. Digita: "Voglio studiare Python 3 ore a settimana" (3s)
3. Premi Invio (0.5s)
4. Mostra risposta AI + obiettivo creato (2s)
```

**Commento da aggiungere:**
"💬 Scrivi in linguaggio naturale → 🎯 Obiettivo creato automaticamente"

---

### 2. **plan-generation.gif** - Genera Piano Settimanale
**Durata:** 6-8 secondi  
**Dimensioni:** 900x600px  
**Size target:** < 2.5MB

**Script:**
```
1. Mostra sezione Piano Settimanale vuoto (1s)
2. Click su "Genera Piano" (1s)
3. Calendario si popola con animazione (4s)
4. Zoom su calendario completo (2s)
```

**Commento da aggiungere:**
"🤖 AI genera il tuo piano perfetto in secondi"

---

### 3. **diary-sentiment.gif** - Diario con Sentiment Analysis
**Durata:** 5-7 secondi  
**Dimensioni:** 800x500px  
**Size target:** < 2MB

**Script:**
```
1. Focus su chat (1s)
2. Digita: "Oggi mi sento motivato e ho raggiunto i miei obiettivi!" (3s)
3. AI risponde con sentiment analysis (2s)
4. Mostra emoji sentiment 😊 (1s)
```

**Commento da aggiungere:**
"📔 Diario intelligente con analisi emotiva automatica"

---

### 4. **full-dashboard.gif** - Dashboard Completa
**Durata:** 8-10 secondi  
**Dimensioni:** 1200x700px  
**Size target:** < 3MB

**Script:**
```
1. Panoramica homepage (2s)
2. Scroll verso calendario (2s)
3. Mostra grafici analytics (2s)
4. Scroll verso diario book (2s)
5. Torna su (2s)
```

**Commento da aggiungere:**
"✨ Tutto sotto controllo: Calendario, Obiettivi, Spese, Diario, Analytics"

---

## 🛠️ TOOL CONSIGLIATO: ScreenToGif (Windows)

### Download
https://www.screentogif.com/

### Setup Ottimale
```
Frame Rate: 15 FPS
Encoder: FFmpeg
Quality: High (80-90%)
Size: Reduce by 50% if > 3MB
```

### Workflow
1. **Prepara la scena** - Apri l'app, posiziona la finestra
2. **Avvia ScreenToGif** - Click "Recorder"
3. **Posiziona il frame** - Allinea la selezione
4. **Record** - Click record, esegui le azioni
5. **Stop** - Click stop quando finisci
6. **Edit** - Aggiungi text overlays, riduci FPS se pesante
7. **Export** - Save as GIF

---

## 🎨 EDITING: Aggiungi Commenti

### Con ScreenToGif (Built-in)
```
1. Dopo la registrazione, click "Edit"
2. Seleziona frame dove vuoi il testo
3. Click "Caption" o "Text"
4. Aggiungi il commento
5. Scegli font grande, colore contrastante
6. Posiziona in basso o alto
```

### Con ezgif.com (Online)
```
1. Vai su https://ezgif.com/add-text
2. Upload la tua GIF
3. Add Text
4. Scrivi il commento
5. Scegli posizione, font, colore
6. Save
```

---

## 📐 SPECIFICHE TECNICHE

### Dimensioni Raccomandate
| GIF | Width | Height | Aspect Ratio |
|-----|-------|--------|--------------|
| Chat to Goal | 800px | 500px | 16:10 |
| Plan Generation | 900px | 600px | 3:2 |
| Diary Sentiment | 800px | 500px | 16:10 |
| Full Dashboard | 1200px | 700px | 12:7 |

### Ottimizzazione
```
✅ FPS: 12-15 (non di più)
✅ Colors: Reduce to 256 se > 2MB
✅ Dithering: Floyd-Steinberg
✅ Loop: Infinite
✅ Delay ultimo frame: +1000ms (pausa finale)
```

---

## 🚀 QUICK ACTIONS

### Per Ogni GIF:

**1. Prepara Browser**
```
- Zoom 100%
- Risoluzione 1920x1080
- Nascondi bookmarks bar
- Full screen mode (F11)
```

**2. Registra**
```
- Open ScreenToGif
- Set area 800x500 o dimensioni target
- Click Record
- Esegui azioni lentamente e chiaramente
- Stop
```

**3. Edita**
```
- Delete primi/ultimi frame inutili
- Aggiungi text overlay con commento
- Riduci FPS se > 20
- Crop se necessario
```

**4. Ottimizza**
```
- File → Save As → GIF
- Se > target size:
  - Reduce colors a 128
  - Remove ogni 2° frame
  - Resize 90%
```

**5. Testa**
```
- Apri in browser
- Verifica loop funziona
- Check leggibilità testo
- Verify size < target
```

---

## 📊 CHECKLIST PRE-REGISTRAZIONE

### Prima di Registrare Ogni GIF:

- [ ] App aperta e caricata completamente
- [ ] Dati di test presenti (obiettivi, impegni, diario)
- [ ] Dark mode OFF (più leggibile)
- [ ] Zoom browser 100%
- [ ] ScreenToGif pronto con area selezionata
- [ ] Script delle azioni a portata di mano
- [ ] Mouse cursor visible (importante!)

---

## 🎬 SEQUENZA DI REGISTRAZIONE

### Registra in Questo Ordine:

**1. chat-to-goal.gif** (più facile)
- Più semplice, usala come test

**2. diary-sentiment.gif** (simile)
- Stessa meccanica del primo

**3. plan-generation.gif** (media difficoltà)
- Richiede dati pre-caricati

**4. full-dashboard.gif** (più complessa)
- Richiede coordinazione scroll

**Tempo totale stimato:** 1-2 ore (incluso editing)

---

## 💾 DOVE SALVARE LE GIF

### Struttura File:
```
agenda/
├── static/
│   ├── gifs/
│   │   ├── chat-to-goal.gif
│   │   ├── plan-generation.gif
│   │   ├── diary-sentiment.gif
│   │   └── full-dashboard.gif
│   └── gifs/
│       └── thumbnails/
│           ├── chat-to-goal-thumb.jpg
│           ├── plan-generation-thumb.jpg
│           ├── diary-sentiment-thumb.jpg
│           └── full-dashboard-thumb.jpg
```

---

## 🆘 TROUBLESHOOTING

### GIF Troppo Grande (> 3MB)
```
Soluzione 1: Riduci FPS a 10
Soluzione 2: Riduci colors a 128
Soluzione 3: Resize 80%
Soluzione 4: Remove ogni 2° frame
```

### GIF Sgranata
```
Soluzione: Aumenta quality 90%
Soluzione: Usa encoder FFmpeg
Soluzione: Aumenta bitrate
```

### Testo Non Leggibile
```
Soluzione: Font più grande (24px+)
Soluzione: Outline/shadow sul testo
Soluzione: Background semi-trasparente dietro testo
```

### Loop Non Funziona
```
Soluzione: Verifica "Loop Forever" checked
Soluzione: Aggiungi delay ultimo frame +1000ms
```

---

## ✅ QUANDO HAI FINITO

**Testa Ogni GIF:**
1. Apri in browser
2. Verifica loop
3. Check size file
4. Leggibilità testo
5. Qualità immagine

**Mandami i file e aggiorno la homepage!**

---

## 🎨 TESTI DA USARE

### Overlay Text per Ogni GIF:

**chat-to-goal.gif:**
```
Top: "💬 Scrivi in linguaggio naturale"
Bottom: "🎯 Obiettivo creato automaticamente!"
```

**plan-generation.gif:**
```
Top: "🤖 Genera il tuo piano perfetto"
Bottom: "⚡ In pochi secondi!"
```

**diary-sentiment.gif:**
```
Top: "📔 Scrivi le tue riflessioni"
Bottom: "😊 Analisi emotiva automatica"
```

**full-dashboard.gif:**
```
Top: "✨ Tutto sotto controllo"
Bottom: "Calendario • Obiettivi • Diario • Analytics"
```

---

**Made with ❤️ for Product Hunt Success**  
**Target: GIF pronte in 1-2 ore! 🎬**

