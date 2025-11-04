"""Test per NLP Parser (Input Manager)"""
import pytest
from app.core.input_manager import InputManager


class TestObiettiviParsing:
    """Test parsing obiettivi"""
    
    def test_obiettivo_con_ore_settimanali(self):
        """Test: 'Voglio studiare Python 3 ore a settimana'"""
        result = InputManager.analizza_input("Voglio studiare Python 3 ore a settimana")
        
        assert result['tipo'] == 'obiettivo'
        assert 'Python' in result['dati']['nome']
        assert result['dati']['durata_settimanale'] == 3.0
    
    def test_obiettivo_imparare(self):
        """Test: 'Voglio imparare inglese 5 ore a settimana'"""
        result = InputManager.analizza_input("Voglio imparare inglese 5 ore a settimana")
        
        assert result['tipo'] == 'obiettivo'
        assert 'inglese' in result['dati']['nome'].lower()
        assert result['dati']['durata_settimanale'] == 5.0
    
    def test_obiettivo_allenarsi(self):
        """Test: 'Voglio allenarmi in palestra 4 ore a settimana'"""
        result = InputManager.analizza_input("Voglio allenarmi in palestra 4 ore a settimana")
        
        assert result['tipo'] == 'obiettivo'
        assert result['dati']['durata_settimanale'] == 4.0


class TestImpegniParsing:
    """Test parsing impegni"""
    
    def test_impegno_oggi_con_orario(self):
        """Test: 'Oggi riunione ore 15'"""
        result = InputManager.analizza_input("Oggi riunione ore 15")
        
        assert result['tipo'] == 'impegno'
        assert 'Riunione' in result['dati']['nome']
        assert '15:00' in result['dati']['ora_inizio']
    
    def test_impegno_domani(self):
        """Test: 'Domani palestra ore 18'"""
        result = InputManager.analizza_input("Domani palestra ore 18")
        
        assert result['tipo'] == 'impegno'
        assert 'Palestra' in result['dati']['nome']
        assert 'domani' in result['dati']['giorno']
    
    def test_impegno_con_range_orario(self):
        """Test: 'Lunedì riunione dalle 10 alle 12'"""
        result = InputManager.analizza_input("Lunedì riunione dalle 10 alle 12")
        
        assert result['tipo'] in ['impegno', 'impegno_ricorrente']
        assert 'riunione' in result['dati']['nome'].lower()
    
    def test_impegno_ricorrente(self):
        """Test: 'Ogni lunedì palestra ore 18'"""
        result = InputManager.analizza_input("Ogni lunedì palestra ore 18")
        
        assert result['tipo'] == 'impegno_ricorrente'
        assert 'Palestra' in result['dati']['nome']
        assert '18:00' in result['dati']['ora_inizio']


class TestDiarioParsing:
    """Test parsing diario"""
    
    def test_riflessione_lunga(self):
        """Test riflessione diario con testo lungo"""
        testo = "Oggi mi sento molto motivato dopo aver completato il progetto. Ho imparato tanto su Python e Flask."
        result = InputManager.analizza_input(testo)
        
        assert result['tipo'] == 'diario'
        assert 'sentiment' in result['dati']
        assert result['dati']['testo'] == testo
    
    def test_sentiment_positivo(self):
        """Test sentiment positivo"""
        result = InputManager.analizza_input("Oggi sono felice perché ho raggiunto il mio obiettivo")
        
        assert result['tipo'] == 'diario'
        # Sentiment può essere string o dict
        assert 'sentiment' in result['dati']


class TestSpeseParsing:
    """Test parsing spese"""
    
    def test_spesa_con_importo_euro(self):
        """Test: 'Speso 15 euro per pranzo'"""
        result = InputManager.analizza_input("Speso 15 euro per pranzo")
        
        assert result['tipo'] == 'spesa'
        assert result['dati']['importo'] == 15.0
        assert 'pranzo' in result['dati']['descrizione'].lower()
    
    def test_spesa_formato_breve(self):
        """Test: '25€ benzina'"""
        result = InputManager.analizza_input("25€ benzina")
        
        assert result['tipo'] == 'spesa'
        assert result['dati']['importo'] == 25.0
    
    def test_spesa_con_virgola(self):
        """Test: 'Comprato libro 12.50 euro' (punto invece di virgola)"""
        result = InputManager.analizza_input("Comprato libro 12.50 euro")
        
        assert result['tipo'] == 'spesa'
        assert result['dati']['importo'] == 12.50


class TestFallbackIntelligente:
    """Test fallback per input strani"""
    
    def test_input_vuoto(self):
        """Test input vuoto"""
        result = InputManager.analizza_input("")
        
        assert result['tipo'] in ['aiuto', 'sconosciuto']
        # Almeno ritorna qualcosa senza crashare
        assert result is not None
    
    def test_input_troppo_corto(self):
        """Test input troppo corto"""
        result = InputManager.analizza_input("x")
        
        assert result['tipo'] in ['aiuto', 'sconosciuto']
        # Non deve crashare
        assert result is not None
    
    def test_input_non_riconosciuto(self):
        """Test input non riconosciuto"""
        result = InputManager.analizza_input("asdasdasd qweqweqwe")
        
        assert result['tipo'] in ['sconosciuto', 'errore', 'aiuto']
        # Non deve crashare
        assert result is not None
    
    def test_input_con_errore(self):
        """Test che input strani non crashano"""
        inputs_strani = [
            "123!@#$%^&*()",
            "ñçéà",
            "a" * 1000,  # Input molto lungo
        ]
        
        for inp in inputs_strani:
            result = InputManager.analizza_input(inp)
            # Non deve crashare, deve ritornare qualcosa
            assert result is not None
            assert 'tipo' in result


class TestRichiestaAiuto:
    """Test richiesta aiuto"""
    
    def test_aiuto_esplicito(self):
        """Test: 'aiuto'"""
        result = InputManager.analizza_input("aiuto")
        
        assert result['tipo'] == 'aiuto'
        assert 'suggerimenti' in result['dati']
    
    def test_come_faccio(self):
        """Test: 'come faccio a...'"""
        result = InputManager.analizza_input("come faccio a creare un obiettivo")
        
        assert result['tipo'] == 'aiuto'


@pytest.mark.unit
class TestIdentificazioneTipoAttivita:
    """Test identificazione tipo attività"""
    
    def test_attivita_studio(self):
        """Test identificazione attività di studio"""
        tipo = InputManager._identifica_tipo_attivita("studiare Python")
        assert tipo == 'studio'
    
    def test_attivita_fitness(self):
        """Test identificazione attività fitness"""
        tipo = InputManager._identifica_tipo_attivita("allenarmi in palestra")
        assert tipo in ['fitness', 'sport']  # Può essere sia fitness che sport
    
    def test_attivita_lavoro(self):
        """Test identificazione attività lavoro"""
        tipo = InputManager._identifica_tipo_attivita("lavorare al progetto")
        assert tipo == 'lavoro'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

