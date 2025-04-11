from functools import wraps
from flask import request, jsonify
from app.utils.jwt_handler import decode_token

# from app.utils.decorators import login_required, role_required             <<use this import to use decoraters

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Authorization token missing"}), 401

        token = auth_header.split(" ")[1]
        payload = decode_token(token)
        if payload is None:
            return jsonify({"message": "Invalid or expired token"}), 401

        # Attach user info to request
        request.user_id = payload.get("user_id")
        request.role = payload.get("role")

        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"message": "Authorization token missing"}), 401

            token = auth_header.split(" ")[1]
            payload = decode_token(token)
            if payload is None:
                return jsonify({"message": "Invalid or expired token"}), 401

            if payload.get('role') != required_role:
                return jsonify({"message": "Access forbidden: insufficient permissions"}), 403

            request.user = payload
            return f(*args, **kwargs)
        return decorated_function
    return decorator
