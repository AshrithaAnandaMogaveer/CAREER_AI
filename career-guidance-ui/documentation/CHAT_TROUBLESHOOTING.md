# Community Chat Room - Troubleshooting Guide

## 🔴 Error: 404 Not Found

### Symptoms
```
GET http://localhost:5000/api/community/2/messages 404 (NOT FOUND)
GET http://localhost:5000/api/community/2/members 404 (NOT FOUND)
POST http://localhost:5000/api/community/message/send 404 (NOT FOUND)
```

### Root Cause
The Flask backend is running an old version of the code that doesn't include the new chat endpoints.

### ✅ Solution: Restart Flask Backend

#### Step 1: Stop the Backend
In the terminal where Flask is running:
- Press `Ctrl + C` to stop the server

#### Step 2: Restart the Backend
```bash
cd career-guidance-ui
python flask_cors_config.py
```

#### Step 3: Verify Success
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

 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

#### Step 4: Test the Chat
1. Refresh your browser (F5 or Ctrl+R)
2. Go to Community tab
3. Join a community (if not already joined)
4. Click "💬 Open Chat Room"
5. Chat room should open without errors

---

## 🔴 Error: Port Already in Use

### Symptoms
```
OSError: [Errno 98] Address already in use
```

### Solution

#### Windows
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace <PID> with actual PID)
taskkill /PID <PID> /F

# Restart Flask
python flask_cors_config.py
```

#### Linux/Mac
```bash
# Find and kill process using port 5000
lsof -ti:5000 | xargs kill -9

# Or use fuser
fuser -k 5000/tcp

# Restart Flask
python flask_cors_config.py
```

---

## 🔴 Error: Module Not Found

### Symptoms
```
ModuleNotFoundError: No module named 'flask'
ModuleNotFoundError: No module named 'community_models'
```

### Solution
```bash
cd career-guidance-ui/backend
pip install -r requirements.txt
```

---

## 🔴 Error: Database Table Not Found

### Symptoms
```
sqlite3.OperationalError: no such table: posts
```

### Solution
The database needs to be recreated with the new CHAT_MESSAGE post type.

```bash
cd career-guidance-ui/backend

# Backup existing database (optional)
copy career_guidance.db career_guidance_backup.db

# Delete database
rm career_guidance.db  # Linux/Mac
del career_guidance.db  # Windows

# Restart Flask - it will recreate the database
cd ..
python flask_cors_config.py
```

**Note:** This will delete all existing data. If you need to preserve data, use database migration tools.

---

## 🔴 Error: Image Upload Fails

### Symptoms
```
FileNotFoundError: [Errno 2] No such file or directory: 'uploads/community_images'
```

### Solution
The uploads directory doesn't exist.

```bash
cd career-guidance-ui

# Create directory
mkdir -p uploads/community_images  # Linux/Mac
New-Item -ItemType Directory -Force -Path "uploads/community_images"  # Windows PowerShell

# Set permissions (Linux/Mac only)
chmod 755 uploads/community_images
```

---

## 🔴 Error: 403 Forbidden

### Symptoms
```json
{
  "success": false,
  "message": "You must be a member to view messages"
}
```

### Solution
You're not a member of the community. Join the community first:

1. Go to Community tab
2. Find the community
3. Click "Join Community"
4. Wait for success message
5. Button should change to "💬 Open Chat Room"
6. Now click to open chat

---

## 🔴 Error: 401 Unauthorized

### Symptoms
```json
{
  "success": false,
  "message": "Token is missing"
}
```

### Solution
Your authentication token is missing or expired.

1. Log out
2. Log in again
3. Try accessing the chat room

---

## 🔴 Error: Images Don't Display

### Symptoms
- Image uploads successfully
- But doesn't display in chat
- 404 error for image URL

### Solution

#### Check 1: Verify Upload Directory
```bash
cd career-guidance-ui
ls -la uploads/community_images/  # Linux/Mac
dir uploads\community_images\  # Windows
```

#### Check 2: Verify Image Endpoint
Test directly in browser:
```
http://localhost:5000/uploads/community_images/test.jpg
```

#### Check 3: Check File Permissions (Linux/Mac)
```bash
chmod 644 uploads/community_images/*
```

---

## 🔴 Error: Messages Don't Update

### Symptoms
- Can send messages
- But don't see new messages from others
- Have to refresh page to see updates

### Solution
This is expected behavior. The chat uses 5-second polling, not WebSocket.

- Messages update every 5 seconds automatically
- For instant updates, consider implementing WebSocket (future enhancement)

---

## 🔴 Error: CORS Issues

### Symptoms
```
Access to fetch at 'http://localhost:5000/...' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

### Solution
CORS should already be configured. If you see this error:

1. Check flask_cors_config.py has CORS enabled
2. Restart Flask backend
3. Clear browser cache
4. Try in incognito mode

---

## 🟡 Performance Issues

### Symptoms
- Chat is slow
- Messages take long to load
- High CPU usage

### Solutions

#### 1. Reduce Polling Frequency
Edit `CommunityChatRoom.jsx`:
```javascript
// Change from 5 seconds to 10 seconds
const interval = setInterval(fetchMessages, 10000);
```

#### 2. Limit Message History
Edit `community_service.py`:
```python
# Change from 100 to 50 messages
messages = Post.query.filter_by(...).limit(50).all()
```

#### 3. Add Database Indexes
Already included, but verify:
```sql
CREATE INDEX idx_post_community_type ON posts(community_id, post_type);
```

---

## 🟢 Verification Checklist

After fixing issues, verify everything works:

- [ ] Backend starts without errors
- [ ] Frontend compiles without errors
- [ ] Can join a community
- [ ] "Open Chat Room" button appears
- [ ] Chat room modal opens
- [ ] Can see message history
- [ ] Can send text messages
- [ ] Can upload images
- [ ] Images display correctly
- [ ] Can see member list
- [ ] Messages update automatically
- [ ] No console errors

---

## 📝 Debug Mode

### Enable Detailed Logging

#### Backend (Flask)
Already enabled in debug mode. Check terminal for detailed logs.

#### Frontend (React)
Open browser DevTools (F12):
- Console tab: JavaScript errors
- Network tab: API requests/responses
- Application tab: LocalStorage (check token)

### Test API Endpoints Directly

#### Get Messages
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/api/community/1/messages
```

#### Send Message
```bash
curl -X POST \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -F "community_id=1" \
     -F "content=Test message" \
     http://localhost:5000/api/community/message/send
```

#### Get Members
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/api/community/1/members
```

---

## 🆘 Still Having Issues?

### 1. Check All Services Running
- [ ] Flask backend on port 5000
- [ ] React frontend on port 3000
- [ ] Database file exists

### 2. Check File Changes
Verify these files were updated:
- [ ] flask_cors_config.py (new endpoints)
- [ ] backend/community_service.py (new methods)
- [ ] backend/community_models.py (CHAT_MESSAGE enum)
- [ ] src/components/community/CommunityChatRoom.jsx (new file)
- [ ] src/components/community/CommunityGroups.jsx (updated)

### 3. Fresh Start
If all else fails:

```bash
# Stop everything
# Ctrl+C in both terminals

# Backend
cd career-guidance-ui
python flask_cors_config.py

# Frontend (new terminal)
cd career-guidance-ui
npm start
```

### 4. Check Logs
- Backend: Check Flask terminal for errors
- Frontend: Check browser console (F12)
- Network: Check Network tab in DevTools

---

## 📞 Quick Reference

### Backend Commands
```bash
# Start backend
python flask_cors_config.py

# Check Python version
python --version

# Install dependencies
pip install -r backend/requirements.txt

# Check database
sqlite3 backend/career_guidance.db ".tables"
```

### Frontend Commands
```bash
# Start frontend
npm start

# Check Node version
node --version

# Install dependencies
npm install

# Clear cache
npm cache clean --force
```

---

**Most Common Fix:** Just restart the Flask backend! 🔄

**Time to Fix:** < 1 minute

**Impact:** None (just a restart)

