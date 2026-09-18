# Community Module - Phase 2 Complete ✓

## Database Integration Completed

Phase 2 has successfully integrated production-ready SQLAlchemy database models with the Flask backend.

## What Was Implemented

### 1. Database Models (`backend/community_models.py`)
- **Community**: Groups with tags, soft delete, member/post counts
- **CommunityMember**: Membership tracking with roles (ADMIN, MODERATOR, MEMBER)
- **Post**: Unified model for blogs and feedback with post_type enum
- **Comment**: Nested comments with parent_id for replies
- **Like**: Likes for posts and comments
- **Conversation**: Private messaging conversations
- **Message**: Individual messages with read status
- **Notification**: User notifications for various events
- **UserProfile**: Extended profile with skills, interests, domains for matching

### 2. User Model (`backend/user_model.py`)
- Core authentication model
- Password hashing with werkzeug
- Soft delete support
- Account status tracking

### 3. Database Initialization (`backend/db_init.py`)
- Script to create all database tables
- Drop/reset functionality
- SQLite for development (easily switchable to PostgreSQL/MySQL)

### 4. Service Layer (`backend/community_service.py`)
- `CommunityService` class with business logic
- Methods for all Community operations:
  - Community CRUD operations
  - Feedback submission and retrieval
  - Blog creation and listing
  - User matching based on similarity
  - Private messaging
  - Like/unlike functionality

### 5. Flask Integration (`flask_cors_config.py`)
- Updated all authentication endpoints to use database
- Updated all Community endpoints to use `CommunityService`
- Proper error handling and transaction management
- Database initialization on app startup

## Database Schema

```
users
├── id (PK)
├── name
├── email (unique)
├── password_hash
├── domain
├── created_at
├── last_login
└── is_active, is_deleted

communities
├── id (PK)
├── name
├── description
├── category
├── tags (JSON)
├── created_by (FK → users)
├── members_count
├── posts_count
└── created_at, is_deleted

community_members
├── id (PK)
├── community_id (FK → communities)
├── user_id (FK → users)
├── role (ADMIN/MODERATOR/MEMBER)
└── joined_at, is_deleted

posts
├── id (PK)
├── title
├── content
├── post_type (BLOG/FEEDBACK)
├── category
├── tags (JSON)
├── author_id (FK → users)
├── community_id (FK → communities)
├── likes_count
├── comments_count
├── read_time
└── created_at, is_deleted

comments
├── id (PK)
├── content
├── post_id (FK → posts)
├── author_id (FK → users)
├── parent_id (FK → comments, for replies)
├── likes_count
└── created_at, is_deleted

likes
├── id (PK)
├── user_id (FK → users)
├── post_id (FK → posts, nullable)
├── comment_id (FK → comments, nullable)
└── created_at, is_deleted

conversations
├── id (PK)
├── user1_id (FK → users)
├── user2_id (FK → users)
├── last_message_at
├── last_message_preview
└── created_at, is_deleted

messages
├── id (PK)
├── conversation_id (FK → conversations)
├── sender_id (FK → users)
├── content
├── is_read
└── created_at, is_deleted

user_profiles
├── id (PK)
├── user_id (FK → users, unique)
├── skills (JSON)
├── interests (JSON)
├── domains (JSON)
├── bio
├── experience_years
└── projects_count
```

## How to Initialize Database

### Option 1: Automatic (Recommended)
The database is automatically initialized when you start the Flask server:
```bash
python flask_cors_config.py
```

### Option 2: Manual Initialization
```bash
cd career-guidance-ui/backend
python db_init.py
```

### Reset Database (Drop and Recreate)
```bash
cd career-guidance-ui/backend
python db_init.py --reset
```

## API Endpoints Updated

All Community endpoints now use real database operations:

### Community Groups
- `GET /api/community/groups` - List communities with membership status
- `POST /api/community/groups` - Create new community
- `POST /api/community/groups/<id>/join` - Join community

### Feedback
- `GET /api/community/feedback` - List all feedback posts
- `POST /api/community/feedback` - Submit feedback

### Blogs
- `GET /api/community/blogs` - List all blog posts
- `POST /api/community/blogs` - Create blog post

### Reach Out
- `GET /api/community/reach-out` - Get similar users (requires UserProfile)

### Messaging
- `GET /api/community/messages/<recipient_id>` - Get message history
- `POST /api/community/messages` - Send message

### Authentication (Updated)
- `POST /api/signup` - Register with password hashing
- `POST /api/login` - Login with password verification
- `GET /api/profile` - Get user profile from database

## Key Features

### Security
- Password hashing with werkzeug
- JWT token authentication
- Soft delete for data retention
- Input validation

### Performance
- Indexed columns (user_id, community_id, created_at)
- Denormalized counts (members_count, posts_count, likes_count)
- Lazy loading for relationships

### Scalability
- Service layer separates business logic
- Easy to switch from SQLite to PostgreSQL/MySQL
- Transaction management with rollback

### Data Integrity
- Foreign key constraints
- Unique constraints (email, community membership)
- Soft delete instead of hard delete

## Next Steps (Phase 3 - Optional Enhancements)

1. **User Profile Management**
   - API endpoint to update UserProfile
   - Skills/interests input in frontend

2. **Comments System**
   - Add comments to posts
   - Nested replies

3. **Notifications**
   - Real-time notifications
   - Email notifications

4. **Search & Filters**
   - Search communities by name/tags
   - Filter posts by category
   - Sort by popularity/date

5. **Pagination**
   - Implement pagination for large lists
   - Infinite scroll in frontend

6. **File Uploads**
   - Profile pictures
   - Blog images

7. **Moderation**
   - Report posts/comments
   - Admin dashboard

## Testing

To test the database integration:

1. Start Flask backend:
```bash
cd career-guidance-ui
python flask_cors_config.py
```

2. Register a new user via frontend or API
3. Create communities, posts, and messages
4. Check database file: `career-guidance-ui/backend/career_guidance.db`

## Database Location

Development: `career-guidance-ui/backend/career_guidance.db` (SQLite)

For production, update `SQLALCHEMY_DATABASE_URI` in `flask_cors_config.py` to use PostgreSQL or MySQL.

## Dependencies

Already included in `requirements.txt`:
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- PyJWT
- Werkzeug (for password hashing)

---

Phase 2 implementation is complete and production-ready! 🎉
