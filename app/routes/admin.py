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


@bp.route('/migrate-community', methods=['GET'])
def migrate_community():
    """
    ENDPOINT TEMPORANEO: Forza creazione tabelle community
    Chiamare UNA VOLTA per creare reflection_shares, reactions, comments, etc.
    """
    try:
        results = {
            'status': 'running',
            'steps': []
        }
        
        with db.engine.connect() as conn:
            # Step 1: Crea tabella reflection_shares
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS reflection_shares (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES user_profiles(id),
                        diary_entry_id INTEGER REFERENCES diario(id),
                        shared_text TEXT NOT NULL,
                        original_text TEXT,
                        visibility VARCHAR(20) NOT NULL DEFAULT 'anonymous',
                        category VARCHAR(30) NOT NULL,
                        tags VARCHAR(200),
                        sentiment VARCHAR(20),
                        sentiment_score FLOAT,
                        language VARCHAR(5) DEFAULT 'it',
                        reactions_count INTEGER DEFAULT 0,
                        comments_count INTEGER DEFAULT 0,
                        views_count INTEGER DEFAULT 0,
                        flagged BOOLEAN DEFAULT FALSE,
                        flag_count INTEGER DEFAULT 0,
                        approved BOOLEAN DEFAULT TRUE,
                        moderation_notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.commit()
                results['steps'].append('✅ reflection_shares table created')
            except Exception as e:
                results['steps'].append(f'⚠️ reflection_shares: {str(e)}')
            
            # Step 2: Crea tabella reactions
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS reactions (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES user_profiles(id),
                        reflection_id INTEGER NOT NULL REFERENCES reflection_shares(id) ON DELETE CASCADE,
                        reaction_type VARCHAR(20) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, reflection_id)
                    )
                """))
                conn.commit()
                results['steps'].append('✅ reactions table created')
            except Exception as e:
                results['steps'].append(f'⚠️ reactions: {str(e)}')
            
            # Step 3: Crea tabella comments
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS comments (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES user_profiles(id),
                        reflection_id INTEGER NOT NULL REFERENCES reflection_shares(id) ON DELETE CASCADE,
                        parent_id INTEGER REFERENCES comments(id) ON DELETE CASCADE,
                        text TEXT NOT NULL,
                        approved BOOLEAN DEFAULT TRUE,
                        flagged BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.commit()
                results['steps'].append('✅ comments table created')
            except Exception as e:
                results['steps'].append(f'⚠️ comments: {str(e)}')
            
            # Step 4: Crea tabella circles
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS circles (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        description TEXT,
                        creator_id INTEGER NOT NULL REFERENCES user_profiles(id),
                        max_members INTEGER DEFAULT 10,
                        is_private BOOLEAN DEFAULT TRUE,
                        invite_code VARCHAR(20) UNIQUE,
                        focus_category VARCHAR(50),
                        active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.commit()
                results['steps'].append('✅ circles table created')
            except Exception as e:
                results['steps'].append(f'⚠️ circles: {str(e)}')
            
            # Step 5: Crea tabella circle_members
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS circle_members (
                        id SERIAL PRIMARY KEY,
                        circle_id INTEGER NOT NULL REFERENCES circles(id) ON DELETE CASCADE,
                        user_id INTEGER NOT NULL REFERENCES user_profiles(id),
                        role VARCHAR(20) DEFAULT 'member',
                        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(circle_id, user_id)
                    )
                """))
                conn.commit()
                results['steps'].append('✅ circle_members table created')
            except Exception as e:
                results['steps'].append(f'⚠️ circle_members: {str(e)}')
            
            # Step 6: Verifica tabelle create
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            required_tables = ['reflection_shares', 'reactions', 'comments', 'circles', 'circle_members']
            found_tables = [t for t in required_tables if t in tables]
            missing_tables = [t for t in required_tables if t not in tables]
            
            results['tables_found'] = found_tables
            results['tables_missing'] = missing_tables
            
            if not missing_tables:
                results['status'] = 'success'
                results['message'] = '🎉 Community tables created! Ready to share reflections.'
            else:
                results['status'] = 'incomplete'
                results['message'] = f'⚠️ Some tables missing: {missing_tables}'
        
        return jsonify(results)
        
    except Exception as e:
        import traceback
        return jsonify({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc(),
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

