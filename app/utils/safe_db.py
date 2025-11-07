"""
Safe database operations che non crashano l'app
"""
from sqlalchemy import inspect


def get_user_profile_safely(db, UserProfile):
    """
    Get profilo utente senza crashare se ci sono problemi con colonne
    """
    try:
        profilo = UserProfile.query.first()
        
        if not profilo:
            # Crea profilo nuovo
            profilo = UserProfile(nome="Utente")
            db.session.add(profilo)
            db.session.commit()
        
        return profilo
        
    except Exception as e:
        # Se fallisce (es: colonne extra nel DB), prova con raw SQL
        try:
            from sqlalchemy import text
            result = db.session.execute(text("""
                SELECT id, nome, stress_tollerato, concentrazione, 
                       priorita, stile_vita, livello_energia, livello_stress
                FROM user_profiles 
                LIMIT 1
            """))
            row = result.first()
            
            if row:
                # Restituisci un oggetto mock con i dati essenziali
                class MockProfile:
                    def __init__(self, data):
                        self.id = data[0]
                        self.nome = data[1]
                        self.stress_tollerato = data[2] or 'medio'
                        self.concentrazione = data[3] or 'media'
                        self.priorita = data[4] or 'bilanciato'
                        self.stile_vita = data[5] or 'bilanciato'
                        self.livello_energia = data[6] or 80
                        self.livello_stress = data[7] or 30
                        
                        # Relationships mock
                        from app.models import Obiettivo, Impegno, DiarioGiornaliero, Spesa
                        self.obiettivi = Obiettivo.query.filter_by(user_id=self.id)
                        self.impegni = Impegno.query.filter_by(user_id=self.id)
                        self.diario_entries = DiarioGiornaliero.query.filter_by(user_id=self.id)
                        self.spese = Spesa.query.filter_by(user_id=self.id)
                
                return MockProfile(row)
            else:
                # Crea nuovo con raw SQL
                db.session.execute(text("""
                    INSERT INTO user_profiles (nome, stress_tollerato, concentrazione, priorita, stile_vita)
                    VALUES ('Utente', 'medio', 'media', 'bilanciato', 'bilanciato')
                """))
                db.session.commit()
                
                # Riprova
                return get_user_profile_safely(db, UserProfile)
                
        except:
            # Ultimo fallback: ritorna None
            return None

