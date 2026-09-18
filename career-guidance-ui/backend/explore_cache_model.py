"""
UserAnalysisCache Model
Stores the last Analyze result per user for Explore personalization.
Written by the analyze endpoint, read by Explore.
Does NOT modify any existing models.
"""

from datetime import datetime
from community_models import db


class UserAnalysisCache(db.Model):
    """
    Caches the most recent analyze result for a user.
    Updated every time the user runs an analysis.
    """
    __tablename__ = 'user_analysis_cache'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)

    # Core analyze outputs
    readiness_score = db.Column(db.Integer, default=0)
    target_domain = db.Column(db.String(200), nullable=True)
    extracted_skills = db.Column(db.JSON, default=list)
    missing_skills = db.Column(db.JSON, default=list)

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'readiness_score': self.readiness_score,
            'target_domain': self.target_domain,
            'extracted_skills': self.extracted_skills,
            'missing_skills': self.missing_skills,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
