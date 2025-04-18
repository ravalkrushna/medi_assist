from flask import Flask
from app.extension import db, jwt
from app.routes.adminroutes import admin_bp
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions here only
    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        db.create_all()

    return app
