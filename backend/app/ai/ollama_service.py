"""
Ollama AI Integration - FastAPI version
"""
import httpx
import json
from typing import Optional
from config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """Sei un assistente AI per la produttività personale. Il tuo nome è "Assistente Intelligente".
Aiuti le persone a organizzare agenda, obiettivi, diario e spese.

Puoi:
1. Creare obiettivi ("Voglio studiare Python 3 ore a settimana")
2. Aggiungere impegni ("Lunedì riunione dalle 10 alle 12")
3. Scrivere nel diario ("Oggi ho parlato con Sara, mi sento motivato!")
4. Registrare spese ("Speso 50€ per spesa")
5. Dare consigli sulla produttività

Rispondi in modo breve, amichevole e diretto. Usa emoji quando appropriato.
Se l'utente ti chiede di fare qualcosa che puoi fare, indica l'azione con un tag:
[ACTION:tipo] dove tipo è: obiettivo, impegno, diario, spesa

Esempio: "Perfetto! Ho registrato il tuo obiettivo 🎯 [ACTION:obiettivo]"
"""


async def chat_with_ollama(message: str, context: dict = None) -> dict:
    """
    Chiama Ollama per la chat AI.
    Falls back a risposta generica se Ollama non è disponibile.
    """
    user_context = ""
    if context:
        if context.get("obiettivi"):
            names = [o["nome"] for o in context["obiettivi"][:5]]
            user_context += f"\nObiettivi attivi: {', '.join(names)}"
        if context.get("impegni"):
            user_context += f"\nImpegni oggi: {len(context['impegni'])}"
    
    full_system = SYSTEM_PROMPT + user_context
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{settings.ollama_host}/api/chat",
                json={
                    "model": settings.ollama_model,
                    "messages": [
                        {"role": "system", "content": full_system},
                        {"role": "user", "content": message}
                    ],
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data["message"]["content"]
                
                # Estrai action se presente
                suggestions = extract_suggestions(ai_response)
                
                return {
                    "response": ai_response,
                    "suggestions": suggestions
                }
    except Exception as e:
        pass
    
    # Fallback: risposta intelligente senza AI
    return fallback_response(message)


def extract_suggestions(response: str) -> list:
    """Estrai suggerimenti dalla risposta AI"""
    suggestions = []
    if "[ACTION:obiettivo]" in response:
        suggestions.append("obiettivo")
    if "[ACTION:impegno]" in response:
        suggestions.append("impegno")
    if "[ACTION:diario]" in response:
        suggestions.append("diario")
    if "[ACTION:spesa]" in response:
        suggestions.append("spesa")
    return suggestions


def fallback_response(message: str) -> dict:
    """Risposta intelligente senza AI (quando Ollama non è disponibile)"""
    msg = message.lower()
    
    # Riconoscimento intento
    if any(w in msg for w in ["obiettivo", "voglio", "goal", "target", "imparare"]):
        return {
            "response": "🎯 Capito! Vuoi creare un nuovo obiettivo. Dimmi:\n- Nome dell'obiettivo\n- Quante ore a settimana vuoi dedicarci\n- Tipo (studio, sport, progetto, personale, lavoro)",
            "suggestions": ["obiettivo"]
        }
    
    if any(w in msg for w in ["impegno", "riunione", "appuntamento", "meeting", "alle", "dalle"]):
        return {
            "response": "📅 Vuoi aggiungere un impegno! Dimmi:\n- Cosa devi fare\n- Quando (data e ora)\n- Durata",
            "suggestions": ["impegno"]
        }
    
    if any(w in msg for w in ["diario", "giorno", "sentono", "sentito", "emozione", "oggi ho"]):
        return {
            "response": "📖 Vuoi scrivere nel diario! Raccontami la tua giornata o come ti senti.",
            "suggestions": ["diario"]
        }
    
    if any(w in msg for w in ["speso", "spesa", "euro", "€", "pagato", "acquisto"]):
        return {
            "response": "💰 Vuoi registrare una spesa! Dimmi:\n- Quanto hai speso\n- Per cosa\n- Categoria (cibo, trasporti, svago, salute, casa, etc.)",
            "suggestions": ["spesa"]
        }
    
    if any(w in msg for w in ["ciao", "hey", "hello", "buongiorno", "buonasera"]):
        return {
            "response": "Ciao! 👋 Sono il tuo assistente intelligente. Posso aiutarti con:\n\n🎯 Obiettivi\n📅 Agenda\n📖 Diario\n💰 Spese\n\nCosa vuoi fare oggi?",
            "suggestions": []
        }
    
    return {
        "response": "🤔 Non ho capito perfettamente. Puoi provare a:\n- Creare un obiettivo: \"Voglio studiare 3 ore a settimana\"\n- Aggiungere un impegno: \"Riunione lunedì dalle 10 alle 12\"\n- Scrivere nel diario: \"Oggi è stata una bella giornata\"\n- Registrare una spesa: \"Speso 30€ al supermercato\"",
        "suggestions": []
    }
