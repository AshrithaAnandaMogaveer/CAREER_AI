"""
Test Routine Generation API Response
Verify that the API returns dynamic topics and YouTube videos
"""

import sys
import os
import json
import tempfile

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

def test_routine_generation_response():
    """Test that routine generation returns dynamic topics and videos"""
    print("=" * 60)
    print("TESTING ROUTINE GENERATION API RESPONSE")
    print("=" * 60)
    
    try:
        # Import Flask app
        from flask_cors_config import app
        
        # Create test client
        client = app.test_client()
        
        with app.app_context():
            # Import models
            from user_model import User
            from community_models import db
            
            # Create test user
            test_user = User.query.filter_by(email='routine_test@example.com').first()
            
            if not test_user:
                test_user = User(
                    name='Routine Tester',
                    email='routine_test@example.com'
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
            
            # Create test analysis file
            print("\n📄 Creating test analysis file...")
            
            test_analysis = {
                'missingSkills': ['Python', 'Machine Learning', 'React'],
                'priorityScores': {
                    'Python': 0.9,
                    'Machine Learning': 0.85,
                    'React': 0.8
                },
                'gapSeverity': {
                    'Python': 0.8,
                    'Machine Learning': 0.7,
                    'React': 0.6
                },
                'targetDomain': 'Data Science',
                'readinessScore': 45,
                'extractedSkills': ['JavaScript', 'HTML', 'CSS']
            }
            
            # Create temporary JSON file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(test_analysis, f)
                temp_path = f.name
            
            print(f"✅ Test file created: {temp_path}")
            
            # Test routine generation
            print("\n" + "=" * 60)
            print("TEST: Generate Routine with Dynamic Topics and Videos")
            print("=" * 60)
            
            with open(temp_path, 'rb') as f:
                response = client.post(
                    '/api/routine/generate',
                    data={
                        'file': (f, 'analysis.json'),
                        'hoursPerWeek': '15'
                    },
                    headers={
                        'Authorization': f'Bearer {token}'
                    },
                    content_type='multipart/form-data'
                )
            
            # Clean up temp file
            os.unlink(temp_path)
            
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            result = response.get_json()
            
            assert result['success'] == True, "Response should be successful"
            assert 'routine' in result, "Response should contain routine"
            
            routine = result['routine']
            
            # Verify structure
            print("\n✅ Routine Structure:")
            print(f"   Target Domain: {routine['target_domain']}")
            print(f"   Readiness Score: {routine['readiness_score']}")
            print(f"   Skills Count: {len(routine['prioritized_skills'])}")
            
            # Check metadata
            assert 'metadata' in routine
            assert routine['metadata']['dynamic_topics_enabled'] == True
            print(f"\n✅ Dynamic Topics Enabled: {routine['metadata']['dynamic_topics_enabled']}")
            
            # Check skill_roadmaps
            assert 'skill_roadmaps' in routine, "Routine should contain skill_roadmaps"
            skill_roadmaps = routine['skill_roadmaps']
            
            print(f"\n✅ Skill Roadmaps ({len(skill_roadmaps)} skills):")
            for roadmap in skill_roadmaps:
                print(f"\n   Skill: {roadmap['skill']}")
                print(f"   Total Topics: {roadmap['total_topics']}")
                print(f"   Has Custom Mapping: {roadmap.get('has_custom_mapping', False)}")
                
                # Show first 3 topics
                topics = roadmap.get('topics', [])
                print(f"   Topics (showing first 3):")
                for i, topic_data in enumerate(topics[:3]):
                    print(f"      {i+1}. {topic_data['topic']}")
                    print(f"         Objective: {topic_data['objective']}")
            
            # Check weekly_schedule
            assert 'weekly_schedule' in routine, "Routine should contain weekly_schedule"
            weekly_schedule = routine['weekly_schedule']
            
            print(f"\n✅ Weekly Schedule ({len(weekly_schedule)} weeks):")
            
            # Check first 3 weeks
            for week in weekly_schedule[:3]:
                print(f"\n   Week {week['week']} ({week['start_date']} to {week['end_date']}):")
                print(f"   Total Hours: {week['total_hours']}")
                
                for skill_entry in week['skills']:
                    print(f"\n      Skill: {skill_entry['name']}")
                    print(f"      Topic: {skill_entry['topic']}")
                    print(f"      Objective: {skill_entry['objective']}")
                    print(f"      Hours: {skill_entry['hours']}")
                    
                    # VERIFY VIDEO FIELDS
                    assert 'video_title' in skill_entry, "Skill entry should have video_title"
                    assert 'video_url' in skill_entry, "Skill entry should have video_url"
                    assert 'video_platform' in skill_entry, "Skill entry should have video_platform"
                    
                    print(f"      📺 Video: {skill_entry['video_title']}")
                    print(f"      🔗 URL: {skill_entry['video_url']}")
                    print(f"      📱 Platform: {skill_entry['video_platform']}")
                    
                    # Verify it's not static
                    assert skill_entry['topic'] != 'Static Topic', "Topic should be dynamic"
                    assert 'youtube.com' in skill_entry['video_url'] or 'youtu.be' in skill_entry['video_url'], \
                        "Video URL should be a YouTube link"
            
            # Verify topics are different (not static)
            all_topics = []
            for week in weekly_schedule:
                for skill_entry in week['skills']:
                    all_topics.append(skill_entry['topic'])
            
            unique_topics = set(all_topics)
            print(f"\n✅ Topic Diversity:")
            print(f"   Total Topics: {len(all_topics)}")
            print(f"   Unique Topics: {len(unique_topics)}")
            print(f"   Sample Topics: {list(unique_topics)[:5]}")
            
            # Verify videos are present
            all_videos = []
            for week in weekly_schedule:
                for skill_entry in week['skills']:
                    all_videos.append(skill_entry['video_url'])
            
            unique_videos = set(all_videos)
            print(f"\n✅ Video Resources:")
            print(f"   Total Video Links: {len(all_videos)}")
            print(f"   Unique Videos: {len(unique_videos)}")
            
            print("\n" + "=" * 60)
            print("ALL CHECKS PASSED ✅")
            print("=" * 60)
            print("\nVerified:")
            print("✅ Dynamic topics enabled")
            print("✅ Skill roadmaps included")
            print("✅ Weekly schedule with topics")
            print("✅ Video titles present")
            print("✅ Video URLs present")
            print("✅ YouTube links valid")
            print("✅ Topics are dynamic (not static)")
            
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
    success = test_routine_generation_response()
    sys.exit(0 if success else 1)
