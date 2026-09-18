# Blog Video Upload Feature

## Overview
Added video upload functionality to blog posts. Users can now attach video URLs (YouTube, Vimeo, or direct video links) to their blogs, which will be displayed when viewing the blog.

## Changes Made

### 1. Backend Changes

#### Database Model (`community_models.py`)
- Added `video_url` field to `Post` model
- Field type: `String(1000)`, nullable
- Updated `to_dict()` method to include `video_url` in API responses

#### Service Layer (`community_service.py`)
- Updated `create_blog()` method to accept `video_url` parameter
- Video URL is optional and defaults to `None`

#### API Endpoint (`flask_cors_config.py`)
- Updated `POST /api/community/blogs` endpoint
- Now accepts `video_url` in request body
- Passes video URL to service layer

### 2. Frontend Changes

#### CreateBlogModal Component
- Added `videoUrl` field to form state
- Added video URL input field below content textarea
- Input accepts YouTube, Vimeo, or direct video URLs
- Sends `video_url` to backend API when creating blog

#### Blogs Component
- Added video player section below blog content
- Automatically detects video platform:
  - **YouTube**: Embeds using YouTube iframe player
  - **Vimeo**: Embeds using Vimeo iframe player
  - **Direct URLs**: Uses HTML5 video player
- Video player is responsive (100% width, 400px height)
- Only displays if `video_url` exists

### 3. Database Migration
- Created migration script: `add_video_url_to_posts.py`
- Safely adds `video_url` column to existing databases
- Checks if column already exists before adding

## Usage

### For Users

1. **Creating a Blog with Video:**
   - Click "Write Blog" button
   - Fill in title and content
   - Scroll down to "Video URL (Optional)" field
   - Paste your video URL (YouTube, Vimeo, or direct link)
   - Click "Publish Blog"

2. **Viewing Blogs with Videos:**
   - Videos appear below the blog content
   - Click play to watch the video
   - Videos are embedded and play within the page

### For Developers

1. **Run Database Migration:**
   ```bash
   cd career-guidance-ui/backend
   python add_video_url_to_posts.py
   ```

2. **Supported Video URLs:**
   - YouTube: `https://www.youtube.com/watch?v=VIDEO_ID`
   - YouTube Short: `https://youtu.be/VIDEO_ID`
   - Vimeo: `https://vimeo.com/VIDEO_ID`
   - Direct: `https://example.com/video.mp4`

3. **API Request Example:**
   ```json
   POST /api/community/blogs
   {
     "title": "My Blog Title",
     "content": "Blog content here...",
     "tags": ["React", "JavaScript"],
     "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
   }
   ```

4. **API Response Example:**
   ```json
   {
     "success": true,
     "blog": {
       "id": 1,
       "title": "My Blog Title",
       "content": "Blog content here...",
       "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
       "tags": ["React", "JavaScript"],
       "author_name": "John Doe",
       "created_at": "2026-03-08T10:30:00",
       ...
     }
   }
   ```

## Technical Details

### Video Embedding Logic

```javascript
// YouTube detection and embedding
if (url.includes('youtube.com') || url.includes('youtu.be')) {
  // Convert to embed URL
  embedUrl = url.replace('watch?v=', 'embed/')
                .replace('youtu.be/', 'youtube.com/embed/');
}

// Vimeo detection and embedding
if (url.includes('vimeo.com')) {
  // Convert to player URL
  embedUrl = url.replace('vimeo.com/', 'player.vimeo.com/video/');
}

// Direct video URLs
// Uses HTML5 <video> tag with controls
```

### Database Schema

```sql
ALTER TABLE posts ADD COLUMN video_url VARCHAR(1000);
```

### Security Considerations

- Video URLs are stored as strings (not uploaded files)
- No file upload handling required
- Videos are embedded from external sources
- XSS protection through React's built-in escaping

## Testing

### Manual Testing Steps

1. **Test Blog Creation with Video:**
   - Create a new blog
   - Add a YouTube URL
   - Verify blog is created successfully
   - Check video appears in blog list

2. **Test Different Video Platforms:**
   - YouTube: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
   - Vimeo: `https://vimeo.com/148751763`
   - Direct: Any `.mp4` URL

3. **Test Without Video:**
   - Create blog without video URL
   - Verify blog works normally
   - No video player should appear

4. **Test Video Playback:**
   - Click on a blog with video
   - Verify video loads and plays
   - Test fullscreen mode
   - Test video controls

### Database Migration Testing

```bash
# Run migration
cd career-guidance-ui/backend
python add_video_url_to_posts.py

# Expected output:
# ✅ Successfully added 'video_url' column
# ✅ MIGRATION COMPLETED SUCCESSFULLY!
```

## Backward Compatibility

- ✅ Existing blogs without videos continue to work
- ✅ Video URL is optional (nullable field)
- ✅ No breaking changes to existing API
- ✅ Frontend gracefully handles missing video URLs
- ✅ Database migration is safe and idempotent

## Files Modified

### Backend
1. `career-guidance-ui/backend/community_models.py` - Added video_url field
2. `career-guidance-ui/backend/community_service.py` - Updated create_blog method
3. `career-guidance-ui/flask_cors_config.py` - Updated API endpoint

### Frontend
1. `career-guidance-ui/src/components/community/CreateBlogModal.jsx` - Added video input
2. `career-guidance-ui/src/components/community/Blogs.jsx` - Added video player

### New Files
1. `career-guidance-ui/backend/add_video_url_to_posts.py` - Migration script
2. `career-guidance-ui/BLOG_VIDEO_FEATURE.md` - This documentation

## Future Enhancements

Potential improvements:
1. Video thumbnail preview in blog list
2. Multiple video support
3. Video upload to server (instead of URLs only)
4. Video validation (check if URL is accessible)
5. Video duration display
6. Auto-play options
7. Video quality selection

## Troubleshooting

### Issue: Video not displaying
**Solution:** 
- Check if video URL is valid
- Verify video is publicly accessible
- Check browser console for errors

### Issue: Migration fails
**Solution:**
- Check if database file exists
- Verify Flask app can connect to database
- Run migration script from correct directory

### Issue: YouTube video not embedding
**Solution:**
- Use full YouTube URL (not shortened)
- Ensure video is not private
- Check if video allows embedding

## Conclusion

The blog video feature is now fully implemented and ready to use. Users can enhance their blogs with videos from YouTube, Vimeo, or direct video URLs. The feature is backward compatible and doesn't affect existing functionality.

✅ All changes tested
✅ No errors introduced
✅ Backward compatible
✅ Ready for production
