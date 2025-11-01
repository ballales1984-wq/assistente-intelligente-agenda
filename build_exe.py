"""Script per creare l'eseguibile standalone dell'applicazione"""
import os
import sys

def build_exe():
    """
    Crea l'eseguibile usando PyInstaller
    """
    print("🔨 Creazione eseguibile in corso...")
    print("📦 Questo potrebbe richiedere qualche minuto...\n")
    
    # Comando PyInstaller
    comando = [
        'pyinstaller',
        '--name=AssistenteIntelligente',
        '--onefile',
        '--windowed',  # Nessuna console su Windows
        '--icon=static/icon.ico' if os.path.exists('static/icon.ico') else '',
        '--add-data=templates;templates',
        '--add-data=static;static',
        '--hidden-import=flask',
        '--hidden-import=flask_sqlalchemy',
        '--hidden-import=sqlalchemy',
        '--hidden-import=app',
        '--hidden-import=app.core',
        '--hidden-import=app.models',
        '--hidden-import=app.managers',
        '--hidden-import=app.routes',
        'run.py'
    ]
    
    # Rimuovi elementi vuoti
    comando = [c for c in comando if c]
    
    print("🔧 Comando:", ' '.join(comando))
    print()
    
    os.system(' '.join(comando))
    
    print("\n✅ Build completato!")
    print("\n📁 L'eseguibile si trova in: dist/AssistenteIntelligente.exe")
    print("📦 Dimensione approssimativa: ~30-50 MB")
    print("\n💡 Per distribuire:")
    print("   1. Copia dist/AssistenteIntelligente.exe dove vuoi")
    print("   2. Doppio click per avviare!")
    print("   3. Si aprirà automaticamente nel browser\n")


if __name__ == '__main__':
    build_exe()

