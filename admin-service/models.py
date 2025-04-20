from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):  # Can share schema with auth-service if needed
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    role = db.Column(db.String(20), default="patient")
    is_blocked = db.Column(db.Boolean, default=False)
