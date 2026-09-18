# Routine Build - Quick Start Guide

## Why You Don't See the Tabs

The Progress Tracking and Evolution tabs (and the Save/Load buttons) **only appear AFTER you generate a routine**.

### Current State Check:

**If you see this**:
```
┌─────────────────────────────────────────┐
│  📄 Upload Analysis Report              │
│                                         │
│  [Drag & drop area]                     │
│                                         │
│  [ Generate Routine ]                   │
└─────────────────────────────────────────┘
```
**You're at**: Step 1 - Need to generate routine first

**If you see this**:
```
┌─────────────────────────────────────────┐
│  [Routine To Follow] [Chat] [Progress] [Evolution] │
│                                         │
│  Week 1: Python (15 hours)              │
│  Week 2: React (12 hours)               │
│  ...                                    │
└─────────────────────────────────────────┘
```
**You're at**: Step 2 - Routine generated, tabs visible

## Complete Workflow

### Step 1: Generate a Routine (REQUIRED FIRST)

1. **Upload Analysis File**:
   - Click the upload area or drag & drop
   - Select a file: JSON, PDF, or DOCX
   - File should be from the Analyze module

2. **Click "Generate Routine"**:
   - Button turns cyan/blue when file is uploaded
   - Click it
   - Wait for "Generating Your Routine..." to complete
   - Takes 5-10 seconds

3. **Verify Routine Generated**:
   - You should now see 4 tabs appear:
     - Routine To Follow
     - Chat With AI
     - Progress Tracking ← You need this
     - Evolution Over Time ← And this

### Step 2: Update Progress

**Now the tabs are visible!**

1. **Click "Progress Tracking" tab**
2. **You'll see**:
   - Overall Completion bar
   - Current Week selector
   - List of skills with sliders
   - Each skill has a "Save" button

3. **Update a skill**:
   - Move slider (e.g., Python to 75%)
   - Click "Save" button next to percentage
   - Repeat for 2-3 skills

### Step 3: View Evolution

1. **Click "Evolution Over Time" tab**
2. **You'll see**:
   - "Refresh Data" button at top right
   - Or it auto-loads
   - Evolution metrics display

## Visual Flow

```
START
  ↓
Upload File
  ↓
Click "Generate Routine"
  ↓
Wait for generation...
  ↓
✅ TABS APPEAR! ← This is when you see everything
  ↓
Click "Progress Tracking" tab
  ↓
Move sliders + Click "Save" buttons
  ↓
Click "Evolution Over Time" tab
  ↓
See your evolution data!
```

## Why Tabs Are Hidden Initially

The tabs are hidden because:
- You need a routine first to track progress
- Can't track progress without knowing what skills to track
- Can't show evolution without progress data

**Solution**: Generate a routine first!

## How to Generate a Routine

### Option 1: Use Sample File

If you have the sample file:
```
career-guidance-ui/backend/test_analyze_sample.json
```

1. Navigate to that file
2. Upload it
3. Click "Generate Routine"

### Option 2: Use Your Own Analysis

1. Go to "Analyze" module first
2. Upload your resume
3. Run analysis
4. Download the analysis JSON
5. Come back to Routine Build
6. Upload that JSON
7. Click "Generate Routine"

### Option 3: Create Test JSON

Create a file `test.json`:
```json
{
  "missingSkills": ["Python", "React", "Docker"],
  "priorityScores": {
    "Python": 0.9,
    "React": 0.8,
    "Docker": 0.7
  },
  "gapSeverity": {
    "Python": 0.8,
    "React": 0.7,
    "Docker": 0.6
  },
  "targetDomain": "Software Development",
  "readinessScore": 45,
  "extractedSkills": ["JavaScript", "HTML", "CSS"]
}
```

Upload this file and generate routine.

## Troubleshooting

### "I uploaded a file but Generate button is gray"

**Check**:
- File format: Must be .json, .pdf, or .docx
- File selected: Should show filename in upload area

**Solution**: Try uploading again

### "Generate button does nothing"

**Check**:
- Backend running: `python flask_cors_config.py`
- Logged in: Check if you're authenticated
- Console errors: Open DevTools (F12)

**Solution**: Restart backend and try again

### "Routine generated but no tabs"

**Check**:
- Refresh page: Ctrl+R or Cmd+R
- Check console: Look for errors

**Solution**: Try generating again

### "I see tabs but they're empty"

**You're good!** Tabs are there. Now:
1. Click "Progress Tracking"
2. Update some skills
3. Click "Evolution Over Time"

## Quick Test

To quickly test everything:

```bash
# 1. Start backend
cd career-guidance-ui
python flask_cors_config.py

# 2. In browser:
# - Login
# - Go to Routine Build
# - Upload: backend/test_analyze_sample.json
# - Click "Generate Routine"
# - Wait for tabs to appear
# - Click "Progress Tracking"
# - Move Python slider to 75%
# - Click "Save" button
# - Click "Evolution Over Time"
# - See data!
```

## Summary

**The buttons ARE there, but only after generating a routine!**

1. ✅ Upload file
2. ✅ Generate routine
3. ✅ Tabs appear
4. ✅ Progress Tracking tab → Save buttons visible
5. ✅ Evolution Over Time tab → Refresh Data button visible

**Current Issue**: You haven't generated a routine yet, so tabs are hidden.

**Solution**: Generate a routine first! 🚀

---

**Remember**: No routine = No tabs = No buttons. Generate routine first!
