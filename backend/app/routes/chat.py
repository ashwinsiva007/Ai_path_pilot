from flask import Blueprint, jsonify, request
from app.utilities.response import success_response, error_response

bp = Blueprint('chat', __name__)

SYSTEM_CONTEXT = """You are an expert AI Career Coach and guide for students and young professionals.
You help with: job searching, resume writing, interview preparation, skill development, career planning,
hackathon strategies, internship hunting, and learning roadmaps.
Keep responses concise, practical, and encouraging. Format multi-step answers with numbered lists or bullet points."""

@bp.route('/message', methods=['POST'])
def chat_message():
    data = request.get_json(silent=True)
    if not data or 'message' not in data:
        return error_response("No message provided", 400)

    user_message = data['message'].strip()
    if not user_message:
        return error_response("Message cannot be empty", 400)

    try:
        from app.services.gemini_service import gemini_service
        prompt = f"{SYSTEM_CONTEXT}\n\nUser: {user_message}\nAssistant:"
        response_text = gemini_service.generate_content(prompt)
        return success_response("Response generated", {"response": response_text})
    except Exception as e:
        return error_response(f"AI service error: {str(e)}", 500)
