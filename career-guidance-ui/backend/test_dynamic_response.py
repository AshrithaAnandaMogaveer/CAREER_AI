"""
Quick test to verify dynamic responses are working
"""

from mistral_local_chat import get_mistral_chat

print("="*60)
print("Testing Dynamic Chatbot Response")
print("="*60)

# Get chat instance
chat = get_mistral_chat()

# Check status
info = chat.get_model_info()
print(f"\n✅ Integration Status:")
print(f"  Using Mistral: {info['using_mistral']}")
print(f"  Using LM Studio: {info['using_lm_studio']}")
print(f"  Model Loaded: {info['model_loaded']}")

if info['using_mistral']:
    print("\n🎯 Testing dynamic response...")
    
    # Test with a specific question
    result = chat.generate_response(
        "I'm interested in data science but currently work with Python. What should I focus on?",
        routine_data={'prioritized_skills': [{'skill': 'Python'}, {'skill': 'React'}]},
        progress_data={'overall_completion': 20}
    )
    
    print(f"\n📝 Response Source: {result.get('source', 'unknown')}")
    print(f"📏 Response Length: {len(result['response'])} characters")
    print(f"\n💬 Response Preview:")
    print(result['response'][:300] + "..." if len(result['response']) > 300 else result['response'])
    
    if result.get('source') == 'mistral_lm_studio':
        print("\n✅ SUCCESS! Dynamic responses are working!")
        print("   The chatbot is now using LM Studio for intelligent responses.")
    else:
        print("\n⚠️  Using fallback AI (template-based)")
        print("   Make sure LM Studio is running and restart Flask server.")
else:
    print("\n⚠️  Mistral not available - using fallback AI")
    print("   Start LM Studio and restart Flask server for dynamic responses.")

print("\n" + "="*60)
