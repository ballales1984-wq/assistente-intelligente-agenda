"""Generatore di agenda dinamica"""
from datetime import datetime, timedelta, time
from typing import List, Dict, Any
from app.models import UserProfile, Obiettivo, Impegno


class AgendaDinamica:
    """Genera e gestisce l'agenda dinamica dell'utente"""
    
    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.piano_settimanale = []
    
    def genera_piano_settimanale(self, data_inizio: datetime = None) -> List[Dict[str, Any]]:
        """
        Genera un piano settimanale basato su obiettivi e impegni
        
        Args:
            data_inizio: Data di inizio del piano (default: lunedì prossimo)
            
        Returns:
            Lista di attività pianificate
        """
        if data_inizio is None:
            # Trova il prossimo lunedì
            oggi = datetime.now()
            giorni_al_lunedi = (7 - oggi.weekday()) % 7
            data_inizio = oggi + timedelta(days=giorni_al_lunedi if giorni_al_lunedi > 0 else 0)
        
        data_inizio = data_inizio.replace(hour=0, minute=0, second=0, microsecond=0)
        piano = []
        
        # Ottieni obiettivi attivi e impegni
        obiettivi = self.user_profile.obiettivi.filter_by(attivo=True).all()
        impegni = self._ottieni_impegni_settimana(data_inizio)
        
        # Genera piano giorno per giorno
        for giorno_offset in range(7):
            data_giorno = data_inizio + timedelta(days=giorno_offset)
            piano_giorno = self._pianifica_giorno(data_giorno, obiettivi, impegni)
            piano.extend(piano_giorno)
        
        self.piano_settimanale = piano
        return piano
    
    def _pianifica_giorno(
        self, 
        data: datetime, 
        obiettivi: List[Obiettivo], 
        impegni: List[Impegno]
    ) -> List[Dict[str, Any]]:
        """Pianifica le attività per un singolo giorno"""
        piano_giorno = []
        
        # Aggiungi impegni fissi
        impegni_giorno = [imp for imp in impegni if imp.data_inizio.date() == data.date()]
        for impegno in impegni_giorno:
            piano_giorno.append({
                'tipo': 'impegno',
                'nome': impegno.nome,
                'data_inizio': impegno.data_inizio,
                'data_fine': impegno.data_fine,
                'fisso': not impegno.spostabile,
                'priorita': impegno.priorita
            })
        
        # Calcola slot liberi
        slot_liberi = self._calcola_slot_liberi(data, impegni_giorno)
        
        # Distribuisci obiettivi negli slot liberi
        for obiettivo in obiettivi:
            ore_da_allocare = obiettivo.durata_settimanale / 7  # Distribuisci equamente
            
            # Considera preferenze di giorno
            if obiettivo.giorni_preferiti:
                giorni_preferiti = obiettivo.giorni_preferiti.split(',')
                giorno_settimana = self._nome_giorno(data.weekday())
                if giorno_settimana[:3] not in giorni_preferiti:
                    continue
            
            # Trova slot adatto
            slot = self._trova_slot_adatto(slot_liberi, ore_da_allocare, obiettivo)
            if slot:
                piano_giorno.append({
                    'tipo': 'obiettivo',
                    'nome': obiettivo.nome,
                    'data_inizio': slot['inizio'],
                    'data_fine': slot['fine'],
                    'durata_ore': ore_da_allocare,
                    'intensita': obiettivo.intensita,
                    'tipo_attivita': obiettivo.tipo
                })
        
        # Aggiungi pause in base al profilo
        piano_giorno = self._aggiungi_pause(piano_giorno, data)
        
        return sorted(piano_giorno, key=lambda x: x['data_inizio'])
    
    def _ottieni_impegni_settimana(self, data_inizio: datetime) -> List[Impegno]:
        """Ottieni tutti gli impegni della settimana"""
        data_fine = data_inizio + timedelta(days=7)
        impegni = self.user_profile.impegni.filter(
            Impegno.data_inizio >= data_inizio,
            Impegno.data_inizio < data_fine
        ).all()
        return impegni
    
    def _calcola_slot_liberi(
        self, 
        data: datetime, 
        impegni: List[Impegno]
    ) -> List[Dict[str, datetime]]:
        """Calcola gli slot temporali liberi in un giorno"""
        inizio_giornata = datetime.combine(
            data.date(), 
            self.user_profile.ora_inizio_giornata or time(8, 0)
        )
        fine_giornata = datetime.combine(
            data.date(), 
            self.user_profile.ora_fine_giornata or time(23, 0)
        )
        
        # Ordina impegni per ora di inizio
        impegni_ordinati = sorted(impegni, key=lambda x: x.data_inizio)
        
        slot_liberi = []
        ora_corrente = inizio_giornata
        
        for impegno in impegni_ordinati:
            if impegno.data_inizio > ora_corrente:
                slot_liberi.append({
                    'inizio': ora_corrente,
                    'fine': impegno.data_inizio
                })
            ora_corrente = max(ora_corrente, impegno.data_fine)
        
        # Aggiungi ultimo slot fino a fine giornata
        if ora_corrente < fine_giornata:
            slot_liberi.append({
                'inizio': ora_corrente,
                'fine': fine_giornata
            })
        
        return slot_liberi
    
    def _trova_slot_adatto(
        self, 
        slot_liberi: List[Dict[str, datetime]], 
        ore_necessarie: float,
        obiettivo: Obiettivo
    ) -> Dict[str, datetime]:
        """Trova lo slot più adatto per un obiettivo"""
        minuti_necessari = int(ore_necessarie * 60)
        
        for slot in slot_liberi:
            durata_slot = (slot['fine'] - slot['inizio']).total_seconds() / 60
            
            if durata_slot >= minuti_necessari:
                # Considera preferenze orarie
                if obiettivo.orari_preferiti:
                    ora = slot['inizio'].hour
                    if not self._orario_compatibile(ora, obiettivo.orari_preferiti):
                        continue
                
                return {
                    'inizio': slot['inizio'],
                    'fine': slot['inizio'] + timedelta(minutes=minuti_necessari)
                }
        
        return None
    
    def _orario_compatibile(self, ora: int, preferenze: str) -> bool:
        """Verifica se un orario è compatibile con le preferenze"""
        preferenze = preferenze.lower()
        
        if 'mattina' in preferenze and 6 <= ora < 12:
            return True
        if 'pomeriggio' in preferenze and 12 <= ora < 18:
            return True
        if 'sera' in preferenze and 18 <= ora < 23:
            return True
        if 'notte' in preferenze and (23 <= ora or ora < 6):
            return True
        
        return False
    
    def _aggiungi_pause(
        self, 
        piano_giorno: List[Dict[str, Any]], 
        data: datetime
    ) -> List[Dict[str, Any]]:
        """Aggiungi pause intelligenti nel piano giornaliero"""
        if not piano_giorno:
            return piano_giorno
        
        # Parametri pause in base allo stile di vita
        durata_pausa = {
            'intensivo': 15,
            'bilanciato': 30,
            'rilassato': 45
        }
        
        minuti_pausa = durata_pausa.get(self.user_profile.stile_vita, 30)
        piano_con_pause = []
        
        for i, attivita in enumerate(piano_giorno):
            piano_con_pause.append(attivita)
            
            # Aggiungi pausa dopo attività intense
            if attivita.get('intensita') == 'alta' or attivita.get('tipo_attivita') == 'studio':
                if i < len(piano_giorno) - 1:
                    pausa_inizio = attivita['data_fine']
                    pausa_fine = pausa_inizio + timedelta(minutes=minuti_pausa)
                    
                    piano_con_pause.append({
                        'tipo': 'pausa',
                        'nome': 'Pausa',
                        'data_inizio': pausa_inizio,
                        'data_fine': pausa_fine,
                        'suggerimento': self._suggerimento_pausa()
                    })
        
        return piano_con_pause
    
    def _suggerimento_pausa(self) -> str:
        """Genera un suggerimento per la pausa"""
        suggerimenti = [
            'Fai una passeggiata',
            'Bevi un bicchiere d\'acqua',
            'Stretching leggero',
            'Respira profondamente',
            'Ascolta musica rilassante'
        ]
        import random
        return random.choice(suggerimenti)
    
    @staticmethod
    def _nome_giorno(weekday: int) -> str:
        """Converte numero giorno in nome"""
        giorni = ['lun', 'mar', 'mer', 'gio', 'ven', 'sab', 'dom']
        return giorni[weekday]

