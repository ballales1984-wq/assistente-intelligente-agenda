#!/usr/bin/env python
"""Test locale COMPLETO prima di pushare"""
import os
import sys

# Setup ambiente locale
os.environ['DATABASE_URL'] = 'sqlite:///test_local.db'
os.environ['SECRET_KEY'] = 'test-key'

print("\n" + "="*60)
print("🧪 TEST LOCALE COMPLETO")
print("="*60)

print("\n1️⃣ Avvio app...")
from app import create_app, db
from app.models import UserProfile, Obiettivo, Impegno, Spesa, DiarioGiornaliero

app = create_app()

with app.test_client() as client:
    with app.app_context():
        print("✅ App creata")
        
        print("\n2️⃣ Test /api/chat endpoint...")
        
        tests = [
            {
                "messaggio": "Voglio studiare Python 3 ore a settimana",
                "expected": "obiettivo",
                "desc": "Obiettivo"
            },
            {
                "messaggio": "Domenica vado al mare dalle 16 alle 20",
                "expected": "impegno",
                "desc": "Impegno"
            },
            {
                "messaggio": "50 euro benzina",
                "expected": "spesa",
                "desc": "Spesa"
            },
            {
                "messaggio": "Oggi mi sento motivato",
                "expected": "diario",
                "desc": "Diario"
            },
        ]
        
        passed = 0
        failed = []
        
        for test in tests:
            try:
                response = client.post(
                    '/api/chat',
                    json={'messaggio': test['messaggio'], 'lang': 'it'},
                    content_type='application/json'
                )
                
                if response.status_code != 200:
                    print(f"❌ {test['desc']}: Status {response.status_code}")
                    print(f"   Response: {response.get_json()}")
                    failed.append(test['desc'])
                    continue
                
                data = response.get_json()
                tipo = data.get('tipo_riconosciuto')
                
                if tipo == test['expected']:
                    print(f"✅ {test['desc']}: '{test['messaggio']}' → {tipo}")
                    passed += 1
                else:
                    print(f"❌ {test['desc']}: Expected {test['expected']}, got {tipo}")
                    failed.append(test['desc'])
                    
            except Exception as e:
                print(f"❌ {test['desc']}: Exception: {e}")
                import traceback
                traceback.print_exc()
                failed.append(test['desc'])
        
        print("\n" + "="*60)
        print(f"📊 RISULTATO: {passed}/{len(tests)} test passati")
        print("="*60)
        
        if passed == len(tests):
            print("\n🎉 TUTTI I TEST PASSATI!")
            print("\n✅ ORA POSSO PUSHARE SU RENDER!")
            sys.exit(0)
        else:
            print(f"\n❌ {len(failed)} TEST FALLITI:")
            for f in failed:
                print(f"   - {f}")
            print("\n⚠️ NON PUSHARE! FIXA PRIMA!")
            sys.exit(1)

# Cleanup
if os.path.exists('test_local.db'):
    os.remove('test_local.db')

