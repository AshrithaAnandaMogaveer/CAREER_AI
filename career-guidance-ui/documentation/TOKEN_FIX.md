# Token Authentication Fix - 401 Unauthorized Error

## Problem

Users were getting 401 UNAUTHORIZED errors when trying to save progress:
```
Failed to load resource: the server responded with a status of 401 (UNAUTHORIZED)
Failed to create topic record: Invalid token
✅ Successfully created 0/6 topic records (6 failed)
```

## Root Cause

The authentication system stores the token as `authToken` in localStorage, but RoutineBuild.jsx was trying to retrieve it using the wrong key `token`:

```javascript
// WRONG ❌
const token = localStorage.getItem('token');

// CORRECT ✅
const token = localStorage.getItem('authToken');
```

## Solution Applied

Fixed two locations in `career-guidance-ui/src/pages/RoutineBuild.jsx`:

### 1. loadSavedProgress() Function (Line ~100)
**Before:**
```javascript
const token = localStorage.getItem('token');
```

**After:**
```javascript
const token = localStorage.getItem('authToken'); // Fixed: use 'authToken' not 'token'
if (!token) {
    console.warn('No auth token found');
    // Initialize with zeros
    ...
}
```

### 2. handleSaveProgress() Function (Line ~254)
**Before:**
```javascript
const token = localStorage.getItem('token');
```

**After:**
```javascript
const token = localStorage.getItem('authToken'); // Fixed: use 'authToken' not 'token'

if (!token) {
    console.error('❌ No auth token found - cannot create topic records');
    alert(`Progress saved! ${skill}: ${pct}%\nWarning: Not logged in, topic records not created.`);
    setIsSavingProgress(false);
    return;
}
```

### 3. Enhanced Error Handling
Added better error handling for 401 responses:

```javascript
if (!response.ok) {
    const errorData = await response.json();
    failCount++;
    console.error(`Failed to create topic record: ${errorData.message || response.statusText}`);
    
    if (response.status === 401) {
        console.error('❌ Token expired or invalid - please re-login');
        alert('Session expired. Please login again.');
        setIsSavingProgress(false);
        return;
    }
}
```

## How Authentication Works

### Token Storage (authService.js)
When user logs in or signs up:
```javascript
localStorage.setItem('authToken', data.token);  // Stored as 'authToken'
localStorage.setItem('user', JSON.stringify(data.user));
```

### Token Retrieval
```javascript
import { getStoredToken } from './authService';

const token = getStoredToken();  // Returns localStorage.getItem('authToken')
```

### Token Usage
```javascript
headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
}
```

## Testing

### 1. Verify Token Exists
Open browser console (F12) and run:
```javascript
console.log('Auth Token:', localStorage.getItem('authToken'));
console.log('User:', localStorage.getItem('user'));
```

Expected output:
```
Auth Token: eyJ0eXAiOiJKV1QiLCJhbGc...  (long string)
User: {"id":24,"name":"Test User","email":"test@example.com",...}
```

### 2. Test Progress Saving
1. Go to Routine Build → Progress Tracking
2. Adjust slider to 50%
3. Click "Save"
4. Watch console for:
   ```
   💾 Saving progress for Python: 50%
   ✅ Progress saved for Python
   📝 Creating 4 topic records for Python (50% of 8 weeks)
   ✅ Successfully created 4/4 topic records (0 failed)
   ```

### 3. Test Evolution Charts
1. Go to Evolution Over Time tab
2. Click "Refresh Data"
3. Should see charts with data
4. No 401 errors in console

## If Still Getting 401 Errors

### Check 1: Token Exists
```javascript
if (!localStorage.getItem('authToken')) {
    console.error('No token found - please login');
}
```

### Check 2: Token Valid
The token might be expired. Solution:
1. Logout
2. Login again
3. Try saving progress again

### Check 3: Backend Running
Make sure Flask server is running:
```bash
cd career-guidance-ui
python flask_cors_config.py
```

### Check 4: Token Format
Token should start with `eyJ`:
```javascript
const token = localStorage.getItem('authToken');
console.log('Token starts with eyJ:', token?.startsWith('eyJ'));
```

## Console Output After Fix

### Successful Save:
```
💾 Saving progress for Python: 75%
✅ Progress saved for Python
📝 Creating 6 topic records for Python (75% of 8 weeks)
✅ Successfully created 6/6 topic records (0 failed)
```

### If Not Logged In:
```
❌ No auth token found - cannot create topic records
Alert: "Progress saved! Python: 75%
Warning: Not logged in, topic records not created."
```

### If Token Expired:
```
Failed to create topic record: Invalid token
❌ Token expired or invalid - please re-login
Alert: "Session expired. Please login again."
```

## Files Modified

- `career-guidance-ui/src/pages/RoutineBuild.jsx`
  - Line ~100: Fixed `loadSavedProgress()` to use 'authToken'
  - Line ~254: Fixed `handleSaveProgress()` to use 'authToken'
  - Added token validation checks
  - Added better 401 error handling

## Related Files (No Changes Needed)

- `career-guidance-ui/src/services/authService.js` - Already correct
- `career-guidance-ui/src/services/routineService.js` - Already using getStoredToken()

## Summary

✅ Fixed token retrieval to use correct key 'authToken'
✅ Added token validation before API calls
✅ Enhanced error handling for 401 responses
✅ Better user feedback when token is missing/expired
✅ Clear console messages for debugging

The 401 errors should now be resolved. Users will see clear messages if they need to re-login.
