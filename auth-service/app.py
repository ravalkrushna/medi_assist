import os
from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from routes import auth_bp
from models import db

# Load environment variables from .env file
load_dotenv()

def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # App config
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:postgres@db:5432/auth_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    with app.app_context():
        db.create_all()

    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Test route
    @app.route('/')
    def home():
        return "Welcome to Auth Service!"

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
