from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.patientmodel import Patient, HealthQuery
from app.extension import db

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

@patient_bp.route('/create_profile', methods=['POST'])
def create_patient_profile():
    data = request.get_json()
    auth_user_id = data.get("auth_user_id")
    name = data.get("name")
    email = data.get("email")

    if not all([auth_user_id, name, email]):
        return jsonify(msg="Missing required fields"), 400

    if Patient.query.filter_by(auth_user_id=auth_user_id).first():
        return jsonify(msg="Profile already exists"), 409

    patient = Patient(auth_user_id=auth_user_id, name=name, email=email)
    db.session.add(patient)
    db.session.commit()

    return jsonify(msg="Patient profile created successfully"), 201

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
