"""
Test script for Reach-Out feature
Verifies that the profile matching system is working correctly
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from profile_matching_engine import ProfileMatchingEngine


def test_domain_match():
    """Test domain matching logic"""
    print("="*60)
    print("TEST 1: Domain Matching")
    print("="*60)
    
    # Test exact match
    score1 = ProfileMatchingEngine.calculate_domain_match(
        "Data Science",
        ["Data Science", "Machine Learning"]
    )
    assert score1 == 100.0, f"Expected 100.0, got {score1}"
    print(f"✅ Exact match: {score1}%")
    
    # Test partial match
    score2 = ProfileMatchingEngine.calculate_domain_match(
        "Data Science",
        ["Data Science Engineering", "Business Intelligence"]
    )
    assert score2 == 70.0, f"Expected 70.0, got {score2}"
    print(f"✅ Partial match: {score2}%")
    
    # Test no match
    score3 = ProfileMatchingEngine.calculate_domain_match(
        "Data Science",
        ["Web Development", "Mobile Apps"]
    )
    assert score3 == 0.0, f"Expected 0.0, got {score3}"
    print(f"✅ No match: {score3}%")
    
    print("✅ Domain matching tests PASSED\n")


def test_skill_overlap():
    """Test skill overlap calculation"""
    print("="*60)
    print("TEST 2: Skill Overlap")
    print("="*60)
    
    # Test with common skills
    user_skills = ["Python", "SQL", "Machine Learning", "Pandas"]
    profile_skills = ["Python", "SQL", "R", "Statistics"]
    
    score = ProfileMatchingEngine.calculate_skill_overlap(
        user_skills,
        profile_skills
    )
    
    # Jaccard: 2 common / 6 unique = 33.33%
    expected = 33.33
    assert abs(score - expected) < 1, f"Expected ~{expected}, got {score}"
    print(f"✅ Skill overlap: {score}%")
    print(f"   Common: Python, SQL")
    print(f"   Total unique: 6 skills")
    
    # Test with no common skills
    score2 = ProfileMatchingEngine.calculate_skill_overlap(
        ["Python", "Django"],
        ["Java", "Spring"]
    )
    assert score2 == 0.0, f"Expected 0.0, got {score2}"
    print(f"✅ No common skills: {score2}%")
    
    print("✅ Skill overlap tests PASSED\n")


def test_experience_match():
    """Test experience matching"""
    print("="*60)
    print("TEST 3: Experience Matching")
    print("="*60)
    
    # Test exact match
    score1 = ProfileMatchingEngine.calculate_experience_match(3, 3)
    assert score1 == 100.0, f"Expected 100.0, got {score1}"
    print(f"✅ Same experience (3 years): {score1}%")
    
    # Test 1 year difference
    score2 = ProfileMatchingEngine.calculate_experience_match(3, 4)
    assert score2 == 90.0, f"Expected 90.0, got {score2}"
    print(f"✅ 1 year difference: {score2}%")
    
    # Test 5 year difference
    score3 = ProfileMatchingEngine.calculate_experience_match(2, 7)
    assert score3 == 50.0, f"Expected 50.0, got {score3}"
    print(f"✅ 5 year difference: {score3}%")
    
    # Test large difference
    score4 = ProfileMatchingEngine.calculate_experience_match(1, 15)
    assert score4 == 0.0, f"Expected 0.0, got {score4}"
    print(f"✅ 14 year difference: {score4}%")
    
    print("✅ Experience matching tests PASSED\n")


def test_interest_match():
    """Test interest matching"""
    print("="*60)
    print("TEST 4: Interest Matching")
    print("="*60)
    
    user_interests = ["AI", "Machine Learning", "Data Visualization"]
    profile_interests = ["AI", "Deep Learning", "Computer Vision"]
    
    score = ProfileMatchingEngine.calculate_interest_match(
        user_interests,
        profile_interests
    )
    
    # Jaccard: 1 common / 5 unique = 20%
    expected = 20.0
    assert abs(score - expected) < 1, f"Expected ~{expected}, got {score}"
    print(f"✅ Interest match: {score}%")
    print(f"   Common: AI")
    print(f"   Total unique: 5 interests")
    
    print("✅ Interest matching tests PASSED\n")


def test_weighted_score():
    """Test weighted score calculation"""
    print("="*60)
    print("TEST 5: Weighted Score Calculation")
    print("="*60)
    
    # Example scores
    domain_score = 100.0      # Exact domain match
    skill_score = 40.0        # 40% skill overlap
    experience_score = 90.0   # 1 year difference
    interest_score = 25.0     # 25% interest match
    
    total_score = ProfileMatchingEngine.calculate_weighted_score(
        domain_score,
        skill_score,
        experience_score,
        interest_score
    )
    
    # Calculate expected
    expected = (100 * 0.4) + (40 * 0.3) + (90 * 0.2) + (25 * 0.1)
    # = 40 + 12 + 18 + 2.5 = 72.5
    
    assert abs(total_score - expected) < 0.1, f"Expected {expected}, got {total_score}"
    print(f"✅ Weighted score: {total_score}%")
    print(f"   Domain (40%): {domain_score} × 0.4 = {domain_score * 0.4}")
    print(f"   Skills (30%): {skill_score} × 0.3 = {skill_score * 0.3}")
    print(f"   Experience (20%): {experience_score} × 0.2 = {experience_score * 0.2}")
    print(f"   Interests (10%): {interest_score} × 0.1 = {interest_score * 0.1}")
    print(f"   Total: {total_score}%")
    
    print("✅ Weighted score tests PASSED\n")


def test_match_explanation():
    """Test match explanation generation"""
    print("="*60)
    print("TEST 6: Match Explanation")
    print("="*60)
    
    score_breakdown = {
        'domain_match': 100.0,
        'skill_overlap': 75.0,
        'experience_match': 90.0,
        'interest_match': 60.0
    }
    
    explanation = ProfileMatchingEngine.get_match_explanation(score_breakdown)
    
    print(f"✅ Match explanation: {explanation}")
    assert "similar domain" in explanation.lower(), "Should mention domain"
    assert "skill" in explanation.lower(), "Should mention skills"
    assert "experience" in explanation.lower(), "Should mention experience"
    assert "interest" in explanation.lower(), "Should mention interests"
    
    print("✅ Match explanation tests PASSED\n")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("REACH-OUT FEATURE TEST SUITE")
    print("="*60)
    print("\nTesting Profile Matching Engine...\n")
    
    try:
        test_domain_match()
        test_skill_overlap()
        test_experience_match()
        test_interest_match()
        test_weighted_score()
        test_match_explanation()
        
        print("="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nThe Reach-Out feature is working correctly!")
        print("Profile matching algorithm verified.")
        print("\nNext steps:")
        print("1. Ensure Flask server is running")
        print("2. Test the API endpoint: GET /api/community/reach-out")
        print("3. Open the app and navigate to Community → Reach Out")
        print("\n" + "="*60)
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
