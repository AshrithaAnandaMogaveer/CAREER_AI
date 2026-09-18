# Delete Functionality - Testing Guide

## Quick Test Steps

### 1. Start the Application
```bash
# Terminal 1 - Backend
cd career-guidance-ui/backend
python flask_cors_config.py

# Terminal 2 - Frontend
cd career-guidance-ui
npm start
```

### 2. Login to the Application
- Go to http://localhost:3000
- Login with your credentials
- Navigate to Community page

### 3. Test Blog Delete

**Steps**:
1. Go to "Blogs" tab in Community
2. Find a blog post you created
3. Look for trash icon (🗑️) in the top-right of your blog card
4. Click the trash icon
5. Confirm deletion in the modal
6. Verify blog disappears from the list

**Expected Behavior**:
- ✓ Trash icon only appears on YOUR blogs
- ✓ Trash icon does NOT appear on other users' blogs
- ✓ Clicking trash icon shows confirmation modal
- ✓ Clicking "Delete" removes the blog
- ✓ Clicking "Cancel" closes modal without deleting

### 4. Test Community Delete

**Steps**:
1. Go to "Community Groups" tab
2. Find a community you created
3. Look for trash icon (🗑️) in the top-right of your community card
4. Click the trash icon
5. Confirm deletion in the modal
6. Verify community disappears from both "All" and "Recommended" tabs

**Expected Behavior**:
- ✓ Trash icon only appears on communities YOU created
- ✓ Trash icon does NOT appear on communities created by others
- ✓ Clicking trash icon shows confirmation modal with warning
- ✓ Clicking "Delete" removes the community
- ✓ Clicking "Cancel" closes modal without deleting

### 5. Test Feedback Delete

**Steps**:
1. Go to "Feedback" tab in Community
2. Find a feedback post you submitted
3. Look for trash icon (🗑️) in the top-right of your feedback card
4. Click the trash icon
5. Confirm deletion in the modal
6. Verify feedback disappears from the list

**Expected Behavior**:
- ✓ Trash icon only appears on YOUR feedback
- ✓ Trash icon does NOT appear on other users' feedback
- ✓ Clicking trash icon shows confirmation modal
- ✓ Clicking "Delete" removes the feedback
- ✓ Clicking "Cancel" closes modal without deleting

## Verification Checklist

### Authorization Tests
- [ ] Delete button only visible to content owner
- [ ] Delete button NOT visible to other users
- [ ] Backend rejects unauthorized delete attempts

### UI/UX Tests
- [ ] Trash icon appears in correct position
- [ ] Trash icon turns red on hover
- [ ] Confirmation modal appears on click
- [ ] Modal has clear warning message
- [ ] Cancel button works correctly
- [ ] Delete button shows loading state
- [ ] Content disappears after successful deletion

### Error Handling Tests
- [ ] Error message shown if deletion fails
- [ ] Network errors handled gracefully
- [ ] Invalid token shows appropriate error
- [ ] Already deleted content shows error

## Browser Console Checks

### Check Current User
```javascript
// Open browser console (F12)
const user = JSON.parse(localStorage.getItem('user'));
console.log('Current User ID:', user.id);
console.log('Current User Name:', user.name);
```

### Check Blog Author IDs
```javascript
// After blogs load, check in console
// Look for the blog data in Network tab or React DevTools
```

### Check for Errors
```javascript
// Watch console for:
// - "Error deleting blog/community/feedback"
// - 401 Unauthorized errors
// - Network errors
```

## Backend Verification

### Run Test Script
```bash
cd career-guidance-ui/backend
python test_delete_api.py
```

This will verify:
- ✓ Blogs include `author_id`
- ✓ Communities include `created_by`
- ✓ Feedback includes `author_id`

### Check Database
```bash
cd career-guidance-ui/backend
sqlite3 career_guidance.db

# Check if content is soft-deleted (not hard-deleted)
SELECT id, title, author_id, is_deleted, deleted_at FROM posts WHERE post_type='BLOG' LIMIT 5;
SELECT id, name, created_by, is_deleted, deleted_at FROM communities LIMIT 5;
SELECT id, content, author_id, is_deleted, deleted_at FROM posts WHERE post_type='FEEDBACK' LIMIT 5;
```

## Common Issues & Solutions

### Issue: Delete button not appearing

**Solution 1**: Verify you're logged in
```javascript
// Check in browser console
localStorage.getItem('authToken')  // Should return a token
localStorage.getItem('user')       // Should return user JSON
```

**Solution 2**: Verify you own the content
- Delete button only appears for content YOU created
- Check that your user ID matches the content's author/creator ID

**Solution 3**: Clear cache and reload
```javascript
// In browser console
localStorage.clear()
// Then login again
```

### Issue: Delete fails with 401 error

**Solution**: Token might be expired
```javascript
// Clear storage and login again
localStorage.clear()
// Navigate to login page
```

### Issue: Delete fails with 403 error

**Solution**: You don't have permission
- You can only delete content you created
- For communities, only creators/admins can delete

### Issue: Delete button appears but nothing happens

**Solution**: Check browser console for errors
- Open DevTools (F12)
- Look for JavaScript errors
- Check Network tab for failed API calls

## API Endpoints

### Delete Blog
```
DELETE http://localhost:5000/api/community/blogs/{post_id}
Headers: Authorization: Bearer {token}
```

### Delete Community
```
DELETE http://localhost:5000/api/community/groups/{community_id}
Headers: Authorization: Bearer {token}
```

### Delete Feedback
```
DELETE http://localhost:5000/api/community/feedback/{post_id}
Headers: Authorization: Bearer {token}
```

## Test with cURL

### Delete Blog
```bash
curl -X DELETE http://localhost:5000/api/community/blogs/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Delete Community
```bash
curl -X DELETE http://localhost:5000/api/community/groups/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Delete Feedback
```bash
curl -X DELETE http://localhost:5000/api/community/feedback/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Success Criteria

All tests pass when:
1. ✓ Delete buttons appear only for content owner
2. ✓ Confirmation modals work correctly
3. ✓ Content is removed from UI after deletion
4. ✓ Backend soft-deletes (sets is_deleted=True)
5. ✓ Unauthorized users cannot delete
6. ✓ Error messages are clear and helpful
7. ✓ No console errors
8. ✓ No broken functionality in other features
