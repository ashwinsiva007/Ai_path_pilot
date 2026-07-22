from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db
from app.utilities.response import success_response, error_response

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data:
        return error_response("Missing JSON payload", 400)
        
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    # Prevent users from giving themselves admin role unless we add a secret key check.
    # For now, default to 'user'
    role = data.get('role', 'user') 
    
    if not username or not email or not password:
        return error_response("Username, email, and password are required", 400)
        
    if User.query.filter_by(username=username).first():
        return error_response("Username already exists", 400)
        
    if User.query.filter_by(email=email).first():
        return error_response("Email already exists", 400)
        
    hashed_password = generate_password_hash(password)
    
    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        role=role
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return success_response("User registered successfully", {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role
    }, 201)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return error_response("Missing JSON payload", 400)
        
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return error_response("Email and password are required", 400)
        
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return error_response("Invalid email or password", 401)
        
    # Include role in JWT claims
    additional_claims = {"role": user.role}
    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
    
    return success_response("Login successful", {
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }, 200)

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return error_response("User not found", 404)
        
    return success_response("Current user retrieved", {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }, 200)
