"""Modello del profilo utente"""
from app import db
from datetime import datetime


class UserProfile(db.Model):
    """Profilo personalizzato dell'utente"""
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    # Parametri personalizzabili
    stress_tollerato = db.Column(db.String(20), default='medio')  # alto, medio, basso
    concentrazione = db.Column(db.String(20), default='media')  # ottima, media, scarsa
    priorita = db.Column(db.String(50), default='bilanciato')  # studio, sport, riposo, lavoro, bilanciato
    stile_vita = db.Column(db.String(20), default='bilanciato')  # intensivo, bilanciato, rilassato
    
    # Preferenze orarie
    ora_inizio_giornata = db.Column(db.Time, default=datetime.strptime('08:00', '%H:%M').time())
    ora_fine_giornata = db.Column(db.Time, default=datetime.strptime('23:00', '%H:%M').time())
    ore_sonno_desiderate = db.Column(db.Integer, default=8)
    
    # Livelli dinamici (per motore adattivo) - COMMENTATE perché non nel DB
    # livello_energia = db.Column(db.Integer, default=80)  # 0-100
    # livello_stress = db.Column(db.Integer, default=30)   # 0-100
    
    # Authentication fields (presenti nel DB Render)
    token = db.Column(db.String(100), unique=True, index=True, nullable=True)
    fingerprint = db.Column(db.String(100), unique=True, index=True, nullable=True)
    ip_hash = db.Column(db.String(100), nullable=True)
    recovery_code = db.Column(db.String(100), nullable=True)
    device_info = db.Column(db.Text, nullable=True)
    first_seen = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    
    # Relazioni
    obiettivi = db.relationship('Obiettivo', backref='utente', lazy='dynamic', cascade='all, delete-orphan')
    impegni = db.relationship('Impegno', backref='utente', lazy='dynamic', cascade='all, delete-orphan')
    diario_entries = db.relationship('DiarioGiornaliero', backref='utente', lazy='dynamic', cascade='all, delete-orphan')
    spese = db.relationship('Spesa', backref='utente', lazy='dynamic', cascade='all, delete-orphan')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserProfile {self.nome}>'
    
    def to_dict(self):
        """Converte il profilo in dizionario"""
        return {
            'id': self.id,
            'nome': self.nome,
            'stress_tollerato': self.stress_tollerato,
            'concentrazione': self.concentrazione,
            'priorita': self.priorita,
            'stile_vita': self.stile_vita,
            'ora_inizio_giornata': self.ora_inizio_giornata.strftime('%H:%M') if self.ora_inizio_giornata else None,
            'ora_fine_giornata': self.ora_fine_giornata.strftime('%H:%M') if self.ora_fine_giornata else None,
            'ore_sonno_desiderate': self.ore_sonno_desiderate
        }

