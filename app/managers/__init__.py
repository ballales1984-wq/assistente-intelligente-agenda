"""Manager per gestione temporale: Passato, Presente, Futuro + Spese"""
from app.managers.passato_manager import PassatoManager
from app.managers.presente_manager import PresenteManager
from app.managers.futuro_manager import FuturoManager
from app.managers.spese_manager import SpeseManager

__all__ = ['PassatoManager', 'PresenteManager', 'FuturoManager', 'SpeseManager']

