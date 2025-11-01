"""Setup Ollama per Wallmind"""
import ollama
import sys

print("\n" + "="*60)
print("🤖 SETUP OLLAMA PER WALLMIND")
print("="*60)

# Check se Ollama è running
print("\n1️⃣  Verifico se Ollama è in esecuzione...")
try:
    models = ollama.list()
    print("✅ Ollama è attivo!")
except Exception as e:
    print(f"❌ Ollama non risponde: {e}")
    print("\n💡 Avvia Ollama con: ollama serve")
    sys.exit(1)

# Lista modelli disponibili
print("\n2️⃣  Modelli disponibili localmente:")
available_models = []
if hasattr(models, 'models'):
    for m in models.models:
        model_name = m.model if hasattr(m, 'model') else str(m)
        size_gb = m.size / (1024**3) if hasattr(m, 'size') else 0
        available_models.append(model_name)
        print(f"   ✅ {model_name} ({size_gb:.1f} GB)")
else:
    print("   ⚠️  Nessun modello trovato")

# Raccomandazioni
print("\n3️⃣  Modelli consigliati per Wallmind:")
recommended = {
    'mistral': {
        'size': '4.1GB',
        'speed': 'Veloce',
        'quality': 'Ottima',
        'best_for': 'Generale, ottimo balance'
    },
    'llama2': {
        'size': '3.8GB',
        'speed': 'Media',
        'quality': 'Ottima',
        'best_for': 'Conversazioni naturali'
    },
    'phi': {
        'size': '1.6GB',
        'speed': 'Molto veloce',
        'quality': 'Buona',
        'best_for': 'Risposte rapide, sistemi limitati'
    },
    'gemma:2b': {
        'size': '1.4GB',
        'speed': 'Velocissimo',
        'quality': 'Buona',
        'best_for': 'PC meno potenti'
    }
}

for model_name, info in recommended.items():
    has_it = any(model_name in m for m in available_models)
    status = "✅ INSTALLATO" if has_it else "📥 Da scaricare"
    print(f"\n   {model_name}:")
    print(f"      Status: {status}")
    print(f"      Size: {info['size']}")
    print(f"      Speed: {info['speed']}")
    print(f"      Quality: {info['quality']}")
    print(f"      Best for: {info['best_for']}")

# Download consigliato
print("\n4️⃣  Azione consigliata:")

if not available_models:
    print("   📥 Nessun modello installato!")
    print("\n   Raccomando: mistral (best balance)")
    print("   Comando: ollama pull mistral")
    
    risposta = input("\n   Vuoi scaricarlo ora? (s/n): ")
    if risposta.lower() == 's':
        print("\n   📥 Download in corso...")
        try:
            ollama.pull('mistral')
            print("   ✅ Mistral scaricato con successo!")
        except Exception as e:
            print(f"   ❌ Errore: {e}")
else:
    print(f"   ✅ Hai già {len(available_models)} modello/i!")
    print(f"   🎯 Userò: {available_models[0]}")

# Test veloce
print("\n5️⃣  Test rapido:")
test_model = available_models[0] if available_models else None

if test_model:
    print(f"   Testing {test_model}...")
    try:
        response = ollama.generate(
            model=test_model,
            prompt="Rispondi in italiano in 10 parole: Cosa fai come assistente personale?"
        )
        print(f"   ✅ Risposta: {response['response'][:100]}...")
    except Exception as e:
        print(f"   ❌ Errore test: {e}")

print("\n" + "="*60)
print("✅ SETUP COMPLETATO!")
print("="*60)
print("\n💡 Per usare LLM nella chat:")
print("   1. Riavvia l'app: python run.py")
print("   2. Scrivi messaggi complessi")
print("   3. L'AI locale risponderà!")
print("\n🚀 Wallmind ora ha un cervello locale! 🧠\n")

