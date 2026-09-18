# SQLite Database Information

## Database File Location

**Main Database File:**
```
career-guidance-ui/backend/career_guidance.db
```

This is the SQLite database file that stores all application data.

## Database Type
- **Database**: SQLite
- **File Format**: `.db` (SQLite database file)
- **Location**: Backend folder

## How to Access the Database

### Method 1: Using SQLite Command Line
```bash
# Navigate to backend folder
cd career-guidance-ui/backend

# Open database with sqlite3
sqlite3 career_guidance.db

# Once inside, you can run SQL commands
.tables                    # List all tables
.schema                    # Show all table schemas
.schema table_name         # Show specific table schema
SELECT * FROM users;       # Query data
.quit                      # Exit
```

### Method 2: Using DB Browser for SQLite (GUI)
1. Download DB Browser for SQLite: https://sqlitebrowser.org/
2. Open the application
3. Click "Open Database"
4. Navigate to `career-guidance-ui/backend/career_guidance.db`
5. Browse tables, run queries, and view data visually

### Method 3: Using Python
```python
import sqlite3

# Connect to database
conn = sqlite3.connect('career_guidance.db')
cursor = conn.cursor()

# Execute query
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# Print results
for row in rows:
    print(row)

# Close connection
conn.close()
```

### Method 4: Using VS Code Extension
1. Install "SQLite" extension in VS Code
2. Right-click on `career_guidance.db` file
3. Select "Open Database"
4. View tables and data in VS Code

## Database Tables

Based on the models in your application, the database contains these tables:

### User Management
- **users** - User accounts and authentication
- **user_profiles** - Extended user profile information

### Community Features
- **communities** - Community groups
- **community_members** - Community membership records
- **posts** - Blog posts and feedback (unified table)
- **comments** - Comments on posts
- **likes** - Likes on posts
- **conversations** - Direct message conversations
- **messages** - Individual messages in conversations
- **notifications** - User notifications

### Progress Tracking
- **routine_progress** - User routine progress tracking
- **weekly_progress** - Weekly progress records
- **topic_completion** - Topic completion tracking

## Common SQL Queries

### View All Users
```sql
SELECT id, name, email, domain, created_at FROM users;
```

### View All Communities
```sql
SELECT id, name, description, created_by, members_count, created_at 
FROM communities 
WHERE is_deleted = 0;
```

### View All Blogs
```sql
SELECT id, title, content, author_id, created_at 
FROM posts 
WHERE post_type = 'BLOG' AND is_deleted = 0;
```

### View All Feedback
```sql
SELECT id, content, category, author_id, created_at 
FROM posts 
WHERE post_type = 'FEEDBACK' AND is_deleted = 0;
```

### View Deleted Content (Soft Deletes)
```sql
-- Deleted blogs
SELECT id, title, author_id, deleted_at 
FROM posts 
WHERE post_type = 'BLOG' AND is_deleted = 1;

-- Deleted communities
SELECT id, name, created_by, deleted_at 
FROM communities 
WHERE is_deleted = 1;

-- Deleted feedback
SELECT id, content, author_id, deleted_at 
FROM posts 
WHERE post_type = 'FEEDBACK' AND is_deleted = 1;
```

### Restore Deleted Content
```sql
-- Restore a blog
UPDATE posts 
SET is_deleted = 0, deleted_at = NULL 
WHERE id = 1 AND post_type = 'BLOG';

-- Restore a community
UPDATE communities 
SET is_deleted = 0, deleted_at = NULL 
WHERE id = 1;

-- Restore feedback
UPDATE posts 
SET is_deleted = 0, deleted_at = NULL 
WHERE id = 1 AND post_type = 'FEEDBACK';
```

### View User's Content
```sql
-- User's blogs
SELECT id, title, created_at 
FROM posts 
WHERE author_id = 1 AND post_type = 'BLOG' AND is_deleted = 0;

-- User's communities
SELECT id, name, created_at 
FROM communities 
WHERE created_by = 1 AND is_deleted = 0;

-- User's feedback
SELECT id, content, created_at 
FROM posts 
WHERE author_id = 1 AND post_type = 'FEEDBACK' AND is_deleted = 0;
```

## Database Backup

### Create Backup
```bash
# Navigate to backend folder
cd career-guidance-ui/backend

# Create backup with timestamp
cp career_guidance.db career_guidance_backup_$(date +%Y%m%d_%H%M%S).db

# Or on Windows
copy career_guidance.db career_guidance_backup.db
```

### Restore from Backup
```bash
# Stop the Flask server first!
# Then restore
cp career_guidance_backup.db career_guidance.db

# Or on Windows
copy career_guidance_backup.db career_guidance.db
```

## Database Configuration

The database configuration is in:
- **File**: `career-guidance-ui/backend/app_config.py`
- **Connection String**: `sqlite:///career_guidance.db`

## Database Initialization

To initialize or reset the database:

```bash
cd career-guidance-ui/backend
python db_init.py
```

This will:
1. Create all tables based on models
2. Set up relationships
3. Create indexes

## Important Notes

### Soft Delete
The application uses soft delete for:
- Communities
- Posts (Blogs and Feedback)
- Comments
- Community Members

This means deleted items have:
- `is_deleted = 1` (True)
- `deleted_at = timestamp`

Data is NOT physically removed from the database.

### File Storage
Some data is stored as files, not in the database:
- **Videos**: `career-guidance-ui/backend/uploads/videos/`
- **Images**: `career-guidance-ui/backend/uploads/community_images/`

### Database Size
To check database size:
```bash
# On Linux/Mac
ls -lh career_guidance.db

# On Windows
dir career_guidance.db
```

## Troubleshooting

### Database Locked Error
If you get "database is locked" error:
1. Stop the Flask server
2. Close any database browser tools
3. Restart the Flask server

### Corrupted Database
If database is corrupted:
1. Stop the Flask server
2. Restore from backup
3. If no backup, delete `career_guidance.db`
4. Run `python db_init.py` to recreate

### Migration Issues
If you change models and need to update database:
1. Stop the Flask server
2. Backup the database
3. Run migration script or recreate database
4. Restart the Flask server

## Security

### Database Access
- Database file should NOT be publicly accessible
- Keep in backend folder (not in public/static folders)
- Add to `.gitignore` if it contains sensitive data

### Backup Strategy
- Regular backups (daily/weekly)
- Store backups securely
- Test restore process periodically

## Tools & Resources

### Recommended Tools
1. **DB Browser for SQLite** - https://sqlitebrowser.org/
2. **SQLite Studio** - https://sqlitestudio.pl/
3. **DBeaver** - https://dbeaver.io/ (Universal database tool)
4. **VS Code SQLite Extension** - Search "SQLite" in VS Code extensions

### SQLite Documentation
- Official Docs: https://www.sqlite.org/docs.html
- SQL Syntax: https://www.sqlite.org/lang.html
- Data Types: https://www.sqlite.org/datatype3.html

## Quick Reference

| Task | Command |
|------|---------|
| Open database | `sqlite3 career_guidance.db` |
| List tables | `.tables` |
| Show schema | `.schema` |
| Export to SQL | `.dump > backup.sql` |
| Import from SQL | `.read backup.sql` |
| Exit | `.quit` |

## Database Location Summary

```
career-guidance-ui/
└── backend/
    ├── career_guidance.db          ← Main SQLite database
    ├── db_init.py                  ← Database initialization script
    ├── community_models.py         ← Database models (tables)
    ├── user_model.py               ← User table model
    ├── progress_tracking_model.py  ← Progress tracking models
    └── uploads/                    ← File uploads (not in database)
        ├── videos/                 ← Video files
        └── community_images/       ← Image files
```
