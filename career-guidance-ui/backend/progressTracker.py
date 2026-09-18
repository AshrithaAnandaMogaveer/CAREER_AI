"""
Progress Tracker Module
Implements progress tracking, lagging skill detection, and growth metrics
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import statistics


class ProgressTracker:
    """Tracks learning progress and detects lagging skills"""
    
    def __init__(self):
        self.progress_data = {}
    
    def calculate_skill_completion(
        self,
        skill: str,
        hours_completed: float,
        hours_planned: float
    ) -> float:
        """Calculate completion percentage for a skill"""
        if hours_planned == 0:
            return 100.0
        return min((hours_completed / hours_planned) * 100, 100.0)
    
    def calculate_overall_completion(
        self,
        skills_progress: List[Dict]
    ) -> float:
        """
        Calculate overall completion percentage
        Weighted by skill priority
        """
        if not skills_progress:
            return 0.0
        
        total_weight = 0
        weighted_completion = 0
        
        for skill in skills_progress:
            weight = skill.get('priority_score', 1.0)
            completion = skill.get('completion_percentage', 0)
            
            weighted_completion += completion * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        return weighted_completion / total_weight
    
    def detect_lagging_skills(
        self,
        skills_progress: List[Dict],
        current_week: int,
        total_weeks: int
    ) -> List[Dict]:
        """
        Detect skills that are behind schedule
        
        Algorithm:
        expectedProgress = (daysPassed / totalPlannedDays) × 100
        If actualProgress < expectedProgress: Mark as lagging
        """
        lagging_skills = []
        expected_progress = (current_week / total_weeks) * 100 if total_weeks > 0 else 0
        
        for skill in skills_progress:
            actual_progress = skill.get('completion_percentage', 0)
            planned_week = skill.get('planned_week', 1)
            
            # Check if skill should have started
            if current_week >= planned_week:
                # Calculate expected progress for this skill
                weeks_since_start = current_week - planned_week + 1
                skill_duration = skill.get('duration_weeks', 1)
                skill_expected = min((weeks_since_start / skill_duration) * 100, 100)
                
                # Lagging if more than 20% behind
                lag_threshold = 20
                if actual_progress < (skill_expected - lag_threshold):
                    lag_amount = skill_expected - actual_progress
                    
                    lagging_skills.append({
                        'skill': skill['skill'],
                        'actual_progress': actual_progress,
                        'expected_progress': skill_expected,
                        'lag_amount': lag_amount,
                        'severity': self._calculate_lag_severity(lag_amount),
                        'recommendation': self._get_lag_recommendation(lag_amount)
                    })
        
        # Sort by severity
        lagging_skills.sort(key=lambda x: x['lag_amount'], reverse=True)
        
        return lagging_skills
    
    def _calculate_lag_severity(self, lag_amount: float) -> str:
        """Determine severity of lag"""
        if lag_amount >= 50:
            return 'critical'
        elif lag_amount >= 30:
            return 'high'
        elif lag_amount >= 20:
            return 'medium'
        else:
            return 'low'
    
    def _get_lag_recommendation(self, lag_amount: float) -> str:
        """Generate recommendation based on lag"""
        if lag_amount >= 50:
            return 'Consider extending timeline or increasing study hours significantly'
        elif lag_amount >= 30:
            return 'Increase study hours by 50% or seek additional resources'
        elif lag_amount >= 20:
            return 'Allocate 2-3 extra hours this week to catch up'
        else:
            return 'Minor adjustment needed, stay focused'
    
    def calculate_monthly_growth_rate(
        self,
        current_score: float,
        previous_score: float
    ) -> float:
        """
        Calculate monthly growth rate
        Formula: ((currentScore - previousScore) / previousScore) × 100
        """
        if previous_score == 0:
            return 100.0 if current_score > 0 else 0.0
        
        growth_rate = ((current_score - previous_score) / previous_score) * 100
        return round(growth_rate, 2)
    
    def calculate_progress_metrics(
        self,
        skills_progress: List[Dict],
        weekly_schedule: List[Dict],
        current_week: int
    ) -> Dict:
        """
        Calculate comprehensive progress metrics
        """
        if not skills_progress:
            return self._empty_metrics()
        
        # Overall completion
        overall_completion = self.calculate_overall_completion(skills_progress)
        
        # Skills breakdown
        completed_skills = [s for s in skills_progress if s.get('completion_percentage', 0) >= 100]
        in_progress_skills = [s for s in skills_progress if 0 < s.get('completion_percentage', 0) < 100]
        not_started_skills = [s for s in skills_progress if s.get('completion_percentage', 0) == 0]
        
        # Time metrics
        total_hours_planned = sum(s.get('hours_planned', 0) for s in skills_progress)
        total_hours_completed = sum(s.get('hours_completed', 0) for s in skills_progress)
        
        # Velocity (skills per week)
        weeks_elapsed = current_week
        velocity = len(completed_skills) / weeks_elapsed if weeks_elapsed > 0 else 0
        
        # Projected completion
        remaining_skills = len(skills_progress) - len(completed_skills)
        projected_weeks = remaining_skills / velocity if velocity > 0 else 0
        
        # Consistency score (based on weekly activity)
        consistency_score = self._calculate_consistency_score(skills_progress, current_week)
        
        return {
            'overall_completion': round(overall_completion, 1),
            'skills_completed': len(completed_skills),
            'skills_in_progress': len(in_progress_skills),
            'skills_not_started': len(not_started_skills),
            'total_skills': len(skills_progress),
            'hours_completed': round(total_hours_completed, 1),
            'hours_planned': round(total_hours_planned, 1),
            'hours_remaining': round(total_hours_planned - total_hours_completed, 1),
            'velocity': round(velocity, 2),
            'projected_weeks_remaining': round(projected_weeks, 1),
            'consistency_score': consistency_score,
            'on_track': overall_completion >= ((current_week / len(weekly_schedule)) * 100) if weekly_schedule else True
        }
    
    def _calculate_consistency_score(
        self,
        skills_progress: List[Dict],
        current_week: int
    ) -> int:
        """
        Calculate consistency score (0-100)
        Based on regular progress updates
        """
        if current_week == 0:
            return 100
        
        # Check how many weeks have progress updates
        weeks_with_progress = set()
        for skill in skills_progress:
            updates = skill.get('progress_updates', [])
            for update in updates:
                weeks_with_progress.add(update.get('week', 0))
        
        consistency = (len(weeks_with_progress) / current_week) * 100 if current_week > 0 else 100
        return min(int(consistency), 100)
    
    def _empty_metrics(self) -> Dict:
        """Return empty metrics structure"""
        return {
            'overall_completion': 0,
            'skills_completed': 0,
            'skills_in_progress': 0,
            'skills_not_started': 0,
            'total_skills': 0,
            'hours_completed': 0,
            'hours_planned': 0,
            'hours_remaining': 0,
            'velocity': 0,
            'projected_weeks_remaining': 0,
            'consistency_score': 100,
            'on_track': True
        }
    
    def generate_progress_report(
        self,
        skills_progress: List[Dict],
        weekly_schedule: List[Dict],
        current_week: int,
        total_weeks: int
    ) -> Dict:
        """
        Generate comprehensive progress report
        """
        metrics = self.calculate_progress_metrics(skills_progress, weekly_schedule, current_week)
        lagging_skills = self.detect_lagging_skills(skills_progress, current_week, total_weeks)
        
        # Calculate trends
        completion_trend = self._calculate_completion_trend(skills_progress)
        
        # Generate insights
        insights = self._generate_insights(metrics, lagging_skills, current_week, total_weeks)
        
        return {
            'metrics': metrics,
            'lagging_skills': lagging_skills,
            'completion_trend': completion_trend,
            'insights': insights,
            'generated_at': datetime.now().isoformat()
        }
    
    def _calculate_completion_trend(self, skills_progress: List[Dict]) -> List[Dict]:
        """Calculate completion trend over time"""
        trend = []
        
        # Group progress by week
        weekly_completion = {}
        for skill in skills_progress:
            updates = skill.get('progress_updates', [])
            for update in updates:
                week = update.get('week', 0)
                completion = update.get('completion', 0)
                
                if week not in weekly_completion:
                    weekly_completion[week] = []
                weekly_completion[week].append(completion)
        
        # Calculate average completion per week
        for week in sorted(weekly_completion.keys()):
            avg_completion = statistics.mean(weekly_completion[week])
            trend.append({
                'week': week,
                'average_completion': round(avg_completion, 1)
            })
        
        return trend
    
    def _generate_insights(
        self,
        metrics: Dict,
        lagging_skills: List[Dict],
        current_week: int,
        total_weeks: int
    ) -> List[str]:
        """Generate actionable insights"""
        insights = []
        
        # Progress insights
        if metrics['overall_completion'] >= 80:
            insights.append("🎉 Excellent progress! You're on track to complete ahead of schedule.")
        elif metrics['overall_completion'] >= 50:
            insights.append("✅ Good progress! Keep up the consistent effort.")
        elif metrics['overall_completion'] >= 25:
            insights.append("📈 Making steady progress. Consider increasing study hours if possible.")
        else:
            insights.append("⚠️ Progress is slower than expected. Review your schedule and priorities.")
        
        # Lagging skills insights
        if lagging_skills:
            critical_count = sum(1 for s in lagging_skills if s['severity'] == 'critical')
            if critical_count > 0:
                insights.append(f"🚨 {critical_count} skill(s) critically behind schedule. Immediate action needed.")
            else:
                insights.append(f"⚡ {len(lagging_skills)} skill(s) need attention to stay on track.")
        
        # Velocity insights
        if metrics['velocity'] > 1:
            insights.append(f"🚀 High velocity! Completing {metrics['velocity']:.1f} skills per week.")
        elif metrics['velocity'] < 0.5 and current_week > 2:
            insights.append("🐌 Low velocity detected. Consider breaking skills into smaller chunks.")
        
        # Consistency insights
        if metrics['consistency_score'] >= 90:
            insights.append("💪 Excellent consistency! Regular practice is key to success.")
        elif metrics['consistency_score'] < 60:
            insights.append("📅 Inconsistent progress detected. Try to study regularly each week.")
        
        # Timeline insights
        progress_ratio = current_week / total_weeks if total_weeks > 0 else 0
        completion_ratio = metrics['overall_completion'] / 100
        
        if completion_ratio > progress_ratio + 0.1:
            insights.append("⏰ Ahead of schedule! Consider adding more advanced skills.")
        elif completion_ratio < progress_ratio - 0.1:
            insights.append("⏱️ Behind schedule. Consider extending timeline or increasing hours.")
        
        return insights
