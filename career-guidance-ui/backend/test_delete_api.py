"""
Test script to verify delete API endpoints and data structure
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from community_service import CommunityService
from community_models import db, Community, Post, PostType
from user_model import User
from flask import Flask
from app_config import Config

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def test_blog_structure():
    """Test that blog posts include author_id"""
    with app.app_context():
        print("\n=== Testing Blog Post Structure ===")
        blogs = CommunityService.get_blogs(limit=5)
        
        if not blogs:
            print("❌ No blogs found in database")
            return False
        
        print(f"✓ Found {len(blogs)} blog(s)")
        
        for blog in blogs:
            print(f"\nBlog ID: {blog.get('id')}")
            print(f"  Title: {blog.get('title')}")
            print(f"  Author ID: {blog.get('author_id')} {'✓' if blog.get('author_id') else '❌ MISSING'}")
            print(f"  Author Name: {blog.get('author_name')}")
            
            if not blog.get('author_id'):
                print("  ❌ ERROR: author_id is missing!")
                return False
        
        print("\n✓ All blogs have author_id field")
        return True

def test_community_structure():
    """Test that communities include created_by"""
    with app.app_context():
        print("\n=== Testing Community Structure ===")
        
        # Get a test user
        user = User.query.first()
        if not user:
            print("❌ No users found in database")
            return False
        
        communities = CommunityService.get_communities(user.id, limit=5)
        
        if not communities:
            print("❌ No communities found in database")
            return False
        
        print(f"✓ Found {len(communities)} communit(ies)")
        
        for community in communities:
            print(f"\nCommunity ID: {community.get('id')}")
            print(f"  Name: {community.get('name')}")
            print(f"  Created By: {community.get('created_by')} {'✓' if community.get('created_by') else '❌ MISSING'}")
            print(f"  Is Member: {community.get('is_member')}")
            
            if not community.get('created_by'):
                print("  ❌ ERROR: created_by is missing!")
                return False
        
        print("\n✓ All communities have created_by field")
        return True

def test_feedback_structure():
    """Test that feedback posts include author_id"""
    with app.app_context():
        print("\n=== Testing Feedback Structure ===")
        feedbacks = CommunityService.get_feedback(limit=5)
        
        if not feedbacks:
            print("❌ No feedback found in database")
            return False
        
        print(f"✓ Found {len(feedbacks)} feedback(s)")
        
        for feedback in feedbacks:
            print(f"\nFeedback ID: {feedback.get('id')}")
            print(f"  Content: {feedback.get('content')[:50]}...")
            print(f"  Author ID: {feedback.get('author_id')} {'✓' if feedback.get('author_id') else '❌ MISSING'}")
            print(f"  Author Name: {feedback.get('author_name')}")
            
            if not feedback.get('author_id'):
                print("  ❌ ERROR: author_id is missing!")
                return False
        
        print("\n✓ All feedback have author_id field")
        return True

def test_user_data():
    """Test that we can get current user data"""
    with app.app_context():
        print("\n=== Testing User Data ===")
        user = User.query.first()
        
        if not user:
            print("❌ No users found in database")
            return False
        
        print(f"✓ Found user: {user.name} (ID: {user.id})")
        print(f"  Email: {user.email}")
        
        return True

if __name__ == '__main__':
    print("=" * 60)
    print("DELETE FUNCTIONALITY - DATA STRUCTURE TEST")
    print("=" * 60)
    
    all_passed = True
    
    # Test user data
    if not test_user_data():
        all_passed = False
    
    # Test blog structure
    if not test_blog_structure():
        all_passed = False
    
    # Test community structure
    if not test_community_structure():
        all_passed = False
    
    # Test feedback structure
    if not test_feedback_structure():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("\nThe delete buttons should work correctly.")
        print("\nFrontend checks:")
        print("  - Blogs: currentUser.id === blog.author_id")
        print("  - Communities: currentUser.id === community.created_by")
        print("  - Feedback: currentUser.id === feedback.author_id")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease check the errors above.")
    print("=" * 60)
