# Test: Progress Tracking to Evolution Charts

## Complete Testing Guide

### Step 1: Generate a Routine
1. Go to Routine Build page
2. Upload an analysis report (JSON/PDF/DOCX)
3. Click "Generate Routine"
4. Wait for routine to be generated
5. Verify you see the weekly schedule

### Step 2: Save Progress
1. Click on "Progress Tracking" tab
2. For Python skill:
   - Move slider to 50%
   - Click "Save" button
   - Wait for "Progress saved!" alert
   - Verify slider stays at 50% (doesn't reset)
3. For React skill:
   - Move slider to 75%
   - Click "Save" button
   - Wait for alert
4. For Machine Learning:
   - Move slider to 25%
   - Click "Save" button
   - Wait for alert

### Step 3: Verify Progress Persists
1. Refresh the page (F5)
2. Upload the same analysis file again
3. Click "Generate Routine"
4. Go to "Progress Tracking" tab
5. Verify sliders show saved values:
   - Python: 50%
   - React: 75%
   - Machine Learning: 25%

### Step 4: Check Backend Data
Open browser console (F12) and run:

```javascript
// Check if topic records were created
fetch('http://localhost:5000/api/routine/progress/weekly', {
    headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('token')
    }
})
.then(r => r.json())
.then(d => {
    console.log('Total progress records:', d.count);
    console.log('Records:', d.progress);
    console.log('Skills tracked:', [...new Set(d.progress.map(p => p.skill))]);
})

// Check analytics data
fetch('http://localhost:5000/api/routine/evolution/analytics', {
    headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('token')
    }
})
.then(r => r.json())
.then(d => {
    console.log('Analytics:', d.analytics);
    console.log('Daily progress points:', d.analytics.daily_progress.length);
    console.log('Weekly progress points:', d.analytics.weekly_progress.length);
    console.log('Monthly progress points:', d.analytics.monthly_progress.length);
    console.log('Skills:', d.analytics.skill_completion.length);
})
```

### Step 5: View Evolution Charts
1. Go to "Evolution Over Time" tab
2. Click "Refresh Data" button
3. Verify you see:
   - ✅ Metrics dashboard with numbers
   - ✅ Daily Progress chart (line chart)
   - ✅ Weekly Progress chart (bar chart)
   - ✅ Monthly Progress chart (line chart)
   - ✅ Skill Completion chart (donut chart)

### Expected Results

#### Progress Tracking Tab:
- Sliders show saved values after page refresh
- Save button creates topic records in background
- Alert confirms successful save

#### Evolution Tab:
- Metrics show correct numbers:
  - Overall: ~50% (average of all skills)
  - Completed: X topics
  - Remaining: Y topics
- Charts display with data points
- No "No data" message

#### Console Output:
```
Total progress records: 12
Skills tracked: ["Python", "React", "Machine Learning"]
Daily progress points: 1
Weekly progress points: 6
Monthly progress points: 1
Skills: 3
```

## Troubleshooting

### Issue: Progress resets to 0
**Cause:** Not loading saved progress from backend
**Fix:** Check browser console for errors, verify token is valid

### Issue: Evolution shows "No data"
**Cause:** Topic records not being created
**Fix:** 
1. Check console logs when clicking Save
2. Should see: "Creating X topic records for [skill]"
3. Should see: "Successfully created X/X topic records"
4. If 0/X, check backend API is running

### Issue: Charts don't display
**Cause:** Analytics endpoint returning empty arrays
**Fix:**
1. Run console commands from Step 4
2. Verify progress records exist
3. Verify analytics returns data
4. Check for JavaScript errors in console

### Issue: 401 Unauthorized
**Cause:** Token expired or invalid
**Fix:**
1. Logout and login again
2. Generate new routine
3. Try saving progress again

## Backend Verification

### Check Database Directly:
```bash
cd career-guidance-ui/backend
python -c "
from flask_cors_config import app, db
from progress_tracking_model import RoutineProgress

with app.app_context():
    records = RoutineProgress.query.all()
    print(f'Total records: {len(records)}')
    for r in records[:5]:
        print(f'  {r.skill} - Week {r.week_number}: {r.topic} - {\"✓\" if r.completed else \"○\"}')
"
```

### Test Analytics Directly:
```bash
cd career-guidance-ui/backend
python -c "
from evolution_analytics import EvolutionAnalytics
from flask_cors_config import app, db
from progress_tracking_model import RoutineProgress

with app.app_context():
    records = RoutineProgress.query.filter_by(user_id=1).all()
    data = [r.to_dict() for r in records]
    
    analytics = EvolutionAnalytics()
    result = analytics.generate_analytics(data)
    
    print('Daily progress:', len(result['daily_progress']))
    print('Weekly progress:', len(result['weekly_progress']))
    print('Monthly progress:', len(result['monthly_progress']))
    print('Skills:', len(result['skill_completion']))
"
```

## Success Criteria

✅ Progress values persist after page refresh
✅ Topic records created when saving progress
✅ Evolution tab shows 4 charts with data
✅ Metrics dashboard shows correct numbers
✅ No console errors
✅ Backend has progress records in database

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Slider resets to 0 | Fixed: Now loads from backend |
| Evolution shows no data | Fixed: Auto-creates topic records |
| Charts don't render | Check console for errors |
| 401 errors | Re-login to get new token |
| Backend not running | Start Flask server: `python flask_cors_config.py` |

## Quick Debug Commands

```javascript
// Check if logged in
console.log('Token:', localStorage.getItem('token') ? 'Present' : 'Missing');

// Check routine data
console.log('Routine:', routine);
console.log('Weekly schedule:', routine?.weekly_schedule?.length, 'weeks');

// Check progress state
console.log('Skill progress:', skillProgress);

// Check evolution state
console.log('Evolution data:', evolution);
```

## Final Verification

After completing all steps, you should be able to:
1. ✅ Save progress and see it persist
2. ✅ View evolution charts with real data
3. ✅ See daily/weekly/monthly trends
4. ✅ Monitor skill completion percentages
5. ✅ Get motivational feedback

If all checks pass, the integration is working correctly! 🎉
