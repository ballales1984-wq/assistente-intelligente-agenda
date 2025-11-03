"""Temporary auth without fingerprint - Quick fix for community"""
from app import db
from app.models import UserProfile
from flask import session
import secrets

def get_or_create_temp_user():
    """
    Get or create user WITHOUT fingerprint column
    Temporary fix until database migration completes
    """
    # Use session to track user
    if 'temp_user_id' not in session:
        # Create new temp user
        nome_random = f"User_{secrets.token_hex(4)}"
        
        # Create user WITHOUT fingerprint
        nuovo_profilo = UserProfile(nome=nome_random)
        db.session.add(nuovo_profilo)
        db.session.commit()
        
        session['temp_user_id'] = nuovo_profilo.id
        session.permanent = True
        
        return nuovo_profilo
    else:
        # Get existing user from session
        user_id = session.get('temp_user_id')
        profilo = UserProfile.query.get(user_id)
        
        if not profilo:
            # Session expired or user deleted, create new
            del session['temp_user_id']
            return get_or_create_temp_user()
        
        return profilo

