from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user, verify_token,logout_user,reset_password
from app.models.user import User
from app.utils.decorators import login_required, role_required
from app import db
from app.utils.jwt_handler import generate_token


from werkzeug.security import check_password_hash


auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data.get('name'), data.get('email'), data.get('password'),data.get('age'),data.get('gender'))

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data.get('email'), data.get('password'))

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



