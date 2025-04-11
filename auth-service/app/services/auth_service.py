

from app.models.user import User
from app import db
from app.utils.jwt_handler import generate_token, decode_token
from werkzeug.security import check_password_hash
from flask import jsonify

def register_user(name, email, password, age, gender):
    if not all([name, email, password, age, gender]):
        return {"message": "All fields are required"}, 400

    if User.query.filter_by(email=email).first():
        return {"message": "Email already registered"}, 400

    new_user = User(name=name, email=email, age=age, gender=gender)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201
def login_user(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = generate_token(user.id, user.role)
    return jsonify({
        "token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200

def verify_token(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Token missing"}), 401

    token = auth_header.split(" ")[1]
    payload = decode_token(token)
    if payload is None:
        return jsonify({"message": "Invalid or expired token"}), 401

    return jsonify({"user_id": payload["user_id"], "role": payload["role"]}), 200


def logout_user(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Token missing"}), 401

    # Optional: Add token to blacklist here if you're implementing that

    return jsonify({"message": "Logout successful"}), 200

def reset_password(user_id, old_password, new_password):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.check_password(old_password):
        return jsonify({"message": "Incorrect current password"}), 401

    user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "Password reset successful"}), 200
