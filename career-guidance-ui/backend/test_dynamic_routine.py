"""
Test Dynamic Routine Generation with Topic-Based Roadmaps
Verifies that routines are generated with specific weekly topics instead of generic objectives
"""

import json
import tempfile
import os
from routineEngineCore import RoutineEngineCore


def test_dynamic_routine_generation():
    """Test that routine generation includes dynamic topic-based roadmaps"""
    
    print("="*70)
    print("DYNAMIC ROUTINE GENERATION TEST")
    print("="*70)
    
    # Create test analysis data
    test_data = {
        'missingSkills': ['Machine Learning', 'Python', 'SQL'],
        'priorityScores': {
            'Machine Learning': 0.9,
            'Python': 0.85,
            'SQL': 0.8
        },
        'gapSeverity': {
            'Machine Learning': 0.8,
            'Python': 0.7,
            'SQL': 0.6
        },
        'targetDomain': 'Data Science',
        'readinessScore': 45,
        'extractedSkills': ['Excel', 'Statistics']
    }
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name
    
    try:
        # Generate routine
        engine = RoutineEngineCore()
        result = engine.generate_routine(temp_path, 'json', 15)
        
        if not result['success']:
            print(f"❌ Routine generation failed: {result['message']}")
            return False
        
        routine = result['routine']
        
        # Test 1: Check skill roadmaps exist
        print("\n" + "="*70)
        print("TEST 1: Skill Roadmaps")
        print("="*70)
        
        if 'skill_roadmaps' not in routine:
            print("❌ FAILED: skill_roadmaps not in response")
            return False
        
        skill_roadmaps = routine['skill_roadmaps']
        print(f"✅ Found {len(skill_roadmaps)} skill roadmaps")
        
        # Test 2: Verify each skill has topics
        print("\n" + "="*70)
        print("TEST 2: Topics for Each Skill")
        print("="*70)
        
        for roadmap in skill_roadmaps:
            skill_name = roadmap['skill']
            topics = roadmap.get('topics', [])
            
            print(f"\n{skill_name}:")
            print(f"  Total Topics: {len(topics)}")
            print(f"  Hours per Topic: {roadmap.get('hours_per_topic', 0)}")
            print(f"  Has Custom Mapping: {roadmap.get('has_custom_mapping', False)}")
            
            if len(topics) == 0:
                print(f"  ❌ FAILED: No topics found for {skill_name}")
                return False
            
            # Show first 3 topics
            print(f"  Sample Topics:")
            for i, topic in enumerate(topics[:3], 1):
                print(f"    Week {i}: {topic}")
            
            if len(topics) > 3:
                print(f"    ... and {len(topics) - 3} more topics")
        
        print("\n✅ All skills have topics")
        
        # Test 3: Verify weekly schedule has topics
        print("\n" + "="*70)
        print("TEST 3: Weekly Schedule with Topics")
        print("="*70)
        
        weekly_schedule = routine['weekly_schedule']
        print(f"Total Weeks: {len(weekly_schedule)}")
        
        # Check first 3 weeks
        for week in weekly_schedule[:3]:
            print(f"\nWeek {week['week']} ({week['start_date']} to {week['end_date']}):")
            print(f"  Total Hours: {week['total_hours']}")
            
            for skill in week['skills']:
                if 'topic' not in skill:
                    print(f"  ❌ FAILED: No topic found for {skill['name']}")
                    return False
                
                print(f"  • {skill['name']}: {skill['topic']}")
                print(f"    Hours: {skill['hours']}, Status: {skill['status']}")
                print(f"    Topic {skill.get('topic_number', '?')}/{skill.get('total_topics', '?')}")
        
        if len(weekly_schedule) > 3:
            print(f"\n  ... and {len(weekly_schedule) - 3} more weeks")
        
        print("\n✅ Weekly schedule includes specific topics")
        
        # Test 4: Verify Machine Learning roadmap
        print("\n" + "="*70)
        print("TEST 4: Machine Learning Roadmap (Detailed)")
        print("="*70)
        
        ml_roadmap = next((r for r in skill_roadmaps if r['skill'] == 'Machine Learning'), None)
        
        if not ml_roadmap:
            print("❌ FAILED: Machine Learning roadmap not found")
            return False
        
        print(f"Machine Learning Roadmap:")
        print(f"  Total Topics: {ml_roadmap['total_topics']}")
        print(f"  Estimated Hours: {ml_roadmap['estimated_hours']}")
        print(f"  Hours per Topic: {ml_roadmap['hours_per_topic']}")
        print(f"\n  Learning Path:")
        
        for i, topic_data in enumerate(ml_roadmap['topics'], 1):
            print(f"    Week {i}: {topic_data['topic']}")
            print(f"             Objective: {topic_data['objective']}")
        
        # Verify expected topics
        expected_topics = [
            'ML Fundamentals',
            'Linear Regression',
            'Logistic Regression',
            'Decision Trees'
        ]
        
        ml_topics_str = ' '.join([t['topic'] for t in ml_roadmap['topics']]).lower()
        found_topics = sum(1 for topic in expected_topics if topic.lower() in ml_topics_str)
        
        if found_topics >= 3:
            print(f"\n✅ Found {found_topics}/{len(expected_topics)} expected ML topics")
        else:
            print(f"\n⚠️  Only found {found_topics}/{len(expected_topics)} expected ML topics")
        
        # Test 5: Verify metadata
        print("\n" + "="*70)
        print("TEST 5: Metadata")
        print("="*70)
        
        metadata = routine.get('metadata', {})
        
        if metadata.get('dynamic_topics_enabled'):
            print("✅ Dynamic topics enabled: True")
        else:
            print("❌ FAILED: Dynamic topics not enabled")
            return False
        
        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        
        print(f"Target Domain: {routine['target_domain']}")
        print(f"Total Skills: {len(skill_roadmaps)}")
        print(f"Total Weeks: {routine['projection']['total_weeks']}")
        print(f"Total Hours: {routine['projection']['total_hours']}")
        print(f"Completion Date: {routine['projection']['completion_date']}")
        
        # Count total topics
        total_topics = sum(len(r['topics']) for r in skill_roadmaps)
        print(f"Total Learning Topics: {total_topics}")
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        print("\nDynamic routine generation is working correctly!")
        print("Each skill is broken down into specific weekly topics.")
        print("Routines are no longer generic - they provide detailed learning paths.")
        
        return True
        
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_multiple_skills():
    """Test with multiple skills to verify comprehensive roadmaps"""
    
    print("\n\n" + "="*70)
    print("COMPREHENSIVE TEST: Multiple Skills")
    print("="*70)
    
    test_data = {
        'missingSkills': ['React', 'Node.js', 'Docker', 'Git', 'MongoDB'],
        'priorityScores': {
            'React': 0.9,
            'Node.js': 0.85,
            'Docker': 0.8,
            'Git': 0.75,
            'MongoDB': 0.7
        },
        'gapSeverity': {
            'React': 0.8,
            'Node.js': 0.7,
            'Docker': 0.6,
            'Git': 0.5,
            'MongoDB': 0.6
        },
        'targetDomain': 'Web Development',
        'readinessScore': 40,
        'extractedSkills': ['HTML', 'CSS', 'JavaScript']
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name
    
    try:
        engine = RoutineEngineCore()
        result = engine.generate_routine(temp_path, 'json', 20)
        
        if not result['success']:
            print(f"❌ Failed: {result['message']}")
            return False
        
        routine = result['routine']
        skill_roadmaps = routine['skill_roadmaps']
        
        print(f"\nGenerated roadmaps for {len(skill_roadmaps)} skills:")
        
        for roadmap in skill_roadmaps:
            print(f"\n{roadmap['skill']}:")
            print(f"  Topics: {roadmap['total_topics']}")
            if roadmap['topics']:
                print(f"  Sample: {roadmap['topics'][0]['topic']}")
                print(f"  Objective: {roadmap['topics'][0]['objective']}")
        
        print(f"\n✅ Successfully generated {len(skill_roadmaps)} detailed roadmaps")
        print(f"Total learning path: {routine['projection']['total_weeks']} weeks")
        
        return True
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


if __name__ == '__main__':
    success1 = test_dynamic_routine_generation()
    success2 = test_multiple_skills()
    
    if success1 and success2:
        print("\n" + "="*70)
        print("🎉 ALL TESTS PASSED - DYNAMIC ROUTINE GENERATION WORKING!")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("❌ SOME TESTS FAILED")
        print("="*70)
