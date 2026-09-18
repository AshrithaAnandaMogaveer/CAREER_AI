"""
Routine Engine Core Module
Main orchestrator for routine generation with all algorithms
"""

from typing import Dict, List, Any
from datetime import datetime
from fileParser import FileParser
from dependencyGraph import DependencyGraph
from weeklyScheduler import WeeklyScheduler
from skillDifficultyEstimator import SkillDifficultyEstimator


class RoutineEngineCore:
    def __init__(self):
        self.file_parser = FileParser()
        self.dependency_graph = DependencyGraph()
        self.scheduler = WeeklyScheduler()
        self.difficulty_estimator = SkillDifficultyEstimator()
        
        # Industry weights for different domains
        self.industry_weights = {
            'Software Development': {
                'Python': 0.9, 'JavaScript': 0.9, 'React': 0.8, 'Node.js': 0.8,
                'Git': 0.8, 'SQL': 0.7, 'Docker': 0.7, 'AWS': 0.7
            },
            'Data Science': {
                'Python': 0.9, 'SQL': 0.9, 'Machine Learning': 0.9,
                'Statistics': 0.9, 'Pandas': 0.8, 'NumPy': 0.8
            },
            'Web Development': {
                'HTML': 0.9, 'CSS': 0.9, 'JavaScript': 0.9, 'React': 0.8,
                'Node.js': 0.8, 'MongoDB': 0.7, 'REST API': 0.8
            },
            'DevOps': {
                'Linux': 0.9, 'Docker': 0.9, 'Kubernetes': 0.8, 'CI/CD': 0.9,
                'AWS': 0.8, 'Terraform': 0.7, 'Git': 0.8
            }
        }
    
    def generate_routine(
        self,
        file_path: str,
        file_type: str,
        available_hours_per_week: int = 10,
        user_domain: str = ''
    ) -> Dict[str, Any]:
        """
        Main routine generation function
        
        Args:
            file_path: Path to uploaded analysis file
            file_type: 'json', 'pdf', or 'docx'
            available_hours_per_week: Weekly study hours
            user_domain: Domain from user's profile (overrides file-parsed domain)
        
        Returns:
            Complete routine with weekly plan
        """
        try:
            # Step 1: Parse file — pass user_domain so domain-specific skills are used
            parsed_data = self.file_parser.parse_file(file_path, file_type, user_domain)
            
            missing_skills = parsed_data['missingSkills']
            priority_scores = parsed_data['priorityScores']
            gap_severity = parsed_data['gapSeverity']
            existing_skills = parsed_data.get('existingSkills', [])

            # Use user's profile domain if provided, otherwise fall back to file-parsed domain
            target_domain = user_domain if user_domain else parsed_data.get('targetDomain', 'General')
            
            if not missing_skills:
                return {
                    'success': False,
                    'message': 'No missing skills found in the analysis report'
                }
            
            # Step 2: Skill Prioritization
            prioritized_skills = self._prioritize_skills(
                missing_skills,
                priority_scores,
                gap_severity,
                target_domain
            )
            
            # Step 3: Dependency Graph & Topological Sort
            sorted_skills = self.dependency_graph.topological_sort(
                [s['skill'] for s in prioritized_skills]
            )
            
            # Reorder prioritized_skills based on topological sort
            # Only include skills that were in the original list
            skill_map = {s['skill'].lower(): s for s in prioritized_skills}
            prioritized_skills = [
                skill_map[skill] 
                for skill in sorted_skills 
                if skill.lower() in skill_map
            ]
            
            # Step 4: Estimate difficulty and hours
            for skill_data in prioritized_skills:
                skill = skill_data['skill']
                severity = gap_severity.get(skill, 0.5)
                
                estimated_hours = self.difficulty_estimator.estimate_hours(
                    skill,
                    severity,
                    existing_skills
                )
                
                difficulty_level = self.difficulty_estimator.get_difficulty_level(estimated_hours)
                
                skill_data['estimated_hours'] = estimated_hours
                skill_data['difficulty'] = difficulty_level
            
            # Step 5: Weekly Scheduling
            schedule_result = self.scheduler.generate_schedule(
                prioritized_skills,
                available_hours_per_week,
                target_domain=target_domain
            )
            
            # Build final response
            return {
                'success': True,
                'routine': {
                    'target_domain': target_domain,
                    'readiness_score': parsed_data.get('readinessScore', 50),
                    'prioritized_skills': prioritized_skills,
                    'skill_roadmaps': schedule_result.get('skillRoadmaps', []),  # Include detailed roadmaps
                    'skill_completion': self._build_skill_completion(prioritized_skills),  # Add completion tracking
                    'weekly_schedule': schedule_result['weeklyPlan'],
                    'projection': {
                        'total_weeks': schedule_result['totalWeeks'],
                        'total_hours': schedule_result['totalHours'],
                        'completion_date': schedule_result['projectedCompletionDate'],
                        'skills_count': len(prioritized_skills)
                    },
                    'metadata': {
                        'available_hours_per_week': available_hours_per_week,
                        'generated_at': datetime.now().isoformat(),
                        'dynamic_topics_enabled': True,
                        'completion_tracking_enabled': True
                    }
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Routine generation failed: {str(e)}'
            }
    
    def _prioritize_skills(
        self,
        skills: List[str],
        priority_scores: Dict[str, float],
        gap_severity: Dict[str, float],
        target_domain: str
    ) -> List[Dict[str, Any]]:
        """
        Algorithm: Skill Prioritization
        Formula: priorityScore = (skillPriority × 0.5) + (gapSeverity × 0.3) + (industryWeight × 0.2)
        """
        industry_weights = self.industry_weights.get(target_domain, {})
        
        prioritized = []
        
        for skill in skills:
            skill_priority = priority_scores.get(skill, 0.5)
            severity = gap_severity.get(skill, 0.5)
            industry_weight = industry_weights.get(skill, 0.5)
            
            # Apply formula
            final_priority = (
                skill_priority * 0.5 +
                severity * 0.3 +
                industry_weight * 0.2
            )
            
            # Determine domain relevance
            if industry_weight >= 0.8:
                relevance = 'critical'
            elif industry_weight >= 0.6:
                relevance = 'high'
            elif industry_weight >= 0.4:
                relevance = 'medium'
            else:
                relevance = 'low'
            
            prioritized.append({
                'skill': skill,
                'priority_score': round(final_priority, 3),
                'skill_priority': skill_priority,
                'gap_severity': severity,
                'industry_weight': industry_weight,
                'domain_relevance': relevance
            })
        
        # Sort by priority (descending)
        prioritized.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return prioritized
    
    def _build_skill_completion(
        self,
        prioritized_skills: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Build skill completion tracking data
        
        Args:
            prioritized_skills: List of skills with topics
        
        Returns:
            List of skills with completion tracking
        """
        from skillTopicsMapping import SkillTopicsMapping
        
        topics_mapper = SkillTopicsMapping()
        completion_data = []
        
        for skill_data in prioritized_skills:
            skill_name = skill_data['skill']
            
            # Get topics for this skill
            topics = topics_mapper.get_topics(skill_name)
            total_topics = len(topics)
            
            # Initially, no topics are completed
            completed_topics = 0
            
            # Calculate completion percentage
            completion_percentage = (completed_topics / total_topics * 100) if total_topics > 0 else 0
            
            # Determine status based on completion
            if completion_percentage >= 80:
                status = 'Achieved'
            elif completion_percentage >= 50:
                status = 'In Progress'
            elif completion_percentage > 0:
                status = 'Started'
            else:
                status = 'Not Started'
            
            completion_data.append({
                'skill_name': skill_name,
                'total_topics': total_topics,
                'completed_topics': completed_topics,
                'completion_percentage': round(completion_percentage, 1),
                'status': status,
                'priority_score': skill_data.get('priority_score', 0.5),
                'difficulty': skill_data.get('difficulty', 'Medium')
            })
        
        return completion_data


if __name__ == "__main__":
    import json
    import tempfile
    
    # Test
    engine = RoutineEngineCore()
    
    # Create test JSON file
    test_data = {
        'missingSkills': ['Python', 'React', 'Docker', 'Git'],
        'priorityScores': {
            'Python': 0.9,
            'React': 0.8,
            'Docker': 0.7,
            'Git': 0.8
        },
        'gapSeverity': {
            'Python': 0.8,
            'React': 0.7,
            'Docker': 0.6,
            'Git': 0.5
        },
        'targetDomain': 'Software Development',
        'readinessScore': 45,
        'extractedSkills': ['JavaScript', 'HTML', 'CSS']
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name
    
    result = engine.generate_routine(temp_path, 'json', 15)
    
    if result['success']:
        routine = result['routine']
        print(f"✅ Routine generated successfully!")
        print(f"Target Domain: {routine['target_domain']}")
        print(f"Total Weeks: {routine['projection']['total_weeks']}")
        print(f"Total Hours: {routine['projection']['total_hours']}")
        print(f"Skills: {len(routine['prioritized_skills'])}")
        print(f"First Week: {routine['weekly_schedule'][0]}")
    else:
        print(f"❌ Failed: {result['message']}")
    
    import os
    os.unlink(temp_path)
