"""Manager per gestione diario e riflessioni"""
import re
from datetime import date, datetime
from typing import List, Dict, Any
from collections import Counter


class DiarioManager:
    """Gestisce il diario personale e l'estrazione di concetti"""
    
    # Parole da escludere (stop words italiane comuni)
    STOP_WORDS = {
        'il', 'lo', 'la', 'i', 'gli', 'le', 'un', 'uno', 'una',
        'di', 'a', 'da', 'in', 'con', 'su', 'per', 'tra', 'fra',
        'e', 'o', 'che', 'ma', 'se', 'ho', 'hai', 'ha', 'hanno',
        'sono', 'sei', 'è', 'siamo', 'siete', 'mi', 'ti', 'si',
        'ci', 'vi', 'me', 'te', 'lui', 'lei', 'noi', 'voi', 'loro',
        'mio', 'tuo', 'suo', 'nostro', 'vostro', 'loro',
        'questo', 'quello', 'questi', 'quelli', 'questa', 'quella',
        'anche', 'oggi', 'ieri', 'domani', 'poi', 'dopo', 'prima',
        'molto', 'tanto', 'poco', 'più', 'meno', 'troppo', 'così',
        'magari', 'forse', 'probabilmente', 'sicuramente',
        'con', 'gli', 'amici', 'alle', 'dalle', 'alla', 'alla',
        'se', 'riesco', 'quando', 'dove', 'come', 'perché'
    }
    
    # Pattern per riconoscere elementi significativi
    PATTERNS = {
        'persona': r'\b([A-Z][a-z]+)\b',  # Nome proprio
        'argomento': r'\b([a-z]{4,})\b',   # Parola significativa (min 4 lettere)
        'emozione': r'\b(felice|triste|arrabbiato|motivato|stanco|entusiasta|annoiato|preoccupato|sereno|ansioso)\b',
    }
    
    @staticmethod
    def analizza_testo(testo: str) -> Dict[str, Any]:
        """
        Analizza un testo di diario ed estrae informazioni chiave
        
        Args:
            testo: Testo del diario
            
        Returns:
            Dizionario con riflessioni, parole chiave, sentiment
        """
        # Pulisci il testo
        testo_pulito = DiarioManager._pulisci_testo(testo)
        
        # Estrai concetti
        persone = DiarioManager._estrai_persone(testo)
        parole_chiave = DiarioManager._estrai_parole_chiave(testo_pulito)
        emozioni = DiarioManager._estrai_emozioni(testo)
        
        # Costruisci riflessioni strutturate
        riflessioni = []
        
        if persone:
            riflessioni.append({
                'tipo': 'persone',
                'valori': persone
            })
        
        if emozioni:
            riflessioni.append({
                'tipo': 'emozioni',
                'valori': emozioni
            })
        
        if parole_chiave:
            riflessioni.append({
                'tipo': 'argomenti',
                'valori': parole_chiave[:10]  # Top 10
            })
        
        # Determina sentiment generale
        sentiment = DiarioManager._calcola_sentiment(emozioni)
        
        return {
            'riflessioni': riflessioni,
            'parole_chiave': parole_chiave[:15],  # Top 15
            'sentiment': sentiment
        }
    
    @staticmethod
    def _pulisci_testo(testo: str) -> str:
        """Pulisce il testo da punteggiatura e caratteri speciali"""
        # Rimuovi punteggiatura ma mantieni spazi
        testo = re.sub(r'[^\w\s]', ' ', testo.lower())
        # Rimuovi spazi multipli
        testo = re.sub(r'\s+', ' ', testo)
        return testo.strip()
    
    @staticmethod
    def _estrai_persone(testo: str) -> List[str]:
        """Estrae nomi propri (persone) dal testo"""
        # Cerca parole che iniziano con maiuscola (probabilmente nomi)
        pattern = re.compile(DiarioManager.PATTERNS['persona'])
        persone = pattern.findall(testo)
        
        # Rimuovi duplicati mantenendo l'ordine
        persone_uniche = []
        seen = set()
        for persona in persone:
            if persona not in seen and persona not in {'Lunedì', 'Martedì', 'Mercoledì', 
                                                        'Giovedì', 'Venerdì', 'Sabato', 'Domenica'}:
                persone_uniche.append(persona)
                seen.add(persona)
        
        return persone_uniche
    
    @staticmethod
    def _estrai_parole_chiave(testo_pulito: str) -> List[str]:
        """Estrae parole chiave significative dal testo"""
        parole = testo_pulito.split()
        
        # Filtra stop words e parole corte
        parole_filtrate = [
            p for p in parole 
            if p not in DiarioManager.STOP_WORDS 
            and len(p) >= 4
            and not p.isdigit()
        ]
        
        # Conta frequenze
        counter = Counter(parole_filtrate)
        
        # Ritorna parole più frequenti
        return [parola for parola, _ in counter.most_common(15)]
    
    @staticmethod
    def _estrai_emozioni(testo: str) -> List[str]:
        """Estrae emozioni espresse nel testo"""
        testo_lower = testo.lower()
        pattern = re.compile(DiarioManager.PATTERNS['emozione'])
        emozioni = pattern.findall(testo_lower)
        
        # Rimuovi duplicati
        return list(set(emozioni))
    
    @staticmethod
    def _calcola_sentiment(emozioni: List[str]) -> str:
        """Calcola il sentiment generale basato sulle emozioni"""
        if not emozioni:
            return 'neutro'
        
        emozioni_positive = {'felice', 'motivato', 'entusiasta', 'sereno'}
        emozioni_negative = {'triste', 'arrabbiato', 'stanco', 'annoiato', 'preoccupato', 'ansioso'}
        
        score_positivo = sum(1 for e in emozioni if e in emozioni_positive)
        score_negativo = sum(1 for e in emozioni if e in emozioni_negative)
        
        if score_positivo > score_negativo:
            return 'positivo'
        elif score_negativo > score_positivo:
            return 'negativo'
        else:
            return 'neutro'
    
    @staticmethod
    def distingui_agenda_vs_diario(testo: str) -> str:
        """
        Determina se il testo è un impegno agenda o una riflessione diario
        
        Args:
            testo: Testo da analizzare
            
        Returns:
            'agenda' o 'diario'
        """
        testo_lower = testo.lower()
        
        # Pattern tipici dell'agenda
        pattern_agenda = [
            r'\b(lunedì|martedì|mercoledì|giovedì|venerdì|sabato|domenica)\b',
            r'\b\d{1,2}:\d{2}\b',  # Orari
            r'\b(dalle|alle|dal|al)\b',
            r'\b(studio|lavoro|riunione|appuntamento|palestra)\b',
            r'\b\d+\s*ore?\b'  # "3 ore"
        ]
        
        # Pattern tipici del diario
        pattern_diario = [
            r'\b(ho|sono|mi sento|oggi|ieri)\b',
            r'\b(parlato|capito|pensato|sentito|visto)\b',
            r'\b(con|insieme|mentre|quando|dopo che)\b',
            r'\b[A-Z][a-z]+\b',  # Nomi propri (persone)
        ]
        
        score_agenda = sum(1 for p in pattern_agenda if re.search(p, testo_lower))
        score_diario = sum(1 for p in pattern_diario if re.search(p, testo_lower))
        
        # Se ha orari specifici, è molto probabilmente agenda
        if re.search(r'\b\d{1,2}:\d{2}\b', testo_lower):
            score_agenda += 3
        
        # Se menziona persone e riflessioni, è probabilmente diario
        if re.search(r'\b(ho capito|ho imparato|mi ha detto|abbiamo parlato)\b', testo_lower):
            score_diario += 3
        
        return 'agenda' if score_agenda > score_diario else 'diario'
    
    @staticmethod
    def estrai_data_da_testo(testo: str) -> date:
        """
        Estrae la data dal testo o ritorna oggi
        
        Args:
            testo: Testo contenente possibile riferimento temporale
            
        Returns:
            Data estratta o data odierna
        """
        from datetime import timedelta
        
        testo_lower = testo.lower()
        oggi = date.today()
        
        # Ieri
        if 'ieri' in testo_lower:
            return oggi - timedelta(days=1)
        
        # Domani
        if 'domani' in testo_lower:
            return oggi + timedelta(days=1)
        
        # Giorni della settimana
        giorni = {
            'lunedì': 0, 'martedì': 1, 'mercoledì': 2, 'giovedì': 3,
            'venerdì': 4, 'sabato': 5, 'domenica': 6
        }
        
        for giorno_nome, giorno_num in giorni.items():
            if giorno_nome in testo_lower:
                # Calcola prossima occorrenza del giorno
                giorni_avanti = (giorno_num - oggi.weekday()) % 7
                if giorni_avanti == 0:
                    giorni_avanti = 7  # Settimana prossima
                return oggi + timedelta(days=giorni_avanti)
        
        # Default: oggi
        return oggi

