from flask import Blueprint, render_template, request, jsonify, redirect
from app.services.auth_service import register_user, login_user, verify_token, logout_user, reset_password
from app import db
from app.utils.jwt_handler import generate_token
from app.utils.decorators import login_required

auth_bp = Blueprint("auth", __name__)

# @auth_bp.route('/auth', methods=['GET'])
# def show_auth_form():
#     return render_template('auth_form.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data.get('name'), data.get('email'), data.get('password'), data.get('age'), data.get('gender'))

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response = login_user(data.get('email'), data.get('password'))
    if response.status_code == 200:
        payload = response.json
        role = payload.get("role")
        if role == "admin":
            return redirect("http://localhost:5003/dashboard")  # admin-service
        else:
            return redirect("http://localhost:5002/chatbot")     # patient-service
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route("/verify", methods=["POST"])
def verify():
    return verify_token(request)

@auth_bp.route('/me', methods=['GET'])
def me():
    user_info = verify_token(request).json  # assuming payload returned
    return jsonify(user_info)

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    return logout_user(request)

@auth_bp.route('/reset-password', methods=['POST'])
@login_required
def reset_password_route():
    data = request.get_json()
    user_id = request.user_id  # assuming you set this in your @login_required decorator
    return reset_password(user_id, data.get('old_password'), data.get('new_password'))
