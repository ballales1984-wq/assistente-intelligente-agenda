"""
Logger Configuration per Production
Logging strutturato con JSON format e file rotation
"""
import logging
import os
from logging.handlers import RotatingFileHandler
try:
    from pythonjsonlogger import jsonlogger
except ImportError:
    # Fallback se pythonjsonlogger non è disponibile
    jsonlogger = None


def setup_logger(app):
    """
    Setup structured logging per produzione
    
    Features:
    - JSON format per parsing facile
    - File rotation (max 10MB, 10 backup)
    - Console output per development
    - Performance monitoring integrato
    """
    
    # Crea directory logs se non esiste
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # File handler con rotazione automatica
    # Max 10MB per file, mantiene 10 backup (100MB totale)
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, 'app.log'),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    
    # JSON formatter per analisi strutturata
    # Facile da parsare con tools come ELK, Splunk, etc.
    if jsonlogger:
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d'
        )
    else:
        # Fallback a formatter standard
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Console handler per development (human-readable)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
    
    # Aggiungi handlers all'app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    
    # Disabilita propagazione per evitare duplicati
    app.logger.propagate = False
    
    # Log startup
    app.logger.info(
        "Logger inizializzato",
        extra={
            'environment': app.config.get('ENV', 'unknown'),
            'debug': app.debug,
            'logs_directory': logs_dir
        }
    )
    
    return app.logger


def log_performance(app):
    """
    Aggiungi performance monitoring automatico
    Log request duration per ogni chiamata API
    """
    from flask import request, g
    import time
    
    @app.before_request
    def start_timer():
        """Inizia timer per ogni richiesta"""
        g.start_time = time.time()
    
    @app.after_request
    def log_request(response):
        """Log richiesta completata con durata"""
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time
            
            # Log richieste lente (> 1 secondo) come WARNING
            if elapsed > 1:
                app.logger.warning(
                    f"Richiesta lenta: {request.method} {request.path}",
                    extra={
                        'method': request.method,
                        'path': request.path,
                        'duration_seconds': round(elapsed, 3),
                        'status_code': response.status_code,
                        'slow_request': True
                    }
                )
            else:
                # Log richieste normali come INFO
                app.logger.info(
                    f"{request.method} {request.path}",
                    extra={
                        'method': request.method,
                        'path': request.path,
                        'duration_seconds': round(elapsed, 3),
                        'status_code': response.status_code
                    }
                )
        
        return response

