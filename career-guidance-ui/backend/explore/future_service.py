"""
Future You Simulation Service
Calculates projected career readiness based on career and duration.
"""

CAREER_DATA = {
    'software engineer':        {'base_readiness': 45, 'learning_rate': 5.5, 'roles': {6: 'Junior Software Engineer', 12: 'Software Engineer'}},
    'data scientist':           {'base_readiness': 40, 'learning_rate': 5.0, 'roles': {6: 'Junior Data Scientist',    12: 'Data Scientist'}},
    'machine learning engineer':{'base_readiness': 35, 'learning_rate': 4.5, 'roles': {6: 'ML Intern / Researcher',   12: 'Junior ML Engineer'}},
    'product manager':          {'base_readiness': 38, 'learning_rate': 4.8, 'roles': {6: 'Associate PM',             12: 'Product Manager'}},
    'ux designer':              {'base_readiness': 50, 'learning_rate': 6.0, 'roles': {6: 'Junior UX Designer',       12: 'UX Designer'}},
    'devops engineer':          {'base_readiness': 38, 'learning_rate': 5.0, 'roles': {6: 'Junior DevOps Engineer',   12: 'DevOps Engineer'}},
    'cybersecurity analyst':    {'base_readiness': 36, 'learning_rate': 4.8, 'roles': {6: 'Security Analyst Trainee', 12: 'Cybersecurity Analyst'}},
    'full stack developer':     {'base_readiness': 48, 'learning_rate': 5.8, 'roles': {6: 'Junior Full Stack Dev',    12: 'Full Stack Developer'}},
}

DEFAULT = {'base_readiness': 40, 'learning_rate': 5.0, 'roles': {6: 'Junior Professional', 12: 'Mid-level Professional'}}


def get_future_projection(career: str, duration: int) -> dict:
    """
    Calculate future readiness score and expected role.
    formula: future_score = base_readiness + (learning_rate × duration)
    Capped at 98.
    """
    if not career or duration not in (6, 12):
        return {'success': False, 'message': 'Invalid input. Provide career and duration (6 or 12).'}

    key = career.strip().lower()
    data = CAREER_DATA.get(key, DEFAULT)

    future_score = min(round(data['base_readiness'] + data['learning_rate'] * duration), 98)
    role = data['roles'].get(duration, 'Professional')

    if future_score >= 85:
        message = f"You will be highly job-ready in {duration} months with strong fundamentals."
    elif future_score >= 70:
        message = f"You will be job-ready in {duration} months. Keep consistent practice."
    else:
        message = f"You will have foundational skills in {duration} months. More time may be needed."

    reasoning = [
        f"Starting readiness of {data['base_readiness']}% for {career}",
        f"Learning rate of {data['learning_rate']} points/month assumed with consistent effort",
        f"Projected gain of {round(data['learning_rate'] * duration)}% over {duration} months",
        "Skill gap closure improves score progressively over time",
    ]
    if future_score >= 85:
        reasoning.append("Strong trajectory — you are on track for a senior role")
    elif future_score < 60:
        reasoning.append("Consider extending your timeline or increasing study intensity")

    return {
        'success': True,
        'future_readiness': future_score,
        'expected_role': role,
        'message': message,
        'career': career,
        'duration': duration,
        'reasoning': reasoning,
    }
