"""
Database Migration: Add video_url column to posts table
Run this script to update existing database
"""
import sys
sys.path.insert(0, '..')

from flask_cors_config import app, db
from sqlalchemy import text

print("=" * 60)
print("DATABASE MIGRATION: Add video_url to posts table")
print("=" * 60)

with app.app_context():
    try:
        # Check if column already exists
        result = db.session.execute(text("PRAGMA table_info(posts)"))
        columns = [row[1] for row in result.fetchall()]
        
        if 'video_url' in columns:
            print("✅ Column 'video_url' already exists in posts table")
        else:
            print("\n📝 Adding 'video_url' column to posts table...")
            db.session.execute(text(
                "ALTER TABLE posts ADD COLUMN video_url VARCHAR(1000)"
            ))
            db.session.commit()
            print("✅ Successfully added 'video_url' column")
        
        # Verify the change
        result = db.session.execute(text("PRAGMA table_info(posts)"))
        columns = [row[1] for row in result.fetchall()]
        
        print(f"\n📊 Posts table now has {len(columns)} columns:")
        for col in columns:
            print(f"   - {col}")
        
        print("\n" + "=" * 60)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Add video URLs when creating blogs")
        print("2. Videos will be displayed in blog posts")
        print("3. Supports YouTube, Vimeo, and direct video URLs")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        db.session.rollback()
        sys.exit(1)
