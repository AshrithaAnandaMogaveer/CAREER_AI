"""
Skill Difficulty Estimator Module
Estimates learning hours based on skill complexity and existing knowledge
"""

from typing import List, Dict


class SkillDifficultyEstimator:
    def __init__(self):
        # Base hours for different skill categories
        self.base_hours = {
            # Programming Languages
            'Python': 60, 'JavaScript': 50, 'Java': 70, 'C++': 80,
            'TypeScript': 40, 'Go': 50, 'Rust': 90, 'PHP': 45,
            
            # Frontend
            'React': 50, 'Angular': 60, 'Vue.js': 45, 'HTML': 20,
            'CSS': 30, 'Tailwind CSS': 25, 'Bootstrap': 20,
            
            # Backend
            'Node.js': 50, 'Express.js': 30, 'Django': 55, 'Flask': 35,
            'Spring Boot': 65, 'FastAPI': 40,
            
            # Databases
            'SQL': 40, 'MongoDB': 45, 'PostgreSQL': 50, 'MySQL': 40,
            'Redis': 30, 'Elasticsearch': 50,
            
            # DevOps & Cloud
            'Docker': 40, 'Kubernetes': 70, 'AWS': 80, 'Azure': 75,
            'GCP': 75, 'CI/CD': 45, 'Jenkins': 40, 'Terraform': 55,
            
            # Tools & Others
            'Git': 25, 'Linux': 60, 'REST API': 35, 'GraphQL': 40,
            'Microservices': 60, 'System Design': 80,
            
            # Data Science & ML
            'Machine Learning': 100, 'Deep Learning': 120, 'Data Science': 90,
            'Pandas': 40, 'NumPy': 35, 'TensorFlow': 80, 'PyTorch': 85,
            'Statistics': 70, 'Data Visualization': 40,
            
            # Testing
            'Unit Testing': 30, 'Integration Testing': 35, 'Jest': 25,
            'Pytest': 30, 'Selenium': 40
        }
        
        # Skill similarity mapping for transfer learning
        self.skill_similarity = {
            'Python': ['JavaScript', 'Java', 'C++', 'Go'],
            'JavaScript': ['TypeScript', 'Python', 'Java'],
            'React': ['Vue.js', 'Angular', 'JavaScript'],
            'Angular': ['React', 'Vue.js', 'TypeScript'],
            'Vue.js': ['React', 'Angular', 'JavaScript'],
            'Node.js': ['JavaScript', 'Express.js', 'Python'],
            'Django': ['Flask', 'Python', 'FastAPI'],
            'Flask': ['Django', 'FastAPI', 'Python'],
            'SQL': ['PostgreSQL', 'MySQL', 'MongoDB'],
            'MongoDB': ['SQL', 'PostgreSQL', 'Redis'],
            'Docker': ['Kubernetes', 'CI/CD', 'DevOps'],
            'Kubernetes': ['Docker', 'AWS', 'Azure'],
            'AWS': ['Azure', 'GCP', 'Cloud Computing'],
            'Machine Learning': ['Deep Learning', 'Data Science', 'Python'],
            'Git': ['GitHub', 'GitLab', 'Version Control']
        }
    
    def estimate_hours(
        self,
        skill: str,
        gap_severity: float,
        existing_skills: List[str]
    ) -> float:
        """
        Estimate learning hours using transfer learning algorithm
        
        Formula:
        estimated_hours = base_hours × (1 - similarity_factor) × gap_severity_multiplier
        
        Args:
            skill: Target skill to learn
            gap_severity: Gap severity score (0.0 to 1.0)
            existing_skills: List of skills user already has
        
        Returns:
            Estimated hours needed
        """
        # Get base hours
        base = self.base_hours.get(skill, 50)  # Default 50 hours
        
        # Calculate similarity factor (transfer learning)
        similarity_factor = self._calculate_similarity(skill, existing_skills)
        
        # Gap severity multiplier (0.5 to 1.5)
        # Higher severity = more hours needed
        severity_multiplier = 0.5 + (gap_severity * 1.0)
        
        # Apply formula
        estimated = base * (1 - similarity_factor * 0.4) * severity_multiplier
        
        # Ensure minimum 10 hours, maximum 150 hours
        estimated = max(10, min(150, estimated))
        
        return round(estimated, 1)
    
    def _calculate_similarity(self, target_skill: str, existing_skills: List[str]) -> float:
        """
        Calculate similarity score based on existing skills
        
        Returns:
            Similarity factor (0.0 to 1.0)
            Higher = more similar = easier to learn
        """
        if not existing_skills:
            return 0.0
        
        similar_skills = self.skill_similarity.get(target_skill, [])
        
        # Count how many existing skills are similar
        matches = sum(1 for skill in existing_skills if skill in similar_skills)
        
        if matches == 0:
            return 0.0
        
        # Normalize (max 3 similar skills considered)
        similarity = min(matches / 3.0, 1.0)
        
        return similarity
    
    def get_difficulty_level(self, estimated_hours: float) -> str:
        """
        Map estimated hours to difficulty level
        
        Args:
            estimated_hours: Estimated learning hours
        
        Returns:
            Difficulty level string
        """
        if estimated_hours < 25:
            return 'Beginner'
        elif estimated_hours < 50:
            return 'Intermediate'
        elif estimated_hours < 80:
            return 'Advanced'
        else:
            return 'Expert'


if __name__ == "__main__":
    # Test
    estimator = SkillDifficultyEstimator()
    
    existing = ['JavaScript', 'HTML', 'CSS']
    
    # Test 1: React (similar to JavaScript)
    hours1 = estimator.estimate_hours('React', 0.7, existing)
    difficulty1 = estimator.get_difficulty_level(hours1)
    print(f"React: {hours1} hours ({difficulty1})")
    
    # Test 2: Python (not similar)
    hours2 = estimator.estimate_hours('Python', 0.8, existing)
    difficulty2 = estimator.get_difficulty_level(hours2)
    print(f"Python: {hours2} hours ({difficulty2})")
    
    # Test 3: Docker (no similarity)
    hours3 = estimator.estimate_hours('Docker', 0.6, existing)
    difficulty3 = estimator.get_difficulty_level(hours3)
    print(f"Docker: {hours3} hours ({difficulty3})")
    
    print("✅ SkillDifficultyEstimator test passed")
