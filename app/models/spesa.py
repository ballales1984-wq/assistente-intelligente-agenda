"""Modello per tracciamento spese quotidiane"""
from app import db
from datetime import datetime


class Spesa(db.Model):
    """Spesa quotidiana con categorizzazione automatica"""
    __tablename__ = 'spese'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    
    # Dettagli spesa
    importo = db.Column(db.Float, nullable=False)  # Euro
    descrizione = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # cibo, trasporti, svago, salute, etc.
    
    # Temporalità
    data = db.Column(db.Date, nullable=False)
    ora = db.Column(db.Time)  # Opzionale, default ora corrente
    
    # Metadata
    luogo = db.Column(db.String(200))  # Dove è stata fatta la spesa (opzionale)
    note = db.Column(db.Text)  # Note aggiuntive
    metodo_pagamento = db.Column(db.String(50))  # contanti, carta, bancomat, etc.
    
    # Classificazione
    necessaria = db.Column(db.Boolean, default=True)  # Necessaria o voluttuaria
    ricorrente = db.Column(db.Boolean, default=False)  # Se è una spesa ricorrente
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Spesa €{self.importo} - {self.descrizione}>'
    
    def to_dict(self):
        """Converte la spesa in dizionario"""
        return {
            'id': self.id,
            'importo': self.importo,
            'descrizione': self.descrizione,
            'categoria': self.categoria,
            'data': self.data.isoformat() if self.data else None,
            'ora': self.ora.strftime('%H:%M') if self.ora else None,
            'luogo': self.luogo,
            'note': self.note,
            'metodo_pagamento': self.metodo_pagamento,
            'necessaria': self.necessaria,
            'ricorrente': self.ricorrente,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# Categorie predefinite
CATEGORIE_SPESE = {
    'cibo': ['pranzo', 'cena', 'colazione', 'spesa', 'supermercato', 'ristorante', 'bar', 'caffè', 'pizza'],
    'trasporti': ['benzina', 'metro', 'bus', 'treno', 'taxi', 'uber', 'parcheggio', 'autostrada'],
    'svago': ['cinema', 'teatro', 'museo', 'concerto', 'bar', 'pub', 'discoteca', 'hobby'],
    'salute': ['farmacia', 'medico', 'dentista', 'palestra', 'sport', 'integratori'],
    'casa': ['affitto', 'bollette', 'luce', 'gas', 'acqua', 'internet', 'telefono'],
    'abbigliamento': ['vestiti', 'scarpe', 'accessori', 'negozio'],
    'tecnologia': ['computer', 'telefono', 'software', 'app', 'abbonamento'],
    'istruzione': ['libri', 'corso', 'università', 'scuola', 'formazione'],
    'regali': ['regalo', 'compleanno', 'natale', 'festa'],
    'altro': []  # Default
}

