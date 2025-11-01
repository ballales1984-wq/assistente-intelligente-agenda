"""
Pattern Recognition & Predictive Analytics
Analizza comportamenti utente e genera suggestions intelligenti
"""
from datetime import datetime, timedelta, date
from collections import defaultdict, Counter
from typing import List, Dict, Any
import numpy as np


class PatternRecognizer:
    """
    Riconosce pattern ricorrenti nei dati utente
    Features:
    - Routine detection
    - Anomaly detection
    - Time optimization suggestions
    - Productivity patterns
    """
    
    def __init__(self, user_profile):
        self.user_profile = user_profile
    
    def detect_routines(self, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Rileva routine ricorrenti (es. "Ogni lunedì alle 9 studio Python")
        
        Returns:
            List of detected routines with confidence scores
        """
        from app.models import Impegno
        
        # Get impegni ultimi N giorni
        data_inizio = date.today() - timedelta(days=days_back)
        impegni = self.user_profile.impegni.filter(
            Impegno.data_inizio >= data_inizio
        ).all()
        
        if not impegni:
            return []
        
        # Group by (day_of_week, hour, tipo)
        patterns = defaultdict(list)
        
        for impegno in impegni:
            day_of_week = impegno.data_inizio.weekday()  # 0=Monday
            hour = impegno.data_inizio.hour
            tipo = impegno.tipo
            
            key = (day_of_week, hour, tipo)
            patterns[key].append(impegno)
        
        # Find recurring patterns (appeared 3+ times)
        routines = []
        giorni_settimana = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']
        
        for (day, hour, tipo), impegni_list in patterns.items():
            if len(impegni_list) >= 3:
                # Calculate confidence based on frequency
                confidence = min(len(impegni_list) / (days_back / 7), 1.0)
                
                # Get average duration
                durations = [(imp.data_fine - imp.data_inizio).total_seconds() / 3600 
                           for imp in impegni_list]
                avg_duration = np.mean(durations)
                
                routines.append({
                    'day_of_week': giorni_settimana[day],
                    'day_num': day,
                    'hour': hour,
                    'tipo': tipo,
                    'frequency': len(impegni_list),
                    'confidence': round(confidence, 2),
                    'avg_duration_hours': round(avg_duration, 1),
                    'suggestion': f"Ogni {giorni_settimana[day]} alle {hour}:00 dedichi ~{round(avg_duration, 1)}h a '{tipo}'"
                })
        
        # Sort by confidence
        routines.sort(key=lambda x: x['confidence'], reverse=True)
        
        return routines
    
    def detect_anomalies(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """
        Rileva anomalie nel comportamento (es. "Oggi hai studiato molto meno del solito")
        
        Returns:
            List of detected anomalies with severity
        """
        from app.models import Impegno, Spesa
        
        anomalies = []
        oggi = date.today()
        
        # Analizza ore dedicate per tipo
        data_inizio = oggi - timedelta(days=days_back)
        impegni_periodo = self.user_profile.impegni.filter(
            Impegno.data_inizio >= data_inizio
        ).all()
        
        # Group by tipo and calculate daily averages
        ore_per_tipo_per_giorno = defaultdict(lambda: defaultdict(float))
        
        for impegno in impegni_periodo:
            giorno = impegno.data_inizio.date()
            tipo = impegno.tipo
            ore = (impegno.data_fine - impegno.data_inizio).total_seconds() / 3600
            ore_per_tipo_per_giorno[tipo][giorno] += ore
        
        # Check for anomalies (oggi vs media)
        for tipo, giorni in ore_per_tipo_per_giorno.items():
            if oggi in giorni:
                ore_oggi = giorni[oggi]
                ore_altri_giorni = [h for d, h in giorni.items() if d != oggi]
                
                if len(ore_altri_giorni) >= 3:
                    media = np.mean(ore_altri_giorni)
                    std = np.std(ore_altri_giorni)
                    
                    # Anomaly if > 2 standard deviations from mean
                    if std > 0:
                        z_score = (ore_oggi - media) / std
                        
                        if abs(z_score) > 2:
                            severity = 'alta' if abs(z_score) > 3 else 'media'
                            direction = 'più' if z_score > 0 else 'meno'
                            
                            anomalies.append({
                                'tipo': tipo,
                                'ore_oggi': round(ore_oggi, 1),
                                'ore_media': round(media, 1),
                                'z_score': round(z_score, 2),
                                'severity': severity,
                                'message': f"Oggi hai dedicato {direction} tempo del solito a '{tipo}' ({round(ore_oggi, 1)}h vs media {round(media, 1)}h)"
                            })
        
        # Analizza spese
        spese_oggi = self.user_profile.spese.filter(Spesa.data == oggi).all()
        totale_oggi = sum(s.importo for s in spese_oggi)
        
        # Compare con media ultimi 7 giorni
        spese_periodo = self.user_profile.spese.filter(
            Spesa.data >= data_inizio,
            Spesa.data < oggi
        ).all()
        
        if spese_periodo:
            spese_per_giorno = defaultdict(float)
            for s in spese_periodo:
                spese_per_giorno[s.data] += s.importo
            
            media_spese = np.mean(list(spese_per_giorno.values()))
            
            if totale_oggi > media_spese * 2:
                anomalies.append({
                    'tipo': 'spese',
                    'importo_oggi': round(totale_oggi, 2),
                    'importo_media': round(media_spese, 2),
                    'severity': 'alta' if totale_oggi > media_spese * 3 else 'media',
                    'message': f"⚠️ Spese oggi molto superiori alla media (€{totale_oggi:.2f} vs €{media_spese:.2f})"
                })
        
        return anomalies
    
    def suggest_optimizations(self) -> List[Dict[str, Any]]:
        """
        Genera suggerimenti per ottimizzare la giornata
        
        Returns:
            List of actionable suggestions
        """
        suggestions = []
        
        # Trova routine
        routines = self.detect_routines(days_back=30)
        
        if routines:
            # Suggerisci di automatizzare routine
            for routine in routines[:3]:  # Top 3
                if routine['confidence'] > 0.7:
                    suggestions.append({
                        'type': 'routine_automation',
                        'priority': 'alta',
                        'message': f"💡 Hai una routine fissa: {routine['suggestion']}. Vuoi che la aggiunga automaticamente?",
                        'action': 'create_recurring_event',
                        'data': routine
                    })
        
        # Trova slot liberi
        oggi = date.today()
        impegni_oggi = self.user_profile.impegni.filter(
            Impegno.data_inizio >= datetime.combine(oggi, datetime.min.time()),
            Impegno.data_inizio < datetime.combine(oggi + timedelta(days=1), datetime.min.time())
        ).order_by(Impegno.data_inizio).all()
        
        if impegni_oggi:
            # Trova gap tra impegni
            for i in range(len(impegni_oggi) - 1):
                gap = (impegni_oggi[i+1].data_inizio - impegni_oggi[i].data_fine).total_seconds() / 3600
                
                if gap > 2:  # Gap > 2 ore
                    suggestions.append({
                        'type': 'free_time',
                        'priority': 'media',
                        'message': f"⏰ Hai {gap:.1f}h libere tra {impegni_oggi[i].data_fine.strftime('%H:%M')} e {impegni_oggi[i+1].data_inizio.strftime('%H:%M')}. Suggerimento: pausa rilassante o obiettivo veloce?",
                        'gap_hours': gap,
                        'start': impegni_oggi[i].data_fine.isoformat(),
                        'end': impegni_oggi[i+1].data_inizio.isoformat()
                    })
        
        # Analizza bilanciamento vita-lavoro
        impegni_settimana = self.user_profile.impegni.filter(
            Impegno.data_inizio >= datetime.combine(oggi - timedelta(days=7), datetime.min.time())
        ).all()
        
        ore_per_tipo = defaultdict(float)
        for imp in impegni_settimana:
            ore = (imp.data_fine - imp.data_inizio).total_seconds() / 3600
            ore_per_tipo[imp.tipo] += ore
        
        total_ore = sum(ore_per_tipo.values())
        if total_ore > 0:
            # Check balance
            lavoro_ore = ore_per_tipo.get('lavoro', 0) + ore_per_tipo.get('studio', 0)
            svago_ore = ore_per_tipo.get('svago', 0) + ore_per_tipo.get('sport', 0)
            
            if lavoro_ore / total_ore > 0.8:  # > 80% lavoro
                suggestions.append({
                    'type': 'work_life_balance',
                    'priority': 'alta',
                    'message': f"⚖️ Attenzione: {lavoro_ore/total_ore*100:.0f}% del tuo tempo è dedicato a lavoro/studio. Considera di aggiungere più attività rilassanti!",
                    'lavoro_percent': round(lavoro_ore/total_ore*100, 1)
                })
        
        return suggestions
    
    def predict_productivity(self, target_date: date = None) -> Dict[str, Any]:
        """
        Predice il livello di produttività per una data
        
        Args:
            target_date: Data da analizzare (default: domani)
            
        Returns:
            Prediction con confidence e suggerimenti
        """
        if target_date is None:
            target_date = date.today() + timedelta(days=1)
        
        # Analizza produttività storica per stesso giorno settimana
        day_of_week = target_date.weekday()
        
        from app.models import Obiettivo, Impegno
        from sqlalchemy import func
        
        # Get historical data for same weekday
        impegni_passati = self.user_profile.impegni.filter(
            func.strftime('%w', Impegno.data_inizio) == str((day_of_week + 1) % 7)
        ).all()
        
        if len(impegni_passati) < 3:
            return {
                'productivity_score': 0.5,
                'confidence': 'bassa',
                'message': "Dati insufficienti per predizione accurata",
                'recommendation': "Continua a usare l'app per migliorare le predizioni!"
            }
        
        # Calculate average hours and completion rate for that weekday
        avg_hours = np.mean([(i.data_fine - i.data_inizio).total_seconds() / 3600 for i in impegni_passati])
        
        # Productivity score based on completion and time invested
        productivity_score = min(avg_hours / 8, 1.0)  # Normalize to 0-1
        
        level = 'alta' if productivity_score > 0.7 else 'media' if productivity_score > 0.4 else 'bassa'
        
        return {
            'target_date': target_date.isoformat(),
            'day_of_week': ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica'][day_of_week],
            'productivity_score': round(productivity_score, 2),
            'productivity_level': level,
            'avg_hours_historical': round(avg_hours, 1),
            'confidence': 'alta' if len(impegni_passati) > 10 else 'media',
            'message': f"Previsione produttività per {target_date.strftime('%d/%m')}: {level.upper()}",
            'recommendation': self._get_productivity_recommendation(productivity_score)
        }
    
    def _get_productivity_recommendation(self, score: float) -> str:
        """Get recommendation based on productivity score"""
        if score > 0.7:
            return "Ottimo! Giornata produttiva in arrivo. Sfruttala per obiettivi importanti!"
        elif score > 0.4:
            return "Giornata nella media. Pianifica attività moderate e lascia spazio per imprevisti."
        else:
            return "Giornata potenzialmente leggera. Perfetta per pause, riflessioni e ricarica!"

