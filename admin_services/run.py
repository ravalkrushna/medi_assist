from app import create_app
from app.extension import db
from app.models.usermodel import AdminUser

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        if not AdminUser.query.filter_by(username="admin").first():
            admin = AdminUser(username="admin")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")
    app.run(debug=True, port=5001)
