"""AI-Enhanced Chat usando Ollama"""
from flask import Blueprint, request, jsonify
from app.models import UserProfile, Obiettivo, Impegno, Spesa
from app.ai.ollama_assistant import OllamaAssistant, OllamaManager
from datetime import date, timedelta

bp = Blueprint('ai_chat', __name__)


@bp.route('/api/chat/ai', methods=['POST'])
def chat_with_ai():
    """
    Chat potenziata con LLM locale (Ollama)
    Usa questo per domande complesse o conversazioni naturali
    """
    data = request.json
    messaggio = data.get('messaggio', '').strip()
    
    if not messaggio:
        return jsonify({'errore': 'Messaggio vuoto'}), 400
    
    # Verifica Ollama disponibile
    if not OllamaManager.check_ollama_running():
        return jsonify({
            'errore': 'Ollama non disponibile',
            'messaggio': 'Avvia Ollama con: ollama serve'
        }), 503
    
    # Get user context
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Profilo non trovato'}), 404
    
    # Build context
    oggi = date.today()
    context = {
        'obiettivi': [o.to_dict() for o in profilo.obiettivi.filter_by(attivo=True).limit(5).all()],
        'impegni_oggi': [
            i.to_dict() for i in profilo.impegni.filter(
                Impegno.data_inizio >= oggi,
                Impegno.data_inizio < oggi + timedelta(days=1)
            ).limit(10).all()
        ],
        'spese_oggi': [
            s.to_dict() for s in profilo.spese.filter(
                Spesa.data == oggi
            ).limit(10).all()
        ]
    }
    
    # Get best available model (preferisci più piccolo per velocità)
    models = OllamaManager.list_available_models()
    model_to_use = 'gemma3:1b'  # Più piccolo = più veloce
    
    # Se user specifica modello preferito
    preferred_model = data.get('model')
    if preferred_model and preferred_model in models:
        model_to_use = preferred_model
    elif 'llama3.2' in str(models):
        model_to_use = 'llama3.2:latest'
    
    # Create assistant
    assistant = OllamaAssistant(model=model_to_use)
    
    try:
        # Get AI response
        risposta_ai = assistant.chat(messaggio, context)
        
        return jsonify({
            'messaggio': messaggio,
            'risposta': risposta_ai,
            'model_used': model_to_use,
            'ai_powered': True,
            'local': True,  # 100% locale, zero costi!
            'context_items': len(context['obiettivi']) + len(context['impegni_oggi']) + len(context['spese_oggi'])
        })
        
    except Exception as e:
        return jsonify({
            'errore': f'Errore AI: {str(e)}',
            'fallback': 'Usa /api/chat normale per input strutturati'
        }), 500


@bp.route('/api/ai/suggest-plan', methods=['POST'])
def suggest_weekly_plan():
    """Genera piano settimanale con AI"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Profilo non trovato'}), 404
    
    obiettivi = [o.to_dict() for o in profilo.obiettivi.filter_by(attivo=True).all()]
    impegni = [i.to_dict() for i in profilo.impegni.limit(20).all()]
    
    # Use gemma (fast)
    assistant = OllamaAssistant(model='gemma3:1b')
    
    try:
        piano = assistant.suggest_weekly_plan(profilo, obiettivi, impegni)
        
        return jsonify({
            'piano': piano,
            'model_used': 'gemma3:1b',
            'generated_at': date.today().isoformat()
        })
    except Exception as e:
        return jsonify({'errore': str(e)}), 500


@bp.route('/api/ai/analyze-productivity', methods=['GET'])
def analyze_productivity_ai():
    """Analisi produttività con AI"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Profilo non trovato'}), 404
    
    # Gather historical data
    impegni_settimana = profilo.impegni.filter(
        Impegno.data_inizio >= date.today() - timedelta(days=7)
    ).all()
    
    historical_data = {
        'impegni_completati': len(impegni_settimana),
        'ore_totali': sum(
            (i.data_fine - i.data_inizio).total_seconds() / 3600 
            for i in impegni_settimana
        ),
        'distribuzione_tipo': {}
    }
    
    for imp in impegni_settimana:
        historical_data['distribuzione_tipo'][imp.tipo] = \
            historical_data['distribuzione_tipo'].get(imp.tipo, 0) + 1
    
    assistant = OllamaAssistant(model='llama3.2:latest')
    
    try:
        analisi = assistant.analyze_productivity(historical_data)
        
        return jsonify({
            'analisi': analisi,
            'data': historical_data,
            'model_used': 'llama3.2:latest'
        })
    except Exception as e:
        return jsonify({'errore': str(e)}), 500


@bp.route('/api/ai/models', methods=['GET'])
def list_ai_models():
    """Lista modelli Ollama disponibili"""
    try:
        models = OllamaManager.list_available_models()
        return jsonify({
            'available_models': models,
            'recommended': 'gemma3:1b',  # Più veloce
            'ollama_running': OllamaManager.check_ollama_running()
        })
    except Exception as e:
        return jsonify({'errore': str(e)}), 500

