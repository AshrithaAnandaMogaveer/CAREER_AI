"""
Community Service Layer
Business logic for Community module operations
"""

from datetime import datetime
from sqlalchemy import or_, and_, desc
from community_models import (
    db, Community, CommunityMember, Post, Comment, Like,
    Conversation, Message, Notification, UserProfile,
    CommunityRole, PostType, calculate_similarity
)
from user_model import User
from recommendation_engine import RecommendationEngine
from feed_ranking_engine import FeedRankingEngine
from profile_matching_engine import ProfileMatchingEngine


class CommunityService:
    """Service class for Community operations"""
    
    # ============================================
    # COMMUNITY GROUPS
    # ============================================
    
    @staticmethod
    def get_communities(user_id, limit=50):
        """Get list of communities with membership status"""
        communities = Community.query.filter_by(is_deleted=False).limit(limit).all()
        
        # Get user's memberships
        user_memberships = set(
            m.community_id for m in 
            CommunityMember.query.filter_by(user_id=user_id, is_deleted=False).all()
        )
        
        result = []
        for community in communities:
            data = community.to_dict()
            data['is_member'] = community.id in user_memberships
            result.append(data)
        
        return result
    
    @staticmethod
    def create_community(user_id, name, description, category, tags=None):
        """
        Create a new community
        - Creator becomes ADMIN
        - Automatically joins as first member
        - Returns community data
        """
        # Validate inputs
        if not name or not description:
            return {'success': False, 'message': 'Name and description are required'}
        
        # Check for duplicate name
        existing = Community.query.filter_by(name=name, is_deleted=False).first()
        if existing:
            return {'success': False, 'message': 'Community with this name already exists'}
        
        try:
            # Create community
            community = Community(
                name=name,
                description=description,
                category=category or 'General',
                tags=tags or [],
                created_by=user_id,
                members_count=1
            )
            db.session.add(community)
            db.session.flush()
            
            # Add creator as ADMIN member
            member = CommunityMember(
                community_id=community.id,
                user_id=user_id,
                role=CommunityRole.ADMIN
            )
            db.session.add(member)
            db.session.commit()
            
            return {
                'success': True,
                'community': community.to_dict(),
                'message': 'Community created successfully'
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    @staticmethod
    def join_community(user_id, community_id):
        """
        Join a community
        - Prevents duplicate membership
        - Creates notification for community admins
        - Updates member count
        """
        # Check if community exists
        community = Community.query.filter_by(id=community_id, is_deleted=False).first()
        if not community:
            return {'success': False, 'message': 'Community not found'}
        
        # Check if already a member
        existing = CommunityMember.query.filter_by(
            community_id=community_id,
            user_id=user_id,
            is_deleted=False
        ).first()
        
        if existing:
            return {'success': False, 'message': 'Already a member of this community'}
        
        try:
            # Add membership
            member = CommunityMember(
                community_id=community_id,
                user_id=user_id,
                role=CommunityRole.MEMBER
            )
            db.session.add(member)
            
            # Update community member count
            community.members_count += 1
            
            # Get user info for notification
            user = User.query.get(user_id)
            
            # Create notification for community admins
            admins = CommunityMember.query.filter_by(
                community_id=community_id,
                role=CommunityRole.ADMIN,
                is_deleted=False
            ).all()
            
            for admin in admins:
                if admin.user_id != user_id:  # Don't notify self
                    notification = Notification(
                        user_id=admin.user_id,
                        type='COMMUNITY_JOIN',
                        title='New Member Joined',
                        message=f'{user.name if user else "Someone"} joined {community.name}',
                        entity_type='COMMUNITY',
                        entity_id=community_id,
                        actor_id=user_id
                    )
                    db.session.add(notification)
            
            db.session.commit()
            
            return {
                'success': True,
                'message': f'Successfully joined {community.name}',
                'community': community.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    # ============================================
    # FEEDBACK
    # ============================================
    
    @staticmethod
    def get_feedback(limit=50):
        """Get all feedback posts"""
        posts = Post.query.filter_by(
            post_type=PostType.FEEDBACK,
            is_deleted=False
        ).order_by(desc(Post.created_at)).limit(limit).all()
        
        return [p.to_dict(include_author=True) for p in posts]
    
    @staticmethod
    def submit_feedback(user_id, content, category=None):
        """Submit new feedback"""
        post = Post(
            content=content,
            post_type=PostType.FEEDBACK,
            category=category or 'General',
            author_id=user_id
        )
        db.session.add(post)
        db.session.commit()
        
        return post.to_dict(include_author=True)
    
    # ============================================
    # BLOGS
    # ============================================
    
    @staticmethod
    def get_blogs(limit=50):
        """Get all blog posts"""
        posts = Post.query.filter_by(
            post_type=PostType.BLOG,
            is_deleted=False
        ).order_by(desc(Post.created_at)).limit(limit).all()
        
        return [p.to_dict(include_author=True) for p in posts]
    
    @staticmethod
    def create_blog(user_id, title, content, tags=None, community_id=None, video_url=None):
        """Create a new blog post"""
        # Calculate read time (200 words per minute)
        word_count = len(content.split())
        read_time = max(1, word_count // 200)
        
        post = Post(
            title=title,
            content=content,
            post_type=PostType.BLOG,
            tags=tags or [],
            video_url=video_url,
            author_id=user_id,
            community_id=community_id,
            read_time=read_time
        )
        db.session.add(post)
        
        # Update community post count if applicable
        if community_id:
            community = Community.query.get(community_id)
            if community:
                community.posts_count += 1
        
        db.session.commit()
        return post.to_dict(include_author=True)
    
    # ============================================
    # UNIFIED POST MANAGEMENT
    # ============================================
    
    @staticmethod
    def create_post(user_id, post_type, content, title=None, category=None, tags=None, community_id=None):
        """
        Unified method to create any type of post (blog or feedback)
        - Saves user_id with content
        - Calculates read time for blogs
        - Updates community post count
        - Returns post data for feed ranking
        """
        try:
            # Validate post type
            if post_type.upper() not in ['BLOG', 'FEEDBACK']:
                return {'success': False, 'message': 'Invalid post type. Must be BLOG or FEEDBACK'}
            
            # Validate required fields
            if not content:
                return {'success': False, 'message': 'Content is required'}
            
            if post_type.upper() == 'BLOG' and not title:
                return {'success': False, 'message': 'Title is required for blog posts'}
            
            # Calculate read time for blogs
            read_time = None
            if post_type.upper() == 'BLOG':
                word_count = len(content.split())
                read_time = max(1, word_count // 200)
            
            # Create post
            post = Post(
                title=title,
                content=content,
                post_type=PostType.BLOG if post_type.upper() == 'BLOG' else PostType.FEEDBACK,
                category=category,
                tags=tags or [],
                author_id=user_id,
                community_id=community_id,
                read_time=read_time
            )
            db.session.add(post)
            db.session.flush()
            
            # Update community post count if applicable
            if community_id:
                community = Community.query.get(community_id)
                if community:
                    community.posts_count += 1
            
            # Create notifications for relevant users
            CommunityService._create_post_notifications(post, user_id)
            
            db.session.commit()
            
            return {
                'success': True,
                'post': post.to_dict(include_author=True),
                'message': f'{post_type.capitalize()} posted successfully'
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    @staticmethod
    def get_posts(post_type=None, limit=50, user_id=None):
        """
        Get posts with optional filtering
        - Can filter by post_type (BLOG/FEEDBACK)
        - Can filter by user_id
        - Returns posts ordered by creation date
        """
        query = Post.query.filter_by(is_deleted=False)
        
        # Filter by post type
        if post_type:
            if post_type.upper() == 'BLOG':
                query = query.filter_by(post_type=PostType.BLOG)
            elif post_type.upper() == 'FEEDBACK':
                query = query.filter_by(post_type=PostType.FEEDBACK)
        
        # Filter by user
        if user_id:
            query = query.filter_by(author_id=user_id)
        
        # Order and limit
        posts = query.order_by(desc(Post.created_at)).limit(limit).all()
        
        return [p.to_dict(include_author=True) for p in posts]
    
    @staticmethod
    def _create_post_notifications(post, author_id):
        """
        Create notifications for relevant users when a post is created
        - Notify community members if posted in a community
        - Notify users with matching interests (relevance-based)
        """
        notifications_created = 0
        
        # If posted in a community, notify community members
        if post.community_id:
            community = Community.query.get(post.community_id)
            if community:
                # Get community members (excluding author)
                members = CommunityMember.query.filter(
                    CommunityMember.community_id == post.community_id,
                    CommunityMember.user_id != author_id,
                    CommunityMember.is_deleted == False
                ).limit(50).all()  # Limit to avoid spam
                
                author = User.query.get(author_id)
                post_type_label = 'blog' if post.post_type == PostType.BLOG else 'feedback'
                
                for member in members:
                    notification = Notification(
                        user_id=member.user_id,
                        type='NEW_POST',
                        title=f'New {post_type_label} in {community.name}',
                        message=f'{author.name if author else "Someone"} posted: {post.title or post.content[:50]}...',
                        entity_type='POST',
                        entity_id=post.id,
                        actor_id=author_id
                    )
                    db.session.add(notification)
                    notifications_created += 1
        
        # TODO: Add relevance-based notifications for users with matching interests
        # This would use the recommendation engine to find users interested in post tags
        
        return notifications_created
    
    # ============================================
    # REACH OUT (USER MATCHING) - PHASE 7
    # ============================================
    
    @staticmethod
    def get_related_profiles(user_id, limit=50, min_score=0, include_breakdown=False):
        """
        Get related user profiles based on weighted similarity scoring
        
        Phase 7 Weighted Formula:
        score = 0.4 × domainMatch + 0.3 × skillOverlap + 0.2 × experienceMatch + 0.1 × interestMatch
        
        Args:
            user_id: Current user's ID
            limit: Maximum number of profiles to return (default 10)
            min_score: Minimum similarity score threshold 0-100 (default 0)
            include_breakdown: Include detailed score breakdown (default False)
        
        Returns:
            list: Ranked list of matching profiles with similarity scores
        """
        # Use the new weighted profile matching engine
        matches = ProfileMatchingEngine.match_profiles(
            user_id=user_id,
            limit=limit,
            min_score=min_score
        )
        
        # Add match explanation for each result
        for match in matches:
            match['match_reason'] = ProfileMatchingEngine.get_match_explanation(
                match['score_breakdown']
            )
            
            # Remove breakdown if not requested (reduce payload size)
            if not include_breakdown:
                del match['score_breakdown']
        
        return matches
    
    # ============================================
    # MESSAGING
    # ============================================
    # MESSAGING - PHASE 8
    # ============================================
    
    @staticmethod
    def get_or_create_conversation(user1_id, user2_id):
        """
        Get existing conversation or create new one
        Ensures consistent ordering (lower ID first)
        """
        # Ensure consistent ordering (lower ID first)
        if user1_id > user2_id:
            user1_id, user2_id = user2_id, user1_id
        
        conversation = Conversation.query.filter_by(
            user1_id=user1_id,
            user2_id=user2_id,
            is_deleted=False
        ).first()
        
        if not conversation:
            conversation = Conversation(
                user1_id=user1_id,
                user2_id=user2_id
            )
            db.session.add(conversation)
            db.session.commit()
        
        return conversation
    
    @staticmethod
    def get_messages(user_id, other_user_id, limit=100):
        """
        Get message history between two users
        Marks messages as read for the current user
        """
        conversation = CommunityService.get_or_create_conversation(user_id, other_user_id)
        
        messages = Message.query.filter_by(
            conversation_id=conversation.id,
            is_deleted=False
        ).order_by(Message.created_at).limit(limit).all()
        
        # Mark unread messages as read for current user
        unread_messages = [msg for msg in messages if not msg.is_read and msg.sender_id != user_id]
        for msg in unread_messages:
            msg.is_read = True
            msg.read_at = datetime.utcnow()
        
        if unread_messages:
            db.session.commit()
        
        result = []
        for msg in messages:
            data = msg.to_dict(include_sender=True)
            data['is_own'] = msg.sender_id == user_id
            result.append(data)
        
        return result
    
    @staticmethod
    def get_conversations(user_id, limit=50):
        """
        Get all conversations for a user
        Returns list of conversations with last message preview
        """
        # Get conversations where user is participant
        conversations = Conversation.query.filter(
            or_(
                Conversation.user1_id == user_id,
                Conversation.user2_id == user_id
            ),
            Conversation.is_deleted == False
        ).order_by(Conversation.last_message_at.desc()).limit(limit).all()
        
        result = []
        for conv in conversations:
            # Get other user
            other_user_id = conv.user2_id if conv.user1_id == user_id else conv.user1_id
            other_user = User.query.get(other_user_id)
            
            if not other_user or other_user.is_deleted:
                continue
            
            # Count unread messages
            unread_count = Message.query.filter_by(
                conversation_id=conv.id,
                is_read=False,
                is_deleted=False
            ).filter(Message.sender_id != user_id).count()
            
            result.append({
                'conversation_id': conv.id,
                'other_user': {
                    'id': other_user.id,
                    'name': other_user.name,
                    'email': other_user.email,
                    'domain': other_user.domain
                },
                'last_message_at': conv.last_message_at.isoformat() if conv.last_message_at else None,
                'last_message_preview': conv.last_message_preview,
                'unread_count': unread_count,
                'created_at': conv.created_at.isoformat() if conv.created_at else None
            })
        
        return result
    
    @staticmethod
    def send_message(sender_id, recipient_id, content):
        """
        Send a message to another user
        
        Phase 8 Logic:
        - Create conversation if not exists
        - Store message
        - Mark unread for receiver
        - Trigger notification event
        """
        # Validate content
        if not content or not content.strip():
            return {'success': False, 'message': 'Message content cannot be empty'}
        
        # Check if recipient exists
        recipient = User.query.get(recipient_id)
        if not recipient or recipient.is_deleted or not recipient.is_active:
            return {'success': False, 'message': 'Recipient not found'}
        
        # Get sender info
        sender = User.query.get(sender_id)
        
        try:
            # Create conversation if not exists
            conversation = CommunityService.get_or_create_conversation(sender_id, recipient_id)
            
            # Store message (unread by default)
            message = Message(
                conversation_id=conversation.id,
                sender_id=sender_id,
                content=content.strip(),
                is_read=False  # Mark unread for receiver
            )
            db.session.add(message)
            
            # Update conversation last message
            conversation.last_message_at = datetime.utcnow()
            conversation.last_message_preview = content[:200]
            
            # Trigger notification event
            notification = Notification(
                user_id=recipient_id,
                type='NEW_MESSAGE',
                title='New Message',
                message=f'{sender.name if sender else "Someone"} sent you a message',
                entity_type='MESSAGE',
                entity_id=message.id,
                actor_id=sender_id
            )
            db.session.add(notification)
            
            db.session.commit()
            
            return {
                'success': True,
                'message': message.to_dict(include_sender=True),
                'conversation_id': conversation.id
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    @staticmethod
    def mark_conversation_read(user_id, conversation_id):
        """
        Mark all messages in a conversation as read for the user
        """
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return {'success': False, 'message': 'Conversation not found'}
        
        # Verify user is participant
        if conversation.user1_id != user_id and conversation.user2_id != user_id:
            return {'success': False, 'message': 'Unauthorized'}
        
        # Mark all unread messages as read
        unread_messages = Message.query.filter_by(
            conversation_id=conversation_id,
            is_read=False,
            is_deleted=False
        ).filter(Message.sender_id != user_id).all()
        
        count = 0
        for msg in unread_messages:
            msg.is_read = True
            msg.read_at = datetime.utcnow()
            count += 1
        
        if count > 0:
            db.session.commit()
        
        return {
            'success': True,
            'marked_read': count
        }
    
    # ============================================
    # LIKES
    # ============================================
    
    # ============================================
    # LIKES - PHASE 9 ENHANCED
    # ============================================
    
    @staticmethod
    def toggle_like(user_id, post_id=None, comment_id=None):
        """
        Toggle like on post or comment
        Phase 9: Triggers notification when someone likes post
        """
        if post_id:
            existing = Like.query.filter_by(
                user_id=user_id,
                post_id=post_id,
                is_deleted=False
            ).first()
            
            if existing:
                # Unlike
                existing.is_deleted = True
                existing.deleted_at = datetime.utcnow()
                post = Post.query.get(post_id)
                if post:
                    post.likes_count = max(0, post.likes_count - 1)
                action = 'unliked'
            else:
                # Like — reuse soft-deleted row if exists, else create new
                existing_deleted = Like.query.filter_by(
                    user_id=user_id,
                    post_id=post_id
                ).first()
                if existing_deleted:
                    existing_deleted.is_deleted = False
                    existing_deleted.deleted_at = None
                else:
                    like = Like(user_id=user_id, post_id=post_id)
                    db.session.add(like)
                post = Post.query.get(post_id)
                if post:
                    post.likes_count += 1
                    
                    # Phase 9: Create notification for post author (if not self-like)
                    author_id = post.author_id
                    if author_id and author_id != user_id:
                        # Get liker name in same session
                        liker_name = db.session.query(User.name).filter_by(id=user_id).scalar() or "Someone"
                        notification = Notification(
                            user_id=author_id,
                            type='POST_LIKE',
                            title='New Like',
                            message=f'{liker_name} liked your post',
                            entity_type='POST',
                            entity_id=post_id,
                            actor_id=user_id
                        )
                        db.session.add(notification)
                
                action = 'liked'
        
        elif comment_id:
            existing = Like.query.filter_by(
                user_id=user_id,
                comment_id=comment_id,
                is_deleted=False
            ).first()
            
            if existing:
                # Unlike
                existing.is_deleted = True
                existing.deleted_at = datetime.utcnow()
                comment = Comment.query.get(comment_id)
                if comment:
                    comment.likes_count = max(0, comment.likes_count - 1)
                action = 'unliked'
            else:
                # Like — reuse soft-deleted row if exists, else create new
                existing_deleted = Like.query.filter_by(
                    user_id=user_id,
                    comment_id=comment_id
                ).first()
                if existing_deleted:
                    existing_deleted.is_deleted = False
                    existing_deleted.deleted_at = None
                else:
                    like = Like(user_id=user_id, comment_id=comment_id)
                    db.session.add(like)
                comment = Comment.query.get(comment_id)
                if comment:
                    comment.likes_count += 1
                    
                    # Phase 9: Create notification for comment author (if not self-like)
                    author_id = comment.author_id
                    if author_id and author_id != user_id:
                        # Get liker name in same session
                        liker_name = db.session.query(User.name).filter_by(id=user_id).scalar() or "Someone"
                        notification = Notification(
                            user_id=author_id,
                            type='COMMENT_LIKE',
                            title='New Like',
                            message=f'{liker_name} liked your comment',
                            entity_type='COMMENT',
                            entity_id=comment_id,
                            actor_id=user_id
                        )
                        db.session.add(notification)
                
                action = 'liked'
        else:
            return {'success': False, 'message': 'Must provide post_id or comment_id'}
        
        db.session.commit()
        
        # Return updated likes count
        likes_count = None
        if post_id:
            post = Post.query.get(post_id)
            if post:
                likes_count = post.likes_count
        elif comment_id:
            comment = Comment.query.get(comment_id)
            if comment:
                likes_count = comment.likes_count
        
        return {'success': True, 'action': action, 'likes_count': likes_count}
    
    @staticmethod
    def add_comment(user_id, post_id, content, parent_comment_id=None):
        """
        Add a comment to a post
        Phase 9: Triggers notification when someone comments
        """
        # Validate inputs
        if not content or not content.strip():
            return {'success': False, 'message': 'Comment content cannot be empty'}
        
        # Check if post exists
        post = Post.query.filter_by(id=post_id, is_deleted=False).first()
        if not post:
            return {'success': False, 'message': 'Post not found'}
        
        try:
            # Create comment
            comment = Comment(
                post_id=post_id,
                author_id=user_id,
                content=content.strip(),
                parent_comment_id=parent_comment_id
            )
            db.session.add(comment)
            
            # Update post comment count
            post.comments_count += 1
            
            # Phase 9: Create notification for post author (if not self-comment)
            author_id = post.author_id
            if author_id and author_id != user_id:
                # Get commenter name in same session
                commenter_name = db.session.query(User.name).filter_by(id=user_id).scalar() or "Someone"
                notification = Notification(
                    user_id=author_id,
                    type='NEW_COMMENT',
                    title='New Comment',
                    message=f'{commenter_name} commented on your post',
                    entity_type='COMMENT',
                    entity_id=comment.id,
                    actor_id=user_id
                )
                db.session.add(notification)
            
            # If replying to a comment, notify the parent comment author
            if parent_comment_id:
                parent_comment = Comment.query.get(parent_comment_id)
                if parent_comment:
                    parent_author_id = parent_comment.author_id
                    if parent_author_id and parent_author_id != user_id:
                        # Get commenter name in same session
                        commenter_name = db.session.query(User.name).filter_by(id=user_id).scalar() or "Someone"
                        notification = Notification(
                            user_id=parent_author_id,
                            type='COMMENT_REPLY',
                            title='New Reply',
                            message=f'{commenter_name} replied to your comment',
                            entity_type='COMMENT',
                            entity_id=comment.id,
                            actor_id=user_id
                        )
                        db.session.add(notification)
            
            db.session.commit()
            
            return {
                'success': True,
                'comment': comment.to_dict(include_author=True)
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
    
    # ============================================
    # RECOMMENDATIONS
    # ============================================
    
    @staticmethod
    def get_recommended_communities(user_id, limit=5):
        """
        Get recommended communities based on user interests
        Uses vector-based cosine similarity matching
        """
        return RecommendationEngine.recommend_communities(
            user_id=user_id,
            limit=limit,
            exclude_joined=True
        )
    
    @staticmethod
    def get_trending_communities(limit=5):
        """
        Get trending communities based on activity
        Fallback when user has no profile
        """
        return RecommendationEngine.get_trending_communities(limit=limit)
    
    # ============================================
    # FEED RANKING
    # ============================================
    
    @staticmethod
    def get_ranked_feed(user_id, post_type=None, limit=50, include_scores=False):
        """
        Get personalized ranked feed for user
        Uses recency, engagement, and relevance scoring
        """
        return FeedRankingEngine.rank_feed(
            user_id=user_id,
            post_type=post_type,
            limit=limit,
            include_scores=include_scores
        )
    
    @staticmethod
    def get_trending_posts(post_type=None, time_window_hours=24, limit=10):
        """
        Get trending posts based on recent engagement
        """
        return FeedRankingEngine.get_trending_posts(
            post_type=post_type,
            time_window_hours=time_window_hours,
            limit=limit
        )
    
    @staticmethod
    def get_feed_stats(user_id):
        """
        Get feed statistics for user
        """
        return FeedRankingEngine.get_feed_stats(user_id)


    # ============================================
    # COMMUNITY CHAT ROOM
    # ============================================
    
    @staticmethod
    def get_community_messages(community_id, limit=100):
        """
        Get messages from a community chat room
        Returns messages with user information
        """
        try:
            import json
            from community_models import db
            
            # Query messages (we'll use Post model with CHAT_MESSAGE type)
            messages = Post.query.filter_by(
                community_id=community_id,
                post_type=PostType.CHAT_MESSAGE,
                is_deleted=False
            ).order_by(Post.created_at.asc()).limit(limit).all()
            
            result = []
            for msg in messages:
                user = User.query.get(msg.author_id)
                
                # Parse content to extract text and image URL
                content_text = msg.content
                image_url = None
                
                # Check if content contains image marker
                if '[IMAGE:' in msg.content:
                    parts = msg.content.split('[IMAGE:')
                    content_text = parts[0].strip()
                    if len(parts) > 1:
                        image_url = parts[1].split(']')[0]
                
                result.append({
                    'id': msg.id,
                    'user_id': msg.author_id,
                    'user_name': user.name if user else 'Unknown',
                    'content': content_text,
                    'image_url': image_url,
                    'created_at': msg.created_at.isoformat() if msg.created_at else None
                })
            
            return result
            
        except Exception as e:
            print(f"Error getting community messages: {e}")
            return []
    
    @staticmethod
    def send_community_message(community_id, user_id, content, image_url=None):
        """
        Send a message to a community chat room
        Creates a post with type CHAT_MESSAGE
        """
        try:
            # Validate community exists
            community = Community.query.get(community_id)
            if not community or community.is_deleted:
                return {'success': False, 'message': 'Community not found'}
            
            # Prepare content with image URL if provided
            message_content = content if content else ''
            if image_url:
                message_content = f"{message_content}\n[IMAGE:{image_url}]" if message_content else f"[IMAGE:{image_url}]"
            
            # Ensure we have some content
            if not message_content.strip():
                return {'success': False, 'message': 'Message cannot be empty'}
            
            # Create message as a Post with CHAT_MESSAGE type
            message = Post(
                community_id=community_id,
                author_id=user_id,
                content=message_content,
                post_type=PostType.CHAT_MESSAGE,
                title=''  # Chat messages don't need titles
            )
            
            db.session.add(message)
            
            # Update community's last activity
            community.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Create notifications for all other members who haven't read this message
            try:
                from community_models import Notification
                sender = User.query.get(user_id)
                sender_name = sender.name if sender else 'Someone'
                
                other_members = CommunityMember.query.filter(
                    CommunityMember.community_id == community_id,
                    CommunityMember.user_id != user_id,
                    CommunityMember.is_deleted == False
                ).all()
                
                preview = (content[:60] + '...') if content and len(content) > 60 else (content or '📷 Image')
                
                for member in other_members:
                    # Skip if there's already an unread notification for this community from this sender
                    existing = Notification.query.filter_by(
                        user_id=member.user_id,
                        type='NEW_COMMUNITY_MESSAGE',
                        entity_id=community_id,
                        actor_id=user_id,
                        is_read=False,
                        is_deleted=False
                    ).first()
                    if existing:
                        # Update the preview to the latest message
                        existing.message = f'{sender_name}: {preview}'
                        existing.created_at = datetime.utcnow()
                    else:
                        notif = Notification(
                            user_id=member.user_id,
                            type='NEW_COMMUNITY_MESSAGE',
                            title=f'New message in {community.name}',
                            message=f'{sender_name}: {preview}',
                            entity_type='COMMUNITY',
                            entity_id=community_id,
                            actor_id=user_id,
                            is_read=False
                        )
                        db.session.add(notif)
                
                db.session.commit()
            except Exception as notif_err:
                print(f"Warning: Could not create community message notifications: {notif_err}")
            
            return {
                'success': True,
                'message': 'Message sent successfully',
                'message_id': message.id
            }
            
        except Exception as e:
            db.session.rollback()
            print(f"Error sending community message: {e}")
            return {'success': False, 'message': str(e)}
    
    @staticmethod
    def get_community_members(community_id):
        """
        Get all members of a community with their roles
        """
        try:
            members = CommunityMember.query.filter_by(
                community_id=community_id,
                is_deleted=False
            ).all()
            
            result = []
            for member in members:
                user = User.query.get(member.user_id)
                if user:
                    result.append({
                        'user_id': member.user_id,
                        'user_name': user.name,
                        'role': member.role.value if member.role else 'MEMBER',
                        'joined_at': member.created_at.isoformat() if member.created_at else None
                    })
            
            return result
            
        except Exception as e:
            print(f"Error getting community members: {e}")
            return []

    # ============================================
    # DELETE OPERATIONS
    # ============================================
    
    @staticmethod
    def delete_community(community_id, user_id):
        """
        Delete a community (soft delete)
        Any user can delete any community
        """
        community = Community.query.get(community_id)
        if not community:
            raise ValueError('Community not found')
        
        if community.is_deleted:
            raise ValueError('Community already deleted')
        
        # Soft delete - no authorization check, any user can delete
        community.is_deleted = True
        community.deleted_at = datetime.utcnow()
        db.session.commit()
        
        return {'success': True, 'message': 'Community deleted successfully'}
    
    @staticmethod
    def delete_blog(post_id, user_id):
        """
        Delete a blog post (soft delete)
        Any user can delete any blog
        """
        post = Post.query.get(post_id)
        if not post:
            raise ValueError('Blog not found')
        
        if post.is_deleted:
            raise ValueError('Blog already deleted')
        
        if post.post_type != PostType.BLOG:
            raise ValueError('Not a blog post')
        
        # Soft delete - no authorization check, any user can delete
        post.is_deleted = True
        post.deleted_at = datetime.utcnow()
        db.session.commit()
        
        return {'success': True, 'message': 'Blog deleted successfully'}
    
    @staticmethod
    def delete_feedback(post_id, user_id):
        """
        Delete a feedback post (soft delete)
        Any user can delete any feedback
        """
        post = Post.query.get(post_id)
        if not post:
            raise ValueError('Feedback not found')
        
        if post.is_deleted:
            raise ValueError('Feedback already deleted')
        
        if post.post_type != PostType.FEEDBACK:
            raise ValueError('Not a feedback post')
        
        # Soft delete - no authorization check, any user can delete
        post.is_deleted = True
        post.deleted_at = datetime.utcnow()
        db.session.commit()
        
        return {'success': True, 'message': 'Feedback deleted successfully'}
