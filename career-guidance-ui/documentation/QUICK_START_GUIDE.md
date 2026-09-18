# Community Module - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Step 1: Install Backend Dependencies
```bash
cd career-guidance-ui/backend
pip install -r requirements.txt
```

### Step 2: Install Frontend Dependencies
```bash
cd career-guidance-ui
npm install
```

### Step 3: Start Backend Server
```bash
cd career-guidance-ui
python flask_cors_config.py
```
Backend runs on: `http://localhost:5000`

### Step 4: Start Frontend Server
```bash
cd career-guidance-ui
npm start
```
Frontend runs on: `http://localhost:3000`

### Step 5: Test the Application
1. Navigate to `http://localhost:3000`
2. Sign up for a new account
3. Navigate to Community tab
4. Explore all features!

## 📋 Quick API Test

### Test Authentication
```bash
# Signup
curl -X POST http://localhost:5000/api/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"password123","domain":"Technology"}'

# Login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Test Community Features
```bash
# Get communities (replace TOKEN with your JWT)
curl http://localhost:5000/api/community/groups \
  -H "Authorization: Bearer TOKEN"

# Get notifications
curl http://localhost:5000/api/community/notifications \
  -H "Authorization: Bearer TOKEN"

# Get feed
curl http://localhost:5000/api/community/feed \
  -H "Authorization: Bearer TOKEN"
```

## 🧪 Run Tests
```bash
cd career-guidance-ui/backend

# Test recommendations
python test_recommendations.py

# Test feed ranking
python test_feed_ranking.py

# Test messaging
python test_messaging.py

# Test profile matching
python test_profile_matching.py
```

## 📱 Frontend Routes

- `/` - Home page
- `/login` - Login page
- `/signup` - Signup page
- `/community` - Community hub (4 tabs)
- `/profile` - User profile with notifications
- `/analyze` - Analyze module (existing)
- `/routine` - Routine module (existing)
- `/explore` - Explore module (existing)

## 🎯 Key Features to Try

### 1. Create a Community
1. Go to Community tab
2. Click "Community Groups"
3. Click "Create Community"
4. Fill in details and submit

### 2. Post a Blog
1. Go to Community tab
2. Click "Blogs"
3. Click "Create Blog"
4. Write your blog and publish

### 3. Send a Message
1. Go to Community tab
2. Click "Reach Out"
3. Find a user
4. Click "Message"
5. Start chatting!

### 4. Check Notifications
1. Look at Navbar (red badge shows unread count)
2. Click Profile
3. See all notifications

## 🔧 Configuration

### Environment Variables (.env)
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///backend/career_guidance.db
FLASK_ENV=development
```

### CORS Settings
Default: Allows `http://localhost:3000`
Production: Update in `flask_cors_config.py`

## 📊 Database

### Location
`career-guidance-ui/backend/career_guidance.db`

### Tables Created
- users
- communities
- community_members
- posts
- comments
- likes
- conversations
- messages
- notifications
- user_profiles

### Reset Database
```bash
cd career-guidance-ui/backend
rm career_guidance.db
python flask_cors_config.py  # Will recreate
```

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check port 5000 is free

### Frontend won't start
- Check Node version: `node --version`
- Clear cache: `npm cache clean --force`
- Reinstall: `rm -rf node_modules && npm install`

### CORS errors
- Ensure backend is running on port 5000
- Check CORS settings in `flask_cors_config.py`
- Hard refresh browser: Ctrl+Shift+R

### Database errors
- Delete and recreate: `rm backend/career_guidance.db`
- Restart backend server

## 📚 Documentation

- **Architecture:** `PHASE10_ARCHITECTURE.md`
- **Implementation:** `IMPLEMENTATION_SUMMARY.md`
- **Phase Details:** `PHASE[1-9]_*.md` files
- **Troubleshooting:** `TROUBLESHOOTING.md`

## 🎓 Learning Path

### For Backend Developers
1. Read `community_models.py` - Understand data structure
2. Read `community_service.py` - Understand business logic
3. Read `flask_cors_config.py` - Understand API routes
4. Run tests to see how it works

### For Frontend Developers
1. Read `src/pages/Community.jsx` - Main page structure
2. Read `src/components/community/` - Individual components
3. Read `src/services/authService.js` - Authentication
4. Explore the UI and inspect network calls

## 🚢 Deployment

### Production Checklist
- [ ] Set SECRET_KEY environment variable
- [ ] Configure production database
- [ ] Update CORS origins
- [ ] Enable HTTPS
- [ ] Set up monitoring
- [ ] Configure logging
- [ ] Set up backups
- [ ] Test all endpoints
- [ ] Load testing
- [ ] Security audit

### Quick Deploy (Example)
```bash
# Build frontend
npm run build

# Serve with production server
gunicorn flask_cors_config:app

# Or use Docker
docker build -t community-app .
docker run -p 5000:5000 community-app
```

## 💡 Tips

1. **Use the test files** - They show how to use each feature
2. **Check browser console** - Helpful error messages
3. **Use Postman** - Test API endpoints easily
4. **Read the code** - Well-commented and clean
5. **Start simple** - Try one feature at a time

## 🆘 Need Help?

1. Check `TROUBLESHOOTING.md`
2. Read phase-specific documentation
3. Review test files for examples
4. Check browser console for errors
5. Check Flask terminal for backend errors

## ✅ Verification

### Backend Health Check
```bash
curl http://localhost:5000/api/profile \
  -H "Authorization: Bearer YOUR_TOKEN"
```
Should return user profile if working.

### Frontend Health Check
Open `http://localhost:3000` - Should see home page.

### Database Health Check
```bash
cd career-guidance-ui/backend
python -c "from community_models import db; from app_config import create_app; app = create_app(); print('DB OK')"
```

## 🎉 Success!

If you can:
- ✅ Sign up and login
- ✅ See the Community tab
- ✅ Create a community
- ✅ Post a blog
- ✅ See notifications

**You're all set! The Community module is working perfectly.**

---

**Happy Coding! 🚀**
