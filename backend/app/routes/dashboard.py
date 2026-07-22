from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.match_report import MatchReport
from app.models.resume import Resume
from app.services.profile_scanner import profile_scanner

bp = Blueprint('dashboard', __name__)

# In-memory storage for demo purposes
user_links = {
    "resume": None,
    "portfolio": None,
    "linkedin": None,
    "github": None,
    "leetcode": None
}

# Default Mock Match Report for seamless serverless/stateless demo capability
MOCK_MATCH_REPORT = {
    "company_name": "Google",
    "job_role": "Associate Software Engineer",
    "match_score": 85,
    "matched_skills": ["Python", "JavaScript", "React", "SQL", "Git"],
    "missing_skills": ["Docker", "Kubernetes", "AWS Cloud"],
    "resume_improvements": [
        "Include metrics for your AI Path Pilot project (e.g. reduced comparison time by 40%).",
        "Add more details about cloud deployment or Docker experience if any."
    ],
    "recommended_courses": [
        "Docker & Kubernetes Masterclass on Udemy",
        "AWS Cloud Practitioner Course on Coursera"
    ],
    "learning_roadmap": [
        "Day 1-3: Learn Docker containerization basics and write a Dockerfile.",
        "Day 4-7: Deploy a simple React + Flask app using Docker Compose.",
        "Day 8-15: Learn AWS ECS and RDS database setup.",
        "Day 16-30: Build a complete CI/CD pipeline with GitHub Actions."
    ],
    "should_apply": "YES",
    "reason": "You have a very strong frontend and API background matching Google's core stack. Bridging the cloud deployment skills will make your profile outstanding."
}

@bp.route('', methods=['GET'])
def get_dashboard_data():
    """Conforms to GET /api/dashboard endpoint."""
    user_id = 1
    
    # Try fetching the latest match report and resume from database
    report = MatchReport.query.filter_by(user_id=user_id).order_by(MatchReport.id.desc()).first()
    resume = Resume.query.filter_by(user_id=user_id).first()
    
    # Retrieve user links
    links_res = user_links.copy()
    if resume:
        links_res["resume"] = resume.filename

    # Base response payload
    response_data = {
        "links": links_res,
        "resume_score": resume.score if resume else 88,
        "career_readiness": int(resume.readiness) if (resume and resume.readiness and resume.readiness.isdigit()) else 85,
        "has_resume": resume is not None
    }

    # If database has a match report, return it. Otherwise, return mock match report.
    if report:
        response_data.update({
            "company_name": report.company_name,
            "job_role": report.job_role,
            "match_score": report.match_score,
            "matched_skills": report.matched_skills,
            "missing_skills": report.missing_skills,
            "resume_improvements": report.resume_improvements,
            "recommended_courses": report.recommended_courses,
            "learning_roadmap": report.learning_roadmap,
            "should_apply": report.should_apply,
            "reason": report.reason
        })
    else:
        response_data.update({
            "company_name": MOCK_MATCH_REPORT["company_name"],
            "job_role": MOCK_MATCH_REPORT["job_role"],
            "match_score": MOCK_MATCH_REPORT["match_score"],
            "matched_skills": MOCK_MATCH_REPORT["matched_skills"],
            "missing_skills": MOCK_MATCH_REPORT["missing_skills"],
            "resume_improvements": MOCK_MATCH_REPORT["resume_improvements"],
            "recommended_courses": MOCK_MATCH_REPORT["recommended_courses"],
            "learning_roadmap": MOCK_MATCH_REPORT["learning_roadmap"],
            "should_apply": MOCK_MATCH_REPORT["should_apply"],
            "reason": MOCK_MATCH_REPORT["reason"]
        })

    return jsonify(response_data), 200

@bp.route('/summary', methods=['GET'])
def get_summary():
    """Redirect /summary to the new full dashboard data payload."""
    return get_dashboard_data()

@bp.route('/links', methods=['GET'])
def get_links():
    user_id = 1
    resume = Resume.query.filter_by(user_id=user_id).first()
    links_res = user_links.copy()
    if resume:
        links_res["resume"] = resume.filename
    return jsonify(links_res), 200

@bp.route('/links', methods=['POST'])
def update_links():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400
        
    for key in user_links.keys():
        if key in data:
            user_links[key] = data[key]
            
    return jsonify({"message": "Links updated successfully", "links": user_links}), 200

@bp.route('/scan', methods=['POST'])
def scan_profiles():
    try:
        profile_scores = profile_scanner.scan_profiles(user_links)
        
        # Fetch Resume from DB (user_id = 1 for demo)
        resume_record = None
        try:
            user_id = 1
            resume_record = Resume.query.filter_by(user_id=user_id).first()
        except Exception as e:
            print(f"Skipping DB fetch due to ephemeral serverless reset: {e}")
            from app.extensions import db
            # Optional: recreate tables for future use in this container
            try:
                db.create_all()
            except:
                pass
        
        bio = ""
        skills = []
        
        if resume_record and resume_record.parsed_json:
            parsed_json = resume_record.parsed_json
            # In some database dialects, JSON may be returned as a string if not properly typed
            if isinstance(parsed_json, str):
                import json
                try:
                    parsed_json = json.loads(parsed_json)
                except:
                    parsed_json = {}
            bio = parsed_json.get("CareerObjective") or ""
            skills = parsed_json.get("TechnicalSkills") or []
            if not isinstance(skills, list):
                skills = []
                
        recommendations = profile_scanner.generate_recommendations(bio, skills)
        
        return jsonify({
            "scores": profile_scores,
            "recommendations": recommendations
        }), 200
    except Exception as general_err:
        print(f"Critical error in /scan: {general_err}")
        return jsonify({
            "scores": {"error": {"score": 0, "username": "Error"}},
            "recommendations": profile_scanner.generate_recommendations("", [])
        }), 200
