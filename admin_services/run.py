from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True,port=5001)


from app.extension import db
from app.models.usermodel import AdminUser

with app.app_context():
    admin = AdminUser(username="admin")
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
    print("Admin user created.")
