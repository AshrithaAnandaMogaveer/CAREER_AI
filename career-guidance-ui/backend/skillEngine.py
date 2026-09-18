"""
Skill Engine Module
Handles skill matching, gap analysis, and career readiness scoring
"""

import numpy as np
from typing import List, Dict, Set, Tuple
from sklearn.metrics.pairwise import cosine_similarity


# Role skill matrix - defines required skills for each domain/role
ROLE_SKILL_MATRIX = {
    'Software Development': {
        'required': ['python', 'javascript', 'git', 'sql', 'rest api', 'data structures', 'algorithms'],
        'preferred': ['java', 'docker', 'kubernetes', 'aws', 'ci/cd', 'microservices', 'design patterns'],
        'weights': {'required': 3, 'preferred': 1}
    },
    'Data Science': {
        'required': ['python', 'sql', 'statistics', 'machine learning', 'pandas', 'numpy', 'data analysis'],
        'preferred': ['tensorflow', 'pytorch', 'deep learning', 'big data', 'spark', 'tableau'],
        'weights': {'required': 3, 'preferred': 1}
    },
    'Machine Learning': {
        'required': ['python', 'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'statistics', 'mathematics'],
        'preferred': ['nlp', 'computer vision', 'mlops', 'aws', 'docker', 'kubernetes'],
        'weights': {'required': 3, 'preferred': 1}
    },
    'Web Development': {
        'required': ['html', 'css', 'javascript', 'react', 'node.js', 'rest api', 'git'],
        'preferred': ['typescript', 'next.js', 'mongodb', 'postgresql', 'docker', 'aws'],
        'weights': {'required': 3, 'preferred': 1}
    },
    'Mobile Development': {
        'required': ['java', 'kotlin', 'swift', 'react native', 'flutter', 'rest api', 'git'],
        'preferred': ['firebase', 'push notifications', 'app store', 'play store', 'ui/ux'],
        'weights': {'required': 3, 'preferred': 1}
    },
    'DevOps': {
        'required': ['linux', 'docker', 'kubernetes', 'ci/cd', 'jenkins', 'git', 'bash'],
        'preferred': ['terraform', 'ansible', 'aws', 'azure', 'monitoring', 'prometheus'],
        'weights': {'required': 3, 'preferred': 1}
    },
    'Cybersecurity': {
        'required': ['networking', 'linux', 'cybersecurity', 'penetration testing', 'owasp', 'encryption'],
        'preferred': ['python', 'bash', 'wireshark', 'metasploit', 'burp suite', 'security auditing'],
        'weights': {'required': 3, 'preferred': 1}
    },
    'Cloud Computing': {
        'required': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'linux', 'networking'],
        'preferred': ['terraform', 'serverless', 'lambda', 'microservices', 'ci/cd'],
        'weights': {'required': 3, 'preferred': 1}
    },
    'UI/UX Design': {
        'required': ['figma', 'sketch', 'adobe xd', 'wireframing', 'prototyping', 'user research'],
        'preferred': ['html', 'css', 'javascript', 'responsive design', 'accessibility', 'design systems'],
        'weights': {'required': 3, 'preferred': 1}
    },
    'Product Management': {
        'required': ['product strategy', 'roadmapping', 'agile', 'scrum', 'user stories', 'stakeholder management'],
        'preferred': ['sql', 'data analysis', 'jira', 'confluence', 'a/b testing', 'analytics'],
        'weights': {'required': 3, 'preferred': 1}
    },
}


# Common resume mistakes patterns
RESUME_MISTAKES = {
    'generic_phrases': [
        'hard worker', 'team player', 'detail oriented', 'fast learner',
        'self motivated', 'excellent communication', 'results driven'
    ],
    'missing_metrics': [
        'improved', 'increased', 'reduced', 'optimized', 'enhanced',
        'developed', 'created', 'built', 'designed', 'implemented'
    ],
    'required_sections': ['experience', 'education', 'skills', 'projects']
}


class SkillEngine:
    """Handles skill analysis, matching, and scoring"""
    
    def __init__(self):
        self.role_matrix = ROLE_SKILL_MATRIX
        self.mistakes = RESUME_MISTAKES
    
    def normalize_skills(self, skills: List[str]) -> Set[str]:
        """Normalize and deduplicate skills"""
        normalized = set()
        for skill in skills:
            skill_lower = skill.lower().strip()
            if skill_lower:
                normalized.add(skill_lower)
        return normalized
    
    def merge_skills(self, resume_skills: List[str], manual_skills: List[str]) -> List[str]:
        """Merge skills from resume and manual entry"""
        all_skills = self.normalize_skills(resume_skills + manual_skills)
        return sorted(list(all_skills))
    
    def create_skill_vector(self, user_skills: Set[str], domain: str) -> np.ndarray:
        """Create binary skill vector for user"""
        if domain not in self.role_matrix:
            domain = 'Software Development'  # Default
        
        role_skills = self.role_matrix[domain]
        all_required_skills = role_skills['required'] + role_skills['preferred']
        
        # Create binary vector
        vector = np.zeros(len(all_required_skills))
        for i, skill in enumerate(all_required_skills):
            if skill in user_skills:
                vector[i] = 1
        
        return vector
    
    def create_role_vector(self, domain: str) -> np.ndarray:
        """Create weighted skill vector for role"""
        if domain not in self.role_matrix:
            domain = 'Software Development'
        
        role_skills = self.role_matrix[domain]
        weights = role_skills['weights']
        
        # Create weighted vector
        required_count = len(role_skills['required'])
        preferred_count = len(role_skills['preferred'])
        
        vector = np.concatenate([
            np.full(required_count, weights['required']),
            np.full(preferred_count, weights['preferred'])
        ])
        
        return vector
    
    def calculate_cosine_similarity(self, user_vector: np.ndarray, role_vector: np.ndarray) -> float:
        """Calculate cosine similarity between user and role vectors"""
        if np.sum(user_vector) == 0 or np.sum(role_vector) == 0:
            return 0.0
        
        similarity = cosine_similarity(
            user_vector.reshape(1, -1),
            role_vector.reshape(1, -1)
        )[0][0]
        
        return float(similarity)
    
    def calculate_readiness_score(
        self,
        user_skills: Set[str],
        domain: str,
        experience_years: int = 0,
        has_projects: bool = False,
        has_certifications: bool = False
    ) -> Dict:
        """Calculate comprehensive career readiness score"""
        
        if domain not in self.role_matrix:
            domain = 'Software Development'
        
        role_skills = self.role_matrix[domain]
        required_skills = set(role_skills['required'])
        preferred_skills = set(role_skills['preferred'])
        
        # Calculate skill coverage
        matched_required = user_skills.intersection(required_skills)
        matched_preferred = user_skills.intersection(preferred_skills)
        
        required_coverage = len(matched_required) / len(required_skills) if required_skills else 0
        preferred_coverage = len(matched_preferred) / len(preferred_skills) if preferred_skills else 0
        
        # Base score from skill coverage (70% weight)
        skill_score = (required_coverage * 0.7 + preferred_coverage * 0.3) * 70
        
        # Experience bonus (15% weight)
        experience_score = min(experience_years * 3, 15)
        
        # Project bonus (10% weight)
        project_score = 10 if has_projects else 0
        
        # Certification bonus (5% weight)
        cert_score = 5 if has_certifications else 0
        
        # Total score
        total_score = skill_score + experience_score + project_score + cert_score
        total_score = min(total_score, 100)  # Cap at 100
        
        # Confidence level
        confidence = self._calculate_confidence(
            required_coverage,
            preferred_coverage,
            experience_years,
            has_projects
        )
        
        return {
            'total_score': round(total_score, 1),
            'skill_score': round(skill_score, 1),
            'experience_score': round(experience_score, 1),
            'project_score': round(project_score, 1),
            'certification_score': round(cert_score, 1),
            'required_coverage': round(required_coverage * 100, 1),
            'preferred_coverage': round(preferred_coverage * 100, 1),
            'confidence_level': confidence,
            'matched_required': len(matched_required),
            'total_required': len(required_skills),
            'matched_preferred': len(matched_preferred),
            'total_preferred': len(preferred_skills),
        }
    
    def _calculate_confidence(
        self,
        required_coverage: float,
        preferred_coverage: float,
        experience_years: int,
        has_projects: bool
    ) -> str:
        """Calculate confidence level"""
        score = (
            required_coverage * 50 +
            preferred_coverage * 30 +
            min(experience_years / 5, 1) * 15 +
            (5 if has_projects else 0)
        )
        
        if score >= 80:
            return 'High'
        elif score >= 60:
            return 'Medium'
        else:
            return 'Low'
    
    def identify_missing_skills(self, user_skills: Set[str], domain: str) -> Dict:
        """Identify missing skills with prioritization"""
        if domain not in self.role_matrix:
            domain = 'Software Development'
        
        role_skills = self.role_matrix[domain]
        required_skills = set(role_skills['required'])
        preferred_skills = set(role_skills['preferred'])
        
        missing_required = required_skills - user_skills
        missing_preferred = preferred_skills - user_skills
        
        return {
            'critical': sorted(list(missing_required)),
            'recommended': sorted(list(missing_preferred)),
            'total_missing': len(missing_required) + len(missing_preferred),
        }
    
    def calculate_resume_strength(
        self,
        text: str,
        skills: List[str],
        projects: List[str],
        certifications: List[str],
        experience_years: int
    ) -> Dict:
        """Calculate resume strength score"""
        text_lower = text.lower()
        
        # Skill coverage (30 points)
        skill_score = min(len(skills) * 2, 30)
        
        # Project count (20 points)
        project_score = min(len(projects) * 4, 20)
        
        # Certification bonus (15 points)
        cert_score = min(len(certifications) * 3, 15)
        
        # Experience (15 points)
        exp_score = min(experience_years * 3, 15)
        
        # Measurable impact keywords (10 points)
        impact_keywords = ['increased', 'reduced', 'improved', 'optimized', 'achieved', 'delivered']
        impact_count = sum(1 for keyword in impact_keywords if keyword in text_lower)
        impact_score = min(impact_count * 2, 10)
        
        # Quantifiable metrics (10 points)
        metric_pattern = r'\d+%|\d+x|\$\d+|\d+\s*(?:users|customers|clients|projects)'
        import re
        metric_count = len(re.findall(metric_pattern, text_lower))
        metric_score = min(metric_count * 2, 10)
        
        total_strength = skill_score + project_score + cert_score + exp_score + impact_score + metric_score
        
        return {
            'total_strength': round(total_strength, 1),
            'skill_score': skill_score,
            'project_score': project_score,
            'certification_score': cert_score,
            'experience_score': exp_score,
            'impact_score': impact_score,
            'metric_score': metric_score,
            'max_score': 100,
        }
    
    def detect_mistakes(self, text: str, projects: List[str]) -> List[Dict]:
        """Detect common resume mistakes"""
        text_lower = text.lower()
        mistakes = []
        
        # Check for generic phrases
        generic_count = sum(1 for phrase in self.mistakes['generic_phrases'] if phrase in text_lower)
        if generic_count > 2:
            mistakes.append({
                'type': 'generic_phrases',
                'severity': 'medium',
                'message': f'Found {generic_count} generic phrases. Use specific achievements instead.',
                'suggestion': 'Replace generic phrases with quantifiable achievements and specific examples.'
            })
        
        # Check for missing metrics
        has_metrics = any(keyword in text_lower for keyword in self.mistakes['missing_metrics'])
        import re
        metric_pattern = r'\d+%|\d+x|\$\d+|\d+\s*(?:users|customers|clients|projects)'
        metric_count = len(re.findall(metric_pattern, text_lower))
        
        if has_metrics and metric_count < 3:
            mistakes.append({
                'type': 'missing_metrics',
                'severity': 'high',
                'message': 'Action words found but lacking quantifiable metrics.',
                'suggestion': 'Add specific numbers, percentages, or metrics to demonstrate impact.'
            })
        
        # Check for project descriptions
        if len(projects) == 0:
            mistakes.append({
                'type': 'no_projects',
                'severity': 'high',
                'message': 'No projects section found.',
                'suggestion': 'Add a projects section with 2-3 relevant projects showcasing your skills.'
            })
        
        # Check for required sections
        missing_sections = []
        for section in self.mistakes['required_sections']:
            if section not in text_lower:
                missing_sections.append(section)
        
        if missing_sections:
            mistakes.append({
                'type': 'missing_sections',
                'severity': 'high',
                'message': f'Missing sections: {", ".join(missing_sections)}',
                'suggestion': 'Ensure your resume includes all standard sections.'
            })
        
        return mistakes
    
    def generate_suggestions(
        self,
        readiness_score: float,
        missing_skills: Dict,
        resume_strength: Dict,
        mistakes: List[Dict]
    ) -> List[str]:
        """Generate prioritized improvement suggestions"""
        suggestions = []
        
        # Skill-based suggestions
        if missing_skills['critical']:
            suggestions.append(
                f"🎯 Priority: Learn these critical skills: {', '.join(missing_skills['critical'][:3])}"
            )
        
        if readiness_score < 60:
            suggestions.append(
                "📚 Focus on building foundational skills in your target domain"
            )
        
        # Resume strength suggestions
        if resume_strength['project_score'] < 12:
            suggestions.append(
                "💼 Add 2-3 substantial projects to demonstrate practical experience"
            )
        
        if resume_strength['impact_score'] < 6:
            suggestions.append(
                "📊 Include measurable achievements (e.g., 'Improved performance by 40%')"
            )
        
        if resume_strength['certification_score'] < 9:
            suggestions.append(
                "🏆 Consider obtaining relevant certifications to boost credibility"
            )
        
        # Mistake-based suggestions
        for mistake in mistakes:
            if mistake['severity'] == 'high':
                suggestions.append(f"⚠️ {mistake['suggestion']}")
        
        # General suggestions
        if missing_skills['recommended']:
            suggestions.append(
                f"✨ Enhance your profile with: {', '.join(missing_skills['recommended'][:3])}"
            )
        
        return suggestions[:8]  # Return top 8 suggestions
    
    def suggest_domains(self, user_skills: Set[str], top_n: int = 3) -> List[Dict]:
        """Suggest best matching domains based on skills"""
        domain_scores = []
        
        for domain, role_data in self.role_matrix.items():
            required_skills = set(role_data['required'])
            preferred_skills = set(role_data['preferred'])
            
            # Calculate match score
            required_match = len(user_skills.intersection(required_skills))
            preferred_match = len(user_skills.intersection(preferred_skills))
            
            total_match = required_match * 3 + preferred_match
            max_possible = len(required_skills) * 3 + len(preferred_skills)
            
            match_percentage = (total_match / max_possible * 100) if max_possible > 0 else 0
            
            domain_scores.append({
                'domain': domain,
                'match_percentage': round(match_percentage, 1),
                'matched_skills': required_match + preferred_match,
                'total_skills': len(required_skills) + len(preferred_skills),
            })
        
        # Sort by match percentage
        domain_scores.sort(key=lambda x: x['match_percentage'], reverse=True)
        
        return domain_scores[:top_n]
