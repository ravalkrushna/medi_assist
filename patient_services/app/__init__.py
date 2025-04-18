from flask import Flask
from app.extension import db, jwt
from app.routes.patientroutes import patient_bp
from app.config import Config  # Import Config class

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Use config from the config file

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(patient_bp)

    with app.app_context():
        db.create_all()

    return app
