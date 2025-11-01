"""Script di setup per inizializzare l'applicazione"""
import os
from app import create_app, db
from app.models import UserProfile


def setup_database():
    """Inizializza il database e crea tabelle"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Creazione database...")
        db.create_all()
        
        # Verifica se esiste già un profilo
        profilo = UserProfile.query.first()
        
        if not profilo:
            print("👤 Creazione profilo utente di default...")
            profilo = UserProfile(
                nome="Utente",
                stress_tollerato="medio",
                concentrazione="media",
                priorita="bilanciato",
                stile_vita="bilanciato"
            )
            db.session.add(profilo)
            db.session.commit()
            print(f"✅ Profilo creato: {profilo.nome}")
        else:
            print(f"✅ Profilo esistente trovato: {profilo.nome}")
        
        print("\n🎉 Setup completato con successo!")
        print("\nPer avviare l'applicazione, esegui:")
        print("  python run.py")
        print("\nQuindi apri il browser su:")
        print("  http://localhost:5000")


if __name__ == '__main__':
    setup_database()

