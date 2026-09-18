# Resume Builder - Quick Start Guide

## 🚀 Immediate Testing (Frontend Only)

### 1. Start the React App
```bash
cd career-guidance-ui
npm start
```

### 2. Navigate to Resume Builder
```
http://localhost:3000/build-resume
```

### 3. Test Features
- ✅ Fill in personal information
- ✅ Add professional summary
- ✅ Add skills (click "+ Add Skill")
- ✅ Add experience entries
- ✅ Add education entries
- ✅ Add projects
- ✅ Switch between 5 templates
- ✅ Watch real-time preview update
- ✅ Test collapsible sections
- ✅ Test responsive design (resize browser)

**Note**: Download buttons will show error until backend is set up.

---

## 🔧 Backend Setup (For PDF/DOCX Downloads)

### Step 1: Create Backend Structure
```bash
# From project root
mkdir -p backend/routes backend/utils
cd backend
```

### Step 2: Create requirements.txt
```bash
cat > requirements.txt << EOF
Flask==2.3.0
Flask-CORS==4.0.0
reportlab==4.0.4
python-docx==0.8.11
EOF
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Copy Backend Code

Copy the following files from `RESUME_BUILDER_BACKEND.md`:

**File 1: `backend/app.py`**
```python
from flask import Flask
from flask_cors import CORS
from routes.resume import resume_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(resume_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**File 2: `backend/routes/resume.py`**
- Copy the complete code from section "1. Resume Routes" in RESUME_BUILDER_BACKEND.md

**File 3: `backend/utils/pdf_generator.py`**
- Copy the complete code from section "2. PDF Generator" in RESUME_BUILDER_BACKEND.md

**File 4: `backend/utils/docx_generator.py`**
- Copy the complete code from section "3. DOCX Generator" in RESUME_BUILDER_BACKEND.md

### Step 5: Start Backend Server
```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

---

## ✅ Full Testing (Frontend + Backend)

### Terminal 1: Frontend
```bash
cd career-guidance-ui
npm start
# Runs on http://localhost:3000
```

### Terminal 2: Backend
```bash
cd backend
python app.py
# Runs on http://localhost:5000
```

### Test Flow:
1. Open browser: `http://localhost:3000/build-resume`
2. Fill in resume details
3. Click "PDF" button → Downloads PDF
4. Click "DOCX" button → Downloads DOCX
5. Open downloaded files to verify

---

## 🎯 Navigation Flow

```
Home (/) 
  → Login/Signup
  → Navbar: "Analyze/Build"
  → /analyze page
  → Click "Create Resume" card
  → /create-resume (landing page)
  → Click "Start Building Resume"
  → /build-resume (actual builder) ✨
```

---

## 🐛 Troubleshooting

### Issue: Download buttons show error
**Solution**: Make sure Flask backend is running on port 5000

### Issue: CORS error
**Solution**: Verify Flask-CORS is installed and configured in app.py

### Issue: PDF generation fails
**Solution**: Check reportlab is installed: `pip install reportlab`

### Issue: DOCX generation fails
**Solution**: Check python-docx is installed: `pip install python-docx`

### Issue: Port 5000 already in use
**Solution**: 
```bash
# Find process
lsof -i :5000
# Kill process
kill -9 <PID>
```

---

## 📦 Project Structure

```
Intelligent_Career_Guidance_Project/
├── career-guidance-ui/              # React Frontend
│   ├── src/
│   │   ├── pages/
│   │   │   └── BuildResume.jsx      # Main page
│   │   ├── components/
│   │   │   └── resume/              # Resume components
│   │   └── App.js                   # Routes configured
│   └── package.json
│
└── backend/                         # Flask Backend (create this)
    ├── routes/
    │   └── resume.py                # API endpoints
    ├── utils/
    │   ├── pdf_generator.py         # PDF generation
    │   └── docx_generator.py        # DOCX generation
    ├── app.py                       # Flask app
    └── requirements.txt             # Dependencies
```

---

## 🎨 Features Overview

### Templates (5):
1. **Modern Professional** - Blue accents, clean layout
2. **Minimal Clean** - Centered name, minimal design
3. **Two-Column Executive** - Skills sidebar, content right
4. **Fresher Compact** - Gray sections, compact layout
5. **Technical Profile** - Blue borders, tech-focused

### Sections (8):
1. Personal Information (6 fields)
2. Professional Summary (textarea)
3. Skills (dynamic list)
4. Experience (dynamic entries)
5. Education (dynamic entries)
6. Projects (dynamic entries)
7. Certifications (dynamic list)
8. Achievements (dynamic list)

### Actions:
- ✅ Add/Remove dynamic fields
- ✅ Collapse/Expand sections
- ✅ Switch templates instantly
- ✅ Download PDF
- ✅ Download DOCX

---

## 🔥 Quick Demo Data

Use this sample data for quick testing:

**Personal Info:**
- Name: John Doe
- Email: john.doe@example.com
- Phone: +1 (555) 123-4567
- LinkedIn: linkedin.com/in/johndoe
- GitHub: github.com/johndoe
- Location: San Francisco, CA

**Summary:**
```
Experienced Full-Stack Developer with 5+ years of expertise in React, Node.js, and Python. Proven track record of building scalable web applications and leading development teams.
```

**Skills:**
- React.js
- Node.js
- Python
- TypeScript
- MongoDB
- AWS

**Experience:**
- Company: Tech Corp
- Role: Senior Software Engineer
- Duration: Jan 2020 - Present
- Description: Led development of microservices architecture serving 1M+ users

**Education:**
- Degree: B.S. Computer Science
- Institution: Stanford University
- Year: 2019
- Grade: 3.8 GPA

---

## 📞 Support

If you encounter issues:
1. Check `RESUME_BUILDER_COMPLETE.md` for full documentation
2. Check `RESUME_BUILDER_BACKEND.md` for backend code
3. Verify all dependencies are installed
4. Check browser console for errors
5. Check Flask terminal for backend errors

---

## ✨ Success Indicators

You'll know it's working when:
- ✅ Form inputs update preview in real-time
- ✅ Template switching is instant
- ✅ Sections collapse/expand smoothly
- ✅ Add/Remove buttons work
- ✅ PDF downloads successfully
- ✅ DOCX downloads successfully
- ✅ Files open correctly in PDF/Word viewers

---

**Ready to build professional resumes! 🎉**
