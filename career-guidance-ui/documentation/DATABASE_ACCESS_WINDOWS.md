# SQLite Database Access - Windows Guide

## Database Location
```
career-guidance-ui\backend\career_guidance.db
```

## ⚠️ SQLite3 Not Installed on Windows

The `sqlite3` command is not available by default on Windows. Here are your options:

---

## Option 1: Use Python Script (EASIEST - RECOMMENDED)

I've created a Python script for you to view and query the database.

### Steps:
```powershell
# Navigate to backend folder
cd career-guidance-ui\backend

# Run the database viewer
python view_database.py
```

### Features:
- ✅ View all tables
- ✅ View users
- ✅ View communities
- ✅ View blogs
- ✅ View feedback
- ✅ View deleted content
- ✅ Run custom SQL queries

### Menu Options:
```
1. List all tables
2. View users
3. View communities
4. View blogs
5. View feedback
6. View deleted content
7. Custom SQL query
8. Exit
```

---

## Option 2: Download DB Browser for SQLite (GUI - BEST FOR BEGINNERS)

### Steps:
1. **Download**: https://sqlitebrowser.org/dl/
2. **Install**: Run the installer (DB.Browser.for.SQLite-3.x.x-win64.msi)
3. **Open Database**:
   - Launch DB Browser for SQLite
   - Click "Open Database"
   - Navigate to: `career-guidance-ui\backend\career_guidance.db`
   - Click "Open"

### Features:
- ✅ Visual table browser
- ✅ Execute SQL queries
- ✅ Edit data directly
- ✅ Export data
- ✅ View table structure
- ✅ Create backups

---

## Option 3: Install SQLite3 Command Line Tool

### Download SQLite3:
1. Go to: https://www.sqlite.org/download.html
2. Download: **sqlite-tools-win32-x86-xxxxxxx.zip**
3. Extract the ZIP file
4. Copy `sqlite3.exe` to a folder in your PATH (e.g., `C:\Windows\System32`)

### Or Add to PATH:
1. Extract ZIP to a folder (e.g., `C:\sqlite`)
2. Add folder to PATH:
   - Right-click "This PC" → Properties
   - Advanced system settings → Environment Variables
   - Edit "Path" variable
   - Add: `C:\sqlite`
   - Click OK

### Then Use:
```powershell
cd career-guidance-ui\backend
sqlite3 career_guidance.db
```

---

## Option 4: Use Python Directly

Create a quick Python script:

```python
# quick_query.py
import sqlite3

conn = sqlite3.connect('career_guidance.db')
cursor = conn.cursor()

# View all users
cursor.execute("SELECT id, name, email FROM users")
for row in cursor.fetchall():
    print(row)

conn.close()
```

Run it:
```powershell
cd career-guidance-ui\backend
python quick_query.py
```

---

## Option 5: Use VS Code Extension

### Steps:
1. Open VS Code
2. Install "SQLite" extension (by alexcvzz)
3. Open Command Palette (Ctrl+Shift+P)
4. Type: "SQLite: Open Database"
5. Select: `career_guidance.db`
6. View tables in "SQLITE EXPLORER" panel

---

## Common Queries (Use with Python Script or DB Browser)

### View All Users
```sql
SELECT id, name, email, domain, created_at FROM users;
```

### View All Communities
```sql
SELECT id, name, description, members_count, created_at 
FROM communities 
WHERE is_deleted = 0;
```

### View All Blogs
```sql
SELECT id, title, author_id, created_at 
FROM posts 
WHERE post_type = 'BLOG' AND is_deleted = 0;
```

### View Deleted Content
```sql
-- Deleted blogs
SELECT id, title, deleted_at 
FROM posts 
WHERE post_type = 'BLOG' AND is_deleted = 1;

-- Deleted communities
SELECT id, name, deleted_at 
FROM communities 
WHERE is_deleted = 1;
```

### Restore Deleted Content
```sql
-- Restore a blog (replace 1 with actual ID)
UPDATE posts 
SET is_deleted = 0, deleted_at = NULL 
WHERE id = 1 AND post_type = 'BLOG';

-- Restore a community
UPDATE communities 
SET is_deleted = 0, deleted_at = NULL 
WHERE id = 1;
```

---

## Quick Start (Recommended)

**For viewing data:**
```powershell
cd career-guidance-ui\backend
python view_database.py
```

**For GUI access:**
- Download DB Browser for SQLite
- Open `career_guidance.db`

---

## Backup Database

### Using PowerShell:
```powershell
cd career-guidance-ui\backend

# Create backup with timestamp
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item career_guidance.db "career_guidance_backup_$timestamp.db"
```

### Using Python:
```python
# backup_db.py
import shutil
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy('career_guidance.db', f'career_guidance_backup_{timestamp}.db')
print(f"Backup created: career_guidance_backup_{timestamp}.db")
```

---

## Troubleshooting

### "Database is locked" Error
1. Stop the Flask server
2. Close any database tools
3. Try again

### "Permission denied" Error
1. Close any programs using the database
2. Run as Administrator if needed

### Can't find database file
Make sure you're in the correct directory:
```powershell
cd C:\Users\amash\Desktop\PROJECT_3\Intelligent_Career_Guidance_Project\career-guidance-ui\backend
dir career_guidance.db
```

---

## Summary

| Method | Difficulty | Best For |
|--------|-----------|----------|
| Python Script | Easy | Quick viewing |
| DB Browser | Easy | Visual browsing |
| SQLite3 CLI | Medium | Advanced users |
| Python Direct | Easy | Custom scripts |
| VS Code Extension | Easy | Developers |

**Recommended for you:** Use the Python script (`python view_database.py`) or download DB Browser for SQLite.
