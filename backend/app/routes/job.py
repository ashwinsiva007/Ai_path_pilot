from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from app.models.resume import Resume
from app.models.match_report import MatchReport
from app.services.job_scraper import job_scraper
from app.services.job_parser import job_parser
from app.services.matching_service import matching_service
from app.services.skill_gap_service import skill_gap_service
from app.services.recommendation_service import recommendation_service
from app.services.roadmap_service import roadmap_service
from app.utilities.response import success_response, error_response

bp = Blueprint('job', __name__)

# Default Mock Resume Profile for seamless serverless/stateless demo capability
MOCK_RESUME_DATA = {
    "FullName": "Ashwin Siva",
    "EmailAddress": "ashwin@example.com",
    "PhoneNumber": "+91 98765 43210",
    "Skills": ["Python", "JavaScript", "React", "Node.js", "Express", "Flask", "SQL", "Git", "HTML", "CSS"],
    "TechnicalSkills": ["Python", "JavaScript", "React", "Flask", "SQLite", "REST APIs"],
    "SoftSkills": ["Communication", "Problem Solving", "Team Collaboration"],
    "Education": ["B.E. Computer Science and Engineering"],
    "Experience": ["Full Stack Developer Intern @ TechCorp (3 months)"],
    "Projects": [
        {
            "Title": "AI Path Pilot",
            "Description": "AI-powered career coaching and resume matching platform built with React and Flask.",
            "TechnologiesUsed": ["React", "Flask", "Gemini API", "SQLite"]
        }
    ],
    "Certifications": ["Google Cloud Digital Leader"],
    "Achievements": ["First Place in College Hackathon 2025"],
    "Interests": ["Artificial Intelligence", "Open Source Contribution"],
    "CareerDomain": "Software Engineering",
    "PreferredRole": "Full Stack Developer",
    "ResumeScore": 88,
    "CareerReadinessScore": 85,
    "raw_text": "Ashwin Siva. Software Engineer candidate with experience in Python, JavaScript, React, and Flask. Developed AI Path Pilot. B.E. CSE graduate."
}

@bp.route('/analyze', methods=['POST'])
def analyze_job():
    data = request.json or {}
    job_url = data.get('job_url', '')
    job_text = data.get('job_text', '')

    if not job_url and not job_text:
        return error_response("Please provide either a job_url or job_text.", 400)

    try:
        raw_text = job_text
        if job_url:
            raw_text = job_scraper.scrape_url(job_url)

        structured_job = job_parser.parse_job_description(raw_text)
        return success_response("Job description analyzed successfully.", structured_job)
    except Exception as e:
        return error_response(f"Failed to analyze job: {str(e)}", 500)

@bp.route('/match', methods=['POST'])
def match_job():
    data = request.json or {}
    job_url = data.get('job_url', '')
    job_text = data.get('job_text', '')

    # Associate with dummy user_id = 1
    user_id = 1
    
    # 1. Read Resume
    resume_record = Resume.query.filter_by(user_id=user_id).first()
    if resume_record and resume_record.parsed_json:
        resume_data = resume_record.parsed_json
    else:
        # Fallback to default mock resume if SQLite is empty
        resume_data = MOCK_RESUME_DATA

    if not job_url and not job_text:
        return error_response("Please provide either a job_url or job_text.", 400)

    try:
        # 3. Read Job URL or Job Description
        raw_job_text = job_text
        if job_url:
            raw_job_text = job_scraper.scrape_url(job_url)

        # 4. Extract Job Requirements
        structured_job = job_parser.parse_job_description(raw_job_text)

        # 5. Compare Resume vs Job & 6. Calculate Semantic Similarity
        matching_results = matching_service.evaluate_match(resume_data, structured_job)

        # 7. Detect Skill Gaps
        skill_gaps = skill_gap_service.detect_gaps(
            resume_skills=resume_data.get("Skills", []),
            job_skills=structured_job.get("RequiredSkills", []),
            preferred_skills=structured_job.get("PreferredSkills", [])
        )

        # 8. Generate Resume Improvements & 9. Generate AI Recommendation
        recommendations = recommendation_service.generate_recommendation(
            resume_data=resume_data,
            job_requirements=structured_job,
            matching_results=matching_results,
            skill_gaps=skill_gaps
        )

        # 10. Generate Learning Roadmap
        roadmap_data = roadmap_service.generate_roadmap_plan(
            missing_skills=skill_gaps.get("missing_skills", []),
            role=structured_job.get("JobRole", "Software Engineer")
        )

        # Build final response object conforming to Feature 11 response format
        final_report = {
            "resume_score": resume_data.get("ResumeScore", 80),
            "career_readiness": resume_data.get("CareerReadinessScore", 80),
            "match_score": matching_results.get("overall_match", 75),
            "matched_skills": skill_gaps.get("matched_skills", []),
            "missing_skills": skill_gaps.get("missing_skills", []),
            "resume_improvements": recommendations.get("resume_improvements", []),
            "recommended_courses": roadmap_data.get("recommended_courses", []),
            "learning_roadmap": roadmap_data.get("plan_7_day", []) + roadmap_data.get("plan_30_day", []),
            "should_apply": recommendations.get("should_apply", "MAYBE"),
            "reason": recommendations.get("reason", "Good match with a few skill gaps to address.")
        }

        # Store the report in SQLite MatchReport model
        report_record = MatchReport(
            user_id=user_id,
            company_name=structured_job.get("CompanyName", "Target Company"),
            job_role=structured_job.get("JobRole", "Target Role"),
            job_url=job_url,
            job_description=raw_job_text,
            resume_score=final_report["resume_score"],
            career_readiness=final_report["career_readiness"],
            match_score=final_report["match_score"],
            matched_skills=final_report["matched_skills"],
            missing_skills=final_report["missing_skills"],
            resume_improvements=final_report["resume_improvements"],
            recommended_courses=final_report["recommended_courses"],
            learning_roadmap=final_report["learning_roadmap"],
            should_apply=final_report["should_apply"],
            reason=final_report["reason"]
        )

        # Clear older reports for the same user to keep the database tidy
        MatchReport.query.filter_by(user_id=user_id).delete()
        db.session.add(report_record)
        db.session.commit()

        return jsonify(final_report)

    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to match candidate with job: {str(e)}", 500)

@bp.route('/report', methods=['GET'])
def get_report():
    user_id = 1
    report = MatchReport.query.filter_by(user_id=user_id).order_by(MatchReport.id.desc()).first()
    if not report:
        # Fallback to realistic mock report if SQLite state was cleared by Vercel serverless
        from app.routes.dashboard import MOCK_MATCH_REPORT
        return success_response("Match report retrieved successfully.", {
            "id": 1,
            "company_name": MOCK_MATCH_REPORT["company_name"],
            "job_role": MOCK_MATCH_REPORT["job_role"],
            "job_url": "",
            "resume_score": 88,
            "career_readiness": 85,
            "match_score": MOCK_MATCH_REPORT["match_score"],
            "matched_skills": MOCK_MATCH_REPORT["matched_skills"],
            "missing_skills": MOCK_MATCH_REPORT["missing_skills"],
            "resume_improvements": MOCK_MATCH_REPORT["resume_improvements"],
            "recommended_courses": MOCK_MATCH_REPORT["recommended_courses"],
            "learning_roadmap": MOCK_MATCH_REPORT["learning_roadmap"],
            "should_apply": MOCK_MATCH_REPORT["should_apply"],
            "reason": MOCK_MATCH_REPORT["reason"],
            "created_at": "2026-07-22T00:00:00Z"
        })

    return success_response("Match report retrieved successfully.", {
        "id": report.id,
        "company_name": report.company_name,
        "job_role": report.job_role,
        "job_url": report.job_url,
        "resume_score": report.resume_score,
        "career_readiness": report.career_readiness,
        "match_score": report.match_score,
        "matched_skills": report.matched_skills,
        "missing_skills": report.missing_skills,
        "resume_improvements": report.resume_improvements,
        "recommended_courses": report.recommended_courses,
        "learning_roadmap": report.learning_roadmap,
        "should_apply": report.should_apply,
        "reason": report.reason,
        "created_at": report.created_at.isoformat()
    })
