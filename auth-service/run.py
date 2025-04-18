

from app import create_app, db
from flask import Flask

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(port=5001,debug=True, host="0.0.0.0")
