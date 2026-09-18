"""
Community Recommendation Engine
Vector-based interest matching using cosine similarity
"""

import numpy as np
from typing import List, Dict, Tuple
from community_models import Community, UserProfile
from user_model import User


class RecommendationEngine:
    """
    Recommendation engine for community matching
    Uses cosine similarity between user interests and community tags
    """
    
    @staticmethod
    def _build_vocabulary(user_interests: List[str], community_tags_list: List[List[str]]) -> Dict[str, int]:
        """
        Build vocabulary from all unique terms
        Returns: {term: index} mapping
        """
        vocabulary = set()
        
        # Add user interests
        vocabulary.update([interest.lower().strip() for interest in user_interests])
        
        # Add all community tags
        for tags in community_tags_list:
            vocabulary.update([tag.lower().strip() for tag in tags])
        
        # Create index mapping
        return {term: idx for idx, term in enumerate(sorted(vocabulary))}
    
    @staticmethod
    def _vectorize(terms: List[str], vocabulary: Dict[str, int]) -> np.ndarray:
        """
        Convert list of terms into binary vector
        Returns: numpy array of 0s and 1s
        """
        vector = np.zeros(len(vocabulary))
        
        for term in terms:
            term_lower = term.lower().strip()
            if term_lower in vocabulary:
                idx = vocabulary[term_lower]
                vector[idx] = 1
        
        return vector
    
    @staticmethod
    def _cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Compute cosine similarity between two vectors
        Formula: cos(θ) = (A · B) / (||A|| * ||B||)
        Returns: similarity score between 0 and 1
        """
        # Handle zero vectors
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Compute dot product and normalize
        dot_product = np.dot(vec1, vec2)
        similarity = dot_product / (norm1 * norm2)
        
        return float(similarity)
    
    @staticmethod
    def recommend_communities(
        user_id: int,
        limit: int = 5,
        exclude_joined: bool = True
    ) -> List[Dict]:
        """
        Recommend communities based on user interests
        
        Algorithm:
        1. Get user interests from UserProfile
        2. Get all communities with their tags
        3. Build vocabulary from all terms
        4. Convert user interests to binary vector
        5. Convert each community tags to binary vector
        6. Compute cosine similarity for each community
        7. Sort by similarity descending
        8. Return top N communities
        
        Args:
            user_id: User ID
            limit: Number of recommendations to return (default 5)
            exclude_joined: Exclude communities user already joined
        
        Returns:
            List of recommended communities with similarity scores
        """
        # Get user profile
        user_profile = UserProfile.query.filter_by(user_id=user_id).first()
        
        if not user_profile:
            # No profile, return empty recommendations
            return []
        
        # Get user interests (combine skills, interests, domains)
        user_interests = []
        if user_profile.skills:
            user_interests.extend(user_profile.skills)
        if user_profile.interests:
            user_interests.extend(user_profile.interests)
        if user_profile.domains:
            user_interests.extend(user_profile.domains)
        
        if not user_interests:
            # No interests, return empty recommendations
            return []
        
        # Get all active communities
        communities = Community.query.filter_by(is_deleted=False).all()
        
        if not communities:
            return []
        
        # Filter out joined communities if requested
        if exclude_joined:
            from community_models import CommunityMember
            joined_ids = set(
                m.community_id for m in 
                CommunityMember.query.filter_by(user_id=user_id, is_deleted=False).all()
            )
            communities = [c for c in communities if c.id not in joined_ids]
        
        if not communities:
            return []
        
        # Extract community tags
        community_tags_list = [c.tags or [] for c in communities]
        
        # Build vocabulary
        vocabulary = RecommendationEngine._build_vocabulary(user_interests, community_tags_list)
        
        if not vocabulary:
            return []
        
        # Vectorize user interests
        user_vector = RecommendationEngine._vectorize(user_interests, vocabulary)
        
        # Compute similarity for each community
        recommendations = []
        for community, tags in zip(communities, community_tags_list):
            # Vectorize community tags
            community_vector = RecommendationEngine._vectorize(tags, vocabulary)
            
            # Compute cosine similarity
            similarity = RecommendationEngine._cosine_similarity(user_vector, community_vector)
            
            # Only include if there's some similarity
            if similarity > 0:
                # Find matching tags
                matching_tags = [
                    tag for tag in tags 
                    if tag.lower().strip() in [i.lower().strip() for i in user_interests]
                ]
                
                recommendations.append({
                    'community': community,
                    'similarity_score': similarity,
                    'matching_tags': matching_tags
                })
        
        # Sort by similarity descending
        recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Return top N with formatted data
        results = []
        for rec in recommendations[:limit]:
            community = rec['community']
            results.append({
                'id': community.id,
                'name': community.name,
                'description': community.description,
                'category': community.category,
                'tags': community.tags,
                'members_count': community.members_count,
                'posts_count': community.posts_count,
                'similarity_score': round(rec['similarity_score'] * 100, 2),  # Convert to percentage
                'matching_tags': rec['matching_tags'],
                'match_reason': f"Matches {len(rec['matching_tags'])} of your interests"
            })
        
        return results
    
    @staticmethod
    def get_trending_communities(limit: int = 5) -> List[Dict]:
        """
        Get trending communities based on activity
        Fallback when user has no profile or interests
        
        Ranking factors:
        - Members count (40%)
        - Posts count (30%)
        - Recent activity (30%)
        
        Returns:
            List of trending communities
        """
        communities = Community.query.filter_by(is_deleted=False).all()
        
        if not communities:
            return []
        
        # Calculate trending score
        trending = []
        for community in communities:
            # Normalize scores (simple approach)
            members_score = min(community.members_count / 100, 1.0) * 0.4
            posts_score = min(community.posts_count / 50, 1.0) * 0.3
            
            # Recent activity score (communities created recently get boost)
            from datetime import datetime, timedelta
            days_old = (datetime.utcnow() - community.created_at).days
            recency_score = max(0, 1 - (days_old / 365)) * 0.3
            
            trending_score = members_score + posts_score + recency_score
            
            trending.append({
                'community': community,
                'trending_score': trending_score
            })
        
        # Sort by trending score
        trending.sort(key=lambda x: x['trending_score'], reverse=True)
        
        # Format results
        results = []
        for item in trending[:limit]:
            community = item['community']
            results.append({
                'id': community.id,
                'name': community.name,
                'description': community.description,
                'category': community.category,
                'tags': community.tags,
                'members_count': community.members_count,
                'posts_count': community.posts_count,
                'trending_score': round(item['trending_score'] * 100, 2),
                'is_trending': True
            })
        
        return results
