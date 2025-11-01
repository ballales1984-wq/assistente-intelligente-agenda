"""Manager per analisi del passato - Storico attività e riflessioni"""
from datetime import date, datetime, timedelta
from typing import Dict, Any, List
from sqlalchemy import func
from app.models import UserProfile, Obiettivo, Impegno, DiarioGiornaliero


class PassatoManager:
    """
    Gestisce l'analisi dello storico delle attività, impegni e riflessioni.
    Risponde a domande come: "Cosa ho fatto la settimana scorsa?"
    """
    
    def __init__(self, user_profile: UserProfile):
        """
        Inizializza il PassatoManager
        
        Args:
            user_profile: Profilo dell'utente
        """
        self.user_profile = user_profile
    
    def analizza_passato(
        self, 
        data_inizio: date, 
        data_fine: date
    ) -> Dict[str, Any]:
        """
        Analizza il periodo passato e restituisce un riepilogo completo
        
        Args:
            data_inizio: Data inizio periodo
            data_fine: Data fine periodo
            
        Returns:
            Dizionario con:
            - riepilogo_attivita: Lista attività per tipo
            - ore_totali: Ore dedicate per categoria
            - riflessioni: Lista riflessioni del periodo
            - sentiment_medio: Sentiment medio del periodo
            - parole_chiave_frequenti: Parole più usate
            - persone_incontrate: Persone menzionate
            - insights: Analisi e suggerimenti
        """
        # Recupera dati del periodo
        impegni = self._get_impegni_periodo(data_inizio, data_fine)
        riflessioni = self._get_riflessioni_periodo(data_inizio, data_fine)
        obiettivi = self._get_obiettivi_periodo(data_inizio, data_fine)
        
        # Analizza impegni per tipo
        riepilogo_attivita = self._raggruppa_impegni_per_tipo(impegni)
        
        # Calcola ore totali per categoria
        ore_totali = self._calcola_ore_per_categoria(impegni)
        
        # Analizza riflessioni
        analisi_riflessioni = self._analizza_riflessioni(riflessioni)
        
        # Genera insights
        insights = self._genera_insights_passato(
            impegni, 
            riflessioni, 
            obiettivi, 
            ore_totali
        )
        
        return {
            'periodo': {
                'inizio': data_inizio.isoformat(),
                'fine': data_fine.isoformat(),
                'giorni': (data_fine - data_inizio).days + 1
            },
            'riepilogo_attivita': riepilogo_attivita,
            'ore_totali': ore_totali,
            'impegni_count': len(impegni),
            'riflessioni': {
                'totali': len(riflessioni),
                'sentiment_medio': analisi_riflessioni['sentiment_medio'],
                'parole_chiave': analisi_riflessioni['parole_chiave_top'],
                'persone': analisi_riflessioni['persone'],
                'emozioni': analisi_riflessioni['emozioni']
            },
            'obiettivi': {
                'totali': len(obiettivi),
                'ore_completate': sum(obj.ore_completate for obj in obiettivi),
                'tasso_completamento': self._calcola_tasso_completamento(obiettivi)
            },
            'insights': insights
        }
    
    def cosa_ho_fatto_settimana_scorsa(self) -> Dict[str, Any]:
        """
        Risponde alla domanda: "Cosa ho fatto la settimana scorsa?"
        
        Returns:
            Riepilogo attività settimana scorsa
        """
        oggi = date.today()
        # Calcola lunedì della settimana scorsa
        lunedi_questa_settimana = oggi - timedelta(days=oggi.weekday())
        lunedi_scorso = lunedi_questa_settimana - timedelta(days=7)
        domenica_scorsa = lunedi_scorso + timedelta(days=6)
        
        return self.analizza_passato(lunedi_scorso, domenica_scorsa)
    
    def cosa_ho_fatto_mese_scorso(self) -> Dict[str, Any]:
        """
        Risponde alla domanda: "Cosa ho fatto il mese scorso?"
        
        Returns:
            Riepilogo attività mese scorso
        """
        oggi = date.today()
        primo_questo_mese = oggi.replace(day=1)
        ultimo_mese_scorso = primo_questo_mese - timedelta(days=1)
        primo_mese_scorso = ultimo_mese_scorso.replace(day=1)
        
        return self.analizza_passato(primo_mese_scorso, ultimo_mese_scorso)
    
    def statistiche_periodo(
        self, 
        data_inizio: date, 
        data_fine: date
    ) -> Dict[str, Any]:
        """
        Genera statistiche dettagliate per un periodo
        
        Args:
            data_inizio: Data inizio
            data_fine: Data fine
            
        Returns:
            Statistiche dettagliate con grafici dati
        """
        analisi = self.analizza_passato(data_inizio, data_fine)
        
        # Aggiungi breakdown giornaliero
        breakdown_giornaliero = self._breakdown_per_giorno(data_inizio, data_fine)
        
        # Trend temporale
        trend = self._calcola_trend(data_inizio, data_fine)
        
        analisi['breakdown_giornaliero'] = breakdown_giornaliero
        analisi['trend'] = trend
        
        return analisi
    
    # Metodi privati di supporto
    
    def _get_impegni_periodo(
        self, 
        data_inizio: date, 
        data_fine: date
    ) -> List[Impegno]:
        """Recupera impegni del periodo"""
        dt_inizio = datetime.combine(data_inizio, datetime.min.time())
        dt_fine = datetime.combine(data_fine, datetime.max.time())
        
        return self.user_profile.impegni.filter(
            Impegno.data_inizio >= dt_inizio,
            Impegno.data_inizio <= dt_fine
        ).all()
    
    def _get_riflessioni_periodo(
        self, 
        data_inizio: date, 
        data_fine: date
    ) -> List[DiarioGiornaliero]:
        """Recupera riflessioni del periodo"""
        return self.user_profile.diario_entries.filter(
            DiarioGiornaliero.data >= data_inizio,
            DiarioGiornaliero.data <= data_fine
        ).all()
    
    def _get_obiettivi_periodo(
        self, 
        data_inizio: date, 
        data_fine: date
    ) -> List[Obiettivo]:
        """Recupera obiettivi attivi nel periodo"""
        dt_fine = datetime.combine(data_fine, datetime.max.time())
        
        return self.user_profile.obiettivi.filter(
            Obiettivo.created_at <= dt_fine,
            Obiettivo.attivo == True
        ).all()
    
    def _raggruppa_impegni_per_tipo(self, impegni: List[Impegno]) -> Dict[str, int]:
        """Raggruppa impegni per tipo e conta occorrenze"""
        riepilogo = {}
        for impegno in impegni:
            tipo = impegno.tipo or 'altro'
            riepilogo[tipo] = riepilogo.get(tipo, 0) + 1
        return riepilogo
    
    def _calcola_ore_per_categoria(self, impegni: List[Impegno]) -> Dict[str, float]:
        """Calcola ore totali per ogni categoria"""
        ore_per_tipo = {}
        
        for impegno in impegni:
            durata = (impegno.data_fine - impegno.data_inizio).total_seconds() / 3600
            tipo = impegno.tipo or 'altro'
            ore_per_tipo[tipo] = ore_per_tipo.get(tipo, 0) + durata
        
        return {k: round(v, 2) for k, v in ore_per_tipo.items()}
    
    def _analizza_riflessioni(self, riflessioni: List[DiarioGiornaliero]) -> Dict[str, Any]:
        """Analizza riflessioni ed estrae pattern"""
        if not riflessioni:
            return {
                'sentiment_medio': 'neutro',
                'parole_chiave_top': [],
                'persone': [],
                'emozioni': []
            }
        
        # Calcola sentiment medio
        sentiments = [r.sentiment for r in riflessioni if r.sentiment]
        sentiment_counts = {'positivo': 0, 'neutro': 0, 'negativo': 0}
        for s in sentiments:
            sentiment_counts[s] = sentiment_counts.get(s, 0) + 1
        
        sentiment_medio = max(sentiment_counts, key=sentiment_counts.get)
        
        # Aggrega parole chiave
        tutte_parole = []
        for r in riflessioni:
            if r.parole_chiave:
                tutte_parole.extend(r.parole_chiave.split(','))
        
        # Conta frequenze
        from collections import Counter
        parole_freq = Counter(tutte_parole)
        parole_top = [p for p, _ in parole_freq.most_common(10)]
        
        # Estrai persone (dalle riflessioni JSON)
        persone = set()
        for r in riflessioni:
            riflessioni_data = r.get_riflessioni()
            for rif in riflessioni_data:
                if rif.get('tipo') == 'persone':
                    persone.update(rif.get('valori', []))
        
        # Estrai emozioni
        emozioni = set()
        for r in riflessioni:
            riflessioni_data = r.get_riflessioni()
            for rif in riflessioni_data:
                if rif.get('tipo') == 'emozioni':
                    emozioni.update(rif.get('valori', []))
        
        return {
            'sentiment_medio': sentiment_medio,
            'distribuzione_sentiment': sentiment_counts,
            'parole_chiave_top': parole_top,
            'persone': list(persone),
            'emozioni': list(emozioni)
        }
    
    def _calcola_tasso_completamento(self, obiettivi: List[Obiettivo]) -> float:
        """Calcola percentuale completamento obiettivi"""
        if not obiettivi:
            return 0.0
        
        ore_previste = sum(obj.durata_settimanale for obj in obiettivi)
        ore_completate = sum(obj.ore_completate for obj in obiettivi)
        
        if ore_previste == 0:
            return 0.0
        
        return round((ore_completate / ore_previste) * 100, 1)
    
    def _genera_insights_passato(
        self,
        impegni: List[Impegno],
        riflessioni: List[DiarioGiornaliero],
        obiettivi: List[Obiettivo],
        ore_totali: Dict[str, float]
    ) -> List[str]:
        """Genera insights intelligenti sul periodo passato"""
        insights = []
        
        # Insights su attività
        if ore_totali:
            categoria_max = max(ore_totali, key=ore_totali.get)
            ore_max = ore_totali[categoria_max]
            insights.append(
                f"📊 Hai dedicato più tempo a: {categoria_max} ({ore_max}h)"
            )
        
        # Insights su riflessioni
        if riflessioni:
            analisi = self._analizza_riflessioni(riflessioni)
            sentiment = analisi['sentiment_medio']
            
            emoji = {'positivo': '😊', 'neutro': '😐', 'negativo': '😔'}
            insights.append(
                f"{emoji.get(sentiment, '📝')} Sentiment medio del periodo: {sentiment}"
            )
            
            if analisi['persone']:
                persone_str = ', '.join(analisi['persone'][:3])
                insights.append(f"👥 Hai interagito con: {persone_str}")
        
        # Insights su obiettivi
        if obiettivi:
            tasso = self._calcola_tasso_completamento(obiettivi)
            if tasso >= 80:
                insights.append("🌟 Eccellente progresso sugli obiettivi!")
            elif tasso >= 50:
                insights.append("👍 Buon progresso sugli obiettivi")
            else:
                insights.append("💡 Gli obiettivi necessitano più attenzione")
        
        # Insights su produttività
        giorni_lavorativi = len(set(imp.data_inizio.date() for imp in impegni))
        if giorni_lavorativi > 0:
            insights.append(f"📅 Hai avuto attività in {giorni_lavorativi} giorni")
        
        return insights
    
    def _breakdown_per_giorno(
        self, 
        data_inizio: date, 
        data_fine: date
    ) -> List[Dict[str, Any]]:
        """Genera breakdown giornaliero delle attività"""
        breakdown = []
        
        current_date = data_inizio
        while current_date <= data_fine:
            impegni_giorno = self._get_impegni_periodo(current_date, current_date)
            riflessioni_giorno = self._get_riflessioni_periodo(current_date, current_date)
            
            ore_giorno = sum(
                (imp.data_fine - imp.data_inizio).total_seconds() / 3600 
                for imp in impegni_giorno
            )
            
            breakdown.append({
                'data': current_date.isoformat(),
                'impegni': len(impegni_giorno),
                'ore': round(ore_giorno, 2),
                'riflessioni': len(riflessioni_giorno),
                'sentiment': riflessioni_giorno[0].sentiment if riflessioni_giorno else 'neutro'
            })
            
            current_date += timedelta(days=1)
        
        return breakdown
    
    def _calcola_trend(
        self, 
        data_inizio: date, 
        data_fine: date
    ) -> Dict[str, str]:
        """Calcola trend di produttività nel periodo"""
        breakdown = self._breakdown_per_giorno(data_inizio, data_fine)
        
        if len(breakdown) < 2:
            return {'produttivita': 'stabile', 'mood': 'stabile'}
        
        # Trend produttività (basato su ore)
        ore_prima_meta = sum(d['ore'] for d in breakdown[:len(breakdown)//2])
        ore_seconda_meta = sum(d['ore'] for d in breakdown[len(breakdown)//2:])
        
        if ore_seconda_meta > ore_prima_meta * 1.2:
            trend_produttivita = 'crescente'
        elif ore_seconda_meta < ore_prima_meta * 0.8:
            trend_produttivita = 'decrescente'
        else:
            trend_produttivita = 'stabile'
        
        # Trend mood (basato su sentiment)
        sentiment_values = {'positivo': 1, 'neutro': 0, 'negativo': -1}
        mood_prima_meta = sum(
            sentiment_values.get(d['sentiment'], 0) 
            for d in breakdown[:len(breakdown)//2]
        )
        mood_seconda_meta = sum(
            sentiment_values.get(d['sentiment'], 0) 
            for d in breakdown[len(breakdown)//2:]
        )
        
        if mood_seconda_meta > mood_prima_meta:
            trend_mood = 'miglioramento'
        elif mood_seconda_meta < mood_prima_meta:
            trend_mood = 'peggioramento'
        else:
            trend_mood = 'stabile'
        
        return {
            'produttivita': trend_produttivita,
            'mood': trend_mood
        }
    
    def trova_pattern_ricorrenti(
        self, 
        data_inizio: date, 
        data_fine: date
    ) -> Dict[str, Any]:
        """
        Trova pattern ricorrenti nelle attività
        
        Args:
            data_inizio: Data inizio analisi
            data_fine: Data fine analisi
            
        Returns:
            Pattern identificati (giorni preferiti, orari, etc.)
        """
        impegni = self._get_impegni_periodo(data_inizio, data_fine)
        
        # Analizza giorni della settimana preferiti
        giorni_freq = {}
        for impegno in impegni:
            giorno_nome = impegno.data_inizio.strftime('%A')
            giorni_freq[giorno_nome] = giorni_freq.get(giorno_nome, 0) + 1
        
        # Analizza fasce orarie preferite
        fasce_orarie = {
            'mattina (6-12)': 0,
            'pomeriggio (12-18)': 0,
            'sera (18-23)': 0,
            'notte (23-6)': 0
        }
        
        for impegno in impegni:
            ora = impegno.data_inizio.hour
            if 6 <= ora < 12:
                fasce_orarie['mattina (6-12)'] += 1
            elif 12 <= ora < 18:
                fasce_orarie['pomeriggio (12-18)'] += 1
            elif 18 <= ora < 23:
                fasce_orarie['sera (18-23)'] += 1
            else:
                fasce_orarie['notte (23-6)'] += 1
        
        return {
            'giorni_frequenti': giorni_freq,
            'fasce_orarie': fasce_orarie,
            'giorno_piu_attivo': max(giorni_freq, key=giorni_freq.get) if giorni_freq else None,
            'fascia_preferita': max(fasce_orarie, key=fasce_orarie.get)
        }

