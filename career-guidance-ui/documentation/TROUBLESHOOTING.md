# Troubleshooting Guide

## Issue: "Server Error. Try Again" when creating community/feedback/blog

### Root Cause
CORS (Cross-Origin Resource Sharing) preflight requests returning 404.

### Symptoms
- Browser console shows OPTIONS requests with 404 status
- POST requests never reach the server
- Frontend shows "Server error. Try again."

### Solution

#### Step 1: Stop Flask Server
Press `CTRL+C` in the terminal where Flask is running.

#### Step 2: Verify Changes Applied
The file `flask_cors_config.py` should have these changes:

**CORS Configuration (around line 40):**
```python
CORS(app, 
     resources={r"/api/*": {"origins": "*"}},
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True,
     expose_headers=["Content-Type", "Authorization"]
)
```

**Preflight Handler (around line 1145):**
```python
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        return response
```

#### Step 3: Restart Flask
```bash
cd C:\Users\amash\Desktop\PROJECT_4\Intelligent_Career_Guidance_Project\career-guidance-ui
python flask_cors_config.py
```

#### Step 4: Clear Browser Cache
- Press `Ctrl+Shift+Delete`
- Select "Cached images and files"
- Click "Clear data"

OR do a hard refresh:
- Press `Ctrl+Shift+R` (Windows/Linux)
- Or `Cmd+Shift+R` (Mac)

#### Step 5: Test Again
1. Go to Community page
2. Try creating a community
3. Try submitting feedback
4. Try creating a blog

### Verification

**Before Fix:**
```
127.0.0.1 - - [01/Mar/2026 15:40:20] "OPTIONS /api/community/feed HTTP/1.1" 404 -
```

**After Fix:**
```
127.0.0.1 - - [01/Mar/2026 15:45:20] "OPTIONS /api/community/feed HTTP/1.1" 200 -
127.0.0.1 - - [01/Mar/2026 15:45:20] "GET /api/community/feed HTTP/1.1" 200 -
```

### Additional Checks

#### Check 1: Verify Flask is Running
You should see:
```
✓ Database initialized: sqlite:///...
* Running on http://127.0.0.1:5000
* Debugger is active!
```

#### Check 2: Check Browser Console
Open Developer Tools (F12) → Console tab
- Should NOT see CORS errors
- Should NOT see 404 errors for OPTIONS
- Should see successful 200/201 responses

#### Check 3: Check Network Tab
Open Developer Tools (F12) → Network tab
- Filter by "Fetch/XHR"
- Click on a request
- Check "Response" tab for actual error message

### Common Issues

#### Issue: Still getting 404
**Solution:** Make sure you restarted Flask after making changes.

#### Issue: CORS error still appears
**Solution:** Clear browser cache completely and hard refresh.

#### Issue: "Token is missing" error
**Solution:** Log out and log in again to get a fresh token.

#### Issue: Database errors
**Solution:** 
```bash
cd backend
python db_init.py --reset
```

### Testing Individual Endpoints

#### Test Create Community
```bash
curl -X POST http://localhost:5000/api/community/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d "{\"name\":\"Test\",\"description\":\"Test\",\"category\":\"Tech\"}"
```

#### Test Submit Feedback
```bash
curl -X POST http://localhost:5000/api/community/feedback \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d "{\"content\":\"Test feedback\",\"category\":\"General\"}"
```

#### Test Create Blog
```bash
curl -X POST http://localhost:5000/api/community/blogs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d "{\"title\":\"Test\",\"content\":\"Test content\",\"tags\":[]}"
```

### If Still Not Working

1. **Check Python version:**
   ```bash
   python --version
   ```
   Should be Python 3.7+

2. **Reinstall Flask-CORS:**
   ```bash
   pip install --upgrade flask-cors
   ```

3. **Check for port conflicts:**
   ```bash
   netstat -ano | findstr :5000
   ```

4. **Try different port:**
   Edit `flask_cors_config.py` at the bottom:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```
   Then update frontend to use port 5001.

### Success Indicators

✅ No 404 errors in Flask logs
✅ OPTIONS requests return 200
✅ POST requests return 200/201
✅ Communities/feedback/blogs appear in UI
✅ No CORS errors in browser console

### Need More Help?

Check the Flask terminal output for specific error messages and share them for more targeted help.
