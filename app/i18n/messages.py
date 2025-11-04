"""Internationalization Messages"""

MESSAGES = {
    'it': {
        'no_events_today': 'Non ci sono impegni per oggi',
        'no_events_for': 'Non ci sono impegni per {}',
        'you_have_events': 'Hai {} impegni per {}',
        'from': 'dalle',
        'to': 'alle',
        'calm_days_to_recover': 'giorni più tranquilli per recuperare',
        'average': 'media',
        'loading': 'Caricamento...',
    },
    'en': {
        'no_events_today': 'No events for today',
        'no_events_for': 'No events for {}',
        'you_have_events': 'You have {} events for {}',
        'from': 'from',
        'to': 'to',
        'calm_days_to_recover': 'calmer days to recover',
        'average': 'average',
        'loading': 'Loading...',
    },
    'es': {
        'no_events_today': 'No hay eventos para hoy',
        'no_events_for': 'No hay eventos para {}',
        'you_have_events': 'Tienes {} eventos para {}',
        'from': 'desde',
        'to': 'hasta',
        'calm_days_to_recover': 'días más tranquilos para recuperar',
        'average': 'promedio',
        'loading': 'Cargando...',
    },
    'zh': {
        'no_events_today': '今天没有活动',
        'no_events_for': '没有活动 {}',
        'you_have_events': '你有 {} 个活动 {}',
        'from': '从',
        'to': '到',
        'calm_days_to_recover': '更平静的日子来恢复',
        'average': '平均',
        'loading': '加载中...',
    },
    'ru': {
        'no_events_today': 'Сегодня нет событий',
        'no_events_for': 'Нет событий на {}',
        'you_have_events': 'У вас {} событий на {}',
        'from': 'с',
        'to': 'до',
        'calm_days_to_recover': 'более спокойные дни для восстановления',
        'average': 'средний',
        'loading': 'Загрузка...',
    },
    'hi': {
        'no_events_today': 'आज कोई कार्यक्रम नहीं',
        'no_events_for': '{} के लिए कोई कार्यक्रम नहीं',
        'you_have_events': 'आपके पास {} कार्यक्रम हैं {}',
        'from': 'से',
        'to': 'तक',
        'calm_days_to_recover': 'ठीक होने के लिए शांत दिन',
        'average': 'औसत',
        'loading': 'लोड हो रहा है...',
    },
    'ar': {
        'no_events_today': 'لا توجد أحداث اليوم',
        'no_events_for': 'لا توجد أحداث ل {}',
        'you_have_events': 'لديك {} أحداث ل {}',
        'from': 'من',
        'to': 'إلى',
        'calm_days_to_recover': 'أيام أكثر هدوءاً للتعافي',
        'average': 'متوسط',
        'loading': 'جار التحميل...',
    }
}

def get_message(key, lang='it', *args):
    """Get translated message"""
    messages = MESSAGES.get(lang, MESSAGES['it'])
    message = messages.get(key, MESSAGES['it'].get(key, key))
    
    if args:
        return message.format(*args)
    return message


def detect_language_from_path(path):
    """Detect language from URL path"""
    if '/en' in path:
        return 'en'
    elif '/es' in path:
        return 'es'
    elif '/zh' in path:
        return 'zh'
    elif '/ru' in path:
        return 'ru'
    elif '/hi' in path:
        return 'hi'
    elif '/ar' in path:
        return 'ar'
    else:
        return 'it'

