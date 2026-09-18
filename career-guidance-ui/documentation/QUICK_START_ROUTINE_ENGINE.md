# Quick Start: Routine Engine

## 🚀 Start in 3 Steps

### Step 1: Start Backend
```bash
cd career-guidance-ui
python flask_cors_config.py
```
✅ Backend running on `http://localhost:5000`

### Step 2: Start Frontend
```bash
cd career-guidance-ui
npm start
```
✅ Frontend running on `http://localhost:3000`

### Step 3: Test
1. Login to the app
2. Click **"Routine Build"** in navbar
3. Upload `backend/test_analyze_sample.json`
4. Click **"Generate Routine"**
5. View your personalized learning schedule!

## 📁 Test File Location
```
career-guidance-ui/backend/test_analyze_sample.json
```

## ✅ What You'll See

After generating routine:

1. **Routine To Follow Tab**:
   - Week-by-week schedule
   - Skills with hours
   - Difficulty levels
   - Completion dates

2. **Chat With AI Tab**:
   - Ask questions about your routine
   - Get personalized advice

3. **Progress Tracking Tab**:
   - Mark skills complete
   - Update progress

4. **Evolution Over Time Tab**:
   - View progress graphs
   - Track completion

## 🔧 Troubleshooting

### Backend won't start?
```bash
pip install flask flask-cors pyjwt PyPDF2 python-docx
```

### Frontend errors?
```bash
npm install
```

### Can't upload file?
- Make sure you're logged in
- Use JSON, PDF, or DOCX files only

## 📚 More Info

- **Complete docs**: `ROUTINE_ENGINE_COMPLETE.md`
- **Testing guide**: `ROUTINE_ENGINE_TESTING.md`
- **Summary**: `ROUTINE_ENGINE_SUMMARY.md`

## 🎯 Features

✅ Upload analysis files (JSON, PDF, DOCX)
✅ AI-powered skill prioritization
✅ Dependency-aware scheduling
✅ Weekly learning plans
✅ Hour estimates
✅ Completion projections

## 🔐 Authentication

You must be logged in to use Routine Build. If you see "Authentication required", login first.

## 💡 Tips

- Start with 10-15 hours per week
- Follow the weekly schedule
- Mark skills complete as you learn
- Chat with AI for guidance
- Track your evolution over time

---

**Ready to build your learning routine? Let's go! 🚀**
