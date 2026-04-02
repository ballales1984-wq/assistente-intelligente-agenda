"""
Sistema di autenticazione fingerprint - FastAPI version
"""
import hashlib
import json
import secrets
from random import choice
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.schemas import UserProfile

ADJECTIVES = [
    'Curious', 'Mindful', 'Brave', 'Calm', 'Focused',
    'Creative', 'Thoughtful', 'Wise', 'Kind', 'Bold',
    'Gentle', 'Strong', 'Peaceful', 'Bright', 'Steady'
]

NOUNS = [
    'Explorer', 'Seeker', 'Dreamer', 'Builder', 'Thinker',
    'Learner', 'Creator', 'Achiever', 'Warrior', 'Soul',
    'Mind', 'Heart', 'Spirit', 'Journey', 'Path'
]


def generate_fingerprint_hash(fingerprint_data: dict) -> str:
    """Genera hash fingerprint dai dati client"""
    fingerprint_string = json.dumps(fingerprint_data, sort_keys=True)
    fingerprint_hash = hashlib.sha256(fingerprint_string.encode()).hexdigest()
    return f"fp_{fingerprint_hash[:16]}"


def get_or_create_user(db: Session, fingerprint: str, client_data: dict = None) -> tuple:
    """
    Ottieni utente esistente o creane uno nuovo.
    Returns: (user, is_new)
    """
    # Cerca per fingerprint
    user = db.query(UserProfile).filter(UserProfile.fingerprint == fingerprint).first()
    
    if user:
        user.last_seen = datetime.utcnow()
        db.commit()
        return user, False
    
    # Crea nuovo utente
    anonymous_name = f"{choice(ADJECTIVES)} {choice(NOUNS)}"
    
    user = UserProfile(
        nome=anonymous_name,
        fingerprint=fingerprint,
        created_at=datetime.utcnow(),
        last_seen=datetime.utcnow()
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user, True
