"""
Ollama LLM Integration - AI Assistant Locale
Usa modelli LLM locali tramite Ollama (zero costi API!)
"""
import ollama
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, date


class OllamaAssistant:
    """
    Assistente AI alimentato da Ollama (LLM locale)
    
    Features:
    - Conversazioni naturali
    - Suggerimenti intelligenti basati su contesto
    - Analisi dati utente
    - Planning assistito
    - Zero costi API
    - 100% privacy (tutto locale)
    """
    
    def __init__(self, model: str = 'llama2'):
        """
        Args:
            model: Nome modello Ollama (llama2, mistral, phi, gemma, etc.)
        """
        self.model = model
        self.conversation_history = []
    
    def chat(self, user_message: str, context: Dict[str, Any] = None) -> str:
        """
        Conversazione naturale con l'utente
        
        Args:
            user_message: Messaggio dell'utente
            context: Contesto utente (obiettivi, impegni, spese, etc.)
            
        Returns:
            Risposta dell'assistente
        """
        # Costruisci prompt con contesto
        system_prompt = self._build_system_prompt(context or {})
        
        # Prepara messaggio completo
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ]
        
        try:
            # Chiamata a Ollama
            response = ollama.chat(
                model=self.model,
                messages=messages
            )
            
            assistant_message = response['message']['content']
            
            # Salva conversazione per contesto futuro
            self.conversation_history.append({
                'user': user_message,
                'assistant': assistant_message,
                'timestamp': datetime.now().isoformat()
            })
            
            return assistant_message
            
        except Exception as e:
            return f"Mi dispiace, ho avuto un problema tecnico: {str(e)}\nProva a riformulare la domanda!"
    
    def suggest_weekly_plan(self, user_profile, obiettivi: List[Dict], impegni: List[Dict]) -> str:
        """
        Genera suggerimenti per piano settimanale ottimale
        
        Args:
            user_profile: Profilo utente con preferenze
            obiettivi: Lista obiettivi attivi
            impegni: Lista impegni fissi
            
        Returns:
            Piano settimanale suggerito (testo)
        """
        context = {
            'profilo': {
                'stile_vita': user_profile.stile_vita,
                'stress_tollerato': user_profile.stress_tollerato,
                'ore_disponibili': f"{user_profile.ora_inizio_giornata}-{user_profile.ora_fine_giornata}"
            },
            'obiettivi': [{'nome': o['nome'], 'ore': o['durata_settimanale']} for o in obiettivi],
            'impegni_fissi': len(impegni)
        }
        
        prompt = f"""
        Sei un assistente per la pianificazione personale.
        
        Utente:
        - Stile vita: {context['profilo']['stile_vita']}
        - Stress tollerato: {context['profilo']['stress_tollerato']}
        - Ore giornaliere: {context['profilo']['ore_disponibili']}
        
        Obiettivi attivi:
        {json.dumps(context['obiettivi'], indent=2, ensure_ascii=False)}
        
        Impegni fissi questa settimana: {context['impegni_fissi']}
        
        Genera un piano settimanale ottimale che:
        1. Distribuisce le ore degli obiettivi in modo bilanciato
        2. Considera lo stile di vita dell'utente
        3. Include pause e momenti di riposo
        4. Rispetta i limiti di stress
        
        Rispondi in italiano, in modo amichevole e motivante!
        """
        
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt
            )
            return response['response']
        except Exception as e:
            return f"Non riesco a generare il piano al momento. Errore: {str(e)}"
    
    def analyze_productivity(self, historical_data: Dict[str, Any]) -> str:
        """
        Analizza produttività basandosi su dati storici
        
        Args:
            historical_data: Dati storici (impegni passati, completamenti, etc.)
            
        Returns:
            Analisi e suggerimenti
        """
        prompt = f"""
        Analizza questi dati di produttività:
        
        {json.dumps(historical_data, indent=2, ensure_ascii=False)}
        
        Fornisci:
        1. Pattern identificati (es. "Sei più produttivo al mattino")
        2. Anomalie o comportamenti insoliti
        3. Suggerimenti concreti per migliorare
        4. Aree di forza e debolezza
        
        Rispondi in italiano, in modo costruttivo e motivante!
        """
        
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt
            )
            return response['response']
        except Exception as e:
            return f"Analisi non disponibile: {str(e)}"
    
    def smart_categorization(self, description: str, amount: float) -> Dict[str, Any]:
        """
        Categorizzazione intelligente spese usando LLM
        
        Args:
            description: Descrizione spesa
            amount: Importo
            
        Returns:
            Categoria suggerita + reasoning
        """
        categorie = ['Cibo', 'Trasporti', 'Svago', 'Salute', 'Casa', 
                    'Abbigliamento', 'Tecnologia', 'Istruzione', 'Regali', 'Altro']
        
        prompt = f"""
        Categorizza questa spesa:
        Descrizione: "{description}"
        Importo: €{amount}
        
        Categorie disponibili: {', '.join(categorie)}
        
        Rispondi SOLO con JSON:
        {{
            "categoria": "categoria scelta",
            "confidence": "alta/media/bassa",
            "reasoning": "breve spiegazione"
        }}
        """
        
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt
            )
            
            # Parse JSON dalla risposta
            result = json.loads(response['response'])
            return result
        except:
            # Fallback: usa categorizzazione base
            from app.managers.spese_manager import SpeseManager
            categoria = SpeseManager(None).categorizza_spesa(description)
            return {
                'categoria': categoria,
                'confidence': 'media',
                'reasoning': 'Categorizzazione automatica base'
            }
    
    def expand_vague_input(self, vague_input: str) -> Dict[str, Any]:
        """
        Espande input vaghi chiedendo dettagli
        
        Args:
            vague_input: Input poco chiaro (es. "Palestra")
            
        Returns:
            Domande di chiarimento + suggerimenti
        """
        prompt = f"""
        L'utente ha scritto: "{vague_input}"
        
        Questo input è troppo vago per essere processato automaticamente.
        
        Genera:
        1. Una domanda amichevole per chiarire l'intento
        2. 2-3 esempi di come riformulare
        
        Rispondi in italiano, in modo utile e amichevole!
        
        Formato JSON:
        {{
            "domanda": "...",
            "esempi": ["esempio 1", "esempio 2", "esempio 3"]
        }}
        """
        
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt
            )
            return json.loads(response['response'])
        except:
            return {
                'domanda': "Puoi essere più specifico? 🤔",
                'esempi': [
                    "Se è un impegno: 'Domani palestra 18-19'",
                    "Se è un obiettivo: 'Palestra 3 ore a settimana'",
                    "Se è una nota: 'Oggi sono andato in palestra'"
                ]
            }
    
    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Costruisce system prompt con contesto utente"""
        
        base_prompt = """
        Sei l'assistente intelligente di Wallmind Agenda.
        Aiuti l'utente a gestire obiettivi, impegni, spese e vita quotidiana.
        
        Caratteristiche:
        - Rispondi sempre in italiano
        - Sii amichevole, pratico e motivante
        - Dai suggerimenti concreti e attuabili
        - Usa emoji appropriati (ma senza esagerare)
        - Sii conciso ma completo
        """
        
        if context:
            base_prompt += f"""
            
            Contesto utente corrente:
            """
            
            if context.get('obiettivi'):
                base_prompt += f"\nObiettivi attivi: {len(context['obiettivi'])}"
                for obj in context.get('obiettivi', [])[:3]:
                    base_prompt += f"\n  - {obj.get('nome', 'N/A')}"
            
            if context.get('impegni_oggi'):
                base_prompt += f"\nImpegni oggi: {len(context['impegni_oggi'])}"
            
            if context.get('spese_oggi'):
                totale = sum(s.get('importo', 0) for s in context.get('spese_oggi', []))
                base_prompt += f"\nSpese oggi: €{totale:.2f}"
            
            if context.get('sentiment_recente'):
                base_prompt += f"\nUmore recente: {context['sentiment_recente']}"
        
        return base_prompt


class OllamaManager:
    """Manager per operazioni Ollama (download modelli, health check, etc.)"""
    
    @staticmethod
    def check_ollama_running() -> bool:
        """Verifica se Ollama è in esecuzione"""
        try:
            ollama.list()
            return True
        except:
            return False
    
    @staticmethod
    def list_available_models() -> List[str]:
        """Lista modelli disponibili localmente"""
        try:
            models = ollama.list()
            if hasattr(models, 'models'):
                return [m.model for m in models.models]
            return []
        except:
            return []
    
    @staticmethod
    def pull_model(model_name: str) -> bool:
        """
        Scarica un modello se non presente
        
        Modelli consigliati:
        - llama2 (7B) - General purpose, buono
        - mistral (7B) - Veloce e accurato
        - phi (3B) - Piccolo e veloce
        - gemma (7B) - Google, ottimo per ragionamento
        """
        try:
            print(f"📥 Downloading {model_name}... (può richiedere qualche minuto)")
            ollama.pull(model_name)
            print(f"✅ {model_name} scaricato!")
            return True
        except Exception as e:
            print(f"❌ Errore download: {e}")
            return False
    
    @staticmethod
    def recommend_model() -> str:
        """Raccomanda modello migliore basato su sistema"""
        models = OllamaManager.list_available_models()
        
        # Preferenze in ordine
        preferred = ['mistral', 'llama2', 'phi', 'gemma']
        
        for model in preferred:
            if any(model in m for m in models):
                return model
        
        # Se nessuno disponibile, raccomanda mistral (best balance)
        return 'mistral'

