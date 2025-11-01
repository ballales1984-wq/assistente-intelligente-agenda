"""Motore adattivo per aggiustamenti in tempo reale"""
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.models import UserProfile, Obiettivo


class MotoreAdattivo:
    """Adatta il piano in tempo reale in base allo stato e ai cambiamenti"""
    
    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.stato_corrente = {
            'energia': 'normale',
            'stress': 'normale',
            'tempo_libero': 0
        }
    
    def aggiorna_stato(self, tipo_aggiornamento: str, valore: Any) -> Dict[str, Any]:
        """
        Aggiorna lo stato corrente dell'utente
        
        Args:
            tipo_aggiornamento: Tipo di aggiornamento (energia, stress, completamento)
            valore: Valore dell'aggiornamento
            
        Returns:
            Suggerimenti in base al nuovo stato
        """
        if tipo_aggiornamento == 'energia':
            self.stato_corrente['energia'] = valore
        elif tipo_aggiornamento == 'stress':
            self.stato_corrente['stress'] = valore
        
        return self._genera_suggerimenti()
    
    def attivita_completata(
        self, 
        attivita: Dict[str, Any], 
        tempo_effettivo: float
    ) -> Dict[str, Any]:
        """
        Gestisce il completamento di un'attività
        
        Args:
            attivita: Attività completata
            tempo_effettivo: Tempo impiegato in ore
            
        Returns:
            Informazioni sul tempo libero e suggerimenti
        """
        # Aggiorna ore completate se è un obiettivo
        if attivita.get('tipo') == 'obiettivo' and 'id_obiettivo' in attivita:
            obiettivo = Obiettivo.query.get(attivita['id_obiettivo'])
            if obiettivo:
                obiettivo.ore_completate += tempo_effettivo
        
        # Calcola tempo libero
        tempo_previsto = attivita.get('durata_ore', 0)
        tempo_risparmiato = tempo_previsto - tempo_effettivo
        
        if tempo_risparmiato > 0:
            self.stato_corrente['tempo_libero'] += tempo_risparmiato
            
            return {
                'messaggio': f'Ottimo lavoro! Hai risparmiato {tempo_risparmiato:.1f} ore.',
                'tempo_libero': self.stato_corrente['tempo_libero'],
                'suggerimenti': self._suggerisci_uso_tempo_libero(tempo_risparmiato)
            }
        
        return {
            'messaggio': 'Attività completata!',
            'tempo_libero': self.stato_corrente['tempo_libero'],
            'suggerimenti': []
        }
    
    def adatta_piano(
        self, 
        piano_originale: List[Dict[str, Any]], 
        evento: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Adatta il piano esistente in base a un nuovo evento
        
        Args:
            piano_originale: Piano originale
            evento: Nuovo evento da inserire
            
        Returns:
            Piano adattato
        """
        piano_adattato = piano_originale.copy()
        
        # Inserisci nuovo evento
        data_evento = evento.get('data_inizio')
        
        # Trova attività sovrapposte
        attivita_da_spostare = []
        for i, attivita in enumerate(piano_adattato):
            if self._si_sovrappongono(attivita, evento):
                # Se l'attività è flessibile, spostala
                if attivita.get('tipo') == 'obiettivo':
                    attivita_da_spostare.append((i, attivita))
        
        # Rimuovi attività da spostare
        for i, _ in reversed(attivita_da_spostare):
            piano_adattato.pop(i)
        
        # Aggiungi nuovo evento
        piano_adattato.append(evento)
        
        # Riposiziona attività spostate
        for _, attivita in attivita_da_spostare:
            nuovo_slot = self._trova_nuovo_slot(piano_adattato, attivita)
            if nuovo_slot:
                attivita['data_inizio'] = nuovo_slot['inizio']
                attivita['data_fine'] = nuovo_slot['fine']
                piano_adattato.append(attivita)
        
        return sorted(piano_adattato, key=lambda x: x['data_inizio'])
    
    def _genera_suggerimenti(self) -> List[str]:
        """Genera suggerimenti in base allo stato corrente"""
        suggerimenti = []
        
        # Suggerimenti basati sull'energia
        if self.stato_corrente['energia'] == 'bassa':
            suggerimenti.append('💤 Considera una pausa o un\'attività leggera')
            suggerimenti.append('☕ Forse è il momento per un caffè o uno snack')
        elif self.stato_corrente['energia'] == 'alta':
            suggerimenti.append('🚀 Ottimo momento per attività impegnative!')
            suggerimenti.append('🎯 Puoi affrontare obiettivi ad alta intensità')
        
        # Suggerimenti basati sullo stress
        if self.stato_corrente['stress'] == 'alto':
            suggerimenti.append('🧘 Prenditi una pausa per rilassarti')
            suggerimenti.append('🌿 Considera tecniche di respirazione o meditazione')
            suggerimenti.append('📉 Riduci il carico di lavoro per oggi')
        
        # Suggerimenti sul tempo libero
        if self.stato_corrente['tempo_libero'] > 0:
            suggerimenti.extend(
                self._suggerisci_uso_tempo_libero(self.stato_corrente['tempo_libero'])
            )
        
        return suggerimenti
    
    def _suggerisci_uso_tempo_libero(self, ore: float) -> List[str]:
        """Suggerisce come usare il tempo libero"""
        suggerimenti = []
        
        if ore >= 2:
            suggerimenti.append('🎮 Hai tempo per un hobby o attività ricreativa')
            suggerimenti.append('🏃 Perfetto per una sessione di sport')
        elif ore >= 1:
            suggerimenti.append('📚 Puoi anticipare un obiettivo di studio')
            suggerimenti.append('🎨 Tempo per un\'attività creativa')
        else:
            suggerimenti.append('☕ Goditi una pausa meritata')
            suggerimenti.append('🚶 Una breve passeggiata ti farà bene')
        
        return suggerimenti
    
    def _si_sovrappongono(
        self, 
        attivita1: Dict[str, Any], 
        attivita2: Dict[str, Any]
    ) -> bool:
        """Verifica se due attività si sovrappongono"""
        inizio1 = attivita1['data_inizio']
        fine1 = attivita1['data_fine']
        inizio2 = attivita2['data_inizio']
        fine2 = attivita2['data_fine']
        
        return not (fine1 <= inizio2 or fine2 <= inizio1)
    
    def _trova_nuovo_slot(
        self, 
        piano: List[Dict[str, Any]], 
        attivita: Dict[str, Any]
    ) -> Dict[str, datetime]:
        """Trova un nuovo slot per un'attività spostata"""
        durata = (attivita['data_fine'] - attivita['data_inizio']).total_seconds() / 3600
        
        # Ordina piano per data
        piano_ordinato = sorted(piano, key=lambda x: x['data_inizio'])
        
        # Cerca slot tra le attività esistenti
        for i in range(len(piano_ordinato) - 1):
            gap_inizio = piano_ordinato[i]['data_fine']
            gap_fine = piano_ordinato[i + 1]['data_inizio']
            gap_durata = (gap_fine - gap_inizio).total_seconds() / 3600
            
            if gap_durata >= durata:
                return {
                    'inizio': gap_inizio,
                    'fine': gap_inizio + timedelta(hours=durata)
                }
        
        # Se non trovato, metti alla fine
        if piano_ordinato:
            ultimo = piano_ordinato[-1]
            return {
                'inizio': ultimo['data_fine'],
                'fine': ultimo['data_fine'] + timedelta(hours=durata)
            }
        
        return None
    
    def analizza_produttivita(self, periodo_giorni: int = 7) -> Dict[str, Any]:
        """
        Analizza la produttività dell'utente
        
        Args:
            periodo_giorni: Numero di giorni da analizzare
            
        Returns:
            Statistiche e insights
        """
        data_inizio = datetime.now() - timedelta(days=periodo_giorni)
        
        obiettivi = self.user_profile.obiettivi.filter(
            Obiettivo.updated_at >= data_inizio
        ).all()
        
        statistiche = {
            'obiettivi_totali': len(obiettivi),
            'ore_completate': sum(obj.ore_completate for obj in obiettivi),
            'ore_pianificate': sum(obj.durata_settimanale for obj in obiettivi),
            'tasso_completamento': 0,
            'insights': []
        }
        
        if statistiche['ore_pianificate'] > 0:
            statistiche['tasso_completamento'] = (
                statistiche['ore_completate'] / statistiche['ore_pianificate']
            ) * 100
        
        # Genera insights
        if statistiche['tasso_completamento'] >= 90:
            statistiche['insights'].append('🌟 Eccellente! Stai rispettando il piano')
        elif statistiche['tasso_completamento'] >= 70:
            statistiche['insights'].append('👍 Buon lavoro! Continua così')
        else:
            statistiche['insights'].append('💡 Potresti aver bisogno di rivedere gli obiettivi')
        
        return statistiche

