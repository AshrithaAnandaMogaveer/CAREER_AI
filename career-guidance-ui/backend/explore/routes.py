"""
Explore Module Routes
Flask Blueprint for all 5 Explore feature endpoints + personalization.
"""

from flask import Blueprint, request, jsonify
import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # backend root

from future_service import get_future_projection
from comparator_service import compare_careers
from roi_service import get_skill_roi
from confusion_service import suggest_path
from reality_service import get_reality_check
from user_profile_helper import (
    get_user_profile, compute_fit_score, get_missing_high_roi_skills, CAREER_SKILL_MAP
)

# Production utilities
utils_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils')
if utils_path not in sys.path:
    sys.path.insert(0, utils_path)

from utils.cache import cache_response
from utils.logger import log_request, log_error
from utils.validators import (
    validate_future, validate_compare, validate_roi,
    validate_reality, validate_path_suggest,
)

explore_bp = Blueprint('explore', __name__, url_prefix='/api/explore')


def _token_required_wrapper(f):
    """Inline token validation to avoid circular imports."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        import flask
        app = flask.current_app
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(' ')[1]
            except IndexError:
                return jsonify({'success': False, 'message': 'Invalid token format'}), 401
        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401
        try:
            import jwt
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user_id']
        except Exception:
            return jsonify({'success': False, 'message': 'Invalid or expired token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


# ─── PERSONALIZED SUMMARY ────────────────────────────────────────────────────

@explore_bp.route('/personalized-summary', methods=['GET'])
@_token_required_wrapper
@cache_response(ttl=300)
def personalized_summary(current_user):
    """GET /api/explore/personalized-summary — Career Snapshot for the user."""
    t0 = time.time()
    try:
        profile = get_user_profile(current_user)
        readiness = profile['readiness_score']
        target = profile['target_domain'] or 'Not set'
        missing = profile['missing_skills'][:5] if profile['missing_skills'] else []
        user_skills = profile['user_skills_raw']

        # Determine recommended focus from missing skills or target domain
        if missing:
            recommended_focus = missing[0]
        elif target and target.lower() in CAREER_SKILL_MAP:
            required = CAREER_SKILL_MAP[target.lower()]
            user_lower = profile['user_skills']
            gap = [s for s in required if s.lower() not in user_lower]
            recommended_focus = gap[0] if gap else (required[0] if required else 'Core Skills')
        else:
            recommended_focus = 'Core Skills'

        payload = {
            'success': True,
            'current_level': readiness,
            'target_role': target,
            'top_missing_skills': missing,
            'recommended_focus': recommended_focus,
            'user_skills': user_skills[:10],
            'has_analysis': profile['has_analysis'],
        }
        elapsed = (time.time() - t0) * 1000
        log_request(current_user, '/explore/personalized-summary', {}, 'success', elapsed)
        from flask import make_response
        resp = make_response(jsonify(payload), 200)
        resp.headers['X-Response-Time'] = f"{elapsed:.0f}ms"
        return resp
    except Exception as e:
        log_error(current_user, '/explore/personalized-summary', str(e))
        return jsonify({'success': False, 'message': str(e)}), 500


# ─── FUTURE SIMULATION ───────────────────────────────────────────────────────

@explore_bp.route('/future', methods=['POST'])
@_token_required_wrapper
@cache_response(ttl=300)
def future_projection(current_user):
    """POST /api/explore/future — Future You Simulation (personalized)."""
    t0 = time.time()
    try:
        data = request.get_json() or {}

        # Validate input
        ok, err = validate_future(data)
        if not ok:
            return jsonify(err), 400

        career = data.get('career', '')
        duration = int(data.get('duration', 6))

        result = get_future_projection(career, duration)
        if not result['success']:
            return jsonify(result), 400

        # Personalize: override base_readiness with real readiness if available
        profile = get_user_profile(current_user)
        if profile['readiness_score'] > 0:
            from future_service import CAREER_DATA, DEFAULT
            key = career.strip().lower()
            career_data = CAREER_DATA.get(key, DEFAULT)
            real_base = profile['readiness_score']
            personalized_score = min(round(real_base + career_data['learning_rate'] * duration), 98)
            result['future_readiness'] = personalized_score
            result['personalized'] = True
            result['base_readiness_used'] = real_base

            if personalized_score >= 85:
                result['message'] = f"Based on your profile, you'll be highly job-ready in {duration} months."
            elif personalized_score >= 70:
                result['message'] = f"Based on your profile, you'll be job-ready in {duration} months."
            else:
                result['message'] = f"Based on your profile, you'll have foundational skills in {duration} months. Keep building."

            # Personalize reasoning
            result['reasoning'] = [
                f"Based on your actual readiness score of {real_base}% from Analyze",
                f"Projected gain of {round(career_data['learning_rate'] * duration)}% over {duration} months with consistent learning",
                "Skill gap closure improves score progressively over time",
            ]
            if profile['missing_skills']:
                top_missing = profile['missing_skills'][:2]
                result['reasoning'].append(f"Closing gaps in {', '.join(top_missing)} will accelerate your progress")
            if personalized_score >= 85:
                result['reasoning'].append("You are on a strong trajectory — stay consistent")
            elif personalized_score < 60:
                result['reasoning'].append("Consider increasing study intensity or extending your timeline")
        else:
            result['personalized'] = False

        elapsed = (time.time() - t0) * 1000
        log_request(current_user, '/explore/future', {'career': career, 'duration': duration}, 'success', elapsed)
        from flask import make_response
        resp = make_response(jsonify(result), 200)
        resp.headers['X-Response-Time'] = f"{elapsed:.0f}ms"
        return resp
    except Exception as e:
        log_error(current_user, '/explore/future', str(e))
        return jsonify({'success': False, 'message': str(e)}), 500


# ─── CAREER COMPARATOR ───────────────────────────────────────────────────────

@explore_bp.route('/compare', methods=['POST'])
@_token_required_wrapper
@cache_response(ttl=300)
def compare(current_user):
    """POST /api/explore/compare — Career Comparator (with fit scores)."""
    t0 = time.time()
    try:
        data = request.get_json() or {}

        ok, err = validate_compare(data)
        if not ok:
            return jsonify(err), 400

        career_a = data.get('careerA', '')
        career_b = data.get('careerB', '')

        result = compare_careers(career_a, career_b)
        if not result['success']:
            return jsonify(result), 400

        # Add personalized fit scores + enrich reasoning
        profile = get_user_profile(current_user)
        user_skills = profile['user_skills']
        fit_a = compute_fit_score(career_a.strip().lower(), user_skills)
        fit_b = compute_fit_score(career_b.strip().lower(), user_skills)
        result['careerA']['fit_score'] = fit_a
        result['careerB']['fit_score'] = fit_b
        result['personalized'] = len(user_skills) > 0

        # Enrich reasoning with personalized context
        if user_skills:
            if fit_a > fit_b:
                result['reasoning'].insert(0, f"Your skills align better with {career_a} ({fit_a}% fit vs {fit_b}%)")
            elif fit_b > fit_a:
                result['reasoning'].insert(0, f"Your skills align better with {career_b} ({fit_b}% fit vs {fit_a}%)")
            else:
                result['reasoning'].insert(0, f"Your skills fit both careers equally ({fit_a}%)")

            # Check skill overlap
            from user_profile_helper import CAREER_SKILL_MAP
            req_a = [s.lower() for s in CAREER_SKILL_MAP.get(career_a.strip().lower(), [])]
            req_b = [s.lower() for s in CAREER_SKILL_MAP.get(career_b.strip().lower(), [])]
            overlap_a = [s for s in user_skills if any(s in r or r in s for r in req_a)]
            overlap_b = [s for s in user_skills if any(s in r or r in s for r in req_b)]
            if overlap_a:
                result['reasoning'].append(f"You already have relevant skills for {career_a}: {', '.join(overlap_a[:3])}")
            if overlap_b:
                result['reasoning'].append(f"You already have relevant skills for {career_b}: {', '.join(overlap_b[:3])}")

        elapsed = (time.time() - t0) * 1000
        log_request(current_user, '/explore/compare', {'careerA': career_a, 'careerB': career_b}, 'success', elapsed)
        from flask import make_response
        resp = make_response(jsonify(result), 200)
        resp.headers['X-Response-Time'] = f"{elapsed:.0f}ms"
        return resp
    except Exception as e:
        log_error(current_user, '/explore/compare', str(e))
        return jsonify({'success': False, 'message': str(e)}), 500


# ─── SKILL ROI ───────────────────────────────────────────────────────────────

@explore_bp.route('/roi', methods=['POST'])
@_token_required_wrapper
@cache_response(ttl=300)
def skill_roi(current_user):
    """POST /api/explore/roi — Skill ROI Analyzer (highlights missing skills)."""
    t0 = time.time()
    try:
        data = request.get_json() or {}

        ok, err = validate_roi(data)
        if not ok:
            return jsonify(err), 400

        skill = data.get('skill', '')

        result = get_skill_roi(skill)
        if not result['success']:
            return jsonify(result), 400

        # Flag if this skill is in the user's missing skills
        profile = get_user_profile(current_user)
        user_lower = profile['user_skills']
        missing_lower = [s.lower() for s in profile['missing_skills']]
        skill_lower = skill.strip().lower()

        result['you_have_this_skill'] = skill_lower in user_lower
        result['is_missing_skill'] = skill_lower in missing_lower
        result['high_priority'] = result['is_missing_skill'] and result.get('roi') in ('High', 'Very High')

        # Enrich reasoning with personalized context
        if skill_lower in missing_lower:
            result['reasoning'].insert(0, f"{skill} is identified as a gap in your Analyze profile")
        elif skill_lower in user_lower:
            result['reasoning'].insert(0, f"You already have {skill} — consider deepening expertise")

        # Suggest top missing high-ROI skills
        result['missing_high_roi'] = get_missing_high_roi_skills(
            profile['user_skills_raw'], profile['missing_skills']
        )

        elapsed = (time.time() - t0) * 1000
        log_request(current_user, '/explore/roi', {'skill': skill}, 'success', elapsed)
        from flask import make_response
        resp = make_response(jsonify(result), 200)
        resp.headers['X-Response-Time'] = f"{elapsed:.0f}ms"
        return resp
    except Exception as e:
        log_error(current_user, '/explore/roi', str(e))
        return jsonify({'success': False, 'message': str(e)}), 500


# ─── CONFUSION SOLVER ────────────────────────────────────────────────────────

@explore_bp.route('/path-suggest', methods=['POST'])
@_token_required_wrapper
@cache_response(ttl=300)
def path_suggest(current_user):
    """POST /api/explore/path-suggest — Confusion Solver (skill-aware)."""
    t0 = time.time()
    try:
        data = request.get_json() or {}

        ok, err = validate_path_suggest(data)
        if not ok:
            return jsonify(err), 400

        interest = data.get('interest', '')
        math_level = data.get('math_level', '')
        creativity = data.get('creativity', '')
        risk = data.get('risk', '')

        result = suggest_path(interest, math_level, creativity, risk)
        if not result['success']:
            return jsonify(result), 400

        # Re-rank suggested careers by user skill fit
        profile = get_user_profile(current_user)
        user_skills = profile['user_skills']

        if user_skills and result.get('suggested_careers'):
            scored = []
            for career in result['suggested_careers']:
                fit = compute_fit_score(career.strip().lower(), user_skills)
                scored.append((career, fit))
            scored.sort(key=lambda x: x[1], reverse=True)
            result['suggested_careers'] = [c for c, _ in scored]
            result['career_fit_scores'] = {c: f for c, f in scored}
            result['personalized'] = True
        else:
            result['personalized'] = False

        elapsed = (time.time() - t0) * 1000
        log_request(current_user, '/explore/path-suggest', {'interest': interest}, 'success', elapsed)
        from flask import make_response
        resp = make_response(jsonify(result), 200)
        resp.headers['X-Response-Time'] = f"{elapsed:.0f}ms"
        return resp
    except Exception as e:
        log_error(current_user, '/explore/path-suggest', str(e))
        return jsonify({'success': False, 'message': str(e)}), 500


# ─── REALITY CHECK ───────────────────────────────────────────────────────────

@explore_bp.route('/reality', methods=['GET'])
@_token_required_wrapper
@cache_response(ttl=300)
def reality_check(current_user):
    """GET /api/explore/reality?career=... — Reality Check (with user readiness)."""
    t0 = time.time()
    try:
        career = request.args.get('career', '')

        ok, err = validate_reality(career)
        if not ok:
            return jsonify(err), 400

        result = get_reality_check(career)
        if not result['success']:
            return jsonify(result), 400

        # Add user's current readiness for context
        profile = get_user_profile(current_user)
        result['your_readiness'] = profile['readiness_score']
        result['readiness_gap'] = max(0, result['diff_score'] - profile['readiness_score'])
        result['personalized'] = profile['readiness_score'] > 0

        elapsed = (time.time() - t0) * 1000
        log_request(current_user, '/explore/reality', {'career': career}, 'success', elapsed)
        from flask import make_response
        resp = make_response(jsonify(result), 200)
        resp.headers['X-Response-Time'] = f"{elapsed:.0f}ms"
        return resp
    except Exception as e:
        log_error(current_user, '/explore/reality', str(e))
        return jsonify({'success': False, 'message': str(e)}), 500


# ─── EVALUATION ──────────────────────────────────────────────────────────────

@explore_bp.route('/evaluation', methods=['GET'])
@_token_required_wrapper
def evaluation(current_user):
    """GET /api/explore/evaluation — Run recommendation logic on test dataset and return accuracy."""
    EVAL_DATASET = [
        {'skills': ['Python', 'Statistics', 'Machine Learning', 'SQL'],        'expected': 'data scientist'},
        {'skills': ['HTML', 'CSS', 'JavaScript', 'React'],                     'expected': 'full stack developer'},
        {'skills': ['Python', 'TensorFlow', 'Deep Learning', 'PyTorch'],       'expected': 'machine learning engineer'},
        {'skills': ['Figma', 'User Research', 'Prototyping', 'UI Design'],     'expected': 'ux designer'},
        {'skills': ['Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Linux'],          'expected': 'devops engineer'},
        {'skills': ['Network Security', 'Linux', 'Penetration Testing'],       'expected': 'cybersecurity analyst'},
        {'skills': ['React', 'Node.js', 'JavaScript', 'SQL', 'REST APIs'],     'expected': 'full stack developer'},
        {'skills': ['Python', 'SQL', 'Data Analysis', 'Tableau'],              'expected': 'data scientist'},
        {'skills': ['Product Strategy', 'Agile', 'User Research'],             'expected': 'product manager'},
        {'skills': ['Java', 'Spring Boot', 'SQL', 'Git', 'System Design'],     'expected': 'software engineer'},
    ]

    results = []
    correct = 0

    for item in EVAL_DATASET:
        user_skills_lower = [s.lower() for s in item['skills']]
        # Score each career by skill overlap
        scores = {}
        for career_key, required in CAREER_SKILL_MAP.items():
            req_lower = [r.lower() for r in required]
            overlap = sum(1 for s in user_skills_lower if any(s in r or r in s for r in req_lower))
            scores[career_key] = overlap / len(req_lower) if req_lower else 0

        predicted = max(scores, key=scores.get) if scores else 'unknown'
        is_correct = predicted == item['expected']
        if is_correct:
            correct += 1

        results.append({
            'skills': item['skills'],
            'expected': item['expected'],
            'predicted': predicted,
            'correct': is_correct,
            'confidence': round(scores.get(predicted, 0) * 100),
        })

    accuracy = round(correct / len(EVAL_DATASET), 2)

    return jsonify({
        'success': True,
        'accuracy': accuracy,
        'accuracy_pct': f"{int(accuracy * 100)}%",
        'correct': correct,
        'total': len(EVAL_DATASET),
        'results': results,
    }), 200
