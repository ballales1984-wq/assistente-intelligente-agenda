"""Test rapido database"""
from app import create_app, db
from app.models import Impegno, Spesa, Obiettivo, UserProfile
from datetime import datetime, date

app = create_app()

with app.app_context():
    print("\n" + "="*60)
    print("🔍 VERIFICA DATABASE")
    print("="*60)
    
    # Conta records
    print(f"\n📊 Records nel database:")
    print(f"   UserProfile: {UserProfile.query.count()}")
    print(f"   Obiettivi:   {Obiettivo.query.count()}")
    print(f"   Impegni:     {Impegno.query.count()}")
    print(f"   Spese:       {Spesa.query.count()}")
    
    # Mostra ultimi impegni
    print(f"\n📅 Ultimi 5 impegni:")
    impegni = Impegno.query.order_by(Impegno.created_at.desc()).limit(5).all()
    if impegni:
        for imp in impegni:
            print(f"   - {imp.nome} | {imp.data_inizio.strftime('%d/%m %H:%M')}")
    else:
        print("   ⚠️  Nessun impegno trovato!")
    
    # Mostra ultime spese
    print(f"\n💰 Ultime 5 spese:")
    spese = Spesa.query.order_by(Spesa.created_at.desc()).limit(5).all()
    if spese:
        for s in spese:
            print(f"   - €{s.importo:.2f} | {s.descrizione} | {s.categoria}")
    else:
        print("   ⚠️  Nessuna spesa trovata!")
    
    # Mostra obiettivi
    print(f"\n🎯 Obiettivi attivi:")
    obiettivi = Obiettivo.query.filter_by(attivo=True).all()
    if obiettivi:
        for obj in obiettivi:
            print(f"   - {obj.nome} | {obj.durata_settimanale}h/settimana")
    else:
        print("   ⚠️  Nessun obiettivo trovato!")
    
    print("\n" + "="*60)
    print("✅ Verifica completata!")
    print("="*60 + "\n")

