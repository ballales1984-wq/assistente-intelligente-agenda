"""Configurazione pytest e fixtures condivise"""
import pytest
import os
import tempfile
from app import create_app, db as _db
from config import Config


class TestConfig(Config):
    """Configurazione per testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'
    SERVER_NAME = 'localhost'


@pytest.fixture(scope='session')
def app():
    """
    Crea applicazione Flask per testing
    Con database temporaneo in-memory
    """
    app = create_app(TestConfig)
    
    yield app


@pytest.fixture(scope='session')
def db(app):
    """
    Setup database per testing
    """
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()


@pytest.fixture(scope='function')
def session(app, db):
    """
    Crea una nuova session per ogni test
    Rollback automatico dopo ogni test
    """
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        
        # Usa la session esistente
        session_options = {"bind": connection, "binds": {}}
        session = db.session
        
        yield session
        
        transaction.rollback()
        connection.close()
        session.remove()


@pytest.fixture
def client(app):
    """
    Client di test Flask
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    CLI runner per test comandi
    """
    return app.test_cli_runner()


@pytest.fixture
def auth_headers():
    """
    Headers per autenticazione nei test API
    """
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

