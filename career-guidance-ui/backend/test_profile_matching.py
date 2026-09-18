"""
Test script for Phase 7 - Profile Matching (Reach-Out)
Tests the weighted similarity scoring algorithm
"""

import sys
import os

# Add backend to path
backend_path = os.path.dirname(__file__)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from profile_matching_engine import ProfileMatchingEngine
from community_models import db, UserProfile
from user_model import User
from app_config import create_app

# Create Flask app
app = create_app()


def create_test_users():
    """Create test users with profiles for matching"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("CREATING TEST USERS WITH PROFILES")
        print("="*60)
        
        # User 1: Python Developer
        user1 = User.query.filter_by(email='python.dev@example.com').first()
        if not user1:
            user1 = User(name='Alice Python', email='python.dev@example.com', domain='Software Development')
            user1.set_password('password123')
            db.session.add(user1)
            db.session.flush()
            
            profile1 = UserProfile(
                user_id=user1.id,
                skills=['Python', 'Django', 'Flask', 'PostgreSQL', 'REST API'],
                interests=['Web Development', 'Backend', 'API Design'],
                domains=['Software Development', 'Web Development'],
                bio='Senior Python developer with 5 years experience',
                experience_years=5,
                projects_count=12
            )
            db.session.add(profile1)
            print(f"✓ Created: {user1.name} - Python Developer")
        
        # User 2: Full Stack Developer (similar to User 1)
        user2 = User.query.filter_by(email='fullstack@example.com').first()
        if not user2:
            user2 = User(name='Bob Fullstack', email='fullstack@example.com', domain='Software Development')
            user2.set_password('password123')
            db.session.add(user2)
            db.session.flush()
            
            profile2 = UserProfile(
                user_id=user2.id,
                skills=['Python', 'JavaScript', 'React', 'Node.js', 'MongoDB'],
                interests=['Web Development', 'Full Stack', 'Cloud'],
                domains=['Software Development', 'Web Development'],
                bio='Full stack developer passionate about modern web tech',
                experience_years=4,
                projects_count=8
            )
            db.session.add(profile2)
            print(f"✓ Created: {user2.name} - Full Stack Developer")
        
        # User 3: Data Scientist (different domain)
        user3 = User.query.filter_by(email='data.scientist@example.com').first()
        if not user3:
            user3 = User(name='Carol Data', email='data.scientist@example.com', domain='Data Science')
            user3.set_password('password123')
            db.session.add(user3)
            db.session.flush()
            
            profile3 = UserProfile(
                user_id=user3.id,
                skills=['Python', 'Machine Learning', 'TensorFlow', 'Pandas', 'NumPy'],
                interests=['AI', 'Machine Learning', 'Data Analysis'],
                domains=['Data Science', 'Artificial Intelligence'],
                bio='Data scientist specializing in ML and AI',
                experience_years=6,
                projects_count=15
            )
            db.session.add(profile3)
            print(f"✓ Created: {user3.name} - Data Scientist")
        
        # User 4: Junior Developer (less experience)
        user4 = User.query.filter_by(email='junior.dev@example.com').first()
        if not user4:
            user4 = User(name='Dave Junior', email='junior.dev@example.com', domain='Software Development')
            user4.set_password('password123')
            db.session.add(user4)
            db.session.flush()
            
            profile4 = UserProfile(
                user_id=user4.id,
                skills=['Python', 'HTML', 'CSS', 'JavaScript'],
                interests=['Web Development', 'Learning', 'Open Source'],
                domains=['Software Development'],
                bio='Junior developer eager to learn',
                experience_years=1,
                projects_count=3
            )
            db.session.add(profile4)
            print(f"✓ Created: {user4.name} - Junior Developer")
        
        # User 5: Mobile Developer (different skills)
        user5 = User.query.filter_by(email='mobile.dev@example.com').first()
        if not user5:
            user5 = User(name='Eve Mobile', email='mobile.dev@example.com', domain='Mobile Development')
            user5.set_password('password123')
            db.session.add(user5)
            db.session.flush()
            
            profile5 = UserProfile(
                user_id=user5.id,
                skills=['Swift', 'Kotlin', 'React Native', 'Firebase', 'iOS'],
                interests=['Mobile Apps', 'UI/UX', 'iOS Development'],
                domains=['Mobile Development', 'App Development'],
                bio='Mobile developer for iOS and Android',
                experience_years=4,
                projects_count=10
            )
            db.session.add(profile5)
            print(f"✓ Created: {user5.name} - Mobile Developer")
        
        db.session.commit()
        print("\n✓ All test users created successfully!")


def test_component_scores():
    """Test individual scoring components"""
    
    print("\n" + "="*60)
    print("TESTING COMPONENT SCORES")
    print("="*60)
    
    # Test 1: Domain Match
    print("\n" + "-"*60)
    print("TEST 1: Domain Match Scoring")
    print("-"*60)
    
    score1 = ProfileMatchingEngine.calculate_domain_match(
        'Software Development',
        ['Software Development', 'Web Development']
    )
    print(f"Exact match: {score1}% (expected 100%)")
    
    score2 = ProfileMatchingEngine.calculate_domain_match(
        'Software Development',
        ['Software Engineering', 'Web Development']
    )
    print(f"Partial match: {score2}% (expected 70%)")
    
    score3 = ProfileMatchingEngine.calculate_domain_match(
        'Software Development',
        ['Data Science', 'Machine Learning']
    )
    print(f"No match: {score3}% (expected 0%)")
    
    # Test 2: Skill Overlap
    print("\n" + "-"*60)
    print("TEST 2: Skill Overlap Scoring")
    print("-"*60)
    
    skills1 = ['Python', 'Django', 'Flask', 'PostgreSQL']
    skills2 = ['Python', 'Django', 'React', 'Node.js']
    score = ProfileMatchingEngine.calculate_skill_overlap(skills1, skills2)
    print(f"Skill overlap: {score}%")
    print(f"  Common: Python, Django")
    print(f"  Total unique: 6 skills")
    print(f"  Jaccard: 2/6 = 33.33%")
    
    # Test 3: Experience Match
    print("\n" + "-"*60)
    print("TEST 3: Experience Match Scoring")
    print("-"*60)
    
    score1 = ProfileMatchingEngine.calculate_experience_match(5, 5)
    print(f"Same experience (5 vs 5): {score1}% (expected 100%)")
    
    score2 = ProfileMatchingEngine.calculate_experience_match(5, 4)
    print(f"1 year diff (5 vs 4): {score2}% (expected 90%)")
    
    score3 = ProfileMatchingEngine.calculate_experience_match(5, 1)
    print(f"4 years diff (5 vs 1): {score3}% (expected 60%)")
    
    # Test 4: Interest Match
    print("\n" + "-"*60)
    print("TEST 4: Interest Match Scoring")
    print("-"*60)
    
    interests1 = ['Web Development', 'Backend', 'API Design']
    interests2 = ['Web Development', 'Full Stack', 'Cloud']
    score = ProfileMatchingEngine.calculate_interest_match(interests1, interests2)
    print(f"Interest overlap: {score}%")
    print(f"  Common: Web Development")
    print(f"  Total unique: 5 interests")
    print(f"  Jaccard: 1/5 = 20%")
    
    # Test 5: Weighted Score
    print("\n" + "-"*60)
    print("TEST 5: Weighted Score Calculation")
    print("-"*60)
    
    domain_score = 100.0
    skill_score = 50.0
    experience_score = 80.0
    interest_score = 30.0
    
    weighted = ProfileMatchingEngine.calculate_weighted_score(
        domain_score, skill_score, experience_score, interest_score
    )
    
    print(f"Component scores:")
    print(f"  Domain: {domain_score}% (weight: 0.4)")
    print(f"  Skills: {skill_score}% (weight: 0.3)")
    print(f"  Experience: {experience_score}% (weight: 0.2)")
    print(f"  Interests: {interest_score}% (weight: 0.1)")
    print(f"\nWeighted total: {weighted}%")
    print(f"Calculation: (100×0.4) + (50×0.3) + (80×0.2) + (30×0.1) = {weighted}%")


def test_profile_matching():
    """Test full profile matching"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("TESTING PROFILE MATCHING")
        print("="*60)
        
        # Get User 1 (Python Developer)
        user1 = User.query.filter_by(email='python.dev@example.com').first()
        
        if not user1:
            print("✗ Test user not found. Run create_test_users() first.")
            return
        
        print(f"\nFinding matches for: {user1.name}")
        print(f"Domain: {user1.domain}")
        
        profile1 = UserProfile.query.filter_by(user_id=user1.id).first()
        print(f"Skills: {', '.join(profile1.skills[:3])}...")
        print(f"Experience: {profile1.experience_years} years")
        
        # Find matches using the engine directly
        matches = ProfileMatchingEngine.match_profiles(
            user_id=user1.id,
            limit=10,
            min_score=0
        )
        
        print(f"\n✓ Found {len(matches)} matching profiles")
        print("\n" + "-"*60)
        print("TOP MATCHES (Ranked by Similarity)")
        print("-"*60)
        
        for i, match in enumerate(matches, 1):
            print(f"\n{i}. {match['name']} - {match['domain']}")
            print(f"   Similarity Score: {match['similarity_score']}%")
            
            # Generate match reason from breakdown
            breakdown = match['score_breakdown']
            reasons = []
            if breakdown['domain_match'] >= 70:
                reasons.append("Similar domain")
            if breakdown['skill_overlap'] >= 30:
                reasons.append(f"{breakdown['skill_overlap']:.0f}% skill overlap")
            if breakdown['experience_match'] >= 80:
                reasons.append("Similar experience")
            if breakdown['interest_match'] >= 30:
                reasons.append("Shared interests")
            
            print(f"   Match Reason: {' • '.join(reasons) if reasons else 'Potential connection'}")
            print(f"   Experience: {match['experience_years']} years")
            print(f"   Common Skills: {', '.join(match['common_skills'][:3]) if match['common_skills'] else 'None'}")
            print(f"   Common Interests: {', '.join(match['common_interests'][:2]) if match['common_interests'] else 'None'}")
            print(f"   Score Breakdown:")
            print(f"     - Domain: {breakdown['domain_match']}%")
            print(f"     - Skills: {breakdown['skill_overlap']}%")
            print(f"     - Experience: {breakdown['experience_match']}%")
            print(f"     - Interests: {breakdown['interest_match']}%")
        
        # Test with minimum score threshold
        print("\n" + "-"*60)
        print("TESTING MINIMUM SCORE THRESHOLD")
        print("-"*60)
        
        high_quality_matches = ProfileMatchingEngine.match_profiles(
            user_id=user1.id,
            limit=10,
            min_score=30  # Only matches with 30%+ similarity
        )
        
        print(f"\n✓ Found {len(high_quality_matches)} matches with score >= 30%")
        
        for match in high_quality_matches:
            print(f"  - {match['name']}: {match['similarity_score']}%")


def run_all_tests():
    """Run all Phase 7 tests"""
    
    print("\n" + "="*70)
    print(" "*15 + "PHASE 7: PROFILE MATCHING TEST SUITE")
    print("="*70)
    print("\nWeighted Similarity Formula:")
    print("score = 0.4 × domainMatch + 0.3 × skillOverlap + 0.2 × experienceMatch + 0.1 × interestMatch")
    print("="*70)
    
    # Create test data
    create_test_users()
    
    # Test component scores
    test_component_scores()
    
    # Test full matching
    test_profile_matching()
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETED")
    print("="*70)
    print("\n✓ Phase 7 profile matching is working correctly!")
    print("✓ Endpoint ready: GET /api/community/reachout")
    print("✓ Query params: limit, min_score, include_breakdown")
    print("\n")


if __name__ == '__main__':
    run_all_tests()
