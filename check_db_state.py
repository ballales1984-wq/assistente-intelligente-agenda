#!/usr/bin/env python
"""Controlla lo stato ESATTO del database Render"""
from sqlalchemy import create_engine, text
import sys

DATABASE_URL = "postgresql://agenda_user:YEyNRTKYCOpN5aOz4KsSeLoMgzEpOzSf@dpg-d437timuk2gs738qna4g-a.frankfurt-postgres.render.com/agenda_db_bs07"

print("\n" + "="*60)
print("🔍 CONTROLLO STATO DATABASE")
print("="*60)

try:
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        print("\n✅ Connesso!")
        
        # 1. Check tutte le colonne di user_profiles
        print("\n📋 COLONNE user_profiles:")
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'user_profiles'
            ORDER BY ordinal_position
        """))
        
        columns = list(result)
        for col in columns:
            print(f"   - {col[0]}: {col[1]} (null={col[2]})")
        
        # 2. Check constraints
        print("\n🔒 CONSTRAINTS:")
        result = conn.execute(text("""
            SELECT conname, contype 
            FROM pg_constraint 
            WHERE conrelid = 'user_profiles'::regclass
        """))
        
        constraints = list(result)
        for con in constraints:
            print(f"   - {con[0]}: {con[1]}")
        
        # 3. Check indici
        print("\n📑 INDICI:")
        result = conn.execute(text("""
            SELECT indexname 
            FROM pg_indexes 
            WHERE tablename = 'user_profiles'
        """))
        
        indexes = list(result)
        for idx in indexes:
            print(f"   - {idx[0]}")
        
        # 4. Check se ci sono dati
        print("\n📊 DATI:")
        result = conn.execute(text("""
            SELECT COUNT(*) FROM user_profiles
        """))
        count = result.scalar()
        print(f"   Profili: {count}")
        
        print("\n" + "="*60)
        print("ANALISI:")
        print("="*60)
        
        has_telegram = any('telegram' in col[0] for col in columns)
        
        if has_telegram:
            print("\n❌ PROBLEMA: Colonne telegram ANCORA PRESENTI!")
            print("   Il database_fixer NON ha funzionato!")
        else:
            print("\n✅ Colonne telegram: RIMOSSE")
            print("❌ MA c'è un altro problema che causa 500!")
            
        if count == 0:
            print("\n⚠️ Database VUOTO! Manca profilo utente!")
        
except Exception as e:
    print(f"\n❌ ERRORE: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

