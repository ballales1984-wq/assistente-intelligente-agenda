"""Test per MotoreAdattivo"""
import pytest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import UserProfile, Obiettivo
from app.core.motore_adattivo import MotoreAdattivo


@pytest.fixture
def app():
    """Crea app di test"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def user_profile(app):
    """Crea profilo utente di test"""
    with app.app_context():
        profilo = UserProfile(nome='Test User')
        db.session.add(profilo)
        db.session.commit()
        return profilo


class TestMotoreAdattivo:
    """Test suite per MotoreAdattivo"""
    
    def test_inizializzazione(self, app, user_profile):
        """Test inizializzazione motore"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            motore = MotoreAdattivo(profilo)
            
            assert motore.user_profile.id == profilo.id
            assert 'energia' in motore.stato_corrente
            assert 'stress' in motore.stato_corrente
    
    def test_aggiorna_stato_energia(self, app, user_profile):
        """Test aggiornamento stato energia"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            motore = MotoreAdattivo(profilo)
            
            suggerimenti = motore.aggiorna_stato('energia', 'bassa')
            
            assert motore.stato_corrente['energia'] == 'bassa'
            assert isinstance(suggerimenti, list)
            assert len(suggerimenti) > 0
    
    def test_aggiorna_stato_stress(self, app, user_profile):
        """Test aggiornamento stato stress"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            motore = MotoreAdattivo(profilo)
            
            suggerimenti = motore.aggiorna_stato('stress', 'alto')
            
            assert motore.stato_corrente['stress'] == 'alto'
            assert len(suggerimenti) > 0
    
    def test_attivita_completata(self, app, user_profile):
        """Test completamento attività"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            motore = MotoreAdattivo(profilo)
            
            attivita = {
                'tipo': 'obiettivo',
                'nome': 'Studio',
                'durata_ore': 2.0
            }
            
            risultato = motore.attivita_completata(attivita, tempo_effettivo=1.5)
            
            assert 'messaggio' in risultato
            assert 'tempo_libero' in risultato
            assert risultato['tempo_libero'] == 0.5
    
    def test_suggerisci_uso_tempo_libero(self, app, user_profile):
        """Test suggerimenti per tempo libero"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            motore = MotoreAdattivo(profilo)
            
            # Test con molto tempo libero
            suggerimenti_lunghi = motore._suggerisci_uso_tempo_libero(2.5)
            assert len(suggerimenti_lunghi) > 0
            
            # Test con poco tempo libero
            suggerimenti_brevi = motore._suggerisci_uso_tempo_libero(0.5)
            assert len(suggerimenti_brevi) > 0
    
    def test_si_sovrappongono(self, app, user_profile):
        """Test verifica sovrapposizione attività"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            motore = MotoreAdattivo(profilo)
            
            ora_base = datetime.now()
            
            att1 = {
                'data_inizio': ora_base,
                'data_fine': ora_base + timedelta(hours=2)
            }
            
            att2 = {
                'data_inizio': ora_base + timedelta(hours=1),
                'data_fine': ora_base + timedelta(hours=3)
            }
            
            att3 = {
                'data_inizio': ora_base + timedelta(hours=3),
                'data_fine': ora_base + timedelta(hours=4)
            }
            
            # att1 e att2 si sovrappongono
            assert motore._si_sovrappongono(att1, att2) == True
            
            # att1 e att3 non si sovrappongono
            assert motore._si_sovrappongono(att1, att3) == False
    
    def test_adatta_piano(self, app, user_profile):
        """Test adattamento piano"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            motore = MotoreAdattivo(profilo)
            
            ora_base = datetime.now()
            
            piano_originale = [{
                'tipo': 'obiettivo',
                'nome': 'Studio',
                'data_inizio': ora_base + timedelta(hours=2),
                'data_fine': ora_base + timedelta(hours=4)
            }]
            
            nuovo_evento = {
                'tipo': 'impegno',
                'nome': 'Riunione',
                'data_inizio': ora_base + timedelta(hours=2, minutes=30),
                'data_fine': ora_base + timedelta(hours=3, minutes=30)
            }
            
            piano_adattato = motore.adatta_piano(piano_originale, nuovo_evento)
            
            assert isinstance(piano_adattato, list)
            assert len(piano_adattato) >= 1  # Almeno il nuovo evento
            
            # Verifica che nuovo evento sia presente
            eventi_impegno = [a for a in piano_adattato if a['tipo'] == 'impegno']
            assert len(eventi_impegno) == 1
    
    def test_genera_suggerimenti_energia_alta(self, app, user_profile):
        """Test suggerimenti con energia alta"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            motore = MotoreAdattivo(profilo)
            
            motore.stato_corrente['energia'] = 'alta'
            suggerimenti = motore._genera_suggerimenti()
            
            assert any('impegnative' in s or 'intensità' in s for s in suggerimenti)
    
    def test_genera_suggerimenti_stress_alto(self, app, user_profile):
        """Test suggerimenti con stress alto"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            motore = MotoreAdattivo(profilo)
            
            motore.stato_corrente['stress'] = 'alto'
            suggerimenti = motore._genera_suggerimenti()
            
            assert any('rilassarti' in s or 'pausa' in s or 'Riduci' in s for s in suggerimenti)
    
    def test_analizza_produttivita(self, app, user_profile):
        """Test analisi produttività"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            
            # Crea obiettivo con ore completate
            obiettivo = Obiettivo(
                user_id=profilo.id,
                nome='Test',
                tipo='studio',
                durata_settimanale=10.0,
                ore_completate=8.0
            )
            db.session.add(obiettivo)
            db.session.commit()
            
            motore = MotoreAdattivo(profilo)
            stats = motore.analizza_produttivita()
            
            assert 'obiettivi_totali' in stats
            assert 'ore_completate' in stats
            assert 'tasso_completamento' in stats
            assert 'insights' in stats
            
            assert stats['obiettivi_totali'] == 1
            assert stats['ore_completate'] == 8.0

