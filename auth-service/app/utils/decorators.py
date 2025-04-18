from functools import wraps
from flask import request, jsonify
from app.utils.jwt_handler import decode_token

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Token missing"}), 401

        token = auth_header.split(" ")[1]
        payload = decode_token(token)
        if payload is None:
            return jsonify({"message": "Invalid or expired token"}), 401

        request.user_id = payload["user_id"]
        request.user_role = payload["role"]
        return f(*args, **kwargs)
    return decorated_function
