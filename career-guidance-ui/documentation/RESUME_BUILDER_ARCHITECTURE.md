# Resume Builder - System Architecture

## 🏗️ Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         BuildResume.jsx                          │
│                      (Main Container Page)                       │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │         ResumeTemplateSelector.jsx                       │   │
│  │  [Modern] [Minimal] [Executive] [Fresher] [Technical]   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────┐  ┌──────────────────────────┐   │
│  │   ResumeForm.jsx         │  │  ResumePreview.jsx       │   │
│  │  (Left Panel)            │  │  (Right Panel)           │   │
│  │                          │  │                          │   │
│  │  ┌────────────────────┐ │  │  ┌────────────────────┐ │   │
│  │  │ Personal Info      │ │  │  │                    │ │   │
│  │  │ [Collapsible]      │ │  │  │   Live Preview     │ │   │
│  │  ├────────────────────┤ │  │  │   (White BG)       │ │   │
│  │  │ Summary            │ │  │  │                    │ │   │
│  │  │ [Collapsible]      │ │  │  │   Updates in       │ │   │
│  │  ├────────────────────┤ │  │  │   Real-time        │ │   │
│  │  │ Skills             │ │  │  │                    │ │   │
│  │  │ [+ Add] [x Remove] │ │  │  │   Template:        │ │   │
│  │  ├────────────────────┤ │  │  │   - Modern         │ │   │
│  │  │ Experience         │ │  │  │   - Minimal        │ │   │
│  │  │ [+ Add] [x Remove] │ │  │  │   - Executive      │ │   │
│  │  ├────────────────────┤ │  │  │   - Fresher        │ │   │
│  │  │ Education          │ │  │  │   - Technical      │ │   │
│  │  │ [+ Add] [x Remove] │ │  │  │                    │ │   │
│  │  ├────────────────────┤ │  │  └────────────────────┘ │   │
│  │  │ Projects           │ │  │                          │   │
│  │  │ [+ Add] [x Remove] │ │  │                          │   │
│  │  ├────────────────────┤ │  │                          │   │
│  │  │ Certifications     │ │  │                          │   │
│  │  │ [+ Add] [x Remove] │ │  │                          │   │
│  │  ├────────────────────┤ │  │                          │   │
│  │  │ Achievements       │ │  │                          │   │
│  │  │ [+ Add] [x Remove] │ │  │                          │   │
│  │  └────────────────────┘ │  │                          │   │
│  └──────────────────────────┘  └──────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              DownloadButtons.jsx                         │   │
│  │              [PDF] [DOCX]                                │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

```
┌──────────────┐
│   User Input │
│  (Form Field)│
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  handleDataChange()  │
│  (BuildResume.jsx)   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  setResumeData()     │
│  (State Update)      │
└──────┬───────────────┘
       │
       ├─────────────────────────┐
       │                         │
       ▼                         ▼
┌──────────────┐        ┌──────────────────┐
│ ResumeForm   │        │ ResumePreview    │
│ (Re-render)  │        │ (Re-render)      │
└──────────────┘        └──────────────────┘
                                │
                                ▼
                        ┌──────────────────┐
                        │ Template Render  │
                        │ (Instant Update) │
                        └──────────────────┘
```

---

## 📊 State Structure

```javascript
resumeData = {
  personalInfo: {
    name: string,
    email: string,
    phone: string,
    linkedin: string,
    github: string,
    location: string
  },
  summary: string,
  skills: [string, string, ...],
  experience: [
    {
      company: string,
      role: string,
      duration: string,
      description: string
    },
    ...
  ],
  education: [
    {
      degree: string,
      institution: string,
      year: string,
      grade: string
    },
    ...
  ],
  projects: [
    {
      title: string,
      techStack: string,
      description: string
    },
    ...
  ],
  certifications: [string, string, ...],
  achievements: [string, string, ...]
}
```

---

## 🌐 API Flow (Download)

```
┌─────────────────┐
│  User clicks    │
│  Download PDF   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  DownloadButtons.jsx    │
│  - Set loading state    │
│  - Prepare payload      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  POST /api/resume/download/pdf      │
│  Body: {                            │
│    template: "modern",              │
│    resumeData: { ... }              │
│  }                                  │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Flask Backend                      │
│  routes/resume.py                   │
│  - Validate input                   │
│  - Call pdf_generator.py            │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  utils/pdf_generator.py             │
│  - Create SimpleDocTemplate         │
│  - Build story with Platypus        │
│  - Generate PDF buffer              │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Response: Binary PDF Blob          │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Frontend: DownloadButtons.jsx     │
│  - Create blob URL                  │
│  - Trigger download                 │
│  - Cleanup                          │
│  - Reset loading state              │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  File saved to  │
│  Downloads      │
└─────────────────┘
```

---

## 🎨 Template Rendering Logic

```
┌──────────────────────┐
│ selectedTemplate     │
│ (State)              │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────────────────┐
│ ResumePreview.jsx                │
│ renderTemplate() switch          │
└──────┬───────────────────────────┘
       │
       ├─── "modern" ────────► ModernTemplate(data)
       │
       ├─── "minimal" ───────► MinimalTemplate(data)
       │
       ├─── "executive" ─────► ExecutiveTemplate(data)
       │
       ├─── "fresher" ───────► FresherTemplate(data)
       │
       └─── "technical" ─────► TechnicalTemplate(data)
                                      │
                                      ▼
                              ┌───────────────────┐
                              │ Render JSX with   │
                              │ resumeData        │
                              └───────────────────┘
```

---

## 🔐 Security Flow

```
Frontend Input
     │
     ▼
┌─────────────────────┐
│ Client Validation   │
│ - Required fields   │
│ - Format check      │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Send to Backend     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────────┐
│ Backend Validation      │
│ - Input sanitization    │
│ - XSS prevention        │
│ - Size limits           │
│ - Type checking         │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────┐
│ Generate Document   │
│ - Safe rendering    │
│ - No code execution │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Return File         │
└─────────────────────┘
```

---

## 📱 Responsive Breakpoints

```
Mobile (< 768px)
┌─────────────────┐
│  Template       │
│  Selector       │
│  (2 columns)    │
├─────────────────┤
│                 │
│  Resume Form    │
│  (Full width)   │
│                 │
├─────────────────┤
│                 │
│  Preview        │
│  (Full width)   │
│                 │
├─────────────────┤
│  Download       │
│  Buttons        │
└─────────────────┘

Desktop (≥ 1024px)
┌─────────────────────────────────────┐
│  Template Selector (5 columns)      │
├──────────────────┬──────────────────┤
│                  │                  │
│  Resume Form     │  Preview         │
│  (50%)           │  (50%)           │
│                  │                  │
│                  │                  │
└──────────────────┴──────────────────┘
```

---

## 🔧 Technology Stack

```
Frontend:
├── React 18
├── Tailwind CSS
├── Framer Motion
├── Lucide Icons
└── React Router

Backend:
├── Flask 2.3
├── Flask-CORS
├── ReportLab 4.0
└── python-docx 0.8

Build Tools:
├── Create React App
├── npm/yarn
└── pip
```

---

## 📦 File Dependencies

```
BuildResume.jsx
├── imports ResumeTemplateSelector
├── imports ResumeForm
├── imports ResumePreview
├── imports DownloadButtons
└── imports Button (shared)

ResumeForm.jsx
├── imports Button (shared)
└── uses Framer Motion

ResumePreview.jsx
└── uses Framer Motion

DownloadButtons.jsx
├── imports Button (shared)
└── calls Backend API

Backend:
app.py
├── imports resume_bp from routes/resume
└── enables CORS

routes/resume.py
├── imports pdf_generator
└── imports docx_generator

pdf_generator.py
└── uses reportlab.platypus

docx_generator.py
└── uses python-docx
```

---

## 🎯 Performance Optimization

```
Component Level:
├── Controlled inputs (no uncontrolled re-renders)
├── Conditional rendering (collapsed sections)
├── Memoization ready (can add React.memo)
└── Efficient state updates

Animation Level:
├── Framer Motion (GPU accelerated)
├── CSS transitions (150ms)
└── Smooth template switching

Network Level:
├── Single API call per download
├── Binary file streaming
└── Error handling with retry option
```

---

## 🚀 Deployment Architecture

```
Production Setup:

Frontend (React):
├── Build: npm run build
├── Deploy to: Vercel/Netlify/AWS S3
└── Serve static files

Backend (Flask):
├── Deploy to: Heroku/AWS/DigitalOcean
├── Use Gunicorn for production
├── Enable HTTPS
└── Configure CORS for production domain

Environment Variables:
Frontend:
└── REACT_APP_API_URL=https://api.yourdomain.com

Backend:
├── FLASK_ENV=production
├── CORS_ORIGINS=https://yourdomain.com
└── SECRET_KEY=<random-secret>
```

---

## ✅ Quality Checklist

```
Code Quality:
✅ Clean component structure
✅ Reusable components
✅ Consistent naming
✅ Proper error handling
✅ Loading states
✅ No console errors

UX Quality:
✅ Smooth animations
✅ Instant feedback
✅ Clear error messages
✅ Responsive design
✅ Accessible forms
✅ Intuitive navigation

ATS Quality:
✅ No tables
✅ Standard fonts
✅ Semantic HTML
✅ Clear headings
✅ Proper spacing
✅ No images in body
```

---

**Architecture is production-ready and scalable! 🎉**
