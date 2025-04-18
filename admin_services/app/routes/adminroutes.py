from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required

from app.models.patientmodel import Patient
from app.extension import db

admin_bp = Blueprint("admin", __name__)

# Dashboard
@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    return jsonify({"msg": "Welcome to the admin dashboard!"})


# Get all patients
@admin_bp.route("/patients", methods=["GET"])
@jwt_required()
def get_patients():
    patients = Patient.query.all()
    return jsonify([
        {"id": p.id, "name": p.name, "email": p.email, "is_active": p.is_active}
        for p in patients
    ])


# Add a patient (Create)
@admin_bp.route("/add_patient", methods=["POST"])
@jwt_required()
def add_patient():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not all([name, email]):
        return jsonify(msg="Missing patient data"), 400

    patient = Patient(name=name, email=email)
    db.session.add(patient)
    db.session.commit()

    return jsonify(msg="Patient added successfully"), 200


# Update patient by ID
@admin_bp.route("/patients/<int:patient_id>", methods=["PUT"])
@jwt_required()
def update_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify(msg="Patient not found"), 404

    data = request.get_json()
    patient.name = data.get("name", patient.name)
    patient.email = data.get("email", patient.email)
    db.session.commit()

    return jsonify(msg="Patient updated successfully")


# Delete patient by ID
@admin_bp.route("/patients/<int:patient_id>", methods=["DELETE"])
@jwt_required()
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify(msg="Patient not found"), 404

    db.session.delete(patient)
    db.session.commit()
    return jsonify(msg="Patient deleted successfully")
