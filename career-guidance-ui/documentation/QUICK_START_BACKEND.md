# ⚡ Quick Start - Backend Integration

## 🚀 Start in 3 Steps

### 1. Start Flask Backend
```bash
python flask_cors_config.py
```
✅ Running on http://localhost:5000

### 2. Start React Frontend
```bash
cd career-guidance-ui
npm start
```
✅ Running on http://localhost:5173

### 3. Test Login
- Click "Login / Sign Up"
- Email: `test@example.com`
- Password: `password123`
- Click "Login"
- ✅ Should see "Profile" in navbar

## 📁 Key Files

```
career-guidance-ui/
├── src/
│   ├── services/
│   │   └── authService.js          ← API calls
│   ├── components/
│   │   ├── AuthModal.jsx           ← Updated (API integration)
│   │   └── Button.jsx              ← Updated (disabled state)
│   └── App.js                      ← Updated (session restore)
├── .env                            ← API URL config
└── flask_cors_config.py            ← Backend example
```

## 🔧 What Changed

### AuthModal.jsx
```javascript
// Before: Mock
setTimeout(() => onAuthSuccess(...), 500);

// After: Real API
const response = await loginUser(credentials);
if (response.success) onAuthSuccess(response.user);
```

### App.js
```javascript
// Added: Session restoration
useEffect(() => {
  if (isAuthenticated()) {
    setUser(getStoredUser());
    setIsLoggedIn(true);
  }
}, []);
```

### authService.js (New)
```javascript
export const loginUser = async (credentials) => {
  const response = await fetch(`${API_URL}/api/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });
  const data = await response.json();
  if (data.success) {
    localStorage.setItem('authToken', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
  }
  return data;
};
```

## 🔐 API Endpoints

### Login
```bash
POST http://localhost:5000/api/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}
```

### Signup
```bash
POST http://localhost:5000/api/signup
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "domain": "Software Development"
}
```

### Profile (Protected)
```bash
GET http://localhost:5000/api/profile
Authorization: Bearer YOUR_TOKEN_HERE
```

## ✅ Quick Test Checklist

- [ ] Backend running on port 5000
- [ ] Frontend running on port 5173
- [ ] Can open login modal
- [ ] Can login successfully
- [ ] Navbar shows "Profile"
- [ ] Can refresh and stay logged in
- [ ] Can logout
- [ ] No console errors

## 🐛 Quick Troubleshooting

### CORS Error?
Check Flask backend has:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"]
    }
})
```

### Token Not Stored?
Check browser console:
```javascript
localStorage.getItem('authToken')
localStorage.getItem('user')
```

### Network Error?
- Backend running? ✓
- Correct port (5000)? ✓
- .env file correct? ✓

## 📚 Full Documentation

- **BACKEND_INTEGRATION.md** - Complete guide
- **BACKEND_TESTING.md** - Testing checklist
- **INTEGRATION_SUMMARY.md** - Overview
- **flask_cors_config.py** - Backend code

## 🎯 What Works

✅ Login with real API
✅ Signup with real API
✅ Token storage
✅ Session restoration
✅ Logout
✅ Error handling
✅ Loading states
✅ All animations intact
✅ Mobile responsive

## 🚀 Production Ready

To deploy:
1. Update `.env.production`:
   ```
   VITE_API_URL=https://api.yourdomain.com
   ```
2. Build frontend:
   ```bash
   npm run build
   ```
3. Deploy Flask with gunicorn
4. Enable HTTPS
5. Update CORS origins

---

**Status:** ✅ Ready to Use
**Time to Setup:** < 5 minutes
**Breaking Changes:** None

Happy coding! 🎉
