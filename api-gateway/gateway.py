from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests

app = Flask(__name__)
ADMIN_URL = "http://admin-service:5002"
AUTH_URL="http://auth-service:5001"
# Gateway renders the auth_form.html at root or /register /login GET
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET'])
@app.route('/login', methods=['GET'])
def auth_page():
    return render_template('auth_form.html')


# Register POST - Proxy to auth-service
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    try:
        res = requests.post('http://auth-service:5001/auth/register', json=data)
        return jsonify(res.json()), res.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500


# Login POST - Proxy to auth-service
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    try:
        res = requests.post('http://auth-service:5001/auth/login', json=data)
        return jsonify(res.json()), res.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500
    
    

@app.route("/chatbot")
def chatbot():
    return render_template("index.html")  # Final landing page after success


# existing home/auth routes...

# Admin dashboard
@app.route("/admin", methods=["GET"])
def admin_dashboard():
    return render_template("admin.html")

@app.route("/admin/patients", methods=["GET"])
def proxy_patient_users():
    token = request.headers.get("Authorization")
    resp = requests.get("http://auth-service:5001/auth/users", headers={"Authorization": token})
    return (resp.content, resp.status_code, resp.headers.items())



# ✅ Block a user (change method to PUT and update URL)
@app.route("/admin/patients/<int:uid>/block", methods=["PUT"])
def proxy_block(uid):
    token = request.headers.get("Authorization")
    resp = requests.post(f"{ADMIN_URL}/admin/block/{uid}", headers={"Authorization": token})
    return (resp.content, resp.status_code, resp.headers.items())

# ✅ Unblock a user (change method to PUT and update URL)
@app.route("/admin/patients/<int:uid>/unblock", methods=["PUT"])
def proxy_unblock(uid):
    token = request.headers.get("Authorization")
    resp = requests.post(f"{ADMIN_URL}/admin/unblock/{uid}", headers={"Authorization": token})
    return (resp.content, resp.status_code, resp.headers.items())
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
