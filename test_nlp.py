"""Test NLP pattern matching"""
from app.core.input_manager import InputManager

# Test vari input
test_inputs = [
    # OBIETTIVI
    "Voglio studiare Python 3 ore a settimana",
    "Imparare inglese 2h settimana",
    "Fare sport 5 ore ogni settimana",
    "Leggere libri",  # Senza ore - difficile
    
    # IMPEGNI
    "Lunedì meeting dalle 10 alle 12",
    "Domani palestra 18-19",
    "Mercoledì corso dalle 19 alle 21",
    "Riunione importante domani mattina",  # Senza orario - difficile
    
    # SPESE
    "Speso 12 euro pranzo",
    "50 euro benzina",
    "Pagato 100 euro abbonamento",
    "Comprato scarpe",  # Senza importo - difficile
    
    # DIARIO
    "Oggi ho parlato con Sara",
    "Mi sento stanco",
    "Ho capito i cicli for",
    
    # DOMANDE
    "Cosa devo fare oggi?",
    "Quanto ho speso?",
    "Mostrami obiettivi",
    
    # DIFFICILI (edge cases)
    "Vado in palestra",  # Troppo vago
    "Ho speso soldi",  # Troppo generico
    "Domani",  # Solo parola
]

print("\n" + "="*80)
print("🧪 TEST NLP PATTERN MATCHING")
print("="*80)

for idx, testo in enumerate(test_inputs, 1):
    print(f"\n{idx}. Input: '{testo}'")
    
    risultato = InputManager.analizza_input(testo)
    
    tipo = risultato['tipo']
    emoji = {
        'obiettivo': '🎯',
        'impegno': '📅', 
        'spesa': '💰',
        'diario': '📝',
        'stato': '😊',
        'domanda': '❓',
        'completamento': '✅',
        'unknown': '❌'
    }.get(tipo, '❔')
    
    print(f"   {emoji} Riconosciuto come: {tipo}")
    
    if risultato['dati']:
        for key, value in risultato['dati'].items():
            print(f"      - {key}: {value}")
    
    if tipo == 'unknown':
        print(f"      ⚠️ NON RICONOSCIUTO - Verrà salvato come diario")

print("\n" + "="*80)
print("✅ Test completato!")
print("="*80 + "\n")

