"""
Debug LM Studio Integration
Test LM Studio API directly to diagnose 400 errors
"""

import requests
import json


def test_lm_studio_connection():
    """Test basic connection to LM Studio"""
    
    print("="*60)
    print("LM Studio Diagnostic Test")
    print("="*60)
    
    lm_studio_url = "http://localhost:1234/v1"
    
    # Test 1: Check if LM Studio is running
    print("\n1. Testing connection to LM Studio...")
    try:
        response = requests.get(f"{lm_studio_url}/models", timeout=2)
        print(f"   ✅ Connected! Status: {response.status_code}")
        
        if response.status_code == 200:
            models = response.json()
            print(f"   Models available: {json.dumps(models, indent=2)}")
            
            if models.get('data') and len(models['data']) > 0:
                model_id = models['data'][0].get('id')
                print(f"   Using model: {model_id}")
            else:
                print("   ⚠️ No models loaded in LM Studio!")
                return
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
            return
            
    except Exception as e:
        print(f"   ❌ Connection failed: {str(e)}")
        return
    
    # Test 2: Try a simple chat completion
    print("\n2. Testing chat completion API...")
    
    test_prompts = [
        # Test 1: Simple prompt
        {
            "name": "Simple prompt",
            "messages": [
                {"role": "user", "content": "Hello, how are you?"}
            ]
        },
        # Test 2: With system message
        {
            "name": "With system message",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, how are you?"}
            ]
        },
        # Test 3: Career guidance style (what we actually use)
        {
            "name": "Career guidance style",
            "messages": [
                {
                    "role": "user",
                    "content": "You are an expert Career Guidance AI Mentor. User Question: How do I learn Python? Provide helpful advice."
                }
            ]
        }
    ]
    
    for i, test in enumerate(test_prompts, 1):
        print(f"\n   Test {i}: {test['name']}")
        
        try:
            payload = {
                "model": model_id,
                "messages": test['messages'],
                "temperature": 0.7,
                "max_tokens": 100,
                "stream": False
            }
            
            print(f"   Request: {json.dumps(payload, indent=6)}")
            
            response = requests.post(
                f"{lm_studio_url}/chat/completions",
                json=payload,
                timeout=30
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"   ✅ Success! Response: {content[:100]}...")
            else:
                print(f"   ❌ Error {response.status_code}")
                print(f"   Response: {response.text}")
                
                # Try to parse error details
                try:
                    error_json = response.json()
                    print(f"   Error details: {json.dumps(error_json, indent=6)}")
                except:
                    pass
                    
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
    
    # Test 3: Check LM Studio server logs
    print("\n3. Recommendations:")
    print("   - Check LM Studio console for error messages")
    print("   - Verify model is fully loaded (not just 'loading...')")
    print("   - Try restarting LM Studio")
    print("   - Check if model supports chat format")
    print("   - Ensure max_tokens doesn't exceed model's context window")
    
    print("\n" + "="*60)


if __name__ == '__main__':
    test_lm_studio_connection()
