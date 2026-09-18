"""
Test Evolution Analytics with Monthly Progress
Verify that monthly aggregation works correctly
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

def test_monthly_progress():
    """Test monthly progress calculation"""
    print("=" * 60)
    print("TEST: Monthly Progress Calculation")
    print("=" * 60)
    
    try:
        from backend.evolution_analytics import EvolutionAnalytics
        
        analytics = EvolutionAnalytics()
        
        # Sample data spanning multiple months
        sample_records = [
            # March 2024
            {'skill': 'Python', 'week_number': 1, 'topic': 'Basics', 'completed': True, 'completed_at': '2024-03-01T10:00:00'},
            {'skill': 'Python', 'week_number': 2, 'topic': 'OOP', 'completed': True, 'completed_at': '2024-03-05T10:00:00'},
            {'skill': 'Python', 'week_number': 3, 'topic': 'Advanced', 'completed': True, 'completed_at': '2024-03-15T10:00:00'},
            
            # April 2024
            {'skill': 'React', 'week_number': 1, 'topic': 'Components', 'completed': True, 'completed_at': '2024-04-02T10:00:00'},
            {'skill': 'React', 'week_number': 2, 'topic': 'Hooks', 'completed': True, 'completed_at': '2024-04-10T10:00:00'},
            {'skill': 'React', 'week_number': 3, 'topic': 'State', 'completed': True, 'completed_at': '2024-04-20T10:00:00'},
            {'skill': 'React', 'week_number': 4, 'topic': 'Router', 'completed': True, 'completed_at': '2024-04-25T10:00:00'},
            
            # May 2024
            {'skill': 'Machine Learning', 'week_number': 1, 'topic': 'Linear Regression', 'completed': True, 'completed_at': '2024-05-05T10:00:00'},
            {'skill': 'Machine Learning', 'week_number': 2, 'topic': 'Logistic Regression', 'completed': True, 'completed_at': '2024-05-12T10:00:00'},
        ]
        
        result = analytics.generate_analytics(sample_records)
        
        # Verify monthly_progress exists
        assert 'monthly_progress' in result, "Result should contain monthly_progress"
        monthly_progress = result['monthly_progress']
        
        print("\n✅ Monthly Progress Data:")
        for month_data in monthly_progress:
            print(f"\n   {month_data['month_label']}:")
            print(f"   - Completed Topics: {month_data['completed_topics']}")
            print(f"   - Cumulative Total: {month_data['cumulative_topics']}")
            print(f"   - Growth Rate: {month_data['growth_rate']}%")
        
        # Verify structure
        assert len(monthly_progress) == 3, "Should have 3 months of data"
        assert monthly_progress[0]['month_label'] == 'Mar 2024'
        assert monthly_progress[1]['month_label'] == 'Apr 2024'
        assert monthly_progress[2]['month_label'] == 'May 2024'
        
        # Verify counts
        assert monthly_progress[0]['completed_topics'] == 3, "March should have 3 topics"
        assert monthly_progress[1]['completed_topics'] == 4, "April should have 4 topics"
        assert monthly_progress[2]['completed_topics'] == 2, "May should have 2 topics"
        
        # Verify cumulative
        assert monthly_progress[0]['cumulative_topics'] == 3
        assert monthly_progress[1]['cumulative_topics'] == 7
        assert monthly_progress[2]['cumulative_topics'] == 9
        
        print("\n✅ All monthly progress checks passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_complete_analytics_structure():
    """Test that all analytics components work together"""
    print("\n" + "=" * 60)
    print("TEST: Complete Analytics Structure")
    print("=" * 60)
    
    try:
        from backend.evolution_analytics import EvolutionAnalytics
        
        analytics = EvolutionAnalytics()
        
        sample_records = [
            {'skill': 'Python', 'week_number': 1, 'topic': 'Basics', 'completed': True, 'completed_at': '2024-03-01T10:00:00'},
            {'skill': 'Python', 'week_number': 2, 'topic': 'OOP', 'completed': True, 'completed_at': '2024-03-05T10:00:00'},
            {'skill': 'React', 'week_number': 1, 'topic': 'Components', 'completed': True, 'completed_at': '2024-04-02T10:00:00'},
            {'skill': 'React', 'week_number': 2, 'topic': 'Hooks', 'completed': False, 'completed_at': None},
        ]
        
        result = analytics.generate_analytics(sample_records)
        
        # Verify all required fields
        required_fields = ['daily_progress', 'weekly_progress', 'monthly_progress', 'skill_completion', 'overall_metrics']
        for field in required_fields:
            assert field in result, f"Result should contain {field}"
            print(f"✅ {field}: Present")
        
        # Verify data types
        assert isinstance(result['daily_progress'], list)
        assert isinstance(result['weekly_progress'], list)
        assert isinstance(result['monthly_progress'], list)
        assert isinstance(result['skill_completion'], list)
        assert isinstance(result['overall_metrics'], dict)
        
        print("\n✅ All structure checks passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("TESTING EVOLUTION ANALYTICS WITH MONTHLY PROGRESS")
    print("=" * 60)
    
    test1 = test_monthly_progress()
    test2 = test_complete_analytics_structure()
    
    print("\n" + "=" * 60)
    if test1 and test2:
        print("ALL TESTS PASSED ✅")
        print("=" * 60)
        print("\nSummary:")
        print("✅ Monthly progress calculation")
        print("✅ Complete analytics structure")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED ❌")
        print("=" * 60)
        sys.exit(1)
