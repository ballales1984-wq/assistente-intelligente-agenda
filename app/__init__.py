"""Inizializzazione dell'applicazione Flask"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

# Rate Limiter (protezione DDoS)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"  # Per production: usa Redis
)


def create_app(config_class=Config):
    """Factory per creare l'applicazione Flask"""
    # Specifica il percorso corretto per templates e static
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_class)
    
    # ========================================
    # LOGGING STRUTTURATO
    # ========================================
    from app.utils.logger import setup_logger, log_performance
    setup_logger(app)
    log_performance(app)
    
    app.logger.info(f"🚀 Avvio applicazione in modalità {app.config.get('ENV', 'unknown')}")
    
    # ========================================
    # SECURITY: CORS
    # ========================================
    if app.config.get('ENV') == 'production':
        # Production: solo domini autorizzati
        CORS(app, resources={
            r"/api/*": {
                "origins": app.config.get('ALLOWED_ORIGINS', ["https://tuodominio.com"]),
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "allow_headers": ["Content-Type", "Authorization"]
            }
        })
        app.logger.info("🔒 CORS configurato per production (domini limitati)")
    else:
        # Development: permetti tutto
        CORS(app, resources={r"/api/*": {"origins": "*"}})
        app.logger.info("🔓 CORS configurato per development (tutti i domini)")
    
    # ========================================
    # SECURITY: Rate Limiting
    # ========================================
    limiter.init_app(app)
    app.logger.info("🛡️ Rate limiting attivato (200/day, 50/hour)")
    
    # ========================================
    # SECURITY: Headers & HTTPS
    # ========================================
    from flask import request, redirect
    
    # HTTPS enforcement in production
    if app.config.get('ENV') == 'production':
        @app.before_request
        def enforce_https():
            if not request.is_secure and request.headers.get('X-Forwarded-Proto', 'http') != 'https':
                url = request.url.replace('http://', 'https://', 1)
                app.logger.warning(f"Redirect HTTP -> HTTPS: {request.url}")
                return redirect(url, code=301)
    
    # Security headers
    @app.after_request
    def set_security_headers(response):
        """Aggiungi security headers a tutte le risposte"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        if app.config.get('ENV') == 'production':
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response
    
    # ========================================
    # DATABASE
    # ========================================
    db.init_app(app)
    
    # ========================================
    # BLUEPRINTS
    # ========================================
    from app.routes import api
    from app.routes import beta
    app.register_blueprint(api.bp)
    app.register_blueprint(beta.bp)
    app.logger.info("📋 Blueprints registrati (API + Beta)")
    
    # ========================================
    # DATABASE TABLES
    # ========================================
    with app.app_context():
        db.create_all()
        app.logger.info("✅ Database tabelle create/verificate")
    
    app.logger.info("✨ Applicazione pronta!")
    
    return app

