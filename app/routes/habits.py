"""API endpoints per Habit Tracking"""

from flask import Blueprint, request, jsonify
from datetime import datetime, date, timedelta
from app import db, cache
from app.models.user_profile import UserProfile
from app.models.habit import Habit, HabitCompletion

bp = Blueprint("habits", __name__)


@bp.route("/api/habits", methods=["GET", "POST"])
@cache.cached(timeout=60, key_prefix='habits_list', unless=lambda: request.method == 'POST')
def gestisci_habits():
    """Lista o crea habits"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({"errore": "Nessun profilo trovato"}), 404

    if request.method == "POST":
        data = request.json
        
        habit = Habit(
            user_id=profilo.id,
            nome=data["nome"],
            descrizione=data.get("descrizione", ""),
            icona=data.get("icona", "✅"),
            colore=data.get("colore", "#667eea"),
            frequenza=data.get("frequenza", "daily"),
            giorni_settimana=data.get("giorni_settimana", ""),
            obiettivo_numero=data.get("obiettivo_numero", 1),
            unita_misura=data.get("unita_misura", "volte"),
        )
        
        db.session.add(habit)
        db.session.commit()
        
        # Invalida cache
        cache.delete('habits_list')
        
        return jsonify(habit.to_dict()), 201

    # GET - habits attive
    habits = Habit.query.filter_by(user_id=profilo.id, attiva=True).all()
    return jsonify([h.to_dict() for h in habits])


@bp.route("/api/habits/<int:id>", methods=["GET", "PUT", "DELETE"])
def modifica_habit(id):
    """Recupera, modifica o elimina habit"""
    habit = Habit.query.get_or_404(id)

    if request.method == "GET":
        return jsonify(habit.to_dict())

    elif request.method == "PUT":
        data = request.json
        for key, value in data.items():
            if hasattr(habit, key) and key not in ["id", "user_id", "created_at"]:
                setattr(habit, key, value)

        db.session.commit()
        cache.delete('habits_list')
        return jsonify(habit.to_dict())

    else:  # DELETE
        db.session.delete(habit)
        db.session.commit()
        cache.delete('habits_list')
        return "", 204


@bp.route("/api/habits/<int:id>/complete", methods=["POST"])
def completa_habit(id):
    """Segna habit come completata oggi"""
    habit = Habit.query.get_or_404(id)
    data = request.json or {}
    
    oggi = date.today()
    
    # Verifica se già completata oggi
    existing = HabitCompletion.query.filter_by(
        habit_id=id,
        data=oggi
    ).first()
    
    if existing:
        # Toggle completamento
        existing.completato = not existing.completato
        if not existing.completato:
            # Se de-completa, aggiorna ora
            existing.ora = datetime.now().time()
    else:
        # Crea nuovo completamento
        completion = HabitCompletion(
            habit_id=id,
            data=oggi,
            completato=True,
            valore=data.get('valore'),
            note=data.get('note'),
        )
        db.session.add(completion)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'habit': habit.to_dict(),
        'streak': habit.get_streak()
    })


@bp.route("/api/habits/today", methods=["GET"])
def habits_oggi():
    """Habits di oggi con stato completamento"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({"errore": "Nessun profilo trovato"}), 404

    oggi = date.today()
    habits = Habit.query.filter_by(user_id=profilo.id, attiva=True).all()
    
    result = []
    for habit in habits:
        completion_oggi = HabitCompletion.query.filter_by(
            habit_id=habit.id,
            data=oggi
        ).first()
        
        habit_dict = habit.to_dict()
        habit_dict['completato_oggi'] = completion_oggi.completato if completion_oggi else False
        habit_dict['valore_oggi'] = completion_oggi.valore if completion_oggi else None
        
        result.append(habit_dict)
    
    return jsonify(result)


@bp.route("/api/habits/<int:id>/history", methods=["GET"])
def habit_history(id):
    """Storico completamenti (heatmap data)"""
    habit = Habit.query.get_or_404(id)
    
    # Ultimi 90 giorni
    giorni = int(request.args.get('giorni', 90))
    start_date = date.today() - timedelta(days=giorni)
    
    completions = HabitCompletion.query.filter(
        HabitCompletion.habit_id == id,
        HabitCompletion.data >= start_date
    ).all()
    
    # Crea heatmap data
    heatmap = {}
    for comp in completions:
        heatmap[comp.data.isoformat()] = {
            'completato': comp.completato,
            'valore': comp.valore,
            'note': comp.note
        }
    
    return jsonify({
        'habit': habit.to_dict(),
        'heatmap': heatmap,
        'total_completions': len([c for c in completions if c.completato]),
        'completion_rate': habit.get_completion_rate(giorni)
    })


@bp.route("/api/habits/stats", methods=["GET"])
def habits_stats():
    """Statistiche generali habits"""
    profilo = UserProfile.query.first()
    if not profilo:
        return jsonify({"errore": "Nessun profilo trovato"}), 404

    habits = Habit.query.filter_by(user_id=profilo.id, attiva=True).all()
    
    if not habits:
        return jsonify({
            'total_habits': 0,
            'completed_today': 0,
            'best_streak': 0,
            'total_completions': 0
        })
    
    oggi = date.today()
    completed_today = 0
    best_streak = 0
    total_completions = 0
    
    for habit in habits:
        # Check oggi
        comp_oggi = HabitCompletion.query.filter_by(
            habit_id=habit.id,
            data=oggi,
            completato=True
        ).first()
        if comp_oggi:
            completed_today += 1
        
        # Streak
        streak = habit.get_streak()
        best_streak = max(best_streak, streak)
        
        # Total
        total_completions += habit.completamenti.filter_by(completato=True).count()
    
    return jsonify({
        'total_habits': len(habits),
        'completed_today': completed_today,
        'best_streak': best_streak,
        'total_completions': total_completions,
        'completion_rate_today': round((completed_today / len(habits) * 100), 1) if habits else 0
    })

