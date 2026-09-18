"""
Weekly Scheduler Module
Allocates skills to weeks based on priority, dependencies, and hour constraints
Enhanced with dynamic topic-based roadmaps and video resources
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from skillTopicsMapping import SkillTopicsMapping
from videoResourcesMapping import VideoResourcesMapping


class WeeklyScheduler:
    def __init__(self):
        self.min_hours_per_skill = 5
        self.max_hours_per_skill = 20
        self.topics_mapper = SkillTopicsMapping()
        self.video_mapper = VideoResourcesMapping()
    
    def generate_schedule(
        self,
        prioritized_skills: List[Dict[str, Any]],
        available_hours_per_week: int,
        start_date: str = None,
        target_domain: str = ''
    ) -> Dict[str, Any]:
        """
        Generate weekly schedule with dynamic topic-based roadmaps

        Args:
            prioritized_skills: List of skills with priority, hours, etc.
            available_hours_per_week: Weekly hour limit
            start_date: ISO format start date
            target_domain: User's target career domain (used for video matching)

        Returns:
            Dictionary with weeklyPlan, totalWeeks, totalHours, projectedCompletionDate
        """
        if not start_date:
            start_date = datetime.now().isoformat()

        current_date = datetime.fromisoformat(start_date.split('T')[0])
        weekly_plan = []
        week_number = 1

        # Build skill roadmaps with topics
        skill_roadmaps = self._build_skill_roadmaps(prioritized_skills)
        
        # Track remaining topics for each skill
        skill_topics_remaining = {
            skill['skill']: list(skill['topics'])  # topics is now list of dicts
            for skill in skill_roadmaps
        }
        
        # Track skills in progress
        skills_in_progress = []
        skill_index = 0
        
        total_hours = sum(skill['estimated_hours'] for skill in prioritized_skills)
        
        while skill_topics_remaining and week_number <= 100:  # Safety limit
            week_data = {
                'week': week_number,
                'start_date': current_date.strftime('%Y-%m-%d'),
                'end_date': (current_date + timedelta(days=6)).strftime('%Y-%m-%d'),
                'skills': [],
                'total_hours': 0
            }
            
            hours_allocated = 0
            
            # Continue with skills in progress
            for skill_name in skills_in_progress[:]:
                if hours_allocated >= available_hours_per_week:
                    break
                
                if skill_name in skill_topics_remaining and skill_topics_remaining[skill_name]:
                    # Get next topic for this skill
                    current_topic_data = skill_topics_remaining[skill_name][0]
                    
                    # Find skill details
                    skill_details = next(
                        (s for s in skill_roadmaps if s['skill'] == skill_name),
                        {}
                    )
                    
                    hours_per_topic = skill_details.get('hours_per_topic', 5)
                    hours_available = available_hours_per_week - hours_allocated
                    hours_to_allocate = min(hours_per_topic, hours_available)
                    
                    # Get video resource — pass skill + domain for correct matching
                    video_resource = self.video_mapper.get_video_resource(
                        current_topic_data['topic'], skill_name, target_domain
                    )
                    
                    week_data['skills'].append({
                        'name': skill_name,
                        'topic': current_topic_data['topic'],
                        'objective': current_topic_data['objective'],
                        'hours': round(hours_to_allocate, 1),
                        'difficulty': skill_details.get('difficulty', 'Medium'),
                        'status': 'in-progress',
                        'topic_number': len(skill_details['topics']) - len(skill_topics_remaining[skill_name]) + 1,
                        'total_topics': len(skill_details['topics']),
                        'video_title': video_resource['title'],
                        'video_url': video_resource['url'],
                        'video_platform': video_resource.get('platform', 'YouTube')
                    })
                    
                    hours_allocated += hours_to_allocate
                    
                    # Remove completed topic
                    skill_topics_remaining[skill_name].pop(0)
                    
                    # If no more topics, remove skill from tracking
                    if not skill_topics_remaining[skill_name]:
                        del skill_topics_remaining[skill_name]
                        skills_in_progress.remove(skill_name)
                        week_data['skills'][-1]['status'] = 'complete'
            
            # Add new skills if capacity available
            while hours_allocated < available_hours_per_week and skill_index < len(skill_roadmaps):
                skill = skill_roadmaps[skill_index]
                skill_name = skill['skill']
                
                if skill_name not in skill_topics_remaining or not skill_topics_remaining[skill_name]:
                    skill_index += 1
                    continue
                
                hours_available = available_hours_per_week - hours_allocated
                
                if hours_available >= self.min_hours_per_skill:
                    # Get first topic for this skill
                    current_topic_data = skill_topics_remaining[skill_name][0]
                    hours_per_topic = skill.get('hours_per_topic', 5)
                    hours_to_allocate = min(hours_per_topic, hours_available)
                    
                    # Get video resource — pass skill + domain for correct matching
                    video_resource = self.video_mapper.get_video_resource(
                        current_topic_data['topic'], skill_name, target_domain
                    )
                    
                    week_data['skills'].append({
                        'name': skill_name,
                        'topic': current_topic_data['topic'],
                        'objective': current_topic_data['objective'],
                        'hours': round(hours_to_allocate, 1),
                        'difficulty': skill.get('difficulty', 'Medium'),
                        'status': 'started',
                        'topic_number': 1,
                        'total_topics': len(skill['topics']),
                        'video_title': video_resource['title'],
                        'video_url': video_resource['url'],
                        'video_platform': video_resource.get('platform', 'YouTube')
                    })
                    
                    hours_allocated += hours_to_allocate
                    
                    # Remove completed topic
                    skill_topics_remaining[skill_name].pop(0)
                    
                    # Add to in-progress if more topics remain
                    if skill_topics_remaining[skill_name]:
                        skills_in_progress.append(skill_name)
                    else:
                        del skill_topics_remaining[skill_name]
                        week_data['skills'][-1]['status'] = 'complete'
                    
                    skill_index += 1
                else:
                    break
            
            week_data['total_hours'] = round(hours_allocated, 1)
            weekly_plan.append(week_data)
            
            week_number += 1
            current_date += timedelta(days=7)
        
        projected_completion = current_date.strftime('%Y-%m-%d')
        
        return {
            'weeklyPlan': weekly_plan,
            'totalWeeks': len(weekly_plan),
            'totalHours': round(total_hours, 1),
            'projectedCompletionDate': projected_completion,
            'skillRoadmaps': skill_roadmaps  # Include roadmaps in response
        }
    
    def _build_skill_roadmaps(self, prioritized_skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Build detailed roadmaps for each skill with topics and objectives
        
        Args:
            prioritized_skills: List of skills with estimated hours
        
        Returns:
            List of skills with topics, objectives, and hours per topic
        """
        roadmaps = []
        
        for skill_data in prioritized_skills:
            skill_name = skill_data['skill']
            estimated_hours = skill_data['estimated_hours']
            
            # Get topics with objectives for this skill
            topics_data = self.topics_mapper.get_topics(skill_name)
            
            # Calculate hours per topic
            hours_per_topic = estimated_hours / len(topics_data) if topics_data else estimated_hours
            
            roadmaps.append({
                'skill': skill_name,
                'topics': topics_data,  # Now includes topic and objective
                'total_topics': len(topics_data),
                'estimated_hours': estimated_hours,
                'hours_per_topic': round(hours_per_topic, 1),
                'difficulty': skill_data.get('difficulty', 'Medium'),
                'priority_score': skill_data.get('priority_score', 0.5),
                'has_custom_mapping': self.topics_mapper.has_mapping(skill_name)
            })
        
        return roadmaps


if __name__ == "__main__":
    # Test
    scheduler = WeeklyScheduler()
    
    test_skills = [
        {'skill': 'Python', 'estimated_hours': 60, 'priority_score': 0.9, 'difficulty': 'Intermediate'},
        {'skill': 'React', 'estimated_hours': 50, 'priority_score': 0.8, 'difficulty': 'Intermediate'},
        {'skill': 'Docker', 'estimated_hours': 30, 'priority_score': 0.7, 'difficulty': 'Beginner'},
    ]
    
    result = scheduler.generate_schedule(test_skills, 15)
    
    print(f"Total Weeks: {result['totalWeeks']}")
    print(f"Total Hours: {result['totalHours']}")
    print(f"Completion Date: {result['projectedCompletionDate']}")
    print(f"First Week: {result['weeklyPlan'][0]}")
    print("✅ WeeklyScheduler test passed")
