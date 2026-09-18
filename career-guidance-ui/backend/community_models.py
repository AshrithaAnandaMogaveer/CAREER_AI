"""
Community Module Database Models
SQLAlchemy models for the Community social layer
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, Enum as SQLEnum
import enum

db = SQLAlchemy()


# Enums for role and post types
class CommunityRole(enum.Enum):
    """Community member roles"""
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    MEMBER = "MEMBER"


class PostType(enum.Enum):
    """Post types for content categorization"""
    BLOG = "BLOG"
    FEEDBACK = "FEEDBACK"
    CHAT_MESSAGE = "CHAT_MESSAGE"  # For community chat room messages


# ============================================
# COMMUNITY MODELS
# ============================================

class Community(db.Model):
    """
    Community/Group model
    Represents a community where users can join and interact
    """
    __tablename__ = 'communities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False, index=True)
    tags = db.Column(db.JSON, default=list)  # List of tags for matching
    
    # Creator information
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft delete
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Statistics (denormalized for performance)
    members_count = db.Column(db.Integer, default=0, nullable=False)
    posts_count = db.Column(db.Integer, default=0, nullable=False)
    
    # Relationships
    members = db.relationship('CommunityMember', back_populates='community', lazy='dynamic')
    posts = db.relationship('Post', back_populates='community', lazy='dynamic')
    
    # Indexes
    __table_args__ = (
        Index('idx_community_created_by_deleted', 'created_by', 'is_deleted'),
        Index('idx_community_category_deleted', 'category', 'is_deleted'),
        Index('idx_community_created_at_deleted', 'created_at', 'is_deleted'),
    )
    
    def to_dict(self, include_members=False):
        """Convert to dictionary for API responses"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'tags': self.tags,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'members_count': self.members_count,
            'posts_count': self.posts_count
        }
        if include_members:
            data['members'] = [m.to_dict() for m in self.members.filter_by(is_deleted=False).all()]
        return data


class CommunityMember(db.Model):
    """
    Community membership model
    Tracks which users belong to which communities and their roles
    """
    __tablename__ = 'community_members'

    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    role = db.Column(SQLEnum(CommunityRole), default=CommunityRole.MEMBER, nullable=False)
    
    # Timestamps
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Soft delete
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    community = db.relationship('Community', back_populates='members')
    user = db.relationship('User', backref='community_memberships')
    
    # Indexes
    __table_args__ = (
        Index('idx_member_community_user', 'community_id', 'user_id', unique=True),
        Index('idx_member_user_deleted', 'user_id', 'is_deleted'),
        Index('idx_member_community_deleted', 'community_id', 'is_deleted'),
    )
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'community_id': self.community_id,
            'user_id': self.user_id,
            'role': self.role.value,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None
        }


class Post(db.Model):
    """
    Post model for blogs and feedback
    Unified model for different types of community content
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=True)  # Optional for feedback
    content = db.Column(db.Text, nullable=False)
    post_type = db.Column(SQLEnum(PostType), nullable=False, index=True)
    category = db.Column(db.String(100), nullable=True, index=True)  # For feedback categorization
    tags = db.Column(db.JSON, default=list)  # List of tags
    video_url = db.Column(db.String(1000), nullable=True)  # Video file path for uploaded videos
    
    # Author and community
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), nullable=True, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft delete
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Statistics (denormalized for performance)
    likes_count = db.Column(db.Integer, default=0, nullable=False)
    comments_count = db.Column(db.Integer, default=0, nullable=False)
    views_count = db.Column(db.Integer, default=0, nullable=False)
    
    # Calculated fields
    read_time = db.Column(db.Integer, nullable=True)  # In minutes
    
    # Relationships
    author = db.relationship('User', backref='posts')
    community = db.relationship('Community', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', lazy='dynamic')
    likes = db.relationship('Like', back_populates='post', lazy='dynamic')
    
    # Indexes
    __table_args__ = (
        Index('idx_post_author_type_deleted', 'author_id', 'post_type', 'is_deleted'),
        Index('idx_post_community_type_deleted', 'community_id', 'post_type', 'is_deleted'),
        Index('idx_post_type_created_deleted', 'post_type', 'created_at', 'is_deleted'),
        Index('idx_post_category_deleted', 'category', 'is_deleted'),
    )
    
    def to_dict(self, include_author=True, include_comments=False):
        """Convert to dictionary for API responses"""
        data = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'post_type': self.post_type.value,
            'category': self.category,
            'tags': self.tags,
            'video_url': self.video_url,
            'author_id': self.author_id,
            'community_id': self.community_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'views_count': self.views_count,
            'read_time': self.read_time
        }
        if include_author and self.author:
            data['author_name'] = self.author.name
            data['author_email'] = self.author.email
        if include_comments:
            data['comments'] = [c.to_dict() for c in self.comments.filter_by(is_deleted=False).all()]
        return data


class Comment(db.Model):
    """
    Comment model for posts
    Supports nested comments (replies)
    """
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    
    # Post and author
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Parent comment for nested replies
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft delete
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Statistics
    likes_count = db.Column(db.Integer, default=0, nullable=False)
    
    # Relationships
    post = db.relationship('Post', back_populates='comments')
    author = db.relationship('User', backref='comments')
    parent = db.relationship('Comment', remote_side=[id], backref='replies')
    likes = db.relationship('Like', back_populates='comment', lazy='dynamic')
    
    # Indexes
    __table_args__ = (
        Index('idx_comment_post_deleted', 'post_id', 'is_deleted'),
        Index('idx_comment_author_deleted', 'author_id', 'is_deleted'),
        Index('idx_comment_parent_deleted', 'parent_id', 'is_deleted'),
        Index('idx_comment_created_deleted', 'created_at', 'is_deleted'),
    )
    
    def to_dict(self, include_author=True, include_replies=False):
        """Convert to dictionary for API responses"""
        data = {
            'id': self.id,
            'content': self.content,
            'post_id': self.post_id,
            'author_id': self.author_id,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'likes_count': self.likes_count
        }
        if include_author and self.author:
            data['author_name'] = self.author.name
        if include_replies:
            data['replies'] = [r.to_dict() for r in self.replies if not r.is_deleted]
        return data


class Like(db.Model):
    """
    Like model for posts and comments
    Tracks user likes/upvotes
    """
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Can like either a post or a comment
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True, index=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True, index=True)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Soft delete
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='likes')
    post = db.relationship('Post', back_populates='likes')
    comment = db.relationship('Comment', back_populates='likes')
    
    # Indexes
    __table_args__ = (
        Index('idx_like_user_post', 'user_id', 'post_id', unique=True),
        Index('idx_like_user_comment', 'user_id', 'comment_id', unique=True),
        Index('idx_like_post_deleted', 'post_id', 'is_deleted'),
        Index('idx_like_comment_deleted', 'comment_id', 'is_deleted'),
    )
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'comment_id': self.comment_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Conversation(db.Model):
    """
    Conversation model for private messaging
    Represents a chat between two users
    """
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    
    # Participants (always 2 users for private chat)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Last message info (denormalized for performance)
    last_message_at = db.Column(db.DateTime, nullable=True, index=True)
    last_message_preview = db.Column(db.String(200), nullable=True)
    
    # Soft delete
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user1 = db.relationship('User', foreign_keys=[user1_id], backref='conversations_as_user1')
    user2 = db.relationship('User', foreign_keys=[user2_id], backref='conversations_as_user2')
    messages = db.relationship('Message', back_populates='conversation', lazy='dynamic')
    
    # Indexes
    __table_args__ = (
        Index('idx_conversation_users', 'user1_id', 'user2_id', unique=True),
        Index('idx_conversation_user1_deleted', 'user1_id', 'is_deleted'),
        Index('idx_conversation_user2_deleted', 'user2_id', 'is_deleted'),
        Index('idx_conversation_last_message', 'last_message_at', 'is_deleted'),
    )
    
    def to_dict(self, current_user_id=None):
        """Convert to dictionary for API responses"""
        # Determine the other participant
        other_user_id = self.user2_id if current_user_id == self.user1_id else self.user1_id
        other_user = self.user2 if current_user_id == self.user1_id else self.user1
        
        return {
            'id': self.id,
            'other_user_id': other_user_id,
            'other_user_name': other_user.name if other_user else None,
            'last_message_at': self.last_message_at.isoformat() if self.last_message_at else None,
            'last_message_preview': self.last_message_preview,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Message(db.Model):
    """
    Message model for private conversations
    Individual messages within a conversation
    """
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False, index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    
    # Read status
    is_read = db.Column(db.Boolean, default=False, nullable=False, index=True)
    read_at = db.Column(db.DateTime, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Soft delete
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    conversation = db.relationship('Conversation', back_populates='messages')
    sender = db.relationship('User', backref='sent_messages')
    
    # Indexes
    __table_args__ = (
        Index('idx_message_conversation_created', 'conversation_id', 'created_at'),
        Index('idx_message_sender_deleted', 'sender_id', 'is_deleted'),
        Index('idx_message_conversation_deleted', 'conversation_id', 'is_deleted'),
        Index('idx_message_read_status', 'conversation_id', 'is_read'),
    )
    
    def to_dict(self, include_sender=True):
        """Convert to dictionary for API responses"""
        data = {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'sender_id': self.sender_id,
            'content': self.content,
            'is_read': self.is_read,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_sender and self.sender:
            data['sender_name'] = self.sender.name
        return data


class Notification(db.Model):
    """
    Notification model for user alerts
    Tracks various types of notifications (likes, comments, messages, etc.)
    """
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Notification details
    type = db.Column(db.String(50), nullable=False, index=True)  # LIKE, COMMENT, MESSAGE, MENTION, etc.
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    # Related entity (polymorphic reference)
    entity_type = db.Column(db.String(50), nullable=True)  # POST, COMMENT, MESSAGE, etc.
    entity_id = db.Column(db.Integer, nullable=True, index=True)
    
    # Actor (who triggered the notification)
    actor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    
    # Read status
    is_read = db.Column(db.Boolean, default=False, nullable=False, index=True)
    read_at = db.Column(db.DateTime, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Soft delete
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='notifications')
    actor = db.relationship('User', foreign_keys=[actor_id], backref='triggered_notifications')
    
    # Indexes
    __table_args__ = (
        Index('idx_notification_user_read', 'user_id', 'is_read', 'is_deleted'),
        Index('idx_notification_user_created', 'user_id', 'created_at', 'is_deleted'),
        Index('idx_notification_type_deleted', 'type', 'is_deleted'),
        Index('idx_notification_entity', 'entity_type', 'entity_id'),
    )
    
    def to_dict(self, include_actor=True):
        """Convert to dictionary for API responses"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'actor_id': self.actor_id,  # always include raw actor_id
            'is_read': self.is_read,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_actor and self.actor:
            data['actor_name'] = self.actor.name
        return data


# ============================================
# USER PROFILE EXTENSION (Optional)
# ============================================

class UserProfile(db.Model):
    """
    Extended user profile for community features
    Stores additional information for matching and recommendations
    """
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    
    # Skills and interests for matching
    skills = db.Column(db.JSON, default=list)  # List of skills
    interests = db.Column(db.JSON, default=list)  # List of interests
    domains = db.Column(db.JSON, default=list)  # List of domains
    
    # Profile information
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    website = db.Column(db.String(500), nullable=True)
    
    # Experience
    experience_years = db.Column(db.Integer, default=0)
    projects_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='profile')
    
    # Indexes
    __table_args__ = (
        Index('idx_profile_user', 'user_id'),
    )
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skills': self.skills,
            'interests': self.interests,
            'domains': self.domains,
            'bio': self.bio,
            'location': self.location,
            'website': self.website,
            'experience_years': self.experience_years,
            'projects_count': self.projects_count
        }


# ============================================
# HELPER FUNCTIONS
# ============================================

def init_db(app):
    """Initialize database with app context"""
    db.init_app(app)
    with app.app_context():
        db.create_all()


def calculate_similarity(user1_profile, user2_profile):
    """
    Calculate similarity percentage between two user profiles
    Based on common skills, interests, and domains
    """
    if not user1_profile or not user2_profile:
        return 0
    
    # Get sets for comparison
    skills1 = set(user1_profile.skills or [])
    skills2 = set(user2_profile.skills or [])
    interests1 = set(user1_profile.interests or [])
    interests2 = set(user2_profile.interests or [])
    domains1 = set(user1_profile.domains or [])
    domains2 = set(user2_profile.domains or [])
    
    # Calculate overlaps
    common_skills = len(skills1 & skills2)
    common_interests = len(interests1 & interests2)
    common_domains = len(domains1 & domains2)
    
    total_skills = len(skills1 | skills2)
    total_interests = len(interests1 | interests2)
    total_domains = len(domains1 | domains2)
    
    # Weighted similarity (skills: 50%, interests: 30%, domains: 20%)
    skill_sim = (common_skills / total_skills * 100) if total_skills > 0 else 0
    interest_sim = (common_interests / total_interests * 100) if total_interests > 0 else 0
    domain_sim = (common_domains / total_domains * 100) if total_domains > 0 else 0
    
    similarity = (skill_sim * 0.5) + (interest_sim * 0.3) + (domain_sim * 0.2)
    
    return round(similarity, 2)
