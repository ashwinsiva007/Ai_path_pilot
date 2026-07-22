from flask import Blueprint, jsonify, request
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

@bp.route('/summary', methods=['GET'])
def get_summary():
    return jsonify({"message": "Dashboard summary stub"}), 200

@bp.route('/links', methods=['GET'])
def get_links():
    return jsonify(user_links), 200

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

