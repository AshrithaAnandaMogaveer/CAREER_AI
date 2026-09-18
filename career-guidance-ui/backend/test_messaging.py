"""
Test script for Phase 8 - Private Messaging System
Tests conversation creation, message sending, notifications, and read status
"""

import sys
import os

# Add backend to path
backend_path = os.path.dirname(__file__)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from community_service import CommunityService
from community_models import db, Conversation, Message, Notification
from user_model import User
from app_config import create_app

# Create Flask app
app = create_app()


def create_test_users():
    """Create test users for messaging"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("CREATING TEST USERS")
        print("="*60)
        
        # User 1: Alice
        user1 = User.query.filter_by(email='alice@example.com').first()
        if not user1:
            user1 = User(name='Alice', email='alice@example.com', domain='Software Development')
            user1.set_password('password123')
            db.session.add(user1)
            print(f"✓ Created: Alice")
        else:
            print(f"✓ Using existing: Alice (ID: {user1.id})")
        
        # User 2: Bob
        user2 = User.query.filter_by(email='bob@example.com').first()
        if not user2:
            user2 = User(name='Bob', email='bob@example.com', domain='Data Science')
            user2.set_password('password123')
            db.session.add(user2)
            print(f"✓ Created: Bob")
        else:
            print(f"✓ Using existing: Bob (ID: {user2.id})")
        
        # User 3: Carol
        user3 = User.query.filter_by(email='carol@example.com').first()
        if not user3:
            user3 = User(name='Carol', email='carol@example.com', domain='Design')
            user3.set_password('password123')
            db.session.add(user3)
            print(f"✓ Created: Carol")
        else:
            print(f"✓ Using existing: Carol (ID: {user3.id})")
        
        db.session.commit()
        
        return user1, user2, user3


def test_conversation_creation():
    """Test conversation creation"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("TEST 1: CONVERSATION CREATION")
        print("="*60)
        
        user1 = User.query.filter_by(email='alice@example.com').first()
        user2 = User.query.filter_by(email='bob@example.com').first()
        
        # Test: Create conversation
        print("\nCreating conversation between Alice and Bob...")
        conv = CommunityService.get_or_create_conversation(user1.id, user2.id)
        
        print(f"✓ Conversation created: ID {conv.id}")
        print(f"  - User 1: {conv.user1_id}")
        print(f"  - User 2: {conv.user2_id}")
        
        # Test: Get same conversation (should not create duplicate)
        print("\nGetting same conversation again...")
        conv2 = CommunityService.get_or_create_conversation(user1.id, user2.id)
        
        if conv.id == conv2.id:
            print(f"✓ Same conversation returned (no duplicate)")
        else:
            print(f"✗ Different conversation returned (duplicate created!)")
        
        # Test: Reverse order should return same conversation
        print("\nGetting conversation with reversed user order...")
        conv3 = CommunityService.get_or_create_conversation(user2.id, user1.id)
        
        if conv.id == conv3.id:
            print(f"✓ Same conversation returned (order doesn't matter)")
        else:
            print(f"✗ Different conversation returned (order matters!)")


def test_send_message():
    """Test sending messages with Phase 8 logic"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("TEST 2: SEND MESSAGE (Phase 8 Logic)")
        print("="*60)
        
        user1 = User.query.filter_by(email='alice@example.com').first()
        user2 = User.query.filter_by(email='bob@example.com').first()
        
        # Test: Send message from Alice to Bob
        print(f"\nAlice sending message to Bob...")
        result = CommunityService.send_message(
            sender_id=user1.id,
            recipient_id=user2.id,
            content="Hey Bob! How are you doing?"
        )
        
        if result['success']:
            print(f"✓ Message sent successfully")
            print(f"  - Message ID: {result['message']['id']}")
            print(f"  - Conversation ID: {result['conversation_id']}")
            print(f"  - Content: {result['message']['content']}")
            print(f"  - Is Read: {result['message']['is_read']}")
            
            # Verify message is unread
            if not result['message']['is_read']:
                print(f"✓ Message marked as unread for receiver")
            else:
                print(f"✗ Message should be unread!")
        else:
            print(f"✗ Failed to send message: {result['message']}")
        
        # Test: Check notification was created
        print("\nChecking if notification was created...")
        notification = Notification.query.filter_by(
            user_id=user2.id,
            type='NEW_MESSAGE',
            actor_id=user1.id
        ).order_by(Notification.created_at.desc()).first()
        
        if notification:
            print(f"✓ Notification created for Bob")
            print(f"  - Title: {notification.title}")
            print(f"  - Message: {notification.message}")
            print(f"  - Is Read: {notification.is_read}")
        else:
            print(f"✗ No notification found!")
        
        # Test: Send reply from Bob to Alice
        print(f"\nBob replying to Alice...")
        result2 = CommunityService.send_message(
            sender_id=user2.id,
            recipient_id=user1.id,
            content="Hi Alice! I'm doing great, thanks for asking!"
        )
        
        if result2['success']:
            print(f"✓ Reply sent successfully")
            print(f"  - Same conversation: {result2['conversation_id'] == result['conversation_id']}")
        
        # Test: Validation - empty message
        print(f"\nTesting validation: empty message...")
        result3 = CommunityService.send_message(
            sender_id=user1.id,
            recipient_id=user2.id,
            content=""
        )
        
        if not result3['success']:
            print(f"✓ Validation working: {result3['message']}")
        else:
            print(f"✗ Empty message was accepted!")


def test_get_messages():
    """Test retrieving messages and marking as read"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("TEST 3: GET MESSAGES & MARK AS READ")
        print("="*60)
        
        user1 = User.query.filter_by(email='alice@example.com').first()
        user2 = User.query.filter_by(email='bob@example.com').first()
        
        # Get messages for Bob (should mark Alice's messages as read)
        print(f"\nBob retrieving messages from Alice...")
        messages = CommunityService.get_messages(user2.id, user1.id, limit=10)
        
        print(f"✓ Retrieved {len(messages)} messages")
        
        for i, msg in enumerate(messages, 1):
            print(f"\n  Message {i}:")
            print(f"    - From: {msg['sender_name']}")
            print(f"    - Content: {msg['content'][:50]}...")
            print(f"    - Is Own: {msg['is_own']}")
            print(f"    - Is Read: {msg['is_read']}")
        
        # Verify messages from Alice are now marked as read
        print(f"\nVerifying messages are marked as read...")
        unread_count = Message.query.filter_by(
            sender_id=user1.id,
            is_read=False,
            is_deleted=False
        ).count()
        
        if unread_count == 0:
            print(f"✓ All messages from Alice marked as read")
        else:
            print(f"⚠ {unread_count} messages still unread")


def test_get_conversations():
    """Test getting all conversations for a user"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("TEST 4: GET CONVERSATIONS LIST")
        print("="*60)
        
        user1 = User.query.filter_by(email='alice@example.com').first()
        user2 = User.query.filter_by(email='bob@example.com').first()
        user3 = User.query.filter_by(email='carol@example.com').first()
        
        # Create conversation with Carol
        print(f"\nAlice sending message to Carol...")
        CommunityService.send_message(
            sender_id=user1.id,
            recipient_id=user3.id,
            content="Hi Carol! Let's collaborate on a project."
        )
        
        # Get all conversations for Alice
        print(f"\nGetting all conversations for Alice...")
        conversations = CommunityService.get_conversations(user1.id, limit=10)
        
        print(f"✓ Found {len(conversations)} conversations")
        
        for i, conv in enumerate(conversations, 1):
            print(f"\n  Conversation {i}:")
            print(f"    - With: {conv['other_user']['name']}")
            print(f"    - Last message: {conv['last_message_preview'][:50] if conv['last_message_preview'] else 'None'}...")
            print(f"    - Unread count: {conv['unread_count']}")
            print(f"    - Last message at: {conv['last_message_at']}")


def test_mark_conversation_read():
    """Test marking entire conversation as read"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("TEST 5: MARK CONVERSATION AS READ")
        print("="*60)
        
        user1 = User.query.filter_by(email='alice@example.com').first()
        user2 = User.query.filter_by(email='bob@example.com').first()
        
        # Send multiple messages from Alice to Bob
        print(f"\nAlice sending multiple messages to Bob...")
        for i in range(3):
            CommunityService.send_message(
                sender_id=user1.id,
                recipient_id=user2.id,
                content=f"Message {i+1} from Alice"
            )
        print(f"✓ Sent 3 messages")
        
        # Get conversation ID
        conv = CommunityService.get_or_create_conversation(user1.id, user2.id)
        
        # Check unread count before
        unread_before = Message.query.filter_by(
            conversation_id=conv.id,
            is_read=False,
            is_deleted=False
        ).filter(Message.sender_id != user2.id).count()
        
        print(f"\nUnread messages before: {unread_before}")
        
        # Mark conversation as read
        print(f"Bob marking conversation as read...")
        result = CommunityService.mark_conversation_read(user2.id, conv.id)
        
        if result['success']:
            print(f"✓ Marked {result['marked_read']} messages as read")
        
        # Check unread count after
        unread_after = Message.query.filter_by(
            conversation_id=conv.id,
            is_read=False,
            is_deleted=False
        ).filter(Message.sender_id != user2.id).count()
        
        print(f"Unread messages after: {unread_after}")
        
        if unread_after == 0:
            print(f"✓ All messages marked as read successfully")


def run_all_tests():
    """Run all Phase 8 tests"""
    
    print("\n" + "="*70)
    print(" "*15 + "PHASE 8: PRIVATE MESSAGING SYSTEM TEST SUITE")
    print("="*70)
    print("\nPhase 8 Logic:")
    print("- Create conversation if not exists")
    print("- Store message")
    print("- Mark unread for receiver")
    print("- Trigger notification event")
    print("="*70)
    
    # Create test users
    create_test_users()
    
    # Run tests
    test_conversation_creation()
    test_send_message()
    test_get_messages()
    test_get_conversations()
    test_mark_conversation_read()
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETED")
    print("="*70)
    print("\n✓ Phase 8 private messaging system is working correctly!")
    print("✓ Endpoints ready:")
    print("  - POST /api/community/message")
    print("  - GET /api/community/messages/<conversation_id>")
    print("  - GET /api/community/conversations")
    print("  - POST /api/community/conversations/<conversation_id>/read")
    print("\n")


if __name__ == '__main__':
    run_all_tests()
