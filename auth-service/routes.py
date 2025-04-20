from flask import Blueprint, request, jsonify
from models import db, User
from utils import hash_password, verify_password
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,get_jwt

# Initialize Blueprint
auth_bp = Blueprint('auth', __name__)
# Admin-only decorator
def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"msg": "Admins only"}), 403
        return fn(*args, **kwargs)
    return wrapper

@auth_bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"msg": "Admins only"}), 403

    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "role": u.role,
        "blocked": u.is_blocked
    } for u in users])


# Register Route
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    email = data["email"]
    password = hash_password(data["password"])  # Hash the password
    gender = data.get("gender")
    age = data.get("age")
    role = data.get("role", "patient")

    # Check if the user already exists
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"message": "User already exists"}), 409

    # Create new user
    user = User(
        username=username,
        email=email,
        password=password,
        gender=gender,
        age=age,
        role=role
    )

    # Add and commit to the database
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Login Route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()

    if not user or not verify_password(data["password"], user.password):
        return jsonify({"message": "Invalid credentials"}), 401
    if user.is_blocked:
        return jsonify({"message": "Account is blocked"}), 403
    access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})

    # access_token = create_access_token(identity={"id": user.id, "role": user.role})
    return jsonify(access_token=access_token)



@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    claims=get_jwt()
    role=claims.get("role")
    return jsonify(message=f"Hello, {current_user}! {role}You have accessed a protected route.")