from flask import Blueprint, request, jsonify
from models import db, User

patient_bp = Blueprint('patient_bp', __name__)

# View patient profile
@patient_bp.route('/profile/<int:patient_id>', methods=['GET'])
def view_profile(patient_id):
    patient = User.query.get(patient_id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404

    return jsonify({
        'id': patient.id,
        'name': patient.username,
        'age': patient.age,
        'gender': patient.gender,
        'email': patient.email
    }), 200


# Update patient profile
@patient_bp.route('/profile/<int:patient_id>', methods=['PUT'])
def update_profile(patient_id):
    patient = User.query.get(patient_id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404

    data = request.get_json()
    patient.username = data.get('name', patient.username)
    patient.age = data.get('age', patient.age)
    patient.gender = data.get('gender', patient.gender)
    # Don't allow email updates if that's handled by auth

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200
