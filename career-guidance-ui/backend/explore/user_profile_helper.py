"""
User Profile Helper for Explore Personalization.
Reads UserProfile + UserAnalysisCache to build a personalization context.
Does NOT modify any Analyze, Routine, or Community logic.
"""

# Skill sets per career domain for overlap scoring
CAREER_SKILL_MAP = {
    'software engineer':         ['Python', 'Java', 'JavaScript', 'React', 'Node.js', 'SQL', 'Git', 'System Design'],
    'data scientist':            ['Python', 'Statistics', 'Machine Learning', 'SQL', 'Pandas', 'NumPy', 'Data Analysis', 'TensorFlow'],
    'machine learning engineer': ['Python', 'TensorFlow', 'PyTorch', 'Machine Learning', 'Statistics', 'Deep Learning', 'MLOps'],
    'product manager':           ['Product Strategy', 'Agile', 'User Research', 'Data Analysis', 'Communication', 'Roadmapping'],
    'ux designer':               ['Figma', 'User Research', 'Prototyping', 'UI Design', 'Wireframing', 'Adobe XD'],
    'devops engineer':           ['Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Linux', 'Terraform', 'Python', 'Bash'],
    'cybersecurity analyst':     ['Network Security', 'Python', 'Linux', 'Penetration Testing', 'SIEM', 'Cryptography'],
    'full stack developer':      ['React', 'Node.js', 'JavaScript', 'SQL', 'REST APIs', 'Git', 'CSS', 'TypeScript'],
    'data analyst':              ['SQL', 'Excel', 'Python', 'Data Visualization', 'Tableau', 'Power BI', 'Statistics'],
    'ai engineer':               ['Python', 'Machine Learning', 'Deep Learning', 'LLMs', 'MLOps', 'TensorFlow', 'PyTorch'],
}

# High-ROI skills that are commonly missing
HIGH_ROI_SKILLS = ['System Design', 'Machine Learning', 'AWS', 'Docker', 'Kubernetes',
                   'Python', 'SQL', 'TypeScript', 'React', 'Data Analysis']


def get_user_profile(user_id: int) -> dict:
    """
    Fetch user personalization context from DB.
    Returns skills, domain, readiness, missing_skills.
    Falls back gracefully if no data exists.
    """
    try:
        from community_models import UserProfile
        from user_model import User

        user = User.query.get(user_id)
        profile = UserProfile.query.filter_by(user_id=user_id).first()

        # Try to get cached analysis result
        analysis = _get_cached_analysis(user_id)

        user_skills = []
        target_domain = ''
        readiness_score = 0
        missing_skills = []

        if profile:
            user_skills = profile.skills or []
            domains = profile.domains or []
            target_domain = domains[0] if domains else ''

        if user and not target_domain:
            target_domain = user.domain or ''

        if analysis:
            readiness_score = analysis.get('readiness_score', 0)
            missing_skills = analysis.get('missing_skills', [])
            if not target_domain:
                target_domain = analysis.get('target_domain', '')
            if not user_skills:
                user_skills = analysis.get('extracted_skills', [])

        return {
            'user_id': user_id,
            'user_skills': [s.lower() for s in user_skills],
            'user_skills_raw': user_skills,
            'target_domain': target_domain,
            'readiness_score': readiness_score,
            'missing_skills': missing_skills,
            'has_analysis': bool(analysis),
        }

    except Exception:
        return {
            'user_id': user_id,
            'user_skills': [],
            'user_skills_raw': [],
            'target_domain': '',
            'readiness_score': 0,
            'missing_skills': [],
            'has_analysis': False,
        }


def _get_cached_analysis(user_id: int) -> dict:
    """Read the last analyze result from UserAnalysisCache table."""
    try:
        from explore_cache_model import UserAnalysisCache
        cache = UserAnalysisCache.query.filter_by(user_id=user_id).first()
        if cache:
            return {
                'readiness_score': cache.readiness_score,
                'missing_skills': cache.missing_skills or [],
                'extracted_skills': cache.extracted_skills or [],
                'target_domain': cache.target_domain or '',
            }
    except Exception:
        pass
    return None


def compute_fit_score(career_key: str, user_skills: list) -> int:
    """
    Compute how well a user's skills fit a career.
    fit_score = skill_overlap_ratio * 100
    """
    required = [s.lower() for s in CAREER_SKILL_MAP.get(career_key, [])]
    if not required:
        return 50
    overlap = sum(1 for s in user_skills if any(s in r or r in s for r in required))
    return min(round((overlap / len(required)) * 100), 100)


def get_missing_high_roi_skills(user_skills: list, missing_skills: list) -> list:
    """
    Return high-ROI skills the user is missing.
    Combines missing_skills from analyze with HIGH_ROI_SKILLS list.
    """
    user_lower = [s.lower() for s in user_skills]
    missing_lower = [s.lower() for s in missing_skills]

    result = []
    for skill in HIGH_ROI_SKILLS:
        sl = skill.lower()
        if sl not in user_lower:
            result.append(skill)
        if len(result) >= 5:
            break

    # Prepend analyze missing skills (top 3) if not already included
    for ms in missing_skills[:3]:
        if ms not in result:
            result.insert(0, ms)

    return result[:5]
