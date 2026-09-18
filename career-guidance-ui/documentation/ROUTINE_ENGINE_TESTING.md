# Routine Engine Testing Guide

## Quick Start Testing

### 1. Backend Testing

Test individual modules:

```bash
cd career-guidance-ui/backend

# Test file parser
python fileParser.py

# Test skill difficulty estimator
python skillDifficultyEstimator.py

# Test weekly scheduler
python weeklyScheduler.py

# Test complete routine engine
python routineEngineCore.py
```

All tests should pass with ✅ messages.

### 2. Start Backend Server

```bash
cd career-guidance-ui
python flask_cors_config.py
```

Backend should start on `http://localhost:5000`

### 3. Test API Endpoint

#### Using curl (Windows PowerShell):

```powershell
# Create test JSON file
$testData = @{
    missingSkills = @('Python', 'React', 'Docker')
    priorityScores = @{
        Python = 0.9
        React = 0.8
        Docker = 0.7
    }
    gapSeverity = @{
        Python = 0.8
        React = 0.7
        Docker = 0.6
    }
    targetDomain = 'Software Development'
    readinessScore = 45
} | ConvertTo-Json

$testData | Out-File -FilePath test_analyze.json -Encoding utf8

# Get auth token (replace with your actual token)
$token = "your-jwt-token-here"

# Test API
curl -X POST http://localhost:5000/api/routine/generate `
  -H "Authorization: Bearer $token" `
  -F "file=@test_analyze.json" `
  -F "hoursPerWeek=15"
```

#### Using Postman:

1. **Method**: POST
2. **URL**: `http://localhost:5000/api/routine/generate`
3. **Headers**:
   - `Authorization`: `Bearer YOUR_TOKEN`
4. **Body** (form-data):
   - `file`: Select your JSON/PDF/DOCX file
   - `hoursPerWeek`: `15`

### 4. Frontend Testing

1. **Start React App**:
   ```bash
   cd career-guidance-ui
   npm start
   ```

2. **Login**:
   - Navigate to `http://localhost:3000`
   - Login with your credentials

3. **Test Routine Build**:
   - Click "Routine Build" in navbar
   - Upload a test file (JSON, PDF, or DOCX)
   - Click "Generate Routine"
   - Verify routine appears in "Routine To Follow" tab

### 5. Test File Formats

#### JSON Test File
Create `test_analyze.json`:
```json
{
  "missingSkills": ["Python", "React", "Docker", "Git"],
  "priorityScores": {
    "Python": 0.9,
    "React": 0.8,
    "Docker": 0.7,
    "Git": 0.8
  },
  "gapSeverity": {
    "Python": 0.8,
    "React": 0.7,
    "Docker": 0.6,
    "Git": 0.5
  },
  "targetDomain": "Software Development",
  "readinessScore": 45,
  "extractedSkills": ["JavaScript", "HTML", "CSS"]
}
```

#### PDF Test File
Create a PDF with text:
```
Career Analysis Report

Missing Skills:
- Python (Critical)
- React (High Priority)
- Docker (Medium Priority)

Target Domain: Software Development
Current Readiness: 45%
```

#### DOCX Test File
Create a Word document with similar content as PDF.

### 6. Expected Results

After generating routine, you should see:

1. **Prioritized Skills**:
   - Skills sorted by priority score
   - Difficulty levels assigned
   - Hour estimates calculated

2. **Weekly Schedule**:
   - Week-by-week breakdown
   - Skills allocated per week
   - Hours per skill
   - Start and end dates

3. **Projection**:
   - Total weeks
   - Total hours
   - Completion date
   - Skills count

### 7. Error Testing

Test error handling:

1. **No file uploaded**:
   - Don't select a file
   - Click "Generate Routine"
   - Should show error: "No file uploaded"

2. **Invalid file type**:
   - Upload a .txt or .xlsx file
   - Should show error: "Invalid file type"

3. **Invalid hours**:
   - Set hours to 0 or 200
   - Should show error: "Hours per week must be between 1 and 168"

4. **No authentication**:
   - Logout
   - Try to generate routine
   - Should show error: "Authentication required"

### 8. Integration Testing

Test complete flow:

1. **Analyze Module** → **Routine Build**:
   - Run resume analysis
   - Download analysis JSON
   - Upload to Routine Build
   - Generate routine
   - Verify skills match

2. **Progress Tracking**:
   - Mark skills as complete
   - Update progress
   - Verify routine recalculation

3. **Chat with AI**:
   - Ask questions about routine
   - Verify context-aware responses

4. **Evolution Tracking**:
   - Record snapshots
   - View progress graphs
   - Check completion percentage

### 9. Performance Testing

Test with different file sizes:

1. **Small file** (3-5 skills): Should complete in < 2 seconds
2. **Medium file** (10-15 skills): Should complete in < 5 seconds
3. **Large file** (20+ skills): Should complete in < 10 seconds

### 10. Browser Testing

Test in different browsers:
- Chrome
- Firefox
- Edge
- Safari (if available)

### Common Issues & Solutions

#### Issue: "No module named 'docx'"
**Solution**: 
```bash
pip install python-docx PyPDF2
```

#### Issue: "Token has expired"
**Solution**: 
- Logout and login again
- Get fresh JWT token

#### Issue: "File parsing failed"
**Solution**: 
- Verify file format (JSON, PDF, DOCX only)
- Check file content structure
- Ensure file is not corrupted

#### Issue: "Routine generation failed"
**Solution**: 
- Check backend logs
- Verify all backend modules are present
- Ensure dependencies are installed

### Success Criteria

✅ All backend module tests pass
✅ Flask server starts without errors
✅ API endpoint returns 200 status
✅ Frontend uploads file successfully
✅ Routine displays in UI
✅ Weekly schedule is generated
✅ All tabs work correctly
✅ No console errors
✅ No authentication issues

### Debugging Tips

1. **Check Backend Logs**:
   - Look for Python errors in terminal
   - Check Flask request logs

2. **Check Browser Console**:
   - Open DevTools (F12)
   - Look for network errors
   - Check API responses

3. **Verify File Content**:
   - Open JSON in text editor
   - Validate JSON syntax
   - Check required fields

4. **Test API Directly**:
   - Use Postman or curl
   - Bypass frontend
   - Isolate backend issues

## Automated Testing (Future)

Consider adding:
- Unit tests for each module
- Integration tests for API
- E2E tests for frontend
- Load testing for performance
- Security testing for vulnerabilities

## Conclusion

Follow this guide to thoroughly test the Routine Engine implementation. All tests should pass before deploying to production.
