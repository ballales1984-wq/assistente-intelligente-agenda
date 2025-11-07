#!/usr/bin/env python
"""
Script di test completo per verificare che l'app funzioni
Testa tutti gli endpoint principali e il database
"""

import requests
import sys
from datetime import datetime

BASE_URL = "https://assistente-intelligente-agenda.onrender.com"
# BASE_URL = "http://localhost:5000"  # Per test locale

def print_test(test_name, passed):
    """Stampa risultato test"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {test_name}")
    return passed

def test_homepage():
    """Test homepage italiana"""
    try:
        r = requests.get(f"{BASE_URL}/", timeout=10)
        return print_test("Homepage IT", r.status_code == 200)
    except Exception as e:
        print(f"❌ FAIL - Homepage IT: {e}")
        return False

def test_english():
    """Test homepage inglese"""
    try:
        r = requests.get(f"{BASE_URL}/en", timeout=10)
        return print_test("Homepage EN", r.status_code == 200)
    except Exception as e:
        print(f"❌ FAIL - Homepage EN: {e}")
        return False

def test_profilo():
    """Test endpoint profilo"""
    try:
        r = requests.get(f"{BASE_URL}/api/profilo", timeout=10)
        return print_test("API Profilo", r.status_code == 200 and 'nome' in r.json())
    except Exception as e:
        print(f"❌ FAIL - API Profilo: {e}")
        return False

def test_chat_obiettivo():
    """Test chat con creazione obiettivo"""
    try:
        payload = {
            "messaggio": "Voglio studiare Python 3 ore a settimana",
            "lang": "it"
        }
        r = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=10)
        data = r.json()
        passed = (
            r.status_code == 200 and 
            data.get('tipo_riconosciuto') == 'obiettivo' and
            'Python' in data.get('risposta', '')
        )
        return print_test("Chat - Obiettivo", passed)
    except Exception as e:
        print(f"❌ FAIL - Chat Obiettivo: {e}")
        return False

def test_chat_impegno():
    """Test chat con creazione impegno"""
    try:
        payload = {
            "messaggio": "Domani meeting dalle 10 alle 12",
            "lang": "it"
        }
        r = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=10)
        data = r.json()
        passed = (
            r.status_code == 200 and 
            data.get('tipo_riconosciuto') == 'impegno'
        )
        return print_test("Chat - Impegno", passed)
    except Exception as e:
        print(f"❌ FAIL - Chat Impegno: {e}")
        return False

def test_chat_spesa():
    """Test chat con creazione spesa"""
    try:
        payload = {
            "messaggio": "50 euro benzina",
            "lang": "it"
        }
        r = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=10)
        data = r.json()
        passed = (
            r.status_code == 200 and 
            data.get('tipo_riconosciuto') == 'spesa'
        )
        return print_test("Chat - Spesa", passed)
    except Exception as e:
        print(f"❌ FAIL - Chat Spesa: {e}")
        return False

def test_obiettivi():
    """Test endpoint obiettivi"""
    try:
        r = requests.get(f"{BASE_URL}/api/obiettivi", timeout=10)
        passed = r.status_code == 200 and isinstance(r.json(), list)
        return print_test("API Obiettivi", passed)
    except Exception as e:
        print(f"❌ FAIL - API Obiettivi: {e}")
        return False

def test_statistiche():
    """Test endpoint statistiche"""
    try:
        r = requests.get(f"{BASE_URL}/api/statistiche", timeout=10)
        data = r.json()
        passed = (
            r.status_code == 200 and 
            'obiettivi_attivi' in data
        )
        return print_test("API Statistiche", passed)
    except Exception as e:
        print(f"❌ FAIL - API Statistiche: {e}")
        return False

def test_presente_oggi():
    """Test endpoint presente/oggi"""
    try:
        r = requests.get(f"{BASE_URL}/api/presente/oggi", timeout=10)
        passed = r.status_code == 200
        return print_test("API Presente/Oggi", passed)
    except Exception as e:
        print(f"❌ FAIL - API Presente/Oggi: {e}")
        return False

def test_no_telegram():
    """Verifica che Telegram sia stato rimosso"""
    try:
        r = requests.post(f"{BASE_URL}/api/telegram-webhook", json={}, timeout=10)
        # Dovrebbe dare 404 (endpoint non esiste)
        passed = r.status_code == 404
        return print_test("Telegram Rimosso", passed)
    except requests.exceptions.ConnectionError:
        return print_test("Telegram Rimosso", True)
    except Exception as e:
        print(f"❌ FAIL - Telegram Check: {e}")
        return False

def main():
    """Esegue tutti i test"""
    print("\n" + "="*60)
    print(f"🧪 TEST COMPLETO APP - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Target: {BASE_URL}")
    print("="*60 + "\n")
    
    tests = [
        ("🏠 HOMEPAGE", [
            test_homepage,
            test_english,
        ]),
        ("📊 API BASE", [
            test_profilo,
            test_obiettivi,
            test_statistiche,
            test_presente_oggi,
        ]),
        ("💬 CHAT NLP", [
            test_chat_obiettivo,
            test_chat_impegno,
            test_chat_spesa,
        ]),
        ("🧹 PULIZIA", [
            test_no_telegram,
        ])
    ]
    
    total_passed = 0
    total_tests = 0
    
    for category, test_funcs in tests:
        print(f"\n{category}")
        print("-" * 40)
        for test_func in test_funcs:
            if test_func():
                total_passed += 1
            total_tests += 1
    
    print("\n" + "="*60)
    print(f"📊 RISULTATO FINALE: {total_passed}/{total_tests} test passati")
    
    if total_passed == total_tests:
        print("✅ TUTTI I TEST PASSATI! APP FUNZIONANTE! 🎉")
        print("="*60 + "\n")
        return 0
    else:
        print(f"⚠️ {total_tests - total_passed} test falliti")
        print("="*60 + "\n")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrotto dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRORE CRITICO: {e}")
        sys.exit(1)

