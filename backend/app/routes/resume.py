import os
import pdfplumber
import docx
import tempfile
from werkzeug.utils import secure_filename
from flask import Blueprint, request, current_app
from app.utilities.response import success_response, error_response
from app.services.gemini_service import gemini_service
from app.extensions import db
from app.models.resume import Resume
from app.models.user import User

bp = Blueprint('resume', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])

@bp.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return error_response("No file part in the request", 400)
    
    file = request.files['file']
    if file.filename == '':
        return error_response("No selected file", 400)
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        upload_folder = tempfile.gettempdir()
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        try:
            from app.services.resume_parser import resume_parser
            structured_data = resume_parser.parse_resume(filepath, filename)
            
            # Associate with a dummy user for now (user_id = 1)
            user_id = 1
            user = User.query.get(user_id)
            if not user:
                user = User(id=user_id, username='testuser', email='test@example.com', password_hash='mock')
                db.session.add(user)
                db.session.commit()
                
            # Replace previous AI profile if exists
            resume_record = Resume.query.filter_by(user_id=user_id).first()
            if resume_record:
                resume_record.filename = filename
                resume_record.parsed_json = structured_data
                resume_record.score = float(structured_data.get("ResumeScore", 0))
                resume_record.readiness = str(structured_data.get("CareerReadinessScore", 0))
            else:
                resume_record = Resume(
                    user_id=user_id, 
                    filename=filename, 
                    parsed_json=structured_data,
                    score=float(structured_data.get("ResumeScore", 0)),
                    readiness=str(structured_data.get("CareerReadinessScore", 0))
                )
                db.session.add(resume_record)
                
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            return error_response(f"Failed to parse file: {str(e)}", 500)
            
        # Return success with the structured data for testing/UI details view
        return success_response("Resume analyzed successfully.", structured_data)
        
    return error_response("File type not allowed. Please upload PDF or DOCX.", 400)

@bp.route('/analyze', methods=['GET'])
def analyze_resume():
    return success_response("Analyze resume stub")

@bp.route('/details', methods=['GET'])
def get_resume_details():
    try:
        # Assume user_id = 1 for now
        user_id = 1
        resume_record = Resume.query.filter_by(user_id=user_id).first()
        
        if not resume_record or not resume_record.parsed_json:
            return error_response("No resume found for this user.", 404)
            
        return success_response("Resume details retrieved.", resume_record.parsed_json)
        
    except Exception as e:
        return error_response(f"Failed to retrieve resume details: {str(e)}", 500)
