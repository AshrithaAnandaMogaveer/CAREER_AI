"""
Evolution Tracker Module
Computes progress evolution, growth rates, and excellence metrics
"""

import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
from collections import defaultdict


class EvolutionTracker:
    def __init__(self, progress_manager=None):
        self.progress_manager = progress_manager
        self.excellence_threshold = 85.0  # 85% mastery threshold
    
    def compute_evolution(
        self,
        user_id: str,
        routine_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Compute complete evolution data with all algorithms
        
        Args:
            user_id: User identifier
            routine_data: Current routine information
        
        Returns:
            Dictionary with evolution metrics and graph data
        """
        try:
            if not self.progress_manager:
                return {
                    'success': False,
                    'message': 'Progress manager not initialized'
                }
            
            # Get user progress
            user_progress = self.progress_manager.user_progress.get(user_id, {})
            progress_history = self.progress_manager.progress_history
            
            if not user_progress and not routine_data:
                return {
                    'success': True,
                    'dailyGraphData': [],
                    'monthlyGraphData': [],
                    'excellenceLevel': 0,
                    'remainingSkills': [],
                    'motivationMessage': 'Start your learning journey to see your evolution!',
                    'metrics': {
                        'total_skills': 0,
                        'completed_skills': 0,
                        'overall_completion': 0
                    }
                }
            
            # Algorithm 1: Compute daily progress change
            daily_graph_data = self._compute_daily_progress(user_id, progress_history)
            
            # Algorithm 2: Compute monthly growth rate
            monthly_graph_data = self._compute_monthly_growth(user_id, progress_history)
            
            # Algorithm 3: Detect remaining skills
            remaining_skills = self._detect_remaining_skills(user_id, user_progress, routine_data)
            
            # Algorithm 4: Detect excellence threshold
            excellence_level = self._detect_excellence_level(user_id, user_progress, routine_data)
            
            # Algorithm 5: Generate motivational message
            motivation_message = self._generate_motivation_message(
                excellence_level,
                len(remaining_skills),
                daily_graph_data,
                monthly_graph_data
            )
            
            # Calculate overall metrics
            overall_completion = 0
            completed_skills = 0
            total_skills = 0
            
            if routine_data:
                prioritized_skills = routine_data.get('prioritized_skills', [])
                total_skills = len(prioritized_skills)
                
                for skill_data in prioritized_skills:
                    skill_name = skill_data.get('skill', '')
                    if skill_name in user_progress:
                        completion = user_progress[skill_name]['completion_percentage']
                        if completion >= 100:
                            completed_skills += 1
                
                # Calculate overall completion
                if total_skills > 0:
                    overall_completion = self.progress_manager._calculate_overall_completion(
                        user_id, routine_data
                    )
            
            return {
                'success': True,
                'dailyGraphData': daily_graph_data,
                'monthlyGraphData': monthly_graph_data,
                'excellenceLevel': round(excellence_level, 2),
                'remainingSkills': remaining_skills,
                'motivationMessage': motivation_message,
                'metrics': {
                    'total_skills': total_skills,
                    'completed_skills': completed_skills,
                    'in_progress_skills': total_skills - completed_skills - len(remaining_skills),
                    'overall_completion': round(overall_completion, 2),
                    'excellence_achieved': excellence_level >= self.excellence_threshold
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Evolution computation failed: {str(e)}'
            }
    
    def _compute_daily_progress(
        self,
        user_id: str,
        progress_history: Dict
    ) -> List[Dict]:
        """
        Algorithm 1: Compute daily progress change
        Returns daily progress data with change indicators
        """
        daily_data = []
        
        # Aggregate all skill history by date
        date_completion = defaultdict(list)
        
        for key, history in progress_history.items():
            if key.startswith(f"{user_id}:"):
                for entry in history:
                    date = entry['date'].split('T')[0]  # Get date only
                    date_completion[date].append(entry['completion_percentage'])
        
        # Calculate average completion per day and change
        sorted_dates = sorted(date_completion.keys())
        previous_completion = 0
        
        for i, date in enumerate(sorted_dates[-30:]):  # Last 30 days
            completions = date_completion[date]
            avg_completion = sum(completions) / len(completions) if completions else 0
            
            # Calculate change from previous day
            change = avg_completion - previous_completion if i > 0 else 0
            change_percentage = (change / previous_completion * 100) if previous_completion > 0 else 0
            
            daily_data.append({
                'date': date,
                'completion': round(avg_completion, 2),
                'change': round(change, 2),
                'change_percentage': round(change_percentage, 2),
                'trend': 'up' if change > 0 else 'down' if change < 0 else 'stable'
            })
            
            previous_completion = avg_completion
        
        return daily_data
    
    def _compute_monthly_growth(
        self,
        user_id: str,
        progress_history: Dict
    ) -> List[Dict]:
        """
        Algorithm 2: Compute monthly growth rate
        Formula: ((currentScore - previousMonthScore) / previousMonthScore) × 100
        """
        monthly_data = []
        
        # Aggregate by month
        month_completion = defaultdict(list)
        
        for key, history in progress_history.items():
            if key.startswith(f"{user_id}:"):
                for entry in history:
                    date = entry['date'].split('T')[0]
                    month = date[:7]  # YYYY-MM
                    month_completion[month].append(entry['completion_percentage'])
        
        # Calculate average completion per month and growth rate
        sorted_months = sorted(month_completion.keys())
        previous_score = 0
        
        for i, month in enumerate(sorted_months[-12:]):  # Last 12 months
            completions = month_completion[month]
            current_score = sum(completions) / len(completions) if completions else 0
            
            # Calculate growth rate
            if i > 0 and previous_score > 0:
                growth_rate = ((current_score - previous_score) / previous_score) * 100
            else:
                growth_rate = 0
            
            monthly_data.append({
                'month': month,
                'completion': round(current_score, 2),
                'growth_rate': round(growth_rate, 2),
                'previous_score': round(previous_score, 2),
                'trend': 'growth' if growth_rate > 0 else 'decline' if growth_rate < 0 else 'stable'
            })
            
            previous_score = current_score
        
        return monthly_data
    
    def _detect_remaining_skills(
        self,
        user_id: str,
        user_progress: Dict,
        routine_data: Dict[str, Any]
    ) -> List[Dict]:
        """
        Algorithm 3: Detect remaining skills
        Returns list of skills not yet completed
        """
        if not routine_data:
            return []
        
        remaining_skills = []
        prioritized_skills = routine_data.get('prioritized_skills', [])
        
        for skill_data in prioritized_skills:
            skill_name = skill_data.get('skill', '')
            estimated_hours = skill_data.get('estimated_hours', 0)
            difficulty = skill_data.get('difficulty', 'Intermediate')
            priority_score = skill_data.get('priority_score', 0)
            
            # Check if skill is not completed
            completion = 0
            if skill_name in user_progress:
                completion = user_progress[skill_name]['completion_percentage']
            
            if completion < 100:
                remaining_hours = estimated_hours * (100 - completion) / 100
                
                remaining_skills.append({
                    'skill': skill_name,
                    'completion': round(completion, 2),
                    'remaining_hours': round(remaining_hours, 2),
                    'difficulty': difficulty,
                    'priority_score': round(priority_score, 3),
                    'status': 'in_progress' if completion > 0 else 'not_started'
                })
        
        # Sort by priority score (descending)
        remaining_skills.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return remaining_skills
    
    def _detect_excellence_level(
        self,
        user_id: str,
        user_progress: Dict,
        routine_data: Dict[str, Any]
    ) -> float:
        """
        Algorithm 4: Detect excellence threshold (>85% mastery)
        Returns excellence level as percentage
        """
        if not routine_data:
            return 0.0
        
        prioritized_skills = routine_data.get('prioritized_skills', [])
        if not prioritized_skills:
            return 0.0
        
        # Calculate weighted excellence score
        total_weight = 0
        excellence_score = 0
        
        for skill_data in prioritized_skills:
            skill_name = skill_data.get('skill', '')
            estimated_hours = skill_data.get('estimated_hours', 0)
            
            # Use estimated hours as weight (more hours = more important)
            weight = estimated_hours
            total_weight += weight
            
            # Get completion percentage
            completion = 0
            if skill_name in user_progress:
                completion = user_progress[skill_name]['completion_percentage']
            
            # Only count towards excellence if >= 85%
            if completion >= self.excellence_threshold:
                excellence_score += weight
        
        if total_weight == 0:
            return 0.0
        
        # Calculate excellence level as percentage of total weight
        excellence_level = (excellence_score / total_weight) * 100
        
        return excellence_level
    
    def _generate_motivation_message(
        self,
        excellence_level: float,
        remaining_skills_count: int,
        daily_data: List[Dict],
        monthly_data: List[Dict]
    ) -> str:
        """
        Algorithm 5: Generate motivational message based on progress stage
        """
        # Analyze recent trends
        recent_trend = 'stable'
        if daily_data:
            recent_changes = [d['change'] for d in daily_data[-7:]]  # Last 7 days
            avg_change = sum(recent_changes) / len(recent_changes) if recent_changes else 0
            if avg_change > 0:
                recent_trend = 'improving'
            elif avg_change < 0:
                recent_trend = 'declining'
        
        # Analyze monthly growth
        monthly_growth = 0
        if monthly_data and len(monthly_data) >= 2:
            monthly_growth = monthly_data[-1]['growth_rate']
        
        # Generate message based on excellence level
        if excellence_level >= 95:
            message = "🏆 OUTSTANDING! You've achieved mastery level! You're in the top tier of learners. Your dedication is truly inspiring!"
        
        elif excellence_level >= self.excellence_threshold:
            message = f"🌟 EXCELLENT! You've reached {excellence_level:.1f}% excellence level! You're demonstrating exceptional mastery. Keep this momentum going!"
        
        elif excellence_level >= 70:
            message = f"💪 GREAT PROGRESS! You're at {excellence_level:.1f}% excellence level. You're on the path to mastery. Just a bit more to reach excellence!"
        
        elif excellence_level >= 50:
            message = f"📈 SOLID WORK! You're at {excellence_level:.1f}% excellence level. You're building strong foundations. Keep pushing forward!"
        
        elif excellence_level >= 25:
            message = f"🎯 GOOD START! You're at {excellence_level:.1f}% excellence level. You're making steady progress. Consistency is key!"
        
        elif excellence_level > 0:
            message = f"🚀 BEGINNING YOUR JOURNEY! You're at {excellence_level:.1f}% excellence level. Every expert was once a beginner. Keep going!"
        
        else:
            message = "📚 READY TO START! Begin your learning journey and watch your excellence level grow. The first step is always the hardest!"
        
        # Add trend-based encouragement
        if recent_trend == 'improving':
            message += f" Your recent progress is trending upward - fantastic! 📊"
        elif recent_trend == 'declining':
            message += f" Take a moment to review your approach. Small adjustments can make a big difference! 💡"
        
        # Add monthly growth insight
        if monthly_growth > 10:
            message += f" Your monthly growth rate of {monthly_growth:.1f}% is impressive! 🚀"
        elif monthly_growth > 0:
            message += f" You're growing at {monthly_growth:.1f}% monthly. Steady progress wins the race! 🐢"
        
        # Add remaining skills insight
        if remaining_skills_count == 0:
            message += " You've completed all skills! Time to celebrate! 🎉"
        elif remaining_skills_count == 1:
            message += f" Just 1 skill remaining. You're almost there! 🏁"
        elif remaining_skills_count <= 3:
            message += f" Only {remaining_skills_count} skills left. The finish line is in sight! 🎯"
        else:
            message += f" {remaining_skills_count} skills remaining. Focus on one at a time! 📝"
        
        return message


if __name__ == "__main__":
    # Test
    from progressManager import ProgressManager
    
    manager = ProgressManager()
    tracker = EvolutionTracker(manager)
    
    # Test routine data
    routine_data = {
        'prioritized_skills': [
            {'skill': 'Python', 'estimated_hours': 60, 'difficulty': 'Advanced', 'priority_score': 0.9},
            {'skill': 'React', 'estimated_hours': 50, 'difficulty': 'Intermediate', 'priority_score': 0.8},
            {'skill': 'Docker', 'estimated_hours': 30, 'difficulty': 'Beginner', 'priority_score': 0.7}
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
    
    # Update some progress
    manager.update_progress('user123', 1, 'Python', 90.0, '2026-02-28', routine_data)
    manager.update_progress('user123', 2, 'React', 75.0, '2026-03-07', routine_data)
    manager.update_progress('user123', 3, 'Docker', 50.0, '2026-03-14', routine_data)
    
    # Test evolution computation
    result = tracker.compute_evolution('user123', routine_data)
    
    print(f"Success: {result['success']}")
    print(f"Excellence Level: {result['excellenceLevel']}%")
    print(f"Remaining Skills: {len(result['remainingSkills'])}")
    print(f"Daily Data Points: {len(result['dailyGraphData'])}")
    print(f"Monthly Data Points: {len(result['monthlyGraphData'])}")
    print(f"Motivation: {result['motivationMessage'][:100]}...")
    print("✅ EvolutionTracker test passed")
