"""Modelli per Community Features"""
from app import db
from datetime import datetime
from enum import Enum
import json


class VisibilityType(str, Enum):
    """Tipi di visibilità per riflessioni condivise"""
    PRIVATE = 'private'
    ANONYMOUS = 'anonymous'
    FRIENDS = 'friends'
    PUBLIC = 'public'


class CategoryType(str, Enum):
    """Categorie riflessioni"""
    PERSONAL_GROWTH = 'personal_growth'
    MENTAL_HEALTH = 'mental_health'
    GOALS = 'goals'
    RELATIONSHIPS = 'relationships'
    WORK = 'work'
    HEALTH = 'health'
    CREATIVITY = 'creativity'
    SPIRITUALITY = 'spirituality'


class ReactionType(str, Enum):
    """Tipi di reazioni (NO likes!)"""
    SUPPORT = 'support'        # ❤️ Sending support
    ME_TOO = 'me_too'          # 🤝 Me too
    INSIGHTFUL = 'insightful'  # 💡 Helpful insight
    INSPIRING = 'inspiring'    # 🌟 Inspiring


class ReflectionShare(db.Model):
    """Riflessioni condivise con la community"""
    __tablename__ = 'reflection_shares'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    diary_entry_id = db.Column(db.Integer, db.ForeignKey('diario.id'), nullable=True)
    
    # Content
    shared_text = db.Column(db.Text, nullable=False)
    original_text = db.Column(db.Text)  # Backup originale se user edita
    
    # Visibility
    visibility = db.Column(db.String(20), nullable=False, default='anonymous')
    
    # Categorization
    category = db.Column(db.String(30), nullable=False)
    tags = db.Column(db.String(200))  # Comma-separated
    
    # Sentiment (from AI)
    sentiment = db.Column(db.String(20))  # positive, neutral, negative
    sentiment_score = db.Column(db.Float)  # 0.0 to 1.0
    
    # Language
    language = db.Column(db.String(5), default='it')  # it, en, es, etc
    
    # Engagement
    reactions_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    views_count = db.Column(db.Integer, default=0)
    
    # Moderation
    flagged = db.Column(db.Boolean, default=False)
    flag_count = db.Column(db.Integer, default=0)
    approved = db.Column(db.Boolean, default=True)
    moderation_notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reactions = db.relationship('Reaction', backref='reflection', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='reflection', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ReflectionShare {self.id} by User {self.user_id}>'
    
    def to_dict(self, include_user=False):
        """Converte in dizionario per API"""
        data = {
            'id': self.id,
            'text': self.shared_text,
            'visibility': self.visibility,
            'category': self.category,
            'tags': self.tags.split(',') if self.tags else [],
            'sentiment': self.sentiment,
            'language': self.language,
            'reactions_count': self.reactions_count,
            'comments_count': self.comments_count,
            'views_count': self.views_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Include user info only if public/friends
        if include_user and self.visibility != 'anonymous':
            from app.models import UserProfile
            user = UserProfile.query.get(self.user_id)
            if user:
                data['user'] = {
                    'id': user.id,
                    'name': user.nome,
                    'avatar': user.avatar_url if hasattr(user, 'avatar_url') else None
                }
        else:
            data['user'] = {
                'name': 'Anonymous',
                'avatar': None
            }
        
        return data


class Reaction(db.Model):
    """Reazioni a riflessioni (NO likes, ma supporto!)"""
    __tablename__ = 'reactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    reflection_id = db.Column(db.Integer, db.ForeignKey('reflection_shares.id'), nullable=False)
    
    reaction_type = db.Column(db.String(20), nullable=False)  # support, me_too, insightful, inspiring
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint: un utente può dare solo una reazione per riflessione
    __table_args__ = (
        db.UniqueConstraint('user_id', 'reflection_id', name='unique_user_reflection'),
    )
    
    def __repr__(self):
        return f'<Reaction {self.reaction_type} by User {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.reaction_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Comment(db.Model):
    """Commenti thoughtful (min 50 caratteri)"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    reflection_id = db.Column(db.Integer, db.ForeignKey('reflection_shares.id'), nullable=False)
    
    text = db.Column(db.Text, nullable=False)
    
    # Nesting (1 level only)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    
    # Moderation
    flagged = db.Column(db.Boolean, default=False)
    approved = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    
    def __repr__(self):
        return f'<Comment {self.id} on Reflection {self.reflection_id}>'
    
    def to_dict(self, include_user=True):
        from app.models import UserProfile
        
        data = {
            'id': self.id,
            'text': self.text,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'replies_count': self.replies.count()
        }
        
        if include_user:
            user = UserProfile.query.get(self.user_id)
            data['user'] = {
                'id': user.id,
                'name': user.nome
            } if user else {'name': 'Unknown'}
        
        return data


class Circle(db.Model):
    """Circles di accountability (gruppi piccoli supporto)"""
    __tablename__ = 'circles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Creator
    creator_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    
    # Settings
    max_members = db.Column(db.Integer, default=10)
    is_private = db.Column(db.Boolean, default=True)
    invite_code = db.Column(db.String(50), unique=True, nullable=False)
    
    # Category focus
    focus_category = db.Column(db.String(30))  # Quale tipo di obiettivi condividono
    
    # Status
    active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    members = db.relationship('CircleMember', backref='circle', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Circle {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'max_members': self.max_members,
            'current_members': self.members.count(),
            'is_private': self.is_private,
            'focus_category': self.focus_category,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class CircleMember(db.Model):
    """Membri di un circle"""
    __tablename__ = 'circle_members'
    
    id = db.Column(db.Integer, primary_key=True)
    circle_id = db.Column(db.Integer, db.ForeignKey('circles.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    
    role = db.Column(db.String(20), default='member')  # admin, member
    
    # Engagement
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    contributions = db.Column(db.Integer, default=0)  # Comments, supporto dato
    
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('circle_id', 'user_id', name='unique_circle_member'),
    )
    
    def __repr__(self):
        return f'<CircleMember User {self.user_id} in Circle {self.circle_id}>'
    
    def to_dict(self):
        from app.models import UserProfile
        user = UserProfile.query.get(self.user_id)
        
        return {
            'id': self.id,
            'user': {
                'id': user.id,
                'name': user.nome
            } if user else {'name': 'Unknown'},
            'role': self.role,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'contributions': self.contributions
        }


class Challenge(db.Model):
    """Challenge mensili community"""
    __tablename__ = 'challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Duration
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    # Category
    category = db.Column(db.String(30))
    
    # Creator
    creator_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=True)
    is_official = db.Column(db.Boolean, default=False)  # Official vs community-created
    
    # Participants
    participants_count = db.Column(db.Integer, default=0)
    
    # Language
    language = db.Column(db.String(5), default='it')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    participations = db.relationship('ChallengeParticipation', backref='challenge', lazy='dynamic')
    
    def __repr__(self):
        return f'<Challenge {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'category': self.category,
            'is_official': self.is_official,
            'participants_count': self.participants_count,
            'language': self.language
        }


class ChallengeParticipation(db.Model):
    """Partecipazione a un challenge"""
    __tablename__ = 'challenge_participations'
    
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    
    # Progress
    days_completed = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    
    # Timestamps
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_check_in = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('challenge_id', 'user_id', name='unique_challenge_participation'),
    )
    
    def __repr__(self):
        return f'<ChallengeParticipation User {self.user_id} in Challenge {self.challenge_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'days_completed': self.days_completed,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'completed': self.completed,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'last_check_in': self.last_check_in.isoformat() if self.last_check_in else None
        }


class UserBan(db.Model):
    """Sistema di ban per utenti che violano regole"""
    __tablename__ = 'user_bans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    
    # Ban details
    ban_type = db.Column(db.String(20), nullable=False)  # 'temporary', 'permanent'
    reason = db.Column(db.Text, nullable=False)
    violation_type = db.Column(db.String(30))  # 'violence', 'hate', 'spam', 'minor', etc
    
    # Timing
    banned_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)  # Null se permanent
    
    # Status
    active = db.Column(db.Boolean, default=True)
    
    # Who banned
    moderator_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=True)
    
    # Appeal
    appeal_text = db.Column(db.Text, nullable=True)
    appeal_status = db.Column(db.String(20))  # 'pending', 'approved', 'rejected'
    appeal_reviewed_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<UserBan User {self.user_id} - {self.ban_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'ban_type': self.ban_type,
            'reason': self.reason,
            'violation_type': self.violation_type,
            'banned_at': self.banned_at.isoformat() if self.banned_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'active': self.active
        }


class ModerationLog(db.Model):
    """Log di tutte le azioni di moderazione (transparency!)"""
    __tablename__ = 'moderation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    moderator_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'))
    
    action_type = db.Column(db.String(20), nullable=False)  # warn, remove, ban, unban
    target_type = db.Column(db.String(20))  # reflection, comment, user
    target_id = db.Column(db.Integer)
    
    reason = db.Column(db.Text)
    notes = db.Column(db.Text)  # Internal notes
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ModerationLog {self.action_type} by {self.moderator_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'action_type': self.action_type,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'reason': self.reason,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

