"""Script per inizializzare tabelle community su Render"""
from app import create_app, db

print("🔧 Inizializzazione database community...")

app = create_app()

with app.app_context():
    # Import esplicito di tutti i modelli
    from app.models import (
        UserProfile, Obiettivo, Impegno, DiarioGiornaliero, Spesa,
        ReflectionShare, Reaction, Comment, Circle, CircleMember,
        Challenge, ChallengeParticipation, UserBan, ModerationLog
    )
    
    print("✅ Modelli importati")
    
    # Crea tutte le tabelle
    db.create_all()
    print("✅ db.create_all() eseguito")
    
    # Verifica tabelle create
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    print(f"\n📊 Totale tabelle nel database: {len(tables)}")
    print("\nTabelle presenti:")
    for table in sorted(tables):
        print(f"  ✅ {table}")
    
    # Check specifiche tabelle community
    community_tables = [
        'reflection_shares', 'reactions', 'comments', 
        'circles', 'circle_members', 'challenges', 
        'challenge_participations', 'user_bans', 'moderation_logs'
    ]
    
    print("\n🔍 Verifica Tabelle Community:")
    missing = []
    for table in community_tables:
        if table in tables:
            print(f"  ✅ {table} - OK")
        else:
            print(f"  ❌ {table} - MISSING!")
            missing.append(table)
    
    if missing:
        print(f"\n⚠️ ATTENZIONE: {len(missing)} tabelle mancanti!")
        print("Riprova ad eseguire questo script.")
    else:
        print("\n🎉 SUCCESSO! Tutte le tabelle community sono presenti!")
        print("\n✅ La pagina /community dovrebbe funzionare ora!")

print("\n✨ Script completato!")
