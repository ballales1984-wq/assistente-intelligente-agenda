"""Debug AI fallback"""
from app import create_app, db
from app.models import UserProfile
from app.core.input_manager import InputManager
from app.ai.ollama_assistant import OllamaAssistant, OllamaManager

app = create_app()

with app.app_context():
    print("\n" + "="*60)
    print("🔍 DEBUG AI FALLBACK")
    print("="*60)
    
    # Test 1: Ollama running?
    print("\n1️⃣  Ollama Status:")
    running = OllamaManager.check_ollama_running()
    print(f"   Running: {running}")
    
    if running:
        models = OllamaManager.list_available_models()
        print(f"   Models: {models}")
    
    # Test 2: Input Manager
    print("\n2️⃣  Input Manager:")
    messaggio = "Vado in palestra"
    risultato = InputManager.analizza_input(messaggio)
    print(f"   Input: '{messaggio}'")
    print(f"   Tipo: {risultato['tipo']}")
    print(f"   Should trigger AI: {risultato['tipo'] in ['sconosciuto', 'domanda', 'aiuto']}")
    
    # Test 3: AI Assistant Direct
    if running:
        print("\n3️⃣  AI Assistant Direct Test:")
        try:
            profilo = UserProfile.query.first()
            
            context = {
                'obiettivi': [o.to_dict() for o in profilo.obiettivi.filter_by(attivo=True).limit(3).all()]
            }
            
            assistant = OllamaAssistant(model='gemma3:1b')
            print(f"   Model: gemma3:1b")
            print(f"   Chiamata AI...")
            
            risposta_ai = assistant.chat(messaggio, context)
            print(f"   ✅ AI Response: {risposta_ai[:200]}...")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("✅ DEBUG COMPLETATO!")
    print("="*60 + "\n")

