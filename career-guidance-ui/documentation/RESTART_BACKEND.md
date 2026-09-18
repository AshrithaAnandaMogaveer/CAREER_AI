# Fix for 404 Errors - Backend Restart Required

## Issue
The new chat room endpoints are returning 404 errors because the Flask backend needs to be restarted to load the new routes.

## Solution

### Step 1: Stop the Backend
In the terminal where Flask is running, press:
```
Ctrl + C
```

### Step 2: Restart the Backend
```bash
cd career-guidance-ui
python flask_cors_config.py
```

### Step 3: Verify Backend Started
You should see:
```
============================================================
🚀 Flask Backend Server Starting...
============================================================
📍 Backend URL: http://localhost:5000
🗄️  Database: sqlite:///...
🔐 JWT Secret: ********************
============================================================

✅ Server is ready! Waiting for requests...

 * Running on http://0.0.0.0:5000
```

### Step 4: Test the Chat Room
1. Refresh your browser (F5)
2. Go to Community tab
3. Click "💬 Open Chat Room" on a joined community
4. The chat room should now load without errors

## Why This Happens
Flask loads all routes when it starts. When we add new routes to the code, Flask needs to be restarted to register them.

## Verification
After restarting, the following endpoints should work:
- ✅ GET /api/community/<id>/messages
- ✅ POST /api/community/message/send
- ✅ GET /api/community/<id>/members
- ✅ GET /uploads/community_images/<filename>

## Still Having Issues?

### Check Backend Logs
Look for any error messages in the Flask terminal.

### Check Frontend Console
Open browser DevTools (F12) and check the Console tab for errors.

### Verify Endpoints
Test an endpoint directly:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:5000/api/community/1/messages
```

### Common Issues

1. **Port Already in Use**
   - Error: `Address already in use`
   - Solution: Kill the process using port 5000
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   
   # Linux/Mac
   lsof -ti:5000 | xargs kill -9
   ```

2. **Module Import Errors**
   - Error: `ModuleNotFoundError`
   - Solution: Reinstall dependencies
   ```bash
   cd career-guidance-ui/backend
   pip install -r requirements.txt
   ```

3. **Database Errors**
   - Error: `no such table`
   - Solution: Delete and recreate database
   ```bash
   cd career-guidance-ui/backend
   rm career_guidance.db
   # Restart Flask - it will recreate the database
   ```

## Quick Restart Script

### Windows (PowerShell)
```powershell
# Save as restart-backend.ps1
cd career-guidance-ui
python flask_cors_config.py
```

### Linux/Mac (Bash)
```bash
# Save as restart-backend.sh
#!/bin/bash
cd career-guidance-ui
python flask_cors_config.py
```

---

**Status:** Ready to restart
**Time Required:** < 1 minute
**Impact:** None (just a restart)

