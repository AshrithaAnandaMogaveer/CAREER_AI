# 🧪 Backend Integration Testing Checklist

## Pre-Testing Setup

### 1. Start Backend
```bash
python flask_cors_config.py
```
✅ Backend running on http://localhost:5000

### 2. Start Frontend
```bash
cd career-guidance-ui
npm start
```
✅ Frontend running on http://localhost:5173

### 3. Open Browser Console
- Press F12
- Go to Console tab
- Keep it open to see logs

## 🔐 Login Flow Testing

### Test 1: Successful Login
**Steps:**
1. Click "Login / Sign Up" button
2. Enter credentials:
   - Email: `test@example.com`
   - Password: `password123`
3. Click "Login" button

**Expected Results:**
- [ ] Loading state shows "Logging in..."
- [ ] Modal closes after success
- [ ] Navbar shows "Profile" button
- [ ] Console logs: "User authenticated"
- [ ] localStorage has `authToken`
- [ ] localStorage has `user` data

**Check localStorage:**
```javascript
// In browser console
localStorage.getItem('authToken')
localStorage.getItem('user')
```

### Test 2: Invalid Email Format
**Steps:**
1. Open login modal
2. Enter: `invalid-email`
3. Click "Login"

**Expected Results:**
- [ ] Error message: "Invalid email format"
- [ ] Modal stays open
- [ ] No API call made
- [ ] UI doesn't break

### Test 3: Short Password
**Steps:**
1. Open login modal
2. Enter:
   - Email: `test@example.com`
   - Password: `123`
3. Click "Login"

**Expected Results:**
- [ ] Error message: "Password must be at least 6 characters"
- [ ] Modal stays open
- [ ] No API call made

### Test 4: Empty Fields
**Steps:**
1. Open login modal
2. Leave fields empty
3. Click "Login"

**Expected Results:**
- [ ] Error messages for both fields
- [ ] Modal stays open
- [ ] No API call made

### Test 5: Backend Error (Wrong Credentials)
**Steps:**
1. Open login modal
2. Enter wrong credentials
3. Click "Login"

**Expected Results:**
- [ ] Red error box appears
- [ ] Error message from backend
- [ ] Modal stays open
- [ ] Button re-enabled

## 📝 Signup Flow Testing

### Test 6: Successful Signup
**Steps:**
1. Click "Login / Sign Up"
2. Click "Sign Up" tab
3. Fill all fields:
   - Name: `John Doe`
   - Email: `john@example.com`
   - Password: `password123`
   - Confirm: `password123`
   - Domain: `Software Development`
   - ✓ Agree to terms
4. Click "Sign Up"

**Expected Results:**
- [ ] Loading state shows "Signing up..."
- [ ] Modal closes after success
- [ ] Navbar shows "John Doe"
- [ ] Console logs: "User authenticated"
- [ ] localStorage has `authToken`
- [ ] localStorage has `user` data

### Test 7: Password Mismatch
**Steps:**
1. Open signup modal
2. Enter:
   - Password: `password123`
   - Confirm: `password456`
3. Click "Sign Up"

**Expected Results:**
- [ ] Error: "Passwords do not match"
- [ ] Modal stays open
- [ ] No API call made

### Test 8: Missing Domain
**Steps:**
1. Fill all fields except domain
2. Click "Sign Up"

**Expected Results:**
- [ ] Error: "Please select a domain of interest"
- [ ] Modal stays open
- [ ] No API call made

### Test 9: Terms Not Agreed
**Steps:**
1. Fill all fields
2. Don't check terms checkbox
3. Click "Sign Up"

**Expected Results:**
- [ ] Error: "You must agree to the terms and conditions"
- [ ] Modal stays open
- [ ] No API call made

## 🔄 Session Management Testing

### Test 10: Session Restoration
**Steps:**
1. Login successfully
2. Refresh page (F5)

**Expected Results:**
- [ ] Still logged in
- [ ] Navbar shows "Profile"
- [ ] Console logs: "User session restored"
- [ ] No modal appears

### Test 11: Logout
**Steps:**
1. Login successfully
2. Click "Logout" button

**Expected Results:**
- [ ] Navbar shows "Login / Sign Up"
- [ ] Console logs: "User logged out"
- [ ] localStorage cleared
- [ ] Can't access profile

### Test 12: Logout Persistence
**Steps:**
1. Login
2. Logout
3. Refresh page

**Expected Results:**
- [ ] Still logged out
- [ ] Navbar shows "Login / Sign Up"
- [ ] localStorage empty

## 🌐 Network Testing

### Test 13: Backend Offline
**Steps:**
1. Stop Flask backend
2. Try to login

**Expected Results:**
- [ ] Error message appears
- [ ] UI doesn't crash
- [ ] Button re-enabled
- [ ] Modal stays open

### Test 14: Slow Network
**Steps:**
1. Open DevTools → Network tab
2. Set throttling to "Slow 3G"
3. Try to login

**Expected Results:**
- [ ] Loading state visible
- [ ] Button disabled during request
- [ ] Eventually succeeds or fails
- [ ] UI remains responsive

### Test 15: CORS Check
**Steps:**
1. Check browser console during login
2. Look for CORS errors

**Expected Results:**
- [ ] No CORS errors
- [ ] Request completes successfully
- [ ] Response received

## 🎨 UI/UX Testing

### Test 16: Modal Animations
**Steps:**
1. Open modal
2. Switch tabs
3. Close modal

**Expected Results:**
- [ ] Modal opens with scale animation
- [ ] Backdrop blurs smoothly
- [ ] Tab switch slides smoothly
- [ ] Modal closes with animation
- [ ] No animation glitches

### Test 17: Error Display
**Steps:**
1. Trigger validation error
2. Check error message

**Expected Results:**
- [ ] Error appears below field
- [ ] Red color
- [ ] Smooth fade-in animation
- [ ] Doesn't break layout

### Test 18: Loading State
**Steps:**
1. Submit login form
2. Watch button

**Expected Results:**
- [ ] Button text changes to "Logging in..."
- [ ] Button disabled (opacity 50%)
- [ ] No hover animation
- [ ] Can't click again

### Test 19: Mobile Responsive
**Steps:**
1. Resize browser to mobile width
2. Test login flow

**Expected Results:**
- [ ] Modal fits screen
- [ ] Forms scrollable
- [ ] Buttons touch-friendly
- [ ] No horizontal scroll

## 🔒 Security Testing

### Test 20: Token in Header
**Steps:**
1. Login successfully
2. Open DevTools → Network tab
3. Make a profile request (if implemented)

**Expected Results:**
- [ ] Authorization header present
- [ ] Format: `Bearer TOKEN`
- [ ] Token matches localStorage

### Test 21: Token Expiration
**Steps:**
1. Login
2. Manually expire token in backend
3. Try to access protected route

**Expected Results:**
- [ ] 401 error received
- [ ] Auto logout triggered
- [ ] Redirected to login

### Test 22: XSS Prevention
**Steps:**
1. Try to enter `<script>alert('xss')</script>` in name field
2. Submit form

**Expected Results:**
- [ ] Script doesn't execute
- [ ] Stored safely
- [ ] Displayed safely

## 📊 Console Logs Check

### Expected Console Logs

**On Login:**
```
User authenticated: {name: "...", email: "...", domain: "..."}
```

**On Signup:**
```
User authenticated: {name: "...", email: "...", domain: "..."}
```

**On Logout:**
```
User logged out
```

**On Page Reload (if logged in):**
```
User session restored: {name: "...", email: "...", domain: "..."}
```

**On Error:**
```
Login error: Error message
```

## 🎯 Final Checklist

### Functionality
- [ ] Login works
- [ ] Signup works
- [ ] Logout works
- [ ] Session restores
- [ ] Errors display
- [ ] Validation works
- [ ] Loading states work

### UI/UX
- [ ] Animations smooth
- [ ] No layout breaks
- [ ] Mobile responsive
- [ ] Error messages clear
- [ ] Loading indicators visible

### Security
- [ ] Token stored
- [ ] Token sent in header
- [ ] Auto logout on 401
- [ ] localStorage cleared on logout

### Performance
- [ ] No console errors
- [ ] No memory leaks
- [ ] Fast response times
- [ ] Smooth animations

## 🐛 Common Issues & Solutions

### Issue: CORS Error
**Solution:**
```python
# In Flask backend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### Issue: Token Not Stored
**Check:**
```javascript
// In authService.js
if (data.success && data.token) {
  localStorage.setItem('authToken', data.token);
  localStorage.setItem('user', JSON.stringify(data.user));
}
```

### Issue: Session Not Restored
**Check:**
```javascript
// In App.js useEffect
if (isAuthenticated()) {
  const storedUser = getStoredUser();
  if (storedUser) {
    setUser(storedUser);
    setIsLoggedIn(true);
  }
}
```

### Issue: Error Not Displayed
**Check:**
```javascript
// In AuthModal.jsx
{errors.general && (
  <motion.div className="...">
    {errors.general}
  </motion.div>
)}
```

## 📝 Test Report Template

```
Date: ___________
Tester: ___________
Browser: ___________
Backend: Running / Not Running

Login Tests: ___/5 passed
Signup Tests: ___/4 passed
Session Tests: ___/3 passed
Network Tests: ___/3 passed
UI/UX Tests: ___/4 passed
Security Tests: ___/3 passed

Total: ___/22 passed

Issues Found:
1. _______________________
2. _______________________
3. _______________________

Notes:
_______________________
_______________________
```

---

**All tests passing?** ✅ Backend integration is working perfectly!

**Some tests failing?** Check the Common Issues section above.
