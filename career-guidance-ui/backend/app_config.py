"""
Flask Application Configuration with Database Integration
Integrates SQLAlchemy models with Flask backend
"""

import os
import sys

# Add backend directory to path
backend_path = os.path.dirname(os.path.abspath(__file__))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from flask import Flask
from flask_cors import CORS
from community_models import db
from user_model import User


def create_app():
    """
    Create and configure Flask application with database
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
    
    # Database configuration
    db_path = os.path.join(backend_path, 'career_guidance.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{db_path}'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # CORS Configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Initialize database
    db.init_app(app)
    
    # Create tables if they don't exist
    with app.app_context():
        # Import all models to ensure they're registered
        from community_models import (
            Community, CommunityMember, Post, Comment, Like,
            Conversation, Message, Notification, UserProfile
        )
        db.create_all()
    
    return app


def get_db():
    """Get database instance"""
    return db


if __name__ == '__main__':
    app = create_app()
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("Flask app configured successfully!")
