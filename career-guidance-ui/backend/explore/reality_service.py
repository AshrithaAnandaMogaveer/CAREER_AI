"""
Reality Check Engine Service
Returns honest difficulty/effort/competition data for a career.
"""

REALITY_DB = {
    'software engineer':         {'difficulty': 'Medium',    'learning_time': '2–4 years',  'competition': 'High',      'effort': 'High',      'verdict': 'Achievable with consistent practice', 'diff_score': 60, 'comp_score': 75, 'effort_score': 70},
    'data scientist':            {'difficulty': 'High',      'learning_time': '3–5 years',  'competition': 'Very High', 'effort': 'Very High', 'verdict': 'Requires strong math & programming foundation', 'diff_score': 80, 'comp_score': 85, 'effort_score': 85},
    'product manager':           {'difficulty': 'High',      'learning_time': '5–8 years',  'competition': 'Very High', 'effort': 'High',      'verdict': 'Usually requires prior engineering or business experience', 'diff_score': 75, 'comp_score': 88, 'effort_score': 72},
    'ux designer':               {'difficulty': 'Medium',    'learning_time': '1–3 years',  'competition': 'Medium',    'effort': 'Medium',    'verdict': 'Portfolio-driven — start building projects now', 'diff_score': 50, 'comp_score': 55, 'effort_score': 55},
    'devops engineer':           {'difficulty': 'High',      'learning_time': '3–5 years',  'competition': 'High',      'effort': 'Very High', 'verdict': 'Hands-on lab practice is essential', 'diff_score': 78, 'comp_score': 72, 'effort_score': 82},
    'cybersecurity analyst':     {'difficulty': 'High',      'learning_time': '3–5 years',  'competition': 'Medium',    'effort': 'High',      'verdict': 'Certifications (CEH, CISSP) significantly boost entry', 'diff_score': 75, 'comp_score': 60, 'effort_score': 78},
    'machine learning engineer': {'difficulty': 'Very High', 'learning_time': '4–6 years',  'competition': 'High',      'effort': 'Very High', 'verdict': 'Requires deep math, coding, and research skills', 'diff_score': 90, 'comp_score': 78, 'effort_score': 90},
    'full stack developer':      {'difficulty': 'Medium',    'learning_time': '2–3 years',  'competition': 'High',      'effort': 'High',      'verdict': 'One of the most accessible high-paying paths', 'diff_score': 55, 'comp_score': 72, 'effort_score': 68},
    'ai engineer':               {'difficulty': 'Very High', 'learning_time': '4–6 years',  'competition': 'Very High', 'effort': 'Very High', 'verdict': 'Cutting-edge field — requires research mindset and strong fundamentals', 'diff_score': 92, 'comp_score': 88, 'effort_score': 92},
    'data analyst':              {'difficulty': 'Medium',    'learning_time': '1–2 years',  'competition': 'High',      'effort': 'Medium',    'verdict': 'Great entry point into data careers with SQL and Excel', 'diff_score': 52, 'comp_score': 70, 'effort_score': 58},
    'web development':           {'difficulty': 'Low–Medium','learning_time': '1–2 years',  'competition': 'High',      'effort': 'Medium',    'verdict': 'Highly accessible — strong portfolio matters most', 'diff_score': 45, 'comp_score': 72, 'effort_score': 55},
    'data science':              {'difficulty': 'High',      'learning_time': '3–5 years',  'competition': 'Very High', 'effort': 'Very High', 'verdict': 'Requires strong math & programming foundation', 'diff_score': 80, 'comp_score': 85, 'effort_score': 85},
}

DEFAULT = {'difficulty': 'Medium', 'learning_time': '2–4 years', 'competition': 'High', 'effort': 'High', 'verdict': 'Requires consistent effort and hands-on practice.', 'diff_score': 60, 'comp_score': 70, 'effort_score': 65}


def get_reality_check(career: str) -> dict:
    if not career:
        return {'success': False, 'message': 'Career parameter is required.'}

    key = career.strip().lower()
    data = REALITY_DB.get(key, DEFAULT)

    reasoning = [
        f"Difficulty rated {data['difficulty']} based on required technical depth",
        f"Typical time to proficiency is {data['learning_time']}",
        f"Job market competition is {data['competition']} in this domain",
        f"Sustained effort level required: {data['effort']}",
    ]
    if data['diff_score'] >= 80:
        reasoning.append("Requires advanced mathematics and strong programming fundamentals")
    if data['comp_score'] >= 80:
        reasoning.append("High competition — portfolio and projects are critical differentiators")
    if data['effort_score'] >= 80:
        reasoning.append("Long-term consistency is essential; burnout risk is real without a plan")

    return {
        'success': True,
        'career': career,
        'difficulty': data['difficulty'],
        'learning_time': data['learning_time'],
        'competition': data['competition'],
        'effort': data['effort'],
        'verdict': data['verdict'],
        'diff_score': data['diff_score'],
        'comp_score': data['comp_score'],
        'effort_score': data['effort_score'],
        'reasoning': reasoning,
    }
