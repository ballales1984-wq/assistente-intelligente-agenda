"""
Groq LLM Assistant - Velocissimo e gratuito!
"""

import os
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Import condizionale Groq
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    logger.warning("Groq non installato. Usa: pip install groq")


class GroqAssistant:
    """Assistente AI basato su Groq (velocissimo!)"""
    
    def __init__(self):
        self.client = None
        self.api_key = os.getenv('GROQ_API_KEY')
        
        if GROQ_AVAILABLE and self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                logger.info("✅ Groq client inizializzato")
            except Exception as e:
                logger.error(f"❌ Errore inizializzazione Groq: {e}")
        else:
            if not GROQ_AVAILABLE:
                logger.warning("⚠️ Groq non disponibile - installa: pip install groq")
            if not self.api_key:
                logger.warning("⚠️ GROQ_API_KEY non configurata - imposta variabile ambiente")
    
    def is_available(self) -> bool:
        """Verifica se Groq è disponibile"""
        return self.client is not None
    
    def chat(
        self,
        messaggio: str,
        system_prompt: Optional[str] = None,
        model: str = "llama-3.1-70b-versatile",
        max_tokens: int = 1024,
        temperature: float = 0.7,
        lang: str = 'it'
    ) -> Dict[str, Any]:
        """
        Chat con Groq LLM
        
        Modelli disponibili:
        - llama-3.1-70b-versatile (migliore, bilanciato)
        - llama-3.1-8b-instant (velocissimo)
        - mixtral-8x7b-32768 (context lungo)
        
        Args:
            messaggio: Messaggio utente
            system_prompt: Prompt di sistema (opzionale)
            model: Modello da usare
            max_tokens: Massimo token risposta
            temperature: Creatività (0-1)
            lang: Lingua ('it', 'en', 'es', etc.)
        
        Returns:
            Dict con risposta e metadata
        """
        if not self.is_available():
            return {
                "success": False,
                "error": "Groq non disponibile",
                "risposta": "⚠️ Chat AI non disponibile. Usa i comandi NLP standard!"
            }
        
        try:
            # System prompt personalizzato per lingua
            if not system_prompt:
                prompts = {
                    'it': "Sei un assistente personale intelligente. Aiuti l'utente a organizzare obiettivi, impegni, spese e diario. Rispondi in modo conciso e amichevole in italiano.",
                    'en': "You are a smart personal assistant. You help users organize goals, commitments, expenses, and diary. Reply concisely and friendly in English.",
                    'es': "Eres un asistente personal inteligente. Ayudas a los usuarios a organizar objetivos, compromisos, gastos y diario. Responde de forma concisa y amigable en español.",
                    'zh': "你是一个智能个人助手。你帮助用户组织目标、承诺、支出和日记。用中文简洁友好地回复。",
                    'ru': "Вы умный личный помощник. Вы помогаете пользователям организовать цели, обязательства, расходы и дневник. Отвечайте кратко и дружелюбно на русском языке.",
                    'ar': "أنت مساعد شخصي ذكي. تساعد المستخدمين على تنظيم الأهداف والالتزامات والنفقات واليوميات. أجب بإيجاز وودية بالعربية.",
                }
                system_prompt = prompts.get(lang, prompts['it'])
            
            # Chiamata Groq
            logger.info(f"🚀 Groq chat: model={model}, lang={lang}")
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": messaggio}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            risposta = response.choices[0].message.content
            
            # Metadata
            metadata = {
                "model": model,
                "tokens_used": response.usage.total_tokens,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "finish_reason": response.choices[0].finish_reason,
            }
            
            logger.info(f"✅ Groq risposta: {metadata['tokens_used']} tokens")
            
            return {
                "success": True,
                "risposta": risposta,
                "metadata": metadata,
                "provider": "groq"
            }
            
        except Exception as e:
            logger.error(f"❌ Errore Groq chat: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "risposta": "⚠️ Errore temporaneo. Riprova!"
            }
    
    def analizza_comando(
        self,
        messaggio: str,
        contesto: Optional[Dict] = None,
        lang: str = 'it'
    ) -> Dict[str, Any]:
        """
        Analizza comando complesso con AI
        Usato quando NLP regex fallisce
        
        Args:
            messaggio: Comando utente
            contesto: Contesto opzionale (obiettivi, impegni, etc.)
            lang: Lingua
        
        Returns:
            Dict con tipo, dati estratti, suggerimento
        """
        system_prompts = {
            'it': """Sei un parser intelligente di comandi per agenda.
Estrai da messaggi naturali: obiettivi, impegni, spese, riflessioni diario.

Rispondi SOLO JSON:
{
  "tipo": "obiettivo|impegno|spesa|diario|domanda",
  "dati": {...},
  "suggerimento": "..."
}""",
            'en': """You are a smart command parser for agenda.
Extract from natural messages: goals, commitments, expenses, diary reflections.

Reply ONLY JSON:
{
  "type": "goal|commitment|expense|diary|question",
  "data": {...},
  "suggestion": "..."
}""",
        }
        
        prompt = system_prompts.get(lang, system_prompts['it'])
        
        return self.chat(
            messaggio=messaggio,
            system_prompt=prompt,
            model="llama-3.1-8b-instant",  # Veloce per parsing
            max_tokens=256,
            temperature=0.3,  # Bassa temperatura per parsing preciso
            lang=lang
        )


# Istanza globale
groq_assistant = GroqAssistant()

