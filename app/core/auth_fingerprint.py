"""
Sistema di autenticazione senza password basato su fingerprinting
Usa: IP + User-Agent + Browser Fingerprint per identificare univocamente un utente
"""
import hashlib
import json
from datetime import datetime, timedelta
from flask import request, session
from app import db
from app.models import UserProfile


class FingerprintAuth:
    """
    Autenticazione senza password usando fingerprint del browser
    
    Combina:
    - IP address
    - User-Agent
    - Screen resolution
    - Timezone
    - Language
    - Canvas fingerprint (se disponibile)
    
    → Genera ID univoco per device/browser
    """
    
    @staticmethod
    def generate_fingerprint():
        """
        Genera fingerprint univoco dal request corrente
        
        Returns:
            str: Hash univoco (es: "fp_a1b2c3d4e5f6...")
        """
        # Raccogli dati dal request
        ip = request.remote_addr or request.environ.get('HTTP_X_FORWARDED_FOR', 'unknown')
        user_agent = request.headers.get('User-Agent', 'unknown')
        accept_language = request.headers.get('Accept-Language', 'unknown')
        accept_encoding = request.headers.get('Accept-Encoding', 'unknown')
        
        # Combina in stringa unica
        fingerprint_data = {
            'ip': ip,
            'user_agent': user_agent,
            'accept_language': accept_language,
            'accept_encoding': accept_encoding,
        }
        
        # Genera hash
        fingerprint_string = json.dumps(fingerprint_data, sort_keys=True)
        fingerprint_hash = hashlib.sha256(fingerprint_string.encode()).hexdigest()
        
        return f"fp_{fingerprint_hash[:16]}"
    
    @staticmethod
    def get_or_create_user():
        """
        Ottieni utente esistente o creane uno nuovo basato su fingerprint
        
        Returns:
            UserProfile: L'utente corrente
        """
        # Genera fingerprint
        fingerprint = FingerprintAuth.generate_fingerprint()
        
        # Check session prima (più veloce)
        if 'user_id' in session:
            user = UserProfile.query.get(session['user_id'])
            if user and user.fingerprint == fingerprint:
                # Aggiorna last seen
                user.last_seen = datetime.utcnow()
                db.session.commit()
                return user
        
        # Cerca per fingerprint nel database
        user = UserProfile.query.filter_by(fingerprint=fingerprint).first()
        
        if user:
            # Utente esistente trovato!
            session['user_id'] = user.id
            session['fingerprint'] = fingerprint
            
            # Aggiorna last seen
            user.last_seen = datetime.utcnow()
            db.session.commit()
            
            return user
        
        # Nuovo utente - crea
        user = FingerprintAuth.create_new_user(fingerprint)
        
        return user
    
    @staticmethod
    def create_new_user(fingerprint):
        """
        Crea nuovo utente con fingerprint
        
        Args:
            fingerprint: Hash univoco
            
        Returns:
            UserProfile: Nuovo utente creato
        """
        # Genera nome anonimo carino
        from random import choice
        
        adjectives = [
            'Curious', 'Mindful', 'Brave', 'Calm', 'Focused',
            'Creative', 'Thoughtful', 'Wise', 'Kind', 'Bold',
            'Gentle', 'Strong', 'Peaceful', 'Bright', 'Steady'
        ]
        
        nouns = [
            'Explorer', 'Seeker', 'Dreamer', 'Builder', 'Thinker',
            'Learner', 'Creator', 'Achiever', 'Warrior', 'Soul',
            'Mind', 'Heart', 'Spirit', 'Journey', 'Path'
        ]
        
        # Nome tipo "Mindful Explorer #1234"
        anonymous_name = f"{choice(adjectives)} {choice(nouns)}"
        
        # Crea utente
        user = UserProfile(
            nome=anonymous_name,
            fingerprint=fingerprint,
            created_at=datetime.utcnow(),
            last_seen=datetime.utcnow()
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            
            # Set session
            session['user_id'] = user.id
            session['fingerprint'] = fingerprint
            session['is_new_user'] = True  # Flag per mostrare welcome
            
            return user
            
        except Exception as e:
            db.session.rollback()
            # Fallback: usa utente default se errore
            return UserProfile.query.first()
    
    @staticmethod
    def get_current_user():
        """
        Ottieni utente corrente dalla session
        
        Returns:
            UserProfile or None
        """
        if 'user_id' not in session:
            return None
        
        user = UserProfile.query.get(session['user_id'])
        
        # Verifica fingerprint match (security)
        if user:
            current_fingerprint = FingerprintAuth.generate_fingerprint()
            if user.fingerprint != current_fingerprint:
                # Fingerprint cambiato (VPN, nuovo IP, etc)
                # Per sicurezza, logout
                session.clear()
                return None
        
        return user
    
    @staticmethod
    def update_fingerprint_enhanced(client_data):
        """
        Aggiorna fingerprint con dati dal client (JavaScript)
        
        Args:
            client_data: Dict con {
                'screen_width': 1920,
                'screen_height': 1080,
                'timezone': 'Europe/Rome',
                'canvas_fingerprint': 'hash...',
                'language': 'it-IT'
            }
        """
        if 'user_id' not in session:
            return False
        
        user = UserProfile.query.get(session['user_id'])
        if not user:
            return False
        
        # Combina con fingerprint esistente per enhanced version
        base_fp = user.fingerprint
        enhanced_data = json.dumps(client_data, sort_keys=True)
        enhanced_hash = hashlib.sha256((base_fp + enhanced_data).encode()).hexdigest()
        
        user.fingerprint = f"fp_{enhanced_hash[:16]}"
        db.session.commit()
        
        return True
    
    @staticmethod
    def is_new_user():
        """Check se è la prima volta dell'utente"""
        return session.get('is_new_user', False)
    
    @staticmethod
    def clear_new_user_flag():
        """Rimuovi flag new user (dopo onboarding)"""
        session.pop('is_new_user', None)
    
    @staticmethod
    def logout():
        """Logout (clear session)"""
        session.clear()
    
    @staticmethod
    def get_user_info():
        """Info sull'utente corrente"""
        user = FingerprintAuth.get_current_user()
        
        if not user:
            return None
        
        return {
            'id': user.id,
            'name': user.nome,
            'fingerprint': user.fingerprint[:10] + '...',  # Partial per privacy
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_seen': user.last_seen.isoformat() if user.last_seen else None,
            'is_new': FingerprintAuth.is_new_user()
        }


# ========================================
# Decorator per proteggere routes
# ========================================

def require_user(f):
    """
    Decorator per route che richiedono utente
    Crea automaticamente utente se non esiste
    """
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = FingerprintAuth.get_or_create_user()
        
        if not user:
            from flask import jsonify
            return jsonify({
                'success': False,
                'error': 'Unable to identify user'
            }), 401
        
        # Passa user alla funzione
        return f(user, *args, **kwargs)
    
    return decorated_function

