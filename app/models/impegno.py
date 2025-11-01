"""Modello degli impegni fissi"""
from app import db
from datetime import datetime


class Impegno(db.Model):
    """Impegno fisso in agenda"""
    __tablename__ = 'impegni'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    
    # Dettagli impegno
    nome = db.Column(db.String(200), nullable=False)
    descrizione = db.Column(db.Text)
    tipo = db.Column(db.String(50))  # lavoro, appuntamento, evento, personale
    
    # Temporalità
    data_inizio = db.Column(db.DateTime, nullable=False)
    data_fine = db.Column(db.DateTime, nullable=False)
    
    # Ricorrenza
    ricorrente = db.Column(db.Boolean, default=False)
    pattern_ricorrenza = db.Column(db.String(50))  # giornaliero, settimanale, mensile
    giorni_settimana = db.Column(db.String(50))  # es. "lun,mer,ven" per impegni ricorrenti
    
    # Caratteristiche
    spostabile = db.Column(db.Boolean, default=False)
    priorita = db.Column(db.Integer, default=5)  # 1-10, dove 10 è massima priorità
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Impegno {self.nome}>'
    
    def to_dict(self):
        """Converte l'impegno in dizionario"""
        return {
            'id': self.id,
            'nome': self.nome,
            'descrizione': self.descrizione,
            'tipo': self.tipo,
            'data_inizio': self.data_inizio.isoformat() if self.data_inizio else None,
            'data_fine': self.data_fine.isoformat() if self.data_fine else None,
            'ricorrente': self.ricorrente,
            'pattern_ricorrenza': self.pattern_ricorrenza,
            'giorni_settimana': self.giorni_settimana,
            'spostabile': self.spostabile,
            'priorita': self.priorita
        }

