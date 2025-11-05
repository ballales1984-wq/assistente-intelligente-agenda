"""Script per pulire dati duplicati/test nel database produzione"""

import os
import sys
from datetime import datetime

# Aggiungi la directory corrente al path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models import Obiettivo, Impegno, Spesa, DiarioGiornaliero


def cleanup_duplicates():
    """Rimuove obiettivi duplicati e dati di test"""
    
    print("=" * 60)
    print("🧹 PULIZIA DATABASE PRODUZIONE")
    print("=" * 60)
    print()
    
    app = create_app()
    
    with app.app_context():
        # 1. Trova obiettivi duplicati (stesso nome)
        print("📊 Analisi obiettivi...")
        obiettivi = Obiettivo.query.all()
        print(f"   Totale obiettivi: {len(obiettivi)}")
        
        # Raggruppa per nome
        obiettivi_per_nome = {}
        for obj in obiettivi:
            nome_lower = obj.nome.lower()
            if nome_lower not in obiettivi_per_nome:
                obiettivi_per_nome[nome_lower] = []
            obiettivi_per_nome[nome_lower].append(obj)
        
        # Trova duplicati
        duplicati = {nome: objs for nome, objs in obiettivi_per_nome.items() if len(objs) > 1}
        
        if duplicati:
            print(f"\n⚠️  Trovati {len(duplicati)} obiettivi duplicati:")
            for nome, objs in duplicati.items():
                print(f"\n   '{nome}' ({len(objs)} copie):")
                for i, obj in enumerate(objs):
                    print(f"      {i+1}. ID {obj.id}: {obj.durata_settimanale}h/settimana - ore completate: {obj.ore_completate}")
            
            print("\n🤔 Cosa vuoi fare?")
            print("   1. Mantieni solo il primo di ogni duplicato")
            print("   2. Mantieni quello con più ore completate")
            print("   3. Scegli manualmente per ogni duplicato")
            print("   4. Non fare nulla (esci)")
            
            scelta = input("\nScelta (1-4): ").strip()
            
            if scelta == "1":
                # Mantieni il primo, elimina gli altri
                print("\n🗑️  Eliminazione duplicati (mantieni primo)...")
                eliminati = 0
                for nome, objs in duplicati.items():
                    for obj in objs[1:]:  # Salta il primo
                        print(f"   ❌ Elimino: {obj.nome} (ID {obj.id})")
                        db.session.delete(obj)
                        eliminati += 1
                
                db.session.commit()
                print(f"\n✅ Eliminati {eliminati} obiettivi duplicati!")
            
            elif scelta == "2":
                # Mantieni quello con più ore completate
                print("\n🗑️  Eliminazione duplicati (mantieni più completato)...")
                eliminati = 0
                for nome, objs in duplicati.items():
                    # Ordina per ore_completate (decrescente)
                    objs_sorted = sorted(objs, key=lambda x: x.ore_completate or 0, reverse=True)
                    mantieni = objs_sorted[0]
                    
                    for obj in objs_sorted[1:]:  # Elimina gli altri
                        print(f"   ❌ Elimino: {obj.nome} (ID {obj.id}, {obj.ore_completate}h)")
                        db.session.delete(obj)
                        eliminati += 1
                    
                    print(f"   ✅ Mantengo: {mantieni.nome} (ID {mantieni.id}, {mantieni.ore_completate}h)")
                
                db.session.commit()
                print(f"\n✅ Eliminati {eliminati} obiettivi duplicati!")
            
            elif scelta == "3":
                # Scelta manuale
                print("\n🗑️  Scelta manuale...")
                eliminati = 0
                for nome, objs in duplicati.items():
                    print(f"\n'{nome}' - quale vuoi MANTENERE?")
                    for i, obj in enumerate(objs):
                        print(f"   {i+1}. ID {obj.id}: {obj.durata_settimanale}h/settimana - completate: {obj.ore_completate}h")
                    
                    while True:
                        mantieni_idx = input(f"Mantieni (1-{len(objs)}): ").strip()
                        try:
                            mantieni_idx = int(mantieni_idx) - 1
                            if 0 <= mantieni_idx < len(objs):
                                break
                        except ValueError:
                            pass
                        print("❌ Scelta non valida!")
                    
                    # Elimina gli altri
                    for i, obj in enumerate(objs):
                        if i != mantieni_idx:
                            print(f"   ❌ Elimino: {obj.nome} (ID {obj.id})")
                            db.session.delete(obj)
                            eliminati += 1
                
                db.session.commit()
                print(f"\n✅ Eliminati {eliminati} obiettivi duplicati!")
            
            else:
                print("\n🚫 Operazione annullata.")
        else:
            print("   ✅ Nessun duplicato trovato!")
        
        # 2. Mostra statistiche finali
        print("\n" + "=" * 60)
        print("📊 STATISTICHE FINALI")
        print("=" * 60)
        
        obiettivi_finali = Obiettivo.query.all()
        impegni_finali = Impegno.query.all()
        spese_finali = Spesa.query.all()
        diari_finali = DiarioGiornaliero.query.all()
        
        print(f"\n✅ Obiettivi: {len(obiettivi_finali)}")
        for obj in obiettivi_finali:
            print(f"   - {obj.nome}: {obj.durata_settimanale}h/settimana ({obj.ore_completate}h completate)")
        
        print(f"\n📅 Impegni: {len(impegni_finali)}")
        print(f"💰 Spese: {len(spese_finali)}")
        print(f"📔 Diari: {len(diari_finali)}")
        
        print("\n✨ Pulizia completata!")


if __name__ == "__main__":
    cleanup_duplicates()

