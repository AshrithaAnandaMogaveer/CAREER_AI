"""
Scheduler Module
Implements time allocation algorithm and weekly schedule generation
"""

from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import math


class Scheduler:
    """Handles time allocation and schedule generation"""
    
    def __init__(self):
        # Default time estimates per skill (in hours)
        self.default_hours = {
            'beginner': 40,
            'intermediate': 30,
            'advanced': 20,
        }
    
    def estimate_skill_hours(self, skill: str, proficiency_level: str = 'beginner') -> int:
        """Estimate hours needed to learn a skill"""
        base_hours = self.default_hours.get(proficiency_level.lower(), 30)
        
        # Adjust based on skill complexity
        complexity_multipliers = {
            # High complexity
            'machine learning': 1.5,
            'deep learning': 1.8,
            'kubernetes': 1.4,
            'system design': 1.6,
            'microservices': 1.3,
            
            # Medium complexity (default = 1.0)
            
            # Low complexity
            'html': 0.5,
            'css': 0.6,
            'git': 0.7,
        }
        
        skill_lower = skill.lower()
        multiplier = complexity_multipliers.get(skill_lower, 1.0)
        
        return int(base_hours * multiplier)
    
    def allocate_time(
        self,
        prioritized_skills: List[Dict],
        available_hours_per_week: int,
        total_weeks: int = None
    ) -> List[Dict]:
        """
        Allocate time using weighted greedy scheduling
        
        Args:
            prioritized_skills: List of skills with priority scores
            available_hours_per_week: User's available hours per week
            total_weeks: Optional max weeks (auto-calculated if None)
        
        Returns:
            List of weekly schedules
        """
        if not prioritized_skills:
            return []
        
        # Calculate total hours needed
        total_hours_needed = sum(
            skill.get('estimated_hours', 30) for skill in prioritized_skills
        )
        
        # Calculate weeks needed if not provided
        if total_weeks is None:
            total_weeks = math.ceil(total_hours_needed / available_hours_per_week)
        
        # Generate weekly schedule
        weekly_schedule = []
        current_week = 1
        remaining_skills = prioritized_skills.copy()
        
        while remaining_skills and current_week <= total_weeks:
            week_hours_remaining = available_hours_per_week
            week_skills = []
            
            # Allocate skills to current week
            skills_to_remove = []
            
            for skill in remaining_skills:
                hours_needed = skill.get('hours_remaining', skill.get('estimated_hours', 30))
                
                if hours_needed <= week_hours_remaining:
                    # Skill can be completed this week
                    week_skills.append({
                        'skill': skill['skill'],
                        'hours': hours_needed,
                        'priority': skill.get('priority_score', 0),
                        'status': 'complete',
                        'progress': 100
                    })
                    week_hours_remaining -= hours_needed
                    skills_to_remove.append(skill)
                
                elif week_hours_remaining > 0:
                    # Partial allocation
                    week_skills.append({
                        'skill': skill['skill'],
                        'hours': week_hours_remaining,
                        'priority': skill.get('priority_score', 0),
                        'status': 'in_progress',
                        'progress': int((week_hours_remaining / hours_needed) * 100)
                    })
                    skill['hours_remaining'] = hours_needed - week_hours_remaining
                    week_hours_remaining = 0
                    break
            
            # Remove completed skills
            for skill in skills_to_remove:
                remaining_skills.remove(skill)
            
            # Add week to schedule
            if week_skills:
                weekly_schedule.append({
                    'week': current_week,
                    'start_date': self._get_week_start_date(current_week),
                    'end_date': self._get_week_end_date(current_week),
                    'skills': week_skills,
                    'total_hours': sum(s['hours'] for s in week_skills),
                    'utilization': int((sum(s['hours'] for s in week_skills) / available_hours_per_week) * 100)
                })
            
            current_week += 1
        
        return weekly_schedule
    
    def _get_week_start_date(self, week_number: int) -> str:
        """Calculate start date for a given week"""
        start_date = datetime.now() + timedelta(weeks=week_number - 1)
        return start_date.strftime('%Y-%m-%d')
    
    def _get_week_end_date(self, week_number: int) -> str:
        """Calculate end date for a given week"""
        end_date = datetime.now() + timedelta(weeks=week_number, days=-1)
        return end_date.strftime('%Y-%m-%d')
    
    def optimize_schedule(
        self,
        weekly_schedule: List[Dict],
        max_hours_per_week: int,
        min_hours_per_week: int = 5
    ) -> List[Dict]:
        """
        Optimize schedule to balance workload
        Ensures no week is overloaded or underutilized
        """
        optimized = []
        
        for week in weekly_schedule:
            total_hours = week['total_hours']
            
            if total_hours > max_hours_per_week:
                # Week is overloaded, redistribute
                scale_factor = max_hours_per_week / total_hours
                for skill in week['skills']:
                    skill['hours'] = int(skill['hours'] * scale_factor)
                week['total_hours'] = sum(s['hours'] for s in week['skills'])
            
            elif total_hours < min_hours_per_week and len(optimized) > 0:
                # Week is underutilized, merge with previous week if possible
                prev_week = optimized[-1]
                if prev_week['total_hours'] + total_hours <= max_hours_per_week:
                    prev_week['skills'].extend(week['skills'])
                    prev_week['total_hours'] += total_hours
                    prev_week['end_date'] = week['end_date']
                    continue
            
            optimized.append(week)
        
        # Renumber weeks
        for i, week in enumerate(optimized):
            week['week'] = i + 1
        
        return optimized
    
    def calculate_projected_completion(
        self,
        weekly_schedule: List[Dict]
    ) -> Dict:
        """Calculate projected completion date and statistics"""
        if not weekly_schedule:
            return {
                'completion_date': None,
                'total_weeks': 0,
                'total_hours': 0,
                'skills_count': 0
            }
        
        last_week = weekly_schedule[-1]
        total_hours = sum(week['total_hours'] for week in weekly_schedule)
        
        # Count unique skills
        all_skills = set()
        for week in weekly_schedule:
            for skill in week['skills']:
                all_skills.add(skill['skill'])
        
        return {
            'completion_date': last_week['end_date'],
            'total_weeks': len(weekly_schedule),
            'total_hours': total_hours,
            'skills_count': len(all_skills),
            'average_hours_per_week': total_hours / len(weekly_schedule) if weekly_schedule else 0
        }
    
    def generate_milestone_schedule(
        self,
        weekly_schedule: List[Dict],
        milestone_interval: int = 4
    ) -> List[Dict]:
        """
        Generate milestone checkpoints every N weeks
        """
        milestones = []
        
        for i in range(0, len(weekly_schedule), milestone_interval):
            end_week = min(i + milestone_interval, len(weekly_schedule))
            weeks_group = weekly_schedule[i:end_week]
            
            # Collect skills in this milestone
            milestone_skills = set()
            for week in weeks_group:
                for skill in week['skills']:
                    if skill['status'] == 'complete':
                        milestone_skills.add(skill['skill'])
            
            milestones.append({
                'milestone': len(milestones) + 1,
                'weeks': f"{weeks_group[0]['week']}-{weeks_group[-1]['week']}",
                'start_date': weeks_group[0]['start_date'],
                'end_date': weeks_group[-1]['end_date'],
                'skills_completed': list(milestone_skills),
                'total_hours': sum(week['total_hours'] for week in weeks_group)
            })
        
        return milestones
    
    def recalculate_schedule(
        self,
        original_schedule: List[Dict],
        completed_skills: List[str],
        current_week: int
    ) -> List[Dict]:
        """
        Recalculate remaining schedule based on progress
        Adaptive rescheduling when user completes skills
        """
        # Filter out completed skills from remaining weeks
        remaining_schedule = []
        
        for week in original_schedule:
            if week['week'] < current_week:
                # Past weeks, keep as is
                remaining_schedule.append(week)
            else:
                # Future weeks, filter completed skills
                remaining_skills = [
                    skill for skill in week['skills']
                    if skill['skill'] not in completed_skills
                ]
                
                if remaining_skills:
                    week_copy = week.copy()
                    week_copy['skills'] = remaining_skills
                    week_copy['total_hours'] = sum(s['hours'] for s in remaining_skills)
                    remaining_schedule.append(week_copy)
        
        # Renumber weeks starting from current week
        for i, week in enumerate(remaining_schedule):
            if week['week'] >= current_week:
                week['week'] = current_week + i
        
        return remaining_schedule
