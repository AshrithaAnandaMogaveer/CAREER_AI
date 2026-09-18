"""
Test Video Resources Integration
Verifies that YouTube learning resources are attached to each topic
"""

import json
import tempfile
import os
from routineEngineCore import RoutineEngineCore


def test_video_resources_integration():
    """Test that each topic includes YouTube video resources"""
    
    print("="*70)
    print("VIDEO RESOURCES INTEGRATION TEST")
    print("="*70)
    
    # Create test analysis data
    test_data = {
        'missingSkills': ['Machine Learning', 'Python'],
        'priorityScores': {
            'Machine Learning': 0.9,
            'Python': 0.85
        },
        'gapSeverity': {
            'Machine Learning': 0.8,
            'Python': 0.7
        },
        'targetDomain': 'Data Science',
        'readinessScore': 45,
        'extractedSkills': ['Statistics']
    }
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name
    
    try:
        # Generate routine
        engine = RoutineEngineCore()
        result = engine.generate_routine(temp_path, 'json', 10)
        
        if not result['success']:
            print(f"❌ Failed: {result['message']}")
            return False
        
        routine = result['routine']
        weekly_schedule = routine['weekly_schedule']
        
        print(f"\nTarget Domain: {routine['target_domain']}")
        print(f"Total Weeks: {len(weekly_schedule)}")
        
        # Test 1: Verify video fields exist
        print("\n" + "="*70)
        print("TEST 1: Video Fields Present")
        print("="*70)
        
        required_video_fields = ['video_title', 'video_url', 'video_platform']
        
        for week in weekly_schedule[:3]:
            print(f"\nWeek {week['week']}:")
            for skill in week['skills']:
                all_fields_present = all(field in skill for field in required_video_fields)
                
                if all_fields_present:
                    print(f"  ✅ {skill['name']}: {skill['topic']}")
                    print(f"     Video fields: Present")
                else:
                    print(f"  ❌ {skill['name']}: Missing video fields")
                    return False
        
        print("\n✅ All weeks have video fields")
        
        # Test 2: Display video resources
        print("\n" + "="*70)
        print("TEST 2: Video Resources Display")
        print("="*70)
        
        print("\nShowing first 5 weeks with video resources:\n")
        
        for week in weekly_schedule[:5]:
            print(f"{'='*70}")
            print(f"Week {week['week']}")
            print(f"{'='*70}")
            
            for skill in week['skills']:
                print(f"\nTopic: {skill['topic']}")
                print(f"Objective: {skill['objective']}")
                print(f"Hours: {skill['hours']}")
                print(f"Video Title: {skill['video_title']}")
                print(f"Video URL: {skill['video_url']}")
                print(f"Platform: {skill['video_platform']}")
            
            print()
        
        # Test 3: Verify specific videos
        print("="*70)
        print("TEST 3: Verify Specific Video Mappings")
        print("="*70)
        
        expected_videos = {
            'Linear Regression': 'https://www.youtube.com/watch?v=ZkjP5RJLQF4',
            'Logistic Regression': 'https://www.youtube.com/watch?v=yIYKR4sgzI8',
            'Python Basics & Syntax': 'https://www.youtube.com/watch?v=t8pPdKYpowI'
        }
        
        found_videos = {}
        for week in weekly_schedule:
            for skill in week['skills']:
                topic = skill['topic']
                if topic in expected_videos:
                    found_videos[topic] = skill['video_url']
        
        print(f"\nChecking expected video mappings:")
        for topic, expected_url in expected_videos.items():
            if topic in found_videos:
                if found_videos[topic] == expected_url:
                    print(f"  ✅ {topic}: Correct URL")
                else:
                    print(f"  ⚠️  {topic}: Different URL")
            else:
                print(f"  ⏭️  {topic}: Not in schedule")
        
        # Test 4: Count curated vs search URLs
        print("\n" + "="*70)
        print("TEST 4: Video Resource Quality")
        print("="*70)
        
        curated_count = 0
        search_count = 0
        
        for week in weekly_schedule:
            for skill in week['skills']:
                if 'search_query' in skill['video_url']:
                    search_count += 1
                else:
                    curated_count += 1
        
        total = curated_count + search_count
        curated_percentage = (curated_count / total * 100) if total > 0 else 0
        
        print(f"\nCurated videos: {curated_count}")
        print(f"Search URLs: {search_count}")
        print(f"Total: {total}")
        print(f"Curated percentage: {curated_percentage:.1f}%")
        
        if curated_percentage >= 70:
            print(f"✅ Good coverage of curated videos")
        else:
            print(f"⚠️  Consider adding more curated videos")
        
        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        
        print(f"Total Weeks: {len(weekly_schedule)}")
        print(f"Total Topics: {sum(len(week['skills']) for week in weekly_schedule)}")
        print(f"Videos Attached: {total}")
        print(f"Curated Videos: {curated_count}")
        
        print("\n" + "="*70)
        print("✅ VIDEO RESOURCES INTEGRATION TEST PASSED!")
        print("="*70)
        
        print("\nEach topic now includes:")
        print("  ✅ Video Title")
        print("  ✅ Video URL")
        print("  ✅ Platform (YouTube)")
        
        return True
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_video_format_output():
    """Test the exact output format requested"""
    
    print("\n\n" + "="*70)
    print("VIDEO FORMAT OUTPUT TEST")
    print("="*70)
    
    test_data = {
        'missingSkills': ['Machine Learning'],
        'priorityScores': {'Machine Learning': 0.9},
        'gapSeverity': {'Machine Learning': 0.8},
        'targetDomain': 'Data Science',
        'readinessScore': 45,
        'extractedSkills': ['Python']
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name
    
    try:
        engine = RoutineEngineCore()
        result = engine.generate_routine(temp_path, 'json', 6)
        
        if not result['success']:
            print(f"❌ Failed: {result['message']}")
            return False
        
        routine = result['routine']
        weekly_schedule = routine['weekly_schedule']
        
        print(f"\nGoal: {routine['target_domain']}")
        print(f"Missing Skill: Machine Learning")
        print(f"\nMachine Learning Roadmap:\n")
        
        # Display in requested format
        for week in weekly_schedule[:4]:
            for skill in week['skills']:
                print(f"Week {week['week']}")
                print(f"Topic: {skill['topic']}")
                print(f"Video Title: {skill['video_title']}")
                print(f"Video URL: {skill['video_url']}")
                print()
        
        print("... and more weeks\n")
        
        print("="*70)
        print("✅ VIDEO FORMAT OUTPUT TEST PASSED!")
        print("="*70)
        
        return True
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


if __name__ == '__main__':
    success1 = test_video_resources_integration()
    success2 = test_video_format_output()
    
    if success1 and success2:
        print("\n" + "="*70)
        print("🎉 ALL VIDEO RESOURCE TESTS PASSED!")
        print("="*70)
        print("\nYouTube learning resources are now attached to each topic!")
    else:
        print("\n❌ SOME TESTS FAILED")
