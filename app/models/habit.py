"""Modello per Habit Tracking"""
from app import db
from datetime import datetime, date, timedelta


class Habit(db.Model):
    """Abitudine da tracciare quotidianamente"""
    __tablename__ = 'habits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    
    # Dati abitudine
    nome = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.Text)
    icona = db.Column(db.String(10), default='✅')  # Emoji icona
    colore = db.Column(db.String(20), default='#667eea')  # Colore hex
    
    # Frequenza
    frequenza = db.Column(db.String(20), default='daily')  # daily, weekly, custom
    giorni_settimana = db.Column(db.String(50))  # es: "lunedì,mercoledì,venerdì"
    
    # Obiettivo
    obiettivo_numero = db.Column(db.Integer, default=1)  # es: 5 volte a settimana
    unita_misura = db.Column(db.String(30), default='volte')  # volte, minuti, km, etc
    
    # Stato
    attiva = db.Column(db.Boolean, default=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relazione con completamenti
    completamenti = db.relationship('HabitCompletion', backref='habit', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Habit {self.nome}>'
    
    def get_streak(self):
        """Calcola streak corrente (giorni consecutivi)"""
        if not self.completamenti.count():
            return 0
        
        streak = 0
        current_date = date.today()
        
        while True:
            completion = self.completamenti.filter_by(data=current_date).first()
            if not completion or not completion.completato:
                break
            streak += 1
            current_date -= timedelta(days=1)
        
        return streak
    
    def get_completion_rate(self, days=30):
        """Calcola percentuale completamento ultimi N giorni"""
        start_date = date.today() - timedelta(days=days)
        
        total_days = days
        completed_days = self.completamenti.filter(
            HabitCompletion.data >= start_date,
            HabitCompletion.completato == True
        ).count()
        
        return (completed_days / total_days * 100) if total_days > 0 else 0
    
    def to_dict(self):
        """Converte in dizionario"""
        return {
            'id': self.id,
            'nome': self.nome,
            'descrizione': self.descrizione,
            'icona': self.icona,
            'colore': self.colore,
            'frequenza': self.frequenza,
            'giorni_settimana': self.giorni_settimana.split(',') if self.giorni_settimana else [],
            'obiettivo_numero': self.obiettivo_numero,
            'unita_misura': self.unita_misura,
            'attiva': self.attiva,
            'streak': self.get_streak(),
            'completion_rate_30d': round(self.get_completion_rate(30), 1),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class HabitCompletion(db.Model):
    """Completamento giornaliero di un'abitudine"""
    __tablename__ = 'habit_completions'
    
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    
    # Quando
    data = db.Column(db.Date, nullable=False, default=date.today, index=True)
    ora = db.Column(db.Time, default=datetime.utcnow)
    
    # Stato
    completato = db.Column(db.Boolean, default=True)
    valore = db.Column(db.Float)  # es: 30 minuti, 5 km, etc
    note = db.Column(db.Text)  # Note opzionali
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        # Unico constraint: un completamento per habit per giorno
        db.UniqueConstraint('habit_id', 'data', name='uix_habit_data'),
    )
    
    def __repr__(self):
        return f'<HabitCompletion {self.habit_id} on {self.data}>'
    
    def to_dict(self):
        """Converte in dizionario"""
        return {
            'id': self.id,
            'habit_id': self.habit_id,
            'data': self.data.isoformat() if self.data else None,
            'ora': self.ora.isoformat() if self.ora else None,
            'completato': self.completato,
            'valore': self.valore,
            'note': self.note,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

