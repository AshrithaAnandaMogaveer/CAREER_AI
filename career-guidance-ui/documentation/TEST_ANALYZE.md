# 🧪 Test Analyze Feature - Quick Guide

## Prerequisites

✅ Backend running on http://localhost:5000
✅ Frontend running on http://localhost:5173
✅ User logged in

## Quick Test (5 Minutes)

### 1. Test Navigation
```
1. Login to the app
2. Click "Analyze / Build" in navbar
3. ✅ Should navigate to /analyze page
4. ✅ Should see two cards
```

### 2. Test Upload Modal
```
1. Click "Attach / Enter Your Data" card
2. ✅ Modal should open
3. ✅ "Upload Resume" tab should be active
4. ✅ Should see drag & drop area
```

### 3. Test File Upload
```
1. Click "Choose file" or drag a PDF
2. ✅ File should appear with name and size
3. Click "Analyze Resume" button
4. ✅ Should show "Analyzing..." loading state
5. ✅ Should navigate to /results page
6. ✅ Should see analysis data
```

### 4. Test Manual Entry
```
1. Go back to /analyze
2. Click "Attach / Enter Your Data"
3. Click "Manual Entry" tab
4. ✅ Tab should switch smoothly
5. Enter skills: "Python, React, SQL, Git"
6. Select domain: "Software Development"
7. Click "Analyze Skills"
8. ✅ Should show "Analyzing..." loading state
9. ✅ Should navigate to /results
10. ✅ Should see entered skills in results
```

### 5. Test Results Page
```
1. On /results page, verify:
   ✅ Readiness score shows (e.g., 75%)
   ✅ Progress bar animates
   ✅ Extracted skills listed
   ✅ Missing skills listed
   ✅ Suggested domains shown
   ✅ "Analyze Again" button works
   ✅ "Back to Home" button works
```

### 6. Test Protection
```
1. Logout
2. Try to access /analyze directly
3. ✅ Should redirect to home
4. ✅ Auth modal should open
5. Login again
6. ✅ Should be able to access /analyze
```

### 7. Test Error Handling
```
1. Open upload modal
2. Try to submit without file
3. ✅ Should show error: "Please select a file"
4. Switch to Manual Entry
5. Try to submit without skills
6. ✅ Should show error: "Please enter your skills"
7. Try to submit without domain
8. ✅ Should show error: "Please select a domain"
```

### 8. Test Create Resume
```
1. Go to /analyze
2. Click "Create Resume" card
3. ✅ Should navigate to /create-resume
4. ✅ Should see placeholder page
5. ✅ "Back to Analyze" button works
```

## Expected Backend Logs

When testing, you should see in Flask terminal:
```
127.0.0.1 - - [DATE] "POST /api/analyze/upload HTTP/1.1" 200 -
127.0.0.1 - - [DATE] "POST /api/analyze/manual HTTP/1.1" 200 -
```

## Expected Console Logs

In browser console (F12):
```
// No errors
// Network tab shows successful API calls
```

## Test Checklist

- [ ] Can navigate to /analyze
- [ ] Upload modal opens
- [ ] Can upload file
- [ ] File validation works
- [ ] Manual entry works
- [ ] Loading states show
- [ ] Results page displays data
- [ ] Readiness score animates
- [ ] Skills listed correctly
- [ ] Can navigate back
- [ ] Routes are protected
- [ ] Auth modal opens when not logged in
- [ ] Error messages display
- [ ] Create resume page accessible
- [ ] Mobile responsive
- [ ] No console errors

## Common Issues

### Issue: Can't access /analyze
**Solution:** Make sure you're logged in

### Issue: Upload doesn't work
**Solution:** 
- Check backend is running
- Check file type (PDF, DOC, DOCX only)
- Check file size (< 10MB)

### Issue: Results page is blank
**Solution:** 
- Check backend response in Network tab
- Verify data is being passed via React Router state

### Issue: Modal doesn't open
**Solution:** 
- Check console for errors
- Verify modal state is updating

## Test Data

### Sample Skills for Manual Entry
```
Python, JavaScript, React, Node.js, SQL, Git, REST APIs, Problem Solving, Data Structures, Algorithms
```

### Sample Domains
- Software Development
- Data Science
- Web Development
- Machine Learning

## Success Indicators

✅ All routes work
✅ Authentication protection works
✅ File upload works
✅ Manual entry works
✅ Results display correctly
✅ Animations are smooth
✅ No console errors
✅ Mobile responsive
✅ Error handling works
✅ Loading states show

---

**Time to Test:** ~5 minutes
**Status:** Ready for Testing

Start the backend and frontend, then follow the steps above! 🚀
