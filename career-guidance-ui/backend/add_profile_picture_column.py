"""
Migration: Add profile_picture column to users table
Run once: python add_profile_picture_column.py
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'career_guidance.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if column already exists
cursor.execute("PRAGMA table_info(users)")
columns = [row[1] for row in cursor.fetchall()]

if 'profile_picture' not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN profile_picture VARCHAR(500)")
    conn.commit()
    print("✓ Added profile_picture column to users table")
else:
    print("✓ profile_picture column already exists, skipping")

conn.close()
