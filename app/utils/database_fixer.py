"""
Auto-fix per database issues
Si esegue automaticamente all'avvio dell'app
"""
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)


def fix_telegram_constraint(db):
    """
    Fix UNIQUE constraint su telegram_id che causa errore 500
    Questo script si esegue automaticamente all'avvio
    """
    try:
        # Prova a rimuovere il constraint UNIQUE problematico
        with db.engine.connect() as conn:
            # Drop constraint UNIQUE se esiste
            conn.execute(text("""
                ALTER TABLE user_profiles 
                DROP CONSTRAINT IF EXISTS user_profiles_telegram_id_key
            """))
            conn.commit()
            
            logger.info("✅ Database fix: Constraint UNIQUE rimosso da telegram_id")
            
            # Drop e ricrea indice come non-unique
            conn.execute(text("""
                DROP INDEX IF EXISTS ix_user_profiles_telegram_id
            """))
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_user_profiles_telegram_id 
                ON user_profiles(telegram_id)
            """))
            conn.commit()
            
            logger.info("✅ Database fix: Indice telegram_id ricreato come non-unique")
            
    except Exception as e:
        # Se fallisce, probabilmente il constraint non esiste (già fixato)
        logger.warning(f"⚠️ Database fix: {e}")
        # Non blocchiamo l'avvio dell'app se fallisce
        pass


def auto_fix_database(app, db):
    """
    Esegue tutti i fix automatici necessari
    Chiamato all'avvio dell'app
    """
    with app.app_context():
        try:
            # Fix 1: Telegram constraint
            fix_telegram_constraint(db)
            
            logger.info("✅ Auto-fix database completato")
            
        except Exception as e:
            logger.error(f"❌ Auto-fix database fallito: {e}")
            # Non blocchiamo l'avvio dell'app
            pass

