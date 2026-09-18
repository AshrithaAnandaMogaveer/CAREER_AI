"""
Input validators for Explore endpoints.
Each returns (True, None) on success or (False, error_dict) on failure.
"""


def validate_future(data: dict):
    career = (data.get('career') or '').strip()
    if not career:
        return False, {'error': 'Invalid input', 'message': 'Career path must not be empty'}
    try:
        duration = int(data.get('duration', 6))
    except (ValueError, TypeError):
        return False, {'error': 'Invalid input', 'message': 'Duration must be a number'}
    if not (1 <= duration <= 12):
        return False, {'error': 'Invalid input', 'message': 'Duration must be between 1 and 12 months'}
    return True, None


def validate_compare(data: dict):
    career_a = (data.get('careerA') or '').strip()
    career_b = (data.get('careerB') or '').strip()
    if not career_a or not career_b:
        return False, {'error': 'Invalid input', 'message': 'Both career paths must be selected'}
    if career_a.lower() == career_b.lower():
        return False, {'error': 'Invalid input', 'message': 'Career A and Career B must be different'}
    return True, None


def validate_roi(data: dict):
    skill = (data.get('skill') or '').strip()
    if not skill:
        return False, {'error': 'Invalid input', 'message': 'Skill must not be empty'}
    return True, None


def validate_reality(career: str):
    if not (career or '').strip():
        return False, {'error': 'Invalid input', 'message': 'Career must not be empty'}
    return True, None


def validate_path_suggest(data: dict):
    interest = (data.get('interest') or '').strip()
    if not interest:
        return False, {'error': 'Invalid input', 'message': 'Interest field must not be empty'}
    return True, None
