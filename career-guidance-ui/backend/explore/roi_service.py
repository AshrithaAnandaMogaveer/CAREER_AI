"""
Skill ROI Analyzer Service
Calculates return on investment for learning a skill.
"""

SKILL_DB = {
    'react':            {'career_impact': 8.5, 'learning_effort': 5.0, 'salary_boost': '+₹2–4 LPA', 'time_to_learn': '3–4 months', 'demand': 92, 'impact_score': 85},
    'python':           {'career_impact': 9.5, 'learning_effort': 4.0, 'salary_boost': '+₹3–6 LPA', 'time_to_learn': '2–3 months', 'demand': 95, 'impact_score': 90},
    'machine learning': {'career_impact': 9.8, 'learning_effort': 8.0, 'salary_boost': '+₹5–10 LPA','time_to_learn': '6–9 months', 'demand': 88, 'impact_score': 95},
    'aws':              {'career_impact': 9.0, 'learning_effort': 6.0, 'salary_boost': '+₹3–7 LPA', 'time_to_learn': '4–6 months', 'demand': 90, 'impact_score': 88},
    'docker':           {'career_impact': 8.0, 'learning_effort': 4.0, 'salary_boost': '+₹2–5 LPA', 'time_to_learn': '1–2 months', 'demand': 85, 'impact_score': 80},
    'typescript':       {'career_impact': 7.5, 'learning_effort': 3.5, 'salary_boost': '+₹1–3 LPA', 'time_to_learn': '1–2 months', 'demand': 80, 'impact_score': 75},
    'sql':              {'career_impact': 8.2, 'learning_effort': 3.5, 'salary_boost': '+₹2–4 LPA', 'time_to_learn': '2–3 months', 'demand': 88, 'impact_score': 82},
    'kubernetes':       {'career_impact': 9.2, 'learning_effort': 7.5, 'salary_boost': '+₹4–8 LPA', 'time_to_learn': '4–6 months', 'demand': 82, 'impact_score': 88},
    'system design':    {'career_impact': 9.8, 'learning_effort': 8.5, 'salary_boost': '+₹5–12 LPA','time_to_learn': '6–12 months','demand': 85, 'impact_score': 95},
    'data analysis':    {'career_impact': 8.3, 'learning_effort': 5.5, 'salary_boost': '+₹2–5 LPA', 'time_to_learn': '3–4 months', 'demand': 87, 'impact_score': 83},
}

DEFAULT = {'career_impact': 7.0, 'learning_effort': 5.0, 'salary_boost': '+₹1–3 LPA', 'time_to_learn': '3–6 months', 'demand': 75, 'impact_score': 70}

EFFORT_LABELS = {(0, 4): 'Low', (4, 6.5): 'Medium', (6.5, 10): 'High'}
ROI_LABELS = {(0, 1.2): 'Low', (1.2, 1.6): 'Medium', (1.6, 2.0): 'High', (2.0, 99): 'Very High'}


def _label(value, mapping):
    for (lo, hi), label in mapping.items():
        if lo <= value < hi:
            return label
    return 'Medium'


def get_skill_roi(skill: str) -> dict:
    if not skill:
        return {'success': False, 'message': 'Skill is required.'}

    key = skill.strip().lower()
    data = SKILL_DB.get(key, DEFAULT)

    roi_score = round(data['career_impact'] / data['learning_effort'], 2)
    effort_label = _label(data['learning_effort'], EFFORT_LABELS)
    roi_label = _label(roi_score, ROI_LABELS)

    reasoning = [
        f"Market demand is {data['demand']}% — {'high' if data['demand'] >= 85 else 'moderate'} industry adoption",
        f"Learning effort is {effort_label.lower()} ({data['time_to_learn']} to proficiency)",
        f"Career impact score of {data['impact_score']}% relative to other skills",
        f"Salary boost potential: {data['salary_boost']}",
    ]
    if roi_label in ('High', 'Very High'):
        reasoning.append("Strong ROI — high impact relative to the learning investment required")
    if effort_label == 'Low':
        reasoning.append("Low barrier to entry makes this an efficient skill to acquire quickly")
    if data['demand'] >= 90:
        reasoning.append("Consistently in top demanded skills across job postings")

    return {
        'success': True,
        'skill': skill,
        'roi_score': roi_score,
        'roi': roi_label,
        'impact': 'Very High' if data['impact_score'] >= 90 else ('High' if data['impact_score'] >= 80 else 'Medium'),
        'effort': effort_label,
        'salary_boost': data['salary_boost'],
        'time_to_learn': data['time_to_learn'],
        'demand': data['demand'],
        'impact_score': data['impact_score'],
        'reasoning': reasoning,
    }
