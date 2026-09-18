# Community Chat Room Feature

## Overview
Added a real-time chat room feature for community members to communicate, share images, and exchange ideas.

## Features Implemented

### 1. Community Chat Room Component
**File:** `src/components/community/CommunityChatRoom.jsx`

Features:
- Real-time messaging (polls every 5 seconds)
- Image upload support (max 5MB)
- Member list sidebar
- Message history
- User avatars
- Timestamp display
- Responsive design
- Dark theme UI

### 2. Updated CommunityGroups Component
**File:** `src/components/community/CommunityGroups.jsx`

Changes:
- Changed "Joined" button to "💬 Open Chat Room" for joined communities
- Opens chat room modal when clicked
- No changes to existing join functionality

### 3. Backend API Endpoints
**File:** `flask_cors_config.py`

New endpoints:
- `GET /api/community/<community_id>/messages` - Get chat messages
- `POST /api/community/message/send` - Send message with optional image
- `GET /api/community/<community_id>/members` - Get community members
- `GET /uploads/community_images/<filename>` - Serve uploaded images

### 4. Service Layer Methods
**File:** `backend/community_service.py`

New methods:
- `get_community_messages(community_id, limit)` - Fetch messages
- `send_community_message(community_id, user_id, content, image_url)` - Send message
- `get_community_members(community_id)` - Get member list

### 5. Database Changes
**File:** `backend/community_models.py`

Changes:
- Added `CHAT_MESSAGE` to `PostType` enum
- Uses existing `Post` model for chat messages
- Images stored as URL markers in content field

## How It Works

### User Flow
1. User joins a community
2. "Join Community" button changes to "💬 Open Chat Room"
3. Click button to open chat room modal
4. View message history
5. Send text messages
6. Upload and share images
7. View member list
8. Real-time updates every 5 seconds

### Technical Flow

#### Sending Messages
1. User types message and/or selects image
2. Frontend sends FormData to `/api/community/message/send`
3. Backend validates membership
4. Image saved to `uploads/community_images/` directory
5. Message created as Post with type `CHAT_MESSAGE`
6. Image URL embedded in content as `[IMAGE:url]`
7. Success response returned

#### Receiving Messages
1. Frontend polls `/api/community/<id>/messages` every 5 seconds
2. Backend queries Post table for `CHAT_MESSAGE` type
3. Parses content to extract text and image URL
4. Returns messages with user information
5. Frontend displays messages in chat UI

### Security
- Only community members can view messages
- Only community members can send messages
- Membership validated on every request
- JWT token required for all endpoints
- Image size limited to 5MB
- Secure filename generation

## File Structure

```
career-guidance-ui/
├── src/
│   └── components/
│       └── community/
│           ├── CommunityChatRoom.jsx (NEW)
│           └── CommunityGroups.jsx (UPDATED)
├── backend/
│   ├── community_service.py (UPDATED)
│   └── community_models.py (UPDATED)
├── flask_cors_config.py (UPDATED)
└── uploads/
    └── community_images/ (NEW - auto-created)
```

## API Documentation

### GET /api/community/<community_id>/messages
Get all messages in a community chat room.

**Headers:**
- Authorization: Bearer <token>

**Response:**
```json
{
  "success": true,
  "messages": [
    {
      "id": 1,
      "user_id": 1,
      "user_name": "John Doe",
      "content": "Hello everyone!",
      "image_url": null,
      "created_at": "2026-03-01T10:30:00"
    }
  ],
  "count": 1
}
```

### POST /api/community/message/send
Send a message to a community chat room.

**Headers:**
- Authorization: Bearer <token>
- Content-Type: multipart/form-data

**Body (FormData):**
- community_id: integer (required)
- content: string (optional if image provided)
- image: file (optional, max 5MB)

**Response:**
```json
{
  "success": true,
  "message": "Message sent successfully",
  "message_id": 123
}
```

### GET /api/community/<community_id>/members
Get all members of a community.

**Headers:**
- Authorization: Bearer <token>

**Response:**
```json
{
  "success": true,
  "members": [
    {
      "user_id": 1,
      "user_name": "John Doe",
      "role": "ADMIN",
      "joined_at": "2026-03-01T10:00:00"
    }
  ],
  "count": 1
}
```

## UI Components

### Chat Room Modal
- Full-screen modal overlay
- Header with community name and member count
- Scrollable message area
- Message input with image upload
- Member sidebar (toggleable)
- Close button

### Message Display
- User avatar (colored circle with initial)
- User name (for others' messages)
- Message content
- Image preview (if attached)
- Timestamp (relative time)
- Different styling for own vs others' messages

### Input Area
- Image upload button
- Multi-line text input
- Send button
- Image preview with remove option
- Keyboard shortcuts (Enter to send, Shift+Enter for new line)

## Features

### Real-time Updates
- Polls for new messages every 5 seconds
- Auto-scrolls to bottom on new messages
- Shows "Just now" for recent messages

### Image Sharing
- Click image icon to select file
- Preview before sending
- Remove image before sending
- Images displayed inline in chat
- Max size: 5MB
- Supported formats: All image types

### Member Management
- View all community members
- See member roles (ADMIN/MEMBER)
- Admin badge for administrators
- Member count in header

## Keyboard Shortcuts
- **Enter** - Send message
- **Shift+Enter** - New line in message
- **Esc** - Close chat room (can be added)

## Styling
- Dark theme consistent with app
- Teal accent color for own messages
- Gray for others' messages
- Smooth animations
- Responsive design
- Mobile-friendly

## Performance Considerations
- Message limit: 100 most recent
- Polling interval: 5 seconds
- Image size limit: 5MB
- Auto-scroll optimization
- Efficient re-renders

## Future Enhancements (Optional)
1. WebSocket for real-time updates (no polling)
2. Message editing and deletion
3. Reply to specific messages
4. Emoji picker
5. File attachments (PDFs, docs)
6. Voice messages
7. Video sharing
8. Message search
9. Pinned messages
10. Read receipts
11. Typing indicators
12. Message reactions
13. User mentions (@username)
14. Link previews
15. Code syntax highlighting

## Testing

### Manual Testing Steps
1. Create a community
2. Join the community
3. Click "Open Chat Room"
4. Send a text message
5. Upload and send an image
6. View member list
7. Check message timestamps
8. Verify real-time updates
9. Test with multiple users
10. Test image size limits

### Test Scenarios
- ✅ Send text-only message
- ✅ Send image-only message
- ✅ Send text + image message
- ✅ View message history
- ✅ View member list
- ✅ Real-time message updates
- ✅ Image preview before sending
- ✅ Remove image before sending
- ✅ Keyboard shortcuts
- ✅ Responsive design
- ✅ Member-only access

## Compatibility
- No breaking changes to existing features
- Works with existing authentication
- Uses existing database models
- Compatible with all existing endpoints
- Maintains backward compatibility

## Security Notes
- Membership validation on every request
- JWT authentication required
- Image size limits enforced
- Secure file naming
- SQL injection prevention (ORM)
- XSS prevention (React escaping)

## Deployment Notes
- Create `uploads/community_images/` directory
- Set proper permissions for uploads folder
- Configure max upload size in web server
- Consider CDN for image serving in production
- Set up image optimization pipeline
- Configure backup for uploaded images

---

**Status:** ✅ COMPLETE & READY TO USE

**Version:** 1.0.0  
**Date:** March 1, 2026  
**Breaking Changes:** None  
**Dependencies:** None (uses existing stack)

