"""
User Model
SQLAlchemy model for user authentication and profile
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from community_models import db


class User(db.Model):
    """
    User model for authentication
    Core user table referenced by community models
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(200), nullable=True)
    profile_picture = db.Column(db.String(500), nullable=True)  # URL or path to profile picture
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_sensitive=False):
        """Convert to dictionary for API responses"""
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'domain': self.domain,
            'profile_picture': self.profile_picture,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        if include_sensitive:
            data['is_active'] = self.is_active
        return data
    
    def __repr__(self):
        return f'<User {self.email}>'
