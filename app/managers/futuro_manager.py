"""Manager per proiezioni future - Simulazioni e previsioni"""
from datetime import date, datetime, timedelta
from typing import Dict, Any, List
from app.models import UserProfile, Obiettivo, Impegno


class FuturoManager:
    """
    Gestisce proiezioni future e simulazioni.
    Risponde a domande come: "Come sarà il mio giovedì?" o "Quanto saprò tra 6 mesi?"
    """
    
    def __init__(self, user_profile: UserProfile):
        """
        Inizializza il FuturoManager
        
        Args:
            user_profile: Profilo dell'utente
        """
        self.user_profile = user_profile
    
    def simula_giornata(self, data: date) -> Dict[str, Any]:
        """
        Simula e prevede come sarà una giornata futura
        
        Args:
            data: Data futura da simulare
            
        Returns:
            Simulazione giornata con:
            - impegni_previsti: Impegni già schedulati
            - routine_prevista: Routine basata su pattern passati
            - obiettivi_pianificati: Sessioni obiettivi previste
            - previsione_densita: Quanto sarà piena
            - suggerimenti_preparazione: Come prepararsi
        """
        # Recupera impegni già schedulati per quel giorno
        impegni_fissi = self._get_impegni_giorno(data)
        
        # Analizza routine nei giorni simili (stesso giorno settimana)
        routine_simile = self._analizza_routine_giorno_settimana(data.weekday())
        
        # Prevedi allocazione obiettivi
        obiettivi_attivi = self.user_profile.obiettivi.filter_by(attivo=True).all()
        obiettivi_previsti = self._prevedi_obiettivi_giorno(data, obiettivi_attivi)
        
        # Calcola ore occupate e libere
        ore_impegni = sum(
            (imp.data_fine - imp.data_inizio).total_seconds() / 3600 
            for imp in impegni_fissi
        )
        ore_obiettivi = sum(obj['durata_ore'] for obj in obiettivi_previsti)
        ore_disponibili = self._calcola_ore_disponibili()
        ore_libere = max(0, ore_disponibili - ore_impegni - ore_obiettivi)
        
        # Determina densità
        densita = self._calcola_densita(ore_impegni + ore_obiettivi, ore_disponibili)
        
        # Genera suggerimenti preparazione
        suggerimenti = self._suggerimenti_preparazione(
            impegni_fissi, 
            obiettivi_previsti, 
            densita,
            data
        )
        
        return {
            'data': data.isoformat(),
            'giorno_settimana': data.strftime('%A'),
            'giorni_mancanti': (data - date.today()).days,
            'impegni_fissi': [
                {
                    'nome': imp.nome,
                    'orario': f"{imp.data_inizio.strftime('%H:%M')}-{imp.data_fine.strftime('%H:%M')}",
                    'tipo': imp.tipo
                } for imp in impegni_fissi
            ],
            'obiettivi_previsti': obiettivi_previsti,
            'routine_simile': routine_simile,
            'previsione': {
                'ore_impegni': round(ore_impegni, 2),
                'ore_obiettivi': round(ore_obiettivi, 2),
                'ore_libere': round(ore_libere, 2),
                'densita': densita
            },
            'suggerimenti_preparazione': suggerimenti
        }
    
    def come_sara_giovedi(self) -> Dict[str, Any]:
        """
        Risponde a: "Come sarà il mio giovedì?"
        
        Returns:
            Simulazione del prossimo giovedì
        """
        oggi = date.today()
        
        # Trova prossimo giovedì (weekday 3)
        giorni_al_giovedi = (3 - oggi.weekday()) % 7
        if giorni_al_giovedi == 0:
            giorni_al_giovedi = 7
        
        prossimo_giovedi = oggi + timedelta(days=giorni_al_giovedi)
        
        return self.simula_giornata(prossimo_giovedi)
    
    def proietta_competenze(
        self, 
        obiettivo: str, 
        ore_settimanali: float, 
        mesi: int
    ) -> Dict[str, Any]:
        """
        Proietta competenze future in base al ritmo di studio
        
        Args:
            obiettivo: Nome dell'obiettivo/skill
            ore_settimanali: Ore dedicate a settimana
            mesi: Numero di mesi di proiezione
            
        Returns:
            Proiezione con:
            - ore_totali: Ore accumulate nel periodo
            - livello_stimato: Livello competenza stimato
            - milestones: Traguardi intermedi
            - comparazione: Confronto con standard
            - consigli: Come ottimizzare
        """
        settimane = mesi * 4
        ore_totali = ore_settimanali * settimane
        
        # Stima livello competenza (basato su regola 10.000 ore)
        # Livelli: Principiante (0-100h), Intermedio (100-500h), 
        #          Avanzato (500-2000h), Esperto (2000-5000h), Master (5000+h)
        livello_stimato = self._stima_livello_competenza(ore_totali)
        
        # Genera milestones
        milestones = self._genera_milestones(ore_settimanali, mesi)
        
        # Comparazione con standard
        comparazione = self._compara_con_standard(obiettivo, ore_totali)
        
        # Consigli ottimizzazione
        consigli = self._consigli_apprendimento(ore_settimanali, obiettivo)
        
        return {
            'obiettivo': obiettivo,
            'periodo': {
                'mesi': mesi,
                'settimane': settimane
            },
            'impegno': {
                'ore_settimanali': ore_settimanali,
                'ore_totali': round(ore_totali, 2)
            },
            'proiezione': {
                'livello_stimato': livello_stimato,
                'percentuale_mastery': round((ore_totali / 10000) * 100, 2),
                'competenza_descrizione': self._descrivi_livello(livello_stimato)
            },
            'milestones': milestones,
            'comparazione': comparazione,
            'consigli': consigli
        }
    
    def quanto_sapro_tra_n_mesi(self, obiettivo_nome: str, mesi: int) -> Dict[str, Any]:
        """
        Risponde a: "Quanto saprò di Python tra 6 mesi?"
        
        Args:
            obiettivo_nome: Nome obiettivo (es. "Python")
            mesi: Numero di mesi
            
        Returns:
            Proiezione competenze
        """
        # Trova obiettivo (cerca per nome contenente la stringa)
        obiettivi_attivi = self.user_profile.obiettivi.filter_by(attivo=True).all()
        obiettivi_match = [
            obj for obj in obiettivi_attivi
            if obiettivo_nome.lower() in obj.nome.lower()
        ]
        obiettivo = obiettivi_match[0] if obiettivi_match else None
        
        if obiettivo:
            ore_settimanali = obiettivo.durata_settimanale
            ore_gia_fatte = obiettivo.ore_completate
        else:
            # Default: assume 3h settimanali se non specificato
            ore_settimanali = 3.0
            ore_gia_fatte = 0.0
        
        proiezione = self.proietta_competenze(obiettivo_nome, ore_settimanali, mesi)
        
        # Aggiungi contesto attuale
        proiezione['situazione_attuale'] = {
            'ore_gia_completate': ore_gia_fatte,
            'livello_attuale': self._stima_livello_competenza(ore_gia_fatte)
        }
        
        return proiezione
    
    def prevedi_prossima_settimana(self) -> Dict[str, Any]:
        """
        Prevede come sarà la prossima settimana
        
        Returns:
            Previsione settimana con pattern e suggerimenti
        """
        oggi = date.today()
        lunedi_prossimo = oggi + timedelta(days=(7 - oggi.weekday()))
        domenica_prossima = lunedi_prossimo + timedelta(days=6)
        
        previsione_giorni = []
        
        for i in range(7):
            giorno = lunedi_prossimo + timedelta(days=i)
            simulazione = self.simula_giornata(giorno)
            previsione_giorni.append(simulazione)
        
        # Calcola metriche settimanali
        ore_totali_previste = sum(
            g['previsione']['ore_impegni'] + g['previsione']['ore_obiettivi'] 
            for g in previsione_giorni
        )
        
        giorno_piu_pieno = max(
            previsione_giorni, 
            key=lambda g: g['previsione']['ore_impegni'] + g['previsione']['ore_obiettivi']
        )
        
        return {
            'periodo': {
                'inizio': lunedi_prossimo.isoformat(),
                'fine': domenica_prossima.isoformat()
            },
            'previsione_giorni': previsione_giorni,
            'riepilogo_settimana': {
                'ore_totali_previste': round(ore_totali_previste, 2),
                'giorno_piu_pieno': {
                    'giorno': giorno_piu_pieno['giorno_settimana'],
                    'data': giorno_piu_pieno['data'],
                    'ore': giorno_piu_pieno['previsione']['ore_impegni'] + 
                           giorno_piu_pieno['previsione']['ore_obiettivi']
                }
            },
            'suggerimenti': self._suggerimenti_settimana_futura(previsione_giorni)
        }
    
    # Metodi privati di supporto
    
    def _get_impegni_giorno(self, data: date) -> List[Impegno]:
        """Recupera impegni di un giorno futuro"""
        dt_inizio = datetime.combine(data, datetime.min.time())
        dt_fine = datetime.combine(data, datetime.max.time())
        
        return self.user_profile.impegni.filter(
            Impegno.data_inizio >= dt_inizio,
            Impegno.data_inizio <= dt_fine
        ).all()
    
    def _analizza_routine_giorno_settimana(self, weekday: int) -> Dict[str, Any]:
        """Analizza routine tipica per un giorno della settimana"""
        # Analizza ultimi 4 occorrenze di questo giorno
        oggi = date.today()
        occorrenze_passate = []
        
        for i in range(1, 5):  # Ultime 4 settimane
            giorni_indietro = oggi.weekday() - weekday + (i * 7)
            if giorni_indietro > 0:
                giorno_passato = oggi - timedelta(days=giorni_indietro)
                impegni = self._get_impegni_giorno(giorno_passato)
                
                if impegni:
                    occorrenze_passate.append({
                        'data': giorno_passato.isoformat(),
                        'num_impegni': len(impegni),
                        'tipo_prevalente': max(
                            set(imp.tipo for imp in impegni if imp.tipo),
                            key=lambda t: sum(1 for imp in impegni if imp.tipo == t),
                            default='vario'
                        )
                    })
        
        if occorrenze_passate:
            media_impegni = sum(o['num_impegni'] for o in occorrenze_passate) / len(occorrenze_passate)
            return {
                'pattern_trovato': True,
                'media_impegni': round(media_impegni, 1),
                'occorrenze_analizzate': len(occorrenze_passate)
            }
        
        return {
            'pattern_trovato': False,
            'messaggio': 'Nessun pattern chiaro per questo giorno'
        }
    
    def _prevedi_obiettivi_giorno(
        self, 
        data: date, 
        obiettivi: List[Obiettivo]
    ) -> List[Dict[str, Any]]:
        """Prevede quali obiettivi saranno pianificati quel giorno"""
        obiettivi_previsti = []
        
        for obiettivo in obiettivi:
            # Distribuzione media: ore_settimanali / 7 giorni
            ore_giorno = obiettivo.durata_settimanale / 7
            
            # Considera preferenze giorni
            if obiettivo.giorni_preferiti:
                giorni_pref = obiettivo.giorni_preferiti.split(',')
                giorno_abbr = ['lun', 'mar', 'mer', 'gio', 'ven', 'sab', 'dom'][data.weekday()]
                
                if giorno_abbr not in giorni_pref:
                    continue
            
            obiettivi_previsti.append({
                'nome': obiettivo.nome,
                'tipo': obiettivo.tipo,
                'durata_ore': round(ore_giorno, 2),
                'intensita': obiettivo.intensita,
                'orario_preferito': obiettivo.orari_preferiti or 'flessibile'
            })
        
        return obiettivi_previsti
    
    def _calcola_ore_disponibili(self) -> float:
        """Calcola ore disponibili giornaliere"""
        ora_inizio = self.user_profile.ora_inizio_giornata
        ora_fine = self.user_profile.ora_fine_giornata
        
        if not ora_inizio or not ora_fine:
            return 15.0  # Default
        
        ore = ora_fine.hour - ora_inizio.hour
        minuti = ora_fine.minute - ora_inizio.minute
        
        return ore + (minuti / 60)
    
    def _calcola_densita(self, ore_occupate: float, ore_disponibili: float) -> str:
        """Calcola densità giornata"""
        if ore_disponibili == 0:
            return 'Tranquilla'
        
        percentuale = (ore_occupate / ore_disponibili) * 100
        
        if percentuale >= 80:
            return 'Molto Intensa'
        elif percentuale >= 60:
            return 'Intensa'
        elif percentuale >= 40:
            return 'Equilibrata'
        elif percentuale >= 20:
            return 'Tranquilla'
        else:
            return 'Molto Tranquilla'
    
    def _suggerimenti_preparazione(
        self,
        impegni: List[Impegno],
        obiettivi: List[Dict[str, Any]],
        densita: str,
        data: date
    ) -> List[str]:
        """Genera suggerimenti per prepararsi al giorno"""
        suggerimenti = []
        giorni_mancanti = (data - date.today()).days
        
        # Suggerimenti basati su tempo mancante
        if giorni_mancanti <= 1:
            suggerimenti.append("📌 Domani! Prepara tutto stasera")
        elif giorni_mancanti <= 3:
            suggerimenti.append(f"📅 Tra {giorni_mancanti} giorni - Pianifica in anticipo")
        
        # Suggerimenti basati su densità
        if densita == 'Molto Intensa':
            suggerimenti.append("🔥 Giornata molto intensa - Riposa bene il giorno prima")
            suggerimenti.append("⚡ Considera di spostare qualcosa se possibile")
        elif densita == 'Intensa':
            suggerimenti.append("📊 Giornata intensa - Organizza bene la mattina")
        elif densita == 'Molto Tranquilla':
            suggerimenti.append("🌿 Giornata tranquilla - Ottima per recuperare energie")
        
        # Suggerimenti basati su impegni
        if impegni:
            primo_impegno = min(impegni, key=lambda i: i.data_inizio)
            suggerimenti.append(
                f"⏰ Prima attività: {primo_impegno.nome} " \
                f"alle {primo_impegno.data_inizio.strftime('%H:%M')}"
            )
        
        return suggerimenti
    
    def _stima_livello_competenza(self, ore_totali: float) -> str:
        """Stima livello competenza in base alle ore"""
        if ore_totali < 10:
            return 'principiante_assoluto'
        elif ore_totali < 100:
            return 'principiante'
        elif ore_totali < 500:
            return 'intermedio'
        elif ore_totali < 1000:
            return 'intermedio_avanzato'
        elif ore_totali < 2000:
            return 'avanzato'
        elif ore_totali < 5000:
            return 'esperto'
        else:
            return 'master'
    
    def _descrivi_livello(self, livello: str) -> str:
        """Descrizione testuale del livello"""
        descrizioni = {
            'principiante_assoluto': 'Stai iniziando! Concentrati sulle basi.',
            'principiante': 'Conosci le basi, continua a praticare.',
            'intermedio': 'Buone fondamenta, puoi affrontare progetti.',
            'intermedio_avanzato': 'Competenze solide, puoi insegnare le basi.',
            'avanzato': 'Esperto nella materia, puoi gestire progetti complessi.',
            'esperto': 'Altissimo livello, sei una risorsa preziosa.',
            'master': 'Massimo livello raggiungibile, sei un riferimento!'
        }
        return descrizioni.get(livello, 'Livello non definito')
    
    def _genera_milestones(
        self, 
        ore_settimanali: float, 
        mesi: int
    ) -> List[Dict[str, Any]]:
        """Genera traguardi intermedi"""
        milestones = []
        ore_accumulate = 0
        
        traguardi_ore = [10, 50, 100, 200, 500, 1000, 2000, 5000]
        
        for settimana in range(1, mesi * 4 + 1):
            ore_accumulate += ore_settimanali
            
            # Controlla se raggiungi un traguardo
            for traguardo in traguardi_ore:
                if ore_accumulate >= traguardo and \
                   (ore_accumulate - ore_settimanali) < traguardo:
                    
                    mese_traguardo = settimana // 4
                    milestones.append({
                        'ore': traguardo,
                        'settimana': settimana,
                        'mese': mese_traguardo,
                        'descrizione': self._descrizione_milestone(traguardo)
                    })
        
        return milestones
    
    def _descrizione_milestone(self, ore: int) -> str:
        """Descrizione del traguardo"""
        descrizioni = {
            10: '🌱 Prime 10 ore - Hai rotto il ghiaccio!',
            50: '🔥 50 ore - Inizi a sentirti a tuo agio',
            100: '💯 100 ore - Fondamenta solide costruite',
            200: '⭐ 200 ore - Competenza intermedia raggiunta',
            500: '🚀 500 ore - Sei davvero bravo!',
            1000: '🏆 1000 ore - Livello avanzato, complimenti!',
            2000: '💎 2000 ore - Sei un esperto!',
            5000: '👑 5000 ore - Master level raggiunto!'
        }
        return descrizioni.get(ore, f'{ore} ore completate')
    
    def _compara_con_standard(self, obiettivo: str, ore: float) -> Dict[str, Any]:
        """Compara con standard di apprendimento"""
        # Standard di riferimento
        standard = {
            'python': {'base': 100, 'professionale': 500, 'esperto': 2000},
            'default': {'base': 50, 'professionale': 300, 'esperto': 1000}
        }
        
        obj_lower = obiettivo.lower()
        std = standard.get(obj_lower, standard['default'])
        
        if ore >= std['esperto']:
            livello_raggiunto = 'esperto'
            prossimo_livello = None
            ore_mancanti = 0
        elif ore >= std['professionale']:
            livello_raggiunto = 'professionale'
            prossimo_livello = 'esperto'
            ore_mancanti = std['esperto'] - ore
        elif ore >= std['base']:
            livello_raggiunto = 'base'
            prossimo_livello = 'professionale'
            ore_mancanti = std['professionale'] - ore
        else:
            livello_raggiunto = 'principiante'
            prossimo_livello = 'base'
            ore_mancanti = std['base'] - ore
        
        return {
            'livello_raggiunto': livello_raggiunto,
            'prossimo_livello': prossimo_livello,
            'ore_al_prossimo_livello': round(ore_mancanti, 2) if ore_mancanti > 0 else 0,
            'percentuale_progresso': round((ore / std['esperto']) * 100, 1)
        }
    
    def _consigli_apprendimento(
        self, 
        ore_settimanali: float, 
        obiettivo: str
    ) -> List[str]:
        """Consigli per ottimizzare l'apprendimento"""
        consigli = []
        
        if ore_settimanali < 3:
            consigli.append("📈 Considera di aumentare a 3-5h/settimana per risultati migliori")
        elif ore_settimanali > 15:
            consigli.append("⚠️ Attenzione al burnout! 10-15h/settimana è ottimale")
        else:
            consigli.append("✅ Ritmo di studio ottimale!")
        
        consigli.extend([
            "💡 Distribuzione ideale: Sessioni di 1-2 ore con pause",
            "📚 Pratica costante > sessioni lunghe sporadiche",
            "🎯 Fissa obiettivi intermedi per mantenere motivazione"
        ])
        
        return consigli
    
    def _suggerimenti_settimana_futura(
        self, 
        previsione_giorni: List[Dict[str, Any]]
    ) -> List[str]:
        """Suggerimenti per la settimana futura"""
        suggerimenti = []
        
        # Trova giorni critici
        giorni_molto_pieni = [
            g for g in previsione_giorni 
            if g['previsione']['densita'] in ['Molto Intensa', 'Intensa']
        ]
        
        if len(giorni_molto_pieni) >= 4:
            suggerimenti.append("⚠️ Settimana molto intensa! Pianifica bene il riposo")
        elif len(giorni_molto_pieni) >= 2:
            suggerimenti.append("📊 Alcuni giorni saranno intensi - Gestisci l'energia")
        
        # Giorni leggeri
        giorni_leggeri = [
            g for g in previsione_giorni 
            if g['previsione']['densita'] in ['Tranquilla', 'Molto Tranquilla']
        ]
        
        if giorni_leggeri:
            giorni_str = ', '.join(g['giorno_settimana'] for g in giorni_leggeri[:2])
            suggerimenti.append(f"🌿 {giorni_str}: giorni più tranquilli per recuperare")
        
        return suggerimenti

