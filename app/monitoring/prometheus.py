"""
Prometheus Metrics for Wallmind Agenda
Provides business and technical metrics
"""
from prometheus_client import Counter, Histogram, Gauge, Info
from functools import wraps
import time


# ============================================
# APPLICATION INFO
# ============================================
app_info = Info('wallmind_app', 'Application information')


# ============================================
# HTTP METRICS (RED: Rate, Errors, Duration)
# ============================================
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
)

http_errors_total = Counter(
    'http_errors_total',
    'Total HTTP errors',
    ['method', 'endpoint', 'error_type']
)


# ============================================
# DATABASE METRICS
# ============================================
db_queries_total = Counter(
    'db_queries_total',
    'Total database queries',
    ['query_type', 'model']
)

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['query_type', 'model'],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
)

db_connections = Gauge(
    'db_connections',
    'Current database connections',
    ['state']
)


# ============================================
# BUSINESS METRICS
# ============================================
obiettivi_total = Gauge(
    'obiettivi_total',
    'Total number of objectives',
    ['status']
)

obiettivi_completati_total = Counter(
    'obiettivi_completati_total',
    'Total completed objectives'
)

impegni_total = Gauge(
    'impegni_total',
    'Total number of commitments',
    ['tipo']
)

spese_total = Counter(
    'spese_total',
    'Total expenses recorded',
    ['categoria']
)

spese_amount = Counter(
    'spese_amount_euro',
    'Total amount spent in euros',
    ['categoria']
)

diario_entries_total = Counter(
    'diario_entries_total',
    'Total diary entries',
    ['sentiment']
)

users_active = Gauge(
    'users_active',
    'Number of active users'
)


# ============================================
# AI/ML METRICS
# ============================================
ai_suggestions_total = Counter(
    'ai_suggestions_total',
    'Total AI suggestions generated',
    ['suggestion_type']
)

ai_suggestions_accepted = Counter(
    'ai_suggestions_accepted',
    'Total AI suggestions accepted by users',
    ['suggestion_type']
)

nlp_processing_duration_seconds = Histogram(
    'nlp_processing_duration_seconds',
    'NLP processing duration in seconds',
    ['input_type'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0]
)


# ============================================
# CACHE METRICS
# ============================================
cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_key']
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['cache_key']
)


# ============================================
# HELPER FUNCTIONS
# ============================================
def track_request_metrics(endpoint_name):
    """Decorator to track HTTP request metrics"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            from flask import request
            
            method = request.method
            start_time = time.time()
            
            try:
                response = f(*args, **kwargs)
                status = response[1] if isinstance(response, tuple) else 200
                
                # Track success
                http_requests_total.labels(
                    method=method,
                    endpoint=endpoint_name,
                    status=status
                ).inc()
                
                return response
                
            except Exception as e:
                # Track errors
                http_errors_total.labels(
                    method=method,
                    endpoint=endpoint_name,
                    error_type=type(e).__name__
                ).inc()
                
                http_requests_total.labels(
                    method=method,
                    endpoint=endpoint_name,
                    status=500
                ).inc()
                
                raise
                
            finally:
                # Track duration
                duration = time.time() - start_time
                http_request_duration_seconds.labels(
                    method=method,
                    endpoint=endpoint_name
                ).observe(duration)
        
        return wrapper
    return decorator


def track_db_query(query_type, model_name):
    """Decorator to track database query metrics"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = f(*args, **kwargs)
                
                # Track query
                db_queries_total.labels(
                    query_type=query_type,
                    model=model_name
                ).inc()
                
                return result
                
            finally:
                # Track duration
                duration = time.time() - start_time
                db_query_duration_seconds.labels(
                    query_type=query_type,
                    model=model_name
                ).observe(duration)
        
        return wrapper
    return decorator


def update_business_metrics(app):
    """Update business metrics (call periodically)"""
    from app.models import Obiettivo, Impegno, Spesa, DiarioGiornaliero, UserProfile
    from app import db
    
    with app.app_context():
        # Obiettivi
        obiettivi_attivi = Obiettivo.query.filter_by(attivo=True).count()
        obiettivi_completati = Obiettivo.query.filter_by(attivo=False).count()
        obiettivi_total.labels(status='active').set(obiettivi_attivi)
        obiettivi_total.labels(status='completed').set(obiettivi_completati)
        
        # Impegni per tipo
        from sqlalchemy import func
        impegni_per_tipo = db.session.query(
            Impegno.tipo, func.count(Impegno.id)
        ).group_by(Impegno.tipo).all()
        
        for tipo, count in impegni_per_tipo:
            impegni_total.labels(tipo=tipo).set(count)
        
        # Users
        users_count = UserProfile.query.count()
        users_active.set(users_count)


def init_prometheus(app):
    """Initialize Prometheus metrics"""
    from prometheus_flask_exporter import PrometheusMetrics
    
    # Auto-instrument Flask app
    metrics = PrometheusMetrics(app)
    
    # Set application info
    app_info.info({
        'version': '2.0.0',
        'name': 'Wallmind Agenda Intelligente'
    })
    
    app.logger.info("📊 Prometheus metrics initialized at /metrics")
    
    return metrics

