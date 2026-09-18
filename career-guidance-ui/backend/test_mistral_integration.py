"""
Integration tests for Mistral Local Chat
Verifies that the integration doesn't break existing features
"""

import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))


def test_fallback_compatibility():
    """Test that fallback AI works exactly like before"""
    print("\n" + "="*60)
    print("TEST 1: Fallback Compatibility")
    print("="*60)
    
    try:
        from routineChatAI import RoutineChatAI
        
        chat_ai = RoutineChatAI()
        
        # Test various question types
        test_cases = [
            {
                'question': 'How should I follow my schedule?',
                'routine_data': {
                    'weekly_schedule': [{'week': 1, 'skills': [{'name': 'Python', 'hours': 15}]}],
                    'projection': {'total_weeks': 10, 'completion_date': '2026-05-01'},
                    'metadata': {'available_hours_per_week': 15}
                },
                'expected_category': 'schedule'
            },
            {
                'question': 'I feel stuck and overwhelmed',
                'progress_data': {'overall_completion': 30, 'skills_completed': 2},
                'expected_category': 'motivation'
            },
            {
                'question': 'What is my progress?',
                'progress_data': {'overall_completion': 45, 'skills_completed': 3},
                'routine_data': {'prioritized_skills': [{'skill': 'Python'}, {'skill': 'React'}]},
                'expected_category': 'progress'
            }
        ]
        
        all_passed = True
        for i, test in enumerate(test_cases, 1):
            result = chat_ai.generate_response(
                test['question'],
                test.get('routine_data'),
                test.get('progress_data')
            )
            
            passed = (
                result['success'] and
                result['category'] == test['expected_category'] and
                len(result['response']) > 50
            )
            
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"\n  Test Case {i}: {status}")
            print(f"    Question: {test['question']}")
            print(f"    Expected Category: {test['expected_category']}")
            print(f"    Actual Category: {result['category']}")
            print(f"    Response Length: {len(result['response'])} chars")
            
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n✅ All fallback tests PASSED")
            return True
        else:
            print("\n❌ Some fallback tests FAILED")
            return False
            
    except Exception as e:
        print(f"\n❌ Fallback test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_mistral_integration():
    """Test Mistral integration with automatic fallback"""
    print("\n" + "="*60)
    print("TEST 2: Mistral Integration")
    print("="*60)
    
    try:
        from mistral_local_chat import get_mistral_chat
        
        chat = get_mistral_chat()
        
        # Check model info
        info = chat.get_model_info()
        print(f"\n  Model Info:")
        print(f"    Using Mistral: {info['using_mistral']}")
        print(f"    Using LM Studio: {info.get('using_lm_studio', False)}")
        if info.get('lm_studio_url'):
            print(f"    LM Studio URL: {info['lm_studio_url']}")
        print(f"    Model Loaded: {info['model_loaded']}")
        print(f"    Fallback Available: {info['fallback_available']}")
        
        # Test response generation
        test_questions = [
            "How can I become a better Python developer?",
            "I'm feeling overwhelmed with learning",
            "What's my current progress?"
        ]
        
        all_passed = True
        for i, question in enumerate(test_questions, 1):
            result = chat.generate_response(
                question,
                routine_data={'prioritized_skills': [{'skill': 'Python'}]},
                progress_data={'overall_completion': 35, 'skills_completed': 3}
            )
            
            passed = (
                result['success'] and
                len(result['response']) > 50 and
                'action_items' in result and
                'category' in result
            )
            
            status = "✅ PASS" if passed else "❌ FAIL"
            source = result.get('source', 'fallback')
            print(f"\n  Test {i}: {status}")
            print(f"    Question: {question}")
            print(f"    Source: {source}")
            print(f"    Response Length: {len(result['response'])} chars")
            print(f"    Action Items: {len(result.get('action_items', []))}")
            
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n✅ All Mistral integration tests PASSED")
            return True
        else:
            print("\n❌ Some Mistral integration tests FAILED")
            return False
            
    except Exception as e:
        print(f"\n❌ Mistral integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_response_format_consistency():
    """Test that both Mistral and fallback return same format"""
    print("\n" + "="*60)
    print("TEST 3: Response Format Consistency")
    print("="*60)
    
    try:
        from mistral_local_chat import get_mistral_chat
        from routineChatAI import RoutineChatAI
        
        question = "How should I organize my study time?"
        routine_data = {
            'weekly_schedule': [{'week': 1, 'skills': [{'name': 'Python', 'hours': 15}]}],
            'projection': {'total_weeks': 12},
            'metadata': {'available_hours_per_week': 15}
        }
        
        # Get responses from both
        mistral_chat = get_mistral_chat()
        fallback_chat = RoutineChatAI()
        
        mistral_result = mistral_chat.generate_response(question, routine_data)
        fallback_result = fallback_chat.generate_response(question, routine_data)
        
        # Check required fields
        required_fields = ['success', 'response', 'action_items', 'category', 'timestamp']
        
        mistral_has_all = all(field in mistral_result for field in required_fields)
        fallback_has_all = all(field in fallback_result for field in required_fields)
        
        print(f"\n  Mistral Response:")
        print(f"    Has all required fields: {mistral_has_all}")
        print(f"    Fields: {list(mistral_result.keys())}")
        
        print(f"\n  Fallback Response:")
        print(f"    Has all required fields: {fallback_has_all}")
        print(f"    Fields: {list(fallback_result.keys())}")
        
        if mistral_has_all and fallback_has_all:
            print("\n✅ Response format consistency test PASSED")
            return True
        else:
            print("\n❌ Response format consistency test FAILED")
            return False
            
    except Exception as e:
        print(f"\n❌ Format consistency test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_error_handling():
    """Test error handling and graceful degradation"""
    print("\n" + "="*60)
    print("TEST 4: Error Handling")
    print("="*60)
    
    try:
        from mistral_local_chat import get_mistral_chat
        
        chat = get_mistral_chat()
        
        # Test with invalid inputs
        test_cases = [
            {'question': '', 'should_handle': True},
            {'question': 'a', 'should_handle': True},
            {'question': 'Valid question?', 'should_handle': True},
        ]
        
        all_passed = True
        for i, test in enumerate(test_cases, 1):
            try:
                result = chat.generate_response(test['question'])
                
                # Should always return a response (even if fallback)
                passed = 'success' in result and 'response' in result
                
                status = "✅ PASS" if passed else "❌ FAIL"
                print(f"\n  Test {i}: {status}")
                print(f"    Input: '{test['question']}'")
                print(f"    Success: {result.get('success', False)}")
                print(f"    Has Response: {'response' in result}")
                
                if not passed:
                    all_passed = False
                    
            except Exception as e:
                print(f"\n  Test {i}: ❌ FAIL (Exception)")
                print(f"    Error: {str(e)}")
                all_passed = False
        
        if all_passed:
            print("\n✅ Error handling test PASSED")
            return True
        else:
            print("\n❌ Error handling test FAILED")
            return False
            
    except Exception as e:
        print(f"\n❌ Error handling test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_no_breaking_changes():
    """Verify no breaking changes to existing API"""
    print("\n" + "="*60)
    print("TEST 5: No Breaking Changes")
    print("="*60)
    
    try:
        # Test that old import still works
        from routineChatAI import RoutineChatAI
        
        # Test that new import works
        from mistral_local_chat import get_mistral_chat, MistralLocalChat
        
        # Test that both can be instantiated
        old_chat = RoutineChatAI()
        new_chat = get_mistral_chat()
        
        # Test that both have the same interface
        question = "Test question"
        
        old_result = old_chat.generate_response(question)
        new_result = new_chat.generate_response(question)
        
        # Both should return valid responses
        old_valid = old_result['success'] and 'response' in old_result
        new_valid = new_result['success'] and 'response' in new_result
        
        print(f"\n  Old API (RoutineChatAI):")
        print(f"    Can import: ✅")
        print(f"    Can instantiate: ✅")
        print(f"    Returns valid response: {'✅' if old_valid else '❌'}")
        
        print(f"\n  New API (MistralLocalChat):")
        print(f"    Can import: ✅")
        print(f"    Can instantiate: ✅")
        print(f"    Returns valid response: {'✅' if new_valid else '❌'}")
        
        if old_valid and new_valid:
            print("\n✅ No breaking changes test PASSED")
            return True
        else:
            print("\n❌ No breaking changes test FAILED")
            return False
            
    except Exception as e:
        print(f"\n❌ Breaking changes test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("MISTRAL INTEGRATION TEST SUITE")
    print("="*60)
    print("\nThis test suite verifies:")
    print("1. Fallback AI still works correctly")
    print("2. Mistral integration works (or falls back gracefully)")
    print("3. Response formats are consistent")
    print("4. Error handling is robust")
    print("5. No breaking changes to existing code")
    
    results = []
    
    # Run all tests
    results.append(("Fallback Compatibility", test_fallback_compatibility()))
    results.append(("Mistral Integration", test_mistral_integration()))
    results.append(("Response Format Consistency", test_response_format_consistency()))
    results.append(("Error Handling", test_error_handling()))
    results.append(("No Breaking Changes", test_no_breaking_changes()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED - Integration is safe to use!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed - Review before deployment")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
