"""
Database Initialization Script
Creates all tables and sets up the database schema
"""

import os
import sys
from flask import Flask

# Add backend directory to path
backend_path = os.path.dirname(os.path.abspath(__file__))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from community_models import db
from user_model import User


def create_app():
    """Create Flask app with database configuration"""
    app = Flask(__name__)
    
    # Database configuration
    # Use SQLite for development (change to PostgreSQL/MySQL for production)
    db_path = os.path.join(backend_path, 'career_guidance.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Initialize database
    db.init_app(app)
    
    return app


def init_database():
    """Initialize database and create all tables"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        
        # Import all models to ensure they're registered
        from community_models import (
            Community, CommunityMember, Post, Comment, Like,
            Conversation, Message, Notification, UserProfile
        )
        
        # Create all tables
        db.create_all()
        
        print("✓ Database tables created successfully!")
        print(f"✓ Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Print created tables
        print("\nCreated tables:")
        print("  - users")
        print("  - communities")
        print("  - community_members")
        print("  - posts")
        print("  - comments")
        print("  - likes")
        print("  - conversations")
        print("  - messages")
        print("  - notifications")
        print("  - user_profiles")


def drop_all_tables():
    """Drop all tables (use with caution!)"""
    app = create_app()
    
    with app.app_context():
        print("WARNING: Dropping all database tables...")
        response = input("Are you sure? Type 'yes' to confirm: ")
        
        if response.lower() == 'yes':
            db.drop_all()
            print("✓ All tables dropped successfully!")
        else:
            print("Operation cancelled.")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Database initialization script')
    parser.add_argument('--drop', action='store_true', help='Drop all tables before creating')
    parser.add_argument('--reset', action='store_true', help='Reset database (drop and recreate)')
    
    args = parser.parse_args()
    
    if args.reset:
        drop_all_tables()
        init_database()
    elif args.drop:
        drop_all_tables()
    else:
        init_database()
