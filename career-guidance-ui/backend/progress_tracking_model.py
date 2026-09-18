"""
Progress Tracking Model
Database model for tracking user progress through routine topics
"""

from datetime import datetime
from community_models import db


class RoutineProgress(db.Model):
    """
    Tracks user progress through routine topics
    Each record represents completion status of a specific topic in a week
    """
    __tablename__ = 'routine_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    skill = db.Column(db.String(200), nullable=False, index=True)
    week_number = db.Column(db.Integer, nullable=False)
    topic = db.Column(db.String(500), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes for efficient queries
    __table_args__ = (
        db.Index('idx_user_skill', 'user_id', 'skill'),
        db.Index('idx_user_week', 'user_id', 'week_number'),
        db.Index('idx_user_skill_week', 'user_id', 'skill', 'week_number'),
    )
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skill': self.skill,
            'week_number': self.week_number,
            'topic': self.topic,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<RoutineProgress user={self.user_id} skill={self.skill} week={self.week_number} completed={self.completed}>'


if __name__ == "__main__":
    # Test model creation
    print("RoutineProgress model defined successfully")
    print(f"Table name: {RoutineProgress.__tablename__}")
    print(f"Columns: {[c.name for c in RoutineProgress.__table__.columns]}")
