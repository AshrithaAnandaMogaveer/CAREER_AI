"""
Routine Engine Module
Main orchestrator for routine build functionality
Implements skill prioritization and integrates all algorithms
"""

from typing import List, Dict, Optional
from dependencyGraph import DependencyGraph
from scheduler import Scheduler
from progressTracker import ProgressTracker


# Domain-specific skill weights
DOMAIN_SKILL_WEIGHTS = {
    'Software Development': {
        'python': 0.9, 'javascript': 0.9,
        'git': 0.8, 'sql': 0.8, 'rest api': 0.8,
        'docker': 0.7, 'kubernetes': 0.6, 'aws': 0.7,
        'react': 0.8, 'node.js': 0.8, 'typescript': 0.7,
        'java': 0.5  # relevant for Android/backend Java, not general
    },
    'Data Science': {
        'python': 0.95, 'sql': 0.9, 'statistics': 0.9,
        'machine learning': 0.95, 'pandas': 0.9, 'numpy': 0.9,
        'data visualization': 0.8, 'deep learning': 0.7,
        'tensorflow': 0.7, 'pytorch': 0.7
    },
    'Machine Learning': {
        'python': 0.95, 'machine learning': 0.95, 'deep learning': 0.9,
        'tensorflow': 0.85, 'pytorch': 0.85, 'statistics': 0.9,
        'linear algebra': 0.85, 'calculus': 0.7, 'nlp': 0.8,
        'computer vision': 0.8
    },
    'Web Development': {
        'html': 0.9, 'css': 0.9, 'javascript': 0.95,
        'react': 0.9, 'node.js': 0.85, 'rest api': 0.8,
        'mongodb': 0.7, 'postgresql': 0.7, 'git': 0.8,
        'responsive design': 0.8
    },
    'DevOps': {
        'linux': 0.9, 'docker': 0.95, 'kubernetes': 0.9,
        'ci/cd': 0.9, 'jenkins': 0.7, 'terraform': 0.8,
        'ansible': 0.7, 'aws': 0.85, 'monitoring': 0.8,
        'git': 0.8
    },
    'Mobile Development': {
        'java': 0.8, 'kotlin': 0.8, 'swift': 0.8,
        'react native': 0.85, 'flutter': 0.85,
        'rest api': 0.8, 'mobile development': 0.9,
        'ui/ux': 0.7, 'git': 0.7
    },
    'Cybersecurity': {
        'networking': 0.95, 'linux': 0.9, 'cybersecurity': 0.95,
        'penetration testing': 0.9, 'encryption': 0.85,
        'python': 0.8, 'bash': 0.8, 'security auditing': 0.85
    },
    'Cloud Computing': {
        'aws': 0.95, 'azure': 0.9, 'gcp': 0.9,
        'docker': 0.85, 'kubernetes': 0.85, 'linux': 0.8,
        'networking': 0.8, 'terraform': 0.8, 'serverless': 0.7
    },
    'UI/UX Design': {
        'ui/ux': 0.95, 'figma': 0.9, 'sketch': 0.8,
        'wireframing': 0.85, 'prototyping': 0.85,
        'user research': 0.8, 'html': 0.7, 'css': 0.7,
        'responsive design': 0.8
    },
    'Product Management': {
        'product strategy': 0.95, 'roadmapping': 0.9, 'agile': 0.9,
        'scrum': 0.85, 'user stories': 0.85, 'sql': 0.7,
        'data analysis': 0.8, 'stakeholder management': 0.9
    }
}


class RoutineEngine:
    """Main routine build engine"""
    
    def __init__(self):
        self.dependency_graph = DependencyGraph()
        self.scheduler = Scheduler()
        self.progress_tracker = ProgressTracker()
    
    def calculate_priority_score(
        self,
        skill: str,
        target_domain: str,
        gap_severity: float,
        current_skills: List[str] = None
    ) -> float:
        """
        Calculate priority score for a skill
        
        Formula:
        priorityScore = (industryWeight × 0.4) + (gapSeverity × 0.4) + (domainRelevance × 0.2)
        """
        # Get industry weight (domain relevance)
        domain_weights = DOMAIN_SKILL_WEIGHTS.get(target_domain, {})
        industry_weight = domain_weights.get(skill.lower(), 0.5)  # Default 0.5
        
        # Gap severity (0-1 scale)
        # Higher severity = more critical to learn
        normalized_gap = min(gap_severity / 100, 1.0)
        
        # Domain relevance (check if skill is in domain's top skills)
        domain_relevance = 1.0 if skill.lower() in domain_weights else 0.5
        
        # Calculate weighted priority
        priority_score = (
            (industry_weight * 0.4) +
            (normalized_gap * 0.4) +
            (domain_relevance * 0.2)
        )
        
        # Boost priority if skill is a prerequisite for other missing skills
        if current_skills:
            prerequisite_boost = self._calculate_prerequisite_boost(skill, current_skills)
            priority_score += prerequisite_boost
        
        return min(priority_score, 1.0)
    
    def _calculate_prerequisite_boost(self, skill: str, current_skills: List[str]) -> float:
        """Calculate boost if skill is prerequisite for others"""
        # Check how many skills depend on this one
        dependent_count = 0
        for other_skill in current_skills:
            deps = self.dependency_graph.get_dependencies(other_skill)
            if skill.lower() in deps:
                dependent_count += 1
        
        # Boost by 0.05 per dependent skill (max 0.2)
        return min(dependent_count * 0.05, 0.2)
    
    def prioritize_skills(
        self,
        missing_skills: List[str],
        target_domain: str,
        skill_gap_scores: Dict[str, float] = None,
        current_skills: List[str] = None
    ) -> List[Dict]:
        """
        Prioritize skills using algorithm
        Returns sorted list with priority scores
        """
        if skill_gap_scores is None:
            skill_gap_scores = {}
        
        prioritized = []
        
        for skill in missing_skills:
            gap_severity = skill_gap_scores.get(skill, 50.0)  # Default 50%
            
            priority_score = self.calculate_priority_score(
                skill,
                target_domain,
                gap_severity,
                current_skills
            )
            
            # Estimate learning time
            estimated_hours = self.scheduler.estimate_skill_hours(skill)
            
            prioritized.append({
                'skill': skill,
                'priority_score': round(priority_score, 3),
                'gap_severity': gap_severity,
                'estimated_hours': estimated_hours,
                'domain_relevance': self._get_domain_relevance(skill, target_domain),
                'prerequisites': self.dependency_graph.get_dependencies(skill)
            })
        
        # Sort by priority score (descending)
        prioritized.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return prioritized
    
    def _get_domain_relevance(self, skill: str, target_domain: str) -> str:
        """Get relevance level for skill in domain"""
        domain_weights = DOMAIN_SKILL_WEIGHTS.get(target_domain, {})
        weight = domain_weights.get(skill.lower(), 0)
        
        if weight >= 0.9:
            return 'critical'
        elif weight >= 0.7:
            return 'high'
        elif weight >= 0.5:
            return 'medium'
        else:
            return 'low'
    
    def build_routine(
        self,
        missing_skills: List[str],
        target_domain: str,
        available_hours_per_week: int,
        skill_gap_scores: Dict[str, float] = None,
        current_skills: List[str] = None,
        skill_proficiency_levels: Dict[str, str] = None
    ) -> Dict:
        """
        Main routine build function
        Orchestrates all algorithms to generate complete routine
        """
        if not missing_skills:
            return self._empty_routine()
        
        # Step 1: Prioritize skills
        prioritized_skills = self.prioritize_skills(
            missing_skills,
            target_domain,
            skill_gap_scores,
            current_skills
        )
        
        # Step 2: Apply dependency ordering
        skill_names = [s['skill'] for s in prioritized_skills]
        ordered_skills = self.dependency_graph.topological_sort(skill_names)
        
        # Reorder prioritized skills based on dependencies
        ordered_prioritized = []
        for skill_name in ordered_skills:
            skill_data = next((s for s in prioritized_skills if s['skill'] == skill_name), None)
            if skill_data:
                ordered_prioritized.append(skill_data)
        
        # Step 3: Get learning path with levels
        learning_path = self.dependency_graph.get_learning_path(
            skill_names,
            current_skills or []
        )
        
        # Step 4: Generate weekly schedule
        weekly_schedule = self.scheduler.allocate_time(
            ordered_prioritized,
            available_hours_per_week
        )
        
        # Step 5: Optimize schedule
        optimized_schedule = self.scheduler.optimize_schedule(
            weekly_schedule,
            available_hours_per_week
        )
        
        # Step 6: Calculate projections
        projection = self.scheduler.calculate_projected_completion(optimized_schedule)
        
        # Step 7: Generate milestones
        milestones = self.scheduler.generate_milestone_schedule(optimized_schedule)
        
        # Step 8: Initialize progress tracking
        skills_progress = self._initialize_progress_tracking(ordered_prioritized, optimized_schedule)
        
        # Step 9: Calculate initial metrics
        progress_metrics = self.progress_tracker.calculate_progress_metrics(
            skills_progress,
            optimized_schedule,
            current_week=1
        )
        
        return {
            'prioritized_skills': ordered_prioritized,
            'learning_path': learning_path,
            'weekly_schedule': optimized_schedule,
            'milestones': milestones,
            'projection': projection,
            'progress_metrics': progress_metrics,
            'lagging_skills': [],  # Empty initially
            'recommendations': self._generate_recommendations(ordered_prioritized, target_domain)
        }
    
    def _initialize_progress_tracking(
        self,
        prioritized_skills: List[Dict],
        weekly_schedule: List[Dict]
    ) -> List[Dict]:
        """Initialize progress tracking data"""
        progress = []
        
        for skill in prioritized_skills:
            # Find which week this skill appears in
            planned_week = None
            for week in weekly_schedule:
                if any(s['skill'] == skill['skill'] for s in week['skills']):
                    planned_week = week['week']
                    break
            
            progress.append({
                'skill': skill['skill'],
                'priority_score': skill['priority_score'],
                'hours_planned': skill['estimated_hours'],
                'hours_completed': 0,
                'completion_percentage': 0,
                'planned_week': planned_week or 1,
                'duration_weeks': 1,
                'progress_updates': []
            })
        
        return progress
    
    def _generate_recommendations(
        self,
        prioritized_skills: List[Dict],
        target_domain: str
    ) -> List[str]:
        """Generate learning recommendations"""
        recommendations = []
        
        # Top priority skills
        top_skills = prioritized_skills[:3]
        if top_skills:
            skills_str = ', '.join([s['skill'] for s in top_skills])
            recommendations.append(f"🎯 Focus on these high-priority skills first: {skills_str}")
        
        # Prerequisites check
        skills_with_prereqs = [s for s in prioritized_skills if s.get('prerequisites')]
        if skills_with_prereqs:
            recommendations.append(f"📚 {len(skills_with_prereqs)} skills have prerequisites. Follow the learning path order.")
        
        # Time commitment
        total_hours = sum(s['estimated_hours'] for s in prioritized_skills)
        recommendations.append(f"⏱️ Total estimated time: {total_hours} hours across all skills")
        
        # Domain-specific advice
        if target_domain == 'Software Development':
            recommendations.append("💻 Build projects while learning to reinforce concepts")
        elif target_domain == 'Data Science':
            recommendations.append("📊 Practice with real datasets from Kaggle or UCI ML Repository")
        elif target_domain == 'Machine Learning':
            recommendations.append("🤖 Implement algorithms from scratch before using libraries")
        
        return recommendations
    
    def _empty_routine(self) -> Dict:
        """Return empty routine structure"""
        return {
            'prioritized_skills': [],
            'learning_path': [],
            'weekly_schedule': [],
            'milestones': [],
            'projection': {
                'completion_date': None,
                'total_weeks': 0,
                'total_hours': 0,
                'skills_count': 0
            },
            'progress_metrics': self.progress_tracker._empty_metrics(),
            'lagging_skills': [],
            'recommendations': ['No missing skills identified. Great job!']
        }
    
    def update_progress(
        self,
        routine_data: Dict,
        skill: str,
        hours_completed: float,
        current_week: int
    ) -> Dict:
        """
        Update progress for a skill and recalculate
        Implements adaptive recalculation
        """
        skills_progress = routine_data.get('skills_progress', [])
        
        # Find and update skill
        for skill_progress in skills_progress:
            if skill_progress['skill'] == skill:
                skill_progress['hours_completed'] += hours_completed
                skill_progress['completion_percentage'] = self.progress_tracker.calculate_skill_completion(
                    skill,
                    skill_progress['hours_completed'],
                    skill_progress['hours_planned']
                )
                
                # Add progress update
                skill_progress['progress_updates'].append({
                    'week': current_week,
                    'hours': hours_completed,
                    'completion': skill_progress['completion_percentage'],
                    'timestamp': datetime.now().isoformat()
                })
                
                # Recalculate priority (adaptive)
                completion_ratio = skill_progress['completion_percentage'] / 100
                skill_progress['priority_score'] *= (1 - completion_ratio)
                break
        
        # Recalculate metrics
        weekly_schedule = routine_data.get('weekly_schedule', [])
        progress_metrics = self.progress_tracker.calculate_progress_metrics(
            skills_progress,
            weekly_schedule,
            current_week
        )
        
        # Detect lagging skills
        total_weeks = len(weekly_schedule)
        lagging_skills = self.progress_tracker.detect_lagging_skills(
            skills_progress,
            current_week,
            total_weeks
        )
        
        # Update routine data
        routine_data['skills_progress'] = skills_progress
        routine_data['progress_metrics'] = progress_metrics
        routine_data['lagging_skills'] = lagging_skills
        
        return routine_data
