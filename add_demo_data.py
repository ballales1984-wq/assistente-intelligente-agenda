"""Aggiungi dati demo per testare l'app"""
from app import create_app, db
from app.models import UserProfile, Obiettivo, Impegno, Spesa, DiarioGiornaliero
from datetime import datetime, timedelta, date, time

app = create_app()

with app.app_context():
    print("\n🎯 Aggiunta dati demo...")
    
    # Get user
    profilo = UserProfile.query.first()
    if not profilo:
        profilo = UserProfile(nome='Demo User')
        db.session.add(profilo)
        db.session.commit()
    
    # ==========================================
    # OBIETTIVI
    # ==========================================
    print("\n📚 Creazione obiettivi...")
    obiettivi_demo = [
        {'nome': 'Studiare Python', 'tipo': 'studio', 'durata_settimanale': 5},
        {'nome': 'Palestra', 'tipo': 'sport', 'durata_settimanale': 3},
        {'nome': 'Leggere libri', 'tipo': 'personale', 'durata_settimanale': 2}
    ]
    
    for obj_data in obiettivi_demo:
        exists = Obiettivo.query.filter_by(
            user_id=profilo.id,
            nome=obj_data['nome']
        ).first()
        
        if not exists:
            obj = Obiettivo(
                user_id=profilo.id,
                nome=obj_data['nome'],
                tipo=obj_data['tipo'],
                durata_settimanale=obj_data['durata_settimanale'],
                intensita='media',
                attivo=True
            )
            db.session.add(obj)
            print(f"   ✅ {obj_data['nome']}")
    
    db.session.commit()
    
    # ==========================================
    # IMPEGNI (questa settimana)
    # ==========================================
    print("\n📅 Creazione impegni...")
    oggi = datetime.now()
    lunedi = oggi - timedelta(days=oggi.weekday())
    
    impegni_demo = [
        {'nome': 'Meeting Team', 'giorno': 0, 'ora_inizio': '10:00', 'ora_fine': '11:30', 'tipo': 'lavoro'},
        {'nome': 'Studio Python', 'giorno': 0, 'ora_inizio': '14:00', 'ora_fine': '17:00', 'tipo': 'studio'},
        {'nome': 'Palestra', 'giorno': 1, 'ora_inizio': '18:00', 'ora_fine': '19:30', 'tipo': 'sport'},
        {'nome': 'Corso React', 'giorno': 2, 'ora_inizio': '19:00', 'ora_fine': '21:00', 'tipo': 'studio'},
        {'nome': 'Pranzo con amici', 'giorno': 3, 'ora_inizio': '13:00', 'ora_fine': '15:00', 'tipo': 'svago'},
        {'nome': 'Call importante', 'giorno': 4, 'ora_inizio': '11:00', 'ora_fine': '12:00', 'tipo': 'lavoro'},
        {'nome': 'Weekend al mare', 'giorno': 5, 'ora_inizio': '10:00', 'ora_fine': '18:00', 'tipo': 'svago'}
    ]
    
    for imp_data in impegni_demo:
        data_impegno = lunedi + timedelta(days=imp_data['giorno'])
        ora_inizio = datetime.strptime(imp_data['ora_inizio'], '%H:%M').time()
        ora_fine = datetime.strptime(imp_data['ora_fine'], '%H:%M').time()
        
        data_inizio = datetime.combine(data_impegno.date(), ora_inizio)
        data_fine = datetime.combine(data_impegno.date(), ora_fine)
        
        imp = Impegno(
            user_id=profilo.id,
            nome=imp_data['nome'],
            data_inizio=data_inizio,
            data_fine=data_fine,
            tipo=imp_data['tipo']
        )
        db.session.add(imp)
        print(f"   ✅ {imp_data['nome']} - {data_inizio.strftime('%a %d/%m %H:%M')}")
    
    db.session.commit()
    
    # ==========================================
    # SPESE (ultimi giorni)
    # ==========================================
    print("\n💰 Creazione spese...")
    spese_demo = [
        {'importo': 12.50, 'descrizione': 'Pranzo ristorante', 'categoria': 'Cibo', 'giorni_fa': 0},
        {'importo': 3.50, 'descrizione': 'Caffè bar', 'categoria': 'Cibo', 'giorni_fa': 0},
        {'importo': 50.00, 'descrizione': 'Benzina', 'categoria': 'Trasporti', 'giorni_fa': 1},
        {'importo': 25.00, 'descrizione': 'Cinema con amici', 'categoria': 'Svago', 'giorni_fa': 1},
        {'importo': 89.99, 'descrizione': 'Abbonamento palestra', 'categoria': 'Sport', 'giorni_fa': 2},
        {'importo': 15.00, 'descrizione': 'Farmacia', 'categoria': 'Salute', 'giorni_fa': 3},
        {'importo': 120.00, 'descrizione': 'Spesa supermercato', 'categoria': 'Cibo', 'giorni_fa': 4}
    ]
    
    for spesa_data in spese_demo:
        data_spesa = date.today() - timedelta(days=spesa_data['giorni_fa'])
        
        spesa = Spesa(
            user_id=profilo.id,
            importo=spesa_data['importo'],
            descrizione=spesa_data['descrizione'],
            categoria=spesa_data['categoria'],
            data=data_spesa,
            ora=datetime.now().time()
        )
        db.session.add(spesa)
        print(f"   ✅ €{spesa_data['importo']:.2f} - {spesa_data['descrizione']}")
    
    db.session.commit()
    
    # ==========================================
    # DIARIO (ultimi giorni)
    # ==========================================
    print("\n📝 Creazione diary entries...")
    diario_demo = [
        {'testo': 'Oggi ho fatto progressi con Python! Capiti i decorators.', 'sentiment': 'positivo', 'giorni_fa': 0},
        {'testo': 'Meeting produttivo. Team motivato per nuovo progetto.', 'sentiment': 'positivo', 'giorni_fa': 1},
        {'testo': 'Giornata un po\' stancante. Troppi impegni.', 'sentiment': 'negativo', 'giorni_fa': 2}
    ]
    
    for diario_data in diario_demo:
        data_diario = date.today() - timedelta(days=diario_data['giorni_fa'])
        
        diario = DiarioGiornaliero(
            user_id=profilo.id,
            data=data_diario,
            testo=diario_data['testo'],
            sentiment=diario_data['sentiment'],
            parole_chiave='python,team,progetto'
        )
        db.session.add(diario)
        print(f"   ✅ {diario_data['testo'][:50]}...")
    
    db.session.commit()
    
    # ==========================================
    # RIEPILOGO
    # ==========================================
    print("\n" + "="*60)
    print("✅ DATI DEMO AGGIUNTI!")
    print("="*60)
    print(f"\n📊 Totali:")
    print(f"   Obiettivi:  {Obiettivo.query.count()}")
    print(f"   Impegni:    {Impegno.query.count()}")
    print(f"   Spese:      {Spesa.query.count()}")
    print(f"   Diario:     {DiarioGiornaliero.query.count()}")
    
    print(f"\n🚀 Ricarica la pagina per vedere i dati!")
    print(f"   http://localhost:5000")
    print("\n" + "="*60 + "\n")

