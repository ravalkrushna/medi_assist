from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from app.models.patientmodel import Patient, HealthQuery
from app.extension import db

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')


# ✅ Register a new patient
@patient_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify(msg="All fields are required"), 400

    if Patient.query.filter_by(email=email).first():
        return jsonify(msg="Email already registered"), 409

    hashed_password = generate_password_hash(password)
    new_patient = Patient(name=name, email=email, password_hash=hashed_password)
    db.session.add(new_patient)
    db.session.commit()

    return jsonify(msg="Patient registered successfully"), 201


# ✅ Login and get access token
@patient_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    patient = Patient.query.filter_by(email=email).first()
    if not patient or not check_password_hash(patient.password_hash, password):
        return jsonify(msg="Invalid credentials"), 401

    access_token = create_access_token(identity=str(patient.id))
    return jsonify(access_token=access_token), 200


# ✅ View profile (GET)
@patient_bp.route('/profile', methods=['GET'])
@jwt_required()
def view_profile():
    patient_id = int(get_jwt_identity())
    patient = Patient.query.get(patient_id)

    if not patient:
        return jsonify(msg="Patient not found"), 404

    return jsonify({
        "id": patient.id,
        "name": patient.name,
        "email": patient.email,
        "is_active": patient.is_active
    })


# ✅ Update profile (PUT)
@patient_bp.route('/profile/<int:id>', methods=['PUT'])
@jwt_required()
def update_profile(id):
    current_patient_id = int(get_jwt_identity())
    if current_patient_id != id:
        return jsonify(msg="Unauthorized access"), 403

    patient = Patient.query.get(id)
    if not patient:
        return jsonify(msg="Patient not found"), 404

    data = request.get_json()
    new_name = data.get("name")
    new_email = data.get("email")

    if new_name:
        patient.name = new_name
    if new_email:
        if Patient.query.filter(Patient.email == new_email, Patient.id != id).first():
            return jsonify(msg="Email already taken"), 409
        patient.email = new_email

    db.session.commit()
    return jsonify(msg="Profile updated successfully"), 200


# ✅ Submit a health query
@patient_bp.route('/query', methods=['POST'])
@jwt_required()
def submit_query():
    patient_id = int(get_jwt_identity())
    patient = Patient.query.get(patient_id)

    if not patient:
        return jsonify(msg="Patient not found"), 404

    data = request.get_json()
    question = data.get('question')

    if not question or not isinstance(question, str):
        return jsonify(msg="Question field is required and must be a string"), 400

    query = HealthQuery(question=question, patient_id=patient.id)
    db.session.add(query)
    db.session.commit()

    return jsonify(msg="Health query submitted successfully"), 201


# ✅ Get all queries submitted by logged-in patient
@patient_bp.route('/my_queries', methods=['GET'])
@jwt_required()
def get_my_queries():
    patient_id = int(get_jwt_identity())
    patient = Patient.query.get(patient_id)

    if not patient:
        return jsonify(msg="Patient not found"), 404

    queries = HealthQuery.query.filter_by(patient_id=patient.id).order_by(HealthQuery.timestamp.desc()).all()

    return jsonify([
        {
            "id": q.id,
            "question": q.question,
            "timestamp": q.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for q in queries
    ])
