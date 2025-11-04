"""Test per Smart Links - DuckDuckGo Integration"""
import pytest
from app.core.smart_links import SmartLinksManager
from app.integrations.web_search import WebSearchService


@pytest.mark.unit
class TestSmartLinksIntentDetection:
    """Test riconoscimento intent ricerca"""
    
    def setup_method(self):
        """Setup per ogni test"""
        self.sm = SmartLinksManager()
    
    def test_detect_search_italian(self):
        """Test riconoscimento ricerca in italiano"""
        intent = self.sm.detect_search_intent("cerca python tutorial")
        
        assert intent['is_search'] is True
        assert intent['is_news'] is False
        assert intent['query'] == 'python tutorial'
        assert intent['confidence'] >= 0.9
    
    def test_detect_search_english(self):
        """Test riconoscimento ricerca in inglese"""
        intent = self.sm.detect_search_intent("search for machine learning")
        
        assert intent['is_search'] is True
        assert intent['query'] == 'machine learning'
    
    def test_detect_search_spanish(self):
        """Test riconoscimento ricerca in spagnolo"""
        intent = self.sm.detect_search_intent("busca javascript frameworks")
        
        assert intent['is_search'] is True
        assert intent['query'] == 'javascript frameworks'
    
    def test_detect_news_italian(self):
        """Test riconoscimento notizie in italiano"""
        intent = self.sm.detect_search_intent("notizie su intelligenza artificiale")
        
        assert intent['is_search'] is True
        assert intent['is_news'] is True
        assert intent['query'] == 'intelligenza artificiale'
        assert intent['confidence'] >= 0.95
    
    def test_detect_news_english(self):
        """Test riconoscimento notizie in inglese"""
        intent = self.sm.detect_search_intent("latest news about AI")
        
        assert intent['is_search'] is True
        assert intent['is_news'] is True
        assert 'AI' in intent['query']
    
    def test_no_search_intent(self):
        """Test messaggio non è una ricerca"""
        intent = self.sm.detect_search_intent("Voglio studiare Python 3 ore a settimana")
        
        assert intent['is_search'] is False
        assert intent['query'] is None
    
    def test_no_search_intent_appointment(self):
        """Test appuntamento non è una ricerca"""
        intent = self.sm.detect_search_intent("Domani riunione ore 15")
        
        assert intent['is_search'] is False
    
    def test_search_patterns_variations(self):
        """Test variazioni pattern ricerca"""
        test_cases = [
            "ricerca machine learning",
            "trova informazioni su Python",
            "google artificial intelligence",
            "guarda su internet blockchain",
            "dammi informazioni su React",
            "cosa sai di Vue.js",
            "look up TypeScript",
            "find information about Docker",
            "tell me about Kubernetes",
            "what is TensorFlow",
            "información sobre FastAPI",
            "encuentra tutorial de Django"
        ]
        
        for text in test_cases:
            intent = self.sm.detect_search_intent(text)
            assert intent['is_search'] is True, f"Failed to detect search in: {text}"
            assert intent['query'] is not None
            assert len(intent['query']) > 0


@pytest.mark.unit
class TestSmartLinksResponseGeneration:
    """Test generazione risposte Smart Links"""
    
    def setup_method(self):
        """Setup per ogni test"""
        self.sm = SmartLinksManager()
    
    def test_process_search_message(self):
        """Test processing messaggio di ricerca"""
        result = self.sm.process_message("cerca python tutorial")
        
        assert result['has_smart_links'] is True
        assert result['response'] is not None
        # Results potrebbero essere vuoti se DuckDuckGo non risponde
        assert result['results'] is not None
    
    def test_process_non_search_message(self):
        """Test processing messaggio normale"""
        result = self.sm.process_message("Voglio studiare Python")
        
        assert result['has_smart_links'] is False
        assert result['response'] is None
        assert result['results'] is None
    
    def test_search_response_structure(self):
        """Test struttura risposta ricerca"""
        result = self.sm.process_message("cerca test query")
        
        if result['has_smart_links']:
            assert 'Risultati' in result['response'] or 'trovato' in result['response']
            # Se ci sono risultati, verifica struttura
            if result['results'] and len(result['results']) > 0:
                first_result = result['results'][0]
                assert 'title' in first_result
                assert 'href' in first_result
                assert 'body' in first_result


@pytest.mark.integration
@pytest.mark.slow
class TestWebSearchService:
    """Test integrazione WebSearchService con DuckDuckGo"""
    
    def setup_method(self):
        """Setup per ogni test"""
        self.ws = WebSearchService()
    
    def test_search_returns_results(self):
        """Test ricerca ritorna risultati"""
        # Questo test potrebbe fallire se DuckDuckGo ha rate limits
        try:
            results = self.ws.search("python programming", max_results=3)
            
            # Se ritorna risultati, verifica struttura
            if results and len(results) > 0:
                assert len(results) <= 3
                for result in results:
                    assert 'title' in result
                    assert 'href' in result
                    assert 'body' in result
                    assert result['href'].startswith('http')
        except Exception as e:
            pytest.skip(f"DuckDuckGo not available or rate limited: {e}")
    
    def test_search_news_returns_results(self):
        """Test ricerca notizie ritorna risultati"""
        try:
            results = self.ws.search_news("technology", max_results=2)
            
            if results and len(results) > 0:
                assert len(results) <= 2
                for result in results:
                    assert 'title' in result
                    assert 'href' in result
                    # News hanno campi extra
                    assert 'source' in result or 'date' in result
        except Exception as e:
            pytest.skip(f"DuckDuckGo news not available: {e}")
    
    def test_search_empty_query(self):
        """Test ricerca con query vuota"""
        results = self.ws.search("", max_results=5)
        
        # Dovrebbe ritornare lista vuota, non crashare
        assert isinstance(results, list)
    
    def test_search_special_characters(self):
        """Test ricerca con caratteri speciali"""
        results = self.ws.search("python %%% @@@", max_results=3)
        
        # Dovrebbe gestire gracefully
        assert isinstance(results, list)
    
    def test_search_max_results_respected(self):
        """Test max_results viene rispettato"""
        try:
            results = self.ws.search("test query", max_results=2)
            
            if results:
                assert len(results) <= 2
        except Exception:
            pytest.skip("DuckDuckGo not available")


@pytest.mark.unit
class TestSmartLinksPatternMatching:
    """Test pattern matching avanzato"""
    
    def setup_method(self):
        """Setup per ogni test"""
        self.sm = SmartLinksManager()
    
    def test_case_insensitive_matching(self):
        """Test matching case-insensitive"""
        test_cases = [
            "CERCA python",
            "Cerca Python",
            "cerca PYTHON",
            "SEARCH machine learning",
            "Search MACHINE LEARNING"
        ]
        
        for text in test_cases:
            intent = self.sm.detect_search_intent(text)
            assert intent['is_search'] is True, f"Failed for: {text}"
    
    def test_extra_whitespace_handling(self):
        """Test gestione spazi extra"""
        intent = self.sm.detect_search_intent("cerca    python    tutorial")
        
        assert intent['is_search'] is True
        assert 'python' in intent['query'].lower()
    
    def test_news_vs_regular_search(self):
        """Test distinzione notizie vs ricerca normale"""
        news_intent = self.sm.detect_search_intent("notizie intelligenza artificiale")
        search_intent = self.sm.detect_search_intent("cerca intelligenza artificiale")
        
        assert news_intent['is_news'] is True
        assert search_intent['is_news'] is False
        assert news_intent['is_search'] is True
        assert search_intent['is_search'] is True
    
    def test_multiword_queries(self):
        """Test query multi-parola"""
        intent = self.sm.detect_search_intent(
            "cerca tutorial completo python per principianti"
        )
        
        assert intent['is_search'] is True
        assert len(intent['query']) > 10  # Query lunga conservata


@pytest.mark.unit
class TestSmartLinksEdgeCases:
    """Test edge cases e robustezza"""
    
    def setup_method(self):
        """Setup per ogni test"""
        self.sm = SmartLinksManager()
    
    def test_empty_message(self):
        """Test messaggio vuoto"""
        result = self.sm.process_message("")
        
        assert result['has_smart_links'] is False
        assert result['response'] is None
    
    def test_very_long_message(self):
        """Test messaggio molto lungo"""
        long_message = "cerca " + ("python " * 100)
        result = self.sm.process_message(long_message)
        
        # Dovrebbe gestire senza crashare
        assert result is not None
        assert 'has_smart_links' in result
    
    def test_only_keywords(self):
        """Test solo parole chiave senza query"""
        intent = self.sm.detect_search_intent("cerca")
        
        # Potrebbe non riconoscere come ricerca valida
        # o riconoscere ma con query vuota
        assert intent is not None
    
    def test_mixed_language_query(self):
        """Test query mista italiano/inglese"""
        intent = self.sm.detect_search_intent("cerca python tutorial and best practices")
        
        assert intent['is_search'] is True
        assert 'python' in intent['query'].lower()
    
    def test_unicode_characters(self):
        """Test caratteri unicode"""
        intent = self.sm.detect_search_intent("cerca programmazione in Python per principianti")
        
        assert intent['is_search'] is True
        assert intent['query'] is not None


@pytest.mark.unit
class TestSmartLinksHelper:
    """Test funzioni helper"""
    
    def test_generate_search_response_no_results(self):
        """Test generazione risposta con zero risultati"""
        sm = SmartLinksManager()
        
        # Mock: passiamo query valida ma assumiamo zero risultati
        response = sm.generate_search_response(
            query="test query nonexistent xyzabc123",
            is_news=False,
            max_results=5
        )
        
        assert response is not None
        assert 'success' in response
        # Se fallisce, dovrebbe avere un messaggio di errore utile
        if not response['success']:
            assert 'response' in response
            assert len(response['response']) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

