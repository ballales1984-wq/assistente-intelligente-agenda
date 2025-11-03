"""
Content Safety & Moderation Utils
Protegge community da contenuto dannoso
"""
import re
from typing import Tuple, Dict, List


# ========================================
# CRISIS KEYWORDS (Suicidal ideation)
# ========================================

CRISIS_KEYWORDS_IT = [
    'suicidio', 'suicidarmi', 'uccidermi', 'ammazzarmi',
    'farla finita', 'togliermi la vita', 'non voglio vivere',
    'voglio morire', 'meglio morto', 'finirla qui',
    'non ce la faccio più', 'voglio sparire', 'voglio morire'
]

CRISIS_KEYWORDS_EN = [
    'suicide', 'kill myself', 'end my life', 'want to die',
    'better off dead', 'can\'t go on', 'end it all',
    'want to disappear', 'don\'t want to live'
]

CRISIS_KEYWORDS_ES = [
    'suicidio', 'matarme', 'quiero morir', 'mejor muerto',
    'terminar con mi vida', 'no puedo más'
]

CRISIS_KEYWORDS = CRISIS_KEYWORDS_IT + CRISIS_KEYWORDS_EN + CRISIS_KEYWORDS_ES


# ========================================
# BANNED KEYWORDS (Violence, Hate, etc)
# ========================================

VIOLENCE_KEYWORDS = [
    'uccidere', 'ammazzare', 'kill', 'murder', 'bomb', 'bomba',
    'terrorismo', 'terrorist', 'attentato', 'strage', 'massacre',
    'arma', 'weapon', 'pistola', 'gun', 'knife', 'coltello'
]

# Hate speech - aggiungi cautamente
HATE_KEYWORDS = [
    'frocio', 'negro', 'terrone',  # IT slurs
    # EN/ES slurs omessi per rispetto, ma vanno aggiunti
]

SPAM_KEYWORDS = [
    'clicca qui', 'click here', 'guadagna €', 'earn money', 'make money',
    'buy now', 'compra ora', 'sconto 50%', '50% off', 'limited offer',
    'DM me', 'contact me for', 'whatsapp', 'telegram @',
    'bitcoin', 'crypto investment', 'NFT', 'trading signals',
    'forex', 'get rich', 'guaranteed profit'
]

MEDICAL_MISINFO = [
    'cura cancro', 'cure cancer', 'big pharma lie',
    'vaccines cause', 'vaccini causano', 'non vaccinarti',
    'smetti farmaci', 'stop medication', 'psicofarmaci fanno male'
]

BANNED_KEYWORDS = VIOLENCE_KEYWORDS + HATE_KEYWORDS + SPAM_KEYWORDS + MEDICAL_MISINFO


# ========================================
# AGE KEYWORDS (Minors detection)
# ========================================

MINOR_INDICATORS = [
    'ho 15 anni', 'ho 16 anni', 'ho 17 anni',
    'sono minorenne', 'vado a scuola', 'liceo',
    'miei genitori', 'i miei prof',
    'i am 15', 'i am 16', 'i am 17',
    'tengo 15 años', 'tengo 16', 'tengo 17'
]


# ========================================
# DETECTION FUNCTIONS
# ========================================

def detect_crisis(text: str) -> Tuple[bool, Dict]:
    """
    Rileva se il testo contiene segnali di crisi/suicidio
    
    Returns:
        (crisis_detected, crisis_info)
    """
    text_lower = text.lower()
    
    for keyword in CRISIS_KEYWORDS:
        if keyword in text_lower:
            return True, {
                'severity': 'high',
                'keyword_found': keyword,
                'help_resources': get_crisis_resources()
            }
    
    return False, {}


def check_banned_keywords(text: str) -> Tuple[bool, str]:
    """
    Verifica se contiene parole bannate
    
    Returns:
        (is_ok, error_message)
    """
    text_lower = text.lower()
    
    for keyword in BANNED_KEYWORDS:
        if keyword in text_lower:
            return False, "Contenuto non permesso (viola regole community)"
    
    return True, None


def detect_minor(text: str) -> bool:
    """
    Rileva se user potrebbe essere minorenne
    """
    text_lower = text.lower()
    
    for indicator in MINOR_INDICATORS:
        if indicator in text_lower:
            return True
    
    # Check età esplicita (pattern: "ho X anni" dove X < 18)
    age_pattern = r'ho (\d+) ann[io]|i am (\d+)|tengo (\d+) año'
    matches = re.findall(age_pattern, text_lower)
    
    for match in matches:
        age = int([m for m in match if m][0])
        if age < 18:
            return True
    
    return False


def is_likely_spam(text: str) -> bool:
    """
    Rileva probabilità che sia spam
    """
    spam_score = 0
    
    # Troppi link
    links = len(re.findall(r'http[s]?://', text))
    if links > 2:
        spam_score += 3
    elif links > 0:
        spam_score += 1
    
    # All caps (>50% caratteri)
    uppercase_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    if uppercase_ratio > 0.5 and len(text) > 20:
        spam_score += 2
    
    # Troppi emoji
    emoji_count = len([c for c in text if ord(c) > 127000])
    if emoji_count > 15:
        spam_score += 1
    
    # Parole spam
    for keyword in SPAM_KEYWORDS:
        if keyword in text.lower():
            spam_score += 3
            break
    
    # Ripetizioni eccessive
    words = text.split()
    if len(words) > 5:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.3:  # <30% parole uniche
            spam_score += 2
    
    # Troppi numeri (es. "guadagna 5000 euro in 30 giorni")
    numbers = re.findall(r'\d+', text)
    if len(numbers) > 5:
        spam_score += 1
    
    return spam_score >= 4


def get_crisis_resources() -> List[Dict]:
    """Restituisce lista di risorse per crisi"""
    return [
        {
            'country': 'IT',
            'name': 'Telefono Amico',
            'phone': '02.2327.2327',
            'hours': '24/7',
            'language': 'Italiano',
            'free': True
        },
        {
            'country': 'IT',
            'name': 'Emergenza',
            'phone': '112',
            'hours': '24/7',
            'language': 'Italiano',
            'free': True
        },
        {
            'country': 'IT',
            'name': 'Samaritans Italia',
            'phone': '06.77208977',
            'hours': '13:00-22:00',
            'language': 'Italiano',
            'free': True
        },
        {
            'country': 'IT',
            'name': 'Numero Verde Salute Mentale',
            'phone': '800.274.274',
            'hours': 'Varia per regione',
            'language': 'Italiano',
            'free': True
        },
        {
            'country': 'GB',
            'name': 'Samaritans UK',
            'phone': '116 123',
            'hours': '24/7',
            'language': 'English',
            'free': True
        },
        {
            'country': 'US',
            'name': '988 Suicide & Crisis Lifeline',
            'phone': '988',
            'hours': '24/7',
            'language': 'English',
            'free': True
        },
        {
            'country': 'ES',
            'name': 'Teléfono de la Esperanza',
            'phone': '717 003 717',
            'hours': '24/7',
            'language': 'Español',
            'free': True
        }
    ]


def is_safe_content(text: str) -> Tuple[bool, str, Dict]:
    """
    Verifica completa sicurezza contenuto
    
    Returns:
        (is_safe, error_message, extra_info)
    """
    # 1. Check crisis
    is_crisis, crisis_info = detect_crisis(text)
    if is_crisis:
        return False, 'crisis_detected', crisis_info
    
    # 2. Check banned keywords
    is_ok, error = check_banned_keywords(text)
    if not is_ok:
        return False, 'banned_content', {'type': 'hate_violence_illegal'}
    
    # 3. Check spam
    if is_likely_spam(text):
        return False, 'spam_detected', {'type': 'spam'}
    
    # 4. Check minor indicators
    if detect_minor(text):
        return False, 'minor_detected', {
            'message': 'La community è riservata a maggiorenni (18+)'
        }
    
    return True, None, {}

