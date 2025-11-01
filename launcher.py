"""Launcher per l'applicazione - Apre automaticamente il browser"""
import os
import sys
import webbrowser
import time
from threading import Timer

# Aggiungi il percorso dell'app al PYTHONPATH
if getattr(sys, 'frozen', False):
    # Se è un exe compilato
    base_path = sys._MEIPASS
else:
    # Se è script Python normale
    base_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, base_path)

def apri_browser():
    """Apre il browser dopo 2 secondi"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')
    print("\n✅ Browser aperto!")
    print("🌐 URL: http://localhost:5000")
    print("\n💡 Per chiudere l'applicazione, chiudi questa finestra\n")

if __name__ == '__main__':
    print("╔═══════════════════════════════════════════════════╗")
    print("║                                                   ║")
    print("║       🧠 ASSISTENTE INTELLIGENTE v1.2.0          ║")
    print("║                                                   ║")
    print("╚═══════════════════════════════════════════════════╝")
    print()
    print("🚀 Avvio applicazione...")
    print("⏳ Attendere pochi secondi...")
    print()
    
    # Apri browser in un thread separato
    Timer(2.0, apri_browser).start()
    
    # Importa e avvia l'app
    try:
        from app import create_app
        app = create_app()
        
        print("✅ Server avviato con successo!")
        print("🌐 Indirizzo: http://localhost:5000")
        print()
        
        # Avvia Flask
        app.run(host='127.0.0.1', port=5000, debug=False)
        
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        print("\n⚠️  Premi INVIO per chiudere...")
        input()
        sys.exit(1)

