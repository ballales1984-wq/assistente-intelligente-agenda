"""Test Ollama integration"""
from app.ai.ollama_assistant import OllamaAssistant, OllamaManager

print("\n" + "="*60)
print("🤖 TEST OLLAMA INTEGRATION")
print("="*60)

# Check Ollama
print("\n1️⃣  Ollama status:")
if OllamaManager.check_ollama_running():
    print("   ✅ Ollama is running!")
else:
    print("   ❌ Ollama not running!")
    exit(1)

# List models
print("\n2️⃣  Available models:")
models = OllamaManager.list_available_models()
for model in models:
    print(f"   ✅ {model}")

# Test chat (usa gemma, il più piccolo)
print("\n3️⃣  Test conversation:")
print("   Model: gemma3:1b (fastest)")

assistant = OllamaAssistant(model='gemma3:1b')

test_messages = [
    "Ciao! Come ti chiami?",
    "Aiutami a pianificare la mia giornata",
    "Ho 3 obiettivi: Python, Palestra, Libri. Come distribuirli?"
]

for msg in test_messages:
    print(f"\n   👤 User: {msg}")
    try:
        risposta = assistant.chat(msg, context={
            'obiettivi': [
                {'nome': 'Python', 'durata_settimanale': 5},
                {'nome': 'Palestra', 'durata_settimanale': 3}
            ]
        })
        print(f"   🤖 AI: {risposta[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("✅ TEST COMPLETATO!")
print("="*60 + "\n")

