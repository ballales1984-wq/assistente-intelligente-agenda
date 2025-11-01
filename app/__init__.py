"""Inizializzazione dell'applicazione Flask"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    """Factory per creare l'applicazione Flask"""
    # Specifica il percorso corretto per templates e static
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_class)
    
    # Inizializza estensioni
    db.init_app(app)
    
    # Registra blueprints
    from app.routes import api
    app.register_blueprint(api.bp)
    
    # Crea tabelle database
    with app.app_context():
        db.create_all()
    
    return app

