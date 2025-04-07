from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from app.models.usermodel import authenticate
from app.models.patientmodel import Patient
from app.extension import db

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = authenticate(username, password)
    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    return jsonify({"msg": "Welcome to the admin dashboard!"})


@admin_bp.route("/patients", methods=["GET"])
@jwt_required()
def get_patients():
    patients = Patient.query.all()
    return jsonify([
        {"id": p.id, "name": p.name, "email": p.email, "is_active": p.is_active}
        for p in patients
    ])
