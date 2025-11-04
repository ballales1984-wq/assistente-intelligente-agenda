"""Test per API Endpoints"""
import pytest
import json
from app.models import UserProfile, Obiettivo, Impegno, Spesa, DiarioGiornaliero


@pytest.mark.api
class TestChatEndpoint:
    """Test /api/chat endpoint"""
    
    def test_chat_obiettivo(self, client, session):
        """Test creazione obiettivo via chat"""
        response = client.post('/api/chat', 
            data=json.dumps({
                'messaggio': 'Voglio studiare Python 3 ore a settimana'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['tipo_riconosciuto'] == 'obiettivo'
        assert 'Python' in data['risposta']
        assert data['dati'] is not None
    
    def test_chat_impegno(self, client, session):
        """Test creazione impegno via chat"""
        response = client.post('/api/chat',
            data=json.dumps({
                'messaggio': 'Domani riunione ore 15'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['tipo_riconosciuto'] == 'impegno'
        assert 'riunione' in data['risposta'].lower()
    
    def test_chat_spesa(self, client, session):
        """Test registrazione spesa via chat"""
        response = client.post('/api/chat',
            data=json.dumps({
                'messaggio': 'Speso 25 euro per pranzo'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['tipo_riconosciuto'] == 'spesa'
        assert '25' in data['risposta']
    
    def test_chat_messaggio_vuoto(self, client):
        """Test messaggio vuoto ritorna errore"""
        response = client.post('/api/chat',
            data=json.dumps({'messaggio': ''}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'errore' in data
    
    def test_chat_senza_json(self, client):
        """Test senza Content-Type: application/json"""
        response = client.post('/api/chat',
            data='Voglio studiare Python'
        )
        
        # Dovrebbe gestire gracefully
        assert response.status_code in [200, 400, 415]


@pytest.mark.api
class TestObiettiviEndpoints:
    """Test endpoints obiettivi"""
    
    def test_get_obiettivi(self, client, session):
        """Test GET /api/obiettivi"""
        # Crea profilo e obiettivo di test
        profilo = UserProfile(nome='Test User')
        session.add(profilo)
        session.commit()
        
        obiettivo = Obiettivo(
            user_id=profilo.id,
            nome='Python',
            tipo='studio',
            durata_settimanale=3.0
        )
        session.add(obiettivo)
        session.commit()
        
        response = client.get('/api/obiettivi')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) > 0
        assert data[0]['nome'] == 'Python'
    
    def test_delete_obiettivo(self, client, session):
        """Test DELETE /api/obiettivi/<id>"""
        profilo = UserProfile(nome='Test User')
        session.add(profilo)
        session.commit()
        
        obiettivo = Obiettivo(
            user_id=profilo.id,
            nome='Test Goal',
            tipo='studio',
            durata_settimanale=2.0
        )
        session.add(obiettivo)
        session.commit()
        
        response = client.delete(f'/api/obiettivi/{obiettivo.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True


@pytest.mark.api
class TestImpegniEndpoints:
    """Test endpoints impegni"""
    
    def test_get_impegni(self, client, session):
        """Test GET /api/impegni"""
        profilo = UserProfile(nome='Test User')
        session.add(profilo)
        session.commit()
        
        response = client.get('/api/impegni')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_get_impegni_oggi(self, client, session):
        """Test GET /api/impegni/oggi"""
        response = client.get('/api/impegni/oggi')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)


@pytest.mark.api
class TestSpeseEndpoints:
    """Test endpoints spese"""
    
    def test_get_spese_oggi(self, client, session):
        """Test GET /api/spese/oggi"""
        profilo = UserProfile(nome='Test User')
        session.add(profilo)
        session.commit()
        
        response = client.get('/api/spese/oggi')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_get_spese_settimana(self, client, session):
        """Test GET /api/spese/settimana"""
        response = client.get('/api/spese/settimana')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'totale' in data
        assert 'spese' in data


@pytest.mark.api
class TestDiarioEndpoints:
    """Test endpoints diario"""
    
    def test_get_diario(self, client, session):
        """Test GET /api/diario"""
        profilo = UserProfile(nome='Test User')
        session.add(profilo)
        session.commit()
        
        response = client.get('/api/diario')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_share_diario(self, client, session):
        """Test POST /api/diario/<id>/share"""
        profilo = UserProfile(nome='Test User')
        session.add(profilo)
        session.commit()
        
        entry = DiarioGiornaliero(
            user_id=profilo.id,
            testo='Test entry',
            sentiment='neutral'
        )
        session.add(entry)
        session.commit()
        
        response = client.post(f'/api/diario/{entry.id}/share')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'share_url' in data or 'success' in data


@pytest.mark.api
class TestStatisticheEndpoints:
    """Test endpoints statistiche"""
    
    def test_get_statistiche(self, client, session):
        """Test GET /api/statistiche"""
        profilo = UserProfile(nome='Test User')
        session.add(profilo)
        session.commit()
        
        response = client.get('/api/statistiche')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'obiettivi_attivi' in data or 'totale_obiettivi' in data


@pytest.mark.api
class TestExportEndpoints:
    """Test endpoints export"""
    
    def test_export_icalendar(self, client, session):
        """Test GET /api/export/icalendar"""
        profilo = UserProfile(nome='Test User')
        session.add(profilo)
        session.commit()
        
        response = client.get('/api/export/icalendar')
        
        assert response.status_code == 200
        # Verifica che sia un file .ics
        assert response.headers['Content-Type'] == 'text/calendar'
    
    def test_export_spese_csv(self, client, session):
        """Test GET /api/export/spese/csv"""
        profilo = UserProfile(nome='Test User')
        session.add(profilo)
        session.commit()
        
        response = client.get('/api/export/spese/csv')
        
        assert response.status_code == 200
        assert 'text/csv' in response.headers['Content-Type']
    
    def test_export_tutti_json(self, client, session):
        """Test GET /api/export/tutti"""
        profilo = UserProfile(nome='Test User')
        session.add(profilo)
        session.commit()
        
        response = client.get('/api/export/tutti')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'obiettivi' in data
        assert 'impegni' in data
        assert 'spese' in data


@pytest.mark.api
@pytest.mark.slow
class TestSmartLinksIntegration:
    """Test Smart Links integration in chat"""
    
    def test_smart_links_search_intent(self, client, session):
        """Test riconoscimento intent ricerca"""
        profilo = UserProfile(nome='Test User')
        session.add(profilo)
        session.commit()
        
        response = client.post('/api/chat',
            data=json.dumps({
                'messaggio': 'cerca python programming'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        # Dovrebbe riconoscere come web_search
        assert data['tipo_riconosciuto'] == 'web_search'
        assert 'smart_links' in data
        assert data['smart_links'] is True
    
    def test_smart_links_news_intent(self, client, session):
        """Test riconoscimento intent notizie"""
        profilo = UserProfile(nome='Test User')
        session.add(profilo)
        session.commit()
        
        response = client.post('/api/chat',
            data=json.dumps({
                'messaggio': 'notizie intelligenza artificiale'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['tipo_riconosciuto'] == 'web_search'
        assert 'smart_links' in data


@pytest.mark.api
class TestCommunityEndpoints:
    """Test community endpoints"""
    
    def test_get_reflections(self, client, session):
        """Test GET /api/community/reflections"""
        profilo = UserProfile(nome='Test User')
        session.add(profilo)
        session.commit()
        
        response = client.get('/api/community/reflections?language=it&limit=10')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'success' in data or isinstance(data, dict)
    
    def test_create_reflection(self, client, session):
        """Test POST /api/community/reflections"""
        profilo = UserProfile(nome='Test User')
        session.add(profilo)
        session.commit()
        
        response = client.post('/api/community/reflections',
            data=json.dumps({
                'text': 'This is a test reflection with enough characters to pass validation',
                'visibility': 'public',
                'category': 'personal_growth',
                'language': 'en'
            }),
            content_type='application/json'
        )
        
        # Può essere 200 o 201
        assert response.status_code in [200, 201]
        data = response.get_json()
        assert 'success' in data or 'error' in data


@pytest.mark.api
class TestErrorHandling:
    """Test gestione errori API"""
    
    def test_404_non_existent_endpoint(self, client):
        """Test 404 per endpoint inesistente"""
        response = client.get('/api/nonexistent')
        
        assert response.status_code == 404
    
    def test_405_method_not_allowed(self, client):
        """Test 405 per metodo HTTP non permesso"""
        response = client.put('/api/chat')
        
        assert response.status_code == 405
    
    def test_malformed_json(self, client):
        """Test JSON malformato"""
        response = client.post('/api/chat',
            data='{"messaggio": invalid json}',
            content_type='application/json'
        )
        
        # Dovrebbe gestire l'errore gracefully
        assert response.status_code in [400, 500]


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

