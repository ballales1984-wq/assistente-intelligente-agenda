"""Community Routes - Social Features"""
from flask import Blueprint, request, jsonify, render_template
from datetime import datetime, date, timedelta
from app import db, limiter
from app.models import UserProfile
from app.models.community import (
    ReflectionShare, Reaction, Comment, Circle, CircleMember,
    Challenge, ChallengeParticipation, ReactionType
)
from app.core.auth_fingerprint import FingerprintAuth, require_user
from app.utils.content_safety import is_safe_content, get_crisis_resources
import secrets

bp = Blueprint('community', __name__, url_prefix='/api/community')


# ========================================
# AUTH - User identification
# ========================================

@bp.route('/whoami', methods=['GET'])
def whoami():
    """Get info sull'utente corrente (auto-identificato via fingerprint)"""
    user = FingerprintAuth.get_or_create_user()
    
    if not user:
        return jsonify({
            'success': False,
            'authenticated': False
        })
    
    return jsonify({
        'success': True,
        'authenticated': True,
        'user': {
            'id': user.id,
            'name': user.nome,
            'fingerprint_id': user.fingerprint[:12] + '...' if user.fingerprint else None,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'is_new': FingerprintAuth.is_new_user()
        }
    })


# ========================================
# REFLECTIONS - Condivisione riflessioni
# ========================================

@bp.route('/reflections', methods=['GET'])
def get_reflections():
    """
    Get community feed di riflessioni
    Query params:
    - language: Filtra per lingua (it, en, es, etc)
    - category: Filtra per categoria
    - limit: Max risultati (default 20, max 50)
    """
    language = request.args.get('language', 'it')
    category = request.args.get('category')
    limit = min(int(request.args.get('limit', 20)), 50)
    
    # Base query: solo pubbliche e approvate
    query = ReflectionShare.query.filter_by(
        approved=True,
        language=language
    ).filter(
        ReflectionShare.visibility.in_(['public', 'anonymous'])
    )
    
    # Filter by category
    if category:
        query = query.filter_by(category=category)
    
    # Order by recent
    reflections = query.order_by(
        ReflectionShare.created_at.desc()
    ).limit(limit).all()
    
    return jsonify({
        'success': True,
        'data': [r.to_dict(include_user=True) for r in reflections],
        'total': len(reflections)
    })


@bp.route('/reflections', methods=['POST'])
@limiter.limit("10 per hour")
def create_reflection():
    """
    Condividi una riflessione con la community
    
    Body:
    {
        "text": "La mia riflessione...",
        "visibility": "anonymous/public",
        "category": "personal_growth",
        "tags": ["meditation", "mindfulness"]
    }
    """
    data = request.json
    
    # Validation
    if not data or not data.get('text'):
        return jsonify({'success': False, 'error': 'Text required'}), 400
    
    text = data['text'].strip()
    
    if len(text) < 20:
        return jsonify({'success': False, 'error': 'Reflection too short (min 20 characters)'}), 400
    
    if len(text) > 5000:
        return jsonify({'success': False, 'error': 'Reflection too long (max 5000 characters)'}), 400
    
    # ========================================
    # SAFETY CHECKS (Crisis, Banned Keywords, Spam, Minors)
    # ========================================
    is_safe, error_type, extra_info = is_safe_content(text)
    
    if not is_safe:
        if error_type == 'crisis_detected':
            return jsonify({
                'success': False,
                'crisis_detected': True,
                'message': '🆘 Notiamo che potresti attraversare un momento difficile.\n\n'
                          'Questa community non può sostituire aiuto professionale.\n\n'
                          'Per favore contatta SUBITO:\n'
                          '📞 Telefono Amico: 02.2327.2327 (24/7, gratuito)\n'
                          '🚑 Emergenza: 112\n\n'
                          'Siamo qui per supporto peer, ma crisi acute richiedono professionisti. ❤️',
                'resources': extra_info.get('help_resources', [])
            }), 400
        
        elif error_type == 'banned_content':
            return jsonify({
                'success': False,
                'error': 'Contenuto non permesso. Rispetta le regole community.',
                'details': 'Il tuo post viola le nostre linee guida (violenza, hate speech, o contenuto illegale).'
            }), 400
        
        elif error_type == 'spam_detected':
            return jsonify({
                'success': False,
                'error': 'Il contenuto sembra spam.',
                'details': 'Se non è spam, riformula in modo più naturale (meno link, meno ripetizioni).'
            }), 400
        
        elif error_type == 'minor_detected':
            return jsonify({
                'success': False,
                'error': 'La community è riservata a maggiorenni (18+).',
                'details': 'Puoi usare l\'app personale (agenda/diario privato), ma non le funzioni community.'
            }), 403
    
    # Get or create user automaticamente (fingerprint-based!)
    profilo = FingerprintAuth.get_or_create_user()
    if not profilo:
        return jsonify({'success': False, 'error': 'Unable to identify user'}), 401
    
    # Check if user is banned
    from app.models.community import UserBan
    active_ban = UserBan.query.filter_by(
        user_id=profilo.id,
        active=True
    ).first()
    
    if active_ban:
        return jsonify({
            'success': False,
            'banned': True,
            'ban_type': active_ban.ban_type,
            'reason': active_ban.reason,
            'expires_at': active_ban.expires_at.isoformat() if active_ban.expires_at else None
        }), 403
    
    # Sentiment analysis (basic)
    from app.core.diario_manager import DiarioManager
    diario_mgr = DiarioManager(profilo)
    analisi = diario_mgr.analizza_testo(text)
    
    # Create reflection
    reflection = ReflectionShare(
        user_id=profilo.id,
        shared_text=text,
        original_text=text,
        visibility=data.get('visibility', 'anonymous'),
        category=data.get('category', 'personal_growth'),
        tags=','.join(data.get('tags', [])) if data.get('tags') else '',
        sentiment=analisi.get('sentiment', 'neutral'),
        language=data.get('language', 'it')
    )
    
    try:
        db.session.add(reflection)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': reflection.to_dict(include_user=True),
            'message': 'Reflection shared with community!'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/reflections/<int:reflection_id>', methods=['DELETE'])
def delete_reflection(reflection_id):
    """Elimina una riflessione (solo owner)"""
    reflection = ReflectionShare.query.get_or_404(reflection_id)
    
    # TODO: Check ownership (auth system)
    # if reflection.user_id != current_user.id:
    #     return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        db.session.delete(reflection)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Reflection deleted'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ========================================
# REACTIONS - Reazioni supportive
# ========================================

@bp.route('/reflections/<int:reflection_id>/react', methods=['POST'])
@limiter.limit("30 per hour")
def add_reaction(reflection_id):
    """
    Aggiungi reazione a una riflessione
    
    Body:
    {
        "reaction_type": "support"  // support, me_too, insightful, inspiring
    }
    """
    data = request.json
    reaction_type = data.get('reaction_type')
    
    # Validation
    valid_types = ['support', 'me_too', 'insightful', 'inspiring']
    if reaction_type not in valid_types:
        return jsonify({'success': False, 'error': f'Invalid reaction type. Use: {valid_types}'}), 400
    
    # Get or create user automaticamente
    profilo = FingerprintAuth.get_or_create_user()
    
    # Check reflection exists
    reflection = ReflectionShare.query.get_or_404(reflection_id)
    
    # Check if already reacted
    existing = Reaction.query.filter_by(
        user_id=profilo.id,
        reflection_id=reflection_id
    ).first()
    
    if existing:
        # Update reaction type
        existing.reaction_type = reaction_type
        existing.created_at = datetime.utcnow()
    else:
        # Create new reaction
        reaction = Reaction(
            user_id=profilo.id,
            reflection_id=reflection_id,
            reaction_type=reaction_type
        )
        db.session.add(reaction)
        
        # Update counter
        reflection.reactions_count += 1
    
    try:
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Reaction added',
            'total_reactions': reflection.reactions_count
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/reflections/<int:reflection_id>/react', methods=['DELETE'])
def remove_reaction(reflection_id):
    """Rimuovi la tua reazione"""
    profilo = FingerprintAuth.get_or_create_user()
    
    reaction = Reaction.query.filter_by(
        user_id=profilo.id,
        reflection_id=reflection_id
    ).first()
    
    if not reaction:
        return jsonify({'success': False, 'error': 'Reaction not found'}), 404
    
    # Update counter
    reflection = ReflectionShare.query.get(reflection_id)
    if reflection:
        reflection.reactions_count = max(0, reflection.reactions_count - 1)
    
    try:
        db.session.delete(reaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Reaction removed'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ========================================
# COMMENTS - Commenti thoughtful
# ========================================

@bp.route('/reflections/<int:reflection_id>/comments', methods=['GET'])
def get_comments(reflection_id):
    """Get commenti di una riflessione"""
    comments = Comment.query.filter_by(
        reflection_id=reflection_id,
        parent_id=None,  # Solo top-level
        approved=True
    ).order_by(Comment.created_at.asc()).all()
    
    # Include replies
    result = []
    for comment in comments:
        comment_dict = comment.to_dict()
        
        # Add replies
        replies = Comment.query.filter_by(
            parent_id=comment.id,
            approved=True
        ).order_by(Comment.created_at.asc()).all()
        
        comment_dict['replies'] = [r.to_dict() for r in replies]
        result.append(comment_dict)
    
    return jsonify({
        'success': True,
        'data': result,
        'total': len(result)
    })


@bp.route('/reflections/<int:reflection_id>/comments', methods=['POST'])
@limiter.limit("20 per hour")
def create_comment(reflection_id):
    """
    Aggiungi commento thoughtful
    
    Body:
    {
        "text": "Your thoughtful response...",
        "parent_id": null  // Optional, for replies
    }
    """
    data = request.json
    
    # Validation
    if not data or not data.get('text'):
        return jsonify({'success': False, 'error': 'Text required'}), 400
    
    text = data['text'].strip()
    
    # Enforce thoughtful comments (min 50 characters)
    if len(text) < 50:
        return jsonify({
            'success': False,
            'error': 'Comment too short. Please share your experience or advice (min 50 characters)'
        }), 400
    
    if len(text) > 2000:
        return jsonify({'success': False, 'error': 'Comment too long (max 2000 characters)'}), 400
    
    # Get or create user automaticamente
    profilo = FingerprintAuth.get_or_create_user()
    
    # Check reflection exists
    reflection = ReflectionShare.query.get_or_404(reflection_id)
    
    # Create comment
    comment = Comment(
        user_id=profilo.id,
        reflection_id=reflection_id,
        text=text,
        parent_id=data.get('parent_id')
    )
    
    # Update counter
    reflection.comments_count += 1
    
    try:
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': comment.to_dict(),
            'message': 'Comment added'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ========================================
# CIRCLES - Accountability groups
# ========================================

@bp.route('/circles', methods=['GET'])
def get_my_circles():
    """Get circles dell'utente"""
    profilo = FingerprintAuth.get_or_create_user()
    
    # Get circles where user is member
    memberships = CircleMember.query.filter_by(user_id=profilo.id).all()
    circles = [Circle.query.get(m.circle_id) for m in memberships]
    circles = [c for c in circles if c and c.active]
    
    return jsonify({
        'success': True,
        'data': [c.to_dict() for c in circles]
    })


@bp.route('/circles', methods=['POST'])
@limiter.limit("5 per day")
def create_circle():
    """
    Crea un nuovo circle
    
    Body:
    {
        "name": "Python Learners",
        "description": "Learning Python together",
        "max_members": 10,
        "is_private": true,
        "focus_category": "learning"
    }
    """
    data = request.json
    
    # Validation
    if not data or not data.get('name'):
        return jsonify({'success': False, 'error': 'Circle name required'}), 400
    
    # Get or create user automaticamente
    profilo = FingerprintAuth.get_or_create_user()
    
    # Generate unique invite code
    invite_code = secrets.token_urlsafe(12)
    
    # Create circle
    circle = Circle(
        name=data['name'],
        description=data.get('description'),
        creator_id=profilo.id,
        max_members=min(int(data.get('max_members', 10)), 50),  # Max 50
        is_private=data.get('is_private', True),
        invite_code=invite_code,
        focus_category=data.get('focus_category')
    )
    
    try:
        db.session.add(circle)
        db.session.flush()  # Get circle.id
        
        # Add creator as admin member
        member = CircleMember(
            circle_id=circle.id,
            user_id=profilo.id,
            role='admin'
        )
        db.session.add(member)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': circle.to_dict(),
            'invite_code': invite_code,
            'message': f'Circle "{circle.name}" created! Share invite code with friends.'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/circles/join/<invite_code>', methods=['POST'])
def join_circle(invite_code):
    """Join un circle tramite invite code"""
    
    # Find circle
    circle = Circle.query.filter_by(invite_code=invite_code, active=True).first()
    
    if not circle:
        return jsonify({'success': False, 'error': 'Circle not found or inactive'}), 404
    
    # Check if full
    current_members = circle.members.count()
    if current_members >= circle.max_members:
        return jsonify({'success': False, 'error': 'Circle is full'}), 400
    
    # Get or create user automaticamente
    profilo = FingerprintAuth.get_or_create_user()
    
    # Check if already member
    existing = CircleMember.query.filter_by(
        circle_id=circle.id,
        user_id=profilo.id
    ).first()
    
    if existing:
        return jsonify({
            'success': True,
            'message': 'Already a member!',
            'data': circle.to_dict()
        })
    
    # Add member
    member = CircleMember(
        circle_id=circle.id,
        user_id=profilo.id,
        role='member'
    )
    
    try:
        db.session.add(member)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': circle.to_dict(),
            'message': f'Joined circle "{circle.name}"!'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/circles/<int:circle_id>/members', methods=['GET'])
def get_circle_members(circle_id):
    """Get membri di un circle"""
    circle = Circle.query.get_or_404(circle_id)
    
    # TODO: Check user is member (auth)
    
    members = CircleMember.query.filter_by(circle_id=circle_id).all()
    
    return jsonify({
        'success': True,
        'data': [m.to_dict() for m in members],
        'total': len(members)
    })


# ========================================
# CHALLENGES - Monthly challenges
# ========================================

@bp.route('/challenges', methods=['GET'])
def get_challenges():
    """Get active challenges"""
    language = request.args.get('language', 'it')
    
    today = date.today()
    
    # Get active challenges
    challenges = Challenge.query.filter(
        Challenge.end_date >= today,
        Challenge.language == language
    ).order_by(
        Challenge.participants_count.desc()
    ).limit(20).all()
    
    return jsonify({
        'success': True,
        'data': [c.to_dict() for c in challenges]
    })


@bp.route('/challenges/<int:challenge_id>/join', methods=['POST'])
def join_challenge(challenge_id):
    """Unisciti a un challenge"""
    challenge = Challenge.query.get_or_404(challenge_id)
    
    # Check if still active
    if challenge.end_date < date.today():
        return jsonify({'success': False, 'error': 'Challenge has ended'}), 400
    
    # Get or create user automaticamente
    profilo = FingerprintAuth.get_or_create_user()
    
    # Check if already joined
    existing = ChallengeParticipation.query.filter_by(
        challenge_id=challenge_id,
        user_id=profilo.id
    ).first()
    
    if existing:
        return jsonify({
            'success': True,
            'message': 'Already participating!',
            'data': existing.to_dict()
        })
    
    # Create participation
    participation = ChallengeParticipation(
        challenge_id=challenge_id,
        user_id=profilo.id
    )
    
    # Update counter
    challenge.participants_count += 1
    
    try:
        db.session.add(participation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': participation.to_dict(),
            'message': f'Joined challenge "{challenge.title}"!'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/challenges/<int:challenge_id>/checkin', methods=['POST'])
def challenge_checkin(challenge_id):
    """Daily check-in per un challenge"""
    profilo = FingerprintAuth.get_or_create_user()
    
    participation = ChallengeParticipation.query.filter_by(
        challenge_id=challenge_id,
        user_id=profilo.id
    ).first_or_404()
    
    # Check if already checked in today
    today = date.today()
    if participation.last_check_in and participation.last_check_in.date() == today:
        return jsonify({
            'success': True,
            'message': 'Already checked in today!',
            'data': participation.to_dict()
        })
    
    # Update participation
    participation.days_completed += 1
    participation.last_check_in = datetime.utcnow()
    
    # Update streak
    if participation.last_check_in and \
       (today - participation.last_check_in.date()).days == 1:
        participation.current_streak += 1
    else:
        participation.current_streak = 1
    
    # Update longest streak
    if participation.current_streak > participation.longest_streak:
        participation.longest_streak = participation.current_streak
    
    # Check if completed
    challenge = Challenge.query.get(challenge_id)
    days_total = (challenge.end_date - challenge.start_date).days + 1
    
    if participation.days_completed >= days_total:
        participation.completed = True
        participation.completed_at = datetime.utcnow()
    
    try:
        db.session.commit()
        
        message = f'Day {participation.days_completed} completed! Streak: {participation.current_streak} 🔥'
        
        if participation.completed:
            message = f'🎉 Challenge completed! You did all {days_total} days!'
        
        return jsonify({
            'success': True,
            'data': participation.to_dict(),
            'message': message
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ========================================
# STATS - Community statistics
# ========================================

@bp.route('/stats', methods=['GET'])
def community_stats():
    """Statistiche community globali"""
    
    total_reflections = ReflectionShare.query.filter_by(approved=True).count()
    total_comments = Comment.query.filter_by(approved=True).count()
    total_reactions = Reaction.query.count()
    total_circles = Circle.query.filter_by(active=True).count()
    total_challenges = Challenge.query.filter(Challenge.end_date >= date.today()).count()
    
    # Top categories
    from sqlalchemy import func
    top_categories = db.session.query(
        ReflectionShare.category,
        func.count(ReflectionShare.id).label('count')
    ).filter_by(approved=True).group_by(
        ReflectionShare.category
    ).order_by(
        func.count(ReflectionShare.id).desc()
    ).limit(5).all()
    
    return jsonify({
        'success': True,
        'data': {
            'total_reflections': total_reflections,
            'total_comments': total_comments,
            'total_reactions': total_reactions,
            'total_circles': total_circles,
            'active_challenges': total_challenges,
            'top_categories': [
                {'category': cat, 'count': count}
                for cat, count in top_categories
            ]
        }
    })


# ========================================
# MODERATION - Basic tools
# ========================================

@bp.route('/reflections/<int:reflection_id>/flag', methods=['POST'])
@limiter.limit("10 per day")
def flag_reflection(reflection_id):
    """Segnala una riflessione inappropriata"""
    data = request.json
    reason = data.get('reason', 'No reason provided')
    
    reflection = ReflectionShare.query.get_or_404(reflection_id)
    
    reflection.flagged = True
    reflection.flag_count += 1
    
    # Auto-hide if too many flags
    if reflection.flag_count >= 3:
        reflection.approved = False
    
    try:
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Reflection flagged for review. Thank you for keeping our community safe.'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

