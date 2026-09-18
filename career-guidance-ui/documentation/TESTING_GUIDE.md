# Testing Guide: Reach-Out Feature

## ✅ Status: READY TO TEST

The Reach-Out feature is fully implemented and working. All backend tests pass.

---

## 🎯 What to Test

Test that users with the same domain appear in each other's Reach-Out section.

---

## 📋 Testing Steps

### Step 1: Ensure Flask Server is Running

```bash
cd career-guidance-ui
python flask_cors_config.py
```

You should see:
```
✅ Server is ready! Waiting for requests...
* Running on http://127.0.0.1:5000
```

### Step 2: Create Two Test Accounts

1. **Open your browser** and go to your app (usually `http://localhost:3000`)

2. **Create Account 1:**
   - Name: `Alice Test`
   - Email: `alice.test@example.com`
   - Password: `password123`
   - Domain: `Data Science` ⚠️ **IMPORTANT: Use exact same domain**

3. **Logout** (if needed)

4. **Create Account 2:**
   - Name: `Bob Test`
   - Email: `bob.test@example.com`
   - Password: `password123`
   - Domain: `Data Science` ⚠️ **IMPORTANT: Use exact same domain**

### Step 3: Test Reach-Out

1. **Login as Alice** (`alice.test@example.com`)

2. **Navigate to:** Community → Reach-Out

3. **Expected Result:**
   - You should see `Bob Test` in the list
   - Match score should be around 40-48% (domain match)
   - Profile card should show:
     - Name: Bob Test
     - Domain: Data Science
     - Match percentage
     - Message button

4. **Login as Bob** (`bob.test@example.com`)

5. **Navigate to:** Community → Reach-Out

6. **Expected Result:**
   - You should see `Alice Test` in the list
   - Match score should be around 40-48%

---

## ✅ Success Criteria

- ✅ Both users appear in each other's Reach-Out
- ✅ Match score is displayed (40-48% for same domain only)
- ✅ Profile information is shown correctly
- ✅ No errors in browser console
- ✅ No errors in Flask server logs

---

## 🔍 Troubleshooting

### Issue: Users don't appear in Reach-Out

**Check 1: Verify profiles were created**
```bash
cd career-guidance-ui
python -c "from flask_cors_config import app, db; from community_models import UserProfile; app.app_context().push(); profiles = UserProfile.query.all(); print(f'Total profiles: {len(profiles)}'); [print(f'  User {p.user_id}: {p.domains}') for p in profiles[-5:]]"
```

**Check 2: Verify same domain**
- Both users MUST have EXACTLY the same domain
- Case-sensitive: "Data Science" ≠ "data science"

**Check 3: Run migration script**
```bash
cd career-guidance-ui
python backend/create_missing_profiles.py
```

**Check 4: Check Flask logs**
- Look for errors when accessing `/api/community/reach-out`
- Should see 200 status code

### Issue: Match score is 0%

This means:
- Domains don't match exactly
- Check spelling and capitalization
- Update profile with: `PUT /api/profile` with `{"domains": ["Data Science"]}`

### Issue: "Please complete your profile" message

This means the user doesn't have a UserProfile record.

**Solution:**
```bash
cd career-guidance-ui
python backend/create_missing_profiles.py
```

---

## 🧪 Backend Tests (Optional)

Run automated tests to verify everything works:

```bash
cd career-guidance-ui

# Test 1: Profile matching algorithm
python backend/test_reach_out.py

# Test 2: Same domain matching
python backend/test_same_domain.py
```

Both should show: `✅ ALL TESTS PASSED!`

---

## 📊 Current Database Status

Run this to see existing profiles:

```bash
cd career-guidance-ui
python -c "from flask_cors_config import app, db; from community_models import UserProfile; from user_model import User; app.app_context().push(); profiles = UserProfile.query.all(); print(f'\nTotal profiles: {len(profiles)}\n'); users_with_profiles = [(User.query.get(p.user_id), p) for p in profiles]; [print(f'{u.name:20} | Domain: {u.domain:25} | Skills: {len(p.skills)}') for u, p in users_with_profiles if u]"
```

---

## 💡 Tips for Better Matches

After creating accounts, update profiles to get higher match scores:

**Update Profile API:**
```bash
PUT /api/profile
Authorization: Bearer <your_token>

{
  "skills": ["Python", "Machine Learning", "SQL"],
  "interests": ["AI", "Data Analysis"],
  "experience_years": 3,
  "bio": "Data scientist passionate about ML"
}
```

This will increase match scores:
- Same domain: 40%
- + Common skills: +30%
- + Similar experience: +20%
- + Common interests: +10%
- **Total: Up to 100%**

---

## 🎉 Expected Behavior

When everything works correctly:

1. **New signups** automatically get profiles
2. **Same domain users** appear in Reach-Out immediately (40-48% match)
3. **Adding skills/interests** increases match scores
4. **Message button** opens chat (if messaging is implemented)
5. **No errors** in console or server logs

---

## 📞 Need Help?

If you encounter issues:

1. Check Flask server logs for errors
2. Check browser console for errors
3. Verify database has profiles: `python backend/test_same_domain.py`
4. Run migration: `python backend/create_missing_profiles.py`
5. Restart Flask server

---

## ✨ What's Working

- ✅ Automatic profile creation on signup
- ✅ Profile matching algorithm (weighted scoring)
- ✅ Reach-Out API endpoint
- ✅ Frontend component (ReachOut.jsx)
- ✅ Database models (UserProfile)
- ✅ Migration script for existing users
- ✅ All backend tests passing

**Ready to test!** 🚀
