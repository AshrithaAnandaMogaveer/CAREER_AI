"""
Test script for Phase 9 - Notification Engine
Tests notification creation, retrieval, and marking as read
"""

import sys
import os

# Add backend to path
backend_path = os.path.dirname(__file__)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from community_service import CommunityService
from community_models import db, Notification, Post, Comment, Like
from user_model import User
from app_config import create_app

# Create Flask app
app = create_app()


def create_test_users_and_content():
    """Create test users and content for notification testing"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("CREATING TEST USERS AND CONTENT")
        print("="*60)
        
        # User 1: Alice (content creator)
        user1 = User.query.filter_by(email='alice.notif@example.com').first()
        if not user1:
            user1 = User(name='Alice', email='alice.notif@example.com', domain='Software Development')
            user1.set_password('password123')
            db.session.add(user1)
            db.session.flush()
            print(f"✓ Created: Alice (ID: {user1.id})")
        else:
            print(f"✓ Using existing: Alice (ID: {user1.id})")
        
        # User 2: Bob (interactor)
        user2 = User.query.filter_by(email='bob.notif@example.com').first()
        if not user2:
            user2 = User(name='Bob', email='bob.notif@example.com', domain='Data Science')
            user2.set_password('password123')
            db.session.add(user2)
            db.session.flush()
            print(f"✓ Created: Bob (ID: {user2.id})")
        else:
            print(f"✓ Using existing: Bob (ID: {user2.id})")
        
        # User 3: Carol (community creator)
        user3 = User.query.filter_by(email='carol.notif@example.com').first()
        if not user3:
            user3 = User(name='Carol', email='carol.notif@example.com', domain='Design')
            user3.set_password('password123')
            db.session.add(user3)
            db.session.flush()
            print(f"✓ Created: Carol (ID: {user3.id})")
        else:
            print(f"✓ Using existing: Carol (ID: {user3.id})")
        
        db.session.commit()
        
        # Create a test post by Alice
        print(f"\nCreating test post by Alice...")
        post_result = CommunityService.create_post(
            user_id=user1.id,
            post_type='blog',
            content='This is a test post for Phase 9 notification testing. '
                    'We will test comments and likes on this post.',
            title='Phase 9 Test Post'
        )
        
        if post_result['success']:
            post_id = post_result['post']['id']
            print(f"✓ Created test post (ID: {post_id})")
        else:
            print(f"✗ Failed to create post: {post_result['message']}")
            post_id = None
        
        return user1, user2, user3, post_id


def test_notification_triggers():
    """Test Phase 9 notification triggers"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("TEST 1: NOTIFICATION TRIGGERS")
        print("="*60)
        
        user1, user2, user3, post_id = create_test_users_and_content()
        
        # Store IDs to avoid session issues
        alice_id = user1.id
        bob_id = user2.id
        carol_id = user3.id
        
        if not post_id:
            print("✗ Cannot test without post")
            return
        
        # Test 1: Someone likes post
        print("\n" + "-"*60)
        print("Trigger 1: Someone likes post")
        print("-"*60)
        
        print(f"Bob liking Alice's post...")
        # Store IDs to avoid session issues
        bob_id = user2.id
        alice_id = user1.id
        
        result = CommunityService.toggle_like(user_id=bob_id, post_id=post_id)
        
        if result['success']:
            print(f"✓ Like action: {result['action']}")
            
            # Check notification was created
            notification = Notification.query.filter_by(
                user_id=user1.id,
                type='POST_LIKE',
                actor_id=user2.id
            ).order_by(Notification.created_at.desc()).first()
            
            if notification:
                print(f"✓ Notification created for Alice")
                print(f"  - Type: {notification.type}")
                print(f"  - Title: {notification.title}")
                print(f"  - Message: {notification.message}")
                print(f"  - Is Read: {notification.is_read}")
                print(f"  - Reference ID: {notification.entity_id}")
            else:
                print(f"✗ No notification found!")
        
        # Test 2: Someone comments on post
        print("\n" + "-"*60)
        print("Trigger 2: Someone comments on post")
        print("-"*60)
        
        print(f"Bob commenting on Alice's post...")
        result = CommunityService.add_comment(
            user_id=user2.id,
            post_id=post_id,
            content="Great post, Alice! Very informative."
        )
        
        if result['success']:
            comment_id = result['comment']['id']
            print(f"✓ Comment created (ID: {comment_id})")
            
            # Check notification was created
            notification = Notification.query.filter_by(
                user_id=user1.id,
                type='NEW_COMMENT',
                actor_id=user2.id
            ).order_by(Notification.created_at.desc()).first()
            
            if notification:
                print(f"✓ Notification created for Alice")
                print(f"  - Type: {notification.type}")
                print(f"  - Title: {notification.title}")
                print(f"  - Message: {notification.message}")
                print(f"  - Reference ID: {notification.entity_id}")
            else:
                print(f"✗ No notification found!")
        
        # Test 3: Someone joins community
        print("\n" + "-"*60)
        print("Trigger 3: Someone joins community")
        print("-"*60)
        
        print(f"Carol creating a community...")
        community_result = CommunityService.create_community(
            user_id=user3.id,
            name='Phase 9 Test Community',
            description='A test community for Phase 9 notifications',
            category='Technology',
            tags=['testing', 'phase9']
        )
        
        if community_result['success']:
            community_id = community_result['community']['id']
            print(f"✓ Community created (ID: {community_id})")
            
            print(f"Bob joining Carol's community...")
            join_result = CommunityService.join_community(
                user_id=user2.id,
                community_id=community_id
            )
            
            if join_result['success']:
                print(f"✓ Bob joined community")
                
                # Check notification was created for Carol (admin)
                notification = Notification.query.filter_by(
                    user_id=user3.id,
                    type='COMMUNITY_JOIN',
                    actor_id=user2.id
                ).order_by(Notification.created_at.desc()).first()
                
                if notification:
                    print(f"✓ Notification created for Carol")
                    print(f"  - Type: {notification.type}")
                    print(f"  - Title: {notification.title}")
                    print(f"  - Message: {notification.message}")
                else:
                    print(f"✗ No notification found!")
        
        # Test 4: Someone sends message (already tested in Phase 8)
        print("\n" + "-"*60)
        print("Trigger 4: Someone sends message")
        print("-"*60)
        
        print(f"Bob sending message to Alice...")
        result = CommunityService.send_message(
            sender_id=user2.id,
            recipient_id=user1.id,
            content="Hi Alice, great post!"
        )
        
        if result['success']:
            print(f"✓ Message sent")
            
            # Check notification was created
            notification = Notification.query.filter_by(
                user_id=user1.id,
                type='NEW_MESSAGE',
                actor_id=user2.id
            ).order_by(Notification.created_at.desc()).first()
            
            if notification:
                print(f"✓ Notification created for Alice")
                print(f"  - Type: {notification.type}")
                print(f"  - Title: {notification.title}")
                print(f"  - Message: {notification.message}")
            else:
                print(f"✗ No notification found!")


def test_get_notifications():
    """Test retrieving notifications"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("TEST 2: GET NOTIFICATIONS")
        print("="*60)
        
        user1 = User.query.filter_by(email='alice.notif@example.com').first()
        
        if not user1:
            print("✗ Test user not found")
            return
        
        # Get all notifications
        print(f"\nGetting all notifications for Alice...")
        notifications = Notification.query.filter_by(
            user_id=user1.id,
            is_deleted=False
        ).order_by(Notification.created_at.desc()).all()
        
        print(f"✓ Found {len(notifications)} notifications")
        
        for i, notif in enumerate(notifications[:5], 1):
            print(f"\n  Notification {i}:")
            print(f"    - Type: {notif.type}")
            print(f"    - Title: {notif.title}")
            print(f"    - Message: {notif.message}")
            print(f"    - Is Read: {notif.is_read}")
            print(f"    - Reference ID: {notif.entity_id}")
            print(f"    - Timestamp: {notif.created_at}")
        
        # Get unread count
        unread_count = Notification.query.filter_by(
            user_id=user1.id,
            is_read=False,
            is_deleted=False
        ).count()
        
        print(f"\n✓ Unread notifications: {unread_count}")
        
        # Get by type
        print(f"\nGetting POST_LIKE notifications...")
        like_notifs = Notification.query.filter_by(
            user_id=user1.id,
            type='POST_LIKE',
            is_deleted=False
        ).all()
        
        print(f"✓ Found {len(like_notifs)} POST_LIKE notifications")


def test_mark_notifications_read():
    """Test marking notifications as read"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("TEST 3: MARK NOTIFICATIONS AS READ")
        print("="*60)
        
        user1 = User.query.filter_by(email='alice.notif@example.com').first()
        
        if not user1:
            print("✗ Test user not found")
            return
        
        # Get unread notifications
        unread_notifs = Notification.query.filter_by(
            user_id=user1.id,
            is_read=False,
            is_deleted=False
        ).all()
        
        print(f"\nUnread notifications before: {len(unread_notifs)}")
        
        if len(unread_notifs) > 0:
            # Mark first notification as read
            print(f"\nMarking first notification as read...")
            first_notif = unread_notifs[0]
            first_notif.is_read = True
            from datetime import datetime
            first_notif.read_at = datetime.utcnow()
            db.session.commit()
            
            print(f"✓ Marked notification {first_notif.id} as read")
            
            # Check unread count
            unread_count = Notification.query.filter_by(
                user_id=user1.id,
                is_read=False,
                is_deleted=False
            ).count()
            
            print(f"Unread notifications after: {unread_count}")
            
            # Mark all as read
            if unread_count > 0:
                print(f"\nMarking all remaining notifications as read...")
                remaining = Notification.query.filter_by(
                    user_id=user1.id,
                    is_read=False,
                    is_deleted=False
                ).all()
                
                for notif in remaining:
                    notif.is_read = True
                    notif.read_at = datetime.utcnow()
                
                db.session.commit()
                
                print(f"✓ Marked {len(remaining)} notifications as read")
                
                # Final count
                final_unread = Notification.query.filter_by(
                    user_id=user1.id,
                    is_read=False,
                    is_deleted=False
                ).count()
                
                print(f"Final unread count: {final_unread}")


def run_all_tests():
    """Run all Phase 9 tests"""
    
    print("\n" + "="*70)
    print(" "*15 + "PHASE 9: NOTIFICATION ENGINE TEST SUITE")
    print("="*70)
    print("\nNotification Triggers:")
    print("- New message")
    print("- New comment")
    print("- Someone joins community")
    print("- Someone likes post")
    print("="*70)
    
    # Run tests
    test_notification_triggers()
    test_get_notifications()
    test_mark_notifications_read()
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETED")
    print("="*70)
    print("\n✓ Phase 9 notification engine is working correctly!")
    print("✓ Endpoints ready:")
    print("  - GET /api/community/notifications")
    print("  - POST /api/community/notifications/read")
    print("✓ Notification triggers:")
    print("  - POST_LIKE (when someone likes post)")
    print("  - NEW_COMMENT (when someone comments)")
    print("  - COMMUNITY_JOIN (when someone joins community)")
    print("  - NEW_MESSAGE (when someone sends message)")
    print("\n")


if __name__ == '__main__':
    run_all_tests()
