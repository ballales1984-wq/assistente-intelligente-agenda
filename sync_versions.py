"""Script per verificare l'allineamento delle versioni locale/produzione"""

import os
import sys
import requests
from datetime import datetime

# Colori per output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Stampa header colorato"""
    print(f"\n{Colors.CYAN}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.CYAN}{'=' * 70}{Colors.END}\n")


def print_success(text):
    """Stampa messaggio di successo"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text):
    """Stampa messaggio di errore"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_warning(text):
    """Stampa messaggio di warning"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def print_info(text):
    """Stampa informazione"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def check_local_version():
    """Verifica versione locale"""
    print_header("🖥️  VERSIONE LOCALE")
    
    try:
        # Leggi README per versione
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
            import re
            match = re.search(r'version-(\d+\.\d+\.\d+)-blue', content)
            if match:
                version = match.group(1)
                print_success(f"Versione trovata: {version}")
                
                # Verifica server locale
                try:
                    response = requests.get('http://localhost:5000/api/profilo', timeout=3)
                    if response.status_code == 200:
                        print_success("Server locale: ONLINE")
                    else:
                        print_warning("Server locale: risponde ma con errori")
                except requests.exceptions.RequestException:
                    print_warning("Server locale: OFFLINE (avvia con 'python run.py')")
                
                return version
            else:
                print_error("Versione non trovata nel README")
                return None
    except Exception as e:
        print_error(f"Errore lettura versione locale: {e}")
        return None


def check_production_version():
    """Verifica versione produzione"""
    print_header("🌍 VERSIONE PRODUZIONE")
    
    prod_url = "https://assistente-intelligente-agenda.onrender.com"
    
    try:
        # Test homepage
        print_info("Connessione a Render...")
        response = requests.get(prod_url, timeout=10)
        
        if response.status_code == 200:
            print_success("Server produzione: ONLINE")
            
            # Test API
            api_response = requests.get(f"{prod_url}/api/profilo", timeout=10)
            if api_response.status_code == 200:
                print_success("API produzione: FUNZIONANTE")
            else:
                print_warning("API produzione: risponde ma con errori")
            
            # Verifica versione nel HTML
            import re
            match = re.search(r'version-(\d+\.\d+\.\d+)-blue', response.text)
            if match:
                version = match.group(1)
                print_success(f"Versione produzione: {version}")
                return version
            else:
                print_warning("Versione non trovata nella homepage")
                return "unknown"
        else:
            print_error(f"Server produzione: HTTP {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print_error(f"Errore connessione produzione: {e}")
        return None


def check_database_stats(environment="local"):
    """Mostra statistiche database"""
    url_base = "http://localhost:5000" if environment == "local" else "https://assistente-intelligente-agenda.onrender.com"
    
    print_header(f"📊 STATISTICHE DATABASE ({environment.upper()})")
    
    try:
        # Obiettivi
        obiettivi = requests.get(f"{url_base}/api/obiettivi", timeout=10).json()
        print(f"🎯 Obiettivi: {len(obiettivi)}")
        
        # Conta duplicati
        nomi = [obj['nome'].lower() for obj in obiettivi]
        duplicati = len(nomi) - len(set(nomi))
        if duplicati > 0:
            print_warning(f"   {duplicati} obiettivi duplicati rilevati!")
            
            # Mostra duplicati
            from collections import Counter
            counter = Counter(nomi)
            for nome, count in counter.items():
                if count > 1:
                    print(f"      - '{nome}': {count} copie")
        else:
            print_success("   Nessun duplicato")
        
        # Impegni
        impegni = requests.get(f"{url_base}/api/impegni", timeout=10).json()
        print(f"📅 Impegni: {len(impegni)}")
        
        # Spese
        spese = requests.get(f"{url_base}/api/spese", timeout=10).json()
        print(f"💰 Spese: {len(spese)}")
        if spese:
            totale = sum(s['importo'] for s in spese)
            print(f"   Totale: €{totale:.2f}")
        
        return True
    except Exception as e:
        print_error(f"Errore recupero statistiche: {e}")
        return False


def main():
    """Main function"""
    print_header("🔄 VERIFICA ALLINEAMENTO VERSIONI")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    # Check versioni
    local_version = check_local_version()
    prod_version = check_production_version()
    
    # Confronta
    if local_version and prod_version:
        print_header("🔍 CONFRONTO VERSIONI")
        if local_version == prod_version:
            print_success(f"Versioni allineate: {local_version}")
        else:
            print_warning(f"Versioni NON allineate!")
            print(f"   Locale:     {local_version}")
            print(f"   Produzione: {prod_version}")
            print_info("Potrebbe essere necessario aspettare il deploy su Render (2-5 minuti)")
    
    # Statistiche database
    if local_version:
        check_database_stats("local")
    
    if prod_version:
        check_database_stats("production")
    
    # Raccomandazioni
    print_header("💡 RACCOMANDAZIONI")
    
    if local_version and prod_version and local_version != prod_version:
        print_warning("Le versioni non sono allineate:")
        print("   1. Aspetta 2-5 minuti che Render completi il deploy")
        print("   2. Ricontrolla con: python sync_versions.py")
        print("   3. Se persiste, verifica i logs su Render.com")
    else:
        print_success("Tutto OK! Le versioni sono allineate.")
    
    # Script cleanup
    print("\n" + Colors.CYAN + "🧹 Per pulire i duplicati nel database produzione:" + Colors.END)
    print("   Opzione 1: Usa Render Shell (consigliato)")
    print("      - Vai su render.com → tuo servizio → Shell")
    print("      - Esegui: python cleanup_production_db.py")
    print()
    print("   Opzione 2: Connessione remota DATABASE_URL")
    print("      - Imposta: export DATABASE_URL='postgresql://...'")
    print("      - Esegui: python cleanup_production_db.py")
    
    print_header("✨ VERIFICA COMPLETATA")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Operazione interrotta dall'utente{Colors.END}")
        sys.exit(0)

