"""
Flask CORS Configuration with Database Integration
Main Flask backend with SQLAlchemy database support
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt
import datetime
from functools import wraps
import os
import sys

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import database models and services
from community_models import db
from user_model import User
from community_service import CommunityService

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Database configuration
db_path = os.path.join(backend_path, 'career_guidance.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{db_path}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    from community_models import (
        Community, CommunityMember, Post, Comment, Like,
        Conversation, Message, Notification, UserProfile
    )
    db.create_all()
    print(f"✓ Database initialized: {app.config['SQLALCHEMY_DATABASE_URI']}")

# CORS Configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Decorator to require authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer TOKEN
            except IndexError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid token format'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token is missing'
            }), 401
        
        try:
            # Decode JWT token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user_id']  # Get user from token
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Token has expired'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Invalid token'
            }), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated


# Example API Endpoints

@app.route('/api/signup', methods=['POST'])
def signup():
    """
    User signup endpoint
    Expected JSON: {name, email, password, domain}
    Returns: {success, token, user}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'domain']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        name = data['name']
        email = data['email'].lower().strip()
        password = data['password']
        domain = data['domain']
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email, is_deleted=False).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 400
        
        # Create new user
        user = User(name=name, email=email, domain=domain)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            'success': True,
            'token': token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/login', methods=['POST'])
def login():
    """
    User login endpoint
    Expected JSON: {email, password}
    Returns: {success, token, user}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'email' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Find user by email
        user = User.query.filter_by(email=email, is_deleted=False, is_active=True).first()
        
        if not user or not user.check_password(password):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Update last login
        user.last_login = datetime.datetime.utcnow()
        db.session.commit()
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            'success': True,
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """
    Get user profile (protected route)
    Requires: Authorization header with Bearer token
    Returns: {success, user}
    """
    try:
        # Get user from database
        user = User.query.get(current_user)
        
        if not user or user.is_deleted or not user.is_active:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/analyze-resume', methods=['POST'])
@token_required
def analyze_resume_comprehensive(current_user):
    """
    Comprehensive resume analysis with NLP and PDF generation
    Requires: Authorization header with Bearer token
    Accepts: multipart/form-data with optional 'resume' file and JSON data
    Returns: Complete analysis with download link
    """
    try:
        import sys
        import os
        # Add backend directory to Python path
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        from resumeAnalyzer import ResumeAnalyzer
        from skillEngine import SkillEngine
        from reportGenerator import ReportGenerator
        from io import BytesIO
        import base64
        
        # Initialize analyzers
        resume_analyzer = ResumeAnalyzer()
        skill_engine = SkillEngine()
        report_generator = ReportGenerator()
        
        # Get form data
        current_domain = request.form.get('currentDomain', '')
        target_domain = request.form.get('targetDomain', 'Software Development')
        experience_years = int(request.form.get('experienceYears', 0))
        manual_skills = request.form.get('manualSkills', '')
        project_descriptions = request.form.get('projectDescriptions', '')
        certifications = request.form.get('certifications', '')
        strength_level = request.form.get('strengthLevel', 'Intermediate')
        
        # Parse manual inputs
        manual_skills_list = [s.strip() for s in manual_skills.split(',') if s.strip()] if manual_skills else []
        manual_projects = [p.strip() for p in project_descriptions.split('\n') if p.strip()] if project_descriptions else []
        manual_certs = [c.strip() for c in certifications.split(',') if c.strip()] if certifications else []
        
        # Initialize variables
        resume_data = None
        extracted_skills = []
        resume_text = ""
        
        # Process resume if uploaded
        if 'resume' in request.files:
            file = request.files['resume']
            if file and file.filename:
                # Read file into BytesIO
                file_stream = BytesIO(file.read())
                
                # Analyze resume
                resume_data = resume_analyzer.analyze_resume(file_stream, file.filename)
                extracted_skills = resume_data['extracted_skills']
                resume_text = resume_data['cleaned_text']
        
        # Merge skills from resume and manual entry
        all_skills = skill_engine.merge_skills(extracted_skills, manual_skills_list)
        user_skills_set = skill_engine.normalize_skills(all_skills)
        
        # Merge projects and certifications
        all_projects = (resume_data['projects'] if resume_data else []) + manual_projects
        all_certs = (resume_data['certifications'] if resume_data else []) + manual_certs
        
        # Calculate readiness score
        readiness_score = skill_engine.calculate_readiness_score(
            user_skills_set,
            target_domain,
            experience_years,
            len(all_projects) > 0,
            len(all_certs) > 0
        )
        
        # Identify missing skills
        missing_skills = skill_engine.identify_missing_skills(user_skills_set, target_domain)
        
        # Calculate resume strength
        resume_strength = skill_engine.calculate_resume_strength(
            resume_text if resume_text else manual_skills + project_descriptions,
            all_skills,
            all_projects,
            all_certs,
            experience_years
        )
        
        # Detect mistakes
        mistakes = skill_engine.detect_mistakes(
            resume_text if resume_text else manual_skills + project_descriptions,
            all_projects
        )
        
        # Generate suggestions
        suggestions = skill_engine.generate_suggestions(
            readiness_score['total_score'],
            missing_skills,
            resume_strength,
            mistakes
        )
        
        # Suggest domains
        suggested_domains = skill_engine.suggest_domains(user_skills_set, top_n=5)
        
        # Prepare analysis data
        analysis_data = {
            'extracted_skills': all_skills,
            'readiness_score': readiness_score,
            'resume_strength': resume_strength,
            'missing_skills': missing_skills,
            'mistakes': mistakes,
            'suggestions': suggestions,
            'suggested_domains': suggested_domains,
            'experience_years': experience_years,
            'projects_count': len(all_projects),
            'certifications_count': len(all_certs),
        }
        
        # Generate PDF report
        user_info = {
            'name': 'User',  # TODO: Get from database
            'domain': target_domain,
        }
        
        pdf_buffer = report_generator.generate_report(analysis_data, user_info)
        pdf_base64 = base64.b64encode(pdf_buffer.read()).decode('utf-8')
        
        # Return comprehensive response
        return jsonify({
            'success': True,
            'analysis': {
                'extracted_skills': all_skills,
                'total_skills': len(all_skills),
                'readiness_score': readiness_score['total_score'],
                'readiness_details': readiness_score,
                'resume_strength': resume_strength['total_strength'],
                'resume_strength_details': resume_strength,
                'confidence_level': readiness_score['confidence_level'],
                'missing_skills': missing_skills,
                'mistakes': mistakes,
                'suggestions': suggestions,
                'suggested_domains': suggested_domains,
                'experience_years': experience_years,
                'projects_count': len(all_projects),
                'certifications_count': len(all_certs),
            },
            'pdf_report': pdf_base64,
        }), 200
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': f'Analysis failed: {str(e)}'
        }), 500


@app.route('/api/analyze/upload', methods=['POST'])
@token_required
def analyze_upload(current_user):
    """
    Legacy endpoint - redirects to comprehensive analysis
    """
    return analyze_resume_comprehensive(current_user)


@app.route('/api/analyze/manual', methods=['POST'])
@token_required
def analyze_manual(current_user):
    """
    Analyze manually entered skills
    Requires: Authorization header with Bearer token
    Accepts: {skills: string, domain: string}
    Returns: {success, extracted_skills, readiness_score, suggested_domains, missing_skills}
    """
    try:
        data = request.get_json()
        
        if 'skills' not in data or 'domain' not in data:
            return jsonify({
                'success': False,
                'message': 'Skills and domain are required'
            }), 400
        
        skills_text = data['skills']
        domain = data['domain']
        
        # TODO: Process the manual input
        # 1. Parse skills from text
        # 2. Match against domain requirements
        # 3. Calculate readiness score
        # 4. Suggest related domains
        # 5. Identify skill gaps
        
        # Mock response (replace with actual analysis)
        # Parse skills from comma-separated text
        entered_skills = [s.strip() for s in skills_text.split(',') if s.strip()]
        
        return jsonify({
            'success': True,
            'extracted_skills': entered_skills,
            'readiness_score': 68,
            'suggested_domains': [
                domain,
                'Related Domain 1',
                'Related Domain 2'
            ],
            'missing_skills': [
                'Advanced Skill 1',
                'Advanced Skill 2',
                'Industry Tool 1',
                'Best Practice 1'
            ]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/postmatrics/after10th', methods=['GET'])
@token_required
def get_after10th_guidance(current_user):
    """
    Get After 10th guidance recommendations
    Requires: Authorization header with Bearer token
    Returns: {success, streams}
    """
    try:
        # TODO: Implement weighted interest matching algorithm
        # 1. Get user's interests and strengths
        # 2. Calculate stream recommendation scores
        # 3. Return top 3 stream paths with reasoning
        
        # Mock response (replace with actual algorithm)
        return jsonify({
            'success': True,
            'streams': [
                {
                    'id': 'science',
                    'name': 'Science Stream (PCM/PCB)',
                    'description': 'Perfect for students interested in engineering, medicine, and research',
                    'score': 85,
                    'requirements': ['Strong analytical skills', 'Interest in problem-solving'],
                    'prospects': 'High demand in tech and healthcare sectors',
                    'reasoning': 'Based on your strong performance in mathematics and science subjects'
                },
                {
                    'id': 'commerce',
                    'name': 'Commerce Stream',
                    'description': 'Ideal for careers in business, finance, and accounting',
                    'score': 75,
                    'requirements': ['Good with numbers', 'Interest in economics'],
                    'prospects': 'Growing opportunities in finance and business',
                    'reasoning': 'Your interest in economics and business aligns well with this stream'
                },
                {
                    'id': 'arts',
                    'name': 'Arts/Humanities Stream',
                    'description': 'Best for creative minds interested in social sciences and languages',
                    'score': 70,
                    'requirements': ['Creative thinking', 'Good communication skills'],
                    'prospects': 'Diverse career options in media, education, and civil services',
                    'reasoning': 'Your creative abilities and communication skills are strong'
                }
            ]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/postmatrics/after12th', methods=['POST'])
@token_required
def analyze_after12th(current_user):
    """
    Analyze After 12th career options
    Requires: Authorization header with Bearer token
    Accepts: {stream, budget, interests, etc.}
    Returns: {success, careers}
    """
    try:
        data = request.get_json()
        
        # TODO: Implement eligibility mapping and feasibility scoring
        # 1. Match stream to eligible degrees
        # 2. Filter by budget constraints
        # 3. Calculate feasibility scores
        # 4. Estimate ROI
        
        # Mock response (replace with actual algorithm)
        return jsonify({
            'success': True,
            'careers': [
                {
                    'career': 'Software Engineering',
                    'description': 'Design and develop software applications',
                    'score': 88,
                    'demand': 95,
                    'salary': '₹6-15 LPA',
                    'matchedSkills': 7,
                    'totalRequired': 10,
                    'missingSkills': ['System Design', 'Cloud Computing', 'DevOps'],
                    'feasibilityScore': 85
                },
                {
                    'career': 'Data Science',
                    'description': 'Analyze data to derive insights and build ML models',
                    'score': 82,
                    'demand': 90,
                    'salary': '₹7-18 LPA',
                    'matchedSkills': 6,
                    'totalRequired': 10,
                    'missingSkills': ['Machine Learning', 'Statistics', 'Big Data', 'Python'],
                    'feasibilityScore': 78
                }
            ]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/postmatrics/exams', methods=['GET'])
@token_required
def get_competitive_exams(current_user):
    """
    Get competitive exams list
    Requires: Authorization header with Bearer token
    Returns: {success, exams}
    """
    try:
        # TODO: Implement exam eligibility filter and difficulty-weighted ranking
        # 1. Filter exams by education level
        # 2. Match time availability
        # 3. Rank by difficulty tolerance
        
        # Mock response (replace with actual algorithm)
        return jsonify({
            'success': True,
            'exams': [
                {
                    'id': 'jee',
                    'name': 'JEE Main',
                    'fullName': 'Joint Entrance Examination',
                    'difficulty': 'Hard',
                    'eligibility': '12th with PCM',
                    'frequency': 'Twice a year',
                    'duration': '3 hours',
                    'careers': ['Engineering', 'Architecture', 'Technology']
                },
                {
                    'id': 'neet',
                    'name': 'NEET',
                    'fullName': 'National Eligibility cum Entrance Test',
                    'difficulty': 'Hard',
                    'eligibility': '12th with PCB',
                    'frequency': 'Once a year',
                    'duration': '3 hours',
                    'careers': ['Medicine', 'Dentistry', 'Veterinary']
                },
                {
                    'id': 'cat',
                    'name': 'CAT',
                    'fullName': 'Common Admission Test',
                    'difficulty': 'Medium',
                    'eligibility': 'Graduate',
                    'frequency': 'Once a year',
                    'duration': '3 hours',
                    'careers': ['MBA', 'Management', 'Business']
                }
            ]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/postmatrics/skills', methods=['GET'])
@token_required
def get_skill_based_careers(current_user):
    """
    Get skill-based careers
    Requires: Authorization header with Bearer token
    Returns: {success, careers}
    """
    try:
        # TODO: Implement skill accessibility scoring
        # 1. Calculate cost-to-entry scores
        # 2. Rank by income potential
        # 3. Consider internet access and investment capability
        
        # Mock response (replace with actual algorithm)
        return jsonify({
            'success': True,
            'careers': [
                {
                    'career': 'Web Development',
                    'description': 'Build websites and web applications',
                    'score': 90,
                    'demand': 92,
                    'salary': '₹4-12 LPA',
                    'matchedSkills': 5,
                    'totalRequired': 8,
                    'missingSkills': ['React', 'Node.js', 'Database'],
                    'feasibilityScore': 88
                },
                {
                    'career': 'Digital Marketing',
                    'description': 'Promote products and services online',
                    'score': 85,
                    'demand': 88,
                    'salary': '₹3-10 LPA',
                    'matchedSkills': 6,
                    'totalRequired': 8,
                    'missingSkills': ['SEO', 'Analytics'],
                    'feasibilityScore': 90
                },
                {
                    'career': 'Graphic Design',
                    'description': 'Create visual content for brands and media',
                    'score': 80,
                    'demand': 85,
                    'salary': '₹3-8 LPA',
                    'matchedSkills': 4,
                    'totalRequired': 7,
                    'missingSkills': ['Adobe Suite', 'UI/UX', 'Branding'],
                    'feasibilityScore': 82
                }
            ]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/postmatrics/scholarships', methods=['GET'])
@token_required
def get_scholarships(current_user):
    """
    Get scholarships
    Requires: Authorization header with Bearer token
    Returns: {success, scholarships}
    """
    try:
        # TODO: Implement eligibility filtering
        # 1. Filter by income range
        # 2. Filter by category
        # 3. Filter by education level
        # 4. Rank by benefit amount
        
        # Mock response (replace with actual algorithm)
        return jsonify({
            'success': True,
            'scholarships': [
                {
                    'id': 'merit',
                    'name': 'National Merit Scholarship',
                    'provider': 'Government of India',
                    'amount': '50,000',
                    'eligibility': 'Class 12 with 85%+ marks',
                    'category': 'Merit-based',
                    'income': 'Below ₹6 LPA',
                    'deadline': 'March 31, 2026'
                },
                {
                    'id': 'minority',
                    'name': 'Minority Scholarship',
                    'provider': 'Ministry of Minority Affairs',
                    'amount': '30,000',
                    'eligibility': 'Class 10 passed',
                    'category': 'Minority communities',
                    'income': 'Below ₹2.5 LPA',
                    'deadline': 'April 15, 2026'
                },
                {
                    'id': 'scst',
                    'name': 'SC/ST Scholarship',
                    'provider': 'Ministry of Social Justice',
                    'amount': '40,000',
                    'eligibility': 'Class 10 passed',
                    'category': 'SC/ST',
                    'income': 'Below ₹2.5 LPA',
                    'deadline': 'April 30, 2026'
                }
            ]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/postmatrics/interest-test', methods=['POST'])
@token_required
def submit_interest_test(current_user):
    """
    Submit interest assessment test
    Requires: Authorization header with Bearer token
    Accepts: {answers: object}
    Returns: {success, results}
    """
    try:
        data = request.get_json()
        
        if 'answers' not in data:
            return jsonify({
                'success': False,
                'message': 'Answers are required'
            }), 400
        
        answers = data['answers']
        
        # TODO: Implement scoring algorithm
        # 1. Calculate cluster scores
        # 2. Normalize to percentages
        # 3. Map to career clusters
        # 4. Return top 3 recommendations
        
        # Mock response (replace with actual algorithm)
        return jsonify({
            'success': True,
            'results': [
                {
                    'cluster': 'Technical',
                    'score': 85,
                    'careers': ['Software Engineer', 'Data Scientist', 'IT Specialist']
                },
                {
                    'cluster': 'Analytical',
                    'score': 78,
                    'careers': ['Financial Analyst', 'Research Scientist', 'Statistician']
                },
                {
                    'cluster': 'Creative',
                    'score': 72,
                    'careers': ['Graphic Designer', 'Content Creator', 'Architect']
                }
            ]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# Global progress manager instance (shared across requests)
_progress_manager_instance = None

def get_progress_manager():
    """Get or create global progress manager instance"""
    global _progress_manager_instance
    if _progress_manager_instance is None:
        import os
        import sys
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        from progressManager import ProgressManager
        _progress_manager_instance = ProgressManager()
    return _progress_manager_instance


@app.route('/api/routine/evolution', methods=['GET', 'POST'])
@token_required
def get_routine_evolution(current_user):
    """
    Get evolution data with daily/monthly progress and excellence metrics
    
    Requires: Authorization header with Bearer token
    Query Parameters:
        - routineData: JSON string of routine data (optional)
    Returns: {
        success,
        dailyGraphData,
        monthlyGraphData,
        excellenceLevel,
        remainingSkills,
        motivationMessage,
        metrics
    }
    """
    try:
        import os
        import sys
        
        # Import backend modules
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        from evolutionTracker import EvolutionTracker
        
        # Get routine data from query params or request body
        routine_data = None
        if request.method == 'GET' and request.args.get('routineData'):
            try:
                routine_data = json.loads(request.args.get('routineData'))
            except:
                pass
        elif request.method == 'POST':
            data = request.get_json(silent=True)
            if data:
                routine_data = data.get('routineData')
        
        # Use shared progress manager
        manager = get_progress_manager()
        tracker = EvolutionTracker(manager)
        
        # Compute evolution
        result = tracker.compute_evolution(current_user, routine_data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Evolution data fetch failed: {str(e)}'
        }), 500


@app.route('/api/routine/progress', methods=['POST'])
@token_required
def update_routine_progress(current_user):
    """
    Update skill progress and recalculate metrics
    
    Requires: Authorization header with Bearer token
    Accepts: {
        week: int,
        skill: string,
        completionPercentage: float (0-100),
        date: string (ISO format),
        routineData: object
    }
    Returns: {success, progress_metrics, skill_progress}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['week', 'skill', 'completionPercentage', 'date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        week = data['week']
        skill = data['skill']
        completion_percentage = data['completionPercentage']
        date = data['date']
        routine_data = data.get('routineData', None)
        
        # Validate types
        if not isinstance(week, int) or week < 1:
            return jsonify({
                'success': False,
                'message': 'Week must be a positive integer'
            }), 400
        
        if not isinstance(completion_percentage, (int, float)):
            return jsonify({
                'success': False,
                'message': 'Completion percentage must be a number'
            }), 400
        
        if not 0 <= completion_percentage <= 100:
            return jsonify({
                'success': False,
                'message': 'Completion percentage must be between 0 and 100'
            }), 400
        
        if not routine_data:
            return jsonify({
                'success': False,
                'message': 'Routine data is required'
            }), 400
        
        # Use shared progress manager
        manager = get_progress_manager()
        result = manager.update_progress(
            current_user,
            week,
            skill,
            completion_percentage,
            date,
            routine_data
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Progress update failed: {str(e)}'
        }), 500


@app.route('/api/routine/chat', methods=['POST'])
@token_required
def routine_chat(current_user):
    """
    AI chat for routine guidance and support
    
    Requires: Authorization header with Bearer token
    Accepts: {
        userQuestion: string,
        routineData: object (optional),
        progressData: object (optional)
    }
    Returns: {success, response, action_items, category}
    """
    try:
        import os
        import sys
        
        # Import backend modules
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        from routineChatAI import RoutineChatAI
        
        data = request.get_json()
        
        if not data or 'userQuestion' not in data:
            return jsonify({
                'success': False,
                'message': 'userQuestion is required'
            }), 400
        
        user_question = data['userQuestion']
        routine_data = data.get('routineData', None)
        progress_data = data.get('progressData', None)
        
        # Validate question length
        if len(user_question.strip()) < 2:
            return jsonify({
                'success': False,
                'message': 'Question is too short'
            }), 400
        
        if len(user_question) > 1000:
            return jsonify({
                'success': False,
                'message': 'Question is too long (max 1000 characters)'
            }), 400
        
        # Generate AI response
        chat_ai = RoutineChatAI()
        result = chat_ai.generate_response(
            user_question,
            routine_data,
            progress_data
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'response': 'I encountered an error processing your question. Please try again.',
            'message': str(e)
        }), 500


@app.route('/api/routine/generate', methods=['POST'])
@token_required
def generate_routine(current_user):
    """
    Generate personalized learning routine from uploaded analysis file
    
    Requires: Authorization header with Bearer token
    Accepts: multipart/form-data with:
        - file: Analysis report (JSON, PDF, or DOCX)
        - hoursPerWeek: Available study hours per week (optional, default 10)
    Returns: {success, routine}
    """
    try:
        import os
        import tempfile
        from werkzeug.utils import secure_filename
        
        # Import backend modules
        import sys
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        from routineEngineCore import RoutineEngineCore
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400
        
        # Get hours per week (default 10)
        hours_per_week = int(request.form.get('hoursPerWeek', 10))
        
        if hours_per_week < 1 or hours_per_week > 168:
            return jsonify({
                'success': False,
                'message': 'Hours per week must be between 1 and 168'
            }), 400
        
        # Validate file type
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_ext not in ['json', 'pdf', 'docx']:
            return jsonify({
                'success': False,
                'message': 'Invalid file type. Only JSON, PDF, and DOCX are supported'
            }), 400
        
        # Save file temporarily
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"routine_{current_user}_{filename}")
        file.save(temp_path)
        
        try:
            # Generate routine using backend engine
            engine = RoutineEngineCore()
            result = engine.generate_routine(temp_path, file_ext, hours_per_week)
            
            # Clean up temp file
            os.unlink(temp_path)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Routine generation failed: {str(e)}'
        }), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Run Flask app
    # Use debug=False in production
    app.run(debug=True, host='0.0.0.0', port=5000)


"""
Installation Requirements:
pip install flask flask-cors pyjwt

Production Considerations:
1. Use environment variables for SECRET_KEY
2. Enable HTTPS
3. Set secure CORS origins (not localhost)
4. Add rate limiting
5. Implement proper password hashing (bcrypt)
6. Add input validation and sanitization
7. Use a production WSGI server (gunicorn, uwsgi)
8. Set up proper logging
9. Add database connection pooling
10. Implement refresh tokens
"""


# ============================================
# COMMUNITY MODULE API ENDPOINTS
# ============================================

@app.route('/api/community/groups', methods=['GET'])
@token_required
def get_community_groups(current_user):
    """
    Get list of community groups
    Returns: {success, communities}
    """
    try:
        communities = CommunityService.get_communities(current_user)
        
        return jsonify({
            'success': True,
            'communities': communities
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/groups', methods=['POST'])
@token_required
def create_community_group(current_user):
    """
    Create a new community group
    Accepts: {name, description, category, tags}
    Returns: {success, community}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'name' not in data or 'description' not in data:
            return jsonify({
                'success': False,
                'message': 'Name and description are required'
            }), 400
        
        community = CommunityService.create_community(
            user_id=current_user,
            name=data['name'],
            description=data['description'],
            category=data.get('category', 'Other'),
            tags=data.get('tags', [])
        )
        
        return jsonify({
            'success': True,
            'community': community
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/groups/<int:community_id>/join', methods=['POST'])
@token_required
def join_community(current_user, community_id):
    """
    Join a community group
    Returns: {success, message}
    """
    try:
        result = CommunityService.join_community(current_user, community_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/feedback', methods=['GET'])
@token_required
def get_feedback(current_user):
    """
    Get all feedback posts
    Returns: {success, feedbacks}
    """
    try:
        feedbacks = CommunityService.get_feedback()
        
        return jsonify({
            'success': True,
            'feedbacks': feedbacks
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/feedback', methods=['POST'])
@token_required
def submit_feedback(current_user):
    """
    Submit new feedback
    Accepts: {content, category}
    Returns: {success, feedback}
    """
    try:
        data = request.get_json()
        
        if 'content' not in data:
            return jsonify({
                'success': False,
                'message': 'Content is required'
            }), 400
        
        feedback = CommunityService.submit_feedback(
            user_id=current_user,
            content=data['content'],
            category=data.get('category', 'General')
        )
        
        return jsonify({
            'success': True,
            'feedback': feedback
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/blogs', methods=['GET'])
@token_required
def get_blogs(current_user):
    """
    Get all blog posts
    Returns: {success, blogs}
    """
    try:
        blogs = CommunityService.get_blogs()
        
        return jsonify({
            'success': True,
            'blogs': blogs
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/blogs', methods=['POST'])
@token_required
def create_blog(current_user):
    """
    Create a new blog post
    Accepts: {title, content, tags, community_id}
    Returns: {success, blog}
    """
    try:
        data = request.get_json()
        
        if 'title' not in data or 'content' not in data:
            return jsonify({
                'success': False,
                'message': 'Title and content are required'
            }), 400
        
        blog = CommunityService.create_blog(
            user_id=current_user,
            title=data['title'],
            content=data['content'],
            tags=data.get('tags', []),
            community_id=data.get('community_id')
        )
        
        return jsonify({
            'success': True,
            'blog': blog
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/reach-out', methods=['GET'])
@token_required
def get_related_profiles(current_user):
    """
    Get related user profiles based on skills and interests
    Returns: {success, profiles}
    """
    try:
        profiles = CommunityService.get_related_profiles(current_user)
        
        return jsonify({
            'success': True,
            'profiles': profiles
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/messages/<int:recipient_id>', methods=['GET'])
@token_required
def get_messages(current_user, recipient_id):
    """
    Get message history with a specific user
    Returns: {success, messages}
    """
    try:
        messages = CommunityService.get_messages(current_user, recipient_id)
        
        return jsonify({
            'success': True,
            'messages': messages
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/messages', methods=['POST'])
@token_required
def send_message(current_user):
    """
    Send a message to another user
    Accepts: {recipient_id, content}
    Returns: {success, message}
    """
    try:
        data = request.get_json()
        
        if 'recipient_id' not in data or 'content' not in data:
            return jsonify({
                'success': False,
                'message': 'Recipient ID and content are required'
            }), 400
        
        message = CommunityService.send_message(
            sender_id=current_user,
            recipient_id=data['recipient_id'],
            content=data['content']
        )
        
        return jsonify({
            'success': True,
            'message': message
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/recommended', methods=['GET'])
@token_required
def get_recommended_communities(current_user):
    """
    Get recommended communities based on user interests
    Uses vector-based cosine similarity matching
    
    Algorithm:
    1. Get user interests from UserProfile
    2. Get all communities with tags
    3. Build vocabulary from all terms
    4. Convert user interests to binary vector
    5. Convert community tags to binary vectors
    6. Compute cosine similarity for each
    7. Sort by similarity descending
    8. Return top 5 communities
    
    Returns: {success, recommendations, has_profile}
    """
    try:
        # Get limit from query params (default 5)
        limit = int(request.args.get('limit', 5))
        limit = min(max(limit, 1), 20)  # Clamp between 1 and 20
        
        # Get recommendations
        recommendations = CommunityService.get_recommended_communities(
            user_id=current_user,
            limit=limit
        )
        
        # Check if user has profile
        from community_models import UserProfile
        has_profile = UserProfile.query.filter_by(user_id=current_user).first() is not None
        
        # If no recommendations (no profile or no matches), return trending
        if not recommendations:
            recommendations = CommunityService.get_trending_communities(limit=limit)
            return jsonify({
                'success': True,
                'recommendations': recommendations,
                'has_profile': has_profile,
                'recommendation_type': 'trending',
                'message': 'Showing trending communities' if not has_profile else 'No matching communities found, showing trending'
            }), 200
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'has_profile': has_profile,
            'recommendation_type': 'personalized'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
            }), 400
        
        message = CommunityService.send_message(
            sender_id=current_user,
            recipient_id=data['recipient_id'],
            content=data['content']
        )
        
        return jsonify({
            'success': True,
            'message': message
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/recommended', methods=['GET'])
@token_required
def get_recommended_communities(current_user):
    """
    Get recommended communities based on user interests
    Uses vector-based cosine similarity matching
    
    Algorithm:
    1. Get user interests from UserProfile
    2. Get all communities with tags
    3. Build vocabulary from all terms
    4. Convert user interests to binary vector
    5. Convert community tags to binary vectors
    6. Compute cosine similarity for each
    7. Sort by similarity descending
    8. Return top 5 communities
    
    Returns: {success, recommendations, has_profile}
    """
    try:
        # Get limit from query params (default 5)
        limit = int(request.args.get('limit', 5))
        limit = min(max(limit, 1), 20)  # Clamp between 1 and 20
        
        # Get recommendations
        recommendations = CommunityService.get_recommended_communities(
            user_id=current_user,
            limit=limit
        )
        
        # Check if user has profile
        from community_models import UserProfile
        has_profile = UserProfile.query.filter_by(user_id=current_user).first() is not None
        
        # If no recommendations (no profile or no matches), return trending
        if not recommendations:
            recommendations = CommunityService.get_trending_communities(limit=limit)
            return jsonify({
                'success': True,
                'recommendations': recommendations,
                'has_profile': has_profile,
                'recommendation_type': 'trending',
                'message': 'Showing trending communities' if not has_profile else 'No matching communities found, showing trending'
            }), 200
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'has_profile': has_profile,
            'recommendation_type': 'personalized'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
