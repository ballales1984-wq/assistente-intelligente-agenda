"""API endpoints"""
from flask import Blueprint, request, jsonify, render_template
from datetime import datetime, timedelta, date
from app import db
from app.models import UserProfile, Obiettivo, Impegno, DiarioGiornaliero
from app.core import InputManager, AgendaDinamica, MotoreAdattivo, DiarioManager
from app.managers import PassatoManager, PresenteManager, FuturoManager

bp = Blueprint('api', __name__)


@bp.route('/')
def index():
    """Pagina principale"""
    return render_template('index.html')


@bp.route('/api/profilo', methods=['GET', 'POST'])
def gestisci_profilo():
    """Crea o recupera il profilo utente"""
    if request.method == 'POST':
        data = request.json
        
        profilo = UserProfile.query.first()
        if not profilo:
            profilo = UserProfile(
                nome=data.get('nome', 'Utente'),
                stress_tollerato=data.get('stress_tollerato', 'medio'),
                concentrazione=data.get('concentrazione', 'media'),
                priorita=data.get('priorita', 'bilanciato'),
                stile_vita=data.get('stile_vita', 'bilanciato')
            )
            db.session.add(profilo)
        else:
            # Aggiorna profilo esistente
            for key, value in data.items():
                if hasattr(profilo, key):
                    setattr(profilo, key, value)
        
        db.session.commit()
        return jsonify(profilo.to_dict()), 201
    
    # GET
    profilo = UserProfile.query.first()
    if not profilo:
        # Crea profilo di default
        profilo = UserProfile(nome='Utente')
        db.session.add(profilo)
        db.session.commit()
    
    return jsonify(profilo.to_dict())


@bp.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint principale per interazione testuale"""
    data = request.json
    messaggio = data.get('messaggio', '').strip()
    
    if not messaggio:
        return jsonify({'errore': 'Messaggio vuoto'}), 400
    
    # Ottieni profilo utente
    profilo = UserProfile.query.first()
    if not profilo:
        profilo = UserProfile(nome='Utente')
        db.session.add(profilo)
        db.session.commit()
    
    # Analizza input
    input_manager = InputManager()
    risultato = input_manager.analizza_input(messaggio)
    
    risposta = {
        'messaggio': messaggio,
        'tipo_riconosciuto': risultato['tipo'],
        'risposta': '',
        'dati': None
    }
    
    # Gestisci in base al tipo
    if risultato['tipo'] == 'obiettivo':
        obiettivo = Obiettivo(
            user_id=profilo.id,
            nome=risultato['dati']['nome'],
            tipo=risultato['dati']['tipo'],
            durata_settimanale=risultato['dati']['durata_settimanale'],
            intensita='media'
        )
        db.session.add(obiettivo)
        db.session.commit()
        
        risposta['risposta'] = f"✅ Perfetto! Ho aggiunto l'obiettivo '{obiettivo.nome}' " \
                               f"con {obiettivo.durata_settimanale}h a settimana."
        risposta['dati'] = obiettivo.to_dict()
    
    elif risultato['tipo'] == 'impegno':
        # Crea impegno
        dati_impegno = risultato['dati']
        
        # Determina la data (prossima occorrenza del giorno se specificato)
        data_impegno = datetime.now()
        if 'giorno' in dati_impegno:
            # Trova prossima occorrenza del giorno
            giorni = {
                'lunedì': 0, 'martedì': 1, 'mercoledì': 2, 
                'giovedì': 3, 'venerdì': 4, 'sabato': 5, 'domenica': 6
            }
            giorno_target = giorni.get(dati_impegno['giorno'].lower())
            if giorno_target is not None:
                giorni_diff = (giorno_target - data_impegno.weekday()) % 7
                if giorni_diff == 0:
                    giorni_diff = 7
                data_impegno = data_impegno + timedelta(days=giorni_diff)
        
        # Crea datetime con orari
        ora_inizio = datetime.strptime(dati_impegno['ora_inizio'], '%H:%M').time()
        data_inizio = datetime.combine(data_impegno.date(), ora_inizio)
        
        if dati_impegno.get('ora_fine'):
            ora_fine = datetime.strptime(dati_impegno['ora_fine'], '%H:%M').time()
            data_fine = datetime.combine(data_impegno.date(), ora_fine)
        else:
            data_fine = data_inizio + timedelta(hours=1)
        
        impegno = Impegno(
            user_id=profilo.id,
            nome=dati_impegno['nome'],
            data_inizio=data_inizio,
            data_fine=data_fine,
            tipo='personale'
        )
        db.session.add(impegno)
        db.session.commit()
        
        risposta['risposta'] = f"📅 Ho aggiunto l'impegno '{impegno.nome}' " \
                               f"per {data_inizio.strftime('%d/%m/%Y alle %H:%M')}."
        risposta['dati'] = impegno.to_dict()
    
    elif risultato['tipo'] == 'stato':
        risposta['risposta'] = f"💭 Ho capito che sei {risultato['dati']['stato']}. " \
                               f"{risultato['dati']['suggerimento']}"
    
    elif risultato['tipo'] == 'preferenza':
        risposta['risposta'] = "🌿 Ho preso nota della tua preferenza. " \
                               "Adatterò il piano per includere più pause."
    
    elif risultato['tipo'] == 'completamento':
        risposta['risposta'] = risultato['dati']['messaggio']
        risposta['dati'] = risultato['dati']
    
    elif risultato['tipo'] == 'aiuto':
        suggerimenti = '\n'.join(f"• {s}" for s in risultato['dati']['suggerimenti'])
        risposta['risposta'] = f"💡 Ecco come puoi usarmi:\n\n{suggerimenti}"
        risposta['dati'] = risultato['dati']
    
    elif risultato['tipo'] == 'tempo_libero':
        risposta['risposta'] = f"⏰ Con {risultato['dati']['ore']} ore disponibili:\n" \
                               f"{risultato['dati']['suggerimento']}"
        risposta['dati'] = risultato['dati']
    
    elif risultato['tipo'] == 'diario':
        # Salva riflessione nel diario
        dati_diario = risultato['dati']
        
        diario_entry = DiarioGiornaliero(
            user_id=profilo.id,
            data=dati_diario.get('data', date.today()),
            testo=dati_diario['testo'],
            sentiment=dati_diario['sentiment']
        )
        
        # Imposta riflessioni e parole chiave
        diario_entry.set_riflessioni(dati_diario['riflessioni'])
        diario_entry.parole_chiave = ','.join(dati_diario['parole_chiave'])
        
        db.session.add(diario_entry)
        db.session.commit()
        
        # Costruisci risposta
        parole_chiave_str = ', '.join(dati_diario['parole_chiave'][:5])
        sentiment_emoji = {'positivo': '😊', 'neutro': '😐', 'negativo': '😔'}
        emoji = sentiment_emoji.get(dati_diario['sentiment'], '📝')
        
        risposta['risposta'] = f"{emoji} Ho salvato la tua riflessione nel diario!\n\n" \
                               f"📌 Concetti chiave: {parole_chiave_str}\n" \
                               f"💭 Sentiment: {dati_diario['sentiment']}"
        risposta['dati'] = diario_entry.to_dict()
    
    else:
        risposta['risposta'] = "🤔 Non ho capito bene. Prova a dire:\n" \
                               "• 'Voglio studiare Python 3 ore a settimana'\n" \
                               "• 'Domenica vado al mare dalle 16 alle 20'\n" \
                               "• 'Sono stanco' per ricevere suggerimenti\n" \
                               "• 'Aiutami' per vedere tutti i comandi\n" \
                               "• Oppure scrivi una riflessione libera per il diario!"
    
    return jsonify(risposta)


@bp.route('/api/piano', methods=['GET'])
def genera_piano():
    """Genera piano settimanale"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    # Genera piano
    agenda = AgendaDinamica(profilo)
    piano = agenda.genera_piano_settimanale()
    
    # Converti datetime in stringhe
    piano_serializzabile = []
    for attivita in piano:
        att_dict = attivita.copy()
        att_dict['data_inizio'] = attivita['data_inizio'].isoformat()
        att_dict['data_fine'] = attivita['data_fine'].isoformat()
        piano_serializzabile.append(att_dict)
    
    return jsonify({
        'piano': piano_serializzabile,
        'profilo': profilo.to_dict()
    })


@bp.route('/api/obiettivi', methods=['GET', 'POST'])
def gestisci_obiettivi():
    """Lista o crea obiettivi"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    if request.method == 'POST':
        data = request.json
        obiettivo = Obiettivo(
            user_id=profilo.id,
            nome=data['nome'],
            tipo=data.get('tipo', 'personale'),
            durata_settimanale=data['durata_settimanale'],
            intensita=data.get('intensita', 'media')
        )
        
        if 'scadenza' in data:
            obiettivo.scadenza = datetime.fromisoformat(data['scadenza']).date()
        
        db.session.add(obiettivo)
        db.session.commit()
        
        return jsonify(obiettivo.to_dict()), 201
    
    # GET
    obiettivi = profilo.obiettivi.filter_by(attivo=True).all()
    return jsonify([obj.to_dict() for obj in obiettivi])


@bp.route('/api/obiettivi/<int:id>', methods=['PUT', 'DELETE'])
def modifica_obiettivo(id):
    """Modifica o elimina obiettivo"""
    obiettivo = Obiettivo.query.get_or_404(id)
    
    if request.method == 'PUT':
        data = request.json
        for key, value in data.items():
            if hasattr(obiettivo, key):
                setattr(obiettivo, key, value)
        
        db.session.commit()
        return jsonify(obiettivo.to_dict())
    
    # DELETE
    db.session.delete(obiettivo)
    db.session.commit()
    return '', 204


@bp.route('/api/impegni', methods=['GET', 'POST'])
def gestisci_impegni():
    """Lista o crea impegni"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    if request.method == 'POST':
        data = request.json
        impegno = Impegno(
            user_id=profilo.id,
            nome=data['nome'],
            data_inizio=datetime.fromisoformat(data['data_inizio']),
            data_fine=datetime.fromisoformat(data['data_fine']),
            tipo=data.get('tipo', 'personale')
        )
        
        db.session.add(impegno)
        db.session.commit()
        
        return jsonify(impegno.to_dict()), 201
    
    # GET - impegni della settimana (passati 3 giorni + futuri 10 giorni)
    data_inizio = datetime.now() - timedelta(days=3)
    data_fine = datetime.now() + timedelta(days=10)
    
    impegni = profilo.impegni.filter(
        Impegno.data_inizio >= data_inizio,
        Impegno.data_inizio <= data_fine
    ).order_by(Impegno.data_inizio).all()
    
    return jsonify([imp.to_dict() for imp in impegni])


@bp.route('/api/impegni/giorno/<data>', methods=['GET'])
def impegni_giorno(data):
    """Ottieni impegni di un giorno specifico"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    try:
        data_richiesta = datetime.fromisoformat(data).date()
        data_inizio = datetime.combine(data_richiesta, datetime.min.time())
        data_fine = datetime.combine(data_richiesta, datetime.max.time())
        
        impegni = profilo.impegni.filter(
            Impegno.data_inizio >= data_inizio,
            Impegno.data_inizio <= data_fine
        ).order_by(Impegno.data_inizio).all()
        
        return jsonify([imp.to_dict() for imp in impegni])
    except ValueError:
        return jsonify({'errore': 'Formato data non valido'}), 400


@bp.route('/api/statistiche', methods=['GET'])
def statistiche():
    """Statistiche produttività"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    motore = MotoreAdattivo(profilo)
    stats = motore.analizza_produttivita()
    
    return jsonify(stats)


@bp.route('/api/diario', methods=['GET', 'POST'])
def gestisci_diario():
    """Lista o crea entry nel diario"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    if request.method == 'POST':
        data = request.json
        
        # Analizza il testo
        analisi = DiarioManager.analizza_testo(data['testo'])
        
        diario_entry = DiarioGiornaliero(
            user_id=profilo.id,
            data=datetime.fromisoformat(data['data']).date() if 'data' in data else date.today(),
            testo=data['testo'],
            sentiment=analisi['sentiment']
        )
        
        diario_entry.set_riflessioni(analisi['riflessioni'])
        diario_entry.parole_chiave = ','.join(analisi['parole_chiave'])
        
        db.session.add(diario_entry)
        db.session.commit()
        
        return jsonify(diario_entry.to_dict()), 201
    
    # GET - ultime 30 entry del diario
    entries = profilo.diario_entries.order_by(
        DiarioGiornaliero.data.desc()
    ).limit(30).all()
    
    return jsonify([entry.to_dict() for entry in entries])


@bp.route('/api/diario/<int:id>', methods=['GET', 'DELETE'])
def gestisci_diario_entry(id):
    """Recupera o elimina una entry del diario"""
    entry = DiarioGiornaliero.query.get_or_404(id)
    
    if request.method == 'DELETE':
        db.session.delete(entry)
        db.session.commit()
        return '', 204
    
    # GET
    return jsonify(entry.to_dict())


@bp.route('/api/diario/cerca', methods=['POST'])
def cerca_diario():
    """Cerca nel diario per parola chiave o data"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    data = request.json
    query = profilo.diario_entries
    
    # Filtra per parola chiave
    if 'parola_chiave' in data:
        parola = data['parola_chiave'].lower()
        query = query.filter(
            db.or_(
                DiarioGiornaliero.testo.ilike(f'%{parola}%'),
                DiarioGiornaliero.parole_chiave.ilike(f'%{parola}%')
            )
        )
    
    # Filtra per data
    if 'data_inizio' in data:
        query = query.filter(
            DiarioGiornaliero.data >= datetime.fromisoformat(data['data_inizio']).date()
        )
    
    if 'data_fine' in data:
        query = query.filter(
            DiarioGiornaliero.data <= datetime.fromisoformat(data['data_fine']).date()
        )
    
    # Filtra per sentiment
    if 'sentiment' in data:
        query = query.filter(DiarioGiornaliero.sentiment == data['sentiment'])
    
    entries = query.order_by(DiarioGiornaliero.data.desc()).limit(50).all()
    
    return jsonify([entry.to_dict() for entry in entries])


# ═══════════════════════════════════════════════════════════════
# ENDPOINT TEMPORALI - Passato, Presente, Futuro
# ═══════════════════════════════════════════════════════════════

@bp.route('/api/passato/settimana-scorsa', methods=['GET'])
def analizza_settimana_scorsa():
    """Analizza cosa è stato fatto la settimana scorsa"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    passato = PassatoManager(profilo)
    analisi = passato.cosa_ho_fatto_settimana_scorsa()
    
    return jsonify(analisi)


@bp.route('/api/passato/periodo', methods=['POST'])
def analizza_periodo_passato():
    """Analizza un periodo specifico del passato"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    data = request.json
    data_inizio = datetime.fromisoformat(data['data_inizio']).date()
    data_fine = datetime.fromisoformat(data['data_fine']).date()
    
    passato = PassatoManager(profilo)
    analisi = passato.analizza_passato(data_inizio, data_fine)
    
    return jsonify(analisi)


@bp.route('/api/passato/pattern', methods=['POST'])
def trova_pattern():
    """Trova pattern ricorrenti nelle attività"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    data = request.json
    data_inizio = datetime.fromisoformat(data.get('data_inizio', (date.today() - timedelta(days=30)).isoformat())).date()
    data_fine = datetime.fromisoformat(data.get('data_fine', date.today().isoformat())).date()
    
    passato = PassatoManager(profilo)
    pattern = passato.trova_pattern_ricorrenti(data_inizio, data_fine)
    
    return jsonify(pattern)


@bp.route('/api/presente/oggi', methods=['GET'])
def piano_oggi():
    """Piano dettagliato di oggi"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    presente = PresenteManager(profilo)
    piano = presente.cosa_devo_fare_oggi()
    
    return jsonify(piano)


@bp.route('/api/presente/adesso', methods=['GET'])
def cosa_fare_adesso():
    """Cosa fare in questo momento"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    presente = PresenteManager(profilo)
    situazione = presente.ora_corrente_cosa_fare()
    
    return jsonify(situazione)


@bp.route('/api/presente/adatta', methods=['POST'])
def adatta_piano_stato():
    """Adatta il piano allo stato corrente"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    data = request.json
    stato = data.get('stato', 'normale')
    data_piano = datetime.fromisoformat(data.get('data', date.today().isoformat())).date()
    
    presente = PresenteManager(profilo)
    piano_adattato = presente.adatta_piano_a_stato(stato, data_piano)
    
    return jsonify(piano_adattato)


@bp.route('/api/futuro/simula/<data>', methods=['GET'])
def simula_giorno_futuro(data):
    """Simula una giornata futura"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    try:
        data_simulazione = datetime.fromisoformat(data).date()
        futuro = FuturoManager(profilo)
        simulazione = futuro.simula_giornata(data_simulazione)
        
        return jsonify(simulazione)
    except ValueError:
        return jsonify({'errore': 'Formato data non valido'}), 400


@bp.route('/api/futuro/giovedi', methods=['GET'])
def come_sara_giovedi():
    """Simula il prossimo giovedì"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    futuro = FuturoManager(profilo)
    simulazione = futuro.come_sara_giovedi()
    
    return jsonify(simulazione)


@bp.route('/api/futuro/proietta', methods=['POST'])
def proietta_competenze():
    """Proietta competenze future"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    data = request.json
    obiettivo = data['obiettivo']
    ore_settimanali = float(data.get('ore_settimanali', 3.0))
    mesi = int(data.get('mesi', 6))
    
    futuro = FuturoManager(profilo)
    proiezione = futuro.proietta_competenze(obiettivo, ore_settimanali, mesi)
    
    return jsonify(proiezione)


@bp.route('/api/futuro/prossima-settimana', methods=['GET'])
def prevedi_prossima_settimana():
    """Previsione settimana prossima"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({'errore': 'Nessun profilo trovato'}), 404
    
    futuro = FuturoManager(profilo)
    previsione = futuro.prevedi_prossima_settimana()
    
    return jsonify(previsione)

