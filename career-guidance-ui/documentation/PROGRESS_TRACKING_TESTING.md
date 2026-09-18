# Progress Tracking Testing Guide

## Quick Test

### 1. Start Backend
```bash
cd career-guidance-ui
python flask_cors_config.py
```

### 2. Test Backend Module
```bash
cd career-guidance-ui/backend
python progressManager.py
```

Expected output:
```
Test 1 - Update Progress: True
Overall Completion: 21.43%
Test 2 - Update Progress: True
Overall Completion: 48.21%
Test 3 - Evolution Data: True
Skills Completed: 0
✅ ProgressManager test passed
```

### 3. Test in UI

1. **Login** to the app
2. **Generate Routine**:
   - Upload analysis file
   - Click "Generate Routine"
3. **Go to Progress Tracking Tab**
4. **Update Progress**:
   - Move slider for a skill
   - Click "Save Progress"
   - Verify metrics update

## Test Scenarios

### Scenario 1: Update Single Skill

**Steps**:
1. Set Python to 50%
2. Click "Save Progress"

**Expected**:
- Overall completion updates
- Completed hours calculated
- Projected date recalculated
- Skills summary updated
- Success message shown

### Scenario 2: Complete a Skill

**Steps**:
1. Set React to 100%
2. Click "Save Progress"

**Expected**:
- Skills completed count increases
- Overall completion increases significantly
- Projected date moves closer
- Motivational message updates

### Scenario 3: Update Multiple Skills

**Steps**:
1. Set Python to 75%
2. Set React to 50%
3. Set Docker to 25%

**Expected**:
- Each update recalculates metrics
- Overall completion reflects all changes
- History stored for each skill

### Scenario 4: Check On-Track Status

**Steps**:
1. Update skills slowly (low completion)
2. Check projected date

**Expected**:
- `on_track: false` if behind schedule
- Projected date later than original
- Weeks remaining increases

**Steps**:
1. Update skills quickly (high completion)
2. Check projected date

**Expected**:
- `on_track: true` if ahead
- Projected date earlier than original
- Weeks remaining decreases

## API Testing

### Test Update Progress

```bash
curl -X POST http://localhost:5000/api/routine/progress \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "week": 2,
    "skill": "Python",
    "completionPercentage": 75.0,
    "date": "2026-03-07T10:30:00",
    "routineData": {
      "prioritized_skills": [
        {"skill": "Python", "estimated_hours": 60},
        {"skill": "React", "estimated_hours": 50},
        {"skill": "Docker", "estimated_hours": 30}
      ],
      "projection": {
        "total_weeks": 10,
        "total_hours": 140,
        "completion_date": "2026-05-01"
      },
      "metadata": {
        "available_hours_per_week": 15
      }
    }
  }'
```

**Expected Response**:
```json
{
  "success": true,
  "progress_metrics": {
    "overall_completion": 32.14,
    "completed_hours": 45.0,
    "total_hours": 140,
    "projected_completion_date": "2026-04-18",
    "weeks_remaining": 6,
    "on_track": true,
    "skills_completed": 0,
    "skills_in_progress": 1,
    "skills_not_started": 2,
    "total_skills": 3,
    "current_week": 2,
    "last_updated": "2026-03-07T10:30:00"
  },
  "skill_progress": {
    "Python": {
      "completion_percentage": 75.0,
      "week": 2,
      "last_updated": "2026-03-07T10:30:00"
    }
  },
  "message": "Progress updated for Python"
}
```

## Validation Testing

### Test Invalid Inputs

1. **Negative Completion**:
```json
{"completionPercentage": -10}
```
Expected: Error "Completion percentage must be between 0 and 100"

2. **Over 100 Completion**:
```json
{"completionPercentage": 150}
```
Expected: Error "Completion percentage must be between 0 and 100"

3. **Missing Week**:
```json
{"skill": "Python", "completionPercentage": 50}
```
Expected: Error "Missing required field: week"

4. **Invalid Week**:
```json
{"week": 0, "skill": "Python", "completionPercentage": 50}
```
Expected: Error "Week must be a positive integer"

5. **Missing Routine Data**:
```json
{"week": 1, "skill": "Python", "completionPercentage": 50}
```
Expected: Error "Routine data is required"

## Calculation Verification

### Test Overall Completion

**Given**:
- Python: 60 hours, 50% complete
- React: 50 hours, 75% complete
- Docker: 30 hours, 0% complete

**Calculation**:
```
Completed Hours:
- Python: 60 × 0.5 = 30
- React: 50 × 0.75 = 37.5
- Docker: 30 × 0 = 0
Total Completed: 67.5

Total Hours: 140

Overall Completion: (67.5 / 140) × 100 = 48.21%
```

**Verify**: Response shows `overall_completion: 48.21`

### Test Projected Completion

**Given**:
- Total Hours: 140
- Overall Completion: 48.21%
- Hours per Week: 15

**Calculation**:
```
Remaining: 100 - 48.21 = 51.79%
Remaining Hours: 140 × 0.5179 = 72.5
Weeks Needed: 72.5 / 15 = 4.83 (5 weeks)
New Date: Current + 5 weeks
```

**Verify**: Response shows correct `projected_completion_date` and `weeks_remaining`

### Test Skills Summary

**Given**:
- Python: 100% (completed)
- React: 50% (in progress)
- Docker: 0% (not started)

**Expected**:
```json
{
  "skills_completed": 1,
  "skills_in_progress": 1,
  "skills_not_started": 1,
  "total_skills": 3
}
```

## UI Verification

### Progress Tracking Tab

**Should Display**:
- ✅ List of all skills
- ✅ Slider for each skill (0-100)
- ✅ Current completion percentage
- ✅ Save button per skill
- ✅ Loading indicator while saving
- ✅ Success message after save

### Metrics Display

**Should Show**:
- ✅ Overall completion percentage
- ✅ Completed hours / Total hours
- ✅ Skills completed count
- ✅ Skills in progress count
- ✅ Projected completion date
- ✅ On-track status
- ✅ Weeks remaining

### Evolution Tab

**Should Display**:
- ✅ Daily progress graph
- ✅ Monthly progress graph
- ✅ Overall completion
- ✅ Skills completed
- ✅ Motivational message

## Performance Testing

### Response Time
- ✅ Progress update: < 100ms
- ✅ Evolution data: < 200ms
- ✅ No lag in UI
- ✅ Smooth slider movement

### Memory Usage
- ✅ No memory leaks
- ✅ History limited to 100 entries
- ✅ Efficient calculations

## Browser Testing

Test in:
- ✅ Chrome
- ✅ Firefox
- ✅ Edge
- ✅ Safari (if available)

## Integration Testing

### Test Complete Flow

1. **Generate Routine**
2. **Update Progress** for skill 1
3. **Verify** metrics update
4. **Update Progress** for skill 2
5. **Verify** overall completion increases
6. **Complete** a skill (100%)
7. **Verify** skills completed count increases
8. **Check Evolution** tab
9. **Verify** graphs show data

### Test with Chat

1. **Update Progress** to 50%
2. **Go to Chat** tab
3. **Ask** "What's my progress?"
4. **Verify** AI shows correct completion

## Error Testing

### Test Network Errors

1. **Stop backend**
2. **Try to save progress**
3. **Expected**: Error message shown

### Test Authentication Errors

1. **Logout**
2. **Try to save progress**
3. **Expected**: "Authentication required"

### Test Invalid Data

1. **Modify request** to send invalid data
2. **Expected**: Appropriate error message

## Success Criteria

✅ All backend tests pass
✅ API endpoint responds correctly
✅ Calculations are accurate
✅ UI updates properly
✅ Metrics display correctly
✅ History is stored
✅ Evolution data works
✅ Error handling works
✅ No console errors
✅ No authentication issues
✅ Performance is acceptable
✅ Works in all browsers

## Common Issues & Solutions

### Issue: "Routine data is required"
**Solution**: Generate routine first before updating progress

### Issue: Metrics not updating
**Solution**: 
- Check backend is running
- Verify routine data is passed
- Check browser console for errors

### Issue: Completion percentage not saving
**Solution**:
- Verify slider moved
- Click "Save Progress" button
- Check authentication token

### Issue: Projected date incorrect
**Solution**:
- Verify hours per week in routine
- Check total hours calculation
- Ensure all skills have estimated hours

## Debugging

### Check Backend Logs
```bash
# Look for errors in Flask terminal
# Check for successful API calls
```

### Check Browser Console
```javascript
// Open DevTools (F12)
// Look for network errors
// Check API responses
```

### Check Response Data
```javascript
// In browser console after save
console.log(progressMetrics);
```

## Conclusion

Follow this guide to thoroughly test the Progress Tracking system. All tests should pass before considering the feature complete.

**Happy Testing! 🧪**
