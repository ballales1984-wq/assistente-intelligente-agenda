"""Test per AgendaDinamica"""
import pytest
from datetime import datetime, time, timedelta
from app import create_app, db
from app.models import UserProfile, Obiettivo, Impegno
from app.core.agenda_dinamica import AgendaDinamica


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
        profilo = UserProfile(
            nome='Test User',
            stress_tollerato='medio',
            concentrazione='media',
            stile_vita='bilanciato',
            ora_inizio_giornata=time(8, 0),
            ora_fine_giornata=time(23, 0)
        )
        db.session.add(profilo)
        db.session.commit()
        return profilo


@pytest.fixture
def obiettivo_test(app, user_profile):
    """Crea obiettivo di test"""
    with app.app_context():
        obiettivo = Obiettivo(
            user_id=user_profile.id,
            nome='Studio Python',
            tipo='studio',
            durata_settimanale=3.0,
            intensita='media',
            attivo=True
        )
        db.session.add(obiettivo)
        db.session.commit()
        return obiettivo


class TestAgendaDinamica:
    """Test suite per AgendaDinamica"""
    
    def test_genera_piano_vuoto(self, app, user_profile):
        """Test generazione piano senza obiettivi"""
        with app.app_context():
            agenda = AgendaDinamica(user_profile)
            piano = agenda.genera_piano_settimanale()
            
            # Piano vuoto o solo pause
            assert isinstance(piano, list)
    
    def test_genera_piano_con_obiettivo(self, app, user_profile, obiettivo_test):
        """Test generazione piano con obiettivo"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            agenda = AgendaDinamica(profilo)
            piano = agenda.genera_piano_settimanale()
            
            assert isinstance(piano, list)
            assert len(piano) > 0
            
            # Verifica presenza attività legate all'obiettivo
            attivita_obiettivo = [a for a in piano if a.get('tipo') == 'obiettivo']
            assert len(attivita_obiettivo) > 0
    
    def test_calcola_slot_liberi(self, app, user_profile):
        """Test calcolo slot temporali liberi"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            agenda = AgendaDinamica(profilo)
            
            data = datetime.now()
            impegni = []
            
            slot = agenda._calcola_slot_liberi(data, impegni)
            
            assert isinstance(slot, list)
            assert len(slot) > 0
            # Dovrebbe esserci almeno uno slot libero
            assert 'inizio' in slot[0]
            assert 'fine' in slot[0]
    
    def test_orario_compatibile(self, app, user_profile):
        """Test compatibilità orari con preferenze"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            agenda = AgendaDinamica(profilo)
            
            # Test mattina
            assert agenda._orario_compatibile(9, 'mattina') == True
            assert agenda._orario_compatibile(15, 'mattina') == False
            
            # Test pomeriggio
            assert agenda._orario_compatibile(14, 'pomeriggio') == True
            assert agenda._orario_compatibile(9, 'pomeriggio') == False
            
            # Test sera
            assert agenda._orario_compatibile(20, 'sera') == True
            assert agenda._orario_compatibile(10, 'sera') == False
    
    def test_nome_giorno(self, app):
        """Test conversione numero giorno in nome"""
        with app.app_context():
            assert AgendaDinamica._nome_giorno(0) == 'lun'
            assert AgendaDinamica._nome_giorno(6) == 'dom'
    
    def test_aggiungi_pause(self, app, user_profile):
        """Test aggiunta pause intelligenti"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            agenda = AgendaDinamica(profilo)
            
            data = datetime.now()
            piano_base = [{
                'tipo': 'obiettivo',
                'nome': 'Studio',
                'data_inizio': data,
                'data_fine': data + timedelta(hours=2),
                'intensita': 'alta',
                'tipo_attivita': 'studio'
            }]
            
            piano_con_pause = agenda._aggiungi_pause(piano_base, data)
            
            # Dovrebbero esserci più elementi (attività + pause)
            assert len(piano_con_pause) >= len(piano_base)
    
    def test_piano_rispetta_orari_giornalieri(self, app, user_profile, obiettivo_test):
        """Test che il piano rispetti gli orari di inizio/fine giornata"""
        with app.app_context():
            profilo = UserProfile.query.get(user_profile.id)
            agenda = AgendaDinamica(profilo)
            piano = agenda.genera_piano_settimanale()
            
            for attivita in piano:
                ora_inizio = attivita['data_inizio'].time()
                ora_fine = attivita['data_fine'].time()
                
                # Verifica che le attività siano dentro l'orario lavorativo
                assert ora_inizio >= profilo.ora_inizio_giornata or attivita['tipo'] == 'pausa'
                assert ora_fine <= profilo.ora_fine_giornata or attivita['tipo'] == 'pausa'

