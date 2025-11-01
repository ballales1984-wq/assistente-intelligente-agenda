"""Configurazione applicazione"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configurazione base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'agenda.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Parametri applicazione
    DEFAULT_TIMEZONE = 'Europe/Rome'
    PLANNING_HORIZON_DAYS = 7  # Giorni di pianificazione in anticipo

