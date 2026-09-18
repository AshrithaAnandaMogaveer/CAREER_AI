"""
Career Comparator Service
Returns structured side-by-side comparison of two careers.
"""

CAREER_DB = {
    'software engineer':         {'salary': '₹10–20 LPA', 'demand': 'Very High', 'growth': '22%', 'time': '2–4 years', 'difficulty': 'Medium',    'remote': 'Yes', 'diff_score': 60, 'demand_score': 90},
    'data scientist':            {'salary': '₹12–25 LPA', 'demand': 'High',      'growth': '35%', 'time': '3–5 years', 'difficulty': 'High',       'remote': 'Yes', 'diff_score': 80, 'demand_score': 85},
    'product manager':           {'salary': '₹15–30 LPA', 'demand': 'High',      'growth': '19%', 'time': '5–7 years', 'difficulty': 'High',       'remote': 'Partial', 'diff_score': 75, 'demand_score': 82},
    'ux designer':               {'salary': '₹8–18 LPA',  'demand': 'Medium',    'growth': '13%', 'time': '1–3 years', 'difficulty': 'Medium',     'remote': 'Yes', 'diff_score': 50, 'demand_score': 65},
    'devops engineer':           {'salary': '₹12–22 LPA', 'demand': 'Very High', 'growth': '25%', 'time': '3–5 years', 'difficulty': 'High',       'remote': 'Yes', 'diff_score': 78, 'demand_score': 88},
    'cybersecurity analyst':     {'salary': '₹10–22 LPA', 'demand': 'Very High', 'growth': '33%', 'time': '3–5 years', 'difficulty': 'High',       'remote': 'Partial', 'diff_score': 75, 'demand_score': 87},
    'machine learning engineer': {'salary': '₹14–28 LPA', 'demand': 'High',      'growth': '40%', 'time': '4–6 years', 'difficulty': 'Very High',  'remote': 'Yes', 'diff_score': 90, 'demand_score': 83},
    'full stack developer':      {'salary': '₹8–18 LPA',  'demand': 'High',      'growth': '20%', 'time': '2–3 years', 'difficulty': 'Medium',     'remote': 'Yes', 'diff_score': 55, 'demand_score': 80},
    'data analyst':              {'salary': '₹6–14 LPA',  'demand': 'High',      'growth': '23%', 'time': '1–3 years', 'difficulty': 'Medium',     'remote': 'Yes', 'diff_score': 52, 'demand_score': 82},
    'web development':           {'salary': '₹5–15 LPA',  'demand': 'High',      'growth': '18%', 'time': '1–2 years', 'difficulty': 'Low–Medium', 'remote': 'Yes', 'diff_score': 45, 'demand_score': 78},
    'data science':              {'salary': '₹12–25 LPA', 'demand': 'High',      'growth': '35%', 'time': '3–5 years', 'difficulty': 'High',       'remote': 'Yes', 'diff_score': 80, 'demand_score': 85},
    'ai engineer':               {'salary': '₹16–35 LPA', 'demand': 'Very High', 'growth': '45%', 'time': '4–6 years', 'difficulty': 'Very High',  'remote': 'Yes', 'diff_score': 92, 'demand_score': 90},
}

DEFAULT = {'salary': 'N/A', 'demand': 'N/A', 'growth': 'N/A', 'time': 'N/A', 'difficulty': 'N/A', 'remote': 'N/A', 'diff_score': 50, 'demand_score': 50}


def compare_careers(career_a: str, career_b: str) -> dict:
    if not career_a or not career_b:
        return {'success': False, 'message': 'Both careerA and careerB are required.'}

    if career_a.strip().lower() == career_b.strip().lower():
        return {'success': False, 'message': 'Please select two different careers.'}

    data_a = CAREER_DB.get(career_a.strip().lower(), DEFAULT)
    data_b = CAREER_DB.get(career_b.strip().lower(), DEFAULT)

    metrics = ['salary', 'demand', 'growth', 'time', 'difficulty', 'remote']

    # Build base reasoning
    reasoning = []
    if data_a['demand_score'] > data_b['demand_score']:
        reasoning.append(f"{career_a} has higher market demand ({data_a['demand']} vs {data_b['demand']})")
    elif data_b['demand_score'] > data_a['demand_score']:
        reasoning.append(f"{career_b} has higher market demand ({data_b['demand']} vs {data_a['demand']})")
    else:
        reasoning.append(f"Both careers have similar market demand")

    if data_a['diff_score'] < data_b['diff_score']:
        reasoning.append(f"{career_a} is easier to enter ({data_a['difficulty']} vs {data_b['difficulty']} difficulty)")
    elif data_b['diff_score'] < data_a['diff_score']:
        reasoning.append(f"{career_b} is easier to enter ({data_b['difficulty']} vs {data_a['difficulty']} difficulty)")

    reasoning.append(f"Salary range: {career_a} ({data_a['salary']}) vs {career_b} ({data_b['salary']})")
    reasoning.append(f"Growth rate: {career_a} ({data_a['growth']}) vs {career_b} ({data_b['growth']})")

    return {
        'success': True,
        'careerA': {'name': career_a, **{m: data_a[m] for m in metrics}, 'diff_score': data_a['diff_score'], 'demand_score': data_a['demand_score']},
        'careerB': {'name': career_b, **{m: data_b[m] for m in metrics}, 'diff_score': data_b['diff_score'], 'demand_score': data_b['demand_score']},
        'metrics': metrics,
        'reasoning': reasoning,
    }
