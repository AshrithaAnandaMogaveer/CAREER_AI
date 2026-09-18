"""
Migration Script: Create Missing User Profiles
Run this once to create profiles for existing users who signed up before the fix
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask_cors_config import app, db
from user_model import User
from community_models import UserProfile


def create_missing_profiles():
    """Create UserProfile for all users who don't have one"""
    
    print("="*60)
    print("Creating Missing User Profiles")
    print("="*60)
    
    with app.app_context():
        # Get all active users
        users = User.query.filter_by(is_deleted=False, is_active=True).all()
        
        print(f"\nFound {len(users)} active users")
        
        created = 0
        skipped = 0
        
        for user in users:
            # Check if profile already exists
            profile = UserProfile.query.filter_by(user_id=user.id).first()
            
            if profile:
                print(f"  ⏭️  Skipped: {user.name} (profile exists)")
                skipped += 1
            else:
                # Create profile
                profile = UserProfile(
                    user_id=user.id,
                    domains=[user.domain] if user.domain else [],
                    skills=[],
                    interests=[],
                    experience_years=0,
                    projects_count=0
                )
                db.session.add(profile)
                print(f"  ✅ Created: {user.name} (domain: {user.domain})")
                created += 1
        
        # Commit all changes
        if created > 0:
            db.session.commit()
            print(f"\n✅ Successfully created {created} profiles")
        else:
            print(f"\n✅ No profiles needed to be created")
        
        print(f"   Skipped: {skipped} (already had profiles)")
        print(f"   Total: {len(users)} users")
        
        print("\n" + "="*60)
        print("Migration Complete!")
        print("="*60)
        print("\nNext steps:")
        print("1. Users can now appear in Reach-Out")
        print("2. Encourage users to update their profiles with skills/interests")
        print("3. Better profiles = better matches!")
        print("\n" + "="*60)


if __name__ == "__main__":
    try:
        create_missing_profiles()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
