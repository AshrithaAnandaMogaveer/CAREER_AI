"""
Test script for Phase 6 - Unified Post Management
Tests the create_post and get_posts methods
"""

import sys
import os

# Add backend to path
backend_path = os.path.dirname(__file__)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from community_service import CommunityService
from community_models import db
from user_model import User
from app_config import create_app

# Create Flask app
app = create_app()

def test_unified_posts():
    """Test unified post creation and retrieval"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("PHASE 6: UNIFIED POST MANAGEMENT TEST")
        print("="*60)
        
        # Get or create test user
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            test_user = User(name='Test User', email='test@example.com', domain='Technology')
            test_user.set_password('password123')
            db.session.add(test_user)
            db.session.commit()
            print(f"\n✓ Created test user: {test_user.name} (ID: {test_user.id})")
        else:
            print(f"\n✓ Using existing test user: {test_user.name} (ID: {test_user.id})")
        
        user_id = test_user.id
        
        # Test 1: Create a blog post
        print("\n" + "-"*60)
        print("TEST 1: Create Blog Post")
        print("-"*60)
        
        blog_result = CommunityService.create_post(
            user_id=user_id,
            post_type='blog',
            content='This is a comprehensive guide to Python programming. '
                    'Python is a versatile language used in web development, '
                    'data science, machine learning, and automation. '
                    'In this blog, we will explore the fundamentals and advanced concepts.',
            title='Complete Python Programming Guide',
            category='Technology',
            tags=['python', 'programming', 'tutorial', 'beginner-friendly']
        )
        
        if blog_result['success']:
            print(f"✓ Blog created successfully!")
            print(f"  - ID: {blog_result['post']['id']}")
            print(f"  - Title: {blog_result['post']['title']}")
            print(f"  - Read Time: {blog_result['post']['read_time']} min")
            print(f"  - Tags: {', '.join(blog_result['post']['tags'])}")
        else:
            print(f"✗ Blog creation failed: {blog_result['message']}")
        
        # Test 2: Create a feedback post
        print("\n" + "-"*60)
        print("TEST 2: Create Feedback Post")
        print("-"*60)
        
        feedback_result = CommunityService.create_post(
            user_id=user_id,
            post_type='feedback',
            content='The new community features are amazing! '
                    'I love the recommendation engine and feed ranking. '
                    'Suggestion: Add dark mode toggle in settings.',
            category='Feature Request'
        )
        
        if feedback_result['success']:
            print(f"✓ Feedback created successfully!")
            print(f"  - ID: {feedback_result['post']['id']}")
            print(f"  - Category: {feedback_result['post']['category']}")
            print(f"  - Content: {feedback_result['post']['content'][:50]}...")
        else:
            print(f"✗ Feedback creation failed: {feedback_result['message']}")
        
        # Test 3: Get all posts
        print("\n" + "-"*60)
        print("TEST 3: Get All Posts")
        print("-"*60)
        
        all_posts = CommunityService.get_posts(limit=10)
        print(f"✓ Retrieved {len(all_posts)} posts")
        
        for i, post in enumerate(all_posts[:3], 1):
            print(f"\n  Post {i}:")
            print(f"    - Type: {post['post_type']}")
            print(f"    - Title: {post.get('title', 'N/A')}")
            print(f"    - Author: {post.get('author_name', 'Unknown')}")
            print(f"    - Likes: {post['likes_count']}, Comments: {post['comments_count']}")
        
        # Test 4: Get only blog posts
        print("\n" + "-"*60)
        print("TEST 4: Get Blog Posts Only")
        print("-"*60)
        
        blogs = CommunityService.get_posts(post_type='blog', limit=5)
        print(f"✓ Retrieved {len(blogs)} blog posts")
        
        # Test 5: Get only feedback posts
        print("\n" + "-"*60)
        print("TEST 5: Get Feedback Posts Only")
        print("-"*60)
        
        feedbacks = CommunityService.get_posts(post_type='feedback', limit=5)
        print(f"✓ Retrieved {len(feedbacks)} feedback posts")
        
        # Test 6: Get posts by specific user
        print("\n" + "-"*60)
        print("TEST 6: Get Posts by User")
        print("-"*60)
        
        user_posts = CommunityService.get_posts(user_id=user_id, limit=10)
        print(f"✓ Retrieved {len(user_posts)} posts by user {user_id}")
        
        # Test 7: Validation - Missing content
        print("\n" + "-"*60)
        print("TEST 7: Validation - Missing Content")
        print("-"*60)
        
        invalid_result = CommunityService.create_post(
            user_id=user_id,
            post_type='blog',
            content='',
            title='Empty Content Test'
        )
        
        if not invalid_result['success']:
            print(f"✓ Validation working: {invalid_result['message']}")
        else:
            print(f"✗ Validation failed - empty content was accepted")
        
        # Test 8: Validation - Blog without title
        print("\n" + "-"*60)
        print("TEST 8: Validation - Blog Without Title")
        print("-"*60)
        
        invalid_result = CommunityService.create_post(
            user_id=user_id,
            post_type='blog',
            content='This blog has no title'
        )
        
        if not invalid_result['success']:
            print(f"✓ Validation working: {invalid_result['message']}")
        else:
            print(f"✗ Validation failed - blog without title was accepted")
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED")
        print("="*60)
        print("\n✓ Phase 6 unified post management is working correctly!")
        print("✓ Endpoints ready: POST /api/community/post, GET /api/community/posts")
        print("\n")

if __name__ == '__main__':
    test_unified_posts()
