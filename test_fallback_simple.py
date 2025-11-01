"""Test semplice fallback"""
import requests

url = "http://localhost:5000/api/chat"

# Test input vago
messaggio = "Vado in palestra"

print(f"\n🧪 Test: '{messaggio}'\n")

response = requests.post(
    url,
    json={'messaggio': messaggio, 'enable_ai_fallback': True},
    timeout=30
)

if response.status_code == 200:
    data = response.json()
    
    print(f"Tipo: {data['tipo_riconosciuto']}")
    print(f"AI Used: {data.get('ai_used', False)}")
    
    if data.get('ai_used'):
        print(f"🤖 AI Model: {data.get('ai_model')}")
        print(f"\n✅ AUTO-FALLBACK FUNZIONA!\n")
    else:
        print(f"\n⚠️  Regex handled (AI non usata)\n")
    
    print(f"Risposta:\n{data['risposta'][:300]}...\n")
else:
    print(f"❌ Error: {response.status_code}\n{response.text}\n")

