#!/usr/bin/env python
"""Test locale per verificare che il codice funzioni"""
import sys
import os

# Setup per test locale
os.environ.setdefault('DATABASE_URL', 'sqlite:///test.db')
os.environ.setdefault('SECRET_KEY', 'test-secret-key')

from app import create_app, db
from app.models import UserProfile

def test_app():
    """Test che l'app si avvii e risponda"""
    print("\n" + "="*60)
    print("🧪 TEST LOCALE")
    print("="*60)
    
    print("\n1️⃣ Creazione app...")
    app = create_app()
    
    with app.app_context():
        print("✅ App creata")
        
        print("\n2️⃣ Creazione database...")
        db.create_all()
        print("✅ Database creato")
        
        print("\n3️⃣ Creazione profilo utente...")
        profilo = UserProfile.query.first()
        if not profilo:
            profilo = UserProfile(nome="Test User")
            db.session.add(profilo)
            db.session.commit()
        print(f"✅ Profilo: {profilo.nome}")
        
        print("\n4️⃣ Test InputManager...")
        from app.core import InputManager
        
        input_manager = InputManager()
        
        tests = [
            ("Voglio studiare Python 3 ore a settimana", "obiettivo"),
            ("Domani meeting 10-12", "impegno"),
            ("50 euro benzina", "spesa"),
            ("Oggi mi sento bene", "diario"),
        ]
        
        passed = 0
        for messaggio, expected_tipo in tests:
            result = input_manager.analizza_input(messaggio, lang="it")
            tipo = result.get('tipo')
            
            if tipo == expected_tipo:
                print(f"✅ '{messaggio}' → {tipo}")
                passed += 1
            else:
                print(f"❌ '{messaggio}' → {tipo} (expected: {expected_tipo})")
        
        print("\n" + "="*60)
        print(f"📊 RISULTATO: {passed}/{len(tests)} test passati")
        print("="*60)
        
        if passed == len(tests):
            print("\n🎉 CODICE LOCALE FUNZIONA!")
            print("\n❌ Problema è SOLO sul DATABASE di Render!")
            print("\n💡 SOLUZIONE:")
            print("   Devi eseguire lo script SQL sul database Render")
            print("   oppure usare fix_database_remote.py")
            return True
        else:
            print("\n❌ PROBLEMA NEL CODICE!")
            return False

if __name__ == "__main__":
    try:
        success = test_app()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup
        if os.path.exists('test.db'):
            os.remove('test.db')

