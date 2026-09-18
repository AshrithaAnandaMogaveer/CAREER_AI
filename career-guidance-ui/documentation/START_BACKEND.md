# 🚀 How to Start the Backend

## ✅ Backend is Already Running!

The Flask backend is currently running on:
- **http://localhost:5000**
- **http://127.0.0.1:5000**

## 📋 Quick Commands

### Start Backend (if not running)
```bash
cd career-guidance-ui
python flask_cors_config.py
```

### Start Frontend
```bash
cd career-guidance-ui
npm start
```

### Install Backend Dependencies (if needed)
```bash
cd career-guidance-ui
pip install -r requirements.txt
```

## 🧪 Test the Backend

### Test Login Endpoint
Open a new terminal and run:
```bash
curl -X POST http://localhost:5000/api/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

Expected response:
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "name": "John Doe",
    "email": "test@example.com",
    "domain": "Software Development"
  }
}
```

### Test Signup Endpoint
```bash
curl -X POST http://localhost:5000/api/signup ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"John Doe\",\"email\":\"john@example.com\",\"password\":\"password123\",\"domain\":\"Software Development\"}"
```

## 🎯 Now Test with Frontend

1. **Start Frontend** (in a new terminal):
   ```bash
   cd career-guidance-ui
   npm start
   ```

2. **Open Browser**: http://localhost:5173

3. **Test Login**:
   - Click "Login / Sign Up"
   - Email: `test@example.com`
   - Password: `password123`
   - Click "Login"
   - ✅ Should see "Profile" in navbar

4. **Test Signup**:
   - Click "Sign Up" tab
   - Fill all fields
   - Click "Sign Up"
   - ✅ Should see your name in navbar

5. **Test Session**:
   - Refresh page (F5)
   - ✅ Should still be logged in

6. **Test Logout**:
   - Click "Logout"
   - ✅ Should see "Login / Sign Up" again

## 📊 Backend Console Output

You should see logs like:
```
127.0.0.1 - - [DATE] "POST /api/login HTTP/1.1" 200 -
127.0.0.1 - - [DATE] "POST /api/signup HTTP/1.1" 201 -
127.0.0.1 - - [DATE] "GET /api/profile HTTP/1.1" 200 -
```

## 🐛 Troubleshooting

### Port Already in Use
If you see "Address already in use":
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Module Not Found
If you see "ModuleNotFoundError":
```bash
pip install -r requirements.txt
```

### CORS Error in Browser
Check that Flask backend shows:
```
 * Running on http://127.0.0.1:5000
```

And frontend is on:
```
http://localhost:5173
```

## 📝 Backend Files

- **flask_cors_config.py** - Main Flask server
- **requirements.txt** - Python dependencies

## 🔒 Security Note

This is a development server. For production:
1. Use a production WSGI server (gunicorn, uwsgi)
2. Enable HTTPS
3. Change SECRET_KEY
4. Add database
5. Implement password hashing
6. Add rate limiting

## ✅ Current Status

- ✅ Backend running on port 5000
- ✅ CORS configured for localhost:5173
- ✅ JWT authentication enabled
- ✅ All endpoints working
- ✅ Ready for frontend testing

## 🎉 You're All Set!

The backend is running and ready to receive requests from your React frontend. Start the frontend with `npm start` and test the authentication flow!

---

**Backend URL:** http://localhost:5000
**Frontend URL:** http://localhost:5173 (after npm start)
**Status:** ✅ Running
