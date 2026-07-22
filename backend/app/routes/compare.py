import os
import urllib.request
import tempfile
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename
from app.utilities.response import success_response, error_response
from app.services.gemini_service import gemini_service
from app.routes.resume import extract_text_from_pdf, extract_text_from_docx, allowed_file

bp = Blueprint('compare', __name__)

def fetch_job_text(url: str) -> str:
    """Attempt to fetch plain text from a URL."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
            return html
    except Exception as e:
        print(f"Failed to fetch job URL {url}: {e}")
        return f"Job Link: {url}"

@bp.route('/match', methods=['POST'])
def match_resume_job():
    if 'resume' not in request.files:
        return error_response("No resume provided", 400)
    
    file = request.files['resume']
    job_link = request.form.get('jobLink', '')
    
    if file.filename == '':
        return error_response("No selected file", 400)
    
    if not job_link:
        return error_response("No job link provided", 400)
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = tempfile.gettempdir()
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        ext = filename.rsplit('.', 1)[1].lower()
        resume_text = ""
        try:
            if ext == 'pdf':
                resume_text = extract_text_from_pdf(filepath)
            elif ext == 'docx':
                resume_text = extract_text_from_docx(filepath)
        except Exception as e:
            return error_response(f"Failed to parse resume: {str(e)}", 500)
            
        job_text = fetch_job_text(job_link)
        
        try:
            result = gemini_service.compare_resume_to_job(resume_text, job_text)
            return success_response("Comparison successful", result)
        except Exception as e:
            return error_response(f"Failed to analyze fit: {str(e)}", 500)

    return error_response("Invalid file type", 400)
