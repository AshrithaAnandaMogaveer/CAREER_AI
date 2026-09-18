"""
Test: Verify users with same domain appear in Reach-Out
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask_cors_config import app, db
from user_model import User
from community_models import UserProfile
from community_service import CommunityService


def test_same_domain_matching():
    """Test that users with same domain appear in each other's reach-out"""
    
    print("="*60)
    print("Testing Same Domain Matching")
    print("="*60)
    
    with app.app_context():
        # Find users with Data Science domain
        data_science_users = db.session.query(User).join(
            UserProfile, User.id == UserProfile.user_id
        ).filter(
            UserProfile.domains.contains('"Data Science"')
        ).all()
        
        print(f"\nFound {len(data_science_users)} users with 'Data Science' domain:")
        for user in data_science_users:
            print(f"  - {user.name} (ID: {user.id}, Email: {user.email})")
        
        if len(data_science_users) < 2:
            print("\n⚠️  Need at least 2 users with same domain to test matching")
            print("   Please create 2 accounts with 'Data Science' domain")
            return
        
        # Test matching for first user
        test_user = data_science_users[0]
        print(f"\n{'='*60}")
        print(f"Testing Reach-Out for: {test_user.name}")
        print(f"{'='*60}")
        
        # Get matching profiles
        matches = CommunityService.get_related_profiles(
            user_id=test_user.id,
            limit=10,
            min_score=0,
            include_breakdown=True
        )
        
        print(f"\nFound {len(matches)} matching profiles:")
        
        for match in matches:
            print(f"\n  {match['name']}")
            print(f"    Domain: {match['domain']}")
            print(f"    Match Score: {match['similarity_score']:.1f}%")
            if 'score_breakdown' in match:
                print(f"    Breakdown:")
                print(f"      - Domain: {match['score_breakdown']['domain_match']:.1f}%")
                print(f"      - Skills: {match['score_breakdown']['skill_overlap']:.1f}%")
                print(f"      - Experience: {match['score_breakdown']['experience_match']:.1f}%")
                print(f"      - Interests: {match['score_breakdown']['interest_match']:.1f}%")
        
        # Check if other Data Science users appear
        other_ds_users = [u for u in data_science_users if u.id != test_user.id]
        matched_ids = [m['id'] for m in matches]
        
        print(f"\n{'='*60}")
        print("Verification:")
        print(f"{'='*60}")
        
        for other_user in other_ds_users:
            if other_user.id in matched_ids:
                print(f"  ✅ {other_user.name} appears in reach-out (CORRECT)")
            else:
                print(f"  ❌ {other_user.name} NOT in reach-out (ERROR)")
        
        # Success check
        all_matched = all(u.id in matched_ids for u in other_ds_users)
        
        print(f"\n{'='*60}")
        if all_matched:
            print("✅ SUCCESS: All users with same domain appear in Reach-Out!")
        else:
            print("❌ ISSUE: Some users with same domain are missing")
        print(f"{'='*60}")


if __name__ == '__main__':
    test_same_domain_matching()
