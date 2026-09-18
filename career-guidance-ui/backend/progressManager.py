"""
Progress Manager Module
Handles skill progress tracking, completion calculation, and history storage
"""

import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
from collections import defaultdict


class ProgressManager:
    def __init__(self):
        # In-memory storage (replace with database in production)
        self.progress_history = defaultdict(list)
        self.user_progress = {}
    
    def update_progress(
        self,
        user_id: str,
        week: int,
        skill: str,
        completion_percentage: float,
        date: str,
        routine_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Update skill progress and recalculate metrics
        
        Args:
            user_id: User identifier
            week: Current week number
            skill: Skill name
            completion_percentage: Completion percentage (0-100)
            date: ISO format date
            routine_data: Current routine information
        
        Returns:
            Dictionary with updated progress metrics
        """
        try:
            # Validate inputs
            if not 0 <= completion_percentage <= 100:
                return {
                    'success': False,
                    'message': 'Completion percentage must be between 0 and 100'
                }
            
            if not routine_data:
                return {
                    'success': False,
                    'message': 'Routine data is required'
                }
            
            # Initialize user progress if not exists
            if user_id not in self.user_progress:
                self.user_progress[user_id] = {}
            
            # Update skill progress
            self.user_progress[user_id][skill] = {
                'completion_percentage': completion_percentage,
                'week': week,
                'last_updated': date
            }
            
            # Store history for graphing
            self._store_history(user_id, skill, completion_percentage, date)
            
            # Algorithm 1: Calculate overall completion
            overall_completion = self._calculate_overall_completion(
                user_id,
                routine_data
            )
            
            # Algorithm 2: Calculate completed hours
            completed_hours = self._calculate_completed_hours(
                user_id,
                routine_data
            )
            
            # Algorithm 3: Recalculate projected completion
            projected_completion = self._recalculate_projected_completion(
                user_id,
                routine_data,
                overall_completion
            )
            
            # Get skills summary
            skills_summary = self._get_skills_summary(user_id, routine_data)
            
            # Build response
            return {
                'success': True,
                'progress_metrics': {
                    'overall_completion': round(overall_completion, 2),
                    'completed_hours': round(completed_hours, 2),
                    'total_hours': routine_data.get('projection', {}).get('total_hours', 0),
                    'projected_completion_date': projected_completion['date'],
                    'weeks_remaining': projected_completion['weeks_remaining'],
                    'on_track': projected_completion['on_track'],
                    'skills_completed': skills_summary['completed'],
                    'skills_in_progress': skills_summary['in_progress'],
                    'skills_not_started': skills_summary['not_started'],
                    'total_skills': skills_summary['total'],
                    'current_week': week,
                    'last_updated': date
                },
                'skill_progress': self.user_progress[user_id],
                'message': f'Progress updated for {skill}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Progress update failed: {str(e)}'
            }
    
    def _calculate_overall_completion(
        self,
        user_id: str,
        routine_data: Dict[str, Any]
    ) -> float:
        """
        Algorithm: Calculate overall completion
        Formula: totalCompletedHours / totalHours × 100
        """
        prioritized_skills = routine_data.get('prioritized_skills', [])
        if not prioritized_skills:
            return 0.0
        
        total_hours = 0.0
        completed_hours = 0.0
        
        for skill_data in prioritized_skills:
            skill_name = skill_data.get('skill', '')
            estimated_hours = skill_data.get('estimated_hours', 0)
            total_hours += estimated_hours
            
            # Get user's progress for this skill
            if user_id in self.user_progress and skill_name in self.user_progress[user_id]:
                completion_pct = self.user_progress[user_id][skill_name]['completion_percentage']
                completed_hours += (estimated_hours * completion_pct / 100)
        
        if total_hours == 0:
            return 0.0
        
        return (completed_hours / total_hours) * 100
    
    def _calculate_completed_hours(
        self,
        user_id: str,
        routine_data: Dict[str, Any]
    ) -> float:
        """
        Calculate total completed hours
        """
        prioritized_skills = routine_data.get('prioritized_skills', [])
        completed_hours = 0.0
        
        for skill_data in prioritized_skills:
            skill_name = skill_data.get('skill', '')
            estimated_hours = skill_data.get('estimated_hours', 0)
            
            if user_id in self.user_progress and skill_name in self.user_progress[user_id]:
                completion_pct = self.user_progress[user_id][skill_name]['completion_percentage']
                completed_hours += (estimated_hours * completion_pct / 100)
        
        return completed_hours
    
    def _recalculate_projected_completion(
        self,
        user_id: str,
        routine_data: Dict[str, Any],
        overall_completion: float
    ) -> Dict[str, Any]:
        """
        Algorithm: Recalculate projected completion date
        Based on current progress rate
        """
        original_projection = routine_data.get('projection', {})
        total_weeks = original_projection.get('total_weeks', 0)
        total_hours = original_projection.get('total_hours', 0)
        hours_per_week = routine_data.get('metadata', {}).get('available_hours_per_week', 10)
        
        if overall_completion >= 100:
            return {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'weeks_remaining': 0,
                'on_track': True
            }
        
        # Calculate remaining hours
        remaining_percentage = 100 - overall_completion
        remaining_hours = (total_hours * remaining_percentage / 100)
        
        # Calculate weeks needed at current pace
        weeks_needed = remaining_hours / hours_per_week if hours_per_week > 0 else total_weeks
        
        # Calculate new completion date
        new_completion_date = datetime.now() + timedelta(weeks=weeks_needed)
        
        # Check if on track
        original_date_str = original_projection.get('completion_date', '')
        on_track = True
        if original_date_str:
            try:
                original_date = datetime.fromisoformat(original_date_str.split('T')[0])
                on_track = new_completion_date <= original_date
            except:
                pass
        
        return {
            'date': new_completion_date.strftime('%Y-%m-%d'),
            'weeks_remaining': int(weeks_needed) + 1,
            'on_track': on_track
        }
    
    def _get_skills_summary(
        self,
        user_id: str,
        routine_data: Dict[str, Any]
    ) -> Dict[str, int]:
        """
        Get summary of skills by status
        """
        prioritized_skills = routine_data.get('prioritized_skills', [])
        
        completed = 0
        in_progress = 0
        not_started = 0
        
        for skill_data in prioritized_skills:
            skill_name = skill_data.get('skill', '')
            
            if user_id in self.user_progress and skill_name in self.user_progress[user_id]:
                completion_pct = self.user_progress[user_id][skill_name]['completion_percentage']
                if completion_pct >= 100:
                    completed += 1
                elif completion_pct > 0:
                    in_progress += 1
                else:
                    not_started += 1
            else:
                not_started += 1
        
        return {
            'completed': completed,
            'in_progress': in_progress,
            'not_started': not_started,
            'total': len(prioritized_skills)
        }
    
    def _store_history(
        self,
        user_id: str,
        skill: str,
        completion_percentage: float,
        date: str
    ):
        """
        Store progress history for graphing
        """
        history_key = f"{user_id}:{skill}"
        
        self.progress_history[history_key].append({
            'date': date,
            'completion_percentage': completion_percentage,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 100 entries per skill
        if len(self.progress_history[history_key]) > 100:
            self.progress_history[history_key] = self.progress_history[history_key][-100:]
    
    def get_progress_history(
        self,
        user_id: str,
        skill: str = None
    ) -> Dict[str, Any]:
        """
        Get progress history for graphing
        
        Args:
            user_id: User identifier
            skill: Specific skill (optional, returns all if None)
        
        Returns:
            Dictionary with history data
        """
        if skill:
            history_key = f"{user_id}:{skill}"
            return {
                'success': True,
                'skill': skill,
                'history': self.progress_history.get(history_key, [])
            }
        else:
            # Return all skills history
            all_history = {}
            for key, history in self.progress_history.items():
                if key.startswith(f"{user_id}:"):
                    skill_name = key.split(':', 1)[1]
                    all_history[skill_name] = history
            
            return {
                'success': True,
                'history': all_history
            }
    
    def get_evolution_data(
        self,
        user_id: str,
        routine_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Get evolution data for graphing over time
        
        Returns:
            Dictionary with daily and monthly progress data
        """
        try:
            if user_id not in self.user_progress:
                return {
                    'success': True,
                    'evolution_summary': {
                        'daily_progress': [],
                        'monthly_progress': [],
                        'overall_completion': 0,
                        'skills_completed': 0,
                        'total_skills': 0,
                        'motivation_message': 'Start tracking your progress to see your evolution!'
                    }
                }
            
            # Calculate current metrics
            overall_completion = 0
            skills_completed = 0
            total_skills = 0
            
            if routine_data:
                overall_completion = self._calculate_overall_completion(user_id, routine_data)
                skills_summary = self._get_skills_summary(user_id, routine_data)
                skills_completed = skills_summary['completed']
                total_skills = skills_summary['total']
            
            # Generate daily progress (last 30 days)
            daily_progress = self._generate_daily_progress(user_id)
            
            # Generate monthly progress (last 6 months)
            monthly_progress = self._generate_monthly_progress(user_id)
            
            # Generate motivation message
            motivation_message = self._generate_motivation_message(overall_completion)
            
            return {
                'success': True,
                'evolution_summary': {
                    'daily_progress': daily_progress,
                    'monthly_progress': monthly_progress,
                    'overall_completion': round(overall_completion, 2),
                    'skills_completed': skills_completed,
                    'total_skills': total_skills,
                    'remaining_skills': total_skills - skills_completed,
                    'motivation_message': motivation_message,
                    'last_updated': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Evolution data fetch failed: {str(e)}'
            }
    
    def _generate_daily_progress(self, user_id: str) -> List[Dict]:
        """Generate daily progress data for last 30 days"""
        daily_data = []
        
        # Aggregate all skill history by date
        date_completion = defaultdict(list)
        
        for key, history in self.progress_history.items():
            if key.startswith(f"{user_id}:"):
                for entry in history:
                    date = entry['date'].split('T')[0]  # Get date only
                    date_completion[date].append(entry['completion_percentage'])
        
        # Calculate average completion per day
        for date, completions in sorted(date_completion.items())[-30:]:
            avg_completion = sum(completions) / len(completions) if completions else 0
            daily_data.append({
                'date': date,
                'completion': round(avg_completion, 2)
            })
        
        return daily_data
    
    def _generate_monthly_progress(self, user_id: str) -> List[Dict]:
        """Generate monthly progress data for last 6 months"""
        monthly_data = []
        
        # Aggregate by month
        month_completion = defaultdict(list)
        
        for key, history in self.progress_history.items():
            if key.startswith(f"{user_id}:"):
                for entry in history:
                    date = entry['date'].split('T')[0]
                    month = date[:7]  # YYYY-MM
                    month_completion[month].append(entry['completion_percentage'])
        
        # Calculate average completion per month
        for month, completions in sorted(month_completion.items())[-6:]:
            avg_completion = sum(completions) / len(completions) if completions else 0
            monthly_data.append({
                'month': month,
                'completion': round(avg_completion, 2)
            })
        
        return monthly_data
    
    def _generate_motivation_message(self, completion: float) -> str:
        """Generate motivational message based on completion"""
        if completion >= 100:
            return "🎉 Congratulations! You've completed your routine! Time to celebrate your achievement!"
        elif completion >= 75:
            return "🚀 Amazing progress! You're in the final stretch. Keep pushing forward!"
        elif completion >= 50:
            return "💪 Great work! You're halfway there. The momentum is building!"
        elif completion >= 25:
            return "🌟 Good start! You're building solid foundations. Keep it up!"
        elif completion > 0:
            return "🎯 Every journey begins with a single step. You've started - that's what matters!"
        else:
            return "📚 Ready to begin your learning journey? Update your progress to track your growth!"


if __name__ == "__main__":
    # Test
    manager = ProgressManager()
    
    # Test routine data
    routine_data = {
        'prioritized_skills': [
            {'skill': 'Python', 'estimated_hours': 60},
            {'skill': 'React', 'estimated_hours': 50},
            {'skill': 'Docker', 'estimated_hours': 30}
        ],
        'projection': {
            'total_weeks': 10,
            'total_hours': 140,
            'completion_date': '2026-05-01'
        },
        'metadata': {
            'available_hours_per_week': 15
        }
    }
    
    # Test 1: Update progress
    result1 = manager.update_progress(
        'user123',
        1,
        'Python',
        50.0,
        '2026-02-28',
        routine_data
    )
    print(f"Test 1 - Update Progress: {result1['success']}")
    print(f"Overall Completion: {result1['progress_metrics']['overall_completion']}%")
    
    # Test 2: Update another skill
    result2 = manager.update_progress(
        'user123',
        2,
        'React',
        75.0,
        '2026-03-07',
        routine_data
    )
    print(f"Test 2 - Update Progress: {result2['success']}")
    print(f"Overall Completion: {result2['progress_metrics']['overall_completion']}%")
    
    # Test 3: Get evolution data
    result3 = manager.get_evolution_data('user123', routine_data)
    print(f"Test 3 - Evolution Data: {result3['success']}")
    print(f"Skills Completed: {result3['evolution_summary']['skills_completed']}")
    
    print("✅ ProgressManager test passed")
