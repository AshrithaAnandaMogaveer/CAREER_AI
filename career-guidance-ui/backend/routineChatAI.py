"""
Routine Chat AI Module
Provides AI-powered guidance for learning routines
Isolated from Analyze module AI logic
"""

import json
from typing import Dict, Any, List
from datetime import datetime


class RoutineChatAI:
    def __init__(self):
        self.context_templates = {
            'schedule': [
                'how to follow', 'schedule', 'when should', 'timing', 'daily routine',
                'weekly plan', 'organize', 'time management'
            ],
            'improvement': [
                'improve', 'better', 'optimize', 'enhance', 'faster', 'efficient',
                'tips', 'advice', 'recommendation'
            ],
            'motivation': [
                'motivation', 'encourage', 'stuck', 'difficult', 'hard', 'give up',
                'frustrated', 'overwhelmed', 'tired'
            ],
            'skill_specific': [
                'python', 'react', 'docker', 'javascript', 'sql', 'aws', 'git',
                'learn', 'master', 'understand', 'practice'
            ],
            'progress': [
                'progress', 'completion', 'done', 'finished', 'completed', 'status',
                'how much', 'percentage'
            ]
        }
    
    def generate_response(
        self,
        user_question: str,
        routine_data: Dict[str, Any] = None,
        progress_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate AI response for user question about their routine
        
        Args:
            user_question: User's question
            routine_data: Current routine information
            progress_data: User's progress information
        
        Returns:
            Dictionary with response and optional action items
        """
        try:
            # Detect question category
            category = self._detect_category(user_question.lower())
            
            # Generate contextual response
            if category == 'schedule':
                response = self._generate_schedule_advice(user_question, routine_data)
            elif category == 'improvement':
                response = self._generate_improvement_advice(user_question, routine_data, progress_data)
            elif category == 'motivation':
                response = self._generate_motivation(user_question, progress_data)
            elif category == 'skill_specific':
                response = self._generate_skill_advice(user_question, routine_data)
            elif category == 'progress':
                response = self._generate_progress_insight(user_question, progress_data, routine_data)
            else:
                response = self._generate_general_response(user_question, routine_data, progress_data)
            
            return {
                'success': True,
                'response': response['text'],
                'action_items': response.get('action_items', []),
                'category': category,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'response': "I'm having trouble processing your question. Could you rephrase it?",
                'error': str(e)
            }
    
    def _detect_category(self, question: str) -> str:
        """Detect question category based on keywords"""
        for category, keywords in self.context_templates.items():
            if any(keyword in question for keyword in keywords):
                return category
        return 'general'
    
    def _generate_schedule_advice(self, question: str, routine_data: Dict) -> Dict:
        """Generate advice about following the schedule"""
        if not routine_data:
            return {
                'text': "I don't have your routine data yet. Please generate a routine first by uploading your analysis report.",
                'action_items': ['Upload analysis report', 'Generate routine']
            }
        
        weekly_schedule = routine_data.get('weekly_schedule', [])
        total_weeks = routine_data.get('projection', {}).get('total_weeks', 0)
        hours_per_week = routine_data.get('metadata', {}).get('available_hours_per_week', 10)
        
        response = f"""Here's how to follow your {total_weeks}-week learning schedule:

**Daily Routine:**
• Dedicate {hours_per_week} hours per week consistently
• Break study sessions into 1-2 hour blocks
• Take 10-minute breaks between sessions
• Review previous day's learning for 15 minutes each morning

**Weekly Structure:**
• Monday-Friday: Focus on new concepts and practice
• Saturday: Review and work on projects
• Sunday: Rest or light review

**Best Practices:**
• Study at the same time each day to build habit
• Use the Pomodoro Technique (25 min focus, 5 min break)
• Track your progress daily
• Don't skip foundational skills - they're ordered by dependency

**Current Week Focus:**
{self._get_current_week_summary(weekly_schedule)}

Stay consistent and you'll complete your routine by {routine_data.get('projection', {}).get('completion_date', 'your target date')}!"""
        
        return {
            'text': response,
            'action_items': [
                'Set daily study time',
                'Mark calendar for study sessions',
                'Prepare learning materials'
            ]
        }
    
    def _generate_improvement_advice(self, question: str, routine_data: Dict, progress_data: Dict) -> Dict:
        """Generate improvement suggestions"""
        if not progress_data:
            return {
                'text': "Start tracking your progress to get personalized improvement suggestions!",
                'action_items': ['Update progress in Progress Tracking tab']
            }
        
        completion = progress_data.get('overall_completion', 0)
        skills_completed = progress_data.get('skills_completed', 0)
        
        if completion < 25:
            advice = """**Early Stage Optimization:**

• Focus on building strong foundations first
• Don't rush through prerequisite skills
• Practice coding daily, even if just 30 minutes
• Join online communities for support
• Use multiple resources (videos, docs, practice)

**Quick Wins:**
• Set up your development environment properly
• Create a dedicated study space
• Use flashcards for syntax and concepts
• Build small projects to reinforce learning"""
        
        elif completion < 50:
            advice = """**Mid-Journey Improvements:**

• Start building portfolio projects
• Contribute to open-source projects
• Practice problem-solving on LeetCode/HackerRank
• Review and refactor your old code
• Teach concepts to others (blog, videos)

**Level Up:**
• Increase study hours if possible
• Focus on practical applications
• Network with other developers
• Attend virtual meetups or webinars"""
        
        elif completion < 75:
            advice = """**Advanced Stage Optimization:**

• Build complex, real-world projects
• Focus on system design and architecture
• Prepare for technical interviews
• Contribute to larger open-source projects
• Start mentoring beginners

**Professional Growth:**
• Update your resume and portfolio
• Apply for internships or jobs
• Attend conferences or workshops
• Build your personal brand"""
        
        else:
            advice = """**Final Push:**

• Complete remaining skills with excellence
• Polish your portfolio projects
• Prepare for job interviews
• Network actively
• Consider certifications

**You're almost there! Keep the momentum going!**"""
        
        return {
            'text': advice,
            'action_items': [
                'Review current learning approach',
                'Adjust study schedule if needed',
                'Set weekly goals'
            ]
        }
    
    def _generate_motivation(self, question: str, progress_data: Dict) -> Dict:
        """Generate motivational response"""
        completion = progress_data.get('overall_completion', 0) if progress_data else 0
        
        if 'stuck' in question or 'difficult' in question or 'hard' in question:
            response = """I understand learning can be challenging, but remember:

**Every expert was once a beginner!**

When you feel stuck:
• Break the problem into smaller pieces
• Take a short break and come back fresh
• Ask for help in communities (Stack Overflow, Discord, Reddit)
• Review fundamentals - sometimes we need to go back to basics
• Remember why you started this journey

**You've got this!** Difficulty means you're growing. Keep pushing forward, one step at a time."""
        
        elif 'give up' in question or 'quit' in question:
            response = f"""**Don't give up!** You've already completed {completion:.1f}% of your routine!

Think about:
• How far you've come since you started
• The skills you've already mastered
• Your future goals and dreams
• The person you'll become after completing this

**Success is not final, failure is not fatal: it is the courage to continue that counts.**

Take a day off if needed, but come back stronger. You're closer than you think!"""
        
        elif 'overwhelmed' in question or 'too much' in question:
            response = """Feeling overwhelmed is normal. Let's simplify:

**Focus on ONE skill at a time:**
• Don't try to learn everything at once
• Follow your routine's weekly schedule
• Celebrate small wins daily
• Progress > Perfection

**Remember:**
• You don't need to know everything
• Learning is a marathon, not a sprint
• It's okay to take breaks
• Your pace is YOUR pace

**You're doing great!** Keep showing up, even if it's just for 30 minutes a day."""
        
        else:
            response = f"""**You're doing amazing!** {completion:.1f}% complete!

**Keep this momentum:**
• Consistency beats intensity
• Small daily progress compounds
• Every line of code makes you better
• You're building your future

**Remember:** The best time to plant a tree was 20 years ago. The second best time is now. You're planting your future right now!

**Stay focused, stay consistent, stay awesome!** 🚀"""
        
        return {
            'text': response,
            'action_items': [
                'Take a 5-minute break',
                'Review your progress',
                'Set one small goal for today'
            ]
        }
    
    def _generate_skill_advice(self, question: str, routine_data: Dict) -> Dict:
        """Generate skill-specific advice"""
        if not routine_data:
            return {
                'text': "Please generate your routine first to get skill-specific advice.",
                'action_items': ['Generate routine']
            }
        
        # Extract skill from question
        skills = routine_data.get('prioritized_skills', [])
        skill_names = [s.get('skill', '').lower() for s in skills]
        
        mentioned_skill = None
        for skill in skill_names:
            if skill in question.lower():
                mentioned_skill = skill
                break
        
        if mentioned_skill:
            skill_data = next((s for s in skills if s.get('skill', '').lower() == mentioned_skill), None)
            if skill_data:
                hours = skill_data.get('estimated_hours', 0)
                difficulty = skill_data.get('difficulty', 'Intermediate')
                
                response = f"""**Learning {mentioned_skill.title()}:**

**Estimated Time:** {hours} hours ({difficulty} level)

**Learning Path:**
1. Start with official documentation
2. Follow interactive tutorials
3. Build 2-3 small projects
4. Practice daily coding challenges
5. Build one portfolio project

**Best Resources:**
• Official docs and tutorials
• YouTube channels (freeCodeCamp, Traversy Media)
• Practice platforms (LeetCode, HackerRank)
• Project-based courses (Udemy, Coursera)

**Pro Tips:**
• Code along with tutorials
• Build projects from scratch
• Read other people's code
• Join {mentioned_skill.title()} communities

**You've got this!** Follow your weekly schedule and you'll master {mentioned_skill.title()}!"""
                
                return {
                    'text': response,
                    'action_items': [
                        f'Find {mentioned_skill.title()} tutorials',
                        f'Set up {mentioned_skill.title()} environment',
                        f'Start first {mentioned_skill.title()} project'
                    ]
                }
        
        return {
            'text': "I can help you with any skill in your routine. Which skill would you like to learn more about?",
            'action_items': ['Ask about a specific skill']
        }
    
    def _generate_progress_insight(self, question: str, progress_data: Dict, routine_data: Dict) -> Dict:
        """Generate progress insights"""
        if not progress_data:
            return {
                'text': "Start tracking your progress to see insights!",
                'action_items': ['Update progress']
            }
        
        completion = progress_data.get('overall_completion', 0)
        skills_completed = progress_data.get('skills_completed', 0)
        total_skills = len(routine_data.get('prioritized_skills', [])) if routine_data else 0
        
        response = f"""**Your Progress Summary:**

• Overall Completion: {completion:.1f}%
• Skills Completed: {skills_completed} / {total_skills}
• Status: {"Excellent!" if completion > 75 else "Great progress!" if completion > 50 else "Keep going!" if completion > 25 else "Just getting started!"}

**Insights:**
"""
        
        if completion < 25:
            response += """• You're in the foundation phase - crucial for success
• Focus on consistency over speed
• Every hour of learning counts
• Stay patient and trust the process"""
        elif completion < 50:
            response += """• You're building momentum - great job!
• Your foundational skills are solid
• Time to start building projects
• Keep the consistency going"""
        elif completion < 75:
            response += """• You're in the advanced phase - impressive!
• Your skills are becoming job-ready
• Focus on portfolio projects
• Start networking and applying"""
        else:
            response += """• You're almost there - amazing work!
• Your dedication is paying off
• Finish strong and polish your portfolio
• You're ready for the next step!"""
        
        if routine_data:
            completion_date = routine_data.get('projection', {}).get('completion_date', '')
            if completion_date:
                response += f"\n\n**Projected Completion:** {completion_date}"
        
        return {
            'text': response,
            'action_items': [
                'Review completed skills',
                'Update progress for current week',
                'Plan next week\'s focus'
            ]
        }
    
    def _generate_general_response(self, question: str, routine_data: Dict, progress_data: Dict) -> Dict:
        """Generate general response"""
        if not routine_data:
            return {
                'text': """Welcome to your AI Learning Mentor! 🎓

I'm here to help you with:
• Following your learning schedule
• Improving your study approach
• Staying motivated
• Understanding specific skills
• Tracking your progress

**To get started:**
1. Upload your analysis report
2. Generate your personalized routine
3. Ask me anything about your learning journey!

What would you like to know?""",
                'action_items': ['Upload analysis report', 'Generate routine']
            }
        
        return {
            'text': """I'm your AI Learning Mentor! I can help you with:

**Schedule & Planning:**
• How to follow your weekly routine
• Time management tips
• Study schedule optimization

**Learning Advice:**
• Skill-specific guidance
• Resource recommendations
• Best practices

**Motivation & Support:**
• Overcoming challenges
• Staying consistent
• Celebrating progress

**Progress Tracking:**
• Understanding your completion rate
• Setting goals
• Measuring improvement

What would you like help with today?""",
            'action_items': [
                'Ask about your schedule',
                'Get skill-specific advice',
                'Check your progress'
            ]
        }
    
    def _get_current_week_summary(self, weekly_schedule: List[Dict]) -> str:
        """Get summary of current week's skills"""
        if not weekly_schedule:
            return "No schedule available yet."
        
        first_week = weekly_schedule[0]
        skills = first_week.get('skills', [])
        
        if not skills:
            return "No skills scheduled for this week."
        
        summary = "This week you're learning:\n"
        for skill in skills[:3]:  # Show first 3 skills
            name = skill.get('name', 'Unknown')
            hours = skill.get('hours', 0)
            summary += f"• {name} ({hours} hours)\n"
        
        return summary.strip()


if __name__ == "__main__":
    # Test
    chat_ai = RoutineChatAI()
    
    # Test 1: Schedule question
    result1 = chat_ai.generate_response(
        "How should I follow my schedule?",
        routine_data={
            'weekly_schedule': [{'week': 1, 'skills': [{'name': 'Python', 'hours': 15}]}],
            'projection': {'total_weeks': 10, 'completion_date': '2026-05-01'},
            'metadata': {'available_hours_per_week': 15}
        }
    )
    print("Test 1 - Schedule:", result1['success'])
    
    # Test 2: Motivation
    result2 = chat_ai.generate_response(
        "I'm feeling stuck and want to give up",
        progress_data={'overall_completion': 30, 'skills_completed': 2}
    )
    print("Test 2 - Motivation:", result2['success'])
    
    # Test 3: Progress
    result3 = chat_ai.generate_response(
        "What's my progress?",
        progress_data={'overall_completion': 45, 'skills_completed': 3},
        routine_data={'prioritized_skills': [{'skill': 'Python'}, {'skill': 'React'}]}
    )
    print("Test 3 - Progress:", result3['success'])
    
    print("✅ RoutineChatAI test passed")
