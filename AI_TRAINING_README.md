# 🤖 AI TRAINING - README

## 🎯 Obiettivo
Addestrare un modello NLP custom per riconoscere linguaggio naturale completo nell'app Assistente Intelligente.

---

## 🚀 QUICK START (5 minuti)

```bash
# 1. Rendi eseguibile lo script
chmod +x scripts/train_quick_start.sh

# 2. Esegui setup automatico
./scripts/train_quick_start.sh

# 3. Il resto è automatico! 🎉
```

**Cosa fa lo script:**
- ✅ Crea directories (data/, models/, logs/)
- ✅ Installa dipendenze (spaCy, transformers)
- ✅ Genera 800+ esempi sintetici
- ✅ Estrae input reali dai logs (se disponibili)
- ✅ Combina datasets
- ✅ Crea training script base
- ✅ Opzionalmente: avvia training subito

---

## 📁 Struttura File

```
assistente-intelligente-agenda/
├── 📋_PIANO_ADDESTRAMENTO_COMPLETO.md   # Piano dettagliato 8 settimane
├── AI_TRAINING_README.md                 # Questo file
│
├── scripts/
│   ├── train_quick_start.sh             # Setup automatico ⚡
│   ├── generate_synthetic_data.py       # Genera dataset sintetico
│   └── extract_user_inputs.py           # Estrae input reali
│
├── data/                                 # Datasets
│   ├── dataset_synthetic_800.json       # Esempi generati
│   ├── dataset_real_inputs.json         # Esempi reali (se disponibili)
│   └── dataset_combined.json            # Dataset finale
│
├── models/                               # Modelli trained
│   └── nlp_v1/                          # Primo modello
│
├── logs/
│   └── training/                        # Log training
│
└── app/ai/                              # Codice AI
    ├── nlp_model.py                     # Model definition
    ├── nlp_inference.py                 # Inference wrapper
    └── context_manager.py               # Gestione contesto conversazionale
```

---

## 🎓 TUTORIAL PASSO-PASSO

### Step 1: Genera Dataset
```bash
python scripts/generate_synthetic_data.py
```

**Output:** `data/dataset_synthetic_800.json`

**Contiene:**
- 150 esempi obiettivi ("Voglio studiare Python 3h/settimana")
- 200 esempi impegni ("Domani riunione 10-12")
- 150 esempi spese ("Speso 35 euro cena")
- 100 esempi diario ("Oggi mi sento felice")
- 100 esempi domande temporali ("Cosa faccio domani?")
- 100 esempi domande budget ("Quanto ho speso oggi?")

**Personalizza:** Modifica `scripts/generate_synthetic_data.py` per:
- Aggiungere nuovi template
- Cambiare variabili (skills, eventi, ecc.)
- Aumentare/ridurre numero esempi

---

### Step 2: Aggiungi Esempi Reali (Opzionale)
```bash
python scripts/extract_user_inputs.py
```

**Fonti:**
1. Database (`chat_logs` table - se esiste)
2. File log (`logs/app.log`)
3. Esempi manuali (gold standard)

**Se non hai logs ancora:**
1. Implementa logging in `app/routes/api.py`:
```python
import logging
logger = logging.getLogger('chat')

@app.route('/api/chat', methods=['POST'])
def chat():
    text = request.json.get('messaggio', '')
    logger.info(f'User input: "{text}"')
    # ...
```

2. Aggiungi esempi manuali in `scripts/extract_user_inputs.py`:
```python
def manual_examples(self):
    return [
        {"text": "domani riunione 10-12", "intent": "impegno"},
        # ... aggiungi 50-100 esempi gold
    ]
```

---

### Step 3: Train Model
```bash
python train_nlp_model.py data/dataset_combined.json
```

**Parametri:**
- `--n_iter 30` (default) - Numero iterazioni
- `--output models/nlp_v1` (default) - Dove salvare

**Durante training vedrai:**
```
🧠 Training model...
   Dataset: data/dataset_combined.json
   Iterations: 30
   Train: 640, Val: 160
   Labels: obiettivo, impegno, spesa, diario, domanda_temporale, domanda_budget

   Iter 5/30: loss=2.3456
   Iter 10/30: loss=1.2345
   ...
   Iter 30/30: loss=0.5432

📊 Evaluating...
   Accuracy: 87.50%

💾 Model saved to models/nlp_v1

✅ Training completato con successo!
```

**Target accuracy:** 85%+

**Se accuracy < 85%:**
1. Aggiungi più esempi (target 1500+)
2. Bilancia dataset (ogni intent ~stesso numero esempi)
3. Aumenta iterazioni (`--n_iter 50`)
4. Rivedi esempi di bassa qualità

---

### Step 4: Test Model
```bash
# Test rapido
python -c "
import spacy
nlp = spacy.load('models/nlp_v1')
doc = nlp('domani riunione 10-12')
print(doc.cats)
"
```

**Output atteso:**
```python
{
    'obiettivo': 0.05,
    'impegno': 0.92,    # ← Confidence alta!
    'spesa': 0.01,
    'diario': 0.01,
    'domanda_temporale': 0.005,
    'domanda_budget': 0.005
}
```

**Test interattivo:**
```python
import spacy

nlp = spacy.load('models/nlp_v1')

while True:
    text = input('\n📝 Input: ')
    if text.lower() in ['quit', 'exit']:
        break
    
    doc = nlp(text)
    
    # Trova intent con confidence massima
    intent = max(doc.cats, key=doc.cats.get)
    confidence = doc.cats[intent]
    
    print(f'🎯 Intent: {intent}')
    print(f'📊 Confidence: {confidence:.2%}')
    
    if confidence < 0.5:
        print('⚠️  Bassa confidence! Aggiungi esempi simili al dataset.')
```

---

### Step 5: Integra in App
```python
# app/ai/nlp_inference.py

import spacy

class AdvancedNLPManager:
    def __init__(self, model_path="models/nlp_v1"):
        self.nlp = spacy.load(model_path)
        self.confidence_threshold = 0.5
    
    def analyze(self, text: str):
        doc = self.nlp(text.lower())
        
        intent = max(doc.cats, key=doc.cats.get)
        confidence = doc.cats[intent]
        
        return {
            "intent": intent,
            "confidence": confidence,
            "use_fallback": confidence < self.confidence_threshold
        }

# app/routes/api.py
from app.ai.nlp_inference import AdvancedNLPManager

nlp_manager = AdvancedNLPManager()

@app.route('/api/chat', methods=['POST'])
def chat():
    text = request.json.get('messaggio', '')
    
    # Analisi ML
    result = nlp_manager.analyze(text)
    
    if result['use_fallback']:
        # Usa vecchio NLP o Ollama
        return handle_with_fallback(text)
    
    # Route basato su intent
    if result['intent'] == 'impegno':
        return handle_commitment(text)
    elif result['intent'] == 'spesa':
        return handle_expense(text)
    # ...
```

---

## 📊 MONITORAGGIO

### Telemetry (Recommended)
Salva ogni predizione per miglioramento continuo:

```python
# app/ai/telemetry.py

import json
from datetime import datetime

class NLPTelemetry:
    def log_prediction(self, user_input, prediction, user_feedback=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "intent": prediction['intent'],
            "confidence": prediction['confidence'],
            "feedback": user_feedback  # 'correct' / 'wrong'
        }
        
        with open('logs/nlp_predictions.jsonl', 'a') as f:
            f.write(json.dumps(entry) + '\n')

# Uso in api.py
telemetry = NLPTelemetry()

@app.route('/api/chat', methods=['POST'])
def chat():
    result = nlp_manager.analyze(text)
    telemetry.log_prediction(text, result)
    # ...

@app.route('/api/feedback', methods=['POST'])
def receive_feedback():
    """Utente dice se risposta era corretta"""
    telemetry.log_prediction(
        request.json['input'],
        request.json['prediction'],
        user_feedback=request.json['correct']  # True/False
    )
```

### Dashboard Metriche
```bash
# Analizza logs per trovare problemi
python scripts/analyze_predictions.py logs/nlp_predictions.jsonl
```

**Output:**
```
📊 NLP Performance (Last 7 days)
=====================================
Total predictions: 1,234
Average confidence: 0.78

Intent Distribution:
  impegno: 45% (accuracy: 92%)
  obiettivo: 25% (accuracy: 88%)
  spesa: 20% (accuracy: 85%)
  diario: 10% (accuracy: 90%)

Low Confidence Samples (confidence < 0.5):
  1. "giovedì alle 10 riunione team"
  2. "voglio fare sport regolarmente"
  ...

❌ User Reported Wrong (need review):
  - Input: "domani vado palestra"
    Predicted: obiettivo (0.65)
    Should be: impegno
```

---

## 🔄 RE-TRAINING (Weekly)

### Automatic Re-training
```bash
# Cron job ogni domenica
0 2 * * 0 /path/to/retrain.sh
```

```bash
# scripts/retrain.sh
#!/bin/bash

# 1. Extract new real inputs from last week
python scripts/extract_user_inputs.py --last-7-days

# 2. Merge with existing dataset
jq -s 'add' data/dataset_combined.json data/dataset_new_week.json > data/dataset_updated.json

# 3. Re-train
python train_nlp_model.py data/dataset_updated.json --output models/nlp_v2

# 4. Evaluate on test set
python scripts/evaluate_model.py models/nlp_v2 data/test_set.json

# 5. If accuracy > current model: deploy
# (Compare with models/nlp_v1 accuracy)
```

---

## 🆘 TROUBLESHOOTING

### Problema: Accuracy < 70%
**Soluzioni:**
1. Aggiungi più esempi (target 1500+)
2. Bilancia dataset (ogni intent uguale numero)
3. Rivedi qualità esempi (rimuovi duplicati)
4. Aumenta iterazioni (`--n_iter 50`)

### Problema: Model troppo grande (>100MB)
**Soluzioni:**
1. Usa `it_core_news_sm` invece di `lg`
2. Rimuovi pipeline non usate:
```python
nlp = spacy.load("models/nlp_v1", disable=["parser", "ner"])
```

### Problema: Inference lenta (>500ms)
**Soluzioni:**
1. Usa batch processing
2. Cache su Redis per query ripetute
3. Upgrade Render a Pro (più CPU)

### Problema: Out of memory su Render Free
**Soluzioni:**
1. Riduci dimensione modello
2. Usa modello esterno (Groq API - gratis!)
3. Upgrade Render Pro

---

## 📈 ROADMAP

### Settimana 1-2: Base NLP ✅
- [x] Setup training pipeline
- [x] Generate synthetic dataset
- [x] Train basic intent classifier
- [x] Integrate in app

### Settimana 3-4: Entity Extraction
- [ ] Annotate entities in dataset
- [ ] Train NER model
- [ ] Extract date/time/amounts accurately

### Settimana 5-6: Conversational AI
- [ ] Context management
- [ ] Multi-turn dialogues
- [ ] Reference resolution

### Settimana 7-8: Advanced Features
- [ ] Sentiment analysis
- [ ] Recommendation engine
- [ ] Ollama/Groq integration

---

## 📚 RISORSE

### Tutorials:
- [spaCy Training Guide](https://spacy.io/usage/training)
- [Building NLP Apps (Free)](https://www.nltk.org/book/)

### Datasets Italiani:
- [EVALITA](http://www.evalita.it/)
- [UD Italian Treebank](https://universaldependencies.org/treebanks/it/)

### Communities:
- [r/LanguageTechnology](https://reddit.com/r/LanguageTechnology)
- [spaCy Discussions](https://github.com/explosion/spaCy/discussions)

---

## ✅ CHECKLIST

### Setup Iniziale:
- [ ] Run `./scripts/train_quick_start.sh`
- [ ] Verifica dataset generato (800+ esempi)
- [ ] Train primo modello
- [ ] Test model con esempi manualmente
- [ ] Accuracy > 85%?

### Integrazione:
- [ ] Crea `app/ai/nlp_inference.py`
- [ ] Integra in `/api/chat`
- [ ] Aggiungi fallback (confidence < 0.5)
- [ ] Test in produzione con 10% utenti (A/B)

### Monitoring:
- [ ] Implementa telemetry
- [ ] Log ogni predizione
- [ ] User feedback system (👍 👎)
- [ ] Weekly re-training cron job

### Optimization:
- [ ] Profile inference time (<200ms)
- [ ] Optimize model size (<50MB)
- [ ] Cache frequent queries
- [ ] Monitor accuracy in produzione

---

## 🎉 SUCCESS METRICS

| Metrica | Target | Come Misurare |
|---------|--------|---------------|
| **Accuracy** | 85%+ | Validation set |
| **Confidence** | 70%+ avg | Telemetry logs |
| **Fallback Rate** | <20% | % queries con confidence < 0.5 |
| **Inference Time** | <200ms | APM monitoring |
| **User Satisfaction** | 80%+ | Thumbs up/down |

---

**Made with 🤖 + ❤️ by Assistente Intelligente Team**

**Prossimo Step:** Run `./scripts/train_quick_start.sh` e inizia! 🚀

