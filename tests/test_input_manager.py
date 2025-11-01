"""Test per InputManager"""
import pytest
from app.core.input_manager import InputManager


class TestInputManager:
    """Test suite per InputManager"""
    
    def test_riconosci_obiettivo_ore(self):
        """Test riconoscimento obiettivo con ore settimanali"""
        testo = "Voglio studiare Python 3 ore a settimana"
        risultato = InputManager.analizza_input(testo)
        
        assert risultato['tipo'] == 'obiettivo'
        assert risultato['dati']['nome'] == 'Python'
        assert risultato['dati']['durata_settimanale'] == 3.0
        assert risultato['dati']['tipo'] == 'studio'
    
    def test_riconosci_obiettivo_sport(self):
        """Test riconoscimento obiettivo sport"""
        testo = "Fare palestra 4 ore a settimana"
        risultato = InputManager.analizza_input(testo)
        
        assert risultato['tipo'] == 'obiettivo'
        assert risultato['dati']['tipo'] == 'sport'
        assert risultato['dati']['durata_settimanale'] == 4.0
    
    def test_riconosci_impegno_con_orari(self):
        """Test riconoscimento impegno con orari"""
        testo = "Domenica vado al mare dalle 16 alle 20"
        risultato = InputManager.analizza_input(testo)
        
        assert risultato['tipo'] == 'impegno'
        assert 'mare' in risultato['dati']['nome'].lower()
        assert risultato['dati']['ora_inizio'] == '16:00'
        assert risultato['dati']['ora_fine'] == '20:00'
        assert 'giorno' in risultato['dati']
    
    def test_riconosci_stato_emotivo(self):
        """Test riconoscimento stato emotivo"""
        testo = "Sono stanco"
        risultato = InputManager.analizza_input(testo)
        
        assert risultato['tipo'] == 'stato'
        assert risultato['dati']['stato'] == 'stanco'
        assert 'suggerimento' in risultato['dati']
    
    def test_riconosci_preferenza_riposo(self):
        """Test riconoscimento preferenza riposo"""
        testo = "Voglio riposare di più"
        risultato = InputManager.analizza_input(testo)
        
        assert risultato['tipo'] == 'preferenza'
        assert risultato['dati']['tipo_preferenza'] == 'riposo'
    
    def test_input_sconosciuto(self):
        """Test input non riconosciuto"""
        testo = "Ciao come stai?"
        risultato = InputManager.analizza_input(testo)
        
        assert risultato['tipo'] == 'sconosciuto'
    
    def test_identificazione_tipo_attivita(self):
        """Test identificazione corretta tipo attività"""
        assert InputManager._identifica_tipo_attivita('studiare matematica') == 'studio'
        assert InputManager._identifica_tipo_attivita('andare in palestra') == 'sport'
        assert InputManager._identifica_tipo_attivita('riunione lavoro') == 'lavoro'
        assert InputManager._identifica_tipo_attivita('leggere un libro') == 'personale'
    
    def test_suggerimenti_stato(self):
        """Test suggerimenti in base allo stato"""
        assert 'Ridurre' in InputManager._suggerisci_da_stato('stanco')
        assert 'Ridurre' in InputManager._suggerisci_da_stato('stressato')
        assert 'focus' in InputManager._suggerisci_da_stato('concentrato')
        assert 'impegnative' in InputManager._suggerisci_da_stato('rilassato')

