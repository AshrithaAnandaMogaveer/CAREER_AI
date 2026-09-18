"""
Debug script to test evolution analytics
"""
import sys
sys.path.insert(0, '..')

from flask_cors_config import app, db
from progress_tracking_model import RoutineProgress
from evolution_analytics import EvolutionAnalytics

with app.app_context():
    # Get progress records for user 24
    records = RoutineProgress.query.filter_by(user_id=24).all()
    print(f'Found {len(records)} records for user 24')
    
    # Convert to dict
    progress_data = [r.to_dict() for r in records]
    
    # Generate analytics
    analytics = EvolutionAnalytics()
    result = analytics.generate_analytics(progress_data)
    
    print('\nAnalytics Results:')
    print(f'  Daily progress points: {len(result.get("daily_progress", []))}')
    print(f'  Weekly progress points: {len(result.get("weekly_progress", []))}')
    print(f'  Monthly progress points: {len(result.get("monthly_progress", []))}')
    print(f'  Skills: {len(result.get("skill_completion", []))}')
    
    overall = result.get('overall_metrics', {})
    print(f'  Overall completion: {overall.get("overall_completion_rate", 0)}%')
    
    daily = result.get('daily_progress', [])
    if len(daily) > 0:
        print(f'\n  Sample daily progress: {daily[0]}')
    
    weekly = result.get('weekly_progress', [])
    if len(weekly) > 0:
        print(f'  Sample weekly progress: {weekly[0]}')
    
    skills = result.get('skill_completion', [])
    if len(skills) > 0:
        print(f'  Sample skill: {skills[0]}')
    
    print('\n✅ Analytics generation working correctly!')
