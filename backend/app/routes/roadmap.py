from flask import Blueprint, jsonify, request
from app.utilities.response import success_response, error_response
from app.services.gemini_service import gemini_service

bp = Blueprint('roadmap', __name__)

@bp.route('/generate', methods=['POST'])
def generate_roadmap():
    data = request.json or {}
    skills = data.get('skills', [])
    
    if not skills:
        return error_response("No skills provided to generate a roadmap", 400)
        
    try:
        result = gemini_service.generate_roadmap(skills)
        return success_response("Roadmap generated successfully", result)
    except Exception as e:
        return error_response(f"Failed to generate roadmap: {str(e)}", 500)
