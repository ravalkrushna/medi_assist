from app.extension import db
from datetime import datetime

# class Patient(db.Model):
#     __tablename__ = 'patients'  # ✅ Now matches the actual PostgreSQL table

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password_hash = db.Column(db.String(256), nullable=False)
#     is_active = db.Column(db.Boolean, default=True)

#     queries = db.relationship('HealthQuery', backref='patient', lazy=True, cascade="all, delete-orphan")


# class HealthQuery(db.Model):
#     __tablename__ = 'health_queries'

#     id = db.Column(db.Integer, primary_key=True)
#     question = db.Column(db.Text, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)  # ✅ Correct FK target

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_user_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    queries = db.relationship('HealthQuery', backref='patient', lazy=True)

class HealthQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


