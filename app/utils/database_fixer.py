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
    DROPPA LE COLONNE TELEGRAM COMPLETAMENTE
    """
    try:
        # Prova a rimuovere TUTTO relativo a telegram
        with db.engine.connect() as conn:
            # 1. Drop constraint UNIQUE se esiste
            try:
                conn.execute(text("""
                    ALTER TABLE user_profiles 
                    DROP CONSTRAINT IF EXISTS user_profiles_telegram_id_key CASCADE
                """))
                conn.commit()
                logger.info("✅ Database fix: Constraint UNIQUE rimosso")
            except Exception as e:
                logger.warning(f"⚠️ Constraint drop: {e}")
            
            # 2. Drop indici
            try:
                conn.execute(text("""
                    DROP INDEX IF EXISTS ix_user_profiles_telegram_id CASCADE
                """))
                conn.commit()
                logger.info("✅ Database fix: Indice rimosso")
            except Exception as e:
                logger.warning(f"⚠️ Index drop: {e}")
            
            # 3. DROP COLONNE TELEGRAM!
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
                logger.info("✅ Database fix: Colonne telegram droppate!")
            except Exception as e:
                logger.warning(f"⚠️ Column drop: {e}")
            
    except Exception as e:
        # Se fallisce, log ma non bloccare
        logger.error(f"❌ Database fix fallito: {e}")
        # Non blocchiamo l'avvio dell'app
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

