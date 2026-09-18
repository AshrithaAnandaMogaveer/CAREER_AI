# Routine Chat AI Testing Guide

## Quick Test

### 1. Start Backend
```bash
cd career-guidance-ui
python flask_cors_config.py
```

### 2. Test Backend Module
```bash
cd career-guidance-ui/backend
python routineChatAI.py
```

Expected output:
```
Test 1 - Schedule: True
Test 2 - Motivation: True
Test 3 - Progress: True
✅ RoutineChatAI test passed
```

### 3. Test in UI

1. **Login** to the app
2. **Generate Routine**:
   - Upload `backend/test_analyze_sample.json`
   - Click "Generate Routine"
3. **Go to Chat Tab**: Click "Chat With AI"
4. **Test Questions**:

## Test Questions

### Schedule Questions
```
How should I follow my schedule?
When should I study?
How do I organize my time?
What's the best daily routine?
```

**Expected**: Detailed schedule advice with daily/weekly structure

### Motivation Questions
```
I'm feeling stuck
I want to give up
This is too hard
I'm overwhelmed
```

**Expected**: Encouraging response with practical solutions

### Progress Questions
```
What's my progress?
How much have I completed?
Am I on track?
```

**Expected**: Progress summary with completion percentage

### Skill Questions
```
How do I learn Python?
What's the best way to learn React?
Tell me about Docker
```

**Expected**: Skill-specific learning path and resources

### Improvement Questions
```
How can I improve?
Any tips for learning faster?
How do I optimize my routine?
```

**Expected**: Stage-appropriate improvement suggestions

### General Questions
```
Hello
What can you help me with?
Tell me about my routine
```

**Expected**: Welcome message with capabilities overview

## Expected Response Format

Every response should include:
```json
{
  "success": true,
  "response": "Detailed AI response text...",
  "action_items": [
    "Action 1",
    "Action 2",
    "Action 3"
  ],
  "category": "schedule|motivation|progress|skill_specific|improvement|general",
  "timestamp": "2026-02-28T10:30:00"
}
```

## UI Verification

### Chat Interface Should Show:
- ✅ User message with timestamp
- ✅ AI response with timestamp
- ✅ Action items (if any)
- ✅ Loading indicator while processing
- ✅ Smooth scrolling to new messages
- ✅ Input field clears after sending

### Response Quality Checks:
- ✅ Relevant to question asked
- ✅ Uses routine data when available
- ✅ Uses progress data when available
- ✅ Provides actionable advice
- ✅ Encouraging and supportive tone
- ✅ Well-formatted and readable

## Error Testing

### Test Invalid Inputs:

1. **Empty Question**:
   - Send empty message
   - Should not send (button disabled)

2. **Very Short Question**:
   - Send "a"
   - Should return error: "Question is too short"

3. **Very Long Question**:
   - Send 1001+ characters
   - Should return error: "Question is too long"

4. **No Authentication**:
   - Logout and try to chat
   - Should return error: "Authentication required"

## Integration Testing

### Test with Different States:

1. **No Routine Generated**:
   - Ask questions before generating routine
   - Should prompt to generate routine first

2. **Routine Generated, No Progress**:
   - Generate routine but don't update progress
   - Should provide general advice

3. **With Progress Data**:
   - Update some skill progress
   - Ask about progress
   - Should show accurate completion percentage

4. **Multiple Questions**:
   - Ask several questions in sequence
   - Each should get appropriate response

## Performance Testing

### Response Time:
- ✅ Should respond in < 1 second
- ✅ No lag in UI
- ✅ Smooth message display

### Memory Usage:
- ✅ No memory leaks
- ✅ Chat history doesn't slow down app
- ✅ Can handle 50+ messages

## Browser Testing

Test in:
- ✅ Chrome
- ✅ Firefox
- ✅ Edge
- ✅ Safari (if available)

## API Testing with curl

### Test Schedule Question:
```bash
curl -X POST http://localhost:5000/api/routine/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "userQuestion": "How should I follow my schedule?",
    "routineData": {
      "weekly_schedule": [{"week": 1, "skills": [{"name": "Python", "hours": 15}]}],
      "projection": {"total_weeks": 10, "completion_date": "2026-05-01"},
      "metadata": {"available_hours_per_week": 15}
    }
  }'
```

### Test Motivation:
```bash
curl -X POST http://localhost:5000/api/routine/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "userQuestion": "I want to give up",
    "progressData": {
      "overall_completion": 30,
      "skills_completed": 2
    }
  }'
```

### Test Progress:
```bash
curl -X POST http://localhost:5000/api/routine/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "userQuestion": "What is my progress?",
    "progressData": {
      "overall_completion": 45,
      "skills_completed": 3
    },
    "routineData": {
      "prioritized_skills": [
        {"skill": "Python"},
        {"skill": "React"},
        {"skill": "Docker"}
      ]
    }
  }'
```

## Success Criteria

✅ All backend tests pass
✅ API endpoint responds correctly
✅ UI displays messages properly
✅ Responses are relevant and helpful
✅ Action items are provided
✅ Error handling works
✅ No console errors
✅ No authentication issues
✅ Performance is acceptable
✅ Works in all browsers

## Common Issues & Solutions

### Issue: "Authentication required"
**Solution**: Login again to get fresh token

### Issue: "Question is too short"
**Solution**: Type at least 2 characters

### Issue: Chat not responding
**Solution**: 
- Check backend is running
- Check browser console for errors
- Verify authentication token

### Issue: Generic responses
**Solution**: 
- Generate routine first
- Update progress data
- Ask more specific questions

## Debugging

### Check Backend Logs:
```bash
# Look for errors in Flask terminal
# Check for successful API calls
```

### Check Browser Console:
```javascript
// Open DevTools (F12)
// Look for network errors
// Check API responses
```

### Check Response Data:
```javascript
// In browser console after chat
console.log(lastResponse);
```

## Conclusion

Follow this guide to thoroughly test the Routine Chat AI. All tests should pass before considering the feature complete.

**Happy Testing! 🧪**
