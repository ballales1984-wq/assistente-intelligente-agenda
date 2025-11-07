#!/usr/bin/env python
"""Test di tutte le funzioni dell'app live"""
import requests
import json

BASE_URL = "https://assistente-intelligente-agenda.onrender.com"

def test_function(name, url, method="GET", json_data=None):
    """Test singola funzione"""
    try:
        if method == "GET":
            r = requests.get(url, timeout=15)
        else:
            r = requests.post(url, json=json_data, timeout=15)
        
        status = "✅" if r.status_code == 200 else "❌"
        print(f"{status} {name}: Status {r.status_code}")
        
        if r.status_code != 200:
            print(f"   Response: {r.text[:200]}")
        
        return r.status_code == 200
    except Exception as e:
        print(f"❌ {name}: Exception - {e}")
        return False

print("\n" + "="*60)
print("🧪 TEST COMPLETO APP LIVE")
print("="*60)

print("\n📄 HOMEPAGE & PAGINE")
print("-"*60)
test_function("Homepage IT", f"{BASE_URL}/")
test_function("Homepage EN", f"{BASE_URL}/en")
test_function("About", f"{BASE_URL}/about")

print("\n🔌 API BASE")
print("-"*60)
test_function("Profilo", f"{BASE_URL}/api/profilo")
test_function("Statistiche", f"{BASE_URL}/api/statistiche")
test_function("Obiettivi", f"{BASE_URL}/api/obiettivi")
test_function("Presente/Oggi", f"{BASE_URL}/api/presente/oggi")

print("\n💬 CHAT NLP")
print("-"*60)
tests_chat = [
    ("Obiettivo", {"messaggio": "Voglio studiare Python 3 ore a settimana", "lang": "it"}),
    ("Impegno", {"messaggio": "Domenica vado al mare dalle 16 alle 20", "lang": "it"}),
    ("Spesa", {"messaggio": "50 euro benzina", "lang": "it"}),
    ("Diario", {"messaggio": "Oggi mi sento motivato", "lang": "it"}),
]

chat_passed = 0
for name, data in tests_chat:
    if test_function(f"Chat - {name}", f"{BASE_URL}/api/chat", "POST", data):
        chat_passed += 1

print("\n" + "="*60)
print(f"📊 CHAT NLP: {chat_passed}/{len(tests_chat)} funzionanti")
print("="*60)

if chat_passed == 0:
    print("\n❌ CHAT COMPLETAMENTE ROTTA!")
elif chat_passed == len(tests_chat):
    print("\n🎉 CHAT 100% FUNZIONANTE!")
else:
    print(f"\n⚠️ CHAT PARZIALMENTE FUNZIONANTE ({chat_passed}/{len(tests_chat)})")

