#!/usr/bin/env python
"""
Script per fixare il database Render da remoto
Esegue migration per rimuovere unique constraint su telegram_id
"""
import os
import sys

def fix_database():
    """Fix database usando l'API di Render"""
    
    # Chiedi DATABASE_URL all'utente
    print("\n" + "="*60)
    print("🔧 FIX DATABASE RENDER")
    print("="*60)
    print("\nPer fixare il database serve il DATABASE_URL.")
    print("\n📍 DOVE TROVARLO:")
    print("1. Vai su: https://dashboard.render.com/")
    print("2. Clicca su 'assistente-db' (database)")
    print("3. Scorri fino a 'Connections'")
    print("4. Copia 'Internal Database URL'")
    print("\n" + "="*60)
    
    database_url = input("\n📋 Incolla DATABASE_URL qui: ").strip()
    
    if not database_url:
        print("\n❌ DATABASE_URL non fornito!")
        return False
    
    # Fix postgres:// -> postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    print("\n🔌 Connessione al database...")
    
    try:
        from sqlalchemy import create_engine, text
        
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            print("✅ Connesso!")
            
            # Step 1: Check current state
            print("\n🔍 Controllo stato attuale...")
            result = conn.execute(text("""
                SELECT 
                    column_name, 
                    data_type, 
                    is_nullable,
                    column_default
                FROM information_schema.columns 
                WHERE table_name = 'user_profiles' 
                AND column_name IN ('telegram_id', 'telegram_username')
                ORDER BY column_name
            """))
            
            columns = list(result)
            print(f"📊 Colonne trovate: {len(columns)}")
            for col in columns:
                print(f"   - {col[0]}: {col[1]} (nullable={col[2]})")
            
            # Step 2: Check indexes
            print("\n🔍 Controllo indici...")
            result = conn.execute(text("""
                SELECT 
                    indexname, 
                    indexdef
                FROM pg_indexes 
                WHERE tablename = 'user_profiles'
                AND indexname LIKE '%telegram%'
            """))
            
            indexes = list(result)
            print(f"📊 Indici trovati: {len(indexes)}")
            for idx in indexes:
                print(f"   - {idx[0]}")
            
            # Step 3: Drop UNIQUE constraint if exists
            print("\n🔧 Rimuovo constraint UNIQUE...")
            try:
                conn.execute(text("""
                    ALTER TABLE user_profiles 
                    DROP CONSTRAINT IF EXISTS user_profiles_telegram_id_key
                """))
                conn.commit()
                print("✅ Constraint rimosso (se esisteva)")
            except Exception as e:
                print(f"⚠️ {e}")
            
            # Step 4: Drop and recreate index (non-unique)
            print("\n🔧 Ricreo indice (non-unique)...")
            try:
                conn.execute(text("""
                    DROP INDEX IF EXISTS ix_user_profiles_telegram_id
                """))
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS ix_user_profiles_telegram_id 
                    ON user_profiles(telegram_id)
                """))
                conn.commit()
                print("✅ Indice ricreato come non-unique")
            except Exception as e:
                print(f"⚠️ {e}")
            
            # Step 5: Verify final state
            print("\n🔍 Verifica finale...")
            result = conn.execute(text("""
                SELECT indexname, indexdef
                FROM pg_indexes 
                WHERE tablename = 'user_profiles'
                AND indexname LIKE '%telegram%'
            """))
            
            final_indexes = list(result)
            print(f"📊 Indici finali: {len(final_indexes)}")
            for idx in final_indexes:
                print(f"   - {idx[0]}")
                if 'UNIQUE' in idx[1]:
                    print(f"     ⚠️ ANCORA UNIQUE!")
                else:
                    print(f"     ✅ Non-unique")
            
            print("\n" + "="*60)
            print("🎉 FIX COMPLETATO!")
            print("="*60)
            print("\n✅ Ora riavvia il web service su Render:")
            print("   Dashboard → assistente-intelligente-agenda → Manual Deploy")
            print("\n" + "="*60)
            
            return True
            
    except ImportError:
        print("\n❌ sqlalchemy non installato!")
        print("   Installa con: pip install sqlalchemy psycopg2-binary")
        return False
        
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = fix_database()
    sys.exit(0 if success else 1)

