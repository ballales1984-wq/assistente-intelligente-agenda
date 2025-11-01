"""Configurazione applicazione"""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# Carica variabili d'ambiente da .env
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Configurazione base"""
    
    # ========================================
    # SECURITY
    # ========================================
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-CHANGE-IN-PRODUCTION'
    
    # ========================================
    # DATABASE
    # ========================================
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'agenda.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    
    # ========================================
    # ENVIRONMENT
    # ========================================
    ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = ENV == 'development'
    TESTING = os.environ.get('TESTING', 'False').lower() == 'true'
    
    # ========================================
    # LOGGING
    # ========================================
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', 'False').lower() == 'true'
    
    # ========================================
    # SESSION SECURITY (Production)
    # ========================================
    if ENV == 'production':
        SESSION_COOKIE_SECURE = True      # Solo HTTPS
        SESSION_COOKIE_HTTPONLY = True    # No JavaScript access
        SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF protection
        PERMANENT_SESSION_LIFETIME = 3600  # 1 ora
    else:
        SESSION_COOKIE_SECURE = False
        SESSION_COOKIE_HTTPONLY = True
        SESSION_COOKIE_SAMESITE = 'Lax'
        PERMANENT_SESSION_LIFETIME = 86400  # 24 ore in development
    
    # ========================================
    # CORS
    # ========================================
    # Domini autorizzati (production)
    ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', '').split(',') if os.environ.get('ALLOWED_ORIGINS') else ['https://tuodominio.com']
    
    # ========================================
    # RATE LIMITING
    # ========================================
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
    # Per production usa Redis: RATELIMIT_STORAGE_URL=redis://localhost:6379
    
    # ========================================
    # APPLICATION
    # ========================================
    DEFAULT_TIMEZONE = 'Europe/Rome'
    PLANNING_HORIZON_DAYS = 7  # Giorni di pianificazione in anticipo
    
    # ========================================
    # MONITORING (Optional)
    # ========================================
    SENTRY_DSN = os.environ.get('SENTRY_DSN')  # Per error tracking production

