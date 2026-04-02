from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.core.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    fingerprint = Column(String(64), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

    obiettivi = relationship("Obiettivo", back_populates="utente", cascade="all, delete-orphan")
    impegni = relationship("Impegno", back_populates="utente", cascade="all, delete-orphan")
    diario_entries = relationship("DiarioEntry", back_populates="utente", cascade="all, delete-orphan")
    spese = relationship("Spesa", back_populates="utente", cascade="all, delete-orphan")
    habits = relationship("Habit", back_populates="utente", cascade="all, delete-orphan")


class Obiettivo(Base):
    __tablename__ = "obiettivi"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)

    titolo = Column(String(200), nullable=False)
    descrizione = Column(Text)
    categoria = Column(String(50), default="personale")
    frequenza = Column(String(20), default="settimanale")
    ore_necessarie = Column(Float, default=0)
    ore_completate = Column(Float, default=0)
    progresso = Column(Float, default=0)
    data_inizio = Column(Date)
    data_scadenza = Column(Date)
    completato = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    utente = relationship("UserProfile", back_populates="obiettivi")


class Impegno(Base):
    __tablename__ = "impegni"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)

    titolo = Column(String(200), nullable=False)
    descrizione = Column(Text)
    data = Column(Date, nullable=False)
    ora_inizio = Column(String(5), default="09:00")
    ora_fine = Column(String(5), default="10:00")
    categoria = Column(String(50), default="altro")
    completato = Column(Boolean, default=False)
    promemoria = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    utente = relationship("UserProfile", back_populates="impegni")


class DiarioEntry(Base):
    __tablename__ = "diario"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)

    data = Column(Date, nullable=False, default=date.today)
    contenuto = Column(Text, nullable=False)
    umore = Column(String(20))
    sentiment = Column(String(20))
    tags = Column(Text)  # JSON list as text
    share_token = Column(String(64), unique=True, index=True)
    is_public = Column(Boolean, default=False)
    share_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    utente = relationship("UserProfile", back_populates="diario_entries")


class Spesa(Base):
    __tablename__ = "spese"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)

    importo = Column(Float, nullable=False)
    descrizione = Column(String(200), nullable=False)
    categoria = Column(String(50), nullable=False)
    data = Column(Date, nullable=False)
    necessaria = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    utente = relationship("UserProfile", back_populates="spese")


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)

    nome = Column(String(100), nullable=False)
    descrizione = Column(Text)
    icona = Column(String(10), default="✅")
    colore = Column(String(20), default="#667eea")
    frequenza = Column(String(20), default="daily")
    obiettivo_numero = Column(Integer, default=1)
    unita_misura = Column(String(30), default="volte")
    attiva = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    utente = relationship("UserProfile", back_populates="habits")
    completamenti = relationship("HabitCompletion", back_populates="habit", cascade="all, delete-orphan")


class HabitCompletion(Base):
    __tablename__ = "habit_completions"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    data = Column(Date, nullable=False)
    completato = Column(Boolean, default=True)
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    habit = relationship("Habit", back_populates="completamenti")


class CommunityPost(Base):
    __tablename__ = "community_posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    tipo = Column(String(50), nullable=False)
    contenuto = Column(Text, nullable=False)
    tags = Column(String(200))
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
