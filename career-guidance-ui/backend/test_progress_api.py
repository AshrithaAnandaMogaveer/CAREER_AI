"""
Test Progress Tracking API Endpoints
Tests the three new endpoints for weekly progress tracking
"""

import sys
import os
import json

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

def test_progress_tracking_api():
    """Test all progress tracking endpoints"""
    print("=" * 60)
    print("TESTING PROGRESS TRACKING API ENDPOINTS")
    print("=" * 60)
    
    try:
        # Import Flask app
        from flask_cors_config import app
        
        # Create test client
        client = app.test_client()
        
        with app.app_context():
            # Import models and db after app context is set
            from user_model import User
            from progress_tracking_model import RoutineProgress
            from community_models import db
            
            # First, create a test user directly in database
            print("\n" + "=" * 60)
            print("SETUP: Creating Test User")
            print("=" * 60)
            
            # Check if user exists
            test_user = User.query.filter_by(email='progress_test@example.com').first()
            
            if not test_user:
                # Create new user
                test_user = User(
                    name='Progress Tester',
                    email='progress_test@example.com'
                )
                test_user.set_password('TestPassword123')
                db.session.add(test_user)
                db.session.commit()
                print("✅ Test user created")
            else:
                print("ℹ️  Using existing test user")
            
            # Generate JWT token directly
            import jwt
            from datetime import datetime, timedelta
            
            token = jwt.encode({
                'user_id': test_user.id,
                'email': test_user.email,
                'exp': datetime.utcnow() + timedelta(days=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            print(f"✅ Token generated for user ID: {test_user.id}")
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # Test 1: Update progress (create new record)
            print("\n" + "=" * 60)
            print("TEST 1: Create Progress Record")
            print("=" * 60)
            
            progress_data = {
                'skill': 'Machine Learning',
                'week_number': 1,
                'topic': 'Linear Regression',
                'completed': True
            }
            
            response = client.post(
                '/api/routine/progress/weekly',
                data=json.dumps(progress_data),
                headers=headers
            )
            
            assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.get_json()}"
            result = response.get_json()
            assert result['success'] == True
            assert result['progress']['completed'] == True
            print(f"✅ Progress record created: {result['progress']['topic']}")
            print(f"   Status: {'Completed' if result['progress']['completed'] else 'Incomplete'}")
            
            # Test 2: Create more progress records
            print("\n" + "=" * 60)
            print("TEST 2: Create Multiple Progress Records")
            print("=" * 60)
            
            test_records = [
                {'skill': 'Machine Learning', 'week_number': 2, 'topic': 'Logistic Regression', 'completed': True},
                {'skill': 'Machine Learning', 'week_number': 3, 'topic': 'Decision Trees', 'completed': False},
                {'skill': 'Python', 'week_number': 1, 'topic': 'Python Basics', 'completed': True},
                {'skill': 'Python', 'week_number': 2, 'topic': 'Data Structures', 'completed': False},
            ]
            
            for record in test_records:
                response = client.post(
                    '/api/routine/progress/weekly',
                    data=json.dumps(record),
                    headers=headers
                )
                assert response.status_code == 200
                result = response.get_json()
                print(f"✅ Created: {record['skill']} - Week {record['week_number']} - {record['topic']}")
            
            # Test 3: Get weekly progress (all)
            print("\n" + "=" * 60)
            print("TEST 3: Get All Weekly Progress")
            print("=" * 60)
            
            response = client.get(
                '/api/routine/progress/weekly',
                headers=headers
            )
            
            assert response.status_code == 200
            result = response.get_json()
            assert result['success'] == True
            assert result['count'] >= 5
            print(f"✅ Retrieved {result['count']} progress records")
            
            for record in result['progress'][:3]:
                print(f"   - {record['skill']} Week {record['week_number']}: {record['topic']} ({'✓' if record['completed'] else '○'})")
            
            # Test 4: Get weekly progress (filtered by skill)
            print("\n" + "=" * 60)
            print("TEST 4: Get Progress Filtered by Skill")
            print("=" * 60)
            
            response = client.get(
                '/api/routine/progress/weekly?skill=Machine Learning',
                headers=headers
            )
            
            assert response.status_code == 200
            result = response.get_json()
            assert result['success'] == True
            print(f"✅ Retrieved {result['count']} records for 'Machine Learning'")
            
            for record in result['progress']:
                assert record['skill'] == 'Machine Learning'
                print(f"   - Week {record['week_number']}: {record['topic']} ({'✓' if record['completed'] else '○'})")
            
            # Test 5: Update existing progress record
            print("\n" + "=" * 60)
            print("TEST 5: Update Existing Progress Record")
            print("=" * 60)
            
            update_data = {
                'skill': 'Machine Learning',
                'week_number': 3,
                'topic': 'Decision Trees',
                'completed': True  # Change from False to True
            }
            
            response = client.post(
                '/api/routine/progress/weekly',
                data=json.dumps(update_data),
                headers=headers
            )
            
            assert response.status_code == 200
            result = response.get_json()
            assert result['success'] == True
            assert result['progress']['completed'] == True
            print(f"✅ Updated: {result['progress']['topic']} marked as completed")
            
            # Test 6: Get progress summary
            print("\n" + "=" * 60)
            print("TEST 6: Get Progress Summary")
            print("=" * 60)
            
            response = client.get(
                '/api/routine/progress/summary',
                headers=headers
            )
            
            assert response.status_code == 200
            result = response.get_json()
            assert result['success'] == True
            assert result['total_skills'] >= 2
            print(f"✅ Retrieved summary for {result['total_skills']} skills")
            
            for skill_summary in result['summary']:
                print(f"\n   Skill: {skill_summary['skill']}")
                print(f"   Total Topics: {skill_summary['total_topics']}")
                print(f"   Completed: {skill_summary['completed_topics']}")
                print(f"   Completion: {skill_summary['completion_percentage']}%")
                print(f"   Status: {skill_summary['status']}")
            
            # Test 7: Validation - Missing fields
            print("\n" + "=" * 60)
            print("TEST 7: Validation - Missing Required Fields")
            print("=" * 60)
            
            invalid_data = {
                'skill': 'Python',
                'week_number': 1
                # Missing 'topic' and 'completed'
            }
            
            response = client.post(
                '/api/routine/progress/weekly',
                data=json.dumps(invalid_data),
                headers=headers
            )
            
            assert response.status_code == 400
            result = response.get_json()
            assert result['success'] == False
            print(f"✅ Validation working: {result['message']}")
            
            # Test 8: Validation - Invalid week number
            print("\n" + "=" * 60)
            print("TEST 8: Validation - Invalid Week Number")
            print("=" * 60)
            
            invalid_data = {
                'skill': 'Python',
                'week_number': -1,
                'topic': 'Test Topic',
                'completed': True
            }
            
            response = client.post(
                '/api/routine/progress/weekly',
                data=json.dumps(invalid_data),
                headers=headers
            )
            
            assert response.status_code == 400
            result = response.get_json()
            assert result['success'] == False
            print(f"✅ Validation working: {result['message']}")
            
            print("\n" + "=" * 60)
            print("ALL TESTS PASSED ✅")
            print("=" * 60)
            print("\nSummary:")
            print("✅ Create progress record")
            print("✅ Create multiple records")
            print("✅ Get all progress")
            print("✅ Get filtered progress")
            print("✅ Update existing record")
            print("✅ Get progress summary")
            print("✅ Validation - missing fields")
            print("✅ Validation - invalid data")
            
            return True
            
    except AssertionError as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_progress_tracking_api()
    sys.exit(0 if success else 1)
