"""Manager per gestione e analisi spese"""
from datetime import date, datetime, timedelta
from typing import Dict, Any, List
from sqlalchemy import func
from app.i18n import get_message
from app.models import UserProfile, Spesa, CATEGORIE_SPESE


class SpeseManager:
    """
    Gestisce il tracking e l'analisi delle spese quotidiane.
    Risponde a domande come: "Quanto ho speso questa settimana?"
    """
    
    def __init__(self, user_profile: UserProfile):
        """
        Inizializza SpeseManager
        
        Args:
            user_profile: Profilo dell'utente
        """
        self.user_profile = user_profile
    
    def categorizza_spesa(self, descrizione: str) -> str:
        """
        Categorizza automaticamente una spesa in base alla descrizione
        
        Args:
            descrizione: Descrizione della spesa
            
        Returns:
            Categoria identificata
        """
        descrizione_lower = descrizione.lower()
        
        for categoria, parole_chiave in CATEGORIE_SPESE.items():
            if any(parola in descrizione_lower for parola in parole_chiave):
                return categoria
        
        return 'altro'
    
    def analizza_spese_periodo(
        self, 
        data_inizio: date, 
        data_fine: date,
        lang: str = 'it'
    ) -> Dict[str, Any]:
        """
        Analizza le spese di un periodo
        
        Args:
            data_inizio: Data inizio periodo
            data_fine: Data fine periodo
            
        Returns:
            Analisi completa con:
            - totale: Spesa totale periodo
            - per_categoria: Breakdown per categoria
            - per_giorno: Spesa giornaliera media
            - spesa_max: Spesa più alta
            - insights: Suggerimenti automatici
        """
        spese = self._get_spese_periodo(data_inizio, data_fine)
        
        if not spese:
            return {
                'periodo': {
                    'inizio': data_inizio.isoformat(),
                    'fine': data_fine.isoformat(),
                    'giorni': (data_fine - data_inizio).days + 1
                },
                'totale': 0.0,
                'num_spese': 0,
                'messaggio': 'Nessuna spesa registrata in questo periodo'
            }
        
        # Calcola totale
        totale = sum(s.importo for s in spese)
        
        # Raggruppa per categoria
        per_categoria = self._raggruppa_per_categoria(spese)
        
        # Calcola medie
        giorni_periodo = (data_fine - data_inizio).days + 1
        media_giornaliera = totale / giorni_periodo if giorni_periodo > 0 else 0
        
        # Trova spesa massima
        spesa_max = max(spese, key=lambda s: s.importo) if spese else None
        
        # Breakdown necessarie vs voluttuarie
        necessarie = sum(s.importo for s in spese if s.necessaria)
        voluttuarie = totale - necessarie
        
        # Genera insights
        insights = self._genera_insights_spese(
            totale, 
            per_categoria, 
            media_giornaliera,
            necessarie,
            voluttuarie,
            lang=lang
        )
        
        return {
            'periodo': {
                'inizio': data_inizio.isoformat(),
                'fine': data_fine.isoformat(),
                'giorni': giorni_periodo
            },
            'totale': round(totale, 2),
            'num_spese': len(spese),
            'media_giornaliera': round(media_giornaliera, 2),
            'per_categoria': {k: round(v, 2) for k, v in per_categoria.items()},
            'breakdown': {
                'necessarie': round(necessarie, 2),
                'voluttuarie': round(voluttuarie, 2),
                'percentuale_necessarie': round((necessarie/totale)*100, 1) if totale > 0 else 0
            },
            'spesa_max': {
                'importo': spesa_max.importo,
                'descrizione': spesa_max.descrizione,
                'data': spesa_max.data.isoformat()
            } if spesa_max else None,
            'insights': insights
        }
    
    def quanto_ho_speso_oggi(self) -> Dict[str, Any]:
        """
        Risponde a: "Quanto ho speso oggi?"
        
        Returns:
            Analisi spese di oggi
        """
        oggi = date.today()
        return self.analizza_spese_periodo(oggi, oggi)
    
    def quanto_ho_speso_settimana(self) -> Dict[str, Any]:
        """
        Risponde a: "Quanto ho speso questa settimana?"
        
        Returns:
            Analisi spese settimana corrente
        """
        oggi = date.today()
        lunedi = oggi - timedelta(days=oggi.weekday())
        domenica = lunedi + timedelta(days=6)
        
        return self.analizza_spese_periodo(lunedi, domenica)
    
    def quanto_ho_speso_mese(self) -> Dict[str, Any]:
        """
        Risponde a: "Quanto ho speso questo mese?"
        
        Returns:
            Analisi spese mese corrente
        """
        from calendar import monthrange
        
        oggi = date.today()
        primo_mese = oggi.replace(day=1)
        
        # Ultimo giorno del mese (gestisce correttamente tutti i mesi)
        ultimo_giorno = monthrange(oggi.year, oggi.month)[1]
        ultimo_mese = oggi.replace(day=ultimo_giorno)
        
        return self.analizza_spese_periodo(primo_mese, ultimo_mese)
    
    def budget_check(self, budget_mensile: float) -> Dict[str, Any]:
        """
        Verifica stato budget mensile
        
        Args:
            budget_mensile: Budget mensile impostato
            
        Returns:
            Stato budget con proiezioni
        """
        spese_mese = self.quanto_ho_speso_mese()
        oggi = date.today()
        giorni_trascorsi = oggi.day
        giorni_totali_mese = (date(oggi.year, oggi.month + 1, 1) - timedelta(days=1)).day if oggi.month < 12 else 31
        giorni_rimanenti = giorni_totali_mese - giorni_trascorsi
        
        speso = spese_mese['totale']
        rimanente = budget_mensile - speso
        percentuale_usata = (speso / budget_mensile * 100) if budget_mensile > 0 else 0
        
        # Proiezione fine mese
        spesa_media_giorno = spese_mese['media_giornaliera']
        proiezione_fine_mese = speso + (spesa_media_giorno * giorni_rimanenti)
        
        # Quanto puoi spendere al giorno
        budget_giornaliero_rimanente = rimanente / giorni_rimanenti if giorni_rimanenti > 0 else 0
        
        # Status
        if percentuale_usata >= 100:
            status = 'superato'
            emoji = '🔴'
        elif percentuale_usata >= 80:
            status = 'attenzione'
            emoji = '🟡'
        else:
            status = 'ok'
            emoji = '🟢'
        
        return {
            'budget_mensile': budget_mensile,
            'speso': round(speso, 2),
            'rimanente': round(rimanente, 2),
            'percentuale_usata': round(percentuale_usata, 1),
            'giorni': {
                'trascorsi': giorni_trascorsi,
                'rimanenti': giorni_rimanenti,
                'totali': giorni_totali_mese
            },
            'proiezione_fine_mese': round(proiezione_fine_mese, 2),
            'budget_giornaliero_rimanente': round(budget_giornaliero_rimanente, 2),
            'status': status,
            'emoji': emoji,
            'alert': self._genera_alert_budget(status, percentuale_usata, proiezione_fine_mese, budget_mensile)
        }
    
    def statistiche_categoria(self, categoria: str, mesi: int = 3) -> Dict[str, Any]:
        """
        Statistiche dettagliate per una categoria
        
        Args:
            categoria: Categoria da analizzare
            mesi: Numero di mesi da analizzare
            
        Returns:
            Statistiche categoria
        """
        data_fine = date.today()
        data_inizio = data_fine - timedelta(days=mesi * 30)
        
        spese_categoria = self.user_profile.spese.filter(
            Spesa.data >= data_inizio,
            Spesa.data <= data_fine,
            Spesa.categoria == categoria
        ).all()
        
        if not spese_categoria:
            return {
                'categoria': categoria,
                'messaggio': f'Nessuna spesa in {categoria} negli ultimi {mesi} mesi'
            }
        
        totale = sum(s.importo for s in spese_categoria)
        media = totale / len(spese_categoria)
        
        # Spesa più alta e più bassa
        max_spesa = max(spese_categoria, key=lambda s: s.importo)
        min_spesa = min(spese_categoria, key=lambda s: s.importo)
        
        # Trend mensile
        trend = self._calcola_trend_mensile(spese_categoria, mesi)
        
        return {
            'categoria': categoria,
            'periodo_mesi': mesi,
            'totale': round(totale, 2),
            'num_spese': len(spese_categoria),
            'media': round(media, 2),
            'max': {
                'importo': max_spesa.importo,
                'descrizione': max_spesa.descrizione,
                'data': max_spesa.data.isoformat()
            },
            'min': {
                'importo': min_spesa.importo,
                'descrizione': min_spesa.descrizione,
                'data': min_spesa.data.isoformat()
            },
            'trend': trend
        }
    
    def top_spese(self, limite: int = 10, giorni: int = 30) -> List[Dict[str, Any]]:
        """
        Trova le spese più alte recenti
        
        Args:
            limite: Numero di spese da ritornare
            giorni: Periodo in giorni
            
        Returns:
            Lista spese più alte
        """
        data_inizio = date.today() - timedelta(days=giorni)
        
        spese = self.user_profile.spese.filter(
            Spesa.data >= data_inizio
        ).order_by(Spesa.importo.desc()).limit(limite).all()
        
        return [s.to_dict() for s in spese]
    
    # Metodi privati
    
    def _get_spese_periodo(self, data_inizio: date, data_fine: date) -> List[Spesa]:
        """Recupera spese del periodo"""
        return self.user_profile.spese.filter(
            Spesa.data >= data_inizio,
            Spesa.data <= data_fine
        ).order_by(Spesa.data, Spesa.ora).all()
    
    def _raggruppa_per_categoria(self, spese: List[Spesa]) -> Dict[str, float]:
        """Raggruppa spese per categoria"""
        per_categoria = {}
        
        for spesa in spese:
            categoria = spesa.categoria or 'altro'
            per_categoria[categoria] = per_categoria.get(categoria, 0) + spesa.importo
        
        return per_categoria
    
    def _genera_insights_spese(
        self,
        totale: float,
        per_categoria: Dict[str, float],
        media_giornaliera: float,
        necessarie: float,
        voluttuarie: float,
        lang: str = 'it'
    ) -> List[str]:
        """Genera insights sulle spese"""
        insights = []
        
        # Insight su categoria prevalente
        if per_categoria:
            cat_max = max(per_categoria, key=per_categoria.get)
            importo_max = per_categoria[cat_max]
            percentuale = (importo_max / totale * 100) if totale > 0 else 0
            
            insights.append(
                get_message('main_category', lang, cat=cat_max, amount=importo_max, perc=percentuale)
            )
        
        # Insight su necessarie vs voluttuarie
        if voluttuarie > 0:
            perc_voluttuarie = (voluttuarie / totale * 100) if totale > 0 else 0
            if perc_voluttuarie > 40:
                insights.append(
                    get_message('reduce_optional', lang, perc=perc_voluttuarie)
                )
            else:
                insights.append(
                    get_message('good_balance', lang, perc=perc_voluttuarie)
                )
        
        # Insight su media giornaliera
        insights.append(get_message('daily_average', lang, avg=media_giornaliera))
        
        return insights
    
    def _genera_alert_budget(
        self,
        status: str,
        percentuale: float,
        proiezione: float,
        budget: float
    ) -> str:
        """Genera alert per budget"""
        if status == 'superato':
            return f"🔴 BUDGET SUPERATO! Hai già speso il {percentuale:.1f}% del budget mensile"
        elif status == 'attenzione':
            return f"🟡 ATTENZIONE! Hai usato {percentuale:.1f}% del budget. Proiezione fine mese: €{proiezione:.2f}"
        else:
            delta = budget - proiezione
            if delta > 0:
                return f"🟢 Tutto ok! Proiezione: €{proiezione:.2f}. Risparmierai circa €{delta:.2f}"
            else:
                return f"🟡 Proiezione: €{proiezione:.2f}. Rischi di superare di €{abs(delta):.2f}"
    
    def _calcola_trend_mensile(self, spese: List[Spesa], mesi: int) -> str:
        """Calcola trend spese negli ultimi mesi"""
        if len(spese) < 2:
            return 'stabile'
        
        # Raggruppa per mese
        spese_per_mese = {}
        for spesa in spese:
            mese_key = spesa.data.strftime('%Y-%m')
            spese_per_mese[mese_key] = spese_per_mese.get(mese_key, 0) + spesa.importo
        
        if len(spese_per_mese) < 2:
            return 'stabile'
        
        # Calcola trend
        mesi_ordinati = sorted(spese_per_mese.keys())
        totale_primo = spese_per_mese[mesi_ordinati[0]]
        totale_ultimo = spese_per_mese[mesi_ordinati[-1]]
        
        if totale_ultimo > totale_primo * 1.2:
            return 'crescente'
        elif totale_ultimo < totale_primo * 0.8:
            return 'decrescente'
        else:
            return 'stabile'
    
    def esporta_spese_csv(
        self, 
        data_inizio: date, 
        data_fine: date
    ) -> str:
        """
        Esporta spese in formato CSV
        
        Args:
            data_inizio: Data inizio
            data_fine: Data fine
            
        Returns:
            Stringa CSV
        """
        spese = self._get_spese_periodo(data_inizio, data_fine)
        
        csv = "Data,Ora,Importo,Descrizione,Categoria,Necessaria,Metodo\n"
        
        for spesa in spese:
            csv += f"{spesa.data},{spesa.ora or ''},{spesa.importo},"
            csv += f"{spesa.descrizione},{spesa.categoria},"
            csv += f"{'Sì' if spesa.necessaria else 'No'},{spesa.metodo_pagamento or ''}\n"
        
        return csv
    
    def confronta_con_mese_scorso(self) -> Dict[str, Any]:
        """
        Confronta spese mese corrente con mese scorso
        
        Returns:
            Confronto dettagliato
        """
        oggi = date.today()
        
        # Questo mese
        primo_questo_mese = oggi.replace(day=1)
        spese_questo_mese = self.analizza_spese_periodo(primo_questo_mese, oggi)
        
        # Mese scorso
        ultimo_mese_scorso = primo_questo_mese - timedelta(days=1)
        primo_mese_scorso = ultimo_mese_scorso.replace(day=1)
        spese_mese_scorso = self.analizza_spese_periodo(primo_mese_scorso, ultimo_mese_scorso)
        
        # Confronto
        diff = spese_questo_mese['totale'] - spese_mese_scorso['totale']
        diff_perc = (diff / spese_mese_scorso['totale'] * 100) if spese_mese_scorso['totale'] > 0 else 0
        
        return {
            'mese_corrente': spese_questo_mese,
            'mese_scorso': spese_mese_scorso,
            'confronto': {
                'differenza': round(diff, 2),
                'differenza_percentuale': round(diff_perc, 1),
                'trend': 'aumento' if diff > 0 else 'diminuzione' if diff < 0 else 'stabile'
            }
        }

