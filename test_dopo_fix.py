#!/usr/bin/env python
"""Test dopo fix urgente"""
import requests
import time
import sys

BASE_URL = "https://assistente-intelligente-agenda.onrender.com"

def wait_for_deploy():
    """Aspetta che deploy finisca"""
    print("\n⏰ Aspetto che Render finisca il deploy (60 secondi)...")
    for i in range(60, 0, -10):
        print(f"   {i} secondi rimanenti...")
        time.sleep(10)
    print("✅ Deploy dovrebbe essere finito!\n")

def test_chat(messaggio, expected_tipo):
    """Test singolo messaggio chat"""
    try:
        r = requests.post(
            f"{BASE_URL}/api/chat",
            json={"messaggio": messaggio, "lang": "it"},
            timeout=15
        )
        
        if r.status_code != 200:
            print(f"❌ {messaggio}")
            print(f"   Status: {r.status_code}")
            print(f"   Response: {r.text[:200]}")
            return False
        
        data = r.json()
        tipo = data.get('tipo_riconosciuto')
        
        if tipo == expected_tipo:
            print(f"✅ {messaggio}")
            print(f"   Tipo: {tipo}")
            return True
        else:
            print(f"⚠️ {messaggio}")
            print(f"   Expected: {expected_tipo}, Got: {tipo}")
            return False
            
    except Exception as e:
        print(f"❌ {messaggio}")
        print(f"   Errore: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🧪 TEST DOPO FIX URGENTE")
    print("="*60)
    
    # Aspetta deploy
    wait_for_deploy()
    
    print("\n🔍 ESEGUO TEST...\n")
    print("-"*60)
    
    tests = [
        ("Voglio studiare Python 3 ore a settimana", "obiettivo"),
        ("Domani meeting dalle 10 alle 12", "impegno"),
        ("50 euro benzina", "spesa"),
        ("Oggi mi sento motivato", "diario"),
        ("Cosa devo fare oggi?", "domanda"),
    ]
    
    passed = 0
    for messaggio, expected in tests:
        if test_chat(messaggio, expected):
            passed += 1
        print()
    
    print("="*60)
    print(f"📊 RISULTATO: {passed}/{len(tests)} test passati")
    print("="*60)
    
    if passed == len(tests):
        print("\n🎉 TUTTI I TEST PASSATI! APP FUNZIONANTE!")
        return 0
    elif passed > 0:
        print(f"\n⚠️ {len(tests) - passed} test falliti")
        return 1
    else:
        print("\n❌ TUTTI I TEST FALLITI! APP ANCORA ROTTA!")
        return 2

if __name__ == "__main__":
    sys.exit(main())

