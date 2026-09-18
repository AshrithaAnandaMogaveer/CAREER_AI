"""
Flask CORS Configuration with Database Integration
Main Flask backend with SQLAlchemy database support
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail, Message as MailMessage
import jwt
import datetime
import secrets
from functools import wraps
import os
import sys

# Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
except ImportError:
    pass

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

# Flask-Mail configuration (Gmail SMTP)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME', '')
mail = Mail(app)

# Initialize database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    from community_models import (
        Community, CommunityMember, Post, Comment, Like,
        Conversation, Message, Notification, UserProfile
    )
    from progress_tracking_model import RoutineProgress
    from explore_cache_model import UserAnalysisCache
    db.create_all()
    print(f"✓ Database initialized: {app.config['SQLALCHEMY_DATABASE_URI']}")

# CORS Configuration - MUST be after app creation but before routes
CORS(app, 
     resources={
         r"/api/*": {"origins": "*"},
         r"/uploads/*": {"origins": "*"}
     },
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True,
     expose_headers=["Content-Type", "Authorization"]
)

# Rate Limiter — protects expensive endpoints without blocking the whole app
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'success': False, 'message': 'Too many requests. Please try again later.'}), 429

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
        
        # Optional profile picture URL (set after upload via /api/upload/profile-picture)
        if data.get('profile_picture'):
            user.profile_picture = data['profile_picture']
        
        db.session.add(user)
        db.session.flush()  # Get user.id before commit
        
        # Automatically create UserProfile for Reach-Out feature
        from community_models import UserProfile
        user_profile = UserProfile(
            user_id=user.id,
            domains=[domain] if domain else [],
            skills=[],  # User can update later
            interests=[],  # User can update later
            experience_years=0,
            projects_count=0
        )
        db.session.add(user_profile)
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
            'user': user.to_dict(),
            'message': 'Account created successfully! Complete your profile to get better matches.'
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


# In-memory store for password reset tokens: { token: { user_id, expires_at } }
_reset_tokens = {}


@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    """
    Send password reset email with a one-time token link.
    Body: { email }
    """
    try:
        data = request.get_json()
        email = (data.get('email') or '').strip().lower()
        if not email:
            return jsonify({'success': False, 'message': 'Email is required'}), 400

        user = User.query.filter_by(email=email, is_deleted=False).first()
        # Always return success to avoid email enumeration
        if not user:
            return jsonify({'success': True, 'message': 'If that email exists, a reset link has been sent.'}), 200

        # Generate a secure token valid for 15 minutes
        token = secrets.token_urlsafe(32)
        _reset_tokens[token] = {
            'user_id': user.id,
            'expires_at': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        }

        frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
        reset_link = f'{frontend_url}/reset-password?token={token}'

        mail_username = app.config.get('MAIL_USERNAME', '')
        mail_password = app.config.get('MAIL_PASSWORD', '')
        if not mail_username or mail_username == 'your_gmail@gmail.com' or not mail_password or mail_password == 'your_app_password_here':
            # No email configured — return token in response for dev/testing
            return jsonify({
                'success': True,
                'message': 'Reset link generated (email not configured).',
                'dev_reset_link': reset_link
            }), 200

        msg = MailMessage(
            subject='CareerAI — Reset Your Password',
            recipients=[user.email],
            html=f"""
            <div style="font-family:sans-serif;max-width:480px;margin:auto;padding:32px;background:#1a1a2e;color:#e0e0e0;border-radius:12px;">
              <h2 style="color:#7c3aed;">Reset Your Password</h2>
              <p>Hi <strong>{user.name}</strong>,</p>
              <p>We received a request to reset your CareerAI password. Click the button below — this link expires in <strong>15 minutes</strong>.</p>
              <a href="{reset_link}" style="display:inline-block;margin:24px 0;padding:12px 28px;background:#7c3aed;color:#fff;border-radius:8px;text-decoration:none;font-weight:bold;">Reset Password</a>
              <p style="color:#888;font-size:13px;">If you didn't request this, you can safely ignore this email.</p>
            </div>
            """
        )
        mail.send(msg)

        return jsonify({'success': True, 'message': 'Password reset email sent. Check your inbox.'}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    """
    Reset password using the token from the email link.
    Body: { token, new_password }
    """
    try:
        data = request.get_json()
        token = (data.get('token') or '').strip()
        new_password = data.get('new_password', '')

        if not token or not new_password:
            return jsonify({'success': False, 'message': 'Token and new password are required'}), 400

        if len(new_password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400

        entry = _reset_tokens.get(token)
        if not entry:
            return jsonify({'success': False, 'message': 'Invalid or expired reset link'}), 400

        if datetime.datetime.utcnow() > entry['expires_at']:
            del _reset_tokens[token]
            return jsonify({'success': False, 'message': 'Reset link has expired. Please request a new one.'}), 400

        user = User.query.get(entry['user_id'])
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        user.set_password(new_password)
        db.session.commit()

        # Invalidate token after use
        del _reset_tokens[token]

        return jsonify({'success': True, 'message': 'Password reset successfully. You can now log in.'}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """
    Get user profile (protected route)
    Requires: Authorization header with Bearer token
    Returns: {success, user, profile}
    """
    try:
        # Get user from database
        user = User.query.get(current_user)
        
        if not user or user.is_deleted or not user.is_active:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Get user profile for Reach-Out feature
        from community_models import UserProfile
        user_profile = UserProfile.query.filter_by(user_id=current_user).first()
        
        return jsonify({
            'success': True,
            'user': user.to_dict(),
            'profile': user_profile.to_dict() if user_profile else None
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/profile', methods=['PUT', 'PATCH'])
@token_required
def update_profile(current_user):
    """
    Update user profile for Reach-Out matching
    Requires: Authorization header with Bearer token
    Expected JSON: {
        skills: ["Python", "SQL", ...],
        interests: ["AI", "Data Science", ...],
        domains: ["Data Science", ...],
        bio: "About me...",
        location: "City, Country",
        website: "https://...",
        experience_years: 3,
        projects_count: 5
    }
    Returns: {success, profile, message}
    """
    try:
        from community_models import UserProfile
        
        data = request.get_json()
        
        # Get or create user profile
        user_profile = UserProfile.query.filter_by(user_id=current_user).first()
        
        if not user_profile:
            # Create new profile if doesn't exist
            user = User.query.get(current_user)
            user_profile = UserProfile(
                user_id=current_user,
                domains=[user.domain] if user and user.domain else []
            )
            db.session.add(user_profile)
        
        # Update fields if provided
        if 'skills' in data:
            user_profile.skills = data['skills'] if isinstance(data['skills'], list) else []
        
        if 'interests' in data:
            user_profile.interests = data['interests'] if isinstance(data['interests'], list) else []
        
        if 'domains' in data:
            user_profile.domains = data['domains'] if isinstance(data['domains'], list) else []
        
        if 'bio' in data:
            user_profile.bio = data['bio']
        
        if 'location' in data:
            user_profile.location = data['location']
        
        if 'website' in data:
            user_profile.website = data['website']
        
        if 'experience_years' in data:
            user_profile.experience_years = int(data['experience_years']) if data['experience_years'] else 0
        
        if 'projects_count' in data:
            user_profile.projects_count = int(data['projects_count']) if data['projects_count'] else 0
        
        user_profile.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'profile': user_profile.to_dict(),
            'message': 'Profile updated successfully! You can now see matching profiles in Reach-Out.'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/user', methods=['PUT', 'PATCH'])
@token_required
def update_user(current_user):
    """
    Update basic user fields: name, domain, email
    Accepts: {name, domain, email}
    Returns: {success, user}
    """
    try:
        data = request.get_json()
        user = User.query.get(current_user)
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        if 'name' in data and data['name'].strip():
            user.name = data['name'].strip()
        if 'domain' in data:
            user.domain = data['domain'].strip() if data['domain'] else user.domain
        if 'email' in data and data['email'].strip():
            # Check email not taken by another user
            existing = User.query.filter(
                User.email == data['email'].lower().strip(),
                User.id != current_user,
                User.is_deleted == False
            ).first()
            if existing:
                return jsonify({'success': False, 'message': 'Email already in use'}), 400
            user.email = data['email'].lower().strip()

        user.updated_at = datetime.datetime.utcnow()
        db.session.commit()

        return jsonify({'success': True, 'user': user.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/upload/profile-picture', methods=['POST'])
@token_required
def upload_profile_picture(current_user):
    """
    Upload a profile picture for the current user.
    Accepts: multipart/form-data with 'picture' file field
    Returns: {success, profile_picture_url}
    """
    try:
        if 'picture' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400

        file = request.files['picture']
        if not file or file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400

        # Validate file type
        allowed = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
        if ext not in allowed:
            return jsonify({'success': False, 'message': 'Invalid file type. Use PNG, JPG, GIF or WEBP'}), 400

        # Save file
        import uuid
        unique_filename = f"{uuid.uuid4().hex}_{current_user}.{ext}"
        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'profile_pictures')
        os.makedirs(upload_dir, exist_ok=True)
        file.save(os.path.join(upload_dir, unique_filename))

        url = f"/uploads/profile_pictures/{unique_filename}"

        # Update user record
        user = User.query.get(current_user)
        if user:
            user.profile_picture = url
            db.session.commit()

        return jsonify({'success': True, 'profile_picture_url': url}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/uploads/profile_pictures/<filename>')
def serve_profile_picture(filename):
    """Serve uploaded profile pictures"""
    try:
        from flask import send_from_directory
        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'profile_pictures')
        return send_from_directory(upload_dir, filename)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 404


@app.route('/api/analyze-resume', methods=['POST'])
@token_required
@limiter.limit("10 per minute")
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
        
        # Save analyze result to Explore personalization cache (non-blocking)
        try:
            from explore_cache_model import UserAnalysisCache
            cache = UserAnalysisCache.query.filter_by(user_id=current_user).first()
            if not cache:
                cache = UserAnalysisCache(user_id=current_user)
                db.session.add(cache)
            cache.readiness_score = int(readiness_score['total_score'])
            cache.target_domain = target_domain
            cache.extracted_skills = all_skills[:30]
            cache.missing_skills = missing_skills[:15]
            db.session.commit()
        except Exception:
            pass  # Never block analyze if cache write fails

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
@limiter.limit("10 per minute")
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
        
        from mistral_local_chat import get_mistral_chat
        
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
        
        # Generate AI response using Mistral (with automatic fallback)
        chat_ai = get_mistral_chat()
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
        
        # Get user's domain override (sent from frontend localStorage)
        user_domain = request.form.get('userDomain', '').strip()
        
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
            result = engine.generate_routine(temp_path, file_ext, hours_per_week, user_domain)
            
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


# ============================================
# ROUTINE PROGRESS TRACKING API ENDPOINTS
# ============================================

@app.route('/api/routine/progress/weekly', methods=['GET'])
@token_required
def get_weekly_progress(current_user):
    """
    Get user's weekly progress for all topics
    
    Requires: Authorization header with Bearer token
    Query Parameters:
        - skill: Filter by skill (optional)
    Returns: {success, progress}
    """
    try:
        from progress_tracking_model import RoutineProgress
        
        skill_filter = request.args.get('skill')
        
        # Build query
        query = RoutineProgress.query.filter_by(user_id=current_user)
        
        if skill_filter:
            query = query.filter_by(skill=skill_filter)
        
        # Get all progress records
        progress_records = query.order_by(RoutineProgress.week_number).all()
        
        return jsonify({
            'success': True,
            'progress': [record.to_dict() for record in progress_records],
            'count': len(progress_records)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/routine/progress/weekly', methods=['POST'])
@token_required
def update_weekly_progress(current_user):
    """
    Update completion status for a specific week/topic
    
    Requires: Authorization header with Bearer token
    Accepts: {
        skill: string,
        week_number: int,
        topic: string,
        completed: boolean
    }
    Returns: {success, progress, message}
    """
    try:
        from progress_tracking_model import RoutineProgress
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['skill', 'week_number', 'topic', 'completed']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        skill = data['skill']
        week_number = data['week_number']
        topic = data['topic']
        completed = data['completed']
        
        # Validate types
        if not isinstance(week_number, int) or week_number < 1:
            return jsonify({
                'success': False,
                'message': 'Week number must be a positive integer'
            }), 400
        
        if not isinstance(completed, bool):
            return jsonify({
                'success': False,
                'message': 'Completed must be a boolean'
            }), 400
        
        # Check if record exists
        progress_record = RoutineProgress.query.filter_by(
            user_id=current_user,
            skill=skill,
            week_number=week_number,
            topic=topic
        ).first()
        
        if progress_record:
            # Update existing record
            progress_record.completed = completed
            progress_record.completed_at = datetime.datetime.utcnow() if completed else None
            progress_record.updated_at = datetime.datetime.utcnow()
        else:
            # Create new record
            progress_record = RoutineProgress(
                user_id=current_user,
                skill=skill,
                week_number=week_number,
                topic=topic,
                completed=completed,
                completed_at=datetime.datetime.utcnow() if completed else None
            )
            db.session.add(progress_record)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'progress': progress_record.to_dict(),
            'message': f'Progress updated: {topic} marked as {"completed" if completed else "incomplete"}'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/routine/progress/summary', methods=['GET'])
@token_required
def get_progress_summary(current_user):
    """
    Get progress summary with completion statistics per skill
    
    Requires: Authorization header with Bearer token
    Returns: {success, summary}
    """
    try:
        from progress_tracking_model import RoutineProgress
        from sqlalchemy import func
        
        # Get completion stats per skill
        stats = db.session.query(
            RoutineProgress.skill,
            func.count(RoutineProgress.id).label('total_topics'),
            func.sum(db.case((RoutineProgress.completed == True, 1), else_=0)).label('completed_topics')
        ).filter_by(
            user_id=current_user
        ).group_by(
            RoutineProgress.skill
        ).all()
        
        summary = []
        for skill, total, completed in stats:
            completed = completed or 0
            completion_percentage = (completed / total * 100) if total > 0 else 0
            
            # Determine status
            if completion_percentage >= 80:
                status = 'Achieved'
            elif completion_percentage >= 50:
                status = 'In Progress'
            elif completion_percentage > 0:
                status = 'Started'
            else:
                status = 'Not Started'
            
            summary.append({
                'skill': skill,
                'total_topics': total,
                'completed_topics': completed,
                'completion_percentage': round(completion_percentage, 1),
                'status': status
            })
        
        return jsonify({
            'success': True,
            'summary': summary,
            'total_skills': len(summary)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/routine/evolution/analytics', methods=['GET'])
@token_required
def get_evolution_analytics(current_user):
    """
    Get evolution analytics with graph-ready data
    
    Requires: Authorization header with Bearer token
    Query Parameters:
        - skill: Filter by skill (optional)
    Returns: {
        success,
        analytics: {
            daily_progress: [{date, completed_topics, cumulative_topics}],
            weekly_progress: [{week_number, completed_topics, remaining_topics, completion_rate}],
            skill_completion: [{skill, total_topics, completed_topics, completion_percentage, status}],
            overall_metrics: {total_topics, completed_topics, remaining_topics, overall_completion_rate, ...}
        }
    }
    """
    try:
        from progress_tracking_model import RoutineProgress
        from evolution_analytics import EvolutionAnalytics
        
        skill_filter = request.args.get('skill')
        
        # Build query
        query = RoutineProgress.query.filter_by(user_id=current_user)
        
        if skill_filter:
            query = query.filter_by(skill=skill_filter)
        
        # Get all progress records
        progress_records = query.all()
        
        # Convert to dict format
        progress_data = [record.to_dict() for record in progress_records]
        
        # Generate analytics
        analytics_engine = EvolutionAnalytics()
        analytics = analytics_engine.generate_analytics(progress_data)
        
        return jsonify({
            'success': True,
            'analytics': analytics
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


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


@app.route('/api/community/create', methods=['POST'])
@token_required
def create_community(current_user):
    """
    Create a new community
    
    Rules:
    - Only authenticated users can create
    - Creator becomes ADMIN automatically
    - Community name must be unique
    - Automatically joins as first member
    
    Accepts: {name, description, category, tags}
    Returns: {success, community, message}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'name' not in data or 'description' not in data:
            return jsonify({
                'success': False,
                'message': 'Name and description are required'
            }), 400
        
        # Create community
        result = CommunityService.create_community(
            user_id=current_user,
            name=data['name'],
            description=data['description'],
            category=data.get('category', 'General'),
            tags=data.get('tags', [])
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/join', methods=['POST'])
@token_required
def join_community(current_user):
    """
    Join a community
    
    Rules:
    - Only authenticated users can join
    - Prevents duplicate membership
    - Creates notification for community admins
    - Updates member count
    
    Accepts: {community_id}
    Returns: {success, message, community}
    """
    try:
        data = request.get_json()
        
        if 'community_id' not in data:
            return jsonify({
                'success': False,
                'message': 'Community ID is required'
            }), 400
        
        # Join community
        result = CommunityService.join_community(
            user_id=current_user,
            community_id=data['community_id']
        )
        
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


@app.route('/api/community/groups/<int:community_id>', methods=['GET'])
@token_required
def get_community_group(current_user, community_id):
    """Get a single community by ID"""
    try:
        from community_models import Community, CommunityMember
        from user_model import User  # needed to resolve CommunityMember relationships
        community = Community.query.get(community_id)
        if not community or community.is_deleted:
            return jsonify({'success': False, 'message': 'Community not found'}), 404
        is_member = CommunityMember.query.filter_by(
            community_id=community_id, user_id=current_user, is_deleted=False
        ).first() is not None
        data = community.to_dict()
        data['is_member'] = is_member
        return jsonify({'success': True, 'community': data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# Legacy endpoint for backward compatibility
@app.route('/api/community/groups', methods=['POST'])
@token_required
def create_community_group_legacy(current_user):
    """
    Legacy endpoint - redirects to /api/community/create
    """
    return create_community(current_user)


@app.route('/api/community/groups/<int:community_id>/join', methods=['POST'])
@token_required
def join_community_legacy(current_user, community_id):
    """
    Legacy endpoint - Join a community by ID in URL
    Redirects to /api/community/join
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
    Create a new blog post with optional video upload
    Accepts: multipart/form-data with fields: title, content, tags, video (file)
    Returns: {success, blog}
    """
    try:
        import os
        from werkzeug.utils import secure_filename
        
        # Get form data
        title = request.form.get('title')
        content = request.form.get('content')
        tags_str = request.form.get('tags', '')
        
        if not title or not content:
            return jsonify({
                'success': False,
                'message': 'Title and content are required'
            }), 400
        
        # Parse tags
        tags = []
        if tags_str:
            tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        
        # Handle video file upload
        video_path = None
        if 'video' in request.files:
            video_file = request.files['video']
            if video_file and video_file.filename:
                # Validate file extension
                allowed_extensions = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv', 'mpeg', 'mpg'}
                filename = secure_filename(video_file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                
                if file_ext not in allowed_extensions:
                    return jsonify({
                        'success': False,
                        'message': f'Invalid video format. Allowed: {", ".join(allowed_extensions)}'
                    }), 400
                
                # Create unique filename
                import uuid
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                
                # Ensure upload directory exists
                upload_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'videos')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Save file
                file_path = os.path.join(upload_dir, unique_filename)
                video_file.save(file_path)
                
                # Store relative path
                video_path = f"uploads/videos/{unique_filename}"
        
        # Create blog
        blog = CommunityService.create_blog(
            user_id=current_user,
            title=title,
            content=content,
            tags=tags,
            community_id=request.form.get('community_id'),
            video_url=video_path
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


@app.route('/api/community/videos/<path:filename>', methods=['GET'])
def serve_video(filename):
    """
    Serve uploaded video files
    """
    try:
        import os
        from flask import send_from_directory
        
        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'videos')
        return send_from_directory(upload_dir, filename)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Video not found'
        }), 404


@app.route('/api/community/reach-out', methods=['GET'])
@app.route('/api/community/reachout', methods=['GET'])
@token_required
def get_related_profiles(current_user):
    """
    Get related user profiles based on weighted similarity scoring
    
    Phase 7 Weighted Formula:
    score = 0.4 × domainMatch + 0.3 × skillOverlap + 0.2 × experienceMatch + 0.1 × interestMatch
    
    Query Parameters:
    - limit: Maximum number of profiles (default 10, max 50)
    - min_score: Minimum similarity score 0-100 (default 0)
    - include_breakdown: Include detailed score breakdown (true/false, default false)
    
    Returns: {success, profiles, has_profile, count}
    """
    try:
        from community_models import UserProfile
        
        # Get query parameters
        limit = int(request.args.get('limit', 50))
        limit = min(max(limit, 1), 100)  # Clamp between 1 and 100
        
        min_score = float(request.args.get('min_score', 0))
        min_score = min(max(min_score, 0), 100)  # Clamp between 0 and 100
        
        include_breakdown = request.args.get('include_breakdown', 'false').lower() == 'true'
        
        # Check if user has profile (informational only, don't block)
        has_profile = UserProfile.query.filter_by(user_id=current_user).first() is not None
        
        # Get matching profiles
        profiles = CommunityService.get_related_profiles(
            user_id=current_user,
            limit=limit,
            min_score=min_score,
            include_breakdown=include_breakdown
        )
        
        return jsonify({
            'success': True,
            'profiles': profiles,
            'has_profile': True,
            'count': len(profiles),
            'min_score_threshold': min_score
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# ============================================
# PHASE 8: PRIVATE MESSAGING SYSTEM
# ============================================

@app.route('/api/community/message', methods=['POST'])
@token_required
def send_message_v2(current_user):
    """
    Phase 8: Send a message to another user
    
    Logic:
    - Create conversation if not exists
    - Store message
    - Mark unread for receiver
    - Trigger notification event
    
    Accepts: {recipient_id, content}
    Returns: {success, message, conversation_id}
    """
    try:
        data = request.get_json()
        
        if 'recipient_id' not in data or 'content' not in data:
            return jsonify({
                'success': False,
                'message': 'Recipient ID and content are required'
            }), 400
        
        result = CommunityService.send_message(
            sender_id=current_user,
            recipient_id=data['recipient_id'],
            content=data['content']
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/messages/<int:conversation_id>', methods=['GET'])
@token_required
def get_conversation_messages(current_user, conversation_id):
    """
    Phase 8: Get messages from a specific conversation
    
    Query Parameters:
    - limit: Maximum number of messages (default 100, max 500)
    
    Returns: {success, messages, conversation_id}
    """
    try:
        from community_models import Conversation
        
        # Get conversation
        conversation = Conversation.query.get(conversation_id)
        
        if not conversation or conversation.is_deleted:
            return jsonify({
                'success': False,
                'message': 'Conversation not found'
            }), 404
        
        # Verify user is participant
        if conversation.user1_id != current_user and conversation.user2_id != current_user:
            return jsonify({
                'success': False,
                'message': 'Unauthorized access to conversation'
            }), 403
        
        # Get other user ID
        other_user_id = conversation.user2_id if conversation.user1_id == current_user else conversation.user1_id
        
        # Get limit from query params
        limit = int(request.args.get('limit', 100))
        limit = min(max(limit, 1), 500)  # Clamp between 1 and 500
        
        # Get messages (this also marks them as read)
        messages = CommunityService.get_messages(current_user, other_user_id, limit=limit)
        
        return jsonify({
            'success': True,
            'messages': messages,
            'conversation_id': conversation_id,
            'count': len(messages)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/conversations', methods=['GET'])
@token_required
def get_conversations(current_user):
    """
    Get all conversations for the current user
    
    Query Parameters:
    - limit: Maximum number of conversations (default 50, max 100)
    
    Returns: {success, conversations, unread_total}
    """
    try:
        # Get limit from query params
        limit = int(request.args.get('limit', 50))
        limit = min(max(limit, 1), 100)  # Clamp between 1 and 100
        
        # Get conversations
        conversations = CommunityService.get_conversations(current_user, limit=limit)
        
        # Calculate total unread
        unread_total = sum(conv['unread_count'] for conv in conversations)
        
        return jsonify({
            'success': True,
            'conversations': conversations,
            'count': len(conversations),
            'unread_total': unread_total
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/conversations/<int:conversation_id>/read', methods=['POST'])
@token_required
def mark_conversation_read(current_user, conversation_id):
    """
    Mark all messages in a conversation as read
    
    Returns: {success, marked_read}
    """
    try:
        result = CommunityService.mark_conversation_read(current_user, conversation_id)
        
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


# Legacy endpoints (backward compatibility)
@app.route('/api/community/messages/user/<int:recipient_id>', methods=['GET'])
@token_required
def get_messages_legacy(current_user, recipient_id):
    """
    Legacy: Get message history with a specific user
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
def send_message_legacy(current_user):
    """
    Legacy: Send a message to another user
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
        
        result = CommunityService.send_message(
            sender_id=current_user,
            recipient_id=data['recipient_id'],
            content=data['content']
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
        
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


@app.route('/api/community/feed', methods=['GET'])
@token_required
def get_community_feed(current_user):
    """
    Get personalized ranked feed for user
    
    Ranking Formula:
    rankScore = (0.5 × recencyScore) + (0.3 × engagementScore) + (0.2 × relevanceScore)
    
    Where:
    - recencyScore = e^(-0.1 × hoursSincePost)
    - engagementScore = normalized(likes + 2 × comments)
    - relevanceScore = cosine(userInterests, postTags)
    
    Query Parameters:
    - type: Filter by post type ('blog', 'feedback', or omit for all)
    - limit: Maximum number of posts (default 50, max 100)
    - include_scores: Include score breakdown (true/false, default false)
    
    Returns: {success, feed, stats}
    """
    try:
        # Get query parameters
        post_type = request.args.get('type', None)
        limit = int(request.args.get('limit', 50))
        limit = min(max(limit, 1), 100)  # Clamp between 1 and 100
        include_scores = request.args.get('include_scores', 'false').lower() == 'true'
        
        # Get ranked feed
        feed = CommunityService.get_ranked_feed(
            user_id=current_user,
            post_type=post_type,
            limit=limit,
            include_scores=include_scores
        )
        
        # Get feed stats
        stats = CommunityService.get_feed_stats(current_user)
        
        return jsonify({
            'success': True,
            'feed': feed,
            'stats': stats,
            'personalized': stats['personalization_enabled']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/feed/trending', methods=['GET'])
@token_required
def get_trending_feed(current_user):
    """
    Get trending posts based on recent engagement
    
    Query Parameters:
    - type: Filter by post type ('blog', 'feedback', or omit for all)
    - hours: Time window in hours (default 24, max 168)
    - limit: Maximum number of posts (default 10, max 50)
    
    Returns: {success, trending}
    """
    try:
        # Get query parameters
        post_type = request.args.get('type', None)
        time_window_hours = int(request.args.get('hours', 24))
        time_window_hours = min(max(time_window_hours, 1), 168)  # Clamp 1-168 hours
        limit = int(request.args.get('limit', 10))
        limit = min(max(limit, 1), 50)  # Clamp between 1 and 50
        
        # Get trending posts
        trending = CommunityService.get_trending_posts(
            post_type=post_type,
            time_window_hours=time_window_hours,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'trending': trending,
            'time_window_hours': time_window_hours
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500



# ============================================
# PHASE 9: NOTIFICATION ENGINE
# ============================================

@app.route('/api/community/notifications', methods=['GET'])
@token_required
def get_notifications(current_user):
    """
    Phase 9: Get user notifications
    
    Notification fields:
    - user_id: Recipient of notification
    - type: Notification type (NEW_MESSAGE, NEW_COMMENT, COMMUNITY_JOIN, POST_LIKE, etc.)
    - reference_id: Entity ID (entity_id in model)
    - is_read: Read status
    - timestamp: Created at
    
    Query Parameters:
    - unread_only: Filter unread notifications (true/false, default false)
    - limit: Maximum number of notifications (default 50, max 100)
    - type: Filter by notification type (optional)
    
    Returns: {success, notifications, unread_count, total_count}
    """
    try:
        from community_models import Notification
        
        # Get query parameters
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        limit = int(request.args.get('limit', 50))
        limit = min(max(limit, 1), 100)
        notification_type = request.args.get('type', None)
        
        # Build query
        query = Notification.query.filter_by(user_id=current_user, is_deleted=False)
        
        if unread_only:
            query = query.filter_by(is_read=False)
        
        if notification_type:
            query = query.filter_by(type=notification_type)
        
        # Get notifications
        notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
        
        # Get unread count
        unread_count = Notification.query.filter_by(
            user_id=current_user,
            is_read=False,
            is_deleted=False
        ).count()
        
        # Get total count
        total_count = Notification.query.filter_by(
            user_id=current_user,
            is_deleted=False
        ).count()
        
        # Format notifications for Phase 9
        formatted_notifications = []
        for n in notifications:
            notification_data = n.to_dict(include_actor=True)
            # Add Phase 9 fields
            notification_data['reference_id'] = n.entity_id
            notification_data['timestamp'] = n.created_at.isoformat() if n.created_at else None
            # Ensure actor_name is always present if actor_id exists but relationship wasn't loaded
            if n.actor_id and 'actor_name' not in notification_data:
                from user_model import User as UserModel
                actor = UserModel.query.get(n.actor_id)
                if actor:
                    notification_data['actor_name'] = actor.name
            formatted_notifications.append(notification_data)
        
        return jsonify({
            'success': True,
            'notifications': formatted_notifications,
            'unread_count': unread_count,
            'total_count': total_count,
            'count': len(formatted_notifications)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/notifications/read', methods=['POST'])
@token_required
def mark_notifications_read(current_user):
    """
    Phase 9: Mark notification(s) as read
    
    Accepts:
    - notification_id: Single notification ID (optional)
    - notification_ids: Array of notification IDs (optional)
    - all: Mark all as read (true/false, optional)
    
    Returns: {success, message, count}
    """
    try:
        from community_models import Notification
        from datetime import datetime
        
        data = request.get_json() or {}
        
        # Option 1: Mark all as read
        if data.get('all') == True:
            notifications = Notification.query.filter_by(
                user_id=current_user,
                is_read=False,
                is_deleted=False
            ).all()
            
            count = len(notifications)
            for notification in notifications:
                notification.is_read = True
                notification.read_at = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Marked {count} notifications as read',
                'count': count
            }), 200
        
        # Option 2: Mark multiple by IDs
        elif 'notification_ids' in data:
            notification_ids = data['notification_ids']
            
            if not isinstance(notification_ids, list):
                return jsonify({
                    'success': False,
                    'message': 'notification_ids must be an array'
                }), 400
            
            notifications = Notification.query.filter(
                Notification.id.in_(notification_ids),
                Notification.user_id == current_user,
                Notification.is_deleted == False
            ).all()
            
            count = 0
            for notification in notifications:
                if not notification.is_read:
                    notification.is_read = True
                    notification.read_at = datetime.utcnow()
                    count += 1
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Marked {count} notifications as read',
                'count': count
            }), 200
        
        # Option 3: Mark single by ID
        elif 'notification_id' in data:
            notification_id = data['notification_id']
            
            notification = Notification.query.filter_by(
                id=notification_id,
                user_id=current_user,
                is_deleted=False
            ).first()
            
            if not notification:
                return jsonify({
                    'success': False,
                    'message': 'Notification not found'
                }), 404
            
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Notification marked as read',
                'count': 1
            }), 200
        
        else:
            return jsonify({
                'success': False,
                'message': 'Must provide notification_id, notification_ids, or all=true'
            }), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# Legacy endpoints (backward compatibility)
@app.route('/api/community/notifications/<int:notification_id>/read', methods=['POST'])
@token_required
def mark_notification_read_legacy(current_user, notification_id):
    """
    Legacy: Mark notification as read
    Returns: {success, message}
    """
    try:
        from community_models import Notification
        from datetime import datetime
        
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=current_user,
            is_deleted=False
        ).first()
        
        if not notification:
            return jsonify({
                'success': False,
                'message': 'Notification not found'
            }), 404
        
        notification.is_read = True
        notification.read_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Notification marked as read'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/notifications/read-all', methods=['POST'])
@token_required
def mark_all_notifications_read_legacy(current_user):
    """
    Legacy: Mark all notifications as read
    Returns: {success, message, count}
    """
    try:
        from community_models import Notification
        from datetime import datetime
        
        notifications = Notification.query.filter_by(
            user_id=current_user,
            is_read=False,
            is_deleted=False
        ).all()
        
        count = len(notifications)
        for notification in notifications:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Marked {count} notifications as read',
            'count': count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# ============================================
# PHASE 6: UNIFIED POST MANAGEMENT
# ============================================

@app.route('/api/community/post', methods=['POST'])
@token_required
def create_post(current_user):
    """
    Unified endpoint to create any type of post (blog or feedback)
    
    Logic:
    - Saves user_id with content
    - Calculates read time for blogs
    - Updates community post count if applicable
    - Creates notifications for relevant users
    - Returns post data for feed ranking
    
    Accepts: {
        post_type: 'blog' | 'feedback',
        content: string (required),
        title: string (required for blogs),
        category: string (optional),
        tags: array (optional),
        community_id: int (optional)
    }
    Returns: {success, post, message}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'post_type' not in data or 'content' not in data:
            return jsonify({
                'success': False,
                'message': 'post_type and content are required'
            }), 400
        
        # Create post using unified service method
        result = CommunityService.create_post(
            user_id=current_user,
            post_type=data['post_type'],
            content=data['content'],
            title=data.get('title'),
            category=data.get('category'),
            tags=data.get('tags'),
            community_id=data.get('community_id')
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/posts', methods=['GET'])
@token_required
def get_posts(current_user):
    """
    Get posts with optional filtering
    
    Query Parameters:
    - type: Filter by post type ('blog', 'feedback', or omit for all)
    - user_id: Filter by author (optional)
    - limit: Maximum number of posts (default 50, max 100)
    
    Returns: {success, posts, count}
    """
    try:
        # Get query parameters
        post_type = request.args.get('type', None)
        user_id = request.args.get('user_id', None)
        limit = int(request.args.get('limit', 50))
        limit = min(max(limit, 1), 100)  # Clamp between 1 and 100
        
        # Convert user_id to int if provided
        if user_id:
            try:
                user_id = int(user_id)
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid user_id format'
                }), 400
        
        # Get posts
        posts = CommunityService.get_posts(
            post_type=post_type,
            limit=limit,
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'posts': posts,
            'count': len(posts)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# ============================================
# PHASE 9: COMMENTS & LIKES (WITH NOTIFICATIONS)
# ============================================

@app.route('/api/community/posts/<int:post_id>/comments', methods=['POST'])
@token_required
def add_comment(current_user, post_id):
    """
    Phase 9: Add a comment to a post
    Triggers notification when someone comments
    
    Accepts: {content, parent_comment_id (optional)}
    Returns: {success, comment}
    """
    try:
        data = request.get_json()
        
        if 'content' not in data:
            return jsonify({
                'success': False,
                'message': 'Content is required'
            }), 400
        
        result = CommunityService.add_comment(
            user_id=current_user,
            post_id=post_id,
            content=data['content'],
            parent_comment_id=data.get('parent_comment_id')
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/posts/<int:post_id>/like', methods=['POST'])
@token_required
def like_post(current_user, post_id):
    """
    Phase 9: Toggle like on a post
    Triggers notification when someone likes post
    
    Returns: {success, action}
    """
    try:
        result = CommunityService.toggle_like(
            user_id=current_user,
            post_id=post_id
        )
        
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


@app.route('/api/community/comments/<int:comment_id>/like', methods=['POST'])
@token_required
def like_comment(current_user, comment_id):
    """
    Phase 9: Toggle like on a comment
    Triggers notification when someone likes comment
    
    Returns: {success, action}
    """
    try:
        result = CommunityService.toggle_like(
            user_id=current_user,
            comment_id=comment_id
        )
        
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


# Handle OPTIONS requests for CORS preflight
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        return response


# ============================================
# COMMUNITY CHAT ROOM ENDPOINTS
# ============================================

@app.route('/api/community/<int:community_id>/messages', methods=['GET'])
@token_required
def get_community_messages(current_user, community_id):
    """
    Get all messages in a community chat room
    Only members can view messages
    """
    try:
        # Check if user is a member
        from community_models import CommunityMember
        membership = CommunityMember.query.filter_by(
            community_id=community_id,
            user_id=current_user,
            is_deleted=False
        ).first()
        
        if not membership:
            return jsonify({
                'success': False,
                'message': 'You must be a member to view messages'
            }), 403
        
        # Get messages
        messages = CommunityService.get_community_messages(community_id, limit=100)
        
        return jsonify({
            'success': True,
            'messages': messages,
            'count': len(messages)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/message/send', methods=['POST'])
@token_required
def send_community_message(current_user):
    """
    Send a message to a community chat room
    Supports text and image uploads
    """
    try:
        from werkzeug.utils import secure_filename
        import os
        
        community_id = request.form.get('community_id')
        content = request.form.get('content', '').strip()
        image = request.files.get('image')
        
        if not community_id:
            return jsonify({
                'success': False,
                'message': 'Community ID is required'
            }), 400
        
        community_id = int(community_id)
        
        # Check if user is a member
        from community_models import CommunityMember
        membership = CommunityMember.query.filter_by(
            community_id=community_id,
            user_id=current_user,
            is_deleted=False
        ).first()
        
        if not membership:
            return jsonify({
                'success': False,
                'message': 'You must be a member to send messages'
            }), 403
        
        # Validate content or image
        if not content and not image:
            return jsonify({
                'success': False,
                'message': 'Message content or image is required'
            }), 400
        
        # Handle image upload
        image_url = None
        if image:
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'community_images')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate unique filename
            filename = secure_filename(image.filename)
            timestamp = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{current_user}_{timestamp}_{filename}"
            filepath = os.path.join(upload_dir, unique_filename)
            
            # Save image
            image.save(filepath)
            image_url = f"/uploads/community_images/{unique_filename}"
        
        # Send message
        result = CommunityService.send_community_message(
            community_id=community_id,
            user_id=current_user,
            content=content,
            image_url=image_url
        )
        
        return jsonify(result), 200 if result.get('success') else 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/<int:community_id>/members', methods=['GET'])
@token_required
def get_community_members(current_user, community_id):
    """
    Get all members of a community
    Only members can view the member list
    """
    try:
        # Check if user is a member
        from community_models import CommunityMember
        membership = CommunityMember.query.filter_by(
            community_id=community_id,
            user_id=current_user,
            is_deleted=False
        ).first()
        
        if not membership:
            return jsonify({
                'success': False,
                'message': 'You must be a member to view members'
            }), 403
        
        # Get members
        members = CommunityService.get_community_members(community_id)
        
        return jsonify({
            'success': True,
            'members': members,
            'count': len(members)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# ============================================
# DELETE OPERATIONS
# ============================================

@app.route('/api/community/groups/<int:community_id>', methods=['DELETE'])
@token_required
def delete_community_group(current_user, community_id):
    """
    Delete a community group (soft delete)
    Only admins/creators can delete
    """
    try:
        result = CommunityService.delete_community(community_id, current_user)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 403
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/blogs/<int:post_id>', methods=['DELETE'])
@token_required
def delete_blog_post(current_user, post_id):
    """
    Delete a blog post (soft delete)
    Only the author can delete
    """
    try:
        result = CommunityService.delete_blog(post_id, current_user)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 403
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/community/feedback/<int:post_id>', methods=['DELETE'])
@token_required
def delete_feedback_post(current_user, post_id):
    """
    Delete a feedback post (soft delete)
    Only the author can delete
    """
    try:
        result = CommunityService.delete_feedback(post_id, current_user)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 403
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# Serve uploaded images
@app.route('/uploads/community_images/<filename>')
def serve_community_image(filename):
    """Serve uploaded community images"""
    try:
        from flask import send_from_directory
        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'community_images')
        return send_from_directory(upload_dir, filename)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Image not found'
        }), 404


@app.route('/api/community/notifications/<int:notification_id>', methods=['DELETE'])
@token_required
def delete_notification(current_user, notification_id):
    """Delete a single notification for the current user"""
    try:
        from community_models import Notification
        notif = Notification.query.filter_by(
            id=notification_id,
            user_id=current_user
        ).first()
        if not notif:
            return jsonify({'success': False, 'message': 'Notification not found'}), 404
        notif.is_deleted = True
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/community/conversations/<int:conversation_id>', methods=['DELETE'])
@token_required
def delete_conversation(current_user, conversation_id):
    """Soft-delete a conversation for the current user"""
    try:
        from community_models import Conversation
        conv = Conversation.query.filter_by(id=conversation_id).first()
        if not conv:
            return jsonify({'success': False, 'message': 'Conversation not found'}), 404
        if conv.user1_id != current_user and conv.user2_id != current_user:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        conv.is_deleted = True
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# ============================================
# EXPLORE MODULE BLUEPRINT
# ============================================
try:
    from explore.routes import explore_bp
    app.register_blueprint(explore_bp)

    # Apply rate limit: 30 requests/min per IP for all explore routes
    @explore_bp.before_request
    def explore_rate_limit():
        return limiter.limit("30 per minute")(lambda: None)()

    print("✓ Explore blueprint registered")
except Exception as _e:
    print(f"⚠ Explore blueprint not loaded: {_e}")

# ============================================
# RUN APPLICATION
# ============================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Flask Backend Server Starting...")
    print("="*60)
    print(f"📍 Backend URL: http://localhost:5000")
    print(f"🗄️  Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"🔐 JWT Secret: {'*' * 20}")
    print("="*60)
    print("\n✅ Server is ready! Waiting for requests...\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
