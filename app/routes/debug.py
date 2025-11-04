"""DEBUG ENDPOINT - Force database fix via HTTP call"""
from flask import Blueprint, jsonify
from app import db
from sqlalchemy import text

bp = Blueprint('debug', __name__, url_prefix='/debug')

@bp.route('/fix-database', methods=['GET'])
def fix_database():
    """Force database fix - call this URL to trigger fix!"""
    results = {
        'status': 'starting',
        'steps': []
    }
    
    try:
        # Step 1: Create all tables
        results['steps'].append('Creating all tables...')
        db.create_all()
        results['steps'].append('✅ Tables created')
        
        # Step 2: Add fingerprint column if missing
        with db.engine.connect() as conn:
            try:
                # Try to add fingerprint - will fail if exists (that's OK!)
                conn.execute(text("""
                    ALTER TABLE user_profiles 
                    ADD COLUMN IF NOT EXISTS fingerprint VARCHAR(100)
                """))
                conn.commit()
                results['steps'].append('✅ fingerprint column added/exists')
            except Exception as e:
                results['steps'].append(f'fingerprint: {str(e)[:100]}')
            
            try:
                # Try to add last_seen
                conn.execute(text("""
                    ALTER TABLE user_profiles 
                    ADD COLUMN IF NOT EXISTS last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                """))
                conn.commit()
                results['steps'].append('✅ last_seen column added/exists')
            except Exception as e:
                results['steps'].append(f'last_seen: {str(e)[:100]}')
        
        results['status'] = 'completed'
        return jsonify(results), 200
        
    except Exception as e:
        results['status'] = 'failed'
        results['error'] = str(e)
        return jsonify(results), 500

