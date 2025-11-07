#!/usr/bin/env python
"""Fix database Render ADESSO"""
from sqlalchemy import create_engine, text
import sys

DATABASE_URL = "postgresql://agenda_user:YEyNRTKYCOpN5aOz4KsSeLoMgzEpOzSf@dpg-d437timuk2gs738qna4g-a.frankfurt-postgres.render.com/agenda_db_bs07"

print("\n" + "="*60)
print("🔧 FIX DATABASE RENDER")
print("="*60)

try:
    print("\n🔌 Connessione al database...")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        print("✅ Connesso!")
        
        # Step 1: Drop constraint UNIQUE
        print("\n🔧 Rimuovo constraint UNIQUE...")
        try:
            conn.execute(text("""
                ALTER TABLE user_profiles 
                DROP CONSTRAINT IF EXISTS user_profiles_telegram_id_key CASCADE
            """))
            conn.commit()
            print("✅ Constraint rimosso")
        except Exception as e:
            print(f"⚠️ {e}")
        
        # Step 2: Drop indice
        print("\n🔧 Rimuovo indice...")
        try:
            conn.execute(text("""
                DROP INDEX IF EXISTS ix_user_profiles_telegram_id CASCADE
            """))
            conn.commit()
            print("✅ Indice rimosso")
        except Exception as e:
            print(f"⚠️ {e}")
        
        # Step 3: DROP COLONNE!
        print("\n🔧 Droppo colonne telegram...")
        try:
            conn.execute(text("""
                ALTER TABLE user_profiles 
                DROP COLUMN IF EXISTS telegram_id CASCADE
            """))
            conn.execute(text("""
                ALTER TABLE user_profiles 
                DROP COLUMN IF EXISTS telegram_username CASCADE
            """))
            conn.commit()
            print("✅ Colonne droppate!")
        except Exception as e:
            print(f"⚠️ {e}")
        
        # Step 4: Verifica
        print("\n🔍 Verifica finale...")
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'user_profiles' 
            AND column_name LIKE '%telegram%'
        """))
        
        telegram_cols = list(result)
        
        if len(telegram_cols) == 0:
            print("✅ Nessuna colonna telegram trovata! PERFETTO!")
        else:
            print(f"⚠️ Ancora {len(telegram_cols)} colonne telegram:")
            for col in telegram_cols:
                print(f"   - {col[0]}")
        
        print("\n" + "="*60)
        print("🎉 FIX COMPLETATO!")
        print("="*60)
        print("\n✅ Ora testo l'app...")
        
except Exception as e:
    print(f"\n❌ ERRORE: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

