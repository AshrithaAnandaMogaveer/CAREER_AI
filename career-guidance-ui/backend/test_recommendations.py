"""
Test script for recommendation engine
Creates sample data and tests recommendations
"""

import sys
import os

# Add backend to path
backend_path = os.path.dirname(os.path.abspath(__file__))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app_config import create_app
from community_models import db, Community, UserProfile
from user_model import User
from recommendation_engine import RecommendationEngine


def create_sample_data():
    """Create sample communities and user profile for testing"""
    app = create_app()
    
    with app.app_context():
        print("Creating sample data...")
        
        # Check if test user exists
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            print("Test user not found. Please sign up first.")
            return
        
        print(f"✓ Found test user: {test_user.name} (ID: {test_user.id})")
        
        # Create user profile with interests
        profile = UserProfile.query.filter_by(user_id=test_user.id).first()
        if not profile:
            profile = UserProfile(
                user_id=test_user.id,
                skills=['Python', 'JavaScript', 'React', 'Machine Learning'],
                interests=['Web Development', 'AI', 'Data Science', 'Cloud Computing'],
                domains=['Software Development', 'Technology'],
                bio='Full-stack developer interested in AI and web technologies',
                experience_years=3,
                projects_count=10
            )
            db.session.add(profile)
            print("✓ Created user profile with interests")
        else:
            print("✓ User profile already exists")
        
        # Create sample communities if they don't exist
        communities_data = [
            {
                'name': 'Python Developers',
                'description': 'Community for Python enthusiasts and professionals',
                'category': 'Programming',
                'tags': ['Python', 'Backend', 'Django', 'Flask', 'Data Science']
            },
            {
                'name': 'React & Frontend',
                'description': 'Modern frontend development with React and friends',
                'category': 'Web Development',
                'tags': ['React', 'JavaScript', 'Frontend', 'Web Development', 'UI/UX']
            },
            {
                'name': 'Machine Learning Hub',
                'description': 'Discuss ML algorithms, models, and applications',
                'category': 'AI & ML',
                'tags': ['Machine Learning', 'AI', 'Deep Learning', 'Python', 'Data Science']
            },
            {
                'name': 'Cloud Architecture',
                'description': 'Cloud computing, AWS, Azure, and DevOps',
                'category': 'Cloud',
                'tags': ['Cloud Computing', 'AWS', 'Azure', 'DevOps', 'Infrastructure']
            },
            {
                'name': 'Mobile Development',
                'description': 'iOS, Android, and cross-platform mobile apps',
                'category': 'Mobile',
                'tags': ['Mobile', 'iOS', 'Android', 'React Native', 'Flutter']
            },
            {
                'name': 'Blockchain & Crypto',
                'description': 'Blockchain technology and cryptocurrency',
                'category': 'Blockchain',
                'tags': ['Blockchain', 'Cryptocurrency', 'Web3', 'Smart Contracts']
            },
            {
                'name': 'Game Development',
                'description': 'Create games with Unity, Unreal, and more',
                'category': 'Gaming',
                'tags': ['Game Development', 'Unity', 'Unreal Engine', 'C++', 'Graphics']
            }
        ]
        
        created_count = 0
        for comm_data in communities_data:
            existing = Community.query.filter_by(name=comm_data['name']).first()
            if not existing:
                community = Community(
                    name=comm_data['name'],
                    description=comm_data['description'],
                    category=comm_data['category'],
                    tags=comm_data['tags'],
                    created_by=test_user.id,
                    members_count=50 + (created_count * 20),
                    posts_count=10 + (created_count * 5)
                )
                db.session.add(community)
                created_count += 1
        
        if created_count > 0:
            print(f"✓ Created {created_count} sample communities")
        else:
            print("✓ Sample communities already exist")
        
        db.session.commit()
        print("\n✅ Sample data created successfully!")


def test_recommendations():
    """Test the recommendation engine"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("TESTING RECOMMENDATION ENGINE")
        print("="*60)
        
        # Get test user
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            print("❌ Test user not found")
            return
        
        print(f"\nUser: {test_user.name}")
        
        # Get user profile
        profile = UserProfile.query.filter_by(user_id=test_user.id).first()
        if profile:
            print(f"Skills: {', '.join(profile.skills or [])}")
            print(f"Interests: {', '.join(profile.interests or [])}")
            print(f"Domains: {', '.join(profile.domains or [])}")
        else:
            print("No profile found")
        
        print("\n" + "-"*60)
        print("RECOMMENDATIONS (Top 5)")
        print("-"*60)
        
        # Get recommendations
        recommendations = RecommendationEngine.recommend_communities(
            user_id=test_user.id,
            limit=5
        )
        
        if not recommendations:
            print("No recommendations found")
            print("\nTrying trending communities instead...")
            recommendations = RecommendationEngine.get_trending_communities(limit=5)
            
            for i, rec in enumerate(recommendations, 1):
                print(f"\n{i}. {rec['name']}")
                print(f"   Category: {rec['category']}")
                print(f"   Trending Score: {rec['trending_score']}%")
                print(f"   Members: {rec['members_count']} | Posts: {rec['posts_count']}")
                print(f"   Tags: {', '.join(rec['tags'])}")
        else:
            for i, rec in enumerate(recommendations, 1):
                print(f"\n{i}. {rec['name']}")
                print(f"   Category: {rec['category']}")
                print(f"   Similarity Score: {rec['similarity_score']}%")
                print(f"   Matching Tags: {', '.join(rec['matching_tags'])}")
                print(f"   Reason: {rec['match_reason']}")
                print(f"   Members: {rec['members_count']} | Posts: {rec['posts_count']}")
        
        print("\n" + "="*60)
        print("✅ TEST COMPLETE")
        print("="*60)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Test recommendation engine')
    parser.add_argument('--create-data', action='store_true', help='Create sample data')
    parser.add_argument('--test', action='store_true', help='Test recommendations')
    
    args = parser.parse_args()
    
    if args.create_data:
        create_sample_data()
    
    if args.test:
        test_recommendations()
    
    if not args.create_data and not args.test:
        # Run both by default
        create_sample_data()
        test_recommendations()
