"""Modello del diario giornaliero"""
from app import db
from datetime import datetime, date
import json


class DiarioGiornaliero(db.Model):
    """Diario personale con riflessioni giornaliere"""
    __tablename__ = 'diario'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    
    # Data e contenuto
    data = db.Column(db.Date, nullable=False, default=date.today)
    testo = db.Column(db.Text, nullable=False)  # Testo libero dell'utente
    
    # Analisi automatica
    riflessioni = db.Column(db.Text)  # JSON con concetti estratti
    parole_chiave = db.Column(db.String(500))  # Parole chiave separate da virgola
    sentiment = db.Column(db.String(20))  # positivo, neutro, negativo
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<DiarioGiornaliero {self.data}>'
    
    def to_dict(self):
        """Converte il diario in dizionario"""
        return {
            'id': self.id,
            'data': self.data.isoformat() if self.data else None,
            'testo': self.testo,
            'riflessioni': json.loads(self.riflessioni) if self.riflessioni else [],
            'parole_chiave': self.parole_chiave.split(',') if self.parole_chiave else [],
            'sentiment': self.sentiment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def set_riflessioni(self, riflessioni_list):
        """Imposta le riflessioni da una lista"""
        self.riflessioni = json.dumps(riflessioni_list, ensure_ascii=False)
    
    def get_riflessioni(self):
        """Ottiene le riflessioni come lista"""
        return json.loads(self.riflessioni) if self.riflessioni else []

