"""
Test script for community join and create functionality
Tests authentication, role management, and notifications
"""

import sys
import os

# Add backend to path
backend_path = os.path.dirname(os.path.abspath(__file__))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app_config import create_app
from community_models import db, Community, CommunityMember, Notification, CommunityRole
from user_model import User
from community_service import CommunityService


def test_create_community():
    """Test community creation"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("TEST 1: CREATE COMMUNITY")
        print("="*60)
        
        # Get test user
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            print("❌ Test user not found")
            return
        
        print(f"\nUser: {test_user.name} (ID: {test_user.id})")
        
        # Test 1: Create valid community
        print("\n--- Test 1a: Create Valid Community ---")
        result = CommunityService.create_community(
            user_id=test_user.id,
            name='Test Community Phase 5',
            description='A test community for Phase 5 validation',
            category='Testing',
            tags=['test', 'phase5', 'validation']
        )
        
        if result['success']:
            print(f"✓ Community created: {result['community']['name']}")
            print(f"  ID: {result['community']['id']}")
            print(f"  Members: {result['community']['members_count']}")
            community_id = result['community']['id']
            
            # Verify creator is ADMIN
            member = CommunityMember.query.filter_by(
                community_id=community_id,
                user_id=test_user.id
            ).first()
            
            if member and member.role == CommunityRole.ADMIN:
                print(f"✓ Creator is ADMIN")
            else:
                print(f"❌ Creator is not ADMIN")
        else:
            print(f"❌ Failed: {result['message']}")
        
        # Test 2: Try to create duplicate
        print("\n--- Test 1b: Prevent Duplicate Name ---")
        result = CommunityService.create_community(
            user_id=test_user.id,
            name='Test Community Phase 5',
            description='Duplicate test',
            category='Testing'
        )
        
        if not result['success']:
            print(f"✓ Duplicate prevented: {result['message']}")
        else:
            print(f"❌ Duplicate was allowed (should fail)")
        
        # Test 3: Missing required fields
        print("\n--- Test 1c: Validate Required Fields ---")
        result = CommunityService.create_community(
            user_id=test_user.id,
            name='',
            description='',
            category='Testing'
        )
        
        if not result['success']:
            print(f"✓ Validation works: {result['message']}")
        else:
            print(f"❌ Validation failed (should reject empty fields)")


def test_join_community():
    """Test community joining"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("TEST 2: JOIN COMMUNITY")
        print("="*60)
        
        # Get test user
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            print("❌ Test user not found")
            return
        
        # Create a second test user if doesn't exist
        test_user2 = User.query.filter_by(email='test2@example.com').first()
        if not test_user2:
            test_user2 = User(
                name='Test User 2',
                email='test2@example.com',
                domain='Testing'
            )
            test_user2.set_password('test123')
            db.session.add(test_user2)
            db.session.commit()
            print(f"✓ Created second test user: {test_user2.name}")
        
        # Find a community to join
        community = Community.query.filter_by(
            name='Test Community Phase 5',
            is_deleted=False
        ).first()
        
        if not community:
            print("❌ Test community not found. Run create test first.")
            return
        
        print(f"\nCommunity: {community.name} (ID: {community.id})")
        print(f"Current members: {community.members_count}")
        
        # Test 1: Join community
        print("\n--- Test 2a: Join Community ---")
        result = CommunityService.join_community(
            user_id=test_user2.id,
            community_id=community.id
        )
        
        if result['success']:
            print(f"✓ Joined successfully: {result['message']}")
            
            # Verify membership
            member = CommunityMember.query.filter_by(
                community_id=community.id,
                user_id=test_user2.id,
                is_deleted=False
            ).first()
            
            if member:
                print(f"✓ Membership confirmed")
                print(f"  Role: {member.role.value}")
                
                if member.role == CommunityRole.MEMBER:
                    print(f"✓ Role is MEMBER (correct)")
                else:
                    print(f"❌ Role is {member.role.value} (should be MEMBER)")
            
            # Check member count updated
            db.session.refresh(community)
            print(f"✓ Member count updated: {community.members_count}")
        else:
            print(f"❌ Failed: {result['message']}")
        
        # Test 2: Prevent duplicate join
        print("\n--- Test 2b: Prevent Duplicate Join ---")
        result = CommunityService.join_community(
            user_id=test_user2.id,
            community_id=community.id
        )
        
        if not result['success']:
            print(f"✓ Duplicate prevented: {result['message']}")
        else:
            print(f"❌ Duplicate was allowed (should fail)")
        
        # Test 3: Check notifications
        print("\n--- Test 2c: Verify Notifications ---")
        notifications = Notification.query.filter_by(
            user_id=test_user.id,  # Admin user
            type='COMMUNITY_JOIN',
            entity_id=community.id,
            is_deleted=False
        ).all()
        
        if notifications:
            print(f"✓ Notification created for admin")
            for notif in notifications:
                print(f"  - {notif.title}: {notif.message}")
                print(f"    Read: {notif.is_read}")
        else:
            print(f"⚠ No notifications found (may be expected if user joined own community)")


def test_notifications():
    """Test notification system"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("TEST 3: NOTIFICATIONS")
        print("="*60)
        
        # Get test user
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            print("❌ Test user not found")
            return
        
        # Get all notifications
        notifications = Notification.query.filter_by(
            user_id=test_user.id,
            is_deleted=False
        ).order_by(Notification.created_at.desc()).all()
        
        print(f"\nTotal notifications: {len(notifications)}")
        
        # Count unread
        unread = [n for n in notifications if not n.is_read]
        print(f"Unread notifications: {len(unread)}")
        
        if notifications:
            print("\nRecent notifications:")
            for i, notif in enumerate(notifications[:5], 1):
                print(f"\n{i}. {notif.title}")
                print(f"   Type: {notif.type}")
                print(f"   Message: {notif.message}")
                print(f"   Read: {notif.is_read}")
                print(f"   Created: {notif.created_at}")
        else:
            print("\nNo notifications found")


def cleanup():
    """Clean up test data"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("CLEANUP")
        print("="*60)
        
        response = input("\nDelete test community and user? (yes/no): ")
        
        if response.lower() == 'yes':
            # Delete test community
            community = Community.query.filter_by(name='Test Community Phase 5').first()
            if community:
                community.is_deleted = True
                print(f"✓ Deleted community: {community.name}")
            
            # Delete test user 2
            user2 = User.query.filter_by(email='test2@example.com').first()
            if user2:
                user2.is_deleted = True
                print(f"✓ Deleted user: {user2.name}")
            
            db.session.commit()
            print("\n✓ Cleanup complete")
        else:
            print("\nCleanup cancelled")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Test community join and create')
    parser.add_argument('--create', action='store_true', help='Test community creation')
    parser.add_argument('--join', action='store_true', help='Test community joining')
    parser.add_argument('--notifications', action='store_true', help='Test notifications')
    parser.add_argument('--cleanup', action='store_true', help='Clean up test data')
    
    args = parser.parse_args()
    
    if args.create:
        test_create_community()
    
    if args.join:
        test_join_community()
    
    if args.notifications:
        test_notifications()
    
    if args.cleanup:
        cleanup()
    
    if not any([args.create, args.join, args.notifications, args.cleanup]):
        # Run all tests by default
        test_create_community()
        test_join_community()
        test_notifications()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETE")
        print("="*60)
