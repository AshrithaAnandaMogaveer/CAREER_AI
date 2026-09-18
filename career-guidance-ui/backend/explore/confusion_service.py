"""
Confusion Solver / Path Suggestion Service
Maps user answers to career suggestions.
"""

CAREER_MAP = [
    {
        'conditions': {'interest': 'analytical', 'math_level': 'high'},
        'careers': ['Data Scientist', 'Machine Learning Engineer', 'AI Engineer'],
        'match': 92,
        'why': 'Your analytical mindset and strong math skills are ideal for data-driven roles.',
        'next': ['Learn Python & Statistics', 'Complete an ML course', 'Work on Kaggle datasets'],
    },
    {
        'conditions': {'interest': 'building', 'creativity': 'low'},
        'careers': ['Backend Developer', 'DevOps Engineer', 'Software Engineer'],
        'match': 89,
        'why': 'You enjoy building systems and prefer structured, logic-driven work.',
        'next': ['Master a backend language', 'Learn system design', 'Build 2–3 projects'],
    },
    {
        'conditions': {'interest': 'building', 'creativity': 'high'},
        'careers': ['Full Stack Developer', 'Software Engineer', 'Product Engineer'],
        'match': 87,
        'why': 'You combine technical building skills with creative thinking — full stack is a great fit.',
        'next': ['Learn React + Node.js', 'Build a portfolio project', 'Contribute to open source'],
    },
    {
        'conditions': {'interest': 'design', 'creativity': 'high'},
        'careers': ['UX Designer', 'Product Designer', 'UI Developer'],
        'match': 88,
        'why': 'Your creativity and design interest align perfectly with UX/UI roles.',
        'next': ['Learn Figma', 'Study UX principles', 'Build a design portfolio'],
    },
    {
        'conditions': {'interest': 'security', 'risk': 'low'},
        'careers': ['Cybersecurity Analyst', 'Security Engineer', 'Penetration Tester'],
        'match': 85,
        'why': 'Your interest in security and preference for stability suits cybersecurity well.',
        'next': ['Get CompTIA Security+', 'Learn networking basics', 'Practice CTF challenges'],
    },
    {
        'conditions': {'interest': 'management', 'risk': 'medium'},
        'careers': ['Product Manager', 'Engineering Manager', 'Tech Lead'],
        'match': 84,
        'why': 'Leadership instinct and balanced risk tolerance make PM a strong match.',
        'next': ['Learn product frameworks', 'Study user research', 'Build communication skills'],
    },
]

DEFAULT_RESULT = {
    'careers': ['Software Engineer', 'Product Manager', 'Data Analyst'],
    'match': 78,
    'why': 'Your balanced profile suits multiple tech roles. Explore each to find your best fit.',
    'next': ['Explore both technical and product paths', 'Build a side project', 'Talk to professionals in both fields'],
}


def suggest_path(interest: str, math_level: str, creativity: str, risk: str) -> dict:
    if not interest:
        return {'success': False, 'message': 'At least interest is required.'}

    interest_l = interest.strip().lower()
    math_l = (math_level or '').strip().lower()
    creativity_l = (creativity or '').strip().lower()
    risk_l = (risk or '').strip().lower()

    for rule in CAREER_MAP:
        cond = rule['conditions']
        match_count = 0
        total = len(cond)
        if cond.get('interest') and cond['interest'] in interest_l:
            match_count += 1
        if cond.get('math_level') and cond['math_level'] in math_l:
            match_count += 1
        if cond.get('creativity') and cond['creativity'] in creativity_l:
            match_count += 1
        if cond.get('risk') and cond['risk'] in risk_l:
            match_count += 1
        if match_count >= max(1, total - 1):
            return {
                'success': True,
                'suggested_careers': rule['careers'],
                'match_score': rule['match'],
                'why': rule['why'],
                'next_steps': rule['next'],
            }

    return {
        'success': True,
        'suggested_careers': DEFAULT_RESULT['careers'],
        'match_score': DEFAULT_RESULT['match'],
        'why': DEFAULT_RESULT['why'],
        'next_steps': DEFAULT_RESULT['next'],
    }
