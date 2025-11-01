"""Modelli dati dell'applicazione"""
from app.models.user_profile import UserProfile
from app.models.obiettivo import Obiettivo
from app.models.impegno import Impegno
from app.models.diario import DiarioGiornaliero
from app.models.spesa import Spesa, CATEGORIE_SPESE

__all__ = ['UserProfile', 'Obiettivo', 'Impegno', 'DiarioGiornaliero', 'Spesa', 'CATEGORIE_SPESE']

