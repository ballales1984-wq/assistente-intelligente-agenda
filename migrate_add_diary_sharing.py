#!/usr/bin/env python3
"""
Migrazione: Aggiunge campi di condivisione al modello DiarioGiornaliero
"""
import sys
import os
from sqlalchemy import create_engine, MetaData, Table, Column, String, Boolean, Integer, Index, text

# Setup path
sys.path.insert(0, os.path.dirname(__file__))

from config import Config

def migrate():
    """Aggiunge i campi share_token, is_public, share_count alla tabella diario"""
    
    print("🔄 Avvio migrazione: Aggiunta campi condivisione diario...")
    
    # Connetti al database
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    metadata = MetaData()
    
    try:
        # Controlla quale database stiamo usando
        db_uri = Config.SQLALCHEMY_DATABASE_URI
        is_sqlite = db_uri.startswith('sqlite')
        is_postgres = 'postgresql' in db_uri
        
        with engine.connect() as conn:
            # Per SQLite
            if is_sqlite:
                print("📊 Rilevato database SQLite")
                
                # Controlla se le colonne esistono già
                result = conn.execute(text("PRAGMA table_info(diario)"))
                columns = [row[1] for row in result]
                
                if 'share_token' not in columns:
                    print("➕ Aggiunta colonna share_token...")
                    conn.execute(text("ALTER TABLE diario ADD COLUMN share_token VARCHAR(64)"))
                    conn.commit()
                
                if 'is_public' not in columns:
                    print("➕ Aggiunta colonna is_public...")
                    conn.execute(text("ALTER TABLE diario ADD COLUMN is_public BOOLEAN DEFAULT 0"))
                    conn.commit()
                
                if 'share_count' not in columns:
                    print("➕ Aggiunta colonna share_count...")
                    conn.execute(text("ALTER TABLE diario ADD COLUMN share_count INTEGER DEFAULT 0"))
                    conn.commit()
                
                # Crea indice per share_token
                try:
                    conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_diario_share_token ON diario (share_token)"))
                    conn.commit()
                    print("📑 Creato indice su share_token")
                except:
                    pass
            
            # Per PostgreSQL
            elif is_postgres:
                print("📊 Rilevato database PostgreSQL")
                
                # Controlla se le colonne esistono
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='diario'
                """))
                columns = [row[0] for row in result]
                
                if 'share_token' not in columns:
                    print("➕ Aggiunta colonna share_token...")
                    conn.execute(text("ALTER TABLE diario ADD COLUMN share_token VARCHAR(64)"))
                    conn.commit()
                
                if 'is_public' not in columns:
                    print("➕ Aggiunta colonna is_public...")
                    conn.execute(text("ALTER TABLE diario ADD COLUMN is_public BOOLEAN DEFAULT FALSE"))
                    conn.commit()
                
                if 'share_count' not in columns:
                    print("➕ Aggiunta colonna share_count...")
                    conn.execute(text("ALTER TABLE diario ADD COLUMN share_count INTEGER DEFAULT 0"))
                    conn.commit()
                
                # Crea indice unico per share_token
                try:
                    conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_diario_share_token ON diario (share_token)"))
                    conn.commit()
                    print("📑 Creato indice su share_token")
                except:
                    pass
        
        print("\n✅ Migrazione completata con successo!")
        print("\n📋 Campi aggiunti:")
        print("   - share_token (VARCHAR 64, unique)")
        print("   - is_public (BOOLEAN, default False)")
        print("   - share_count (INTEGER, default 0)")
        print("\n🔗 Ora puoi condividere le voci del diario!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Errore durante la migrazione: {e}")
        return False
    finally:
        engine.dispose()

if __name__ == '__main__':
    success = migrate()
    sys.exit(0 if success else 1)

