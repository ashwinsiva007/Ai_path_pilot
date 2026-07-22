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

@bp.route('', methods=['GET'])
def get_dashboard_data():
    """Conforms to GET /api/dashboard endpoint."""
    user_id = 1
    
    # Try fetching the latest match report from database
    report = MatchReport.query.filter_by(user_id=user_id).order_by(MatchReport.id.desc()).first()
    resume = Resume.query.filter_by(user_id=user_id).first()
    
    # Retrieve user links
    links_res = user_links.copy()
    if resume:
        links_res["resume"] = resume.filename

    response_data = {
        "links": links_res,
        "resume_score": resume.score if resume else None,
        "career_readiness": int(resume.readiness) if (resume and resume.readiness and resume.readiness.isdigit()) else None,
        "has_resume": resume is not None
    }

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
        # Fallback empty metrics structure
        response_data.update({
            "company_name": None,
            "job_role": None,
            "match_score": None,
            "matched_skills": [],
            "missing_skills": [],
            "resume_improvements": [],
            "recommended_courses": [],
            "learning_roadmap": [],
            "should_apply": None,
            "reason": None
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
    profile_scores = profile_scanner.scan_profiles(user_links)
    recommendations = profile_scanner.generate_recommendations(user_links, profile_scores)
    
    return jsonify({
        "scores": profile_scores,
        "recommendations": recommendations
    }), 200
