"""Aggiungi campi fingerprint e last_seen a user_profiles"""
from app import create_app, db
from datetime import datetime

app = create_app()

with app.app_context():
    print("🔧 Aggiungendo campi auth a user_profiles...")
    
    try:
        # Aggiungi colonne con SQL diretto
        with db.engine.connect() as conn:
            # Check se esistono già
            result = conn.execute(db.text("PRAGMA table_info(user_profiles)"))
            columns = [row[1] for row in result]
            
            if 'fingerprint' not in columns:
                print("  Aggiungendo fingerprint...")
                conn.execute(db.text(
                    "ALTER TABLE user_profiles ADD COLUMN fingerprint VARCHAR(100)"
                ))
                conn.commit()
                print("  ✅ fingerprint aggiunto")
            else:
                print("  ✅ fingerprint già presente")
            
            if 'last_seen' not in columns:
                print("  Aggiungendo last_seen...")
                conn.execute(db.text(
                    "ALTER TABLE user_profiles ADD COLUMN last_seen DATETIME"
                ))
                conn.commit()
                print("  ✅ last_seen aggiunto")
            else:
                print("  ✅ last_seen già presente")
        
        # Aggiorna utenti esistenti con fingerprint fake
        from app.models import UserProfile
        import hashlib
        
        users_without_fp = UserProfile.query.filter_by(fingerprint=None).all()
        
        for user in users_without_fp:
            # Genera fingerprint legacy
            fake_fp = hashlib.sha256(f"legacy_{user.id}".encode()).hexdigest()
            user.fingerprint = f"fp_{fake_fp[:16]}"
            user.last_seen = datetime.utcnow()
        
        if users_without_fp:
            db.session.commit()
            print(f"\n✅ Aggiornati {len(users_without_fp)} utenti esistenti con fingerprint")
        
        print("\n🎉 COMPLETATO! Database pronto per community!")
        
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()

