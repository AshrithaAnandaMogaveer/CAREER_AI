"""
Simple SQLite Database Viewer
Run this script to view and query the database
"""

import sqlite3
import sys
from datetime import datetime

DB_FILE = 'career_guidance.db'

def connect_db():
    """Connect to the database"""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def list_tables(conn):
    """List all tables in the database"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print("\n" + "="*60)
    print("DATABASE TABLES")
    print("="*60)
    for i, table in enumerate(tables, 1):
        print(f"{i}. {table[0]}")
    print("="*60 + "\n")

def view_users(conn):
    """View all users"""
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, domain, created_at FROM users LIMIT 20")
    users = cursor.fetchall()
    
    print("\n" + "="*80)
    print("USERS")
    print("="*80)
    print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Domain':<15}")
    print("-"*80)
    
    for user in users:
        print(f"{user['id']:<5} {user['name']:<20} {user['email']:<30} {user['domain'] or 'N/A':<15}")
    
    print(f"\nTotal users shown: {len(users)}")
    print("="*80 + "\n")

def view_communities(conn):
    """View all communities"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, description, created_by, members_count, is_deleted, created_at 
        FROM communities 
        ORDER BY created_at DESC 
        LIMIT 20
    """)
    communities = cursor.fetchall()
    
    print("\n" + "="*100)
    print("COMMUNITIES")
    print("="*100)
    print(f"{'ID':<5} {'Name':<25} {'Creator ID':<12} {'Members':<10} {'Deleted':<10} {'Created':<20}")
    print("-"*100)
    
    for comm in communities:
        deleted = "Yes" if comm['is_deleted'] else "No"
        created = comm['created_at'][:19] if comm['created_at'] else 'N/A'
        print(f"{comm['id']:<5} {comm['name'][:24]:<25} {comm['created_by']:<12} {comm['members_count']:<10} {deleted:<10} {created:<20}")
    
    print(f"\nTotal communities shown: {len(communities)}")
    print("="*100 + "\n")

def view_blogs(conn):
    """View all blog posts"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, author_id, is_deleted, created_at 
        FROM posts 
        WHERE post_type = 'BLOG'
        ORDER BY created_at DESC 
        LIMIT 20
    """)
    blogs = cursor.fetchall()
    
    print("\n" + "="*90)
    print("BLOG POSTS")
    print("="*90)
    print(f"{'ID':<5} {'Title':<40} {'Author ID':<12} {'Deleted':<10} {'Created':<20}")
    print("-"*90)
    
    for blog in blogs:
        deleted = "Yes" if blog['is_deleted'] else "No"
        created = blog['created_at'][:19] if blog['created_at'] else 'N/A'
        title = blog['title'][:39] if blog['title'] else 'Untitled'
        print(f"{blog['id']:<5} {title:<40} {blog['author_id']:<12} {deleted:<10} {created:<20}")
    
    print(f"\nTotal blogs shown: {len(blogs)}")
    print("="*90 + "\n")

def view_feedback(conn):
    """View all feedback posts"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, content, category, author_id, is_deleted, created_at 
        FROM posts 
        WHERE post_type = 'FEEDBACK'
        ORDER BY created_at DESC 
        LIMIT 20
    """)
    feedbacks = cursor.fetchall()
    
    print("\n" + "="*100)
    print("FEEDBACK POSTS")
    print("="*100)
    print(f"{'ID':<5} {'Content':<40} {'Category':<15} {'Author':<10} {'Deleted':<10} {'Created':<20}")
    print("-"*100)
    
    for fb in feedbacks:
        deleted = "Yes" if fb['is_deleted'] else "No"
        created = fb['created_at'][:19] if fb['created_at'] else 'N/A'
        content = fb['content'][:39] if fb['content'] else 'N/A'
        category = fb['category'] or 'N/A'
        print(f"{fb['id']:<5} {content:<40} {category:<15} {fb['author_id']:<10} {deleted:<10} {created:<20}")
    
    print(f"\nTotal feedback shown: {len(feedbacks)}")
    print("="*100 + "\n")

def view_deleted_content(conn):
    """View all deleted content"""
    cursor = conn.cursor()
    
    # Deleted communities
    cursor.execute("""
        SELECT id, name, created_by, deleted_at 
        FROM communities 
        WHERE is_deleted = 1
        ORDER BY deleted_at DESC
    """)
    deleted_communities = cursor.fetchall()
    
    # Deleted blogs
    cursor.execute("""
        SELECT id, title, author_id, deleted_at 
        FROM posts 
        WHERE post_type = 'BLOG' AND is_deleted = 1
        ORDER BY deleted_at DESC
    """)
    deleted_blogs = cursor.fetchall()
    
    # Deleted feedback
    cursor.execute("""
        SELECT id, content, author_id, deleted_at 
        FROM posts 
        WHERE post_type = 'FEEDBACK' AND is_deleted = 1
        ORDER BY deleted_at DESC
    """)
    deleted_feedback = cursor.fetchall()
    
    print("\n" + "="*80)
    print("DELETED CONTENT")
    print("="*80)
    
    print("\nDeleted Communities:")
    print("-"*80)
    if deleted_communities:
        for comm in deleted_communities:
            print(f"ID: {comm['id']}, Name: {comm['name']}, Deleted: {comm['deleted_at'][:19]}")
    else:
        print("No deleted communities")
    
    print("\nDeleted Blogs:")
    print("-"*80)
    if deleted_blogs:
        for blog in deleted_blogs:
            title = blog['title'][:50] if blog['title'] else 'Untitled'
            print(f"ID: {blog['id']}, Title: {title}, Deleted: {blog['deleted_at'][:19]}")
    else:
        print("No deleted blogs")
    
    print("\nDeleted Feedback:")
    print("-"*80)
    if deleted_feedback:
        for fb in deleted_feedback:
            content = fb['content'][:50] if fb['content'] else 'N/A'
            print(f"ID: {fb['id']}, Content: {content}, Deleted: {fb['deleted_at'][:19]}")
    else:
        print("No deleted feedback")
    
    print("="*80 + "\n")

def custom_query(conn):
    """Execute a custom SQL query"""
    print("\n" + "="*60)
    print("CUSTOM QUERY")
    print("="*60)
    print("Enter your SQL query (or 'back' to return):")
    query = input("> ")
    
    if query.lower() == 'back':
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            if results:
                # Print column names
                print("\nResults:")
                print("-"*60)
                if hasattr(results[0], 'keys'):
                    print(" | ".join(results[0].keys()))
                    print("-"*60)
                
                # Print rows
                for row in results:
                    print(" | ".join(str(val) for val in row))
                
                print(f"\nTotal rows: {len(results)}")
            else:
                print("No results found")
        else:
            conn.commit()
            print(f"Query executed successfully. Rows affected: {cursor.rowcount}")
    
    except Exception as e:
        print(f"Error executing query: {e}")
    
    print("="*60 + "\n")

def main_menu():
    """Display main menu"""
    print("\n" + "="*60)
    print("SQLite DATABASE VIEWER")
    print("Database: career_guidance.db")
    print("="*60)
    print("1. List all tables")
    print("2. View users")
    print("3. View communities")
    print("4. View blogs")
    print("5. View feedback")
    print("6. View deleted content")
    print("7. Custom SQL query")
    print("8. Exit")
    print("="*60)
    
    choice = input("\nEnter your choice (1-8): ")
    return choice

def main():
    """Main function"""
    conn = connect_db()
    
    print("\n" + "="*60)
    print("Connected to database successfully!")
    print("="*60)
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            list_tables(conn)
        elif choice == '2':
            view_users(conn)
        elif choice == '3':
            view_communities(conn)
        elif choice == '4':
            view_blogs(conn)
        elif choice == '5':
            view_feedback(conn)
        elif choice == '6':
            view_deleted_content(conn)
        elif choice == '7':
            custom_query(conn)
        elif choice == '8':
            print("\nClosing database connection...")
            conn.close()
            print("Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")
    
    sys.exit(0)

if __name__ == '__main__':
    main()
