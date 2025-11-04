"""Inizializzazione dell'applicazione Flask"""

import os
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
cache = Cache()


# Rate Limiter (protezione DDoS)
# Usa Redis se disponibile, altrimenti memory
def get_limiter_storage_uri():
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        return redis_url
    return "memory://"


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=get_limiter_storage_uri(),
)


def create_app(config_class=Config):
    """Factory per creare l'applicazione Flask"""
    # Specifica il percorso corretto per templates e static
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_class)

    # ========================================
    # ANTI-CACHE: Force template reload
    # ========================================
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.jinja_env.auto_reload = True
    app.logger.info("🔄 Template auto-reload attivato (no cache)")

    # ========================================
    # LOGGING STRUTTURATO
    # ========================================
    from app.utils.logger import setup_logger, log_performance

    setup_logger(app)
    log_performance(app)

    app.logger.info(
        f"🚀 Avvio applicazione in modalità {app.config.get('ENV', 'unknown')}"
    )

    # ========================================
    # SECURITY: CORS
    # ========================================
    if app.config.get("ENV") == "production":
        # Production: solo domini autorizzati
        CORS(
            app,
            resources={
                r"/api/*": {
                    "origins": app.config.get(
                        "ALLOWED_ORIGINS", ["https://tuodominio.com"]
                    ),
                    "methods": ["GET", "POST", "PUT", "DELETE"],
                    "allow_headers": ["Content-Type", "Authorization"],
                }
            },
        )
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
    if app.config.get("ENV") == "production":

        @app.before_request
        def enforce_https():
            if (
                not request.is_secure
                and request.headers.get("X-Forwarded-Proto", "http") != "https"
            ):
                url = request.url.replace("http://", "https://", 1)
                app.logger.warning(f"Redirect HTTP -> HTTPS: {request.url}")
                return redirect(url, code=301)

    # Security headers
    @app.after_request
    def set_security_headers(response):
        """Aggiungi security headers a tutte le risposte"""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        if app.config.get("ENV") == "production":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        return response

    # ========================================
    # DATABASE
    # ========================================
    db.init_app(app)

    # ========================================
    # REDIS CACHING
    # ========================================
    redis_url = os.getenv("REDIS_URL")

    if redis_url:
        # Production: usa Redis
        cache.init_app(
            app,
            config={
                "CACHE_TYPE": "redis",
                "CACHE_REDIS_URL": redis_url,
                "CACHE_DEFAULT_TIMEOUT": 300,  # 5 minuti default
                "CACHE_KEY_PREFIX": "agenda_",
            },
        )
        app.logger.info("🔴 Redis caching attivato!")
    else:
        # Development: usa SimpleCache (memory)
        cache.init_app(
            app, config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 300}
        )
        app.logger.info("💾 SimpleCache attivato (dev mode)")

    # ========================================
    # BLUEPRINTS
    # ========================================
    from app.routes import api
    from app.routes import beta
    from app.routes import ai_chat
    from app.routes import community
    from app.routes import debug
    from app.routes import admin

    app.register_blueprint(api.bp)
    app.register_blueprint(beta.bp)
    app.register_blueprint(ai_chat.bp)
    app.register_blueprint(community.bp)
    app.register_blueprint(debug.bp)
    app.register_blueprint(admin.bp)
    app.logger.info(
        "📋 Blueprints registrati (API + Beta + AI + Community + Debug + Admin)"
    )

    # ========================================
    # DATABASE TABLES
    # ========================================
    with app.app_context():
        db.create_all()
        app.logger.info("✅ Database tabelle create/verificate")

    # ========================================
    # ERROR HANDLERS
    # ========================================
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors"""
        # Distingui API da frontend
        if request.path.startswith("/api/"):
            return (
                jsonify(
                    {
                        "error": "Not Found",
                        "message": "The requested resource was not found",
                        "path": request.path,
                        "status": 404,
                    }
                ),
                404,
            )
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        app.logger.error(f"500 Internal Error: {error}")
        db.session.rollback()  # Rollback eventuali transazioni pendenti

        # Distingui API da frontend
        if request.path.startswith("/api/"):
            return (
                jsonify(
                    {
                        "error": "Internal Server Error",
                        "message": "An internal error occurred. Please try again later.",
                        "status": 500,
                    }
                ),
                500,
            )
        return render_template("500.html"), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle 403 errors"""
        if request.path.startswith("/api/"):
            return (
                jsonify(
                    {
                        "error": "Forbidden",
                        "message": "You do not have permission to access this resource",
                        "status": 403,
                    }
                ),
                403,
            )
        return (
            render_template(
                "error.html",
                error_title="403 - Accesso Negato",
                error_message="Non hai i permessi per accedere a questa risorsa.",
            ),
            403,
        )

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle all other exceptions"""
        app.logger.error(f"Unhandled exception: {e}", exc_info=True)
        db.session.rollback()

        # Distingui API da frontend
        if request.path.startswith("/api/"):
            return (
                jsonify(
                    {
                        "error": "Server Error",
                        "message": (
                            str(e) if app.config.get("DEBUG") else "An error occurred"
                        ),
                        "status": 500,
                    }
                ),
                500,
            )

        return (
            render_template(
                "error.html",
                error_title="Si è Verificato un Errore",
                error_message="Qualcosa non ha funzionato. Riprova tra poco!",
                error_details=str(e) if app.config.get("DEBUG") else None,
            ),
            500,
        )

    app.logger.info("🛡️ Error handlers registrati (404, 500, 403, Exception)")
    app.logger.info("✨ Applicazione pronta!")

    return app
