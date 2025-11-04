"""Admin routes per manutenzione"""
from flask import Blueprint, jsonify
from app import db
from sqlalchemy import text, inspect

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/migrate-diary-sharing', methods=['GET'])
def migrate_diary_sharing():
    """
    ENDPOINT TEMPORANEO: Forza migrazione campi condivisione diario
    Chiamare UNA VOLTA, poi rimuovere questo endpoint
    """
    try:
        results = {
            'status': 'running',
            'steps': []
        }
        
        with db.engine.connect() as conn:
            # Step 1: Aggiungi share_token
            try:
                conn.execute(text("ALTER TABLE diario ADD COLUMN IF NOT EXISTS share_token VARCHAR(64)"))
                conn.commit()
                results['steps'].append('✅ share_token column added')
            except Exception as e:
                results['steps'].append(f'⚠️ share_token: {str(e)}')
            
            # Step 2: Aggiungi is_public
            try:
                conn.execute(text("ALTER TABLE diario ADD COLUMN IF NOT EXISTS is_public BOOLEAN DEFAULT FALSE"))
                conn.commit()
                results['steps'].append('✅ is_public column added')
            except Exception as e:
                results['steps'].append(f'⚠️ is_public: {str(e)}')
            
            # Step 3: Aggiungi share_count
            try:
                conn.execute(text("ALTER TABLE diario ADD COLUMN IF NOT EXISTS share_count INTEGER DEFAULT 0"))
                conn.commit()
                results['steps'].append('✅ share_count column added')
            except Exception as e:
                results['steps'].append(f'⚠️ share_count: {str(e)}')
            
            # Step 4: Crea indice
            try:
                conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_diario_share_token ON diario (share_token)"))
                conn.commit()
                results['steps'].append('✅ Unique index created')
            except Exception as e:
                results['steps'].append(f'⚠️ index: {str(e)}')
            
            # Step 5: Verifica campi
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='diario'
                ORDER BY ordinal_position
            """))
            columns = [row[0] for row in result]
            results['columns_found'] = columns
            
            # Check se tutti i campi ci sono
            required_fields = ['share_token', 'is_public', 'share_count']
            missing = [f for f in required_fields if f not in columns]
            
            if missing:
                results['status'] = 'incomplete'
                results['missing_fields'] = missing
            else:
                results['status'] = 'success'
                results['message'] = '🎉 Migration completed! All fields present.'
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'message': 'Migration failed. Check database permissions.'
        }), 500


@bp.route('/health', methods=['GET'])
def health_check():
    """Health check con info database"""
    try:
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        # Check diario table
        diario_columns = []
        if 'diario' in tables:
            with db.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='diario'
                """))
                diario_columns = [row[0] for row in result]
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'tables_count': len(tables),
            'diario_columns': diario_columns,
            'has_sharing_fields': all(f in diario_columns for f in ['share_token', 'is_public', 'share_count'])
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

