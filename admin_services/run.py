from app import create_app
from app.extension import db

app = create_app()

if __name__ == "__main__":
    # No need to create an AdminUser now that it's handled by auth-service
    app.run(debug=True, port=5003, host="0.0.0.0")
