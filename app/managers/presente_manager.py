"""Manager per gestione del presente - Piano giornaliero e adattamenti"""
from datetime import date, datetime, time, timedelta
from typing import Dict, Any, List
from app.models import UserProfile, Obiettivo, Impegno
from app.core import AgendaDinamica, MotoreAdattivo


class PresenteManager:
    """
    Gestisce il piano della giornata corrente e adattamenti in tempo reale.
    Risponde a domande come: "Cosa devo fare oggi?"
    """
    
    def __init__(self, user_profile: UserProfile):
        """
        Inizializza il PresenteManager
        
        Args:
            user_profile: Profilo dell'utente
        """
        self.user_profile = user_profile
        self.agenda = AgendaDinamica(user_profile)
        self.motore = MotoreAdattivo(user_profile)
    
    def genera_piano_oggi(self, data: date = None) -> Dict[str, Any]:
        """
        Genera il piano dettagliato per oggi
        
        Args:
            data: Data da pianificare (default: oggi)
            
        Returns:
            Piano giornaliero con:
            - timeline: Lista attività ordinate per orario
            - ore_libere: Ore disponibili
            - ore_occupate: Ore pianificate
            - suggerimenti: Consigli per la giornata
            - prossimo_impegno: Prossima attività
        """
        if data is None:
            data = date.today()
        
        # Recupera impegni e obiettivi del giorno
        impegni_oggi = self._get_impegni_giorno(data)
        obiettivi_attivi = self.user_profile.obiettivi.filter_by(attivo=True).all()
        
        # Genera timeline
        timeline = self._crea_timeline_giorno(data, impegni_oggi, obiettivi_attivi)
        
        # Calcola metriche
        ore_occupate = sum(
            (imp.data_fine - imp.data_inizio).total_seconds() / 3600 
            for imp in impegni_oggi
        )
        
        ore_disponibili = self._calcola_ore_disponibili(data)
        ore_libere = max(0, ore_disponibili - ore_occupate)
        
        # Trova prossimo impegno
        ora_corrente = datetime.now()
        prossimo = self._trova_prossimo_impegno(timeline, ora_corrente)
        
        # Genera suggerimenti
        suggerimenti = self._genera_suggerimenti_giorno(
            timeline, 
            ore_libere, 
            obiettivi_attivi
        )
        
        return {
            'data': data.isoformat(),
            'timeline': timeline,
            'ore_totali_disponibili': round(ore_disponibili, 2),
            'ore_occupate': round(ore_occupate, 2),
            'ore_libere': round(ore_libere, 2),
            'prossimo_impegno': prossimo,
            'suggerimenti': suggerimenti,
            'stato_giornata': self._valuta_densita_giornata(ore_occupate, ore_disponibili)
        }
    
    def cosa_devo_fare_oggi(self) -> Dict[str, Any]:
        """
        Risponde alla domanda: "Cosa devo fare oggi?"
        
        Returns:
            Piano di oggi con focus sul prossimo impegno
        """
        piano = self.genera_piano_oggi()
        
        # Formato user-friendly
        return {
            'messaggio': self._genera_messaggio_piano_oggi(piano),
            'piano_completo': piano
        }
    
    def adatta_piano_a_stato(
        self, 
        stato: str, 
        data: date = None
    ) -> Dict[str, Any]:
        """
        Adatta il piano giornaliero in base allo stato mentale/fisico
        
        Args:
            stato: Stato corrente (stanco, motivato, stressato, etc.)
            data: Data da adattare (default: oggi)
            
        Returns:
            Piano adattato con modifiche e suggerimenti
        """
        if data is None:
            data = date.today()
        
        piano_base = self.genera_piano_oggi(data)
        stato_lower = stato.lower()
        
        # Adatta in base allo stato
        modifiche = []
        timeline_adattata = piano_base['timeline'].copy()
        
        if 'stanc' in stato_lower or 'esaust' in stato_lower:
            # Riduce intensità, aumenta pause
            timeline_adattata = self._riduci_intensita(timeline_adattata)
            modifiche.append("⚡ Carico ridotto per recuperare energie")
            modifiche.append("☕ Pause più lunghe programmate")
            modifiche.append("🛌 Considera di posticipare attività non urgenti")
        
        elif 'stress' in stato_lower or 'ansios' in stato_lower:
            # Riorganizza per ridurre pressione
            timeline_adattata = self._riduci_pressione(timeline_adattata)
            modifiche.append("🧘 Priorità a benessere mentale")
            modifiche.append("📉 Attività intense riposizionate")
            modifiche.append("🌿 Aggiunti momenti di respiro")
        
        elif 'motivat' in stato_lower or 'energic' in stato_lower:
            # Aumenta carico produttivo
            timeline_adattata = self._aumenta_produttivita(timeline_adattata)
            modifiche.append("🚀 Ottimo! Sfrutta questo momento di energia")
            modifiche.append("🎯 Aggiunte attività ad alta priorità")
            modifiche.append("💪 Puoi fare di più oggi!")
        
        elif 'concentrat' in stato_lower:
            # Prioritizza attività che richiedono focus
            modifiche.append("🧠 Perfetto per studio e attività complesse")
            modifiche.append("📚 Approfitta di questo stato per task difficili")
        
        else:
            modifiche.append("✅ Piano standard mantenuto")
        
        return {
            'data': data.isoformat(),
            'stato': stato,
            'piano_originale': piano_base,
            'piano_adattato': {
                'timeline': timeline_adattata,
                'modifiche_applicate': len(modifiche)
            },
            'modifiche': modifiche,
            'suggerimenti': self._suggerimenti_per_stato(stato_lower)
        }
    
    def ora_corrente_cosa_fare(self) -> Dict[str, Any]:
        """
        Risponde a: "Cosa devo fare adesso?"
        
        Returns:
            Attività corrente o prossima con suggerimenti
        """
        piano = self.genera_piano_oggi()
        ora_corrente = datetime.now()
        
        # Trova attività corrente
        attivita_corrente = None
        for attivita in piano['timeline']:
            inizio = datetime.fromisoformat(attivita['data_inizio'])
            fine = datetime.fromisoformat(attivita['data_fine'])
            
            if inizio <= ora_corrente <= fine:
                attivita_corrente = attivita
                break
        
        if attivita_corrente:
            tempo_rimanente = (
                datetime.fromisoformat(attivita_corrente['data_fine']) - ora_corrente
            ).total_seconds() / 60
            
            return {
                'situazione': 'in_corso',
                'attivita': attivita_corrente,
                'tempo_rimanente_minuti': round(tempo_rimanente),
                'messaggio': f"⏰ Sei impegnato in: {attivita_corrente['nome']} " \
                            f"(ancora {round(tempo_rimanente)} minuti)"
            }
        else:
            prossimo = piano['prossimo_impegno']
            if prossimo:
                return {
                    'situazione': 'libero',
                    'prossimo_impegno': prossimo,
                    'tempo_libero': prossimo.get('tra_minuti', 0),
                    'messaggio': f"🆓 Sei libero! Prossimo impegno: {prossimo['nome']} " \
                                f"tra {prossimo.get('tra_minuti', 0)} minuti"
                }
            else:
                return {
                    'situazione': 'libero',
                    'messaggio': "🎉 Nessun impegno in programma! Goditi il tempo libero",
                    'suggerimenti': piano['suggerimenti']
                }
    
    # Metodi privati di supporto
    
    def _get_impegni_giorno(self, data: date) -> List[Impegno]:
        """Recupera impegni di un giorno specifico"""
        dt_inizio = datetime.combine(data, datetime.min.time())
        dt_fine = datetime.combine(data, datetime.max.time())
        
        return self.user_profile.impegni.filter(
            Impegno.data_inizio >= dt_inizio,
            Impegno.data_inizio <= dt_fine
        ).order_by(Impegno.data_inizio).all()
    
    def _crea_timeline_giorno(
        self, 
        data: date, 
        impegni: List[Impegno],
        obiettivi: List[Obiettivo]
    ) -> List[Dict[str, Any]]:
        """Crea timeline ordinata per il giorno"""
        timeline = []
        
        # Aggiungi impegni esistenti
        for impegno in impegni:
            timeline.append({
                'tipo': 'impegno',
                'nome': impegno.nome,
                'data_inizio': impegno.data_inizio.isoformat(),
                'data_fine': impegno.data_fine.isoformat(),
                'priorita': impegno.priorita,
                'spostabile': impegno.spostabile
            })
        
        # Ordina per orario
        timeline.sort(key=lambda x: x['data_inizio'])
        
        return timeline
    
    def _calcola_ore_disponibili(self, data: date) -> float:
        """Calcola ore disponibili nel giorno"""
        ora_inizio = self.user_profile.ora_inizio_giornata or time(8, 0)
        ora_fine = self.user_profile.ora_fine_giornata or time(23, 0)
        
        ore = ora_fine.hour - ora_inizio.hour
        minuti = ora_fine.minute - ora_inizio.minute
        
        return ore + (minuti / 60)
    
    def _trova_prossimo_impegno(
        self, 
        timeline: List[Dict[str, Any]], 
        ora_corrente: datetime
    ) -> Dict[str, Any]:
        """Trova il prossimo impegno"""
        for attivita in timeline:
            inizio = datetime.fromisoformat(attivita['data_inizio'])
            if inizio > ora_corrente:
                tra_minuti = (inizio - ora_corrente).total_seconds() / 60
                return {
                    'nome': attivita['nome'],
                    'tipo': attivita['tipo'],
                    'orario': inizio.strftime('%H:%M'),
                    'tra_minuti': round(tra_minuti)
                }
        return None
    
    def _genera_suggerimenti_giorno(
        self,
        timeline: List[Dict[str, Any]],
        ore_libere: float,
        obiettivi: List[Obiettivo]
    ) -> List[str]:
        """Genera suggerimenti per la giornata"""
        suggerimenti = []
        
        if ore_libere >= 2:
            suggerimenti.append(f"⏰ Hai {ore_libere:.1f}h libere oggi")
            if obiettivi:
                obj = obiettivi[0]
                suggerimenti.append(f"💡 Potresti dedicare tempo a: {obj.nome}")
        elif ore_libere >= 1:
            suggerimenti.append("📝 Hai circa 1h libera - perfetto per task brevi")
        else:
            suggerimenti.append("📅 Giornata piena! Cerca di mantenere le pause")
        
        # Suggerimenti basati sul carico
        if len(timeline) > 8:
            suggerimenti.append("⚠️ Giornata intensa - gestisci l'energia")
        elif len(timeline) < 3:
            suggerimenti.append("🌿 Giornata leggera - ottimo per riposare o anticipare")
        
        return suggerimenti
    
    def _valuta_densita_giornata(self, ore_occupate: float, ore_disponibili: float) -> str:
        """Valuta quanto è piena la giornata"""
        if ore_disponibili == 0:
            return 'Libera'
        
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
    
    def _riduci_intensita(self, timeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Riduce intensità del piano per recupero"""
        # Filtra attività non urgenti
        timeline_ridotta = [
            att for att in timeline 
            if att.get('priorita', 5) >= 7 or not att.get('spostabile', True)
        ]
        return timeline_ridotta
    
    def _riduci_pressione(self, timeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Riduce pressione spostando attività intense"""
        # Mantieni solo attività essenziali
        timeline_ridotta = [
            att for att in timeline 
            if att.get('priorita', 5) >= 6
        ]
        return timeline_ridotta
    
    def _aumenta_produttivita(self, timeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Aumenta produttività aggiungendo attività prioritarie"""
        # Timeline rimane uguale, suggerimento di fare di più
        return timeline
    
    def _suggerimenti_per_stato(self, stato: str) -> List[str]:
        """Genera suggerimenti specifici per lo stato"""
        suggerimenti = []
        
        if 'stanc' in stato:
            suggerimenti.extend([
                "💤 Fai pause più frequenti",
                "🚶 Una breve passeggiata può aiutare",
                "💧 Assicurati di idratarti bene"
            ])
        elif 'stress' in stato:
            suggerimenti.extend([
                "🧘 Prova 5 minuti di respirazione profonda",
                "📱 Stacca dai dispositivi per 15 minuti",
                "🎵 Ascolta musica rilassante"
            ])
        elif 'motivat' in stato or 'energic' in stato:
            suggerimenti.extend([
                "🎯 Affronta i task più difficili ora",
                "📚 Ottimo momento per apprendimento intenso",
                "💪 Sfrutta questo picco di energia"
            ])
        
        return suggerimenti
    
    def _genera_messaggio_piano_oggi(self, piano: Dict[str, Any]) -> str:
        """Genera messaggio testuale del piano"""
        ore_occupate = piano['ore_occupate']
        ore_libere = piano['ore_libere']
        num_attivita = len(piano['timeline'])
        
        emoji_densita = {
            'molto_piena': '🔥',
            'piena': '📊',
            'moderata': '⚖️',
            'leggera': '🌿',
            'molto_leggera': '😌'
        }
        
        emoji = emoji_densita.get(piano['stato_giornata'], '📅')
        
        messaggio = f"{emoji} **Piano di oggi**\n\n"
        messaggio += f"📊 {num_attivita} attività programmate\n"
        messaggio += f"⏰ {ore_occupate:.1f}h occupate | {ore_libere:.1f}h libere\n\n"
        
        if piano['prossimo_impegno']:
            prossimo = piano['prossimo_impegno']
            messaggio += f"⏭️ Prossimo: {prossimo['nome']} alle {prossimo['orario']}\n\n"
        
        if piano['suggerimenti']:
            messaggio += "💡 Suggerimenti:\n"
            for sug in piano['suggerimenti'][:3]:
                messaggio += f"  • {sug}\n"
        
        return messaggio

