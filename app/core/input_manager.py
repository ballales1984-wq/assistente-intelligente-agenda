"""Manager per l'analisi dell'input testuale"""
import re
from datetime import datetime, timedelta, date
from typing import Dict, Any, Optional
from app.core.diario_manager import DiarioManager


class InputManager:
    """Gestisce e analizza l'input testuale dell'utente"""
    
    # Pattern per riconoscere intenzioni comuni (migliorati!)
    PATTERNS = {
        'obiettivo_ore': r'(?:studiare|fare|dedicare|imparare|allenarmi|esercitarmi|lavorare su|praticare)\s+(.+?)\s+(\d+)\s*(?:ore?|h)\s*(?:a|alla|per|ogni|alla|al)?\s*settimana',
        'obiettivo_durata': r'(?:voglio|devo|vorrei|mi piacerebbe)\s+(.+?)\s+per\s+(\d+)\s*(?:giorni|settimane|mesi)',
        'impegno_specifico': r'(.+?)\s+(?:dalle|dal|alle|al|dalle\s+ore|alle\s+ore)\s+(\d{1,2}):?(\d{2})?\s*(?:alle|al|-|–)?\s*(\d{1,2})?:?(\d{2})?',
        'impegno_oggi_domani': r'(?:oggi|domani)\s+(.+?)\s+(?:alle|dalle|al|\s)(\d{1,2}):?(\d{2})?(?:\s*-\s*(\d{1,2}):?(\d{2})?)?',
        'impegno_ricorrente': r'ogni\s+(luned[ìi]|marted[ìi]|mercoled[ìi]|gioved[ìi]|venerd[ìi]|sabato|domenica|giorno)\s+(.+?)\s+(?:ore|alle|dalle)\s+(\d{1,2})',
        'stato_emotivo': r'(?:sono|mi sento|sto|mi trovo)\s+(stanco|stanca|concentrato|concentrata|rilassato|rilassata|stressato|stressata|motivato|motivata|energico|energica|esausto|esausta)',
        'preferenza_riposo': r'(?:voglio|preferisco|vorrei|ho bisogno di)\s+(?:riposare|rilassarmi|pause|più pause|pause più lunghe|dormire di più)',
        'giorno_settimana': r'(luned[ìi]|marted[ìi]|mercoled[ìi]|gioved[ìi]|venerd[ìi]|sabato|domenica|oggi|domani)',
        'completamento': r'(?:ho finito|ho completato|finito|completato|fatto)\s+(.+)',
        'modifica_piano': r'(?:sposta|cambia|modifica|rimuovi|elimina)\s+(.+)',
        'richiesta_aiuto': r'(?:aiutami|aiuto|come faccio|suggeriscimi|consigliami)',
        'tempo_disponibile': r'(?:ho|dispongo di)\s+(\d+)\s*(?:ore?|h|minuti|min)\s+(?:libere?|liberi|disponibili)',
        'spesa': r'(?:spesa|speso|pagato|costo|ho speso|comprato|comprata|preso)\s+(\d+(?:[.,]\d+)?)\s*(?:euro?|€|eur)?\s*(?:per|di)?\s*([^.!?\n]{1,100})',
        'spesa_diretta': r'(\d+(?:[.,]\d+)?)\s*(?:euro?|€|eur)\s+(?:per|di|per|di|in)?\s+([^.!?\n]{1,100})',
        'spesa_solo_importo': r'^(\d+(?:[.,]\d+)?)\s*(?:euro?|€|eur)\s+(.+)',
    }
    
    @staticmethod
    def analizza_input(testo: str) -> Dict[str, Any]:
        """
        Analizza l'input testuale e estrae informazioni strutturate
        
        Args:
            testo: Input testuale dell'utente
            
        Returns:
            Dizionario con informazioni estratte
        """
        testo_originale = testo
        testo = testo.lower().strip()
        risultato = {
            'tipo': None,
            'dati': {},
            'testo_originale': testo_originale
        }
        
        # Prima di tutto: distingui se è agenda o diario
        tipo_contenuto = DiarioManager.distingui_agenda_vs_diario(testo)
        
        # Se è chiaramente diario (riflessione personale), gestiscilo subito
        if tipo_contenuto == 'diario' and len(testo.split()) > 10:
            # È una riflessione lunga, probabilmente diario
            analisi_diario = DiarioManager.analizza_testo(testo_originale)
            risultato['tipo'] = 'diario'
            risultato['dati'] = {
                'testo': testo_originale,
                'riflessioni': analisi_diario['riflessioni'],
                'parole_chiave': analisi_diario['parole_chiave'],
                'sentiment': analisi_diario['sentiment'],
                'data': DiarioManager.estrai_data_da_testo(testo)
            }
            return risultato
        
        # Riconosci obiettivo con ore settimanali
        match = re.search(InputManager.PATTERNS['obiettivo_ore'], testo, re.IGNORECASE)
        if match:
            risultato['tipo'] = 'obiettivo'
            risultato['dati'] = {
                'nome': match.group(1).strip().title(),
                'durata_settimanale': float(match.group(2)),
                'tipo': InputManager._identifica_tipo_attivita(match.group(1))
            }
            return risultato
        
        # Riconosci impegno RICORRENTE (es. "ogni lunedì palestra ore 18")
        match_ricorrente = re.search(InputManager.PATTERNS['impegno_ricorrente'], testo, re.IGNORECASE)
        if match_ricorrente:
            giorno_o_frequenza = match_ricorrente.group(1).lower()
            nome = match_ricorrente.group(2).strip().title()
            ora = int(match_ricorrente.group(3))
            
            risultato['tipo'] = 'impegno_ricorrente'
            risultato['dati'] = {
                'nome': nome,
                'ora_inizio': f"{ora}:00",
                'ora_fine': f"{ora+1}:00",
                'pattern': 'settimanale' if giorno_o_frequenza != 'giorno' else 'giornaliero',
                'giorno_settimana': giorno_o_frequenza if giorno_o_frequenza != 'giorno' else None
            }
            return risultato
        
        # Riconosci impegno con data completa (formato flessibile)
        # Cerca pattern con data + ora
        match_data_ora = re.search(
            r'(luned[ìi]|marted[ìi]|mercoled[ìi]|gioved[ìi]|venerd[ìi]|sabato|domenica)\s+(\d{1,2})\s+(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)(?:\s+(\d{4}))?.+?(?:ore|alle|dalle)\s+(\d{1,2})',
            testo, re.IGNORECASE
        )
        
        if match_data_ora:
            giorno_settimana = match_data_ora.group(1)
            giorno_numero = int(match_data_ora.group(2))
            mese_nome = match_data_ora.group(3).lower()
            anno = int(match_data_ora.group(4)) if match_data_ora.group(4) else datetime.now().year
            ora = int(match_data_ora.group(5))
            
            # Estrai nome impegno (prima della data o tra data e ora)
            # Cerca tutto prima del giorno della settimana
            nome_match = re.search(rf'(.+?)\s+{giorno_settimana}', testo, re.IGNORECASE)
            if nome_match:
                nome_impegno = nome_match.group(1).strip().title()
            else:
                # Fallback: estrai tra mese e "alle/ore"
                nome_match = re.search(rf'{mese_nome}.+?(\w+(?:\s+\w+)*)\s+(?:ore|alle|dalle)', testo, re.IGNORECASE)
                nome_impegno = nome_match.group(1).strip().title() if nome_match else 'Impegno'
            
            # Converti mese
            mesi = {
                'gennaio': 1, 'febbraio': 2, 'marzo': 3, 'aprile': 4,
                'maggio': 5, 'giugno': 6, 'luglio': 7, 'agosto': 8,
                'settembre': 9, 'ottobre': 10, 'novembre': 11, 'dicembre': 12
            }
            mese_num = mesi.get(mese_nome, 1)
            
            risultato['tipo'] = 'impegno'
            risultato['dati'] = {
                'nome': nome_impegno,
                'ora_inizio': f"{ora}:00",
                'ora_fine': f"{ora+1}:00",
                'data_specifica': f"{anno}-{mese_num:02d}-{giorno_numero:02d}"
            }
            return risultato
        
        # Riconosci impegno oggi/domani con formato "ore XX" o "XX-XX"
        match_ore = re.search(r'(?:oggi|domani)\s+(.+?)\s+ore\s+(\d{1,2})', testo, re.IGNORECASE)
        if match_ore:
            risultato['tipo'] = 'impegno'
            risultato['dati'] = {
                'nome': match_ore.group(1).strip().title(),
                'ora_inizio': f"{match_ore.group(2)}:00",
                'ora_fine': f"{int(match_ore.group(2))+1}:00",  # +1 ora di default
                'giorno': 'oggi' if 'oggi' in testo else 'domani'
            }
            return risultato
        
        # Riconosci impegno oggi/domani con formato semplice (es. "18-19")
        match_semplice = re.search(r'(?:oggi|domani)\s+(.+?)\s+(\d{1,2})\s*-\s*(\d{1,2})', testo, re.IGNORECASE)
        if match_semplice:
            risultato['tipo'] = 'impegno'
            risultato['dati'] = {
                'nome': match_semplice.group(1).strip().title(),
                'ora_inizio': f"{match_semplice.group(2)}:00",
                'ora_fine': f"{match_semplice.group(3)}:00",
                'giorno': 'oggi' if 'oggi' in testo else 'domani'
            }
            return risultato
        
        # Riconosci impegno con orari specifici
        match = re.search(InputManager.PATTERNS['impegno_specifico'], testo, re.IGNORECASE)
        if match:
            risultato['tipo'] = 'impegno'
            ora_inizio = f"{match.group(2)}:{match.group(3) or '00'}"
            ora_fine = f"{match.group(4)}:{match.group(5) or '00'}" if match.group(4) else None
            
            risultato['dati'] = {
                'nome': match.group(1).strip().title(),
                'ora_inizio': ora_inizio,
                'ora_fine': ora_fine
            }
            
            # Cerca giorno della settimana
            giorno_match = re.search(InputManager.PATTERNS['giorno_settimana'], testo, re.IGNORECASE)
            if giorno_match:
                risultato['dati']['giorno'] = giorno_match.group(1)
            
            return risultato
        
        # Riconosci stato emotivo/fisico
        match = re.search(InputManager.PATTERNS['stato_emotivo'], testo, re.IGNORECASE)
        if match:
            risultato['tipo'] = 'stato'
            risultato['dati'] = {
                'stato': match.group(1).strip(),
                'suggerimento': InputManager._suggerisci_da_stato(match.group(1))
            }
            return risultato
        
        # Riconosci preferenza per il riposo
        if re.search(InputManager.PATTERNS['preferenza_riposo'], testo, re.IGNORECASE):
            risultato['tipo'] = 'preferenza'
            risultato['dati'] = {
                'tipo_preferenza': 'riposo',
                'azione': 'aumenta_pause'
            }
            return risultato
        
        # Riconosci completamento attività
        match = re.search(InputManager.PATTERNS['completamento'], testo, re.IGNORECASE)
        if match:
            risultato['tipo'] = 'completamento'
            risultato['dati'] = {
                'attivita': match.group(1).strip(),
                'messaggio': f"Ottimo lavoro! Hai completato: {match.group(1).strip()}"
            }
            return risultato
        
        # Riconosci richiesta di aiuto
        if re.search(InputManager.PATTERNS['richiesta_aiuto'], testo, re.IGNORECASE):
            risultato['tipo'] = 'aiuto'
            risultato['dati'] = {
                'suggerimenti': [
                    "Puoi dire: 'Voglio studiare Python 3 ore a settimana'",
                    "Oppure: 'Domenica vado al mare dalle 16 alle 20'",
                    "O ancora: 'Sono stanco' per ricevere suggerimenti",
                    "Usa 'Genera piano' per vedere la tua settimana organizzata"
                ]
            }
            return risultato
        
        # Riconosci tempo disponibile
        match = re.search(InputManager.PATTERNS['tempo_disponibile'], testo, re.IGNORECASE)
        if match:
            risultato['tipo'] = 'tempo_libero'
            risultato['dati'] = {
                'ore': float(match.group(1)),
                'suggerimento': InputManager._suggerisci_attivita_per_tempo(float(match.group(1)))
            }
            return risultato
        
        # Riconosci spesa
        match = re.search(InputManager.PATTERNS['spesa'], testo, re.IGNORECASE)
        if not match:
            match = re.search(InputManager.PATTERNS['spesa_diretta'], testo, re.IGNORECASE)
        if not match:
            match = re.search(InputManager.PATTERNS['spesa_solo_importo'], testo, re.IGNORECASE)
        
        if match:
            importo_str = match.group(1).replace(',', '.')
            importo = float(importo_str)
            descrizione = match.group(2).strip() if len(match.groups()) >= 2 else 'Spesa generica'
            
            # Categorizza automaticamente
            from app.managers.spese_manager import SpeseManager
            categoria = SpeseManager(None).categorizza_spesa(descrizione)
            
            risultato['tipo'] = 'spesa'
            risultato['dati'] = {
                'importo': importo,
                'descrizione': descrizione.title(),
                'categoria': categoria,
                'data': InputManager._estrai_data_spesa(testo)
            }
            return risultato
        
        # Riconosci domande comuni
        domande = {
            r'(?:cosa|che cosa|che)\s+(?:devo|dovrei|posso)\s+fare\s+(?:oggi|adesso|ora)': 'domanda_oggi',
            r'(?:quanto|quanti)\s+(?:ho\s+)?speso': 'domanda_spese',
            r'(?:mostra|fammi vedere|visualizza)\s+(?:i\s+)?(?:miei\s+)?obiettivi': 'domanda_obiettivi',
            r'(?:come|qual è|qual\s+è)\s+(?:il\s+mio\s+)?piano': 'domanda_piano',
            r'(?:cosa|che)\s+(?:ho fatto|abbiamo fatto)': 'domanda_passato'
        }
        
        for pattern, tipo_domanda in domande.items():
            if re.search(pattern, testo, re.IGNORECASE):
                risultato['tipo'] = 'domanda'
                risultato['dati'] = {'tipo_domanda': tipo_domanda}
                return risultato
        
        # Se contiene riflessioni personali o nomi propri, è diario
        if any(word in testo for word in ['ho parlato', 'ho incontrato', 'ho capito', 'ho imparato', 'mi è piaciuto', 'oggi', 'stamattina', 'stasera']):
            analisi_diario = DiarioManager.analizza_testo(testo_originale)
            risultato['tipo'] = 'diario'
            risultato['dati'] = {
                'testo': testo_originale,
                'riflessioni': analisi_diario['riflessioni'],
                'parole_chiave': analisi_diario['parole_chiave'],
                'sentiment': analisi_diario['sentiment'],
                'data': DiarioManager.estrai_data_da_testo(testo)
            }
            return risultato
        
        # Input non riconosciuto - fallback a diario per non perdere nulla
        risultato['tipo'] = 'sconosciuto'
        return risultato
    
    @staticmethod
    def _identifica_tipo_attivita(attivita: str) -> str:
        """Identifica il tipo di attività dal nome"""
        attivita = attivita.lower()
        
        # Parole chiave per studio
        if any(keyword in attivita for keyword in [
            'studiare', 'imparare', 'corso', 'lezione', 'esame', 'python', 'programmare',
            'matematica', 'fisica', 'chimica', 'inglese', 'italiano', 'storia', 'geografia',
            'coding', 'computer', 'università', 'scuola', 'libro', 'leggere un libro di testo'
        ]):
            return 'studio'
        
        # Parole chiave per sport
        if any(keyword in attivita for keyword in [
            'palestra', 'correre', 'nuoto', 'calcio', 'sport', 'allenamento', 'fitness',
            'yoga', 'pilates', 'crossfit', 'tennis', 'basket', 'bici', 'ciclismo',
            'camminare', 'trekking', 'arrampicata', 'arti marziali', 'boxe', 'danza'
        ]):
            return 'sport'
        
        # Parole chiave per lavoro
        if any(keyword in attivita for keyword in [
            'lavoro', 'progetto', 'riunione', 'meeting', 'call', 'presentazione',
            'report', 'analisi', 'sviluppo', 'design', 'consulenza', 'cliente'
        ]):
            return 'lavoro'
        
        # Parole chiave per hobbies/personale
        if any(keyword in attivita for keyword in [
            'hobby', 'chitarra', 'pianoforte', 'musica', 'disegno', 'pittura',
            'fotografia', 'cucina', 'giardinaggio', 'videogiochi', 'serie tv'
        ]):
            return 'personale'
        
        # Default
        return 'personale'
    
    @staticmethod
    def _suggerisci_da_stato(stato: str) -> str:
        """Suggerisce azioni in base allo stato emotivo"""
        stato = stato.lower()
        
        if 'stanc' in stato or 'esaust' in stato:
            return 'Ridurre il carico di lavoro e aumentare le pause. Considera una pausa lunga o riposo.'
        elif 'stress' in stato:
            return 'Prenditi una pausa, fai respiri profondi. Riduci le attività intense per oggi.'
        elif 'concentrat' in stato or 'energic' in stato or 'motivat' in stato:
            return 'Ottimo momento per attività che richiedono focus e impegno mentale!'
        elif 'rilassat' in stato:
            return 'Puoi affrontare attività più impegnative o dedicarti a progetti importanti.'
        
        return 'Continua così! Sei sulla buona strada.'
    
    @staticmethod
    def _suggerisci_attivita_per_tempo(ore: float) -> str:
        """Suggerisce attività in base al tempo disponibile"""
        if ore >= 4:
            return 'Ottimo! Hai tempo per un progetto importante, studio approfondito o sport + relax.'
        elif ore >= 2:
            return 'Puoi dedicarti a uno studio intenso, allenamento completo o hobby creativo.'
        elif ore >= 1:
            return 'Perfetto per una sessione di studio mirata, esercizio breve o attività ricreativa.'
        elif ore >= 0.5:
            return 'Tempo ideale per una pausa attiva, lettura leggera o breve allenamento.'
        else:
            return 'Ottimo per una pausa, stretching o meditazione breve.'
    
    @staticmethod
    def _estrai_data_spesa(testo: str) -> date:
        """Estrae data dalla spesa (oggi, ieri, o data specifica)"""
        testo_lower = testo.lower()
        
        if 'ieri' in testo_lower:
            return date.today() - timedelta(days=1)
        
        # Default: oggi
        return date.today()

