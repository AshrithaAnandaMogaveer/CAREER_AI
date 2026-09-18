"""
Test Evolution Analytics Module and API
Tests analytics generation and graph-ready data
"""

import sys
import os
import json

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

def test_evolution_analytics_module():
    """Test the EvolutionAnalytics class directly"""
    print("=" * 60)
    print("TEST 1: Evolution Analytics Module")
    print("=" * 60)
    
    try:
        from backend.evolution_analytics import EvolutionAnalytics
        
        analytics = EvolutionAnalytics()
        
        # Sample progress data
        sample_records = [
            {'skill': 'Python', 'week_number': 1, 'topic': 'Python Basics', 'completed': True, 'completed_at': '2024-03-01T10:00:00'},
            {'skill': 'Python', 'week_number': 2, 'topic': 'OOP', 'completed': True, 'completed_at': '2024-03-02T10:00:00'},
            {'skill': 'Python', 'week_number': 3, 'topic': 'Advanced', 'completed': False, 'completed_at': None},
            {'skill': 'Machine Learning', 'week_number': 1, 'topic': 'Linear Regression', 'completed': True, 'completed_at': '2024-03-01T14:00:00'},
            {'skill': 'Machine Learning', 'week_number': 2, 'topic': 'Logistic Regression', 'completed': True, 'completed_at': '2024-03-03T10:00:00'},
            {'skill': 'Machine Learning', 'week_number': 3, 'topic': 'Decision Trees', 'completed': False, 'completed_at': None},
            {'skill': 'React', 'week_number': 1, 'topic': 'Components', 'completed': False, 'completed_at': None},
        ]
        
        result = analytics.generate_analytics(sample_records)
        
        # Verify structure
        assert 'daily_progress' in result
        assert 'weekly_progress' in result
        assert 'skill_completion' in result
        assert 'overall_metrics' in result
        
        print("\n✅ Daily Progress:")
        for day in result['daily_progress']:
            print(f"   {day['date']}: {day['completed_topics']} topics (cumulative: {day['cumulative_topics']})")
        
        print("\n✅ Weekly Progress:")
        for week in result['weekly_progress']:
            print(f"   Week {week['week_number']}: {week['completed_topics']}/{week['total_topics']} completed ({week['completion_rate']}%)")
        
        print("\n✅ Skill Completion:")
        for skill in result['skill_completion']:
            print(f"   {skill['skill']}: {skill['completed_topics']}/{skill['total_topics']} ({skill['completion_percentage']}%) - {skill['status']}")
        
        print("\n✅ Overall Metrics:")
        metrics = result['overall_metrics']
        print(f"   Total Topics: {metrics['total_topics']}")
        print(f"   Completed: {metrics['completed_topics']}")
        print(f"   Remaining: {metrics['remaining_topics']}")
        print(f"   Overall Rate: {metrics['overall_completion_rate']}%")
        print(f"   Unique Skills: {metrics['unique_skills']}")
        print(f"   Avg Topics/Week: {metrics['avg_topics_per_week']}")
        print(f"   Current Streak: {metrics['current_streak_days']} days")
        
        # Verify calculations
        assert metrics['total_topics'] == 7
        assert metrics['completed_topics'] == 4
        assert metrics['remaining_topics'] == 3
        assert metrics['unique_skills'] == 3
        
        print("\n✅ Module test passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Module test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_evolution_analytics_api():
    """Test the Evolution Analytics API endpoint"""
    print("\n" + "=" * 60)
    print("TEST 2: Evolution Analytics API")
    print("=" * 60)
    
    try:
        # Import Flask app
        from flask_cors_config import app
        
        # Create test client
        client = app.test_client()
        
        with app.app_context():
            # Import models and db
            from user_model import User
            from progress_tracking_model import RoutineProgress
            from community_models import db
            
            # Create test user
            test_user = User.query.filter_by(email='evolution_test@example.com').first()
            
            if not test_user:
                test_user = User(
                    name='Evolution Tester',
                    email='evolution_test@example.com'
                )
                test_user.set_password('TestPassword123')
                db.session.add(test_user)
                db.session.commit()
                print("✅ Test user created")
            else:
                print("ℹ️  Using existing test user")
            
            # Generate JWT token
            import jwt
            from datetime import datetime, timedelta
            
            token = jwt.encode({
                'user_id': test_user.id,
                'email': test_user.email,
                'exp': datetime.utcnow() + timedelta(days=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # Create sample progress data
            print("\n📊 Creating sample progress data...")
            
            test_records = [
                {'skill': 'Python', 'week_number': 1, 'topic': 'Python Basics', 'completed': True},
                {'skill': 'Python', 'week_number': 2, 'topic': 'OOP', 'completed': True},
                {'skill': 'Python', 'week_number': 3, 'topic': 'Advanced', 'completed': False},
                {'skill': 'Machine Learning', 'week_number': 1, 'topic': 'Linear Regression', 'completed': True},
                {'skill': 'Machine Learning', 'week_number': 2, 'topic': 'Logistic Regression', 'completed': True},
                {'skill': 'Machine Learning', 'week_number': 3, 'topic': 'Decision Trees', 'completed': False},
                {'skill': 'React', 'week_number': 1, 'topic': 'Components', 'completed': True},
                {'skill': 'React', 'week_number': 2, 'topic': 'Hooks', 'completed': False},
            ]
            
            for record in test_records:
                response = client.post(
                    '/api/routine/progress/weekly',
                    data=json.dumps(record),
                    headers=headers
                )
                assert response.status_code == 200
            
            print(f"✅ Created {len(test_records)} progress records")
            
            # Test 1: Get all analytics
            print("\n" + "=" * 60)
            print("TEST 2.1: Get All Analytics")
            print("=" * 60)
            
            response = client.get(
                '/api/routine/evolution/analytics',
                headers=headers
            )
            
            assert response.status_code == 200
            result = response.get_json()
            assert result['success'] == True
            assert 'analytics' in result
            
            analytics = result['analytics']
            
            print("\n✅ Daily Progress:")
            for day in analytics['daily_progress'][:3]:
                print(f"   {day['date']}: {day['completed_topics']} topics (cumulative: {day['cumulative_topics']})")
            
            print("\n✅ Weekly Progress:")
            for week in analytics['weekly_progress']:
                print(f"   Week {week['week_number']}: {week['completed_topics']}/{week['total_topics']} completed ({week['completion_rate']}%)")
            
            print("\n✅ Skill Completion:")
            for skill in analytics['skill_completion']:
                print(f"   {skill['skill']}: {skill['completed_topics']}/{skill['total_topics']} ({skill['completion_percentage']}%) - {skill['status']}")
            
            print("\n✅ Overall Metrics:")
            metrics = analytics['overall_metrics']
            print(f"   Total Topics: {metrics['total_topics']}")
            print(f"   Completed: {metrics['completed_topics']}")
            print(f"   Remaining: {metrics['remaining_topics']}")
            print(f"   Overall Rate: {metrics['overall_completion_rate']}%")
            print(f"   Unique Skills: {metrics['unique_skills']}")
            
            # Test 2: Get analytics filtered by skill
            print("\n" + "=" * 60)
            print("TEST 2.2: Get Analytics Filtered by Skill")
            print("=" * 60)
            
            response = client.get(
                '/api/routine/evolution/analytics?skill=Python',
                headers=headers
            )
            
            assert response.status_code == 200
            result = response.get_json()
            assert result['success'] == True
            
            analytics = result['analytics']
            
            print("\n✅ Python Skill Analytics:")
            for skill in analytics['skill_completion']:
                assert skill['skill'] == 'Python'
                print(f"   {skill['skill']}: {skill['completed_topics']}/{skill['total_topics']} ({skill['completion_percentage']}%)")
            
            print("\n✅ API test passed!")
            return True
            
    except AssertionError as e:
        print(f"\n❌ API test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ API test error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_graph_data_format():
    """Test that data is in correct format for charting libraries"""
    print("\n" + "=" * 60)
    print("TEST 3: Graph Data Format Validation")
    print("=" * 60)
    
    try:
        from backend.evolution_analytics import EvolutionAnalytics
        
        analytics = EvolutionAnalytics()
        
        sample_records = [
            {'skill': 'Python', 'week_number': 1, 'topic': 'Basics', 'completed': True, 'completed_at': '2024-03-01T10:00:00'},
            {'skill': 'Python', 'week_number': 2, 'topic': 'OOP', 'completed': True, 'completed_at': '2024-03-02T10:00:00'},
        ]
        
        result = analytics.generate_analytics(sample_records)
        
        # Validate daily_progress format (for line charts)
        print("\n✅ Daily Progress Format (Line Chart):")
        for day in result['daily_progress']:
            assert 'date' in day
            assert 'completed_topics' in day
            assert 'cumulative_topics' in day
            assert isinstance(day['completed_topics'], int)
            assert isinstance(day['cumulative_topics'], int)
            print(f"   ✓ {day}")
        
        # Validate weekly_progress format (for bar charts)
        print("\n✅ Weekly Progress Format (Bar Chart):")
        for week in result['weekly_progress']:
            assert 'week_number' in week
            assert 'completed_topics' in week
            assert 'remaining_topics' in week
            assert 'completion_rate' in week
            assert isinstance(week['week_number'], int)
            assert isinstance(week['completed_topics'], int)
            assert isinstance(week['remaining_topics'], int)
            print(f"   ✓ Week {week['week_number']}: {week}")
        
        # Validate skill_completion format (for pie/donut charts)
        print("\n✅ Skill Completion Format (Pie/Donut Chart):")
        for skill in result['skill_completion']:
            assert 'skill' in skill
            assert 'total_topics' in skill
            assert 'completed_topics' in skill
            assert 'completion_percentage' in skill
            assert 'status' in skill
            assert isinstance(skill['completion_percentage'], (int, float))
            print(f"   ✓ {skill['skill']}: {skill}")
        
        # Validate overall_metrics format
        print("\n✅ Overall Metrics Format:")
        metrics = result['overall_metrics']
        required_fields = [
            'total_topics', 'completed_topics', 'remaining_topics',
            'overall_completion_rate', 'unique_skills', 'total_weeks',
            'avg_topics_per_week', 'current_streak_days'
        ]
        for field in required_fields:
            assert field in metrics
            print(f"   ✓ {field}: {metrics[field]}")
        
        print("\n✅ Graph data format validation passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Format validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("TESTING EVOLUTION ANALYTICS")
    print("=" * 60)
    
    test1 = test_evolution_analytics_module()
    test2 = test_evolution_analytics_api()
    test3 = test_graph_data_format()
    
    print("\n" + "=" * 60)
    if test1 and test2 and test3:
        print("ALL TESTS PASSED ✅")
        print("=" * 60)
        print("\nSummary:")
        print("✅ Evolution Analytics Module")
        print("✅ Evolution Analytics API")
        print("✅ Graph Data Format Validation")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED ❌")
        print("=" * 60)
        sys.exit(1)
