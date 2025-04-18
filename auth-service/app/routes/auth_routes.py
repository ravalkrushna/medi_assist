from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user, verify_token, logout_user, reset_password
from app.utils.decorators import login_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data)
    return register_user(data.get('name'), data.get('email'), data.get('password'), data.get('age'), data.get('gender'))

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response, status = login_user(data.get('email'), data.get('password'))
    if status == 200:
        payload = response.get_json()
        role = payload.get("user", {}).get("role")
        redirect_url = "http://localhost:5003/dashboard" if role == "admin" else "http://localhost:5002/chatbot"
        return jsonify({
            "redirect": redirect_url,
            "token": payload.get("token"),
            "user": payload.get("user")
        }), 200
    else:
        return response, status

@auth_bp.route("/verify", methods=["POST"])
def verify():
    return verify_token(request)

@auth_bp.route('/me', methods=['GET'])
def me():
    response, status = verify_token(request)
    return response, status

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    return logout_user(request)

@auth_bp.route('/reset-password', methods=['POST'])
@login_required
def reset_password_route():
    data = request.get_json()
    user_id = request.user_id
    return reset_password(user_id, data.get('old_password'), data.get('new_password'))
