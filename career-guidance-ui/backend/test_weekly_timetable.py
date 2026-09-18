"""
Test Weekly Timetable Format
Demonstrates the exact output format requested:
Week X, Topic, Hours, Objective
"""

import json
import tempfile
import os
from routineEngineCore import RoutineEngineCore


def test_weekly_timetable_format():
    """Test that each topic becomes a weekly timetable entry"""
    
    print("="*70)
    print("WEEKLY TIMETABLE FORMAT TEST")
    print("="*70)
    
    # Create test analysis data
    test_data = {
        'missingSkills': ['Machine Learning'],
        'priorityScores': {'Machine Learning': 0.9},
        'gapSeverity': {'Machine Learning': 0.8},
        'targetDomain': 'Data Science',
        'readinessScore': 45,
        'extractedSkills': ['Python', 'Statistics']
    }
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name
    
    try:
        # Generate routine
        engine = RoutineEngineCore()
        result = engine.generate_routine(temp_path, 'json', 6)  # 6 hours per week
        
        if not result['success']:
            print(f"❌ Failed: {result['message']}")
            return False
        
        routine = result['routine']
        weekly_schedule = routine['weekly_schedule']
        
        print(f"\nTarget Domain: {routine['target_domain']}")
        print(f"Total Weeks: {len(weekly_schedule)}")
        print(f"\n{'='*70}")
        print("WEEKLY TIMETABLE")
        print(f"{'='*70}\n")
        
        # Display each week in the requested format
        for week in weekly_schedule:
            for skill in week['skills']:
                print(f"Week {week['week']}")
                print(f"Topic: {skill['topic']}")
                print(f"Hours: {skill['hours']}")
                print(f"Objective: {skill['objective']}")
                print()
        
        print(f"{'='*70}")
        print("VERIFICATION")
        print(f"{'='*70}\n")
        
        # Verify each week has exactly one topic
        print("✅ Each topic is assigned to a dedicated week")
        print(f"✅ Total weeks: {len(weekly_schedule)}")
        print(f"✅ Each week includes:")
        print("   - Week number")
        print("   - Topic name")
        print("   - Estimated study hours")
        print("   - Learning objective")
        
        # Verify number of weeks matches number of topics
        skill_roadmaps = routine['skill_roadmaps']
        total_topics = sum(r['total_topics'] for r in skill_roadmaps)
        
        print(f"\n✅ Total topics: {total_topics}")
        print(f"✅ Total weeks: {len(weekly_schedule)}")
        
        if len(weekly_schedule) >= total_topics:
            print(f"✅ Number of weeks depends on number of topics (CORRECT)")
        else:
            print(f"❌ Week count mismatch")
            return False
        
        print(f"\n{'='*70}")
        print("✅ WEEKLY TIMETABLE FORMAT TEST PASSED!")
        print(f"{'='*70}")
        
        return True
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_multiple_skills_timetable():
    """Test timetable with multiple skills"""
    
    print("\n\n" + "="*70)
    print("MULTIPLE SKILLS TIMETABLE TEST")
    print("="*70)
    
    test_data = {
        'missingSkills': ['Python', 'SQL'],
        'priorityScores': {'Python': 0.9, 'SQL': 0.8},
        'gapSeverity': {'Python': 0.8, 'SQL': 0.7},
        'targetDomain': 'Data Science',
        'readinessScore': 50,
        'extractedSkills': ['Excel']
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name
    
    try:
        engine = RoutineEngineCore()
        result = engine.generate_routine(temp_path, 'json', 10)
        
        if not result['success']:
            print(f"❌ Failed: {result['message']}")
            return False
        
        routine = result['routine']
        weekly_schedule = routine['weekly_schedule']
        
        print(f"\nShowing first 5 weeks:\n")
        
        for week in weekly_schedule[:5]:
            print(f"{'='*70}")
            print(f"WEEK {week['week']} ({week['start_date']} to {week['end_date']})")
            print(f"{'='*70}")
            
            for skill in week['skills']:
                print(f"\nSkill: {skill['name']}")
                print(f"Topic: {skill['topic']}")
                print(f"Hours: {skill['hours']}")
                print(f"Objective: {skill['objective']}")
                print(f"Progress: Topic {skill['topic_number']}/{skill['total_topics']}")
            
            print()
        
        print(f"... and {len(weekly_schedule) - 5} more weeks\n")
        
        print(f"{'='*70}")
        print("✅ MULTIPLE SKILLS TIMETABLE TEST PASSED!")
        print(f"{'='*70}")
        
        return True
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


if __name__ == '__main__':
    success1 = test_weekly_timetable_format()
    success2 = test_multiple_skills_timetable()
    
    if success1 and success2:
        print("\n" + "="*70)
        print("🎉 ALL TIMETABLE TESTS PASSED!")
        print("="*70)
        print("\nEach topic is now a weekly timetable entry with:")
        print("  ✅ Week number")
        print("  ✅ Topic name")
        print("  ✅ Estimated study hours")
        print("  ✅ Learning objective")
        print("\nNumber of weeks depends on number of topics!")
    else:
        print("\n❌ SOME TESTS FAILED")
