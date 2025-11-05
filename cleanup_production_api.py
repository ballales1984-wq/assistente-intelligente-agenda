"""Script per pulire duplicati in produzione tramite API REST"""

import requests
from collections import Counter
import sys

# URL produzione
PROD_URL = "https://assistente-intelligente-agenda.onrender.com"

# Colori
class C:
    G = '\033[92m'  # Green
    Y = '\033[93m'  # Yellow
    R = '\033[91m'  # Red
    C = '\033[96m'  # Cyan
    E = '\033[0m'   # End


def print_header(text):
    print(f"\n{C.C}{'=' * 70}{C.E}")
    print(f"{C.C}{text}{C.E}")
    print(f"{C.C}{'=' * 70}{C.E}\n")


def get_obiettivi():
    """Recupera obiettivi da produzione"""
    try:
        response = requests.get(f"{PROD_URL}/api/obiettivi", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"{C.R}❌ Errore recupero obiettivi: {e}{C.E}")
        return None


def delete_obiettivo(obiettivo_id):
    """Elimina un obiettivo tramite API"""
    try:
        response = requests.delete(f"{PROD_URL}/api/obiettivi/{obiettivo_id}", timeout=10)
        return response.status_code in [200, 204]
    except Exception as e:
        print(f"{C.R}❌ Errore eliminazione: {e}{C.E}")
        return False


def main():
    print_header("🧹 PULIZIA DUPLICATI PRODUZIONE (via API)")
    
    # 1. Recupera obiettivi
    print(f"{C.C}📊 Recupero obiettivi da produzione...{C.E}")
    obiettivi = get_obiettivi()
    
    if not obiettivi:
        print(f"{C.R}❌ Impossibile recuperare obiettivi{C.E}")
        return
    
    print(f"{C.G}✅ Trovati {len(obiettivi)} obiettivi{C.E}\n")
    
    # 2. Trova duplicati
    nomi_lower = [obj['nome'].lower() for obj in obiettivi]
    counter = Counter(nomi_lower)
    duplicati = {nome: count for nome, count in counter.items() if count > 1}
    
    if not duplicati:
        print(f"{C.G}✅ Nessun duplicato trovato!{C.E}")
        return
    
    print(f"{C.Y}⚠️  Trovati duplicati:{C.E}\n")
    for nome, count in duplicati.items():
        print(f"   • '{nome}': {count} copie")
    
    # 3. Mostra dettagli duplicati
    print(f"\n{C.C}📋 DETTAGLI DUPLICATI:{C.E}\n")
    
    duplicati_dettagli = {}
    for nome in duplicati.keys():
        objs = [obj for obj in obiettivi if obj['nome'].lower() == nome]
        duplicati_dettagli[nome] = objs
        
        print(f"  '{nome.upper()}':")
        for i, obj in enumerate(objs, 1):
            print(f"    {i}. ID {obj['id']}: "
                  f"{obj['durata_settimanale']}h/sett - "
                  f"{obj.get('ore_completate', 0)}h completate")
        print()
    
    # 4. Chiedi conferma
    print(f"{C.Y}🤔 Cosa vuoi fare?{C.E}")
    print("   1. Mantieni il PRIMO di ogni duplicato (elimina gli altri)")
    print("   2. Mantieni quello con PIÙ ore completate")
    print("   3. Scegli MANUALMENTE per ogni duplicato")
    print("   4. NON fare nulla (esci)")
    
    scelta = input(f"\n{C.C}Scelta (1-4): {C.E}").strip()
    
    if scelta == "1":
        # Mantieni primo
        print(f"\n{C.Y}🗑️  Eliminazione duplicati (mantieni primo)...{C.E}\n")
        eliminati = 0
        
        for nome, objs in duplicati_dettagli.items():
            mantieni = objs[0]
            print(f"  '{nome}': mantengo ID {mantieni['id']}")
            
            for obj in objs[1:]:
                print(f"    ❌ Elimino ID {obj['id']}...", end=" ")
                if delete_obiettivo(obj['id']):
                    print(f"{C.G}OK{C.E}")
                    eliminati += 1
                else:
                    print(f"{C.R}ERRORE{C.E}")
        
        print(f"\n{C.G}✅ Eliminati {eliminati} obiettivi duplicati!{C.E}")
    
    elif scelta == "2":
        # Mantieni quello con più ore
        print(f"\n{C.Y}🗑️  Eliminazione duplicati (mantieni più completato)...{C.E}\n")
        eliminati = 0
        
        for nome, objs in duplicati_dettagli.items():
            objs_sorted = sorted(objs, key=lambda x: x.get('ore_completate', 0), reverse=True)
            mantieni = objs_sorted[0]
            print(f"  '{nome}': mantengo ID {mantieni['id']} ({mantieni.get('ore_completate', 0)}h)")
            
            for obj in objs_sorted[1:]:
                print(f"    ❌ Elimino ID {obj['id']}...", end=" ")
                if delete_obiettivo(obj['id']):
                    print(f"{C.G}OK{C.E}")
                    eliminati += 1
                else:
                    print(f"{C.R}ERRORE{C.E}")
        
        print(f"\n{C.G}✅ Eliminati {eliminati} obiettivi duplicati!{C.E}")
    
    elif scelta == "3":
        # Scelta manuale
        print(f"\n{C.Y}🗑️  Scelta manuale...{C.E}\n")
        eliminati = 0
        
        for nome, objs in duplicati_dettagli.items():
            print(f"\n'{nome.upper()}' - quale vuoi MANTENERE?")
            for i, obj in enumerate(objs, 1):
                print(f"   {i}. ID {obj['id']}: "
                      f"{obj['durata_settimanale']}h/sett - "
                      f"{obj.get('ore_completate', 0)}h completate")
            
            while True:
                try:
                    mantieni_idx = int(input(f"Mantieni (1-{len(objs)}): ")) - 1
                    if 0 <= mantieni_idx < len(objs):
                        break
                except ValueError:
                    pass
                print(f"{C.R}❌ Scelta non valida!{C.E}")
            
            # Elimina gli altri
            for i, obj in enumerate(objs):
                if i != mantieni_idx:
                    print(f"  ❌ Elimino ID {obj['id']}...", end=" ")
                    if delete_obiettivo(obj['id']):
                        print(f"{C.G}OK{C.E}")
                        eliminati += 1
                    else:
                        print(f"{C.R}ERRORE{C.E}")
        
        print(f"\n{C.G}✅ Eliminati {eliminati} obiettivi duplicati!{C.E}")
    
    else:
        print(f"\n{C.Y}🚫 Operazione annullata{C.E}")
        return
    
    # 5. Verifica finale
    print(f"\n{C.C}📊 VERIFICA FINALE:{C.E}\n")
    obiettivi_finali = get_obiettivi()
    
    if obiettivi_finali:
        print(f"{C.G}✅ Obiettivi rimanenti: {len(obiettivi_finali)}{C.E}\n")
        for obj in obiettivi_finali:
            print(f"   • {obj['nome']}: {obj['durata_settimanale']}h/sett")
        
        # Controlla se ci sono ancora duplicati
        nomi_finali = [obj['nome'].lower() for obj in obiettivi_finali]
        counter_finali = Counter(nomi_finali)
        duplicati_finali = {n: c for n, c in counter_finali.items() if c > 1}
        
        if duplicati_finali:
            print(f"\n{C.Y}⚠️  Attenzione: Ci sono ancora duplicati:{C.E}")
            for nome, count in duplicati_finali.items():
                print(f"   • '{nome}': {count} copie")
        else:
            print(f"\n{C.G}✅ Nessun duplicato rimanente! Database pulito!{C.E}")
    
    print(f"\n{C.C}✨ PULIZIA COMPLETATA{C.E}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.Y}⚠️  Operazione interrotta{C.E}")
        sys.exit(0)

