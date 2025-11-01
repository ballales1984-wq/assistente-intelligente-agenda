"""Modello degli obiettivi"""
from app import db
from datetime import datetime


class Obiettivo(db.Model):
    """Obiettivo da raggiungere"""
    __tablename__ = 'obiettivi'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    
    # Dettagli obiettivo
    nome = db.Column(db.String(200), nullable=False)
    descrizione = db.Column(db.Text)
    tipo = db.Column(db.String(50), nullable=False)  # studio, sport, progetto, personale, lavoro
    
    # Parametri temporali
    durata_settimanale = db.Column(db.Float, nullable=False)  # Ore a settimana
    scadenza = db.Column(db.Date)  # Data entro cui completare
    
    # Caratteristiche
    intensita = db.Column(db.String(20), default='media')  # alta, media, bassa
    flessibilita = db.Column(db.String(20), default='media')  # alta, media, bassa (quanto si può spostare)
    
    # Preferenze
    orari_preferiti = db.Column(db.String(100))  # es. "mattina", "pomeriggio", "sera", "notte"
    giorni_preferiti = db.Column(db.String(100))  # es. "lun,mer,ven"
    
    # Tracking
    ore_completate = db.Column(db.Float, default=0.0)
    attivo = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Obiettivo {self.nome}>'
    
    def to_dict(self):
        """Converte l'obiettivo in dizionario"""
        return {
            'id': self.id,
            'nome': self.nome,
            'descrizione': self.descrizione,
            'tipo': self.tipo,
            'durata_settimanale': self.durata_settimanale,
            'scadenza': self.scadenza.isoformat() if self.scadenza else None,
            'intensita': self.intensita,
            'flessibilita': self.flessibilita,
            'orari_preferiti': self.orari_preferiti,
            'giorni_preferiti': self.giorni_preferiti,
            'ore_completate': self.ore_completate,
            'attivo': self.attivo
        }

