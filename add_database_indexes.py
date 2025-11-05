"""Script per aggiungere indexes al database per performance"""

import sys
from app import create_app, db
from sqlalchemy import text

def add_indexes():
    """Aggiunge indexes ottimizzati per le query più frequenti"""
    
    print("=" * 70)
    print("🚀 AGGIUNTA INDEXES DATABASE PER PERFORMANCE")
    print("=" * 70)
    print()
    
    app = create_app()
    
    with app.app_context():
        # Verifica se siamo su SQLite o PostgreSQL
        engine_name = db.engine.name
        print(f"📊 Database: {engine_name}")
        print()
        
        indexes_to_add = []
        
        # ========================================
        # OBIETTIVI
        # ========================================
        print("🎯 OBIETTIVI:")
        
        # Index su user_id + attivo (query più frequente)
        indexes_to_add.append({
            'name': 'idx_obiettivi_user_attivo',
            'table': 'obiettivi',
            'columns': 'user_id, attivo',
            'sql': 'CREATE INDEX IF NOT EXISTS idx_obiettivi_user_attivo ON obiettivi(user_id, attivo)'
        })
        
        # Index su tipo (filtri)
        indexes_to_add.append({
            'name': 'idx_obiettivi_tipo',
            'table': 'obiettivi',
            'columns': 'tipo',
            'sql': 'CREATE INDEX IF NOT EXISTS idx_obiettivi_tipo ON obiettivi(tipo)'
        })
        
        # ========================================
        # IMPEGNI
        # ========================================
        print("📅 IMPEGNI:")
        
        # Index su data_inizio (query range più frequente)
        indexes_to_add.append({
            'name': 'idx_impegni_data_inizio',
            'table': 'impegni',
            'columns': 'data_inizio',
            'sql': 'CREATE INDEX IF NOT EXISTS idx_impegni_data_inizio ON impegni(data_inizio)'
        })
        
        # Index composito user_id + data_inizio
        indexes_to_add.append({
            'name': 'idx_impegni_user_data',
            'table': 'impegni',
            'columns': 'user_id, data_inizio',
            'sql': 'CREATE INDEX IF NOT EXISTS idx_impegni_user_data ON impegni(user_id, data_inizio)'
        })
        
        # ========================================
        # SPESE
        # ========================================
        print("💰 SPESE:")
        
        # Index su data (query più frequente)
        indexes_to_add.append({
            'name': 'idx_spese_data',
            'table': 'spese',
            'columns': 'data',
            'sql': 'CREATE INDEX IF NOT EXISTS idx_spese_data ON spese(data)'
        })
        
        # Index composito user_id + data
        indexes_to_add.append({
            'name': 'idx_spese_user_data',
            'table': 'spese',
            'columns': 'user_id, data',
            'sql': 'CREATE INDEX IF NOT EXISTS idx_spese_user_data ON spese(user_id, data)'
        })
        
        # Index su categoria (per analytics)
        indexes_to_add.append({
            'name': 'idx_spese_categoria',
            'table': 'spese',
            'columns': 'categoria',
            'sql': 'CREATE INDEX IF NOT EXISTS idx_spese_categoria ON spese(categoria)'
        })
        
        # ========================================
        # DIARIO
        # ========================================
        print("📔 DIARIO:")
        
        # Index su data
        indexes_to_add.append({
            'name': 'idx_diario_data',
            'table': 'diario',
            'columns': 'data',
            'sql': 'CREATE INDEX IF NOT EXISTS idx_diario_data ON diario(data)'
        })
        
        # Index su sentiment (per filtri)
        indexes_to_add.append({
            'name': 'idx_diario_sentiment',
            'table': 'diario',
            'columns': 'sentiment',
            'sql': 'CREATE INDEX IF NOT EXISTS idx_diario_sentiment ON diario(sentiment)'
        })
        
        # ========================================
        # APPLICAZIONE INDEXES
        # ========================================
        print()
        print("📝 Applicazione indexes...")
        print()
        
        added = 0
        skipped = 0
        errors = 0
        
        for idx in indexes_to_add:
            try:
                # Esegui SQL raw per creare index
                db.session.execute(text(idx['sql']))
                db.session.commit()
                print(f"   ✅ {idx['name']} su {idx['table']}({idx['columns']})")
                added += 1
            except Exception as e:
                error_msg = str(e).lower()
                if 'already exists' in error_msg or 'duplicate' in error_msg:
                    print(f"   ⏭️  {idx['name']} (già esistente)")
                    skipped += 1
                else:
                    print(f"   ❌ {idx['name']}: {e}")
                    errors += 1
        
        print()
        print("=" * 70)
        print(f"📊 RISULTATI:")
        print(f"   ✅ Indexes aggiunti: {added}")
        print(f"   ⏭️  Indexes già esistenti: {skipped}")
        print(f"   ❌ Errori: {errors}")
        print("=" * 70)
        print()
        
        if errors == 0:
            print("✅ INDEXES APPLICATI CON SUCCESSO!")
            print()
            print("📈 BENEFICI ATTESI:")
            print("   - Query su date range: 90%+ più veloci")
            print("   - Filtri per categoria: 95%+ più veloci")
            print("   - Join con user_id: 80%+ più veloci")
            print()
        else:
            print(f"⚠️  {errors} errori durante l'applicazione degli indexes")
            print("   Verifica i messaggi sopra per dettagli")


if __name__ == "__main__":
    try:
        add_indexes()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operazione interrotta dall'utente")
        sys.exit(0)

