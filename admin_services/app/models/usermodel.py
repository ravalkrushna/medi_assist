from app.extension import db
from werkzeug.security import check_password_hash, generate_password_hash

class AdminUser(db.Model):
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def authenticate(username, password):
    user = AdminUser.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None
