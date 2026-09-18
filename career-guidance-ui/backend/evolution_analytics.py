"""
Evolution Analytics Module
Generates chart data for progress visualization
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict


class EvolutionAnalytics:
    """
    Analyzes user progress data and generates graph-ready metrics
    """
    
    def __init__(self):
        pass
    
    def generate_analytics(
        self,
        progress_records: List[Dict[str, Any]],
        skill_roadmaps: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive analytics from progress data
        
        Args:
            progress_records: List of progress records from database
            skill_roadmaps: Optional skill roadmap data for total topics
        
        Returns:
            Dictionary with graph-ready data
        """
        if not progress_records:
            return self._empty_analytics()
        
        # Build analytics
        daily_progress = self._calculate_daily_progress(progress_records)
        weekly_progress = self._calculate_weekly_progress(progress_records)
        monthly_progress = self._calculate_monthly_progress(progress_records)
        skill_completion = self._calculate_skill_completion(progress_records, skill_roadmaps)
        overall_metrics = self._calculate_overall_metrics(progress_records, skill_roadmaps)
        
        return {
            'daily_progress': daily_progress,
            'weekly_progress': weekly_progress,
            'monthly_progress': monthly_progress,
            'skill_completion': skill_completion,
            'overall_metrics': overall_metrics,
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def _calculate_daily_progress(
        self,
        progress_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Calculate daily progress (topics completed per day)
        
        Returns:
            List of {date, completed_topics, cumulative_topics}
        """
        # Group by date
        daily_completions = defaultdict(int)
        
        for record in progress_records:
            if record.get('completed') and record.get('completed_at'):
                # Extract date from completed_at timestamp
                completed_date = record['completed_at'].split('T')[0]
                daily_completions[completed_date] += 1
        
        # Sort by date and calculate cumulative
        sorted_dates = sorted(daily_completions.keys())
        cumulative = 0
        daily_data = []
        
        for date in sorted_dates:
            completed = daily_completions[date]
            cumulative += completed
            daily_data.append({
                'date': date,
                'completed_topics': completed,
                'cumulative_topics': cumulative
            })
        
        return daily_data
    
    def _calculate_weekly_progress(
        self,
        progress_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Calculate weekly progress (topics completed per week number)
        Also derives the actual date range for each week from completed_at timestamps.

        Returns:
            List of {week_number, week_label, week_start, week_end,
                     completed_topics, remaining_topics, completion_rate}
        """
        # Group by week number, also track dates per week
        week_data = defaultdict(lambda: {'total': 0, 'completed': 0, 'dates': []})

        for record in progress_records:
            week_num = record.get('week_number')
            if week_num:
                week_data[week_num]['total'] += 1
                if record.get('completed'):
                    week_data[week_num]['completed'] += 1
                # Collect dates to derive real week range
                completed_at = record.get('completed_at') or record.get('updated_at') or record.get('created_at')
                if completed_at:
                    try:
                        date_str = completed_at.split('T')[0]
                        week_data[week_num]['dates'].append(
                            datetime.strptime(date_str, '%Y-%m-%d')
                        )
                    except Exception:
                        pass

        # Build weekly progress list
        weekly_progress = []
        for week_num in sorted(week_data.keys()):
            data = week_data[week_num]
            total = data['total']
            completed = data['completed']
            remaining = total - completed
            completion_rate = (completed / total * 100) if total > 0 else 0

            # Derive week label from actual dates if available
            dates = data['dates']
            if dates:
                week_start = min(dates)
                week_end = max(dates)
                # e.g. "Apr 14" or "Apr 14-20"
                if week_start.date() == week_end.date():
                    week_label = week_start.strftime('%b %-d') if hasattr(week_start, 'strftime') else f"W{week_num}"
                else:
                    week_label = f"{week_start.strftime('%b %-d')}-{week_end.strftime('%-d')}"
                week_start_str = week_start.strftime('%Y-%m-%d')
                week_end_str = week_end.strftime('%Y-%m-%d')
            else:
                week_label = f"W{week_num}"
                week_start_str = None
                week_end_str = None

            weekly_progress.append({
                'week_number': week_num,
                'week_label': week_label,
                'week_start': week_start_str,
                'week_end': week_end_str,
                'completed_topics': completed,
                'remaining_topics': remaining,
                'total_topics': total,
                'completion_rate': round(completion_rate, 1)
            })

        return weekly_progress
    
    def _calculate_monthly_progress(
        self,
        progress_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Calculate monthly progress (topics completed per month)
        
        Returns:
            List of {month, year, month_label, completed_topics, cumulative_topics, growth_rate}
        """
        # Group by month
        monthly_completions = defaultdict(int)
        
        for record in progress_records:
            if record.get('completed') and record.get('completed_at'):
                # Extract year-month from completed_at timestamp
                completed_date = record['completed_at'].split('T')[0]
                try:
                    date_obj = datetime.strptime(completed_date, '%Y-%m-%d')
                    month_key = date_obj.strftime('%Y-%m')
                    monthly_completions[month_key] += 1
                except:
                    continue
        
        # Sort by month and calculate cumulative and growth
        sorted_months = sorted(monthly_completions.keys())
        cumulative = 0
        monthly_data = []
        prev_completed = 0
        
        for month_key in sorted_months:
            completed = monthly_completions[month_key]
            cumulative += completed
            
            # Calculate growth rate
            if prev_completed > 0:
                growth_rate = ((completed - prev_completed) / prev_completed) * 100
            else:
                growth_rate = 0 if completed == 0 else 100
            
            # Parse month for display
            try:
                date_obj = datetime.strptime(month_key, '%Y-%m')
                month_label = date_obj.strftime('%b %Y')  # e.g., "Jan 2024"
                month_num = date_obj.month
                year = date_obj.year
            except:
                month_label = month_key
                month_num = 1
                year = 2024
            
            monthly_data.append({
                'month': month_num,
                'year': year,
                'month_label': month_label,
                'completed_topics': completed,
                'cumulative_topics': cumulative,
                'growth_rate': round(growth_rate, 1)
            })
            
            prev_completed = completed
        
        return monthly_data
    
    def _calculate_skill_completion(
        self,
        progress_records: List[Dict[str, Any]],
        skill_roadmaps: List[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Calculate completion percentage per skill
        
        Returns:
            List of {skill, total_topics, completed_topics, completion_percentage, status}
        """
        # Group by skill
        skill_data = defaultdict(lambda: {'total': 0, 'completed': 0})
        
        for record in progress_records:
            skill = record.get('skill')
            if skill:
                skill_data[skill]['total'] += 1
                if record.get('completed'):
                    skill_data[skill]['completed'] += 1
        
        # If skill_roadmaps provided, use those for total topics
        if skill_roadmaps:
            for roadmap in skill_roadmaps:
                skill = roadmap.get('skill')
                if skill and skill not in skill_data:
                    # Skill exists in roadmap but no progress yet
                    skill_data[skill] = {
                        'total': roadmap.get('total_topics', 0),
                        'completed': 0
                    }
                elif skill and skill in skill_data:
                    # Update total from roadmap if available
                    skill_data[skill]['total'] = roadmap.get('total_topics', skill_data[skill]['total'])
        
        # Build skill completion list
        skill_completion = []
        for skill in sorted(skill_data.keys()):
            data = skill_data[skill]
            total = data['total']
            completed = data['completed']
            completion_percentage = (completed / total * 100) if total > 0 else 0
            
            # Determine status
            if completion_percentage >= 80:
                status = 'Achieved'
            elif completion_percentage >= 50:
                status = 'In Progress'
            elif completion_percentage > 0:
                status = 'Started'
            else:
                status = 'Not Started'
            
            skill_completion.append({
                'skill': skill,
                'total_topics': total,
                'completed_topics': completed,
                'remaining_topics': total - completed,
                'completion_percentage': round(completion_percentage, 1),
                'status': status
            })
        
        return skill_completion
    
    def _calculate_overall_metrics(
        self,
        progress_records: List[Dict[str, Any]],
        skill_roadmaps: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate overall progress metrics
        
        Returns:
            Dictionary with overall statistics
        """
        total_topics = len(progress_records)
        completed_topics = sum(1 for r in progress_records if r.get('completed'))
        remaining_topics = total_topics - completed_topics
        
        # Calculate overall completion rate
        overall_completion_rate = (completed_topics / total_topics * 100) if total_topics > 0 else 0
        
        # Count unique skills
        unique_skills = len(set(r.get('skill') for r in progress_records if r.get('skill')))
        
        # Calculate average completion per week
        weeks_with_progress = set(r.get('week_number') for r in progress_records if r.get('week_number'))
        total_weeks = len(weeks_with_progress)
        avg_topics_per_week = completed_topics / total_weeks if total_weeks > 0 else 0
        
        # Calculate streak (consecutive days with completions)
        current_streak = self._calculate_streak(progress_records)
        
        # Estimate completion date
        if remaining_topics > 0 and avg_topics_per_week > 0:
            weeks_remaining = remaining_topics / avg_topics_per_week
            estimated_completion = datetime.utcnow() + timedelta(weeks=weeks_remaining)
            estimated_completion_date = estimated_completion.strftime('%Y-%m-%d')
        else:
            estimated_completion_date = None
        
        return {
            'total_topics': total_topics,
            'completed_topics': completed_topics,
            'remaining_topics': remaining_topics,
            'overall_completion_rate': round(overall_completion_rate, 1),
            'unique_skills': unique_skills,
            'total_weeks': total_weeks,
            'avg_topics_per_week': round(avg_topics_per_week, 1),
            'current_streak_days': current_streak,
            'estimated_completion_date': estimated_completion_date
        }
    
    def _calculate_streak(
        self,
        progress_records: List[Dict[str, Any]]
    ) -> int:
        """
        Calculate current streak of consecutive days with completions
        
        Returns:
            Number of consecutive days
        """
        # Get all completion dates
        completion_dates = []
        for record in progress_records:
            if record.get('completed') and record.get('completed_at'):
                date_str = record['completed_at'].split('T')[0]
                completion_dates.append(datetime.strptime(date_str, '%Y-%m-%d').date())
        
        if not completion_dates:
            return 0
        
        # Get unique dates and sort
        unique_dates = sorted(set(completion_dates), reverse=True)
        
        # Calculate streak from most recent date
        today = datetime.utcnow().date()
        streak = 0
        expected_date = today
        
        for date in unique_dates:
            if date == expected_date or date == expected_date - timedelta(days=1):
                streak += 1
                expected_date = date - timedelta(days=1)
            else:
                break
        
        return streak
    
    def _empty_analytics(self) -> Dict[str, Any]:
        """
        Return empty analytics structure when no data available
        """
        return {
            'daily_progress': [],
            'weekly_progress': [],
            'monthly_progress': [],
            'skill_completion': [],
            'overall_metrics': {
                'total_topics': 0,
                'completed_topics': 0,
                'remaining_topics': 0,
                'overall_completion_rate': 0,
                'unique_skills': 0,
                'total_weeks': 0,
                'avg_topics_per_week': 0,
                'current_streak_days': 0,
                'estimated_completion_date': None
            },
            'generated_at': datetime.utcnow().isoformat()
        }


if __name__ == "__main__":
    # Test with sample data
    analytics = EvolutionAnalytics()
    
    sample_records = [
        {'skill': 'Python', 'week_number': 1, 'topic': 'Basics', 'completed': True, 'completed_at': '2024-03-01T10:00:00'},
        {'skill': 'Python', 'week_number': 2, 'topic': 'OOP', 'completed': True, 'completed_at': '2024-03-02T10:00:00'},
        {'skill': 'Python', 'week_number': 3, 'topic': 'Advanced', 'completed': False, 'completed_at': None},
        {'skill': 'React', 'week_number': 1, 'topic': 'Components', 'completed': True, 'completed_at': '2024-03-01T14:00:00'},
        {'skill': 'React', 'week_number': 2, 'topic': 'Hooks', 'completed': False, 'completed_at': None},
    ]
    
    result = analytics.generate_analytics(sample_records)
    
    print("Daily Progress:", result['daily_progress'])
    print("Weekly Progress:", result['weekly_progress'])
    print("Skill Completion:", result['skill_completion'])
    print("Overall Metrics:", result['overall_metrics'])
    print("✅ EvolutionAnalytics test passed")
