"""
Feed Ranking Engine
Intelligent feed ranking using recency, engagement, and relevance
"""

import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple
from community_models import Post, UserProfile, PostType
from recommendation_engine import RecommendationEngine


class FeedRankingEngine:
    """
    Feed ranking engine for personalized content discovery
    
    Ranking Formula:
    rankScore = (0.5 × recencyScore) + (0.3 × engagementScore) + (0.2 × relevanceScore)
    
    Where:
    - recencyScore = e^(-0.1 × hoursSincePost)
    - engagementScore = normalized(likes + 2 × comments)
    - relevanceScore = cosine(userInterests, postTags)
    """
    
    # Weights for ranking components
    RECENCY_WEIGHT = 0.5
    ENGAGEMENT_WEIGHT = 0.3
    RELEVANCE_WEIGHT = 0.2
    
    # Decay rate for recency (higher = faster decay)
    RECENCY_DECAY_RATE = 0.1
    
    @staticmethod
    def _calculate_recency_score(post_created_at: datetime) -> float:
        """
        Calculate recency score using exponential decay
        
        Formula: e^(-0.1 × hoursSincePost)
        
        Returns: Score between 0 and 1 (1 = just posted, approaches 0 as time passes)
        """
        now = datetime.utcnow()
        time_diff = now - post_created_at
        hours_since_post = time_diff.total_seconds() / 3600
        
        # Exponential decay
        recency_score = np.exp(-FeedRankingEngine.RECENCY_DECAY_RATE * hours_since_post)
        
        return float(recency_score)
    
    @staticmethod
    def _calculate_engagement_score(likes_count: int, comments_count: int, max_engagement: int = 100) -> float:
        """
        Calculate engagement score with weighted comments
        
        Formula: (likes + 2 × comments) / max_engagement
        Comments are weighted 2x because they indicate deeper engagement
        
        Returns: Normalized score between 0 and 1
        """
        # Comments are worth 2x likes (deeper engagement)
        raw_engagement = likes_count + (2 * comments_count)
        
        # Normalize to 0-1 range
        # Use sigmoid-like normalization to handle outliers
        normalized = raw_engagement / (raw_engagement + max_engagement)
        
        return float(normalized)
    
    @staticmethod
    def _calculate_relevance_score(user_interests: List[str], post_tags: List[str]) -> float:
        """
        Calculate relevance score using cosine similarity
        
        Formula: cosine(userInterests, postTags)
        
        Returns: Score between 0 and 1 (1 = perfect match, 0 = no match)
        """
        if not user_interests or not post_tags:
            return 0.0
        
        # Build vocabulary
        vocabulary = RecommendationEngine._build_vocabulary(user_interests, [post_tags])
        
        if not vocabulary:
            return 0.0
        
        # Vectorize
        user_vector = RecommendationEngine._vectorize(user_interests, vocabulary)
        post_vector = RecommendationEngine._vectorize(post_tags, vocabulary)
        
        # Calculate cosine similarity
        similarity = RecommendationEngine._cosine_similarity(user_vector, post_vector)
        
        return float(similarity)
    
    @staticmethod
    def _calculate_rank_score(
        recency_score: float,
        engagement_score: float,
        relevance_score: float
    ) -> float:
        """
        Calculate final rank score using weighted formula
        
        Formula: (0.5 × recency) + (0.3 × engagement) + (0.2 × relevance)
        
        Returns: Final rank score between 0 and 1
        """
        rank_score = (
            FeedRankingEngine.RECENCY_WEIGHT * recency_score +
            FeedRankingEngine.ENGAGEMENT_WEIGHT * engagement_score +
            FeedRankingEngine.RELEVANCE_WEIGHT * relevance_score
        )
        
        return float(rank_score)
    
    @staticmethod
    def rank_feed(
        user_id: int,
        post_type: str = None,
        limit: int = 50,
        include_scores: bool = False
    ) -> List[Dict]:
        """
        Generate ranked feed for user
        
        Args:
            user_id: User ID
            post_type: Filter by post type ('BLOG', 'FEEDBACK', or None for all)
            limit: Maximum number of posts to return
            include_scores: Include score breakdown in response
        
        Returns:
            List of ranked posts with scores
        """
        # Get user profile for relevance scoring
        user_profile = UserProfile.query.filter_by(user_id=user_id).first()
        
        # Get user interests
        user_interests = []
        if user_profile:
            if user_profile.skills:
                user_interests.extend(user_profile.skills)
            if user_profile.interests:
                user_interests.extend(user_profile.interests)
            if user_profile.domains:
                user_interests.extend(user_profile.domains)
        
        # Query posts
        query = Post.query.filter_by(is_deleted=False)
        
        # Filter by post type if specified
        if post_type:
            if post_type.upper() == 'BLOG':
                query = query.filter_by(post_type=PostType.BLOG)
            elif post_type.upper() == 'FEEDBACK':
                query = query.filter_by(post_type=PostType.FEEDBACK)
        
        # Get all posts (we'll rank them in Python)
        posts = query.all()
        
        if not posts:
            return []
        
        # Calculate max engagement for normalization
        max_engagement = max(
            (p.likes_count + 2 * p.comments_count) for p in posts
        ) if posts else 100
        
        # Rank each post
        ranked_posts = []
        for post in posts:
            # Calculate component scores
            recency_score = FeedRankingEngine._calculate_recency_score(post.created_at)
            engagement_score = FeedRankingEngine._calculate_engagement_score(
                post.likes_count,
                post.comments_count,
                max_engagement
            )
            relevance_score = FeedRankingEngine._calculate_relevance_score(
                user_interests,
                post.tags or []
            )
            
            # Calculate final rank score
            rank_score = FeedRankingEngine._calculate_rank_score(
                recency_score,
                engagement_score,
                relevance_score
            )
            
            # Build post data
            post_data = post.to_dict(include_author=True)
            post_data['rank_score'] = round(rank_score * 100, 2)  # Convert to percentage
            
            # Include score breakdown if requested
            if include_scores:
                post_data['score_breakdown'] = {
                    'recency_score': round(recency_score * 100, 2),
                    'engagement_score': round(engagement_score * 100, 2),
                    'relevance_score': round(relevance_score * 100, 2),
                    'hours_since_post': round((datetime.utcnow() - post.created_at).total_seconds() / 3600, 2)
                }
            
            ranked_posts.append(post_data)
        
        # Sort by rank score descending
        ranked_posts.sort(key=lambda x: x['rank_score'], reverse=True)
        
        # Return top N
        return ranked_posts[:limit]
    
    @staticmethod
    def get_trending_posts(
        post_type: str = None,
        time_window_hours: int = 24,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get trending posts based on recent engagement
        
        Args:
            post_type: Filter by post type
            time_window_hours: Time window for trending calculation
            limit: Maximum number of posts
        
        Returns:
            List of trending posts
        """
        from datetime import timedelta
        
        # Calculate cutoff time
        cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
        
        # Query recent posts
        query = Post.query.filter(
            Post.is_deleted == False,
            Post.created_at >= cutoff_time
        )
        
        # Filter by post type if specified
        if post_type:
            if post_type.upper() == 'BLOG':
                query = query.filter_by(post_type=PostType.BLOG)
            elif post_type.upper() == 'FEEDBACK':
                query = query.filter_by(post_type=PostType.FEEDBACK)
        
        posts = query.all()
        
        if not posts:
            return []
        
        # Calculate trending score (engagement / age)
        trending_posts = []
        for post in posts:
            hours_old = (datetime.utcnow() - post.created_at).total_seconds() / 3600
            hours_old = max(hours_old, 0.1)  # Avoid division by zero
            
            # Trending score: engagement per hour
            engagement = post.likes_count + (2 * post.comments_count)
            trending_score = engagement / hours_old
            
            post_data = post.to_dict(include_author=True)
            post_data['trending_score'] = round(trending_score, 2)
            post_data['hours_old'] = round(hours_old, 2)
            
            trending_posts.append(post_data)
        
        # Sort by trending score
        trending_posts.sort(key=lambda x: x['trending_score'], reverse=True)
        
        return trending_posts[:limit]
    
    @staticmethod
    def get_feed_stats(user_id: int) -> Dict:
        """
        Get feed statistics for user
        
        Returns:
            Dictionary with feed stats
        """
        # Get user profile
        user_profile = UserProfile.query.filter_by(user_id=user_id).first()
        
        # Count posts by type
        total_posts = Post.query.filter_by(is_deleted=False).count()
        blog_posts = Post.query.filter_by(is_deleted=False, post_type=PostType.BLOG).count()
        feedback_posts = Post.query.filter_by(is_deleted=False, post_type=PostType.FEEDBACK).count()
        
        # Get recent posts count (last 24 hours)
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(hours=24)
        recent_posts = Post.query.filter(
            Post.is_deleted == False,
            Post.created_at >= cutoff
        ).count()
        
        return {
            'total_posts': total_posts,
            'blog_posts': blog_posts,
            'feedback_posts': feedback_posts,
            'recent_posts_24h': recent_posts,
            'has_profile': user_profile is not None,
            'personalization_enabled': user_profile is not None and (
                bool(user_profile.skills) or 
                bool(user_profile.interests) or 
                bool(user_profile.domains)
            )
        }
