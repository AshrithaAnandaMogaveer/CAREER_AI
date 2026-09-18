"""
Mistral Local LLM Integration for Career Guidance Chat
Supports both LM Studio (recommended) and llama-cpp-python
Falls back to rule-based responses if model unavailable
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from datetime import datetime
from routineChatAI import RoutineChatAI


class MistralLocalChat:
    """
    Enhanced chat AI with local Mistral LLM integration
    Supports LM Studio API and llama-cpp-python
    Maintains backward compatibility with existing RoutineChatAI
    """
    
    def __init__(self, lm_studio_url: Optional[str] = None, model_path: Optional[str] = None):
        """
        Initialize Mistral Local Chat
        
        Args:
            lm_studio_url: LM Studio API URL (e.g., http://localhost:1234/v1)
            model_path: Path to GGUF model file for llama-cpp-python (optional)
        """
        self.lm_studio_url = lm_studio_url or os.getenv('LM_STUDIO_URL', 'http://localhost:1234/v1')
        self.model_path = model_path or os.getenv('MISTRAL_MODEL_PATH')
        self.fallback_ai = RoutineChatAI()
        self.llm = None
        self.use_mistral = False
        self.use_lm_studio = False
        self.lm_studio_model = None  # Store the actual model name from LM Studio
        
        # Try to initialize Mistral model (LM Studio first, then llama-cpp-python)
        self._initialize_mistral()
    
    def _initialize_mistral(self):
        """Initialize local Mistral model - tries LM Studio first, then llama-cpp-python"""
        
        # Try LM Studio first (better performance)
        if self._try_lm_studio():
            return
        
        # Fallback to llama-cpp-python
        self._try_llama_cpp()
    
    def _try_lm_studio(self) -> bool:
        """Try to connect to LM Studio"""
        try:
            print(f"🔄 Checking LM Studio at {self.lm_studio_url}...")
            
            # Test connection to LM Studio and get model name
            response = requests.get(
                f"{self.lm_studio_url}/models",
                timeout=2
            )
            
            if response.status_code == 200:
                models = response.json()
                if models.get('data') and len(models['data']) > 0:
                    self.use_lm_studio = True
                    self.use_mistral = True
                    self.lm_studio_model = models['data'][0].get('id', 'local-model')
                    print(f"✅ LM Studio connected successfully!")
                    print(f"   Using model: {self.lm_studio_model}")
                    return True
                else:
                    print("⚠️ LM Studio is running but no model loaded.")
                    print("   Please load a model in LM Studio and restart.")
            
        except requests.exceptions.ConnectionError:
            print("⚠️ LM Studio not running or not accessible.")
            print("   Start LM Studio and load a model, or use llama-cpp-python.")
        except Exception as e:
            print(f"⚠️ Error connecting to LM Studio: {str(e)}")
        
        return False
    
    def _try_llama_cpp(self):
        """Try to initialize llama-cpp-python"""
        try:
            from llama_cpp import Llama
            
            if not self.model_path or not os.path.exists(self.model_path):
                print("⚠️ Mistral model not found. Using fallback AI.")
                print(f"   Set MISTRAL_MODEL_PATH or start LM Studio")
                return
            
            print(f"🔄 Loading Mistral model from {self.model_path}...")
            
            # Initialize Llama model with Mistral
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=2048,  # Context window
                n_threads=4,  # CPU threads
                n_gpu_layers=0,  # Set to > 0 if you have GPU support
                verbose=False
            )
            
            self.use_mistral = True
            self.use_lm_studio = False
            print("✅ Mistral model loaded successfully (llama-cpp-python)!")
            
        except ImportError:
            print("⚠️ llama-cpp-python not installed. Using fallback AI.")
            print("   Install with: pip install llama-cpp-python")
        except Exception as e:
            print(f"⚠️ Error loading Mistral model: {str(e)}")
            print("   Using fallback AI.")
    
    def generate_response(
        self,
        user_question: str,
        routine_data: Dict[str, Any] = None,
        progress_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate AI response using Mistral LLM or fallback
        
        Args:
            user_question: User's question
            routine_data: Current routine information
            progress_data: User's progress information
        
        Returns:
            Dictionary with response and optional action items
        """
        try:
            # Use Mistral if either LM Studio or llama-cpp is available
            if self.use_mistral:
                return self._generate_mistral_response(
                    user_question, routine_data, progress_data
                )
            else:
                # Fallback to rule-based AI
                return self.fallback_ai.generate_response(
                    user_question, routine_data, progress_data
                )
        
        except Exception as e:
            print(f"Error in Mistral generation: {str(e)}")
            # Always fallback on error
            return self.fallback_ai.generate_response(
                user_question, routine_data, progress_data
            )
    
    def _generate_mistral_response(
        self,
        user_question: str,
        routine_data: Dict[str, Any],
        progress_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate response using local Mistral model (LM Studio or llama-cpp-python)"""
        
        # Build context-aware prompt
        prompt = self._build_career_guidance_prompt(
            user_question, routine_data, progress_data
        )
        
        try:
            # Use LM Studio if available (better performance)
            if self.use_lm_studio:
                generated_text = self._generate_with_lm_studio(prompt)
            else:
                generated_text = self._generate_with_llama_cpp(prompt)
            
            # Parse response and extract action items
            parsed_response = self._parse_mistral_output(generated_text)
            
            # Detect category using fallback AI's logic
            category = self.fallback_ai._detect_category(user_question.lower())
            
            source = 'mistral_lm_studio' if self.use_lm_studio else 'mistral_local'
            
            return {
                'success': True,
                'response': parsed_response['text'],
                'action_items': parsed_response['action_items'],
                'category': category,
                'timestamp': datetime.now().isoformat(),
                'source': source
            }
        
        except Exception as e:
            print(f"Mistral generation error: {str(e)}")
            # Fallback to rule-based on any error
            return self.fallback_ai.generate_response(
                user_question, routine_data, progress_data
            )
    
    def _generate_with_lm_studio(self, prompt: str) -> str:
        """Generate response using LM Studio API"""
        try:
            # Combine system context with user prompt since some models don't support system role
            full_prompt = f"""You are an expert Career Guidance AI Mentor specializing in helping people learn technical skills and advance their careers. Provide practical, actionable advice with empathy and encouragement.

{prompt}"""
            
            response = requests.post(
                f"{self.lm_studio_url}/chat/completions",
                json={
                    "model": self.lm_studio_model,  # Use the actual model name from LM Studio
                    "messages": [
                        {
                            "role": "user",
                            "content": full_prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 512,
                    "stream": False
                },
                timeout=60  # Increased timeout for first request
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                # Enhanced error logging to see what LM Studio is actually saying
                try:
                    error_json = response.json()
                    error_detail = f"{response.status_code} - {error_json}"
                except:
                    error_detail = f"{response.status_code} - {response.text}"
                
                print(f"❌ LM Studio API Error Details:")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text[:500]}")  # First 500 chars
                raise Exception(f"LM Studio API error: {error_detail}")
                
        except Exception as e:
            print(f"LM Studio generation error: {str(e)}")
            raise
    
    def _generate_with_llama_cpp(self, prompt: str) -> str:
        """Generate response using llama-cpp-python"""
        response = self.llm(
            prompt,
            max_tokens=512,
            temperature=0.7,
            top_p=0.9,
            stop=["User:", "Question:", "\n\n\n"],
            echo=False
        )
        
        return response['choices'][0]['text'].strip()
    
    def _build_career_guidance_prompt(
        self,
        user_question: str,
        routine_data: Dict[str, Any],
        progress_data: Dict[str, Any]
    ) -> str:
        """Build context-aware prompt for Mistral"""
        
        # Build user context
        context_parts = []
        
        if routine_data:
            total_weeks = routine_data.get('projection', {}).get('total_weeks', 0)
            hours_per_week = routine_data.get('metadata', {}).get('available_hours_per_week', 0)
            skills_count = len(routine_data.get('prioritized_skills', []))
            
            if total_weeks and hours_per_week:
                context_parts.append(f"The user has a {total_weeks}-week learning routine with {hours_per_week} hours per week.")
            if skills_count:
                context_parts.append(f"They need to learn {skills_count} skills.")
            
            # Add current week info
            weekly_schedule = routine_data.get('weekly_schedule', [])
            if weekly_schedule:
                current_week = weekly_schedule[0]
                skills = current_week.get('skills', [])
                if skills:
                    skill_names = ', '.join([s.get('name', '') for s in skills[:3]])
                    context_parts.append(f"Current week focus: {skill_names}.")
        
        if progress_data:
            completion = progress_data.get('overall_completion', 0)
            skills_completed = progress_data.get('skills_completed', 0)
            
            if completion:
                context_parts.append(f"Progress: {completion:.0f}% complete, {skills_completed} skills completed.")
        
        # Build the full prompt
        if context_parts:
            context_str = " ".join(context_parts)
            prompt = f"Context: {context_str}\n\nUser Question: {user_question}\n\nProvide helpful, encouraging career guidance advice (2-4 paragraphs). If relevant, suggest 2-3 action items."
        else:
            prompt = f"User Question: {user_question}\n\nProvide helpful, encouraging career guidance advice (2-4 paragraphs). If relevant, suggest 2-3 action items."
        
        return prompt
    
    def _parse_mistral_output(self, generated_text: str) -> Dict[str, Any]:
        """Parse Mistral output to extract text and action items"""
        
        # Look for action items in the response
        action_items = []
        response_text = generated_text
        
        # Common patterns for action items
        action_patterns = [
            "Action items:",
            "Next steps:",
            "To do:",
            "Action:",
            "Steps:",
            "Try:",
        ]
        
        # Try to extract action items
        for pattern in action_patterns:
            if pattern.lower() in generated_text.lower():
                parts = generated_text.split(pattern, 1)
                if len(parts) == 2:
                    response_text = parts[0].strip()
                    action_text = parts[1].strip()
                    
                    # Extract bullet points or numbered items
                    lines = action_text.split('\n')
                    for line in lines[:5]:  # Max 5 action items
                        line = line.strip()
                        # Remove bullets, numbers, dashes
                        line = line.lstrip('•-*123456789.() ')
                        if line and len(line) > 5:
                            action_items.append(line)
                    break
        
        # If no action items found, generate some based on context
        if not action_items:
            action_items = [
                'Review the advice provided',
                'Take action on the suggestions',
                'Track your progress'
            ]
        
        return {
            'text': response_text,
            'action_items': action_items[:5]  # Max 5 items
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            'using_mistral': self.use_mistral,
            'using_lm_studio': self.use_lm_studio,
            'lm_studio_url': self.lm_studio_url if self.use_lm_studio else None,
            'model_path': self.model_path,
            'model_loaded': self.llm is not None or self.use_lm_studio,
            'fallback_available': True
        }


# Singleton instance
_mistral_chat_instance = None


def get_mistral_chat(model_path: Optional[str] = None) -> MistralLocalChat:
    """Get or create singleton Mistral chat instance"""
    global _mistral_chat_instance
    
    if _mistral_chat_instance is None:
        _mistral_chat_instance = MistralLocalChat(model_path)
    
    return _mistral_chat_instance


if __name__ == "__main__":
    # Test the Mistral integration
    print("Testing Mistral Local Chat Integration...\n")
    
    chat = MistralLocalChat()
    
    # Show model info
    info = chat.get_model_info()
    print(f"Model Info: {json.dumps(info, indent=2)}\n")
    
    # Test 1: General question
    print("Test 1: General career guidance question")
    result1 = chat.generate_response(
        "How can I become a better Python developer?"
    )
    print(f"Success: {result1['success']}")
    print(f"Source: {result1.get('source', 'fallback')}")
    print(f"Response: {result1['response'][:200]}...\n")
    
    # Test 2: With routine data
    print("Test 2: Question with routine context")
    result2 = chat.generate_response(
        "How should I organize my study schedule?",
        routine_data={
            'weekly_schedule': [{'week': 1, 'skills': [{'name': 'Python', 'hours': 15}]}],
            'projection': {'total_weeks': 12, 'completion_date': '2026-06-01'},
            'metadata': {'available_hours_per_week': 15},
            'prioritized_skills': [{'skill': 'Python'}, {'skill': 'React'}]
        }
    )
    print(f"Success: {result2['success']}")
    print(f"Category: {result2.get('category', 'unknown')}")
    print(f"Action Items: {result2.get('action_items', [])}\n")
    
    # Test 3: Motivation
    print("Test 3: Motivational question")
    result3 = chat.generate_response(
        "I'm feeling overwhelmed with all the things to learn",
        progress_data={'overall_completion': 25, 'skills_completed': 2}
    )
    print(f"Success: {result3['success']}")
    print(f"Response length: {len(result3['response'])} chars\n")
    
    print("✅ All tests completed!")
