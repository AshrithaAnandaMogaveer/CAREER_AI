# Phase 7: Profile Matching (Reach-Out) - COMPLETE ✓

## Overview
Implemented weighted similarity scoring algorithm for user profile matching in the Reach-Out feature.

## Weighted Similarity Formula
```
score = 0.4 × domainMatch + 0.3 × skillOverlap + 0.2 × experienceMatch + 0.1 × interestMatch
```

### Component Scoring Details

1. **Domain Match (40% weight)**
   - Exact match: 100%
   - Partial match (substring): 70%
   - No match: 0%

2. **Skill Overlap (30% weight)**
   - Uses Jaccard similarity coefficient
   - Formula: (common skills / total unique skills) × 100
   - Case-insensitive comparison

3. **Experience Match (20% weight)**
   - Same experience: 100%
   - Decreases by 10% per year difference
   - Max penalty at 10+ years: 0%

4. **Interest Match (10% weight)**
   - Uses Jaccard similarity coefficient
   - Formula: (common interests / total unique interests) × 100
   - Case-insensitive comparison

## Files Created

### Backend
1. **profile_matching_engine.py** (NEW)
   - `ProfileMatchingEngine` class with weighted scoring
   - `calculate_domain_match()` - Domain similarity
   - `calculate_skill_overlap()` - Skill Jaccard similarity
   - `calculate_experience_match()` - Experience proximity
   - `calculate_interest_match()` - Interest Jaccard similarity
   - `calculate_weighted_score()` - Final weighted calculation
   - `match_profiles()` - Main matching algorithm
   - `get_match_explanation()` - Human-readable match reason

2. **test_profile_matching.py** (NEW)
   - Comprehensive test suite
   - Creates 5 test users with diverse profiles
   - Tests all component scoring functions
   - Tests full profile matching with ranking
   - Tests minimum score threshold filtering

### Backend Updates
3. **community_service.py** (UPDATED)
   - Imported `ProfileMatchingEngine`
   - Updated `get_related_profiles()` method
   - Added parameters: `min_score`, `include_breakdown`
   - Returns enhanced profile data with match reasons

4. **flask_cors_config.py** (UPDATED)
   - Updated `/api/community/reach-out` endpoint
   - Added `/api/community/reachout` alias
   - Added query parameters:
     - `limit`: Max profiles (1-50, default 10)
     - `min_score`: Minimum score threshold (0-100, default 0)
     - `include_breakdown`: Show detailed scores (true/false, default false)
   - Returns: `{success, profiles, has_profile, count, min_score_threshold}`

### Frontend Updates
5. **ReachOut.jsx** (UPDATED)
   - Updated to use new `/api/community/reachout` endpoint
   - Added query parameters: `limit=20&min_score=10`
   - Display `similarity_score` instead of `similarity_percentage`
   - Show `match_reason` below score bar
   - Display user bio if available
   - Show common interests with purple badges
   - Capitalize skill and interest names

## API Endpoint

### GET /api/community/reachout
**Aliases:** `/api/community/reach-out`

**Query Parameters:**
- `limit` (optional): Maximum number of profiles (1-50, default 10)
- `min_score` (optional): Minimum similarity score 0-100 (default 0)
- `include_breakdown` (optional): Include detailed score breakdown (true/false, default false)

**Response:**
```json
{
  "success": true,
  "profiles": [
    {
      "id": 2,
      "name": "Bob Fullstack",
      "email": "fullstack@example.com",
      "domain": "Software Development",
      "bio": "Full stack developer passionate about modern web tech",
      "location": null,
      "experience_years": 4,
      "projects_count": 8,
      "similarity_score": 63.33,
      "match_reason": "Similar domain • Similar experience",
      "common_skills": ["python"],
      "common_interests": ["web development"],
      "total_skills": 5,
      "total_interests": 3
    }
  ],
  "has_profile": true,
  "count": 5,
  "min_score_threshold": 10
}
```

**With `include_breakdown=true`:**
```json
{
  "score_breakdown": {
    "domain_match": 100.0,
    "skill_overlap": 11.11,
    "experience_match": 90.0,
    "interest_match": 20.0
  }
}
```

## Test Results

### Component Score Tests
✓ Domain Match: 100% (exact), 70% (partial), 0% (no match)
✓ Skill Overlap: 33.33% (2 common / 6 total)
✓ Experience Match: 100% (same), 90% (1 year diff), 60% (4 years diff)
✓ Interest Match: 20% (1 common / 5 total)
✓ Weighted Score: 74% with example components

### Profile Matching Tests
✓ Created 5 diverse test users
✓ Found 5 matching profiles for Python Developer
✓ Top match: 63.33% (Full Stack Developer - same domain, similar experience)
✓ Lowest match: 18% (Mobile Developer - only experience similarity)
✓ Minimum score filtering: 3 matches with score >= 30%

### Test Users Created
1. Alice Python - Python Developer (5 years, 12 projects)
2. Bob Fullstack - Full Stack Developer (4 years, 8 projects)
3. Carol Data - Data Scientist (6 years, 15 projects)
4. Dave Junior - Junior Developer (1 year, 3 projects)
5. Eve Mobile - Mobile Developer (4 years, 10 projects)

## Algorithm Performance

### Ranking Example (for Alice Python)
1. **Bob Fullstack: 63.33%**
   - Domain: 100% (same domain)
   - Skills: 11.11% (1 common skill: Python)
   - Experience: 90% (1 year difference)
   - Interests: 20% (1 common interest)

2. **Dave Junior: 57.75%**
   - Domain: 100% (same domain)
   - Skills: 12.5%
   - Experience: 60% (4 years difference)
   - Interests: 20%

3. **Carol Data: 21.33%**
   - Domain: 0% (different domain)
   - Skills: 11.11% (Python only)
   - Experience: 90% (1 year difference)
   - Interests: 0%

## Key Features

1. **Weighted Scoring**: Domain has highest weight (40%), reflecting its importance
2. **Jaccard Similarity**: Used for skills and interests for accurate overlap measurement
3. **Experience Proximity**: Rewards similar experience levels
4. **Match Explanations**: Human-readable reasons for each match
5. **Flexible Filtering**: Minimum score threshold to show only quality matches
6. **Scalable**: Efficient algorithm that works with large user bases
7. **Case-Insensitive**: All comparisons ignore case for better matching

## Usage Examples

### Basic Usage
```bash
GET /api/community/reachout
# Returns top 10 matches with any score
```

### With Filters
```bash
GET /api/community/reachout?limit=20&min_score=30
# Returns top 20 matches with score >= 30%
```

### With Detailed Breakdown
```bash
GET /api/community/reachout?include_breakdown=true
# Returns matches with detailed score components
```

## Frontend Integration

The ReachOut component now displays:
- Match score with color-coded progress bar
- Match reason (e.g., "Similar domain • Similar experience")
- User bio
- Common skills (teal badges)
- Common interests (purple badges)
- Experience years and project count

## Next Steps

Phase 7 is complete and tested. The profile matching system is ready for production use.

**To use:**
1. Restart Flask server: `python flask_cors_config.py`
2. Ensure users have UserProfile records with skills, interests, and domains
3. Navigate to Community > Reach Out tab
4. View ranked matching profiles

## Notes

- Users without profiles will see a message to complete their profile
- Minimum score threshold helps filter out low-quality matches
- The algorithm is optimized for accuracy over speed (suitable for <10k users)
- For larger scale, consider caching or background processing
