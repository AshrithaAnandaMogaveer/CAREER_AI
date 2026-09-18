"""
Profile Matching Engine - Phase 7
Weighted similarity scoring for user profile matching (Reach-Out feature)

Scoring Formula:
score = 0.4 × domainMatch + 0.3 × skillOverlap + 0.2 × experienceMatch + 0.1 × interestMatch
"""

from community_models import UserProfile
from user_model import User


class ProfileMatchingEngine:
    """
    Engine for matching user profiles based on weighted similarity
    """
    
    # Weights for similarity components
    DOMAIN_WEIGHT = 0.4
    SKILL_WEIGHT = 0.3
    EXPERIENCE_WEIGHT = 0.2
    INTEREST_WEIGHT = 0.1
    
    @staticmethod
    def calculate_domain_match(user_domain, profile_domains):
        """
        Calculate domain match score (0-100)
        
        Args:
            user_domain: User's primary domain (string)
            profile_domains: Other user's domains (list)
        
        Returns:
            float: Domain match score (0-100)
        """
        if not user_domain or not profile_domains:
            return 0.0
        
        # Normalize to lowercase for comparison
        user_domain_lower = user_domain.lower().strip()
        profile_domains_lower = [d.lower().strip() for d in profile_domains]
        
        # Exact match = 100%
        if user_domain_lower in profile_domains_lower:
            return 100.0
        
        # Partial match (check if domain contains or is contained)
        for domain in profile_domains_lower:
            if user_domain_lower in domain or domain in user_domain_lower:
                return 70.0  # Partial match
        
        return 0.0
    
    @staticmethod
    def calculate_skill_overlap(user_skills, profile_skills):
        """
        Calculate skill overlap score (0-100)
        Uses Jaccard similarity coefficient
        
        Args:
            user_skills: User's skills (list)
            profile_skills: Other user's skills (list)
        
        Returns:
            float: Skill overlap score (0-100)
        """
        if not user_skills or not profile_skills:
            return 0.0
        
        # Convert to sets for comparison (case-insensitive)
        user_skills_set = set(s.lower().strip() for s in user_skills)
        profile_skills_set = set(s.lower().strip() for s in profile_skills)
        
        # Calculate Jaccard similarity
        intersection = len(user_skills_set & profile_skills_set)
        union = len(user_skills_set | profile_skills_set)
        
        if union == 0:
            return 0.0
        
        jaccard_score = (intersection / union) * 100
        return round(jaccard_score, 2)
    
    @staticmethod
    def calculate_experience_match(user_experience, profile_experience):
        """
        Calculate experience match score (0-100)
        Closer experience levels = higher score
        
        Args:
            user_experience: User's experience in years (int)
            profile_experience: Other user's experience in years (int)
        
        Returns:
            float: Experience match score (0-100)
        """
        if user_experience is None or profile_experience is None:
            return 0.0
        
        # Calculate difference in years
        diff = abs(user_experience - profile_experience)
        
        # Score based on difference
        # 0 years diff = 100%, 1 year = 90%, 2 years = 80%, etc.
        # Max penalty at 10+ years difference
        if diff == 0:
            return 100.0
        elif diff <= 10:
            return max(0, 100 - (diff * 10))
        else:
            return 0.0
    
    @staticmethod
    def calculate_interest_match(user_interests, profile_interests):
        """
        Calculate interest match score (0-100)
        Uses Jaccard similarity coefficient
        
        Args:
            user_interests: User's interests (list)
            profile_interests: Other user's interests (list)
        
        Returns:
            float: Interest match score (0-100)
        """
        if not user_interests or not profile_interests:
            return 0.0
        
        # Convert to sets for comparison (case-insensitive)
        user_interests_set = set(i.lower().strip() for i in user_interests)
        profile_interests_set = set(i.lower().strip() for i in profile_interests)
        
        # Calculate Jaccard similarity
        intersection = len(user_interests_set & profile_interests_set)
        union = len(user_interests_set | profile_interests_set)
        
        if union == 0:
            return 0.0
        
        jaccard_score = (intersection / union) * 100
        return round(jaccard_score, 2)
    
    @staticmethod
    def calculate_weighted_score(domain_score, skill_score, experience_score, interest_score):
        """
        Calculate final weighted similarity score
        
        Formula:
        score = 0.4 × domainMatch + 0.3 × skillOverlap + 0.2 × experienceMatch + 0.1 × interestMatch
        
        Args:
            domain_score: Domain match score (0-100)
            skill_score: Skill overlap score (0-100)
            experience_score: Experience match score (0-100)
            interest_score: Interest match score (0-100)
        
        Returns:
            float: Weighted similarity score (0-100)
        """
        weighted_score = (
            (domain_score * ProfileMatchingEngine.DOMAIN_WEIGHT) +
            (skill_score * ProfileMatchingEngine.SKILL_WEIGHT) +
            (experience_score * ProfileMatchingEngine.EXPERIENCE_WEIGHT) +
            (interest_score * ProfileMatchingEngine.INTEREST_WEIGHT)
        )
        
        return round(weighted_score, 2)
    
    @staticmethod
    def match_profiles(user_id, limit=50, min_score=0):
        """
        Find and rank related profiles based on weighted similarity
        
        Args:
            user_id: Current user's ID
            limit: Maximum number of profiles to return
            min_score: Minimum similarity score threshold (0-100)
        
        Returns:
            list: Ranked list of matching profiles with scores
        """
        # Get current user and profile
        user = User.query.get(user_id)
        if not user:
            return []
        
        user_profile = UserProfile.query.filter_by(user_id=user_id).first()
        
        # Get all other active users (regardless of whether they have a UserProfile)
        other_users = User.query.filter(
            User.id != user_id,
            User.is_active == True,
            User.is_deleted == False
        ).all()
        
        results = []
        
        for other_user in other_users:
            # Get their profile if it exists (optional)
            profile = UserProfile.query.filter_by(user_id=other_user.id).first()
            
            # Domain match: compare user.domain vs other_user.domain and profile.domains
            other_domains = []
            if other_user.domain:
                other_domains.append(other_user.domain)
            if profile and profile.domains:
                other_domains.extend(profile.domains)
            
            domain_score = ProfileMatchingEngine.calculate_domain_match(
                user.domain,
                other_domains
            )
            
            skill_score = ProfileMatchingEngine.calculate_skill_overlap(
                (user_profile.skills if user_profile else []) or [],
                (profile.skills if profile else []) or []
            )
            
            experience_score = ProfileMatchingEngine.calculate_experience_match(
                (user_profile.experience_years if user_profile else 0) or 0,
                (profile.experience_years if profile else 0) or 0
            )
            
            interest_score = ProfileMatchingEngine.calculate_interest_match(
                (user_profile.interests if user_profile else []) or [],
                (profile.interests if profile else []) or []
            )
            
            # Calculate weighted total score
            total_score = ProfileMatchingEngine.calculate_weighted_score(
                domain_score,
                skill_score,
                experience_score,
                interest_score
            )
            
            # Always include same-domain users; otherwise apply min_score threshold
            if domain_score > 0 or total_score >= min_score:
                common_skills = list(
                    set(s.lower() for s in ((user_profile.skills if user_profile else []) or [])) &
                    set(s.lower() for s in ((profile.skills if profile else []) or []))
                )
                
                common_interests = list(
                    set(i.lower() for i in ((user_profile.interests if user_profile else []) or [])) &
                    set(i.lower() for i in ((profile.interests if profile else []) or []))
                )
                
                results.append({
                    'id': other_user.id,
                    'name': other_user.name,
                    'email': other_user.email,
                    'domain': other_user.domain,
                    'profile_picture': other_user.profile_picture,
                    'bio': profile.bio if profile else None,
                    'location': profile.location if profile else None,
                    'experience_years': profile.experience_years if profile else 0,
                    'projects_count': profile.projects_count if profile else 0,
                    'similarity_score': total_score,
                    'score_breakdown': {
                        'domain_match': domain_score,
                        'skill_overlap': skill_score,
                        'experience_match': experience_score,
                        'interest_match': interest_score
                    },
                    'common_skills': common_skills[:5],
                    'common_interests': common_interests[:3],
                    'total_skills': len((profile.skills if profile else []) or []),
                    'total_interests': len((profile.interests if profile else []) or [])
                })
        
        # Sort by similarity score (descending)
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Return top N results
        return results[:limit]
    
    @staticmethod
    def get_match_explanation(score_breakdown):
        """
        Generate human-readable explanation of match score
        
        Args:
            score_breakdown: Dictionary with component scores
        
        Returns:
            str: Explanation text
        """
        explanations = []
        
        domain_score = score_breakdown.get('domain_match', 0)
        skill_score = score_breakdown.get('skill_overlap', 0)
        experience_score = score_breakdown.get('experience_match', 0)
        interest_score = score_breakdown.get('interest_match', 0)
        
        if domain_score >= 70:
            explanations.append("Works in similar domain")
        
        if skill_score >= 50:
            explanations.append("Strong skill overlap")
        elif skill_score >= 30:
            explanations.append("Some common skills")
        
        if experience_score >= 80:
            explanations.append("Similar experience level")
        
        if interest_score >= 40:
            explanations.append("Shared interests")
        
        if not explanations:
            return "Potential connection"
        
        return " • ".join(explanations)
