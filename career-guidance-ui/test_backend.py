"""
Quick test script to verify backend modules are working
"""

import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

print("Testing backend modules...")
print("-" * 50)

# Test 1: Import modules
try:
    from resumeAnalyzer import ResumeAnalyzer
    print("✓ ResumeAnalyzer imported successfully")
except Exception as e:
    print(f"✗ ResumeAnalyzer import failed: {e}")

try:
    from skillEngine import SkillEngine
    print("✓ SkillEngine imported successfully")
except Exception as e:
    print(f"✗ SkillEngine import failed: {e}")

try:
    from reportGenerator import ReportGenerator
    print("✓ ReportGenerator imported successfully")
except Exception as e:
    print(f"✗ ReportGenerator import failed: {e}")

print("-" * 50)

# Test 2: Initialize classes
try:
    analyzer = ResumeAnalyzer()
    print("✓ ResumeAnalyzer initialized")
except Exception as e:
    print(f"✗ ResumeAnalyzer initialization failed: {e}")

try:
    engine = SkillEngine()
    print("✓ SkillEngine initialized")
except Exception as e:
    print(f"✗ SkillEngine initialization failed: {e}")

try:
    generator = ReportGenerator()
    print("✓ ReportGenerator initialized")
except Exception as e:
    print(f"✗ ReportGenerator initialization failed: {e}")

print("-" * 50)

# Test 3: Test basic functionality
try:
    engine = SkillEngine()
    test_skills = {'python', 'javascript', 'react', 'sql'}
    result = engine.calculate_readiness_score(
        test_skills,
        'Software Development',
        3,
        True,
        True
    )
    print(f"✓ Readiness score calculation works: {result['total_score']}%")
except Exception as e:
    print(f"✗ Readiness score calculation failed: {e}")

print("-" * 50)
print("Backend test complete!")
