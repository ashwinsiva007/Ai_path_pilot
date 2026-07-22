from app.extensions import db
from datetime import datetime, timezone

class MatchReport(db.Model):
    __tablename__ = 'match_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(200))
    job_role = db.Column(db.String(200))
    job_url = db.Column(db.String(500))
    job_description = db.Column(db.Text)
    
    # Scores
    resume_score = db.Column(db.Integer)
    career_readiness = db.Column(db.Integer)
    match_score = db.Column(db.Integer)
    
    # Matching elements stored as JSON
    matched_skills = db.Column(db.JSON)
    missing_skills = db.Column(db.JSON)
    resume_improvements = db.Column(db.JSON)
    recommended_courses = db.Column(db.JSON)
    learning_roadmap = db.Column(db.JSON)
    
    # Recommendations
    should_apply = db.Column(db.String(20))
    reason = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationship
    user = db.relationship('User', backref=db.backref('match_reports', cascade="all, delete-orphan"))
