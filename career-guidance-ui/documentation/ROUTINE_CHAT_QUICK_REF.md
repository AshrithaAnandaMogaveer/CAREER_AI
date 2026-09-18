# Routine Chat AI - Quick Reference

## 🚀 Quick Start

### Start Backend
```bash
cd career-guidance-ui
python flask_cors_config.py
```

### Test Backend
```bash
cd career-guidance-ui/backend
python routineChatAI.py
```

### Use in UI
1. Login → Generate Routine → Chat Tab
2. Ask questions → Get AI guidance

## 📝 Question Examples

### Schedule
```
How should I follow my schedule?
When should I study?
What's the best daily routine?
```

### Motivation
```
I'm feeling stuck
I want to give up
This is too hard
```

### Progress
```
What's my progress?
How much have I completed?
Am I on track?
```

### Skills
```
How do I learn Python?
Tell me about React
What's the best way to learn Docker?
```

### Improvement
```
How can I improve?
Any tips for learning faster?
How do I optimize my routine?
```

## 🔌 API Endpoint

```
POST /api/routine/chat
Authorization: Bearer {token}
Content-Type: application/json

{
  "userQuestion": "How should I follow my schedule?",
  "routineData": { /* optional */ },
  "progressData": { /* optional */ }
}
```

## 📦 Response Format

```json
{
  "success": true,
  "response": "AI response text...",
  "action_items": ["Action 1", "Action 2"],
  "category": "schedule",
  "timestamp": "2026-02-28T10:30:00"
}
```

## 🎯 Categories

1. **schedule** - Time management
2. **improvement** - Optimization tips
3. **motivation** - Encouragement
4. **skill_specific** - Learning paths
5. **progress** - Completion insights
6. **general** - Overview

## ✅ Features

- Context-aware responses
- Personalized guidance
- Motivational support
- Action items
- Skill-specific advice
- Progress insights
- Isolated from Analyze AI

## 📁 Files

```
backend/routineChatAI.py          - AI module
flask_cors_config.py              - API endpoint
src/services/routineService.js    - Frontend service
src/pages/RoutineBuild.jsx        - UI integration
```

## 🔒 Security

- JWT authentication required
- Input validation (2-1000 chars)
- Safe string processing
- Error handling

## ⚡ Performance

- Response time: < 500ms
- No external API calls
- Pure Python logic
- Minimal memory usage

## 🐛 Troubleshooting

### "Authentication required"
→ Login again

### "Question is too short"
→ Type at least 2 characters

### Chat not responding
→ Check backend is running
→ Check browser console

## 📚 Documentation

- `ROUTINE_CHAT_AI_COMPLETE.md` - Full details
- `ROUTINE_CHAT_TESTING.md` - Testing guide
- `ROUTINE_CHAT_SUMMARY.md` - Summary
- `ROUTINE_CHAT_CHECKLIST.md` - Checklist

## 🎓 Example Conversation

**User**: "How should I follow my schedule?"

**AI**: "Here's how to follow your 10-week learning schedule:

**Daily Routine:**
• Dedicate 15 hours per week consistently
• Break study sessions into 1-2 hour blocks
• Take 10-minute breaks between sessions

**Weekly Structure:**
• Monday-Friday: Focus on new concepts
• Saturday: Review and projects
• Sunday: Rest or light review

Stay consistent and you'll complete by 2026-05-29!"

**Action Items:**
- Set daily study time
- Mark calendar for study sessions
- Prepare learning materials

---

**Ready to chat? Ask me anything about your learning routine! 💬**
