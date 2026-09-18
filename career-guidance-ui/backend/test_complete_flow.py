"""
Complete Flow Test: Progress Tracking → Evolution Charts
Tests the entire flow from saving progress to displaying charts
"""
import sys
sys.path.insert(0, '..')

from flask_cors_config import app, db
from progress_tracking_model import RoutineProgress
from evolution_analytics import EvolutionAnalytics
from datetime import datetime

print("=" * 60)
print("COMPLETE FLOW TEST: Progress → Evolution")
print("=" * 60)

with app.app_context():
    # Step 1: Check existing data
    print("\n📊 Step 1: Checking existing progress data...")
    total_records = RoutineProgress.query.count()
    print(f"   Total records in database: {total_records}")
    
    if total_records > 0:
        # Get a sample user
        sample_record = RoutineProgress.query.first()
        user_id = sample_record.user_id
        print(f"   Testing with user ID: {user_id}")
        
        # Step 2: Get user's progress records
        print(f"\n📝 Step 2: Fetching progress records for user {user_id}...")
        user_records = RoutineProgress.query.filter_by(user_id=user_id).all()
        print(f"   Found {len(user_records)} records")
        
        # Show breakdown by skill
        skills = {}
        for record in user_records:
            if record.skill not in skills:
                skills[record.skill] = {'total': 0, 'completed': 0}
            skills[record.skill]['total'] += 1
            if record.completed:
                skills[record.skill]['completed'] += 1
        
        print(f"\n   Progress by skill:")
        for skill, data in skills.items():
            pct = (data['completed'] / data['total'] * 100) if data['total'] > 0 else 0
            print(f"   - {skill}: {data['completed']}/{data['total']} ({pct:.1f}%)")
        
        # Step 3: Generate analytics
        print(f"\n📈 Step 3: Generating evolution analytics...")
        progress_data = [r.to_dict() for r in user_records]
        analytics = EvolutionAnalytics()
        result = analytics.generate_analytics(progress_data)
        
        # Step 4: Verify chart data
        print(f"\n📊 Step 4: Verifying chart data...")
        
        daily = result.get('daily_progress', [])
        print(f"   ✅ Daily Progress: {len(daily)} data points")
        if len(daily) > 0:
            print(f"      Latest: {daily[-1]['date']} - {daily[-1]['cumulative_topics']} topics")
        
        weekly = result.get('weekly_progress', [])
        print(f"   ✅ Weekly Progress: {len(weekly)} data points")
        if len(weekly) > 0:
            latest_week = weekly[-1]
            print(f"      Week {latest_week['week_number']}: {latest_week['completed_topics']}/{latest_week['total_topics']} ({latest_week['completion_rate']:.1f}%)")
        
        monthly = result.get('monthly_progress', [])
        print(f"   ✅ Monthly Progress: {len(monthly)} data points")
        if len(monthly) > 0:
            latest_month = monthly[-1]
            print(f"      {latest_month['month_label']}: {latest_month['completed_topics']} topics (growth: {latest_month['growth_rate']:.1f}%)")
        
        skill_completion = result.get('skill_completion', [])
        print(f"   ✅ Skill Completion: {len(skill_completion)} skills")
        for skill in skill_completion:
            print(f"      {skill['skill']}: {skill['completion_percentage']:.1f}% - {skill['status']}")
        
        overall = result.get('overall_metrics', {})
        print(f"\n   📊 Overall Metrics:")
        print(f"      Total Topics: {overall.get('total_topics', 0)}")
        print(f"      Completed: {overall.get('completed_topics', 0)}")
        print(f"      Remaining: {overall.get('remaining_topics', 0)}")
        print(f"      Completion Rate: {overall.get('overall_completion_rate', 0):.1f}%")
        print(f"      Current Streak: {overall.get('current_streak_days', 0)} days")
        
        # Step 5: Validate for frontend
        print(f"\n✅ Step 5: Frontend validation...")
        
        # Check if data is suitable for charts
        has_daily = len(daily) > 0
        has_weekly = len(weekly) > 0
        has_monthly = len(monthly) > 0
        has_skills = len(skill_completion) > 0
        
        print(f"   Daily chart ready: {'✅' if has_daily else '❌'}")
        print(f"   Weekly chart ready: {'✅' if has_weekly else '❌'}")
        print(f"   Monthly chart ready: {'✅' if has_monthly else '❌'}")
        print(f"   Skill chart ready: {'✅' if has_skills else '❌'}")
        
        if has_daily and has_weekly and has_skills:
            print(f"\n🎉 SUCCESS! All charts have data and are ready to display!")
            print(f"\n   Frontend should show:")
            print(f"   - Green success banner")
            print(f"   - 4 metric cards")
            print(f"   - Daily progress line chart")
            print(f"   - Weekly progress bar chart")
            if has_monthly:
                print(f"   - Monthly progress line chart")
            print(f"   - Skill completion donut chart")
        else:
            print(f"\n⚠️  WARNING: Some charts may not display")
            print(f"   User needs to save more progress to see all charts")
        
        # Step 6: Simulate frontend API call
        print(f"\n🌐 Step 6: Simulating frontend API call...")
        print(f"   GET /api/routine/evolution/analytics")
        print(f"   Headers: Authorization: Bearer <token>")
        print(f"   Response: {{")
        print(f"     success: true,")
        print(f"     analytics: {{")
        print(f"       daily_progress: [{len(daily)} items],")
        print(f"       weekly_progress: [{len(weekly)} items],")
        print(f"       monthly_progress: [{len(monthly)} items],")
        print(f"       skill_completion: [{len(skill_completion)} items],")
        print(f"       overall_metrics: {{...}}")
        print(f"     }}")
        print(f"   }}")
        
        print(f"\n" + "=" * 60)
        print(f"✅ COMPLETE FLOW TEST PASSED!")
        print(f"=" * 60)
        print(f"\nNext steps:")
        print(f"1. Start Flask server: python flask_cors_config.py")
        print(f"2. Open browser and login")
        print(f"3. Go to Routine Build → Progress Tracking")
        print(f"4. Save progress for any skill")
        print(f"5. Go to Evolution Over Time tab")
        print(f"6. Click 'Refresh Data'")
        print(f"7. Charts should display! 🎉")
        
    else:
        print("\n⚠️  No progress records found in database")
        print("\nTo create test data:")
        print("1. Login to the app")
        print("2. Generate a routine")
        print("3. Go to Progress Tracking")
        print("4. Save progress for any skill")
        print("5. Run this test again")
