# Evolution Tracking Troubleshooting Guide

## Issue: Evolution Tab Shows "No Evolution Data Yet"

### Possible Causes & Solutions

### 1. No Progress Data Updated

**Symptom**: Evolution tab shows "No Evolution Data Yet" message

**Cause**: You haven't updated any progress yet

**Solution**:
1. Go to "Progress Tracking" tab
2. Move sliders to update skill completion (e.g., Python to 50%)
3. Click "Save Progress" for each skill
4. Go back to "Evolution Over Time" tab
5. Click "Load Evolution Data" or it should auto-load

### 2. Backend Not Running

**Symptom**: Clicking "Load Evolution Data" does nothing or shows error

**Cause**: Flask backend is not running

**Solution**:
```bash
cd career-guidance-ui
python flask_cors_config.py
```

Verify backend is running on `http://localhost:5000`

### 3. Authentication Issue

**Symptom**: Console shows "Authentication required" error

**Cause**: JWT token expired or missing

**Solution**:
1. Logout
2. Login again
3. Try loading evolution data again

### 4. Routine Not Generated

**Symptom**: Evolution tab doesn't auto-load

**Cause**: No routine has been generated yet

**Solution**:
1. Upload analysis file (JSON, PDF, or DOCX)
2. Click "Generate Routine"
3. Wait for routine to generate
4. Then go to Evolution tab

### 5. CORS Error

**Symptom**: Console shows CORS error

**Cause**: Backend CORS not configured for frontend URL

**Solution**:
Check `flask_cors_config.py` has correct origins:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://localhost:3000"],
        ...
    }
})
```

### 6. Progress Manager Not Persisting

**Symptom**: Evolution shows 0% for everything even after updating progress

**Cause**: Progress manager instance not shared

**Solution**:
Verify `flask_cors_config.py` has:
```python
_progress_manager_instance = None

def get_progress_manager():
    global _progress_manager_instance
    if _progress_manager_instance is None:
        from progressManager import ProgressManager
        _progress_manager_instance = ProgressManager()
    return _progress_manager_instance
```

And both endpoints use it:
```python
manager = get_progress_manager()
```

## Step-by-Step Testing

### Test 1: Update Progress

1. Generate a routine
2. Go to "Progress Tracking" tab
3. Update Python to 75%
4. Click "Save Progress"
5. Check browser console for success message
6. Verify no errors

**Expected**: Success message in console

### Test 2: Load Evolution

1. Go to "Evolution Over Time" tab
2. Should auto-load or click "Load Evolution Data"
3. Check browser console for API call
4. Check response data

**Expected**: 
- API call to `/api/routine/evolution`
- Response with `success: true`
- Data displayed in UI

### Test 3: Check Backend

```bash
# Test progress endpoint
curl -X POST http://localhost:5000/api/routine/progress \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "week": 1,
    "skill": "Python",
    "completionPercentage": 75,
    "date": "2026-02-28T10:00:00",
    "routineData": {...}
  }'

# Test evolution endpoint
curl -X POST http://localhost:5000/api/routine/evolution \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "routineData": {...}
  }'
```

## Browser Console Debugging

### Check for Errors

Open DevTools (F12) → Console tab

Look for:
- ❌ Network errors (red)
- ❌ Authentication errors
- ❌ CORS errors
- ❌ JavaScript errors

### Check Network Tab

Open DevTools (F12) → Network tab

1. Click "Load Evolution Data"
2. Look for `/api/routine/evolution` request
3. Check:
   - Status: Should be 200
   - Response: Should have `success: true`
   - Preview: Check data structure

### Check Response Data

In Console, after loading evolution:
```javascript
// Check what data was received
console.log(evolution);
```

Should show:
```javascript
{
  overall_completion: 25.5,
  monthly_growth_rate: 0,
  skills_completed: 0,
  skills_remaining: 3,
  dailyGraphData: [...],
  monthlyGraphData: [...],
  excellenceLevel: 15.2,
  motivational_message: "...",
  ...
}
```

## Common Issues

### Issue: "No module named 'progressManager'"

**Solution**:
```bash
cd career-guidance-ui/backend
# Verify file exists
ls progressManager.py

# Test import
python -c "from progressManager import ProgressManager; print('OK')"
```

### Issue: Evolution shows 0% for everything

**Cause**: No progress has been saved

**Solution**:
1. Update progress for at least one skill
2. Save it
3. Reload evolution

### Issue: "Routine data is required"

**Cause**: Routine not passed to evolution endpoint

**Solution**: Verify `loadEvolution()` passes routine:
```javascript
const result = await getRoutineEvolution(routine);
```

### Issue: Auto-load not working

**Cause**: useEffect dependencies

**Solution**: Check useEffect is present:
```javascript
useEffect(() => {
    if (activeTab === 'evolution' && routine && !evolution && !isLoadingEvolution) {
        loadEvolution();
    }
}, [activeTab, routine]);
```

## Verification Checklist

Before reporting an issue, verify:

- [ ] Backend is running (`python flask_cors_config.py`)
- [ ] Routine has been generated
- [ ] At least one skill progress has been updated and saved
- [ ] No errors in browser console
- [ ] No errors in backend terminal
- [ ] Authentication token is valid (not expired)
- [ ] CORS is configured correctly
- [ ] Progress manager is shared (global instance)
- [ ] Evolution endpoint returns data (test with curl)

## Expected Behavior

### When Working Correctly:

1. **Generate Routine**: Upload file → Generate → See weekly schedule
2. **Update Progress**: Go to Progress tab → Move slider → Save → See success
3. **View Evolution**: Go to Evolution tab → Auto-loads or click button → See:
   - Overall completion percentage
   - Monthly growth rate
   - Skills completed/remaining counts
   - Motivational message
   - Graph placeholders

### Data Flow:

```
User Updates Progress
  ↓
POST /api/routine/progress
  ↓
Stored in shared progress manager
  ↓
User Opens Evolution Tab
  ↓
POST /api/routine/evolution
  ↓
Reads from shared progress manager
  ↓
Computes metrics and graphs
  ↓
Returns data to frontend
  ↓
UI displays evolution data
```

## Still Not Working?

If evolution still doesn't show data:

1. **Restart Backend**:
   ```bash
   # Stop backend (Ctrl+C)
   # Start again
   python flask_cors_config.py
   ```

2. **Clear Browser Cache**:
   - Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
   - Or clear cache in DevTools

3. **Check Backend Logs**:
   - Look at terminal where Flask is running
   - Check for errors when calling endpoints

4. **Test Backend Directly**:
   - Use curl or Postman
   - Test progress endpoint first
   - Then test evolution endpoint
   - Verify responses

5. **Check File Modifications**:
   - Verify `flask_cors_config.py` has `get_progress_manager()`
   - Verify both endpoints use `get_progress_manager()`
   - Verify `loadEvolution()` transforms data correctly

## Contact Support

If issue persists, provide:
- Browser console errors (screenshot)
- Backend terminal output (screenshot)
- Network tab showing API calls (screenshot)
- Steps you followed
- What you expected vs what happened

---

**Most Common Solution**: Update progress first, then load evolution! 🚀
