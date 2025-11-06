"""
Internationalization (i18n) module for multilingual support
"""

TRANSLATIONS = {
    'it': {
        # Risposte Chat
        'goal_created': "✅ Perfetto! Ho aggiunto l'obiettivo '{nome}' con {ore}h/settimana ({tipo}).",
        'commitment_created': "✅ Perfetto! Ho aggiunto l'impegno '{nome}' il {data} dalle {ora_inizio} alle {ora_fine}.",
        'expense_created': "✅ Perfetto! Ho registrato la spesa di €{importo} per '{descrizione}' (categoria: {categoria}).",
        'diary_created': "✅ Perfetto! Ho aggiunto la tua riflessione al diario. Sentiment rilevato: {sentiment}",
        
        # Errori
        'empty_message': "Messaggio vuoto",
        'profile_not_found': "Nessun profilo trovato",
        'invalid_data': "Dati non validi",
        'error_creating': "Errore durante la creazione",
        
        # Modifiche impegni
        'commitment_split': "✂️ **Spezzato:** '{nome}' ({vecchio})",
        'commitment_reduced': "📏 **Ridotto:** '{nome}' da {vecchio} a {nuovo}",
        'commitment_deleted': "🗑️ **Eliminato:** '{nome}' ({orario})",
        
        # Messaggi generali
        'loading': "Caricamento...",
        'no_goals': "Nessun obiettivo ancora. Inizia a parlare con l'assistente!",
        'no_entries': "Nessuna riflessione ancora. Scrivi nella chat!",
        'no_expenses': "Nessuna spesa registrata",
        'generate_plan': "Genera il tuo piano!",
        'error_occurred': "Si è verificato un errore. Riprova.",
        
        # Bottoni
        'refresh': "Aggiorna",
        'send': "Invia",
        'cancel': "Annulla",
        'confirm': "Conferma",
        'delete': "Elimina",
        
        # Labels
        'goals': "Obiettivi",
        'hours_completed': "Ore completate",
        'completion': "Completamento",
        'today': "Oggi",
        'this_week': "Questa Settimana",
        'this_month': "Questo Mese",
    },
    
    'en': {
        # Chat Responses
        'goal_created': "✅ Perfect! I've added the goal '{nome}' with {ore}h/week ({tipo}).",
        'commitment_created': "✅ Perfect! I've added the commitment '{nome}' on {data} from {ora_inizio} to {ora_fine}.",
        'expense_created': "✅ Perfect! I've recorded the expense of ${importo} for '{descrizione}' (category: {categoria}).",
        'diary_created': "✅ Perfect! I've added your reflection to the diary. Detected sentiment: {sentiment}",
        
        # Errors
        'empty_message': "Empty message",
        'profile_not_found': "No profile found",
        'invalid_data': "Invalid data",
        'error_creating': "Error during creation",
        
        # Commitment modifications
        'commitment_split': "✂️ **Split:** '{nome}' ({vecchio})",
        'commitment_reduced': "📏 **Reduced:** '{nome}' from {vecchio} to {nuovo}",
        'commitment_deleted': "🗑️ **Deleted:** '{nome}' ({orario})",
        
        # General messages
        'loading': "Loading...",
        'no_goals': "No goals yet. Start talking with the assistant!",
        'no_entries': "No reflections yet. Write in the chat!",
        'no_expenses': "No expenses recorded",
        'generate_plan': "Generate your plan!",
        'error_occurred': "An error occurred. Please try again.",
        
        # Buttons
        'refresh': "Refresh",
        'send': "Send",
        'cancel': "Cancel",
        'confirm': "Confirm",
        'delete': "Delete",
        
        # Labels
        'goals': "Goals",
        'hours_completed': "Hours completed",
        'completion': "Completion",
        'today': "Today",
        'this_week': "This Week",
        'this_month': "This Month",
    }
}


def get_text(key: str, lang: str = 'it', **kwargs) -> str:
    """
    Get translated text for a given key
    
    Args:
        key: Translation key
        lang: Language code ('it', 'en', 'es', etc.)
        **kwargs: Variables to format into the text
    
    Returns:
        Translated and formatted text
    """
    # Fallback to Italian if language not found
    if lang not in TRANSLATIONS:
        lang = 'it'
    
    # Get translation
    text = TRANSLATIONS.get(lang, {}).get(key, key)
    
    # Format with provided variables
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass  # If formatting fails, return unformatted text
    
    return text


def detect_language_from_path(path: str) -> str:
    """
    Detect language from URL path
    
    Args:
        path: Request path (e.g., '/en/community', '/api/chat')
    
    Returns:
        Language code ('it', 'en', 'es', etc.)
    """
    path_parts = path.strip('/').split('/')
    
    # Check if first part is a language code
    if len(path_parts) > 0 and path_parts[0] in ['en', 'es', 'zh', 'ru', 'hi', 'ar']:
        return path_parts[0]
    
    # Default to Italian
    return 'it'

