# 🚀 Quick Start Guide - Complete Project

## Prerequisites

- Node.js (v14 or higher)
- Python 3.8+
- pip (Python package manager)

## 📦 Installation

### 1. Install Frontend Dependencies
```bash
cd career-guidance-ui
npm install
```

### 2. Install Backend Dependencies
```bash
cd career-guidance-ui
pip install flask flask-cors pyjwt
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

## 🏃 Running the Project

### Option 1: Run Both Servers Separately

#### Terminal 1 - Backend (Flask)
```bash
cd career-guidance-ui
python flask_cors_config.py
```
Backend will run on: http://localhost:5000

#### Terminal 2 - Frontend (React)
```bash
cd career-guidance-ui
npm start
```
Frontend will run on: http://localhost:3000 (or 5173 for Vite)

### Option 2: Windows Batch Script (Coming Soon)
Create a `start.bat` file to run both servers automatically.

## 🧪 Testing the Application

### 1. Test Authentication
1. Open http://localhost:3000
2. Click "Login / Sign Up" button
3. Switch to "Sign Up" tab
4. Fill in:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
   - Domain: Software Development
5. Click "Sign Up"
6. You should see "Profile" in navbar

### 2. Test Analyze Feature
1. Click "Analyze / Build" in navbar
2. Try both options:
   - Upload Resume (PDF/DOC)
   - Manual Entry (enter skills)
3. View results page with:
   - Readiness score
   - Extracted skills
   - Suggested domains
   - Missing skills

### 3. Test Post Matrics Module
1. Click "Post Matrics" in navbar
2. Test each category:

#### After 10th Guidance
- Click the card
- Click "Get Started"
- Fill academic score, interests, subjects
- View stream recommendations

#### After 12th Guidance
- Select stream, budget, interests
- View career recommendations with feasibility scores

#### Competitive Exams
- View exam list with difficulty levels
- See eligibility and career opportunities

#### Skill-Based Careers
- Enter interests and current skills
- View accessible career paths

#### Scholarships
- Select category and income level
- View eligible scholarships

#### Interest Assessment
- Take 10-question MCQ test
- Answer all questions
- View top 3 career clusters with scores
- Option to retake test

## 🔧 Configuration

### Environment Variables
Create `.env` file in `career-guidance-ui/`:
```
VITE_API_URL=http://localhost:5000
```

### Backend Configuration
Edit `flask_cors_config.py`:
- Change `SECRET_KEY` for production
- Update CORS origins for deployment
- Configure database connection

## 📊 API Endpoints

### Authentication
- POST /api/signup - User registration
- POST /api/login - User login
- GET /api/profile - Get user profile (protected)

### Analyze Feature
- POST /api/analyze/upload - Upload resume
- POST /api/analyze/manual - Manual skill entry

### Post Matrics
- GET /api/postmatrics/after10th - Stream recommendations
- POST /api/postmatrics/after12th - Career analysis
- GET /api/postmatrics/exams - Competitive exams
- GET /api/postmatrics/skills - Skill-based careers
- GET /api/postmatrics/scholarships - Scholarships
- POST /api/postmatrics/interest-test - Interest assessment

## 🐛 Troubleshooting

### Frontend won't start
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Backend errors
```bash
# Reinstall Python packages
pip install --upgrade flask flask-cors pyjwt
```

### CORS errors
- Check backend is running on port 5000
- Verify CORS origins in flask_cors_config.py
- Check browser console for specific errors

### Port already in use
```bash
# Windows - Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Authentication not working
- Clear browser localStorage
- Check JWT token in Network tab
- Verify SECRET_KEY in backend

## 📱 Mobile Testing

The app is fully responsive. Test on:
- Chrome DevTools (F12 → Toggle device toolbar)
- Real mobile devices
- Different screen sizes

## 🎨 Features Overview

### ✅ Completed Features
- Landing page with Hero, Why Us, How It Helps
- Authentication (Login/Signup)
- Protected routes
- Analyze & Build feature
- Post Matrics module (6 categories)
- Interest assessment test
- Responsive design
- Glassmorphism UI
- Smooth animations

### 🚧 Coming Soon
- Create Resume feature
- Routine Build
- Explore section
- Community features
- Profile management
- Dashboard analytics

## 📚 Documentation

- [Authentication System](AUTH_SYSTEM.md)
- [Backend Integration](BACKEND_INTEGRATION.md)
- [Analyze Feature](ANALYZE_FEATURE.md)
- [Post Matrics Complete](POST_MATRICS_COMPLETE.md)
- [Project Structure](PROJECT_STRUCTURE.md)

## 🆘 Need Help?

Check these files:
- `START_HERE.md` - Project overview
- `QUICKSTART.md` - Quick setup guide
- `READY_TO_TEST.md` - Testing instructions
- `BACKEND_TESTING.md` - Backend testing guide

## 🎯 Current Status

✅ Frontend: Fully functional
✅ Backend: Mock API ready
✅ Authentication: Working
✅ Routing: Complete
✅ UI/UX: Polished
⏳ Database: Not connected (using mock data)
⏳ ML Algorithms: Placeholder logic

**The application is ready for testing with mock data!**
