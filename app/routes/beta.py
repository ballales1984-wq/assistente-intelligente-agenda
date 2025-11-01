"""Beta Program Routes"""
from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from app import db

bp = Blueprint('beta', __name__)


# Beta Signup Model
class BetaSignup(db.Model):
    """Beta program signups"""
    __tablename__ = 'beta_signups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    role = db.Column(db.String(200))
    feedback = db.Column(db.Text)
    invite_code = db.Column(db.String(50), unique=True)
    invited = db.Column(db.Boolean, default=False)
    signed_up_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'invite_code': self.invite_code,
            'invited': self.invited,
            'signed_up_at': self.signed_up_at.isoformat()
        }


@bp.route('/beta')
def beta_landing():
    """Beta program landing page"""
    return render_template('beta.html')


@bp.route('/api/beta/signup', methods=['POST'])
def beta_signup():
    """Handle beta signup"""
    data = request.json
    
    # Validation
    if not data or not data.get('email'):
        return jsonify({'error': 'Email required'}), 400
    
    # Check if already signed up
    existing = BetaSignup.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({'message': 'Already signed up!', 'signup': existing.to_dict()}), 200
    
    # Generate invite code
    import secrets
    invite_code = secrets.token_urlsafe(8)
    
    # Create signup
    signup = BetaSignup(
        name=data.get('name', 'Beta Tester'),
        email=data['email'],
        role=data.get('role'),
        feedback=data.get('feedback'),
        invite_code=invite_code
    )
    
    try:
        db.session.add(signup)
        db.session.commit()
        
        # TODO: Send welcome email
        # send_beta_welcome_email(signup)
        
        return jsonify({
            'message': 'Successfully signed up for beta!',
            'signup': signup.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/api/beta/signups', methods=['GET'])
def list_signups():
    """List all beta signups (admin only)"""
    signups = BetaSignup.query.order_by(BetaSignup.signed_up_at.desc()).all()
    return jsonify({
        'total': len(signups),
        'signups': [s.to_dict() for s in signups]
    })


@bp.route('/api/beta/stats', methods=['GET'])
def beta_stats():
    """Beta program statistics"""
    total = BetaSignup.query.count()
    invited = BetaSignup.query.filter_by(invited=True).count()
    pending = total - invited
    
    return jsonify({
        'total_signups': total,
        'invited': invited,
        'pending': pending,
        'conversion_rate': round(invited / total * 100, 1) if total > 0 else 0
    })

