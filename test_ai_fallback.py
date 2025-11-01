"""Test Auto-Fallback Regex → Ollama AI"""
import requests
import json

print("\n" + "="*70)
print("🧪 TEST AUTO-FALLBACK: Regex → Ollama AI")
print("="*70)

base_url = "http://localhost:5000"

# Test cases: input che regex NON capisce
test_cases = [
    {
        'input': 'Vado in palestra',
        'expected': 'AI dovrebbe chiedere quando/orario'
    },
    {
        'input': 'Aiutami a pianificare la settimana',
        'expected': 'AI dovrebbe fornire piano'
    },
    {
        'input': 'Come posso essere più produttivo?',
        'expected': 'AI dovrebbe dare suggerimenti'
    },
    {
        'input': 'Comprato scarpe',
        'expected': 'AI dovrebbe chiedere prezzo'
    },
    {
        'input': 'Cosa devo fare?',
        'expected': 'AI dovrebbe rispondere con piano giornata'
    }
]

print("\n📊 Testing auto-fallback on vague inputs...\n")

for idx, test in enumerate(test_cases, 1):
    print(f"{idx}. Input: '{test['input']}'")
    print(f"   Expected: {test['expected']}")
    
    try:
        response = requests.post(
            f"{base_url}/api/chat",
            json={'messaggio': test['input'], 'enable_ai_fallback': True},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('ai_used'):
                print(f"   ✅ AI USED! Model: {data.get('ai_model', 'N/A')}")
                print(f"   🤖 Response: {data['risposta'][:150]}...")
            else:
                print(f"   ⚠️  Regex handled (tipo: {data.get('tipo_riconosciuto')})")
                print(f"   📝 Response: {data['risposta'][:100]}...")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    
    print()

print("="*70)
print("✅ TEST FALLBACK COMPLETATO!")
print("="*70)
print("\n💡 Se vedi '✅ AI USED!' = Fallback funziona!")
print("💡 Se vedi '⚠️ Regex handled' = Input riconosciuto da regex\n")

