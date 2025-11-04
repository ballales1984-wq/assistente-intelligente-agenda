#!/bin/bash
# 🚀 COMANDI QUICK START - ADDESTRAMENTO APP
# Creato: 5 Novembre 2025
# Uso: bash 🔧_COMANDI_QUICK_START.sh [fase]

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ========================================
# UTILITY FUNCTIONS
# ========================================

print_header() {
    echo -e "${BLUE}╔═══════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║ $1${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════╝${NC}"
}

print_step() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# ========================================
# FASE 1: NLP TRAINING
# ========================================

fase1_setup() {
    print_header "FASE 1: NLP TRAINING SETUP"
    
    # 1. Crea directory structure
    print_step "Creando directory NLP..."
    mkdir -p data/nlp_training/{obiettivi,impegni,spese,diario}
    mkdir -p models/nlp_italian_v2
    mkdir -p scripts/nlp
    
    # 2. Install dependencies
    print_step "Installando dipendenze spaCy..."
    pip install spacy spacy-transformers
    python -m spacy download it_core_news_sm
    
    # 3. Crea dataset generator
    print_step "Creando dataset generator..."
    cat > scripts/nlp/generate_dataset.py << 'EOF'
import json
import random
from datetime import datetime, timedelta

class DatasetGenerator:
    """Genera dataset di training per NLP"""
    
    def __init__(self):
        self.obiettivi = []
        self.impegni = []
        self.spese = []
        self.diario = []
    
    def generate_obiettivi(self, count=1000):
        """Genera varianti di obiettivi"""
        templates = [
            "Voglio studiare {materia} {ore} ore a settimana",
            "Studio {materia} {ore}h/settimana",
            "Obiettivo: imparare {materia} ({ore} ore settimanali)",
            "Dedico {ore} ore a {materia} ogni settimana",
            "{materia} {ore} ore settimanali come obiettivo",
            "Vorrei dedicare {ore}h settimanali a {materia}",
            "Piano: {ore} ore/settimana per {materia}",
        ]
        
        materie = [
            "Python", "Javascript", "Inglese", "Francese", "Yoga",
            "Palestra", "Lettura", "Scrittura", "Disegno", "Chitarra"
        ]
        
        ore_options = [1, 2, 3, 4, 5, 6, 8, 10]
        
        for _ in range(count):
            template = random.choice(templates)
            materia = random.choice(materie)
            ore = random.choice(ore_options)
            
            text = template.format(materia=materia, ore=ore)
            
            self.obiettivi.append({
                "text": text,
                "entities": [
                    (text.lower().find(materia.lower()), 
                     text.lower().find(materia.lower()) + len(materia), 
                     "MATERIA"),
                    (text.find(str(ore)), 
                     text.find(str(ore)) + len(str(ore)), 
                     "ORE")
                ],
                "label": "obiettivo"
            })
    
    def generate_impegni(self, count=1000):
        """Genera varianti di impegni"""
        templates = [
            "{giorno} {evento} ore {ora}",
            "{evento} {giorno} alle {ora}",
            "{ora} {giorno} {evento}",
            "{giorno} {ora}:00 {evento}",
            "{evento} il {giorno} ore {ora}",
        ]
        
        giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", 
                  "Venerdì", "Sabato", "Domenica", "Domani"]
        eventi = ["riunione", "meeting", "appuntamento", "dottore", 
                  "dentista", "pranzo", "cena"]
        ore = range(8, 21)
        
        for _ in range(count):
            template = random.choice(templates)
            giorno = random.choice(giorni)
            evento = random.choice(eventi)
            ora = random.choice(ore)
            
            text = template.format(giorno=giorno, evento=evento, ora=ora)
            self.impegni.append({
                "text": text,
                "label": "impegno"
            })
    
    def generate_spese(self, count=1000):
        """Genera varianti di spese"""
        templates = [
            "{importo} euro {descrizione}",
            "{descrizione} {importo}€",
            "Ho speso {importo} a {descrizione}",
            "Speso {importo} per {descrizione}",
            "Comprato {descrizione} {importo} euro",
            "{importo},00 {descrizione}",
        ]
        
        descrizioni = {
            "cibo": ["cena", "pranzo", "spesa", "pizza", "ristorante"],
            "trasporti": ["benzina", "treno", "bus", "taxi", "autostrada"],
            "svago": ["cinema", "libro", "concerto", "museo", "teatro"],
            "altro": ["regalo", "farmacia", "abbonamento", "utenze"]
        }
        
        for _ in range(count):
            template = random.choice(templates)
            categoria = random.choice(list(descrizioni.keys()))
            descrizione = random.choice(descrizioni[categoria])
            importo = random.randint(5, 200)
            
            text = template.format(importo=importo, descrizione=descrizione)
            self.spese.append({
                "text": text,
                "label": "spesa",
                "categoria": categoria,
                "importo": importo
            })
    
    def save(self, output_dir="data/nlp_training"):
        """Salva datasets in JSON"""
        import os
        
        with open(f"{output_dir}/obiettivi_1000.json", "w") as f:
            json.dump(self.obiettivi, f, indent=2, ensure_ascii=False)
        
        with open(f"{output_dir}/impegni_1000.json", "w") as f:
            json.dump(self.impegni, f, indent=2, ensure_ascii=False)
        
        with open(f"{output_dir}/spese_1000.json", "w") as f:
            json.dump(self.spese, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Dataset salvati in {output_dir}/")
        print(f"   - Obiettivi: {len(self.obiettivi)}")
        print(f"   - Impegni: {len(self.impegni)}")
        print(f"   - Spese: {len(self.spese)}")

if __name__ == "__main__":
    gen = DatasetGenerator()
    
    print("🔄 Generando dataset...")
    gen.generate_obiettivi(1000)
    gen.generate_impegni(1000)
    gen.generate_spese(1000)
    
    print("💾 Salvando...")
    gen.save()
    
    print("🎉 COMPLETATO!")
EOF
    
    # 4. Genera dataset
    print_step "Generando dataset di training..."
    python scripts/nlp/generate_dataset.py
    
    print_step "✅ FASE 1 SETUP COMPLETATO!"
    echo ""
    echo "Next steps:"
    echo "  1. Controlla dataset in data/nlp_training/"
    echo "  2. Esegui: bash 🔧_COMANDI_QUICK_START.sh fase1_train"
}

fase1_train() {
    print_header "FASE 1: NLP TRAINING"
    
    # 1. Crea training script
    cat > scripts/nlp/train_model.py << 'EOF'
import spacy
from spacy.training import Example
import random
import json

def load_training_data(file_path):
    """Carica dataset JSON"""
    with open(file_path, 'r') as f:
        return json.load(f)

def train_model(iterations=30):
    """Train spaCy model"""
    
    # Carica dati
    print("📊 Caricando dataset...")
    obiettivi = load_training_data("data/nlp_training/obiettivi_1000.json")
    impegni = load_training_data("data/nlp_training/impegni_1000.json")
    spese = load_training_data("data/nlp_training/spese_1000.json")
    
    all_data = obiettivi + impegni + spese
    print(f"   Total samples: {len(all_data)}")
    
    # Create blank Italian model
    nlp = spacy.blank("it")
    
    # Add text classifier
    textcat = nlp.add_pipe("textcat")
    textcat.add_label("obiettivo")
    textcat.add_label("impegno")
    textcat.add_label("spesa")
    textcat.add_label("diario")
    
    # Convert to spaCy format
    print("🔄 Convertendo formato...")
    train_examples = []
    for item in all_data:
        doc = nlp.make_doc(item['text'])
        cats = {
            'obiettivo': 1.0 if item['label'] == 'obiettivo' else 0.0,
            'impegno': 1.0 if item['label'] == 'impegno' else 0.0,
            'spesa': 1.0 if item['label'] == 'spesa' else 0.0,
            'diario': 0.0
        }
        train_examples.append(Example.from_dict(doc, {"cats": cats}))
    
    # Train
    print(f"🎓 Training per {iterations} iterazioni...")
    optimizer = nlp.initialize()
    
    for i in range(iterations):
        random.shuffle(train_examples)
        losses = {}
        
        batches = spacy.util.minibatch(train_examples, size=8)
        for batch in batches:
            nlp.update(batch, sgd=optimizer, losses=losses)
        
        if (i + 1) % 5 == 0:
            print(f"   Iteration {i+1}/{iterations}, Loss: {losses.get('textcat', 0):.4f}")
    
    # Salva modello
    print("💾 Salvando modello...")
    nlp.to_disk("models/nlp_italian_v2")
    
    print("✅ TRAINING COMPLETATO!")
    print("   Modello salvato: models/nlp_italian_v2")

if __name__ == "__main__":
    train_model(iterations=30)
EOF
    
    # 2. Esegui training
    print_step "Iniziando training (potrebbe richiedere 10-15 min)..."
    python scripts/nlp/train_model.py
    
    print_step "✅ TRAINING COMPLETATO!"
}

fase1_test() {
    print_header "FASE 1: NLP TESTING"
    
    # Crea test script
    cat > scripts/nlp/test_model.py << 'EOF'
import spacy

def test_model():
    """Test trained model"""
    
    print("📦 Caricando modello...")
    nlp = spacy.load("models/nlp_italian_v2")
    
    test_cases = [
        ("Voglio studiare Python 3 ore a settimana", "obiettivo"),
        ("Domani riunione 10-12", "impegno"),
        ("Speso 35 euro cena", "spesa"),
        ("Giovedì meeting ore 15", "impegno"),
        ("Studio Javascript 5h/settimana", "obiettivo"),
        ("50€ benzina", "spesa"),
    ]
    
    print("\n🧪 Testing su casi di esempio:\n")
    
    correct = 0
    for text, expected in test_cases:
        doc = nlp(text)
        predicted = max(doc.cats, key=doc.cats.get)
        
        status = "✅" if predicted == expected else "❌"
        print(f"{status} '{text}'")
        print(f"   Expected: {expected}, Got: {predicted}")
        print(f"   Confidence: {doc.cats[predicted]:.2%}\n")
        
        if predicted == expected:
            correct += 1
    
    accuracy = (correct / len(test_cases)) * 100
    print(f"\n📊 Accuracy: {accuracy:.1f}% ({correct}/{len(test_cases)})")

if __name__ == "__main__":
    test_model()
EOF
    
    print_step "Eseguendo test..."
    python scripts/nlp/test_model.py
}

# ========================================
# FASE 2: SMART LINKS
# ========================================

fase2_youtube() {
    print_header "FASE 2: YOUTUBE INTEGRATION"
    
    print_step "Installando dipendenze..."
    pip install google-api-python-client
    
    print_step "Creando YouTube service..."
    # Il file completo è già nel piano principale
    
    print_warning "⚠️  IMPORTANTE: Devi ottenere YouTube API Key da:"
    print_warning "   https://console.cloud.google.com/apis/credentials"
    echo ""
    echo "Aggiungi a .env:"
    echo "  YOUTUBE_API_KEY=your_key_here"
}

fase2_amazon() {
    print_header "FASE 2: AMAZON INTEGRATION"
    
    print_step "Installando dipendenze..."
    pip install beautifulsoup4 lxml requests
    
    print_warning "⚠️  Amazon non ha API gratuita!"
    print_warning "   Opzioni:"
    print_warning "   1. Web scraping (può essere bloccato)"
    print_warning "   2. Amazon Product Advertising API (richiede account affiliato)"
    print_warning "   3. RapidAPI Amazon scraper (~$10/mese)"
}

# ========================================
# FASE 3: ANALYTICS
# ========================================

fase3_analytics() {
    print_header "FASE 3: ANALYTICS SETUP"
    
    print_step "Creando analytics endpoints..."
    # Copia codice da piano principale in app/routes/analytics.py
    
    print_step "Frontend Chart.js setup..."
    echo "Aggiungi a templates/index.html:"
    echo '  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
}

# ========================================
# FASE 4: TESTING
# ========================================

fase4_tests() {
    print_header "FASE 4: TEST SETUP"
    
    print_step "Installando pytest plugins..."
    pip install pytest pytest-cov pytest-mock pytest-asyncio
    
    print_step "Creando test structure..."
    mkdir -p tests/{unit,integration,e2e}
    
    print_step "Eseguendo test suite..."
    pytest --cov=app --cov-report=html --cov-report=term
    
    echo ""
    echo "📊 Coverage report generato in htmlcov/index.html"
}

# ========================================
# FASE 5: PERFORMANCE
# ========================================

fase5_performance() {
    print_header "FASE 5: PERFORMANCE OPTIMIZATION"
    
    print_step "Creando migration per indici..."
    # Crea file migration con indici
    
    print_step "Applicando indici al database..."
    flask db upgrade
    
    print_step "Testing performance..."
    python scripts/benchmark.py
}

# ========================================
# UTILITIES
# ========================================

run_tests() {
    print_header "ESECUZIONE TEST COMPLETA"
    
    print_step "Linter (black + isort)..."
    black app/ tests/
    isort app/ tests/
    
    print_step "Pytest..."
    pytest -v --cov=app
    
    print_step "Type checking..."
    mypy app/
    
    print_step "Security audit..."
    bandit -r app/
}

deploy_staging() {
    print_header "DEPLOY TO STAGING"
    
    print_step "Running tests..."
    pytest
    
    print_step "Building..."
    docker build -t agenda-app:staging .
    
    print_step "Deploying..."
    git push staging main
    
    print_step "✅ DEPLOYED TO STAGING"
    echo "URL: https://staging.agenda-app.com"
}

# ========================================
# MAIN
# ========================================

show_menu() {
    echo ""
    echo "╔═══════════════════════════════════════════════╗"
    echo "║     🚀 AGENDA APP TRAINING - QUICK START      ║"
    echo "╚═══════════════════════════════════════════════╝"
    echo ""
    echo "FASE 1: NLP TRAINING"
    echo "  1) fase1_setup  - Setup iniziale + genera dataset"
    echo "  2) fase1_train  - Train modello NLP"
    echo "  3) fase1_test   - Test accuracy"
    echo ""
    echo "FASE 2: SMART LINKS"
    echo "  4) fase2_youtube - Setup YouTube API"
    echo "  5) fase2_amazon  - Setup Amazon search"
    echo ""
    echo "FASE 3: ANALYTICS"
    echo "  6) fase3_analytics - Setup grafici"
    echo ""
    echo "FASE 4: TESTING"
    echo "  7) fase4_tests  - Test coverage boost"
    echo ""
    echo "FASE 5: PERFORMANCE"
    echo "  8) fase5_performance - Ottimizzazioni"
    echo ""
    echo "UTILITIES:"
    echo "  9) run_tests    - Run all tests"
    echo " 10) deploy_staging - Deploy to staging"
    echo ""
    echo "  0) exit"
    echo ""
}

main() {
    if [ $# -eq 0 ]; then
        # Interactive mode
        while true; do
            show_menu
            read -p "Scegli opzione: " choice
            
            case $choice in
                1) fase1_setup ;;
                2) fase1_train ;;
                3) fase1_test ;;
                4) fase2_youtube ;;
                5) fase2_amazon ;;
                6) fase3_analytics ;;
                7) fase4_tests ;;
                8) fase5_performance ;;
                9) run_tests ;;
                10) deploy_staging ;;
                0) echo "👋 Bye!"; exit 0 ;;
                *) print_error "Opzione non valida!" ;;
            esac
            
            echo ""
            read -p "Premi ENTER per continuare..."
        done
    else
        # Direct command mode
        case $1 in
            fase1_setup) fase1_setup ;;
            fase1_train) fase1_train ;;
            fase1_test) fase1_test ;;
            fase2_youtube) fase2_youtube ;;
            fase2_amazon) fase2_amazon ;;
            fase3_analytics) fase3_analytics ;;
            fase4_tests) fase4_tests ;;
            fase5_performance) fase5_performance ;;
            run_tests) run_tests ;;
            deploy_staging) deploy_staging ;;
            *) 
                print_error "Comando non riconosciuto: $1"
                echo "Uso: bash $0 [comando]"
                echo "Esegui senza argomenti per menu interattivo"
                exit 1
                ;;
        esac
    fi
}

# Run
main "$@"

