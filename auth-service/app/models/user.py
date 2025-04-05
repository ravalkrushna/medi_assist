from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)                 # Full name
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=True)                       # Optional or Required
    gender = db.Column(db.String(10), nullable=True)                 # 'Male', 'Female', 'Other'
    role = db.Column(db.String(50), default="patient")               # patient, admin, doctor (future-proofing)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
